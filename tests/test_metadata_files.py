from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def load(name: str):
    with (ROOT / "datahub" / "metadata" / name).open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def test_required_domains_are_defined():
    domains = {domain["name"] for domain in load("domains.yml")["domains"]}
    assert domains == {
        "Product Knowledge",
        "Technical Documentation",
        "Customer Projects",
        "AI Knowledge",
        "Energy Assets",
        "IoT & Tuya",
        "EMS",
        "Commercial",
        "Regulatory",
    }


def test_no_secret_literals_in_ingestion_recipes():
    for path in (ROOT / "datahub" / "ingestion").glob("*.yml"):
        text = path.read_text(encoding="utf-8").lower()
        assert "replace-locally" not in text
        assert "password:" not in text or "${postgres_password}" in text
        assert "token:" not in text or "${datahub_token}" in text


def test_lineage_has_onedrive_to_ai_platform_path():
    edges = load("lineage.yml")["lineage"]
    upstreams = {edge["upstream"] for edge in edges}
    downstreams = {edge["downstream"] for edge in edges}
    assert any("onedrive" in urn for urn in upstreams)
    assert any("matismart_ai_platform" in urn for urn in downstreams)

