# Matismart Knowledge & AI Integration Hub

## 1. Product Summary

**Matismart Knowledge & AI Integration Hub** is a production service for turning Matismart's business, engineering, commercial, regulatory, and product documents into governed, searchable, AI-ready knowledge.

The product does not replace OneDrive, SharePoint, engineers, or the operating document process. Its role is to register documents, track versions, extract metadata, prepare document content for retrieval, enforce review workflows, and expose approved knowledge to Matismart AI products with citations and provenance.

The core operating principle is:

```text
OneDrive = source of truth
DataHub = metadata and governance catalog
PostgreSQL/pgvector = operational knowledge store
Matismart AI Platform = approved knowledge consumer
```

## 2. Product Problem

Matismart knowledge is spread across project folders, technical documents, commercial files, product documentation, regulatory evidence, spreadsheets, presentations, scanned images, and future AI outputs. Without a controlled knowledge layer, AI answers can become unreliable because the system may not know:

- which document version is current;
- who owns a document or dataset;
- whether engineering review was completed;
- which source supports an AI answer;
- which knowledge is draft, approved, superseded, or published;
- how OneDrive files, processed chunks, embeddings, knowledge graph entities, and AI responses relate to each other.

This creates risk for engineering decisions, customer communication, regulatory work, commercial proposals, and future automation.

The Knowledge Hub solves this by creating a controlled vertical path:

```text
Document registration -> ingestion -> processing -> review -> approval -> governed AI retrieval
```

## 3. Product Goals

The first product goal is to create a reliable foundation for Matismart AI systems that can answer questions using approved project and technical knowledge with traceable sources.

The product is designed to:

- preserve OneDrive as the source of truth for original files;
- register documents and versions in a durable database;
- keep document lifecycle state explicit;
- connect metadata to DataHub domains, glossary terms, tags, ownership, and lineage;
- support PostgreSQL/pgvector as the first operational vector store;
- prepare future knowledge graph, NotebookLM, Google Drive, and API catalog integrations;
- expose REST APIs for document registration, reading, approval, search, and RAG queries;
- keep secrets outside the repository and outside committed configuration files;
- make governance visible before AI is allowed to publish or reuse knowledge.

## 4. Target Users

### Engineering

Engineers need a controlled way to find technical specifications, project assumptions, equipment data, system decisions, calculations, and approved implementation knowledge.

The Hub helps engineers answer:

- what is the latest approved technical document;
- which source supports this recommendation;
- whether a document was reviewed;
- which project, tenant, and security zone the document belongs to;
- whether the document has been superseded.

### Project and Product Teams

Project and product teams need a structured knowledge base for decisions, product logic, implementation status, customer requirements, and solution documentation.

The Hub helps them track:

- product knowledge;
- customer project evidence;
- technical documentation;
- ownership and accountability;
- domain-level organization in DataHub.

### Commercial and Customer-Facing Teams

Commercial users need approved, reusable facts for proposals, presentations, offers, and customer communication.

The Hub should reduce the risk of using outdated figures, draft claims, or unsupported AI-generated content.

### AI Platform and Automation

Matismart AI systems need controlled access to knowledge that has provenance, version history, and workflow state.

The Hub provides a retrieval boundary so AI consumers can use only knowledge that is registered, processed, reviewed, and approved according to product rules.

### Governance and Compliance

Governance users need auditability, ownership, lineage, source references, and clear separation of domains such as regulatory, commercial, energy assets, EMS, IoT, and AI knowledge.

## 5. Domain Model

The product is organized around the following primary entities:

```text
Tenant
  Project
    Document
      DocumentVersion
        DocumentChunk
        Embedding
        Approval
      KnowledgeEntity
      AuditEvent
      QueryCitation
```

### Tenant

A tenant represents an organizational boundary. It is used for isolation, authorization, ownership, and future multi-tenant deployment.

### Project

A project groups documents, versions, knowledge entities, approvals, and audit events under a practical business or engineering context.

### Document

A document is the canonical logical record for a source item. It is not just a file path. It is the durable identity that connects OneDrive metadata, document versions, workflow state, DataHub metadata, chunks, embeddings, approvals, and AI citations.

### Document Version

A document version represents a concrete source state. It can hold checksum, source URI, version number, content type, and workflow state.

### Document Chunk

A document chunk is a processed section of a document version prepared for search, retrieval, or AI processing. Chunks must preserve traceability to the source document and version.

### Embedding

An embedding stores vector representation metadata for a chunk. PostgreSQL with pgvector is the first target store.

### Knowledge Entity

A knowledge entity represents structured knowledge extracted from documents, such as products, sites, devices, energy assets, standards, tariffs, equipment, customers, systems, or technical concepts.

