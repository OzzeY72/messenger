from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=True)
    password_hash = Column(String, nullable=True)  # null when Google
    auth_provider = Column(String, nullable=False, default="email")  # email | google
    created_at = Column(DateTime(timezone=True), server_default=func.now())
