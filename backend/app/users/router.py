from uuid import UUID
from fastapi import APIRouter, Depends
from app.users.models import User
from app.utils.security import get_current_user
from app.users.deps import get_user_service
from app.users.service import UserService

from .schemas import  UserRead

router = APIRouter()

@router.get("/me", response_model=UserRead)
async def get_user(
    current_user: User = Depends(get_current_user),
):
    return current_user

@router.get("/", response_model=list[UserRead])
async def search_users(
    q: str,
    service: UserService = Depends(get_user_service),
):
    return await service.search_users_by_name(q)

@router.get("/{user_id}", response_model=UserRead)
async def get_user_by_id(
    user_id: UUID,
    service: UserService = Depends(get_user_service),
):
    return await service.get_user_by_id(user_id)

