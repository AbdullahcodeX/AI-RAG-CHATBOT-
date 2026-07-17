import chromadb
from app.config import CHROMA_DIR, COLLECTION_NAME


class VectorStore:
    def __init__(self) -> None:
        self.client = chromadb.PersistentClient(path=str(CHROMA_DIR))
        self.collection = self.client.get_or_create_collection(name=COLLECTION_NAME)

    def add_chunks(self, session_id: str, filename: str, chunks: list[str], embeddings: list[list[float]]) -> None:
        ids = [f"{session_id}:{filename}:{i}" for i in range(len(chunks))]
        metadatas = [{"session_id": session_id, "source": filename, "chunk_index": i} for i in range(len(chunks))]
        self.collection.upsert(ids=ids, documents=chunks, embeddings=embeddings, metadatas=metadatas)

    def query(self, session_id: str, query_embedding: list[float], top_k: int) -> dict:
        return self.collection.query(
            query_embeddings=[query_embedding], n_results=top_k, where={"session_id": session_id}
        )

    def get_session_stats(self, session_id: str) -> dict:
        result = self.collection.get(where={"session_id": session_id})
        documents = result.get("documents") or []
        metadatas = result.get("metadatas") or []
        filenames = sorted({m["source"] for m in metadatas if m and "source" in m})
        return {"chunk_count": len(documents), "document_count": len(filenames), "filenames": filenames}

    def delete_session(self, session_id: str) -> None:
        result = self.collection.get(where={"session_id": session_id})
        ids = result.get("ids") or []
        if ids:
            self.collection.delete(ids=ids)
