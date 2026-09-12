# Технічне завдання: Matismart Knowledge & AI Integration Hub

Версія: `1.0-current`

Дата: `2026-09-13`

Репозиторій: `https://github.com/boss240/matismart-knowledge-hub`

## 1. Назва продукту

**Matismart Knowledge & AI Integration Hub**.

Скорочена назва: **Matismart Knowledge Hub**.

## 2. Призначення

Matismart Knowledge Hub є production-орієнтованим сервісом для перетворення документів Matismart у керовану, перевірювану та придатну для AI базу знань.

Система не замінює OneDrive, SharePoint, інженерів або робочий документообіг. Вона створює контрольований шар між джерелами документів і AI-платформою:

```text
OneDrive -> Microsoft Graph -> Ingestion -> Processing -> PostgreSQL/pgvector -> RAG -> Matismart AI Platform
```

Базовий принцип:

```text
OneDrive = джерело істини
DataHub = каталог метаданих, governance та lineage
PostgreSQL/pgvector = операційне сховище знань
Matismart AI Platform = споживач затверджених знань
```

## 3. Бізнес-проблема

Документи Matismart можуть існувати у вигляді технічних описів, комерційних матеріалів, проектних файлів, регуляторних документів, таблиць, презентацій, сканів, креслень та майбутніх AI-висновків.

Без контрольованого knowledge-layer виникають ризики:

- AI може відповідати на основі застарілої версії документа;
- незрозуміло, який файл є чинним джерелом;
- відсутня прозора прив'язка відповіді AI до документа, версії та фрагмента;
- немає контрольованого статусу `draft/reviewed/approved/published`;
- складно визначити власника документа або домену знань;
- немає єдиної lineage-моделі від OneDrive до AI-відповіді;
- складно відокремити технічні, комерційні, регуляторні та клієнтські знання.

## 4. Цілі системи

Система повинна:

- реєструвати документи та версії документів;
- зберігати tenant/project контекст;
- зберігати source URI, checksum, source version, security zone;
- підтримувати workflow станів документа;
- готувати дані для chunking, embeddings та RAG;
- забезпечувати provenance та citations для AI-відповідей;
- інтегруватися з DataHub як governance/catalog layer;
- підтримувати PostgreSQL/pgvector як перше операційне сховище;
- не зберігати секрети в репозиторії;
- мати автоматизовані тести та CI;
- бути розширюваною до Microsoft Graph, Gemini, Knowledge Graph, NotebookLM та інших майбутніх інтеграцій.

## 5. Поточний статус реалізації

Стан на `2026-09-13`:

- репозиторій створено і підключено до GitHub;
- структура сервісу підготовлена;
- FastAPI application skeleton реалізовано;
- SQLAlchemy database layer реалізовано;
- Alembic migrations додано;
- документну модель `Tenant -> Project -> Document -> DocumentVersion` реалізовано;
- реалізовано API реєстрації документа;
- реалізовано API читання одного документа;
- реалізовано API списку документів;
- додано approval/query skeleton;
- підготовлено DataHub metadata-as-code;
- підготовлено DataHub ingestion recipes;
- підготовлено lineage OneDrive -> Matismart AI Platform;
- додано продуктову документацію;
- CI проходить тести та перевірку міграцій.

Важливе обмеження:

**DataHub live deployment ще не виконаний**, тому що для цього потрібні реальні значення `DATAHUB_GMS_URL`, `DATAHUB_TOKEN` та PostgreSQL credentials. У репозиторії підготовлена конфігурація, але секрети не зберігаються і не повинні комітитися.

## 6. Користувачі

### 6.1. Інженери

Потребують доступу до чинних технічних документів, специфікацій, розрахунків, проектних рішень та обладнання з посиланнями на джерела.

### 6.2. Проектні менеджери

Потребують структурованої бази знань за проектами, клієнтами, статусами, рішеннями та документами.

### 6.3. Комерційна команда

Потребує затверджених фактів і матеріалів для пропозицій, презентацій та комунікації з клієнтами.

