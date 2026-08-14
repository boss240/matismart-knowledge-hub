from collections.abc import Iterator

from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from apps.api.main import app
from packages.database.models import Document, DocumentVersion, Project, Tenant
from packages.database.session import Base, get_session


def build_test_session() -> Iterator[Session]:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    local_session = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
    with local_session() as session:
        yield session


def test_register_document_persists_workflow_state():
    session_iterator = build_test_session()
    session = next(session_iterator)

    def override_session() -> Iterator[Session]:
        yield session

    app.dependency_overrides[get_session] = override_session
    client = TestClient(app)

    response = client.post(
        "/v1/documents",
        json={
            "tenant_id": "matismart",
            "project_id": "pilot",
            "canonical_document_id": "onedrive-item-001",
            "title": "Battery Specification",
            "source_uri": "onedrive://drive/items/onedrive-item-001",
            "source_checksum_sha256": "a" * 64,
            "source_version": "v1",
            "security_zone": "engineering",
        },
    )

    assert response.status_code == 202
    assert response.json()["status"] == "RAW"
    assert response.json()["document_version_id"]

    tenant = session.scalar(select(Tenant).where(Tenant.slug == "matismart"))
    project = session.scalar(select(Project).where(Project.slug == "pilot"))
    document = session.scalar(select(Document).where(Document.canonical_document_id == "onedrive-item-001"))
    version = session.scalar(select(DocumentVersion).where(DocumentVersion.document_id == document.id))

    assert tenant is not None
    assert project is not None
    assert document.status == "RAW"
    assert document.security_zone == "engineering"
    assert version.source_checksum_sha256 == "a" * 64
    assert version.status == "RAW"

    app.dependency_overrides.clear()
    session.close()


def test_register_document_is_idempotent_for_same_checksum():
    session_iterator = build_test_session()
    session = next(session_iterator)

    def override_session() -> Iterator[Session]:
        yield session

    app.dependency_overrides[get_session] = override_session
    client = TestClient(app)
    payload = {
        "tenant_id": "matismart",
        "project_id": "pilot",
        "canonical_document_id": "onedrive-item-001",
        "title": "Battery Specification",
        "source_uri": "onedrive://drive/items/onedrive-item-001",
        "source_checksum_sha256": "b" * 64,
    }

    first = client.post("/v1/documents", json=payload)
    second = client.post("/v1/documents", json=payload)

    assert first.status_code == 202
    assert second.status_code == 202
    assert first.json()["document_version_id"] == second.json()["document_version_id"]
    assert len(session.scalars(select(Document)).all()) == 1
    assert len(session.scalars(select(DocumentVersion)).all()) == 1

    app.dependency_overrides.clear()
    session.close()