### Approval

An approval records engineer or authorized reviewer decisions. It supports approve, reject, and future superseding flows.

### Audit Event

An audit event records important state changes, ingestion decisions, approval actions, and AI-facing publication events.

## 6. Workflow Model

The product uses explicit document lifecycle states:

```text
RAW -> INGESTED -> AI_PROCESSED -> ENGINEER_REVIEWED -> APPROVED -> PUBLISHED
```

### RAW

The document exists in the source system but has not yet been fully processed.

### INGESTED

The system registered the document and basic metadata. The original remains in OneDrive or the connected source system.

### AI_PROCESSED

The system extracted content, metadata, chunks, embeddings, and possible structured entities.

### ENGINEER_REVIEWED

A human reviewer checked the AI-processed content or source interpretation.

### APPROVED

The document version is approved for controlled retrieval and reuse.

### PUBLISHED

The approved knowledge is available to Matismart AI Platform or another governed consumer.

## 7. Core Capabilities

### Document Registration

The API registers documents and versions into the database. This creates the first durable record needed for all later processing.

Current vertical:

```text
API request -> validation -> tenant/project lookup or creation -> document -> document version -> workflow state
```

### Document Reading

The API exposes registered documents for downstream services and operational checks:

```text
GET /v1/documents/{id}
GET /v1/documents
```

The list endpoint supports tenant filtering, optional project filtering, limit, and offset.

### OneDrive and Microsoft Graph Integration

OneDrive is treated as the source of truth. Microsoft Graph is the planned connector layer for reading source metadata, file changes, version information, and future webhook or delta sync events.

The Hub should store references and metadata, not replace the source repository of original files.

### Ingestion Pipeline

The ingestion pipeline is responsible for:

- source discovery;
- metadata extraction;
- checksum and version tracking;
- document type detection;
- content extraction for PDF, DOCX, XLSX, PPTX, CSV, images, and future formats;
- chunking;
- preparation for embeddings and retrieval;
- failure capture and retry routing.

### Knowledge Core

The knowledge core stores canonical document and workflow data in PostgreSQL. pgvector is used for vector search over approved or process-ready chunks.

### RAG Engine

The retrieval-augmented generation layer must provide answers with citations. AI responses must be traceable to document versions, chunks, and source metadata.

The RAG engine should support:

- hybrid retrieval;
- citation enforcement;
- provenance metadata;
- Gemini adapter;
- answer confidence and refusal paths;
- filtering by tenant, project, security zone, workflow state, and DataHub governance metadata.

### Approval API

The approval layer allows authorized reviewers to approve or reject document versions. The system should later support superseding, reviewer comments, and policy-based publication rules.

### DataHub Governance

DataHub is the metadata and governance catalog, not the operational source of documents.

The Hub prepares DataHub metadata for:

- domains;
- glossary;
- tags;
- ownership;
- lineage;
- API and dataset catalog entries;
- future knowledge graph visibility.

Target DataHub domains:

- Product Knowledge
- Technical Documentation
- Customer Projects
- AI Knowledge
- Energy Assets
- IoT & Tuya
- EMS
- Commercial
- Regulatory

### Audit and Observability

The product should emit structured logs, metrics, traces, ingestion errors, retries, and audit events for important workflow transitions.

## 8. Lineage Model

The intended lineage is:

```text
OneDrive
  -> Microsoft Graph
  -> Ingestion
  -> Document Processing
  -> PostgreSQL/pgvector
  -> Knowledge Graph
  -> Gemini/RAG
  -> Matismart AI Platform
```

This lineage expresses how original files become governed AI-ready knowledge. It also makes clear that AI output must be grounded in registered and approved source knowledge.

## 9. API Product Surface

The API is the first operational interface of the product.

Current and planned endpoint groups:

- `GET /healthz` for service health;
- `POST /v1/documents` for document registration;
- `GET /v1/documents/{id}` for reading one registered document;
- `GET /v1/documents` for listing registered documents;
- `POST /v1/approvals/{document_version_id}` for review decisions;
- `POST /v1/query` for RAG-style queries;
- future search endpoints for metadata and full-text retrieval;
- future ingestion endpoints for connector events and processing jobs;
- future audit endpoints for governance review.

API responses should prefer stable identifiers, workflow state, source references, project context, and timestamps.

## 10. MVP Scope

The Phase 1 MVP focuses on a real working vertical:

```text
REST API -> PostgreSQL schema -> document registration -> document reading -> workflow state -> tests -> CI
```

MVP includes:

