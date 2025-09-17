from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException, status
import jwt
from app.database import AsyncSessionLocal
from app.users.repository import UserRepository
from app.utils.security import get_current_user


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        open_paths = {"/login", "/register", "/docs", "/openapi.json"}
        
        if request.url.path in open_paths:
            return await call_next(request)

        authorization: str = request.headers.get("Authorization")
        request.state.user = None

        if authorization and authorization.startswith("Bearer "):
            token = authorization.split(" ")[1]
            async with AsyncSessionLocal() as db:
                try:
                    user = await get_current_user(token=token, db=db)
                    request.state.user = user
                except Exception:
                    request.state.user = None

        response = await call_next(request)
        return response
