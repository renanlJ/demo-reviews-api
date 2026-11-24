from fastapi.testclient import TestClient


def test_get_reviews_for_product(client: TestClient) -> None:
    resp = client.get("/api/v1/reviews/SKU-1001")
    assert resp.status_code == 200
    body = resp.json()
    assert len(body) == 3
    for review in body:
        assert review["productId"] == "SKU-1001"
        assert 1 <= review["rating"] <= 5
        assert review["reviewer"]
        assert review["text"]
        assert review["createdAt"]


def test_get_reviews_unknown_product_404(client: TestClient) -> None:
    resp = client.get("/api/v1/reviews/SKU-9999")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "product not found"


def test_list_all_reviews(client: TestClient) -> None:
    resp = client.get("/api/v1/reviews")
    assert resp.status_code == 200
    body = resp.json()
    assert len(body) == 8
    created = [r["createdAt"] for r in body]
    assert created == sorted(created)
