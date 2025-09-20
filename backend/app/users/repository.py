from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.dialects.postgresql import UUID
from .models import User

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_by_id(self, id: UUID):
        result = await self.db.execute(select(User).where(User.id == id))
        return result.scalars().first()

    async def get_by_email(self, email: str):
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalars().first()

    async def search_by_name(self, query: str, limit: int = 10) -> list[User]:
        result = await self.db.execute(
            select(User).where(User.name.ilike(f"%{query}%")).limit(limit)
        )
        return result.scalars().all()

    async def create(self, user: User):
        self.db.add(user)
        print("Added", user)
        await self.db.commit()
        await self.db.refresh(user)
        return user
