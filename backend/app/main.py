import shutil
import uuid
from pathli
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from app.config import CORS_ORIGINS, UPLOADS_DIR
from app.models.schemas import ChatRequest, ChatResponse, SessionStatusResponse, UploadResponse
from app.services.rag_service import RagService

app = FastAPI(title="Doc RAG Chat API", version="1.0.0")
_rag_service: RagService | None = None


def get_rag_service() -> RagService:
    global _rag_service
    if _rag_service is None:
        _rag_service = RagService()
    return _rag_service

app.add_middleware(CORSMiddleware, allow_origins=CORS_ORIGINS, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/api/upload", response_model=UploadResponse)
async def upload_pdf(file: UploadFile = File(...), session_id: str = Form(...)) -> UploadResponse:
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    session_dir = UPLOADS_DIR / session_id
    session_dir.mkdir(parents=True, exist_ok=True)
    safe_name = Path(file.filename).name
    destination = session_dir / safe_name
    try:
        with destination.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        chunk_count = get_rag_service().index_pdf(session_id, safe_name, destination)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to process PDF: {exc}") from exc
    return UploadResponse(session_id=session_id, filename=safe_name, chunks_indexed=chunk_count, message="PDF uploaded and indexed successfully.")


@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    try:
        answer, sources = get_rag_service().chat(request.session_id, request.question.strip())
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Chat failed: {exc}") from exc
    return ChatResponse(answer=answer, sources=sources)


@app.get("/api/session/{session_id}", response_model=SessionStatusResponse)
def session_status(session_id: str) -> SessionStatusResponse:
    stats = get_rag_service().get_session_status(session_id)
    return SessionStatusResponse(session_id=session_id, document_count=stats["document_count"], chunk_count=stats["chunk_count"], filenames=stats["filenames"])


@app.delete("/api/session/{session_id}")
def clear_session(session_id: str) -> dict:
    get_rag_service().clear_session(session_id)
    session_dir = UPLOADS_DIR / session_id
    if session_dir.exists():
        shutil.rmtree(session_dir)
    return {"message": "Session cleared."}


@app.post("/api/session")
def create_session() -> dict:
    return {"session_id": str(uuid.uuid4())}
