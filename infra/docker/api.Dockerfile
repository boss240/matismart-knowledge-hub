FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml README.md ./
COPY apps ./apps
COPY alembic.ini ./
COPY database ./database
COPY packages ./packages

RUN pip install --no-cache-dir -e ".[api]"

EXPOSE 8000

CMD ["sh", "-c", "alembic upgrade head && uvicorn apps.api.main:app --host 0.0.0.0 --port 8000"]
