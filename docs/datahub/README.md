# DataHub Governance Setup

## Operating model

OneDrive remains the source of truth for documents. DataHub stores metadata, ownership, glossary, tags, ingestion status, and lineage. PostgreSQL/pgvector stores normalized knowledge, chunks, embeddings, and approval state for the Matismart Knowledge Hub.

## Domains

The repository defines these DataHub domains:

- Product Knowledge
- Technical Documentation
- Customer Projects
- AI Knowledge
- Energy Assets
- IoT & Tuya
- EMS
- Commercial
- Regulatory

Domain definitions live in `datahub/metadata/domains.yml`.

## Glossary, Tags, Ownership

- Glossary terms live in `datahub/metadata/glossary.yml`.
- Tags live in `datahub/metadata/tags.yml`.
- Ownership groups and default ownership policy live in `datahub/metadata/ownership.yml`.

The initial model separates product, engineering, projects, AI, energy, IoT, EMS, commercial, and compliance ownership. Replace placeholder group URNs with real DataHub corp groups when identity sync is connected.

## Ingestion

PostgreSQL/pgvector ingestion is configured in `datahub/ingestion/postgres-pgvector.yml`.

The recipe reads connection data from environment variables:

- `POSTGRES_HOST`
- `POSTGRES_PORT`
- `POSTGRES_DATABASE`
- `POSTGRES_USERNAME`
- `POSTGRES_PASSWORD`
- `DATAHUB_GMS_URL`
- `DATAHUB_TOKEN`

No credentials should be committed.

## Lineage

Target lineage:

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

Lineage edges live in `datahub/metadata/lineage.yml` and are emitted by `datahub/scripts/bootstrap_matismart_datahub.py`.

## Apply to DataHub

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[datahub]"

$env:DATAHUB_GMS_URL="https://your-datahub.example.com/api/gms"
$env:DATAHUB_TOKEN="..."
$env:POSTGRES_HOST="..."
$env:POSTGRES_PORT="5432"
$env:POSTGRES_DATABASE="matismart_knowledge"
$env:POSTGRES_USERNAME="..."
$env:POSTGRES_PASSWORD="..."

datahub ingest -c datahub/ingestion/postgres-pgvector.yml
python datahub/scripts/bootstrap_matismart_datahub.py
```

## Validation

After applying metadata, validate in DataHub:

1. Domains exist and have owners.
2. Tags exist and are attached to Matismart datasets.
3. Glossary contains source governance, AI governance, and security terms.
4. PostgreSQL datasets are visible.
5. Lineage graph shows the full OneDrive to Matismart AI Platform path.

