from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.database import get_db
from app.utils.security import get_current_user
from app.chats.service import ChatService
from app.chats.schemas import ChatCreate, ChatRead

router = APIRouter()

@router.post("/", response_model=ChatRead, status_code=status.HTTP_201_CREATED)
async def create_chat(
    chat_in: ChatCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    New chat creation
    """
    if current_user.id not in chat_in.user_ids:
        chat_in.user_ids.append(current_user.id) 

    service = ChatService(db)
    chat = await service.create_chat(chat_in)
    ret = await service.get_chat_for_user(chat.id, current_user.id)
    return ret

@router.get("/", response_model=list[ChatRead])
async def get_my_chats(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Get all user's chats
    """
    service = ChatService(db)
    chats = await service.get_user_chats(current_user.id)
    return chats


@router.get("/{chat_id}", response_model=ChatRead)
async def get_chat(
    chat_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Get chat by ID.
    """
    service = ChatService(db)
    chat = await service.get_chat_for_user(chat_id, current_user.id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found or access denied")
    return chat
