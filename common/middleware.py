from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse

from jose import jwt, JWTError

SECRET_KEY = "Tyagi"
ALGORITHM = "HS256"


class AuthMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):

        public_urls = [

            "/",
            "/health",
            "/login",
            "/signup",
            "/docs",
            "/openapi.json",
            "/redoc"

        ]

        if request.url.path in public_urls:

            return await call_next(request)

        auth = request.headers.get("Authorization")

        if auth is None:

            return JSONResponse(
                status_code=401,
                content={"detail": "Authorization header missing"}
            )

        if not auth.startswith("Bearer "):

            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid authorization header"}
            )

        token = auth.split(" ")[1]

        try:

            jwt.decode(
                token,
                SECRET_KEY,
                algorithms=[ALGORITHM]
            )

        except JWTError:

            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid Token"}
            )

        return await call_next(request)
