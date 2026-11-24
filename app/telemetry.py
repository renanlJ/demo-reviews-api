"""OpenTelemetry instrumentation, enabled via OTEL_EXPORTER_OTLP_ENDPOINT."""

import structlog
from fastapi import FastAPI

from app.config import Settings

logger = structlog.get_logger("demo-reviews-api")


def instrument_app(app: FastAPI, settings: Settings) -> None:
    """Attach OTel tracing when an OTLP endpoint is configured.

    Trace context is propagated via standard W3C traceparent headers; the
    middleware already extracts trace_id for log correlation.
    """
    if not settings.otel_exporter_otlp_endpoint:
        return

    try:
        from opentelemetry import trace
        from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
            OTLPSpanExporter,
        )
        from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
        from opentelemetry.sdk.resources import Resource
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import BatchSpanProcessor
    except ImportError:  # pragma: no cover - optional dependency guard
        logger.warning("otel packages unavailable; tracing disabled")
        return

    provider = TracerProvider(resource=Resource.create({"service.name": settings.service_name}))
    provider.add_span_processor(
        BatchSpanProcessor(
            OTLPSpanExporter(endpoint=f"{settings.otel_exporter_otlp_endpoint}/v1/traces")
        )
    )
    trace.set_tracer_provider(provider)
    FastAPIInstrumentor.instrument_app(app)
    logger.info("opentelemetry enabled", endpoint=settings.otel_exporter_otlp_endpoint)
