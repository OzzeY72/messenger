from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select
from app.chats.models import Chat, chat_members_table
from uuid import UUID

from app.chats.schemas import ChatRead
from app.users.models import User
from app.users.schemas import UserRead

class ChatRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_chat_members(self, chat_id: UUID) -> List[UserRead]:
        result = await self.db.execute(
            select(User)
            .join(chat_members_table, chat_members_table.c.user_id == User.id)
            .where(chat_members_table.c.chat_id == chat_id)
        )
        members = result.scalars().all()
        return [UserRead(id=m.id, name=m.name, email=m.email) for m in members]

    async def get_user_chats(self, user_id: UUID):
        subq = (
            select(chat_members_table.c.chat_id)
            .where(chat_members_table.c.user_id == user_id)
            .subquery()
        )

        result = await self.db.execute(
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
        chat = await self.get(chat_id)
        if not chat:
            return None

        result = await self.db.execute(
            select(chat_members_table).where(
                chat_members_table.c.chat_id == chat_id,
                chat_members_table.c.user_id == user_id,
            )
        )
        if not result.first():
            return None

        members_result = await self.db.execute(
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

    async def find_chat_by_users(self, user_ids: list[UUID]) -> Chat | None:
        result = await self.db.execute(
            select(chat_members_table.c.chat_id)
            .where(chat_members_table.c.user_id.in_(user_ids))
            .group_by(chat_members_table.c.chat_id)
            .having(func.count(chat_members_table.c.user_id) == len(user_ids))
        )
        candidate_ids = [row[0] for row in result.all()]

        if not candidate_ids:
            return None

        for chat_id in candidate_ids:
            res = await self.db.execute(
                select(func.count(chat_members_table.c.user_id))
                .where(chat_members_table.c.chat_id == chat_id)
            )
            total_members = res.scalar()
            if total_members == len(user_ids):
                chat_res = await self.db.execute(
                    select(Chat).where(Chat.id == chat_id)
                )
                return chat_res.scalar_one()

        return None

    async def get(self, chat_id: UUID):
        result = await self.db.execute(select(Chat).where(Chat.id == chat_id))
        return result.scalar_one_or_none()

    async def is_member(self, chat_id: UUID, user_id: UUID) -> bool:
        result = await self.db.execute(
            select(chat_members_table).where(
                chat_members_table.c.chat_id == chat_id,
                chat_members_table.c.user_id == user_id
            )
        )
        return result.first() is not None

    async def create(self, chat: Chat, member_ids: list[UUID]):
        self.db.add(chat)
        await self.db.commit()

        # Adding members to help table
        for user_id in member_ids:
            await self.db.execute(
                chat_members_table.insert().values(chat_id=chat.id, user_id=user_id)
            )
        await self.db.commit()
        await self.db.refresh(chat)
        return chat
