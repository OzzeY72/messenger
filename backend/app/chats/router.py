from fastapi import APIRouter, Depends, HTTPException, status, WebSocketDisconnect, WebSocket
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, List
from uuid import UUID

from app.chats.deps import get_chat_service
from app.database import get_db
from app.utils.security import get_current_user
from app.chats.service import ChatService
from app.chats.schemas import ChatCreate, ChatRead
from app.messages.deps import get_message_service
from app.messages.service import MessageService

router = APIRouter()

@router.post("/", response_model=ChatRead, status_code=status.HTTP_201_CREATED)
async def create_chat(
    chat_in: ChatCreate,
    current_user=Depends(get_current_user),
    service: ChatService = Depends(get_chat_service)
):
    """
    New chat creation (delegates all logic to service)
    """
    return await service.create_chat(chat_in, current_user.id)

@router.get("/", response_model=list[ChatRead])
async def get_my_chats(
    current_user=Depends(get_current_user),
    service: ChatService = Depends(get_chat_service)
):
    """
    Get all user's chats
    """
    chats = await service.get_user_chats(current_user.id)
    return chats


@router.get("/{chat_id}", response_model=ChatRead)
async def get_chat(
    chat_id: UUID,
    current_user=Depends(get_current_user),
    service: ChatService = Depends(get_chat_service)
):
    """
    Get chat by ID.
    """
    chat = await service.get_chat_for_user(chat_id, current_user.id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found or access denied")
    return chat
