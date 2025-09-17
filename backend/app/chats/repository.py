from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.chats.models import Chat, chat_members_table
from uuid import UUID

class ChatRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, chat_id: UUID):
        result = await self.db.execute(select(Chat).where(Chat.id == chat_id))
        return result.scalar_one_or_none()

    async def is_member(self, chat_id: UUID, user_id: UUID) -> bool:
        result = await self.db.execute(
            select(chat_members_table).where(
                chat_members_table.c.chat_id == chat_id,
                chat_members_table.c.user_id == user_id
            )
        )
        return result.first() is not None

    async def create(self, chat: Chat, member_ids: list[UUID]):
        self.db.add(chat)
        await self.db.commit()

        # Adding members to help table
        for user_id in member_ids:
            await self.db.execute(
                chat_members_table.insert().values(chat_id=chat.id, user_id=user_id)
            )
        await self.db.commit()
        await self.db.refresh(chat)
        return chat
