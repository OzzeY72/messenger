from fastapi import HTTPException
from app.chats.repository import ChatRepository
from sqlalchemy.dialects.postgresql import UUID
from app.chats.models import Chat
from app.chats.schemas import ChatCreate
from sqlalchemy.ext.asyncio import AsyncSession
from app.chats.models import Chat, chat_members_table
from sqlalchemy import select
from app.chats.schemas import ChatRead
from sqlalchemy.orm import selectinload

from app.users.models import User
from app.users.schemas import UserRead
from app.users.service import UserService

class ChatService:
    def __init__(self, chat_repo: ChatRepository):
        self.repo = chat_repo

    async def create_chat(self, chat_in: ChatCreate, current_user_id: UUID):
        user_ids = list(set(chat_in.user_ids))
        if current_user_id not in user_ids:
            user_ids.append(current_user_id)

        # Check if chat with this user exist 
        existing_chat = await self.repo.find_chat_by_users(user_ids)
        if existing_chat:
            raise HTTPException(
                status_code=400,
                detail="Chat with these users already exists"
            )

        chat = Chat(name="")
        new_chat = await self.repo.create(chat, user_ids)

        return await self.get_chat_for_user(new_chat.id, current_user_id)
    
    async def get_user_chats(self, user_id: UUID):
        return await self.repo.get_user_chats(user_id)

    async def get_chat_for_user(self, chat_id: UUID, user_id: UUID):
        return await self.repo.get_chat_for_user(chat_id, user_id)
