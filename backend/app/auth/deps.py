from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.messages.repository import MessageRepository
from app.users.repository import UserRepository
from app.users.deps import get_user_repo, get_user_service
from .service import AuthService, UserService

def get_auth_service(
    user_repo: UserRepository = Depends(get_user_repo),
    user_service: UserService = Depends(get_user_service)
) -> AuthService:
    """
    Dependency to inject AuthService.
    """
    return AuthService(user_repo, user_service)


