from fastapi import APIRouter, Depends
from app.users.models import User
from app.utils.security import get_current_user

from .schemas import  UserRead


router = APIRouter()

@router.get("/me", response_model=UserRead)
async def get_user(
    current_user: User = Depends(get_current_user),
):
    return current_user