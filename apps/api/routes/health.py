from fastapi import APIRouter

from apps.api.config import settings


router = APIRouter(tags=["health"])


@router.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok", "environment": settings.matismart_env}

