from app.chats.repository import ChatRepository
from sqlalchemy.dialects.postgresql import UUID
from app.chats.models import Chat
from app.chats.schemas import ChatCreate
from sqlalchemy.ext.asyncio import AsyncSession
from app.chats.models import Chat, chat_members_table
from sqlalchemy import select
from app.chats.schemas import ChatRead

class ChatService:
    def __init__(self, db: AsyncSession):
        self.repo = ChatRepository(db)

    async def create_chat(self, chat_in: ChatCreate):
        chat = Chat(name=chat_in.name)
        return await self.repo.create(chat, chat_in.user_ids)
    
    async def get_user_chats(self, user_id: UUID):
        result = await self.repo.db.execute(
            select(Chat)
            .join(chat_members_table)
            .where(chat_members_table.c.user_id == user_id)
        )
        chats = result.scalars().all()
        return [
            ChatRead(
                id=chat.id,
                name=chat.name,
                members=[user_id],
                created_at=chat.created_at,
            )
            for chat in chats
        ]

    async def get_chat_for_user(self, chat_id: UUID, user_id: UUID):
        chat = await self.repo.get(chat_id)
        if not chat:
            return None

        result = await self.repo.db.execute(
            select(chat_members_table).where(
                chat_members_table.c.chat_id == chat_id,
                chat_members_table.c.user_id == user_id,
            )
        )
        if not result.first():
            return None

        return ChatRead(
            id=chat.id,
            name=chat.name,
            members=[user_id],
            created_at=chat.created_at,
        )
