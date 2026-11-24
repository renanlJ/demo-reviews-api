"""Prometheus metrics registry shared by middleware and the /metrics endpoint."""

from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total number of HTTP requests processed.",
    ["method", "route", "status"],
)
ERROR_COUNT = Counter(
    "http_requests_errors_total",
    "Total number of HTTP requests that returned a server error.",
    ["method", "route", "status"],
)
REQUEST_DURATION = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds.",
    ["method", "route", "status"],
)


def render_metrics() -> bytes:
    """Return the registry in Prometheus text exposition format."""
    return generate_latest()


__all__ = [
    "CONTENT_TYPE_LATEST",
    "REQUEST_COUNT",
    "ERROR_COUNT",
    "REQUEST_DURATION",
    "render_metrics",
]
