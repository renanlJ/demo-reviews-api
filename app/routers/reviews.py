"""Review endpoints."""

from fastapi import APIRouter, HTTPException

from app import store
from app.models import Review

router = APIRouter(prefix="/api/v1", tags=["reviews"])


@router.get("/reviews/{product_id}", response_model=list[Review])
def get_reviews(product_id: str) -> list[Review]:
    """Return all customer reviews for a product."""
    if not store.product_exists(product_id):
        raise HTTPException(status_code=404, detail="product not found")
    return store.reviews_for(product_id)


@router.get("/reviews", response_model=list[Review])
def list_reviews() -> list[Review]:
    """Return every review in the catalog, ordered by creation date."""
    return store.all_reviews()
