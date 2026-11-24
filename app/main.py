"""demo-reviews-api application entrypoint."""

from fastapi import FastAPI

from app.config import get_settings
from app.logging import configure_logging
from app.middleware import ObservabilityMiddleware
from app.routers import health, reviews
from app.telemetry import instrument_app

APP_VERSION = "0.1.0"

settings = get_settings()
configure_logging(settings.log_level)

app = FastAPI(
    title="demo-reviews-api",
    description=(
        "Customer reviews service for the Demo Commerce Platform. "
        "Provides per-product reviews consumed by demo-product-api."
    ),
    version=APP_VERSION,
)

app.add_middleware(ObservabilityMiddleware)
app.include_router(health.router)
app.include_router(reviews.router)

instrument_app(app, settings)
