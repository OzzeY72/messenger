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

from .schemas import MessageCreate, MessageRead, MessageUpdate
from .repository import MessageRepository

router = APIRouter()

@router.post("/", response_model=MessageRead)
async def send_message(
    chat_id: UUID = Form(...),
    content: Optional[str] = Form(None),
    files: List[UploadFile] = File([]),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    chat_repo: ChatRepository = Depends(get_chat_repo),
    service: MessageService = Depends(get_message_service),
):
    await verify_chat_membership(chat_id, current_user.id, chat_repo)

    repo = MessageRepository(db)
    message = await repo.create(
        sender_id=current_user.id,
        data={"chat_id": chat_id, "content": content},
    )
    
    if files:
        attachments = await service.save_attachments(message.id, files)
        message.attachments = attachments

    return message

@router.put("/{message_id}", response_model=MessageRead)
async def update_message(
    message_id: UUID,
    data: MessageUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    message = await verify_message_owner(message_id, current_user.id, db)
    repo = MessageRepository(db)

    return await repo.update(message, data.content)


@router.get("/chat/{chat_id}", response_model=List[MessageRead])
async def get_messages_by_chat(
    chat_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    chat_repo: ChatRepository = Depends(get_chat_repo)
):
    await verify_chat_membership(chat_id, current_user.id, chat_repo)

    repo = MessageRepository(db)
    return await repo.get_message_with_attachments(chat_id=chat_id)


@router.delete("/{message_id}")
async def delete_message(
    message_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    message = await verify_message_owner(message_id, current_user.id, db)
    repo = MessageRepository(db)
    
    await repo.delete(message)
    return {"detail": "Message deleted"}
