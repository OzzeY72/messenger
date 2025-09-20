from mailbox import Message
from uuid import UUID
import uuid
from fastapi import UploadFile
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from app.messages.schemas import MessageRead
from app.messages.utils import verify_message_owner
from app.users.service import UserService
from typing import List, Optional
import os

from app.attachments.models import Attachment
from app.messages.repository import MessageRepository
from app.users.models import User
from app.chats.utils import verify_chat_membership
from app.chats.repository import ChatRepository
from app.ws.notifier import Notifier
from dotenv import load_dotenv

from app.attachments.service import AttachmentService

load_dotenv()

UPLOAD_DIR = os.getenv("UPLOAD_DIR")

class MessageService:

    def __init__(self, 
        db: AsyncSession,
        chat_repo: ChatRepository, 
        notifier: Notifier, 
        repo: MessageRepository,
        attachment_service: AttachmentService
    ):
        self.db = db
        self.user_service = UserService(db)
        self.attachment_service = attachment_service
        self.chat_repo = chat_repo
        self.notifier = notifier
        self.repo = repo

    async def send_message(
        self,
        chat_id: UUID,
        content: Optional[str],
        files: List[UploadFile],
        current_user: User,
    ) -> Message:
        await verify_chat_membership(chat_id, current_user.id, self.chat_repo)

        message = await self.repo.create(
            sender_id=current_user.id,
            data={"chat_id": chat_id, "content": content},
        )

        if files:
            attachments = await self.save_attachments(message.id, files)
            message.attachments = attachments

        members = await self.chat_repo.get_chat_members(chat_id=chat_id)
        data = jsonable_encoder(MessageRead.model_validate(message))

        for member in members:
            await self.notifier.send_to_user(
                member.id,
                event="message_created",
                payload={"message": data}
            )

        return message

    async def save_attachments(self, message_id: UUID, files: List[UploadFile]):
        attachments = []

        for file in files:
            attachment_id = uuid.uuid4()
            
            file_ext = os.path.splitext(file.filename)[1]
            file_name = f"{attachment_id}{file_ext}"
            file_path = os.path.join(UPLOAD_DIR, file_name)
            print("Write file")
            with open(file_path, "wb") as f:
                f.write(await file.read())

            file_size = str(os.path.getsize(file_path))

            attachment = await self.attachment_service.create(
                id=attachment_id,
                message_id=message_id,
                file_path=file_name,
                file_type=file.content_type,
                file_size=file_size
            )

            attachments.append(attachment)

        await self.db.commit()
        return attachments
    
    async def update(
        self,
        message_id: UUID,
        current_user_id: UUID,
        new_content: str
    ) -> Message:
        message = await verify_message_owner(message_id, current_user_id, self.db)
        updated_message = await self.repo.update(message, new_content)

        members = await self.chat_repo.get_chat_members(chat_id=message.chat_id)
        data = jsonable_encoder(MessageRead.model_validate(updated_message))

        for member in members:
            await self.notifier.send_to_user(
                member.id,
                event="message_updated",
                payload={"message": data}
            )

        return updated_message
    
    async def get_message_with_attachments(
        self, 
        chat_id: UUID, 
        current_user_id: UUID
    ) -> MessageRead:
        await verify_chat_membership(chat_id, current_user_id, self.chat_repo)
        return await self.repo.get_message_with_attachments(chat_id=chat_id)
    
    async def delete(
        self, 
        message_id: UUID, 
        current_user_id: UUID
    ):
        message = await verify_message_owner(message_id, current_user_id, self.db)
        chat_id = message.chat_id
        
        await self.repo.delete(message)

        members = await self.chat_repo.get_chat_members(chat_id=chat_id)
        json_message_id = jsonable_encoder(message_id)
        json_chat_id = jsonable_encoder(chat_id)

        for member in members:
            await self.notifier.send_to_user(
                member.id,
                event="message_deleted",
                payload={"message_id": json_message_id, "chat_id": json_chat_id}
            )


    

