from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.users.models import User
from app.utils.security import get_current_user
from app.chats.deps import get_chat_repo
from app.chats.repository import ChatRepository
from .service import AttachmentService

def get_attachment_service(
        db: AsyncSession = Depends(get_db), 
        current_user: User = Depends(get_current_user),
        chat_repo: ChatRepository = Depends(get_chat_repo)
    ) -> AttachmentService:
    """
    Dependency to inject AttachmentService.
    """
    return AttachmentService(db, current_user, chat_repo)
