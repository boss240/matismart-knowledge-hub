from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Query, status

from packages.database.repositories import DocumentRepository
from packages.database.session import get_session
from packages.domain.models import DocumentCreate, DocumentRecord


router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("", response_model=DocumentRecord, status_code=status.HTTP_202_ACCEPTED)
def register_document(payload: DocumentCreate, session: Session = Depends(get_session)) -> DocumentRecord:
    return DocumentRepository(session).register_document(payload)


@router.get("", response_model=list[DocumentRecord])
def list_documents(
    tenant_id: str = Query(min_length=1),
    project_id: str | None = Query(default=None, min_length=1),
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    session: Session = Depends(get_session),
) -> list[DocumentRecord]:
    return DocumentRepository(session).list_documents(
        tenant_slug=tenant_id,
        project_slug=project_id,
        limit=limit,
        offset=offset,
    )


@router.get("/{document_id}", response_model=DocumentRecord)
def get_document(
    document_id: str,
    tenant_id: str = Query(min_length=1),
    session: Session = Depends(get_session),
) -> DocumentRecord:
    record = DocumentRepository(session).get_document(
        tenant_slug=tenant_id,
        canonical_document_id=document_id,
    )
    if record is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
    return record
