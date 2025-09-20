from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.chats.deps import get_chat_repo
from app.chats.repository import ChatRepository
from app.messages.repository import MessageRepository
from app.ws.deps import get_notifier
from app.ws.notifier import Notifier
from app.attachments.deps import get_attachment_service
from app.attachments.service import AttachmentService
from .service import MessageService

def get_message_repo(
        db: AsyncSession = Depends(get_db),
) -> MessageRepository:
        return MessageRepository(db)

def get_message_service(
        db: AsyncSession = Depends(get_db),
        chat_repo: ChatRepository = Depends(get_chat_repo),
        notifier: Notifier = Depends(get_notifier),
        repo: MessageRepository = Depends(get_message_repo),
        attachment_service: AttachmentService = Depends(get_attachment_service)
) -> MessageService:
    """
    Dependency to inject MessageService.
    """
    return MessageService(db, chat_repo, notifier, repo, attachment_service)
