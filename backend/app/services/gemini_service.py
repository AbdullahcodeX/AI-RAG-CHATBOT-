import os
from dotenv import load_dotenv
from google import genai
from app.config import CHAT_MODEL, EMBED_

load_dotenv()


class GeminiService:
    def __init__(self) -> None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY is not set. Copy backend/.env.example to backend/.env")
        self.client = genai.Client(api_key=api_key)

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        result = self.client.models.embed_content(model=EMBED_MODEL, contents=texts)
        return [embedding.values for embedding in result.embeddings]

    def embed_query(self, query: str) -> list[float]:
        result = self.client.models.embed_content(model=EMBED_MODEL, contents=[query])
        return result.embeddings[0].values

    def generate_answer(self, prompt: str) -> str:
        response = self.client.models.generate_content(model=CHAT_MODEL, contents=prompt)
        return response.text or "I could not generate an answer."
