import pytest
from fastapi.testclient import TestClient

from app.config import Settings, get_settings
from app.main import app


def test_healthz(client: TestClient) -> None:
    resp = client.get("/healthz")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_readyz(client: TestClient) -> None:
    resp = client.get("/readyz")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ready"}


def test_readyz_fails_when_flagged(client: TestClient) -> None:
    app.dependency_overrides[get_settings] = lambda: Settings(fail_readiness=True)
    try:
        resp = client.get("/readyz")
        assert resp.status_code == 503
        assert resp.json() == {"status": "not ready"}
    finally:
        app.dependency_overrides.clear()


def test_metrics_endpoint(client: TestClient) -> None:
    client.get("/healthz")
    resp = client.get("/metrics")
    assert resp.status_code == 200
    assert resp.headers["content-type"].startswith("text/plain")
    assert "http_requests_total" in resp.text


@pytest.mark.parametrize("path", ["/openapi.json", "/docs"])
def test_api_documentation_available(client: TestClient, path: str) -> None:
    resp = client.get(path)
    assert resp.status_code == 200
