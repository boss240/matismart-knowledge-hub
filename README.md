# Matismart Knowledge Hub

Production service skeleton for Matismart Knowledge & AI Integration Hub.

## Governance principle

- OneDrive is the source of truth for business and technical documents.
- DataHub is the metadata and governance catalog.
- Secrets are never committed. Use environment variables or CI secrets.

## DataHub scope

This repository prepares DataHub metadata for:

- Domains: Product Knowledge, Technical Documentation, Customer Projects, AI Knowledge, Energy Assets, IoT & Tuya, EMS, Commercial, Regulatory
- Business glossary, tags, and ownership model
- PostgreSQL/pgvector ingestion
- Future knowledge datasets and API catalog assets
- Lineage from OneDrive through RAG into Matismart AI Platform

## First run

```powershell
cd matismart-knowledge-hub
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[datahub]"
Copy-Item .env.example .env
```

Edit `.env` locally, then run:

```powershell
datahub ingest -c datahub/ingestion/postgres-pgvector.yml
python datahub/scripts/bootstrap_matismart_datahub.py
```

For CI, configure repository secrets `DATAHUB_GMS_URL`, `DATAHUB_TOKEN`, `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_DATABASE`, `POSTGRES_USERNAME`, and `POSTGRES_PASSWORD`.

