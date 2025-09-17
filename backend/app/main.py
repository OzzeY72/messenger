from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.middleware.auth import AuthMiddleware
from app.auth.router import router as auth_router
from app.chats.router import router as chats_router
from app.messages.router import router as messages_router
from app.attachments.router import router as attachments_router

def create_app() -> FastAPI:
    app = FastAPI(
        title="Messenger API",
        version="0.1.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(AuthMiddleware)

    app.include_router(auth_router, prefix="/auth", tags=["auth"])
    app.include_router(chats_router, prefix="/chats", tags=["chats"])
    app.include_router(messages_router, prefix="/messages", tags=["messages"])
    app.include_router(attachments_router, prefix="/attachments", tags=["attachments"])

    return app

app = create_app()