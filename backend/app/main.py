import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from h11 import Request

from app.middleware.auth import AuthMiddleware
from app.auth.router import router as auth_router
from app.users.router import router as user_router
from app.chats.router import router as chats_router
from app.messages.router import router as messages_router
from app.attachments.router import router as attachments_router
from app.ws.router import router as ws_router

def create_app() -> FastAPI:
    app = FastAPI(
        title="Messenger API",
        version="0.1.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(AuthMiddleware)

    app.mount("/assets", StaticFiles(directory="static/assets"), name="assets")

    app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
    app.include_router(user_router, prefix="/api/users", tags=["users"])
    app.include_router(chats_router, prefix="/api/chats", tags=["chats"])
    app.include_router(messages_router, prefix="/api/messages", tags=["messages"])
    app.include_router(attachments_router, prefix="/api/attachments", tags=["attachments"])

    app.include_router(ws_router, prefix="/ws", tags=["ws"])

    @app.exception_handler(404)
    async def custom_404_handler(request: Request, exc):
        index_path = os.path.join("static", "index.html")

        if not request.url.path.startswith("/api") and not request.url.path.startswith("/ws"):
            return FileResponse(index_path)

        return {"detail": "Not Found"}

    return app

app = create_app()