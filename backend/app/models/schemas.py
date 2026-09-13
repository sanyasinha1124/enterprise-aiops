from typing import Any, Optional
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)
    conversation_id: Optional[str] = None


class Source(BaseModel):
    id: str
    title: str
    text: str
    score: float


class ChatResponse(BaseModel):
    answer: str
    sources: list[Source] = []
    tool_calls: list[dict[str, Any]] = []
    conversation_id: Optional[str] = None


class IngestResponse(BaseModel):
    chunks_indexed: int
    collection: str


class EvaluationResult(BaseModel):
    total: int
    answered: int
    keyword_pass_rate: float
    avg_latency_seconds: float
