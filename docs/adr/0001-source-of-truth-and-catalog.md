# ADR 0001: OneDrive is source of truth, DataHub is governance catalog

## Status

Accepted

## Context

Matismart documents are authored and maintained in OneDrive. The AI platform needs discoverability, governance, lineage, approvals, and retrieval-ready representations without creating a second uncontrolled document source.

## Decision

OneDrive is the source of truth for document content. DataHub is the metadata and governance catalog. PostgreSQL/pgvector stores operational knowledge representations for ingestion, approval, retrieval, and audit.

## Consequences

- Every document record must preserve OneDrive source identity and source version metadata.
- AI answers must cite document versions and chunks.
- DataHub lineage describes the flow but does not own the document content.
- No secrets are committed to the repository.

