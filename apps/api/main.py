from fastapi import FastAPI

from apps.api.routes import approvals, documents, health, query


app = FastAPI(
    title="Matismart Knowledge Hub API",
    version="0.1.0",
    description="Governed knowledge ingestion, approval, and RAG API for Matismart.",
)

app.include_router(health.router)
app.include_router(documents.router, prefix="/v1")
app.include_router(approvals.router, prefix="/v1")
app.include_router(query.router, prefix="/v1")