### 6.4. AI-платформа Matismart

Потребує доступу тільки до знань, які мають джерела, статус, provenance, citations і governance context.

### 6.5. Governance / Compliance

Потребують DataHub domains, glossary, tags, ownership, lineage та audit trail.

## 7. Функціональні вимоги

### 7.1. Реєстрація документів

Система повинна приймати документ через REST API та створювати:

- tenant;
- project;
- canonical document record;
- document version;
- workflow state;
- checksum або fallback checksum;
- source URI;
- source system;
- security zone.

Поточний endpoint:

```text
POST /v1/documents
```

### 7.2. Читання документів

Система повинна надавати читання зареєстрованих документів.

Поточні endpoints:

```text
GET /v1/documents/{id}
GET /v1/documents
```

Параметри:

- `tenant_id` є обов'язковим;
- `project_id` є опційним для списку;
- `limit` підтримує значення від `1` до `500`;
- `offset` підтримує pagination.

### 7.3. Workflow документів

Система повинна підтримувати стани:

```text
RAW
INGESTED
AI_PROCESSED
ENGINEER_REVIEWED
APPROVED
PUBLISHED
REJECTED
SUPERSEDED
```

Основний шлях:

```text
RAW -> INGESTED -> AI_PROCESSED -> ENGINEER_REVIEWED -> APPROVED -> PUBLISHED
```

### 7.4. Approval workflow

Система повинна підтримувати review decisions:

```text
APPROVE
REJECT
REQUEST_CHANGES
```

Поточний skeleton endpoint:

```text
POST /v1/approvals/{document_version_id}
```

### 7.5. Query/RAG API

Система повинна мати RAG API для майбутніх AI-запитів.

Поточний skeleton endpoint:

```text
POST /v1/query
```

Майбутні вимоги:

- hybrid retrieval;
- citations;
- provenance;
- tenant/project/security filtering;
- Gemini adapter;
- query audit trail;
- refusal behavior, якщо немає джерел або знання не затверджені.

### 7.6. DataHub governance

Система повинна описувати в DataHub:

- domains;
- glossary;
- tags;
- ownership;
- lineage;
- PostgreSQL/pgvector ingestion;
- knowledge datasets;
- API/catalog assets.

Поточні домени:

- Product Knowledge
- Technical Documentation
- Customer Projects
- AI Knowledge
- Energy Assets
- IoT & Tuya
- EMS
- Commercial
- Regulatory

### 7.7. Lineage

Цільова lineage-модель:

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

## 8. Нефункціональні вимоги

### 8.1. Безпека

- не комітити секрети;
- використовувати environment variables або GitHub Actions secrets;
- tenant/project isolation;
- security zone для документів;
- audit trail для критичних дій;
- citations/provenance для AI-відповідей;
- не дозволяти AI публікувати знання без review/approval.

### 8.2. Надійність

- database migrations через Alembic;
- automated tests;
- CI на GitHub Actions;
- явна валідація DataHub metadata;
- repeatable local setup.

### 8.3. Масштабованість

Архітектура повинна дозволяти додати:

- Microsoft Graph delta sync;
- webhook events;
- document processing workers;
- chunking;
- pgvector embeddings;
- Knowledge Graph;
- Gemini/RAG runtime;
- NotebookLM/Google Drive bridge;
- DataHub live sync.

### 8.4. Спостережуваність

Система повинна мати основу для:

- structured logs;
- metrics;
- traces;
- ingestion errors;
- retries;
- DLQ для processing failures;
- audit events.

## 9. Поточна архітектура

```text
apps/api
  FastAPI REST API

packages/domain
  Pydantic models, statuses, request/response contracts

packages/database
  SQLAlchemy models, session, repositories

database/alembic
  schema migrations

datahub
  metadata-as-code, ingestion recipes, bootstrap script

docs
  product, architecture, DataHub, ADR, specification

tests
  unit/API/database tests
```

## 10. Поточні API

