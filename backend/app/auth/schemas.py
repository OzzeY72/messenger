from pydantic import BaseModel, EmailStr
from typing import Optional

class RegisterEmail(BaseModel):
    email: EmailStr
    name: Optional[str]
    password: str

class LoginOAuth(BaseModel):
    provider_id: str
    auth_provider: str

class RegisterOAuth(BaseModel):
    email: EmailStr
    name: Optional[str]
    provider_id: str
    auth_provider: str

class LoginEmail(BaseModel):
    email: EmailStr
    password: str

class TokenData(BaseModel):
    user_id: str | None
    
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
