from fastapi import APIRouter

from app.models.schemas import IngestResponse
from app.scripts.ingest import load_knowledge
from app.services.rag import RAGService

router = APIRouter(prefix="/api", tags=["ingestion"])


@router.post("/ingest", response_model=IngestResponse)
def ingest():
    chunks = load_knowledge()
    count = RAGService().index_chunks(chunks)
    return IngestResponse(
        chunks_indexed=count,
        collection=RAGService().settings.qdrant_collection,
    )
