from fastapi import APIRouter

from packages.domain.models import Citation, QueryRequest, QueryResponse


router = APIRouter(prefix="/query", tags=["query"])


@router.post("", response_model=QueryResponse)
def query_knowledge(payload: QueryRequest) -> QueryResponse:
    return QueryResponse(
        answer="RAG engine is not connected yet. This endpoint contract is ready for integration.",
        citations=[
            Citation(
                document_id="placeholder",
                document_version_id="placeholder",
                chunk_id="placeholder",
                source_uri="onedrive://placeholder",
            )
        ],
        tenant_id=payload.tenant_id,
        project_id=payload.project_id,
    )

