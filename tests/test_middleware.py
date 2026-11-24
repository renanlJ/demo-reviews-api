from fastapi.testclient import TestClient


def test_request_id_generated_and_echoed(client: TestClient) -> None:
    resp = client.get("/healthz")
    request_id = resp.headers.get("x-request-id")
    assert request_id is not None
    assert len(request_id) == 32


def test_request_id_propagated(client: TestClient) -> None:
    resp = client.get("/healthz", headers={"X-Request-ID": "req-42"})
    assert resp.headers["x-request-id"] == "req-42"


def test_metrics_recorded_with_route_labels(client: TestClient) -> None:
    client.get("/api/v1/reviews/SKU-1002")
    resp = client.get("/metrics")
    assert 'route="/api/v1/reviews/{product_id}"' in resp.text
    assert 'status="200"' in resp.text
    assert "http_request_duration_seconds_bucket" in resp.text
