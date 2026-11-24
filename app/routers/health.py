"""Health, readiness and metrics endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends, Response
from fastapi.responses import PlainTextResponse

from app.config import Settings, get_settings
from app.metrics import CONTENT_TYPE_LATEST, render_metrics

router = APIRouter(tags=["platform"])


@router.get("/healthz")
def healthz() -> dict[str, str]:
    """Liveness probe: process is up."""
    return {"status": "ok"}


@router.get("/readyz")
def readyz(settings: Annotated[Settings, Depends(get_settings)]) -> Response:
    """Readiness probe: service is ready to serve traffic."""
    if settings.fail_readiness:
        return Response(
            content='{"status": "not ready"}',
            status_code=503,
            media_type="application/json",
        )
    return Response(content='{"status": "ready"}', media_type="application/json")


@router.get("/metrics", include_in_schema=False)
def metrics() -> PlainTextResponse:
    """Prometheus text exposition endpoint."""
    return PlainTextResponse(render_metrics(), media_type=CONTENT_TYPE_LATEST)
