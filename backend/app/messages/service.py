from uuid import UUID
import uuid
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from app.users.service import UserService
from typing import List
import os

from app.attachments.models import Attachment
from app.messages.repository import MessageRepository
from . import schemas
from dotenv import load_dotenv

load_dotenv()

UPLOAD_DIR = os.getenv("UPLOAD_DIR")

class MessageService:

    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = MessageRepository(db)
        self.user_service = UserService(db)

    async def save_attachments(self, message_id: UUID, files: List[UploadFile]):
        attachments = []

        for file in files:
            attachment_id = uuid.uuid4()
            
            file_ext = os.path.splitext(file.filename)[1]
            file_name = f"{attachment_id}{file_ext}"
            file_path = os.path.join(UPLOAD_DIR, file_name)

            with open(file_path, "wb") as f:
                f.write(await file.read())

            attachment = Attachment(
                id=attachment_id,
                message_id=message_id,
                file_path=file_name,
                file_type=file.content_type,
            )
            self.db.add(attachment)
            attachments.append(attachment)

        await self.db.commit()
        return attachments