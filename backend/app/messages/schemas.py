from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional, List
from app.attachments.schemas import AttachmentRead

class AttachmentCreate(BaseModel):
    file_path: str
    file_type: Optional[str] = None

class MessageCreate(BaseModel):
    chat_id: UUID
    content: Optional[str] = None
    attachments: List[AttachmentCreate] = []

class MessageUpdate(BaseModel):
    content: str

class MessageRead(BaseModel):
    id: UUID
    chat_id: UUID
    sender_id: UUID
    content: Optional[str]
    created_at: datetime
    updated_at: datetime
    attachments: List[AttachmentRead] = []

    class Config:
        from_attributes = True
