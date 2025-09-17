from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID
from datetime import datetime

class ChatCreate(BaseModel):
    user_ids: List[UUID] 
    name: Optional[str]

class ChatRead(BaseModel):
    id: UUID
    name: Optional[str]
    members: List[UUID]
    created_at: datetime
