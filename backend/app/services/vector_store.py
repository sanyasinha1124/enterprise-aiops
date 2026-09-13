from typing import Any
from qdrant_client import QdrantClient, models

from app.core.config import get_settings


class VectorStore:
    def __init__(self):
        settings = get_settings()
        self.collection = settings.qdrant_collection
        try:
            self.client = QdrantClient(url=settings.qdrant_url)
            self.client.get_collections()
            self.available = True
        except Exception:
            # Local in-memory fallback keeps the project runnable while learning.
            self.client = QdrantClient(":memory:")
            self.available = True

        # Set default dimension to 3072 to match Gemini embeddings
        self.ensure_collection(vector_size=3072)

    def ensure_collection(self, vector_size: int = 3072):
        names = {c.name for c in self.client.get_collections().collections}
        if self.collection not in names:
            self.client.create_collection(
                collection_name=self.collection,
                vectors_config=models.VectorParams(
                    size=vector_size,
                    distance=models.Distance.COSINE,
                ),
            )

    def upsert(self, points: list[models.PointStruct]):
        self.client.upsert(collection_name=self.collection, points=points)

    def search(self, vector: list[float], limit: int = 5) -> list[Any]:
        # Dynamically create collection matching vector size if it doesn't exist
        self.ensure_collection(vector_size=len(vector))
        response = self.client.query_points(
            collection_name=self.collection,
            query=vector,
            limit=limit,
            with_payload=True,
        )
        return response.points