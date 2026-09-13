from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.chat import router as chat_router
from app.api.routes.health import router as health_router
from app.api.routes.ingest import router as ingest_router
from app.services.database import init_db

app = FastAPI(
    title="EnterpriseOps AI",
    version="1.0.0",
    description="Agentic RAG enterprise AI platform using Gemini.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://127.0.0.1:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    init_db()


app.include_router(health_router)
app.include_router(chat_router)
app.include_router(ingest_router)


@app.get("/")
def root():
    return {
        "name": "EnterpriseOps AI",
        "status": "running",
        "docs": "/docs",
    }
