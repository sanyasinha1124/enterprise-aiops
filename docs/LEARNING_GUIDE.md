# Learning Guide

## Phase 1 — LLM fundamentals

Study:
- Tokens
- Context
- Parameters
- Training vs inference
- Transformer architecture
- Attention
- Embeddings
- Temperature
- Structured outputs

Project files:
- `app/services/llm.py`

Interview questions:
1. What is an LLM?
2. What is a token?
3. What is a parameter?
4. Training vs inference?
5. What does temperature control?
6. What is a context window?

## Phase 2 — Embeddings

Study:
- Dense vectors
- Semantic similarity
- Cosine similarity
- Embedding dimensions

Project:
- `app/services/embeddings.py`

## Phase 3 — RAG

Study:
- Document loading
- Chunking
- Embedding
- Vector DB
- Top-k retrieval
- Metadata filtering
- Reranking
- Grounding

Project:
- `app/services/rag.py`
- `app/services/vector_store.py`

Interview questions:
1. Why RAG?
2. RAG vs fine-tuning?
3. What makes a good chunk?
4. What is top-k?
5. What is Recall@K?
6. How do you reduce hallucinations?

## Phase 4 — Agents and tool calling

Study:
- Function declaration
- Tool selection
- Tool execution
- Tool result
- Agent loop
- Permissions
- Human confirmation

Project:
- `app/services/tools.py`
- `app/services/agent.py`

## Phase 5 — LangChain and LlamaIndex

Use frameworks after understanding the direct pipeline.

LangChain:
- model wrappers
- prompts
- tools
- retrievers
- agents
- runnable pipelines

LlamaIndex:
- ingestion
- indexing
- data connectors
- retrieval

The project deliberately keeps a direct Gemini path visible so you can explain what frameworks abstract.

## Phase 6 — Evaluation

Measure:
- Retrieval Recall@K
- MRR
- answer correctness
- faithfulness
- relevance
- latency
- token usage
- tool accuracy
- failure rate

## Phase 7 — Production

Learn:
- FastAPI
- PostgreSQL
- Docker
- CI/CD
- secrets
- logging
- retries
- timeouts
- validation
- authentication/authorization
- observability
