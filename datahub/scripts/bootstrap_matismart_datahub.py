import os
from pathlib import Path

import yaml
from datahub.emitter.mce_builder import make_dataset_urn
from datahub.emitter.mcp import MetadataChangeProposalWrapper
from datahub.emitter.rest_emitter import DatahubRestEmitter
from datahub.metadata.schema_classes import (
    ChangeTypeClass,
    CorpGroupInfoClass,
    DatasetPropertiesClass,
    DomainPropertiesClass,
    DomainsClass,
    GlobalTagsClass,
    GlossaryTermInfoClass,
    GlossaryTermsClass,
    OwnershipClass,
    OwnerClass,
    OwnershipTypeClass,
    TagAssociationClass,
    TagPropertiesClass,
    UpstreamClass,
    UpstreamLineageClass,
)


ROOT = Path(__file__).resolve().parents[1]
ENV = os.getenv("DATAHUB_ENV", "PROD")


def read_yaml(name: str) -> dict:
    with (ROOT / "metadata" / name).open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def emit_aspect(emitter: DatahubRestEmitter, entity_urn: str, aspect) -> None:
    emitter.emit(
        MetadataChangeProposalWrapper(
            entityUrn=entity_urn,
            aspect=aspect,
            changeType=ChangeTypeClass.UPSERT,
        )
    )


def tag_urn(name: str) -> str:
    return f"urn:li:tag:{name}"


def domain_urn(domain_id: str) -> str:
    return f"urn:li:domain:{domain_id}"


def glossary_term_urn(term_name: str) -> str:
    normalized = term_name.lower().replace(" ", "_").replace("/", "_")
    return f"urn:li:glossaryTerm:matismart.{normalized}"


def owner_aspect(owner_urns: list[str]) -> OwnershipClass:
    return OwnershipClass(
        owners=[
            OwnerClass(owner=owner_urn, type=OwnershipTypeClass.TECHNICAL_OWNER)
            for owner_urn in owner_urns
        ]
    )


def bootstrap_domains(emitter: DatahubRestEmitter) -> None:
    data = read_yaml("domains.yml")
    for domain in data["domains"]:
        urn = domain_urn(domain["id"])
        emit_aspect(
            emitter,
            urn,
            DomainPropertiesClass(
                name=domain["name"],
                description=domain["description"],
            ),
        )
        emit_aspect(emitter, urn, owner_aspect(domain.get("owners", [])))


def bootstrap_tags(emitter: DatahubRestEmitter) -> None:
    for tag in read_yaml("tags.yml")["tags"]:
        emit_aspect(
            emitter,
            tag_urn(tag["name"]),
            TagPropertiesClass(
                name=tag["name"],
                description=tag["description"],
            ),
        )


def bootstrap_groups(emitter: DatahubRestEmitter) -> None:
    for group in read_yaml("ownership.yml")["groups"]:
        emit_aspect(
            emitter,
            group["urn"],
            CorpGroupInfoClass(
                displayName=group["display_name"],
                description=group["role"],
            ),
        )


def bootstrap_glossary(emitter: DatahubRestEmitter) -> None:
    glossary = read_yaml("glossary.yml")["glossary"]
    for node in glossary["nodes"]:
        for term in node["terms"]:
            emit_aspect(
                emitter,
                glossary_term_urn(term["name"]),
                GlossaryTermInfoClass(
                    name=term["name"],
                    definition=term["description"],
                    termSource="Matismart",
                    sourceRef=node["name"],
                ),
            )


def bootstrap_datasets(emitter: DatahubRestEmitter) -> None:
    domains_by_id = {
        domain["id"]: domain for domain in read_yaml("domains.yml")["domains"]
    }
    for asset in read_yaml("knowledge-assets.yml")["datasets"]:
        urn = make_dataset_urn(asset["platform"], asset["name"], ENV)
        emit_aspect(
            emitter,
            urn,
            DatasetPropertiesClass(
                name=asset["display_name"],
                description=asset["description"],
                customProperties={"matismart_source_policy": "onedrive_source_of_truth"},
            ),
        )
        emit_aspect(emitter, urn, DomainsClass(domains=[domain_urn(asset["domain"])]))
        emit_aspect(
            emitter,
            urn,
            GlobalTagsClass(
                tags=[TagAssociationClass(tag=tag_urn(tag)) for tag in asset["tags"]]
            ),
        )
        owners = domains_by_id[asset["domain"]].get("owners", [])
        emit_aspect(emitter, urn, owner_aspect(owners))


def bootstrap_lineage(emitter: DatahubRestEmitter) -> None:
    downstream_to_upstreams: dict[str, list[UpstreamClass]] = {}
    for edge in read_yaml("lineage.yml")["lineage"]:
        downstream_to_upstreams.setdefault(edge["downstream"], []).append(
            UpstreamClass(dataset=edge["upstream"], type="TRANSFORMED")
        )
    for downstream, upstreams in downstream_to_upstreams.items():
        emit_aspect(emitter, downstream, UpstreamLineageClass(upstreams=upstreams))


def main() -> None:
    server = os.environ["DATAHUB_GMS_URL"]
    token = os.environ.get("DATAHUB_TOKEN")
    emitter = DatahubRestEmitter(gms_server=server, token=token)
    bootstrap_groups(emitter)
    bootstrap_domains(emitter)
    bootstrap_tags(emitter)
    bootstrap_glossary(emitter)
    bootstrap_datasets(emitter)
    bootstrap_lineage(emitter)


if __name__ == "__main__":
    main()
