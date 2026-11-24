"""Structured JSON logging configuration built on structlog."""

import logging
import sys

import structlog


def configure_logging(level: str = "info") -> None:
    """Configure stdlib logging and structlog for JSON output."""
    numeric = getattr(logging, level.upper(), logging.INFO)
    logging.basicConfig(format="%(message)s", stream=sys.stdout, level=numeric)

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso", utc=True, key="time"),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(numeric),
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger() -> structlog.typing.FilteringBoundLogger:
    """Return a configured structlog logger."""
    return structlog.get_logger("demo-reviews-api")
