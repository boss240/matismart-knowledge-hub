from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status

from packages.database.repositories import DocumentRepository
from packages.database.session import get_session
from packages.domain.models import DocumentCreate, DocumentRecord


router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("", response_model=DocumentRecord, status_code=status.HTTP_202_ACCEPTED)
def register_document(payload: DocumentCreate, session: Session = Depends(get_session)) -> DocumentRecord:
    return DocumentRepository(session).register_document(payload)
