FROM node:20-alpine AS frontend-builder

WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install

COPY frontend/ .
RUN npm run build

FROM python:3.12-slim

WORKDIR /app/backend

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY backend/ .

RUN pip install --no-cache-dir -r requirements.txt

COPY --from=frontend-builder /app/frontend/dist ./static

COPY backend/entrypoint.sh ./entrypoint.sh
RUN chmod +x ./entrypoint.sh

ENV PORT=8000
ENV HOST=0.0.0.0
ENV PYTHONPATH=/app/backend

ENTRYPOINT ["./entrypoint.sh"]
CMD ["fastapi", "run", "app/main.py", "--port", "8000"]

