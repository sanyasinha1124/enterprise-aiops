# EnterpriseOps AI

An end-to-end, production-oriented AI Engineering project built around the Gemini API.

## What this project demonstrates

- Python + FastAPI
- Gemini LLM inference through Google's current `google-genai` SDK
- Prompt engineering and system instructions
- Structured JSON responses
- Gemini embeddings
- RAG pipeline: ingestion -> chunking -> embeddings -> Qdrant -> retrieval -> generation
- LangChain concepts and integration helpers
- LlamaIndex ingestion/indexing adapter
- Tool calling / agentic workflows
- PostgreSQL via SQLAlchemy
- Evaluation harness
- Pytest
- Docker / Docker Compose
- GitHub Actions CI
- Angular frontend
- Security basics: environment secrets, validation, tool allow-listing
- Observability/logging

## Architecture

```text
Angular + Tailwind
       |
       | REST
       v
    FastAPI
       |
       +-------------------+
       |                   |
       v                   v
   Agent/RAG           PostgreSQL
       |
   +---+-------------------+
   |           |           |
   v           v           v
Gemini      Qdrant      Tools
LLM         Vector DB   Order/Customer/Ticket
   |
   v
Evaluation + Logging
```

## Important

This project uses Gemini as the foundation model. We are NOT training Gemini from scratch.

The project teaches both:
1. LLM fundamentals (tokens, embeddings, transformers, inference)
2. LLM application engineering (RAG, agents, tools, evaluation, deployment)

The model name is configurable through `GEMINI_MODEL`. The default in this starter is `gemini-3.8-flash`, matching Google's current Interactions API examples at the time this project was generated. If your account exposes a different model, change `.env`.

## Quick start

### 1. Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Put your Gemini key into `.env`:

```env
GEMINI_API_KEY=your_key_here
```

Start the API:

```bash
uvicorn app.main:app --reload
```

Open:
- http://127.0.0.1:8000
- http://127.0.0.1:8000/docs

### 2. Start Qdrant + PostgreSQL

If Docker is installed:

```bash
docker compose up -d qdrant postgres
```

The API can also start in demo mode without those services by using the local SQLite fallback and in-memory retrieval.

### 3. Ingest sample knowledge

```bash
python -m app.scripts.ingest
```

This loads the sample enterprise policies from `data/knowledge/`.

### 4. Try the API

```bash
curl -X POST http://127.0.0.1:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Can customer 1001 get a refund for order 5001?"}'
```

### 5. Run tests

```bash
pytest -q
```

## Learning order

Do not try to understand every file at once. Use this order:

1. `app/core/config.py`
2. `app/services/llm.py`
3. `app/services/embeddings.py`
4. `app/services/rag.py`
5. `app/services/tools.py`
6. `app/services/agent.py`
7. `app/api/routes/chat.py`
8. `app/evaluation/evaluator.py`
9. `frontend/`

## Interview topics covered

### LLM
- What is an LLM?
- Tokenization
- Parameters
- Training vs inference
- Context window
- Temperature
- Structured output

### RAG
- Chunking
- Embeddings
- Vector search
- Top-k retrieval
- Metadata
- Grounding
- Hallucination reduction
- Recall@K / MRR

### Agents
- Tool calling
- Function schemas
- Tool execution
- Agent loops
- Permissions
- Failure handling

### Production
- FastAPI
- PostgreSQL
- Docker
- CI/CD
- Secrets
- Logging
- Evaluation
- Latency
- Cost

## Safety note

The sample tools only operate on synthetic local data. Do not connect destructive production actions until authentication, authorization, audit logs, confirmation workflows, and least-privilege permissions are implemented.
