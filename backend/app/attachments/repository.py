from sqlalchemy import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.messages.models import Message
from .models import Attachment


class AttachmentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, message_id, file_path, file_size, file_type=None, id=None):
        attachment = Attachment(
            id=id,
            message_id=message_id,
            file_path=file_path,
            file_type=file_type,
            file_size=file_size
        )
        print("ADD TO DB")
        self.db.add(attachment)
        await self.db.commit()
        await self.db.refresh(attachment)
        return attachment

    async def get_by_id(self, attachment_id: UUID) -> Attachment | None:
        result = await self.db.execute(select(Attachment).where(Attachment.id == attachment_id))
        return result.scalar_one_or_none()

    async def get_message_for_attachment(self, attachment_id: UUID) -> Message | None:
        result = await self.db.execute(
            select(Message).join(Attachment).where(Attachment.id == attachment_id)
        )
        return result.scalar_one_or_none()

    async def get_by_message(self, message_id):
        result = await self.db.execute(
            select(Attachment).where(Attachment.message_id == message_id)
        )
        return result.scalars().all()
