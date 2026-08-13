from fastapi import APIRouter, status

from packages.domain.models import DocumentCreate, DocumentRecord, DocumentStatus


router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("", response_model=DocumentRecord, status_code=status.HTTP_202_ACCEPTED)
def register_document(payload: DocumentCreate) -> DocumentRecord:
    return DocumentRecord(
        document_id=payload.canonical_document_id,
        tenant_id=payload.tenant_id,
        project_id=payload.project_id,
        title=payload.title,
        source_uri=payload.source_uri,
        status=DocumentStatus.RAW,
    )

