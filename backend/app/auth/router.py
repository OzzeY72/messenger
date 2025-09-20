from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.users.deps import get_user_repo, get_user_service
from app.users.repository import UserRepository
from app.users.service import UserService
from app.auth.deps import get_auth_service
from . import schemas
from .service import AuthService

router = APIRouter()

@router.post("/register/email", response_model=schemas.RegisterMessage)
async def register_email(
    data: schemas.RegisterEmail, 
    service: AuthService = Depends(get_auth_service)
):
    user = await service.register_email(data)
    return {"message": "User successfully registrated"}

@router.post("/login/email", response_model=schemas.Token)
async def login_email(
    data: schemas.LoginEmail, 
    service: AuthService = Depends(get_auth_service)
):
    return await service.login_email(data)

@router.post("/login/oauth", response_model=schemas.Token)
async def login_oauth(
    data: schemas.LoginOAuth, 
    service: AuthService = Depends(get_auth_service)
):
    return await service.login_oauth(data)
