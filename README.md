# Doc RAG Chat
Angular + FastAPI + Gemini RAG

## Backend
cd backend && python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt && cp .env.example .env
uvicorn app.main:app --reload --port 8000

## Frontend
cd frontend && npm install && npm start
