from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from . import schemas
from .service import AuthService

router = APIRouter()

@router.post("/register/email", response_model=schemas.Token)
async def register_email(data: schemas.RegisterEmail, db: AsyncSession = Depends(get_db)):
    user = await AuthService(db).register_email(data)
    return {"User successfully registrated"}

@router.post("/login/email", response_model=schemas.Token)
async def login_email(data: schemas.LoginEmail, db: AsyncSession = Depends(get_db)):
    return await AuthService(db).login_email(data)

@router.post("/login/oauth", response_model=schemas.Token)
async def login_oauth(data: schemas.LoginOAuth, db: AsyncSession = Depends(get_db)):
    return await AuthService(db).login_oauth(data)
