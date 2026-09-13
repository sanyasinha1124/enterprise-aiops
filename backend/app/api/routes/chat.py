from fastapi import APIRouter

from app.models.schemas import ChatRequest, ChatResponse
from app.services.agent import AgentService

router = APIRouter(prefix="/api", tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    agent = AgentService()
    answer, sources, tool_calls = agent.run(request.message)
    return ChatResponse(
        answer=answer,
        sources=sources,
        tool_calls=tool_calls,
        conversation_id=request.conversation_id,
    )
