"""Pydantic models for the reviews API."""

from datetime import datetime

from pydantic import BaseModel, Field


class Review(BaseModel):
    """A single customer review."""

    id: str
    product_id: str = Field(serialization_alias="productId")
    reviewer: str
    text: str
    rating: int = Field(ge=1, le=5)
    created_at: datetime = Field(serialization_alias="createdAt")

    model_config = {"populate_by_name": True}
