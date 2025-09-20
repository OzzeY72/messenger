from uuid import UUID
from fastapi import HTTPException, status

from .repository import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession
from .models import User
from . import schemas

class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def create_user(
        self,
        email: str, 
        name: str | None, 
        auth_provider: str, 
        hashed_password: str | None = None, 
    ) -> User:
        existing = await self.user_repo.get_by_email(email)
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")

        user = User(
            email=email,
            name=name,
            auth_provider=auth_provider,
            password_hash=hashed_password if hashed_password else None,
        )
        return await self.user_repo.create(user)

    async def get_user_by_id(self, user_id: UUID) -> User:
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    async def search_users_by_name(self, query: str, limit: int = 10) -> list[User]:
        users = await self.user_repo.search_by_name(query, limit=limit)
        return users