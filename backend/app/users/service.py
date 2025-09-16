from fastapi import HTTPException, status

from .repository import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession
from .models import User
from . import schemas

class UserService:
    def __init__(self, db: AsyncSession):
        self.repo = UserRepository(db)

    async def create_user(
        self,
        email: str, 
        name: str | None, 
        auth_provider: str, 
        hashed_password: str | None = None, 
    ) -> User:
        existing = await self.repo.get_by_email(email)
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")

        user = User(
            email=email,
            name=name,
            auth_provider=auth_provider,
            password_hash=hashed_password if hashed_password else None,
        )
        return await self.repo.create(user)