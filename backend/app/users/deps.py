from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.messages.repository import MessageRepository
from app.users.repository import UserRepository
from .service import UserService

def get_user_repo(
    db: AsyncSession = Depends(get_db),
) -> MessageRepository:
    return UserRepository(db)

def get_user_service(
    user_repo: UserRepository = Depends(get_user_repo)
) -> UserService:
    """
    Dependency to inject UserService.
    """
    return UserService(user_repo)