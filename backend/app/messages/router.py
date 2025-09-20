from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID

from app.database import get_db
from app.users.models import User
from app.utils.security import get_current_user
from app.messages.deps import get_message_service
from app.messages.service import MessageService
from app.chats.models import Chat
from app.chats.utils import verify_chat_membership
from app.messages.utils import verify_message_owner
from app.chats.deps import get_chat_repo
from app.chats.repository import ChatRepository

from .schemas import MessageRead, MessageUpdate
from .repository import MessageRepository

router = APIRouter()

@router.post("/", response_model=MessageRead)
async def send_message(
    chat_id: UUID = Form(...),
    content: Optional[str] = Form(None),
    files: List[UploadFile] = File([]),
    current_user: User = Depends(get_current_user),
    service: MessageService = Depends(get_message_service),
):
    return await service.send_message(
        chat_id=chat_id,
        content=content,
        files=files,
        current_user=current_user,
    )

@router.put("/{message_id}", response_model=MessageRead)
async def update_message(
    message_id: UUID,
    data: MessageUpdate,
    current_user: User = Depends(get_current_user),
    service: MessageRepository = Depends(get_message_service)
):
    return await service.update(message_id, current_user.id, data.content)


@router.get("/chat/{chat_id}", response_model=List[MessageRead])
async def get_messages_by_chat(
    chat_id: UUID,
    current_user: User = Depends(get_current_user),
    service: MessageRepository = Depends(get_message_service)
):
    return await service.get_message_with_attachments(
        chat_id=chat_id, 
        current_user_id=current_user.id
    )

@router.delete("/{message_id}")
async def delete_message(
    message_id: UUID,
    current_user: User = Depends(get_current_user),
    service: MessageRepository = Depends(get_message_service)
):
    await service.delete(message_id, current_user_id=current_user.id)
    return {"detail": "Message deleted"}
