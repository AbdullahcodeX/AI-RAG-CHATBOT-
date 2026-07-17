from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    session_id: str = Field(..., min_length=1)
    question: str = Field(..., min_length=1)


class ChatResponse(BaseModel):
    answer: str
    sources: list[str]


class UploadResponse(BaseModel):
    session_id: str
    filename: str
    chunks_indexed: int
    message: str


class SessionStatusResponse(BaseModel):
    session_id: str
    document_count: int
    chunk_count: int
    filenames: list[str]
