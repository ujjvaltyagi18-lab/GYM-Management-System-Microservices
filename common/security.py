from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from jose import jwt, JWTError
from passlib.context import CryptContext


SECRET_KEY = "Tyagi"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


security = HTTPBearer()


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


# Temporary blacklist
# Production me Redis/database use kare
BLACKLISTED_TOKENS = set()



def hash_password(password: str):
    return pwd_context.hash(password)



def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(
        password,
        hashed_password
    )



def create_access_token(data: dict):

    payload = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload.update({
        "exp": expire
    })

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )



def decode_token(token: str):

    if token in BLACKLISTED_TOKENS:
        raise HTTPException(
            status_code=401,
            detail="Token has been revoked"
        )

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload


    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )



def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):

    token = credentials.credentials

    payload = decode_token(token)

    return {
        "id": payload.get("sub"),
        "email": payload.get("email")
    }



def logout_token(token: str):

    BLACKLISTED_TOKENS.add(token)

    return {
        "message": "Logout successful"
    }
