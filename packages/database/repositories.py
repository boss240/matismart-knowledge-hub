from hashlib import sha256

from sqlalchemy import select
from sqlalchemy.orm import Session

from packages.database.models import Document, DocumentVersion, Project, Tenant
from packages.domain.models import DocumentCreate, DocumentRecord, DocumentStatus


class DocumentRepository:
    def __init__(self, session: Session):
        self.session = session

    def register_document(self, payload: DocumentCreate) -> DocumentRecord:
        tenant = self._get_or_create_tenant(payload.tenant_id)
        project = self._get_or_create_project(tenant, payload.project_id)

        document = self.session.scalar(
            select(Document).where(
                Document.tenant_id == tenant.id,
                Document.canonical_document_id == payload.canonical_document_id,
            )
        )
        if document is None:
            document = Document(
                tenant_id=tenant.id,
                project_id=project.id,
                canonical_document_id=payload.canonical_document_id,
                title=payload.title,
                source_uri=payload.source_uri,
                security_zone=payload.security_zone,
                status=DocumentStatus.RAW.value,
            )
            self.session.add(document)
            self.session.flush()
        else:
            document.project_id = project.id
            document.title = payload.title
            document.source_uri = payload.source_uri
            document.security_zone = payload.security_zone

        checksum = payload.source_checksum_sha256 or self._fallback_checksum(payload)
        version = self.session.scalar(
            select(DocumentVersion).where(
                DocumentVersion.document_id == document.id,
                DocumentVersion.source_checksum_sha256 == checksum,
            )
        )
        if version is None:
            version = DocumentVersion(
                document_id=document.id,
                source_version=payload.source_version,
                source_checksum_sha256=checksum,
                status=DocumentStatus.RAW.value,
            )
            self.session.add(version)
            self.session.flush()

        self.session.commit()

        return self._to_record(document, tenant, project, version)

    def get_document(self, tenant_slug: str, canonical_document_id: str) -> DocumentRecord | None:
        statement = (
            select(Document, Tenant, Project)
            .join(Tenant, Document.tenant_id == Tenant.id)
            .join(Project, Document.project_id == Project.id)
            .where(
                Tenant.slug == tenant_slug,
                Document.canonical_document_id == canonical_document_id,
            )
        )
        row = self.session.execute(statement).first()
        if row is None:
            return None

        document, tenant, project = row
        version = self._latest_version(document.id)
        return self._to_record(document, tenant, project, version)

    def list_documents(
        self,
        tenant_slug: str,
        project_slug: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[DocumentRecord]:
        statement = (
            select(Document, Tenant, Project)
            .join(Tenant, Document.tenant_id == Tenant.id)
            .join(Project, Document.project_id == Project.id)
            .where(Tenant.slug == tenant_slug)
            .order_by(Document.created_at.desc(), Document.canonical_document_id.asc())
            .limit(limit)
            .offset(offset)
        )
        if project_slug is not None:
            statement = statement.where(Project.slug == project_slug)

        records: list[DocumentRecord] = []
        for document, tenant, project in self.session.execute(statement).all():
            records.append(self._to_record(document, tenant, project, self._latest_version(document.id)))
        return records

    def _get_or_create_tenant(self, slug: str) -> Tenant:
        tenant = self.session.scalar(select(Tenant).where(Tenant.slug == slug))
        if tenant is None:
            tenant = Tenant(slug=slug, name=slug)
            self.session.add(tenant)
            self.session.flush()
        return tenant

    def _get_or_create_project(self, tenant: Tenant, slug: str) -> Project:
        project = self.session.scalar(
            select(Project).where(Project.tenant_id == tenant.id, Project.slug == slug)
        )
        if project is None:
            project = Project(tenant_id=tenant.id, slug=slug, name=slug)
            self.session.add(project)
            self.session.flush()
        return project

    def _latest_version(self, document_id: str) -> DocumentVersion | None:
        return self.session.scalar(
            select(DocumentVersion)
            .where(DocumentVersion.document_id == document_id)
            .order_by(DocumentVersion.created_at.desc(), DocumentVersion.id.desc())
            .limit(1)
        )

    @staticmethod
    def _to_record(
        document: Document,
        tenant: Tenant,
        project: Project,
        version: DocumentVersion | None,
    ) -> DocumentRecord:
        return DocumentRecord(
            document_id=document.canonical_document_id,
            tenant_id=tenant.slug,
            project_id=project.slug,
            document_version_id=version.id if version else None,
            title=document.title,
            source_uri=document.source_uri,
            status=DocumentStatus(document.status),
        )

    @staticmethod
    def _fallback_checksum(payload: DocumentCreate) -> str:
        material = "|".join(
            [
                payload.tenant_id,
                payload.project_id,
                payload.canonical_document_id,
                payload.source_uri,
                payload.source_version or "",
            ]
        )
        return sha256(material.encode("utf-8")).hexdigest()
