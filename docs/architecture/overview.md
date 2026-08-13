# Architecture Overview

Matismart Knowledge Hub is a governed knowledge service. It ingests source documents from OneDrive, processes them into approved knowledge, stores search-ready chunks and embeddings in PostgreSQL/pgvector, and exposes citation-first AI retrieval APIs.

## Boundary

OneDrive remains the source of truth for document content. The hub stores normalized metadata, immutable source versions, chunks, embeddings, approvals, audit events, and retrieval traces.

## Core flow

```text
OneDrive
  -> Microsoft Graph connector
  -> ingestion pipeline
  -> document processing
  -> engineer approval
  -> PostgreSQL/pgvector and knowledge graph
  -> Gemini/RAG
  -> Matismart AI Platform
```

## MVP components

- API: health, documents, approvals, query contracts.
- Domain package: shared statuses and request/response models.
- Database: pgvector-enabled schema for tenants, projects, documents, versions, chunks, embeddings, approvals, audit, and RAG citations.
- DataHub: governance catalog, domains, tags, glossary, ownership, ingestion recipes, and lineage.

