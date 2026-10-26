from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlmodel import Session, select
from model import Address, Schedule, Rollcode, Members
from database import get_session
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from sqlalchemy import or_
from fastapi.security import HTTPBearer, OAuth2PasswordRequestForm, HTTPAuthorizationCredentials
import sys
import os

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)
from jose import jwt, JWTError

security = HTTPBearer()
SECRET_KEY = "Tyagi"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60




app = FastAPI(
    title="Auth Service",
    description="Authentication and user management service",
    version="1.0.0",
    root_path="/api/auth"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BLACKLISTED_TOKENS = set()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session),
):
    token = credentials.credentials

    if token in BLACKLISTED_TOKENS:
        raise HTTPException(
            status_code=401,
            detail="Token has been revoked. Please login again."
        )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        user = session.get(Members, int(user_id))

        if not user:
            raise HTTPException(
                status_code=401,
                detail="User not found"
            )

        return user

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )


class SignupRequest(BaseModel):
    username: str
    first_name: str
    last_name: str
    phone: str
    email: str
    password: str


class LoginRequest(BaseModel):
    username_or_email: str
    password: str


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "auth-service"}

@app.get("/")
def root():
    """Root endpoint"""
    return {"message": "Welcome to Auth Service", "version": "1.0.0"}


@app.post("/address/")
def create_address(
    address: Address,
    current_user=Depends(get_current_user),
    session: Session = Depends(get_session)
):
    session.add(address)
    session.commit()
    session.refresh(address)
    return address



@app.get("/address/")
def get_all_address(
    current_user=Depends(get_current_user),
    session: Session = Depends(get_session)
):
    return session.exec(select(Address)).all()



@app.get("/address/{address_id}")
def get_address_by_id(address_id: int, session: Session=Depends(get_session)):
  address=session.get(Address, address_id)
  return address


@app.delete("/address/", status_code=204)
def delete_all_address(session: Session=Depends(get_session)):
  address=session.exec(select(Address)).all()
  for add in address:
    session.delete(add)
    session.commit()
    return{"detail": "all address deleted"}
  

@app.delete("/address/{address_id}", status_code=204)
def delete_address_by_id(address_id: int, session: Session=Depends(get_session)):
  address=session.get(Address, address_id)
  if not address:
    raise HTTPException(status_code=404, detail="address not found")
  session.delete(address)
  session.commit()
  return{"detail": f"address {address_id} delete"}


@app.put("/address/")
def update_address(data: Address, session: Session=Depends(get_session)):
  address=session.exec(select(Address)).all()
  if not address:
    raise HTTPException(status_code=404, detail="address not found")
  update_data = data.dict(exclude_unset=True)
  for a in address:
    for key, value in update_data.items():
      setattr(a, key, value)
    session.commit()
    for a in address:
        session.refresh(a)
    return a
  

@app.put("/address/{address_id}")
def update_address_by_id(address_id: int, data: Address, session: Session=Depends(get_session)):
  address=session.get(Address, address_id)
  if not address:
    raise HTTPException(status_code=404, detail="address not found")
  for key, value in data.dict(exclude_unset=True):
    setattr(address, key, value)
    session.commit()
    session.refresh(address)
    return address




@app.post("/schedule/")
def create_schedule(schedule: Schedule, session: Session=Depends(get_session)):
  session.add(schedule)
  session.commit()
  session.refresh(schedule)
  return schedule


@app.get("/schedule/")
def get_all_schedule(
   current_user=Depends(get_current_user),
   session:Session=Depends(get_session)
):
   return session.exec(select(Schedule)).all()

@app.get("/schedule/{schedule_id}")
def get_schedule_by_id(schedule_id: int, session: Session=Depends(get_session)):
  schedule=session.get(Schedule, schedule_id)
  return schedule


@app.delete("/schedule/", status_code=204)
def delete_all_schedule(session: Session=Depends(get_session)):
  schedule=session.exec(select(Schedule)).all()
  for sch in schedule:
    session.delete(sch)
    session.commit()
    return{"detail": "all schedule deleted"}
  

@app.delete("/schedule/{schedule_id}", status_code=204)
def delete_schedule_by_id(schedule_id: int, session: Session=Depends(get_session)):
  schedule=session.get(Schedule, schedule_id)
  if not schedule:
    raise HTTPException(status_code=404, detail="schedule not found")
  session.delete(schedule)
  session.commit()
  return{"detail": f"schedule {schedule_id} deleted"}


@app.put("/schedule/")
def update_schedule(data: Schedule, session: Session=Depends(get_session)):
  schedule=session.exec(select(Schedule)).all()
  if not schedule:
    raise HTTPException(status_code=404, detail="schedule not found")
  update_data = data.dict(exclude_unset=True)
  for s in schedule:
    for key, value in update_data.items():
      setattr(s, key, value)
    session.commit()
    for s in schedule:
        session.refresh(s)
    return s
  

@app.put("/schedule/{schedule_id}")
def update_schedule_by_id(schedule_id: int, data: Schedule, session: Session=Depends(get_session)):
  schedule=session.get(Schedule, schedule_id)
  if not schedule:
    raise HTTPException(status_code=404, detail="schedule not found")
  for key, value in data.dict(exclude_unset=True):
    setattr(schedule, key, value)
    session.commit()
    session.refresh(schedule)
    return schedule




