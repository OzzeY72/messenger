from fastapi import APIRouter, Depends , WebSocket, WebSocketDisconnect
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.users.models import User
from app.utils.security import get_current_user, get_current_user_ws
from app.ws.deps import get_notifier
from app.ws.notifier import Notifier

router = APIRouter()

@router.websocket("/me")
async def websocket_endpoint(websocket: WebSocket, token: str,  db: AsyncSession = Depends(get_db), notifier: Notifier = Depends(get_notifier)):
    user = await get_current_user_ws(token, db)
    await notifier.connect_user(user.id, websocket)

    try:
        while True:
            data = await websocket.receive_text()
            print(data)
    except WebSocketDisconnect:
        notifier.disconnect_user(user.id, websocket)