| Endpoint | Статус | Призначення |
| --- | --- | --- |
| `GET /healthz` | реалізовано | health check |
| `POST /v1/documents` | реалізовано | реєстрація документа |
| `GET /v1/documents/{id}` | реалізовано | читання одного документа |
| `GET /v1/documents` | реалізовано | список документів |
| `POST /v1/approvals/{document_version_id}` | skeleton | review decision |
| `POST /v1/query` | skeleton | майбутній RAG-запит |

## 11. Поточна модель даних

Реалізовані таблиці:

- `tenants`;
- `projects`;
- `documents`;
- `document_versions`.

Закладена доменна модель:

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

Поточна база вже має foundation для розширення в бік chunks, embeddings, approvals, audit і citations.

## 12. DataHub модель

Підготовлені файли:

- `datahub/metadata/domains.yml`;
- `datahub/metadata/glossary.yml`;
- `datahub/metadata/tags.yml`;
- `datahub/metadata/ownership.yml`;
- `datahub/metadata/lineage.yml`;
- `datahub/metadata/knowledge-assets.yml`;
- `datahub/ingestion/postgres-pgvector.yml`;
- `datahub/ingestion/metadata-bootstrap.yml`;
- `datahub/ingestion/business-glossary.yml`;
- `datahub/scripts/bootstrap_matismart_datahub.py`.

## 13. GitHub Actions

Поточні workflows:

- `Python CI` перевіряє Alembic migrations та тести;
- `DataHub Metadata Sync` валідує metadata на push;
- live apply до DataHub доступний тільки через manual workflow dispatch з `apply_to_datahub=true` і реальними secrets.

## 14. Acceptance criteria для поточної версії

Поточна версія вважається прийнятою, якщо:

- репозиторій синхронізований з GitHub;
- локальний робочий каталог чистий;
- `pytest -q` проходить;
- GitHub Actions `Python CI` проходить;
- Alembic history/upgrade SQL перевіряється;
- API документів має registration/read/list;
- DataHub конфігурації не містять секретів;
- документація містить опис продукту, архітектуру, DataHub setup, lineage та це ТЗ.

## 15. Межі поточної версії

Реалізовано:

- skeleton production service;
- API foundation;
- DB foundation;
- migrations;
- document registration;
- document reading;
- tests;
- DataHub metadata/config foundation;
- продуктова документація.

Не реалізовано повністю:

- live Microsoft Graph connector;
- live OneDrive delta sync;
- document content extraction;
- chunking records;
- pgvector embedding runtime;
- Gemini/RAG runtime;
- production authentication/authorization;
- live DataHub apply;
- engineer review UI.

## 16. Наступний етап

Наступний технічно правильний етап:

```text
Ingestion worker -> source metadata -> document version -> chunk records -> embeddings-ready pipeline
```

Рекомендована черговість:

1. Додати таблиці `document_chunks`, `embeddings`, `approvals`, `audit_events`, `query_citations`.
2. Додати ingestion service interface.
3. Додати локальний file/fixture ingestion для тестування без Microsoft Graph.
4. Додати chunking pipeline.
5. Додати pgvector-ready embedding contract.
6. Додати RAG query path тільки після появи citations і approved state filtering.

## 17. Правила безпеки секретів

У репозиторій не вносити:

- `DATAHUB_TOKEN`;
- PostgreSQL password;
- Microsoft Graph client secret;
- Gemini API key;
- private OneDrive/SharePoint credentials;
- `.env` файли з реальними значеннями.

Дозволено комітити:

- `.env.example`;
- YAML recipes з environment variable placeholders;
- документацію;
- tests;
- scripts без hardcoded credentials.

## 18. Висновок

Matismart Knowledge Hub вже має робочий foundation: API, database model, migrations, tests, CI, DataHub metadata-as-code і документацію.

Ключова цінність продукту: створити контрольований шлях від документів у OneDrive до AI-відповідей Matismart з версіями, власниками, статусами, lineage, citations і human approval.

