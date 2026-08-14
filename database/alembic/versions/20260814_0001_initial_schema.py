"""initial schema

Revision ID: 20260814_0001
Revises:
Create Date: 2026-08-14 00:00:00
"""

from collections.abc import Sequence

from alembic import op


revision: str = "20260814_0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS tenants (
          id varchar(36) PRIMARY KEY,
          slug text NOT NULL UNIQUE,
          name text NOT NULL,
          created_at timestamptz NOT NULL DEFAULT now()
        )
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS projects (
          id varchar(36) PRIMARY KEY,
          tenant_id varchar(36) NOT NULL REFERENCES tenants(id),
          slug text NOT NULL,
          name text NOT NULL,
          created_at timestamptz NOT NULL DEFAULT now(),
          CONSTRAINT uq_projects_tenant_slug UNIQUE (tenant_id, slug)
        )
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS documents (
          id varchar(36) PRIMARY KEY,
          tenant_id varchar(36) NOT NULL REFERENCES tenants(id),
          project_id varchar(36) NOT NULL REFERENCES projects(id),
          canonical_document_id text NOT NULL,
          title text NOT NULL,
          source_uri text NOT NULL,
          source_system text NOT NULL DEFAULT 'onedrive',
          security_zone text NOT NULL DEFAULT 'default',
          status text NOT NULL,
          created_at timestamptz NOT NULL DEFAULT now(),
          updated_at timestamptz NOT NULL DEFAULT now(),
          CONSTRAINT uq_documents_tenant_canonical_id UNIQUE (tenant_id, canonical_document_id)
        )
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS document_versions (
          id varchar(36) PRIMARY KEY,
          document_id varchar(36) NOT NULL REFERENCES documents(id),
          source_version text,
          source_checksum_sha256 text NOT NULL,
          mime_type text,
          byte_size integer,
          status text NOT NULL,
          supersedes_version_id varchar(36) REFERENCES document_versions(id),
          created_at timestamptz NOT NULL DEFAULT now(),
          CONSTRAINT uq_document_versions_document_checksum UNIQUE (document_id, source_checksum_sha256)
        )
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS document_chunks (
          id varchar(36) PRIMARY KEY,
          document_version_id varchar(36) NOT NULL REFERENCES document_versions(id),
          chunk_index integer NOT NULL,
          content text NOT NULL,
          content_sha256 text NOT NULL,
          page_start integer,
          page_end integer,
          token_count integer,
          metadata jsonb NOT NULL DEFAULT '{}'::jsonb,
          created_at timestamptz NOT NULL DEFAULT now(),
          CONSTRAINT uq_document_chunks_version_index UNIQUE (document_version_id, chunk_index)
        )
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS embeddings (
          id varchar(36) PRIMARY KEY,
          document_chunk_id varchar(36) NOT NULL REFERENCES document_chunks(id),
          model text NOT NULL,
          embedding vector(1536) NOT NULL,
          created_at timestamptz NOT NULL DEFAULT now(),
          CONSTRAINT uq_embeddings_chunk_model UNIQUE (document_chunk_id, model)
        )
        """
    )
    op.execute(
        """
        CREATE INDEX IF NOT EXISTS embeddings_vector_idx
          ON embeddings USING ivfflat (embedding vector_cosine_ops)
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS approvals (
          id varchar(36) PRIMARY KEY,
          document_version_id varchar(36) NOT NULL REFERENCES document_versions(id),
          reviewer_id text NOT NULL,
          decision text NOT NULL,
          notes text,
          created_at timestamptz NOT NULL DEFAULT now()
        )
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS audit_events (
          id varchar(36) PRIMARY KEY,
          tenant_id varchar(36) NOT NULL REFERENCES tenants(id),
          project_id varchar(36) REFERENCES projects(id),
          actor_id text,
          event_type text NOT NULL,
          entity_urn text NOT NULL,
          payload jsonb NOT NULL DEFAULT '{}'::jsonb,
          created_at timestamptz NOT NULL DEFAULT now()
        )
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS rag_queries (
          id varchar(36) PRIMARY KEY,
          tenant_id varchar(36) NOT NULL REFERENCES tenants(id),
          project_id varchar(36) NOT NULL REFERENCES projects(id),
          question text NOT NULL,
          answer text,
          model text,
          retrieval_trace jsonb NOT NULL DEFAULT '{}'::jsonb,
          created_at timestamptz NOT NULL DEFAULT now()
        )
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS rag_query_citations (
          id varchar(36) PRIMARY KEY,
          rag_query_id varchar(36) NOT NULL REFERENCES rag_queries(id),
          document_chunk_id varchar(36) NOT NULL REFERENCES document_chunks(id),
          citation_rank integer NOT NULL,
          created_at timestamptz NOT NULL DEFAULT now()
        )
        """
    )


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS rag_query_citations")
    op.execute("DROP TABLE IF EXISTS rag_queries")
    op.execute("DROP TABLE IF EXISTS audit_events")
    op.execute("DROP TABLE IF EXISTS approvals")
    op.execute("DROP INDEX IF EXISTS embeddings_vector_idx")
    op.execute("DROP TABLE IF EXISTS embeddings")
    op.execute("DROP TABLE IF EXISTS document_chunks")
    op.execute("DROP TABLE IF EXISTS document_versions")
    op.execute("DROP TABLE IF EXISTS documents")
    op.execute("DROP TABLE IF EXISTS projects")
    op.execute("DROP TABLE IF EXISTS tenants")
