from packages.domain.models import DocumentCreate, DocumentStatus, QueryRequest


def test_document_status_workflow_values_are_stable():
    assert [status.value for status in DocumentStatus] == [
        "RAW",
        "INGESTED",
        "AI_PROCESSED",
        "ENGINEER_REVIEWED",
        "APPROVED",
        "PUBLISHED",
        "REJECTED",
        "SUPERSEDED",
    ]


def test_document_create_contract_accepts_onedrive_source():
    payload = DocumentCreate(
        tenant_id="matismart",
        project_id="demo",
        canonical_document_id="doc-001",
        title="Example",
        source_uri="onedrive://drive/items/doc-001",
    )

    assert payload.security_zone == "default"


def test_query_request_limits_citations():
    payload = QueryRequest(
        tenant_id="matismart",
        project_id="demo",
        question="What is approved?",
    )

    assert payload.max_citations == 8