- FastAPI application structure;
- SQLAlchemy database models;
- Alembic migrations;
- document registration endpoint;
- document read and list endpoints;
- approval endpoint skeleton;
- RAG/query endpoint placeholder;
- DataHub metadata-as-code configuration;
- CI for tests and migration validation;
- documentation for product, architecture, governance, and DataHub scope.

## 11. Non-Goals for Phase 1

Phase 1 should not attempt to do everything at once.

The following are intentionally outside the first MVP:

- replacing OneDrive as the source of truth;
- committing secrets, tokens, passwords, or private connection strings;
- building a full user interface before the API and data model are stable;
- allowing AI answers without source citations;
- allowing unreviewed AI output to become published knowledge automatically;
- implementing every connector before the document workflow is reliable;
- treating DataHub as the storage engine for operational document data;
- building a full production knowledge graph before ingestion, review, and retrieval contracts are proven.

## 12. Security and Governance Principles

The product must assume that business and technical knowledge can be sensitive.

Security principles:

- no secrets in repository files;
- environment variables and CI secrets for credentials;
- tenant and project isolation;
- future RBAC and ABAC support;
- explicit workflow state checks before publication;
- audit trail for registration, approval, processing, and publication;
- source references preserved for every document version;
- citations required for AI answers;
- DataHub ownership and tags used for governance visibility.

## 13. DataHub Model

DataHub should represent the governance view of the Hub.

### Domains

Domains group knowledge by business meaning. They are used for ownership, discovery, and governance.

### Glossary

The glossary defines business and technical language, including product terms, engineering concepts, document types, workflow states, data classifications, and AI governance concepts.

### Tags

Tags classify assets by status, sensitivity, lifecycle, processing mode, document type, and governance requirement.

Recommended tag categories:

- `source-of-truth`
- `ai-ready`
- `requires-review`
- `approved`
- `published`
- `superseded`
- `confidential`
- `customer-facing`
- `engineering`
- `regulatory`

### Ownership

Ownership should be assigned at domain, dataset, API, and document family level.

Typical owner roles:

- business owner;
- technical owner;
- data steward;
- engineering reviewer;
- security reviewer;
- AI platform owner.

### Lineage

Lineage should connect source systems, processing jobs, database tables, vector stores, knowledge graph entities, RAG pipelines, and AI platform consumers.

## 14. Operational Model

The product should be operated as a service, not as a one-time script.

Expected operational responsibilities:

- keep migrations versioned;
- run tests in CI before promotion;
- keep ingestion configs in repository without secrets;
- store runtime credentials only in local environment or CI secrets;
- monitor failed ingestion jobs;
- preserve audit history;
- review AI-processed content before publication;
- keep DataHub metadata aligned with code and database changes.

## 15. Success Criteria

The product is successful when Matismart can:

- register a document through API and persist it in PostgreSQL;
- read registered documents through API;
- track document workflow state;
- connect a document to tenant, project, source URI, checksum, and version;
- run automated tests and migrations in CI;
- describe domains, ownership, glossary, tags, and lineage in DataHub;
- retrieve AI answers only with citations to source material;
- separate source documents from metadata governance and AI consumption;
- safely extend the system with Microsoft Graph, Gemini, DataHub, and knowledge graph integrations.

## 16. Roadmap

### Phase 1: Working Knowledge Vertical

- PostgreSQL schema and migrations
- Document registration
- Document reading API
- Approval state foundation
- DataHub metadata-as-code
- CI validation

### Phase 2: Source Connectors and Processing

- Microsoft Graph connector
- OneDrive delta sync
- Source version tracking
- Content extraction pipeline
- Chunking and embedding jobs
- Processing failure handling

### Phase 3: Governed Retrieval

- Hybrid search
- pgvector retrieval
- Gemini/RAG adapter
- Mandatory citations
- Tenant/project/security filtering
- Query audit trail

### Phase 4: Review and Publication

- Engineer review interface
- Approval comments
- Superseding workflows
- Publication controls
- Policy checks before AI consumption

### Phase 5: Knowledge Graph and AI Platform Integration

- Knowledge entity extraction
- Relationship modeling
- DataHub lineage enrichment
- Matismart AI Platform integration
- Advanced governance dashboards

## 17. Product Boundary

Matismart Knowledge & AI Integration Hub is the governed bridge between source documents and AI systems.

It should stay disciplined:

- OneDrive remains the place where original business and technical files live.
- DataHub remains the catalog that explains ownership, lineage, and governance.
- PostgreSQL/pgvector remains the operational store for registered knowledge and retrieval.
- AI systems consume approved, cited, governed knowledge rather than uncontrolled files.

That boundary is what makes the product useful: it gives Matismart a foundation for AI that is traceable, reviewable, and operationally expandable.
