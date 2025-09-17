import os
from fastapi import HTTPException, status
from uuid import UUID
from app.attachments.repository import AttachmentRepository
from app.chats.utils import verify_chat_membership
from app.users.models import User
from dotenv import load_dotenv

from app.chats.repository import ChatRepository

load_dotenv()

UPLOAD_DIR = os.getenv("UPLOAD_DIR")

class AttachmentService:
    def __init__(self, db, current_user: User, chat_repo: ChatRepository):
        self.repo = AttachmentRepository(db)
        self.current_user = current_user
        self.db = db
        self.chat_repo = chat_repo
        print(f"AttachmentService created: db={db}, user={current_user.id}, chat_repo={chat_repo}")

    async def get_attachment_file(self, attachment_id: UUID) -> str:
        attachment = await self.repo.get_by_id(attachment_id)
        if not attachment:
            raise HTTPException(status_code=404, detail="Attachment not found")
        
        message = await self.repo.get_message_for_attachment(attachment_id)
        if not message:
            raise HTTPException(status_code=404, detail="Message not found")
        
        await verify_chat_membership(message.chat_id, self.current_user.id, self.chat_repo)

        # Give path of file to ours route handler
        file_path = os.path.join(UPLOAD_DIR, attachment.file_path)
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")

        return file_path, attachment.file_type