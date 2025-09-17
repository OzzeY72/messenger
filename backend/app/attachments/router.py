import os
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.database import get_db
from app.utils.security import get_current_user
from app.users.models import User
from app.messages.utils import verify_message_owner
from app.attachments.service import AttachmentService
from app.attachments.deps import get_attachment_service

from .repository import AttachmentRepository
from .schemas import AttachmentRead
from dotenv import load_dotenv

load_dotenv()

UPLOAD_DIR = os.getenv("UPLOAD_DIR")
os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter()

@router.get("/test-di")
async def test_di(service: AttachmentService = Depends(get_attachment_service)):
    return {"user_id": str(service.current_user.id)}

@router.get("/{attachment_id}")
async def get_attachment(
    attachment_id: UUID,
    service: AttachmentService = Depends(get_attachment_service)
):
    file_path, media_type = await service.get_attachment_file(attachment_id)

    return FileResponse(file_path, media_type=media_type)

@router.post("/{message_id}", response_model=AttachmentRead)
async def upload_attachment(
    message_id: UUID,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    await verify_message_owner(message_id, current_user.id, db)
    # Saving file
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    repo = AttachmentRepository(db)
    return await repo.create(
        message_id=message_id,
        file_path=file_path,
        file_type=file.content_type
    )
