from enum import StrEnum

from pydantic import BaseModel, Field


class DocumentStatus(StrEnum):
    RAW = "RAW"
    INGESTED = "INGESTED"
    AI_PROCESSED = "AI_PROCESSED"
    ENGINEER_REVIEWED = "ENGINEER_REVIEWED"
    APPROVED = "APPROVED"
    PUBLISHED = "PUBLISHED"
    REJECTED = "REJECTED"
    SUPERSEDED = "SUPERSEDED"


class ApprovalDecision(StrEnum):
    APPROVE = "APPROVE"
    REJECT = "REJECT"
    REQUEST_CHANGES = "REQUEST_CHANGES"


class DocumentCreate(BaseModel):
    tenant_id: str = Field(min_length=1)
    project_id: str = Field(min_length=1)
    canonical_document_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    source_uri: str = Field(min_length=1)
    source_checksum_sha256: str | None = None
    source_version: str | None = None
    security_zone: str = "default"


class DocumentRecord(BaseModel):
    document_id: str
    tenant_id: str
    project_id: str
    document_version_id: str | None = None
    title: str
    source_uri: str
    status: DocumentStatus


class ApprovalRequest(BaseModel):
    decision: ApprovalDecision
    reviewer_id: str = Field(min_length=1)
    notes: str | None = None


class ApprovalResult(BaseModel):
    document_version_id: str
    decision: ApprovalDecision
    published: bool


class QueryRequest(BaseModel):
    tenant_id: str = Field(min_length=1)
    project_id: str = Field(min_length=1)
    question: str = Field(min_length=1)
    security_zone: str = "default"
    max_citations: int = Field(default=8, ge=1, le=25)


class Citation(BaseModel):
    document_id: str
    document_version_id: str
    chunk_id: str
    source_uri: str
    page: int | None = None
    text_range: str | None = None


class QueryResponse(BaseModel):
    answer: str
    citations: list[Citation]
    tenant_id: str
    project_id: str
