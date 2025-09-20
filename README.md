# Messenger App

A full-featured messenger application with Google OAuth authentication, chats, messages, and attachments.  
The backend is built with **FastAPI**, the frontend with **Vite (React)**.  
The project runs in Docker via `docker-compose`.

---

## 📦 Getting Started

### 1. Requirements
- Docker
- Docker Compose v2+

### 2. Create `.env` files

#### `backend/.env`
```
DATABASE_URL=postgresql+asyncpg://myuser:mypassword@db:5432/mydb

SECRET_KEY=YOUR_SECRET_KEY
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=240

GOOGLE_CLIENT_ID=YOUR_GOOGLE_CLIENT_ID
GOOGLE_CLIENT_SECRET=YOUR_GOOGLE_CLIENT_SECRET
GOOGLE_REDIRECT_URI=http://localhost:8000/callback/auth/google

UPLOAD_DIR=/app/uploads
```

#### `frontend/.env`
```
VITE_API_BASE_URL=http://localhost:8000/api
VITE_WS_BASE_URL=ws://localhost:8000

VITE_GOOGLE_CLIENT_ID=1069012702745-cpjtta5403rmkv2ie7udd00tadcaemmp.apps.googleusercontent.com
VITE_GOOGLE_REDIRECT_URI=http://localhost:8000/callback/auth/google
```

### 3. Run the project
```bash
docker compose up --build
```

After building, the app will be available at:  
[http://localhost:8000](http://localhost:8000)

---

## ⚙️ Container Architecture

* **backend** — FastAPI app + frontend static files
* **frontend** — Vite (built into static files and mounted in backend)
* **db** — PostgreSQL database
* **migrations** — Alembic migrations (executed automatically via `entrypoint.sh`)

---

## 🔑 Authentication See swagger - /docs

Uses **JWT** + Google OAuth.

* `POST /api/auth/register` — register (email + password)
* `POST /api/auth/login` — login (email + password)
* `POST /api/auth/login/oauth` — login via Google (with `auth_provider`, `provider_id`)
* `GET /api/auth/me` — get current user (by JWT)

---

## 👤 Users

* `GET /api/users/{id}` — get user by ID
* `GET /api/users/me` — get current profile

---

## 💬 Chats & Messages

* `GET /api/chats` — get user’s chats
* `POST /api/chats` — create a chat
* `GET /api/messages/{chat_id}` — get messages in a chat
* `POST /api/messages` — send a message

---

## 📎 Attachments

* `POST /api/attachments/upload` — upload a file
* `GET /api/attachments/{id}` — download a file

---

## 🔌 WebSocket

Connection:  
```
ws://localhost:8000/ws
```

### Events

* **Server response (new message)**
```json
{
  "event": "message_created",
  "message": {
    
  }
}
```
* **Server response (updated message)**
```json
{
  "event": "message_updated",
  "message": {
    
  }
}
```
* **Server response (delete message)**
```json
{
  "event": "message_deleted",
  "message_id": "message_id",
  "chat_id": "chat_id"
}
```

---

## 🛠️ Migrations

Migrations are executed automatically on container startup.  
Run manually if needed:
```bash
alembic upgrade head
```

---

## 🚀 Development Mode

If you want to run outside Docker:

### Backend
```bash
cd backend
fastapi dev ./app/main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev -- --port 5173
```

