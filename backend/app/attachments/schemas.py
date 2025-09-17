from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class AttachmentCreate(BaseModel):
    message_id: UUID

class AttachmentRead(BaseModel):
    id: UUID
    message_id: UUID
    file_path: str
    file_type: str | None
    created_at: datetime

    class Config:
        from_attributes = True
