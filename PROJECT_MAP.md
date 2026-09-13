# Project map

- `backend/app/services/llm.py` — direct Gemini inference
- `backend/app/services/embeddings.py` — Gemini embeddings
- `backend/app/services/vector_store.py` — Qdrant
- `backend/app/services/rag.py` — explicit RAG pipeline
- `backend/app/services/tools.py` — safe application tools
- `backend/app/services/agent.py` — Gemini tool-calling loop
- `backend/app/services/database.py` — SQLAlchemy/SQLite or PostgreSQL
- `backend/app/evaluation/evaluator.py` — basic evaluation harness
- `backend/app/services/langchain_demo.py` — LangChain learning adapter
- `backend/app/services/llamaindex_demo.py` — LlamaIndex learning adapter
- `frontend/` — Angular UI
- `data/knowledge/` — synthetic enterprise documents
- `docs/` — learning and interview material
