from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .models import Message
from .schemas import MessageCreate, MessageUpdate
from uuid import UUID
from sqlalchemy.orm import selectinload
from app.attachments.models import Attachment

class MessageRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, sender_id: UUID, data: MessageCreate):
        message = Message(
            chat_id=data["chat_id"],
            sender_id=sender_id,
            content=data["content"],
        )

        self.db.add(message)
        await self.db.commit()
        await self.db.refresh(message)
        return message

    async def update(self, message: Message, new_content: str):
        message.content = new_content
        self.db.add(message)
        await self.db.commit()
        await self.db.refresh(message)
        return message

    async def get_message_with_attachments(self, chat_id: UUID):
        stmt = (
            select(Message)
            .options(selectinload(Message.attachments))
            .where(Message.chat_id == chat_id)
            .order_by(Message.created_at)
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_by_chat(self, chat_id: UUID):
        query = (
            select(Message)
            .options(selectinload(Message.attachments))
            .where(Message.chat_id == chat_id)
            .order_by(Message.created_at)
        )
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_by_id(self, message_id: UUID):
        query = (
            select(Message)
            .options(selectinload(Message.attachments))
            .where(Message.id == message_id)
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def delete(self, message: Message):
        await self.db.delete(message)
        await self.db.commit()
