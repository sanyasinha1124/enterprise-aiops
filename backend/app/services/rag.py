from uuid import uuid4

from qdrant_client import models

from app.core.config import get_settings
from app.services.embeddings import EmbeddingService
from app.services.llm import GeminiService
from app.services.vector_store import VectorStore


class RAGService:
    def __init__(self):
        self.settings = get_settings()
        self.embeddings = EmbeddingService()
        self.llm = GeminiService()
        self.store = VectorStore()

    def index_chunks(self, chunks: list[dict]) -> int:
        if not chunks:
            return 0

        first_vector = self.embeddings.embed(chunks[0]["text"])
        self.store.ensure_collection(len(first_vector))

        points = []
        for chunk in chunks:
            vector = self.embeddings.embed(chunk["text"])
            points.append(
                models.PointStruct(
                    id=str(uuid4()),
                    vector=vector,
                    payload={
                        "title": chunk["title"],
                        "text": chunk["text"],
                        "source": chunk.get("source", "unknown"),
                    },
                )
            )

        self.store.upsert(points)
        return len(points)

    def retrieve(self, question: str, limit: int | None = None):
        vector = self.embeddings.embed(question)
        hits = self.store.search(vector, limit or self.settings.top_k)

        return [
            {
                "id": str(hit.id),
                "title": hit.payload.get("title", "Unknown"),
                "text": hit.payload.get("text", ""),
                "score": float(hit.score),
            }
            for hit in hits
        ]

    def answer(self, question: str):
        sources = self.retrieve(question)

        context = "\n\n".join(
            f"[SOURCE {i+1}] {s['title']}\n{s['text']}"
            for i, s in enumerate(sources)
        )

        prompt = f"""
You are EnterpriseOps AI, an enterprise support assistant.

Answer the user's question using ONLY the supplied context and tool results.
If the context is insufficient, say that you do not have enough information.
Do not invent policies, customers, orders, or numbers.
Cite sources using [SOURCE N] notation.

CONTEXT:
{context}

QUESTION:
{question}
"""

        answer = self.llm.generate(prompt)

        return answer, sources
