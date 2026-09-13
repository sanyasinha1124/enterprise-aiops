from google import genai

from app.core.config import get_settings


class EmbeddingService:
    def __init__(self):
        settings = get_settings()
        if not settings.gemini_api_key:
            raise RuntimeError("GEMINI_API_KEY is missing.")
        self.settings = settings
        self.client = genai.Client(api_key=settings.gemini_api_key)

    def embed(self, text: str) -> list[float]:
        result = self.client.models.embed_content(
            model=self.settings.gemini_embedding_model,
            contents=text,
        )
        return list(result.embeddings[0].values)