@app.post("/rollcode/")
def create_rollcode(rollcode: Rollcode, session: Session=Depends(get_session)):
  session.add(rollcode)
  session.commit()
  session.refresh(rollcode)
  return rollcode


@app.get("/rollcode/")
def get_all_rollcode(
   current_user=Depends(get_current_user),
   session:Session=Depends(get_session)
):
   return session.exec(select(Rollcode)).all()


@app.get("/rollcode/{rollcode_id}")
def get_rollcode_by_id(rollcode_id: int, session: Session=Depends(get_session)):
  rollcode=session.get(Rollcode, rollcode_id)
  return rollcode


@app.delete("/rollcode/", status_code=204)
def delete_all_rollcode(session: Session=Depends(get_session)):
  rollcode=session.exec(select(Rollcode)).all()
  for r in rollcode:
    session.delete(r)
    session.commit()
    return{"detail": "all rollcode deleted"}
  

@app.delete("/rollcode/{rollcode_id}", status_code=204)
def delete_rollcode_by_id(rollcode_id: int, session: Session=Depends(get_session)):
  rollcode=session.get(Rollcode, rollcode_id)
  if not rollcode:
    raise HTTPException(status_code=404, detail="rollcode not found")
  session.delete(rollcode)
  session.commit()
  return{"detail": f"rollcode {rollcode_id} deleted"}


@app.put("/rollcode/")
def update_rollcode(data: Rollcode, session: Session=Depends(get_session)):
  rollcode=session.exec(select(Rollcode)).all()
  if not rollcode:
    raise HTTPException(status_code=404, detail="rollcode not found")
  update_data = data.dict(exclude_unset=True)
  for r in rollcode:
    for key, value in update_data.items():
      setattr(r, key, value)
    session.commit()
    for r in rollcode:
        session.refresh(r)
    return r
  

@app.put("/rollcode/{rollcode_id}")
def update_rollcode_by_id(rollcode_id: int, data: Rollcode, session: Session=Depends(get_session)):
  rollcode=session.get(Rollcode, rollcode_id)
  if not rollcode:
    raise HTTPException(status_code=404, detail="rollcode not found")
  for key, value in data.dict(exclude_unset=True):
    setattr(rollcode, key, value)
    session.commit()
    session.refresh(rollcode)
    return rollcode
  
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=60)

    to_encode.update({
        "exp": expire
    })

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

  
@app.post("/signup")
def signup(request: SignupRequest,
           session: Session = Depends(get_session)):

    user = session.exec(
        select(Members).where(
            or_(
                Members.username == request.username,
                Members.email == request.email
            )
        )
    ).first()

    if user:

        raise HTTPException(
            status_code=400,
            detail="User already exists"
        )

    new_user = Members(

        username=request.username,
        first_name=request.first_name,
        last_name=request.last_name,
        phone=request.phone,
        email=request.email,
        password=hash_password(request.password)

    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return {
        "message": "Signup successful"
    }




@app.post("/members/")
def create_members(member: Members, session: Session=Depends(get_session)):
  session.add(member)
  session.commit()
  session.refresh(member)
  return member


@app.get("/members/")
def get_all_members(
    current_user=Depends(get_current_user),
    session: Session = Depends(get_session)
):
    return session.exec(select(Members)).all()




@app.get("/members/{member_id}")
def get_by_member_id(member_id: int, session: Session=Depends(get_session)):
  member=session.get(Members, member_id)
  return member


@app.delete("/members/", status_code=204)
def delete_all_members(session: Session=Depends(get_session)):
  member=session.exec(select(Members)).all()
  for Mem in member:
    session.delete(Mem)
    session.commit()
    return{"detail":"all members deleted"}
  

@app.delete("/members/{member_id}", status_code=204)
def delete_by_member_id(member_id: int, session: Session=Depends(get_session)):
  member=session.get(Members, member_id)
  if not member:
    raise HTTPException(status_code=404, detail="member not found")
  session.delete(member)
  session.commit()
  return{"detail": f"member {member_id} deleted"}


@app.put("/members/")
def update_member(data: Members, session: Session=Depends(get_session)):
  member=session.exec(select(Members)).all()
  if not member:
    raise HTTPException(status_code=404, detail="member not found")
  update_data=data.dict(exclude_unset=True)
  for M in member:
    for key, value in update_data.items():
      setattr(M, key, value)
      session.commit()
    for M in member:
      session.refresh(M)
      return M
    

@app.put("/members/{member_id}")
def update_member_by_id(member_id: int, data: Members, session: Session=Depends(get_session)):
  member=session.get(Members, member_id)
  if not member:
    raise HTTPException(status_code=404, detail="member not found")
  for key, value in data.dict(exclude_unset=True):
    setattr(member, key, value)
  session.commit()
  session.refresh(member)
  return member



@app.post("/login")
def login(
    request: LoginRequest,
    session: Session = Depends(get_session)
):

    user = session.exec(
        select(Members).where(
            or_(
                Members.username == request.username_or_email,
                Members.email == request.username_or_email
            )
        )
    ).first()

    if user is None:

        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    if not verify_password(
        request.password,
        user.password
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    token = create_access_token(
        {
            "sub": str(user.id),
            "email": user.email
        }
    )

    return {
        "access_token": token,
        "token_type": "Bearer"
    }

@app.post("/logout")
def logout(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    BLACKLISTED_TOKENS.add(credentials.credentials)

    return {
        "message": "Logout successful"
    }
