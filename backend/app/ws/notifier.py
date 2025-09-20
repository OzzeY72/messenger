from typing import Dict, List
from fastapi import WebSocket
import json
from uuid import UUID

from fastapi.websockets import WebSocketState


class Notifier:
    def __init__(self):
        self.active_connections: Dict[UUID, WebSocket] = {}  # user_id -> websocket

    async def connect_user(self, user_id: UUID, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect_user(self, user_id: UUID, websocket: WebSocket):
        self.active_connections.pop(user_id, None)

    async def send_to_user(self, user_id: UUID, event: str, payload: dict):
        ws = self.active_connections.get(user_id)
        if ws and ws.client_state == WebSocketState.CONNECTED:
            await ws.send_text(json.dumps({"event": event, "data": payload}))
