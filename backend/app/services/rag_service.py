from pathlib import Path
from app.config import TOP_K
from app.services.chunk_service import chunk_text
from app.services.gemini_service import GeminiService
from app.services.pdf_service import extract_text_from_pdf
from app.services.vector_store import VectorStore


class RagService:
    def __init__(self) -> None:
        self._gemini: GeminiService | None = None
        self.vector_store = VectorStore()

    @property
    def gemini(self) -> GeminiService:
        if self._gemini is None:
            self._gemini = GeminiService()
        return self._gemini

    def index_pdf(self, session_id: str, filename: str, file_path: Path) -> int:
        text = extract_text_from_pdf(file_path)
        chunks = chunk_text(text)
        if not chunks:
            raise ValueError("No readable text found in the PDF.")
        embeddings = self.gemini.embed_texts(chunks)
        self.vector_store.add_chunks(session_id, filename, chunks, embeddings)
        return len(chunks)

    def chat(self, session_id: str, question: str) -> tuple[str, list[str]]:
        stats = self.vector_store.get_session_stats(session_id)
        if stats["chunk_count"] == 0:
            raise ValueError("Upload a PDF first before asking questions.")
        query_embedding = self.gemini.embed_query(question)
        hits = self.vector_store.query(session_id, query_embedding, TOP_K)
        documents = hits.get("documents", [[]])[0]
        metadatas = hits.get("metadatas", [[]])[0]
        if not documents:
            raise ValueError("No relevant content found in your uploaded documents.")
        sources = sorted({m["source"] for m in metadatas if m and "source" in m})
        context = "\n\n".join(f"[Source: {m['source']}]\n{doc}" for doc, m in zip(documents, metadatas))
        prompt = f"""Answer using ONLY the context below.
If not in context, say: "I don't know based on the uploaded documents."

Context:
{context}

Question: {question}
"""
        return self.gemini.generate_answer(prompt), sources

    def get_session_status(self, session_id: str) -> dict:
        return self.vector_store.get_session_stats(session_id)

    def clear_session(self, session_id: str) -> None:
        self.vector_store.delete_session(session_id)
