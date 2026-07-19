from pathli

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOADS_DIR = BASE_DIR / "uploads"
CHROMA_DIR = BASE_DIR / "chroma_db"

CHUNK_SIZE = 800
CHUNK_OVERLAP = 100
TOP_K = 4

EMBED_MODEL = "gemini-embedding-001"
CHAT_MODEL = "gemini-2.0-flash"

COLLECTION_NAME = "documents"

CORS_ORIGINS = [
    "http://localhost:4200",
    "http://127.0.0.1:4200",
]
