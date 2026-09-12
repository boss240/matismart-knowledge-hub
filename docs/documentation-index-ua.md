# Індекс документації Matismart Knowledge Hub

Дата актуалізації: `2026-09-13`

Репозиторій: `https://github.com/boss240/matismart-knowledge-hub`

## Головні документи

- [README](../README.md) - короткий старт, принципи governance, API, тести.
- [Опис продукту](product/product-description.md) - повний продуктовий опис Matismart Knowledge & AI Integration Hub.
- [Крайня версія ТЗ](specification/latest-technical-assignment-ua.md) - актуальне технічне завдання українською.

## Архітектура

- [Architecture Overview](architecture/overview.md) - короткий огляд архітектури.
- [DataHub Lineage](architecture/datahub-lineage.md) - lineage OneDrive -> Matismart AI Platform.
- [ADR 0001](adr/0001-source-of-truth-and-catalog.md) - рішення: OneDrive як source of truth, DataHub як catalog/governance layer.

## DataHub

- [DataHub README](datahub/README.md) - operating model, domains, glossary, tags, ownership, ingestion, secrets.
- [Domains](../datahub/metadata/domains.yml) - DataHub domains.
- [Glossary](../datahub/metadata/glossary.yml) - бізнес- і технічний словник.
- [Tags](../datahub/metadata/tags.yml) - governance tags.
- [Ownership](../datahub/metadata/ownership.yml) - ownership model.
- [Lineage](../datahub/metadata/lineage.yml) - lineage edges.
- [Knowledge Assets](../datahub/metadata/knowledge-assets.yml) - майбутні datasets/API/catalog assets.
- [PostgreSQL/pgvector ingestion](../datahub/ingestion/postgres-pgvector.yml) - ingestion recipe.
- [Metadata bootstrap](../datahub/ingestion/metadata-bootstrap.yml) - bootstrap metadata recipe.
- [Business glossary ingestion](../datahub/ingestion/business-glossary.yml) - glossary ingestion recipe.
- [Bootstrap script](../datahub/scripts/bootstrap_matismart_datahub.py) - script для емісії DataHub metadata.

## API та база даних

- `apps/api/main.py` - FastAPI application.
- `apps/api/routes/documents.py` - document registration/read/list API.
- `apps/api/routes/approvals.py` - approval endpoint skeleton.
- `apps/api/routes/query.py` - query/RAG endpoint skeleton.
- `packages/domain/models.py` - API/domain contracts.
- `packages/database/models.py` - SQLAlchemy database models.
- `packages/database/repositories.py` - document repository.
- `database/alembic/versions/20260814_0001_initial_schema.py` - поточна schema migration.

## CI/CD

- `.github/workflows/python-ci.yml` - тести та Alembic validation.
- `.github/workflows/datahub-metadata-sync.yml` - DataHub metadata validation/apply workflow.

## Поточна межа

Готово:

- API foundation;
- PostgreSQL/Alembic foundation;
- document registration;
- document read/list;
- tests;
- CI;
- DataHub metadata/configuration foundation;
- product/specification documentation.

Ще потребує реальних зовнішніх доступів:

- live DataHub apply;
- Microsoft Graph/OneDrive connector;
- live PostgreSQL environment;
- Gemini/RAG runtime;
- production secrets.

Секрети не зберігаються в репозиторії.

