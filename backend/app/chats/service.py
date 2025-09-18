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

class ChatService:
    def __init__(self, db: AsyncSession):
        self.repo = ChatRepository(db)

    async def create_chat(self, chat_in: ChatCreate):
        chat = Chat(name=chat_in.name)
        return await self.repo.create(chat, chat_in.user_ids)
    
    async def get_user_chats(self, user_id: UUID):
        subq = (
            select(chat_members_table.c.chat_id)
            .where(chat_members_table.c.user_id == user_id)
            .subquery()
        )

        result = await self.repo.db.execute(
            select(Chat, User)
            .join(chat_members_table, chat_members_table.c.chat_id == Chat.id)
            .join(User, chat_members_table.c.user_id == User.id)
            .where(Chat.id.in_(select(subq.c.chat_id)))
        )

        rows = result.all()
        chats_dict: dict[UUID, ChatRead] = {}

        for chat, member in rows:
            if chat.id not in chats_dict:
                chats_dict[chat.id] = ChatRead(
                    id=chat.id,
                    name=chat.name,
                    members=[],
                    created_at=chat.created_at,
                )
            chats_dict[chat.id].members.append(UserRead(
                id=member.id,
                name=member.name,
                email=member.email
            ))

        return list(chats_dict.values())

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

        members_result = await self.repo.db.execute(
            select(User)
            .join(chat_members_table, chat_members_table.c.user_id == User.id)
            .where(chat_members_table.c.chat_id == chat_id)
        )
        members = members_result.scalars().all()
        member_schemas = [UserRead(
            id=m.id,
            name=m.name,
            email=m.email
        ) for m in members]

        return ChatRead(
            id=chat.id,
            name=chat.name,
            members=member_schemas,
            created_at=chat.created_at,
        )
