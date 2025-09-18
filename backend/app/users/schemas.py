from uuid import UUID
from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    auth_provider: str
    hashed_password: str | None 

class UserRead(UserBase):
    id: UUID

    class Config:
        orm_mode = True
