"""Deterministic in-memory review fixtures.

The product IDs are shared across all Demo Commerce Platform services so the
product-api orchestrator can correlate responses.
"""

from datetime import UTC, datetime

from app.models import Review

_PRODUCT_IDS = {"SKU-1001", "SKU-1002", "SKU-1003"}

_REVIEWS: dict[str, list[Review]] = {
    "SKU-1001": [
        Review(
            id="rev-1001-1",
            product_id="SKU-1001",
            reviewer="alice.m",
            text="Brews excellent coffee and the timer function is reliable every morning.",
            rating=5,
            created_at=datetime(2026, 9, 14, 8, 32, 0, tzinfo=UTC),
        ),
        Review(
            id="rev-1001-2",
            product_id="SKU-1001",
            reviewer="bob.k",
            text="Solid machine, though the carafe lid feels a bit flimsy.",
            rating=4,
            created_at=datetime(2026, 9, 30, 17, 5, 0, tzinfo=UTC),
        ),
        Review(
            id="rev-1001-3",
            product_id="SKU-1001",
            reviewer="carol.s",
            text="Replaced my old percolator and I could not be happier. Highly recommended.",
            rating=5,
            created_at=datetime(2026, 10, 21, 12, 47, 0, tzinfo=UTC),
        ),
    ],
    "SKU-1002": [
        Review(
            id="rev-1002-1",
            product_id="SKU-1002",
            reviewer="dave.r",
            text="Great tactile feedback. The hot-swappable switches are a nice touch.",
            rating=5,
            created_at=datetime(2026, 8, 19, 9, 12, 0, tzinfo=UTC),
        ),
        Review(
            id="rev-1002-2",
            product_id="SKU-1002",
            reviewer="erin.t",
            text="Good keyboard overall; the stock keycaps show shine quickly though.",
            rating=4,
            created_at=datetime(2026, 10, 2, 20, 41, 0, tzinfo=UTC),
        ),
    ],
    "SKU-1003": [
        Review(
            id="rev-1003-1",
            product_id="SKU-1003",
            reviewer="frank.l",
            text="Motor is quiet and memory presets work well. Assembly took longer than expected.",
            rating=4,
            created_at=datetime(2026, 7, 25, 14, 3, 0, tzinfo=UTC),
        ),
        Review(
            id="rev-1003-2",
            product_id="SKU-1003",
            reviewer="grace.p",
            text="Desk surface scratches easily. Functional but the finish could be better.",
            rating=3,
            created_at=datetime(2026, 9, 8, 11, 26, 0, tzinfo=UTC),
        ),
        Review(
            id="rev-1003-3",
            product_id="SKU-1003",
            reviewer="henry.w",
            text="Wobbles slightly at max height. Customer support was unhelpful.",
            rating=2,
            created_at=datetime(2026, 10, 30, 16, 58, 0, tzinfo=UTC),
        ),
    ],
}


def product_exists(product_id: str) -> bool:
    """Return True when the product ID is part of the demo catalog."""
    return product_id in _PRODUCT_IDS


def reviews_for(product_id: str) -> list[Review]:
    """Return all reviews for a product (possibly empty)."""
    return list(_REVIEWS.get(product_id, []))


def all_reviews() -> list[Review]:
    """Return every review across all products, ordered by creation date."""
    out = [r for reviews in _REVIEWS.values() for r in reviews]
    return sorted(out, key=lambda r: r.created_at)
