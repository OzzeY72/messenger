from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID
from datetime import datetime

from app.users.schemas import UserRead

class ChatCreate(BaseModel):
    user_ids: List[UUID] 

class ChatRead(BaseModel):
    id: UUID
    name: Optional[str]
    members: List[UserRead]
    created_at: datetime
