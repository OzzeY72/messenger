from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.chats.models import Chat
from app.chats.repository import ChatRepository
from app.chats.deps import get_chat_repo

async def verify_chat_membership(
        chat_id: str, 
        user_id: str, 
        chat_repo: ChatRepository
    ):
    chat = await chat_repo.get(chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    is_member = await chat_repo.is_member(chat_id, user_id)
    if not is_member:
        raise HTTPException(status_code=403, detail="User not in this chat")

    return chat
