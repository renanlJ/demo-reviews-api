"""Pure-ASGI observability middleware.

Wraps every HTTP request with:
  * X-Request-ID generation/propagation (echoed on the response)
  * W3C traceparent parsing (trace_id bound to log context)
  * structured JSON access logging
  * Prometheus request/error/duration metrics
"""

import re
import time
import uuid

import structlog
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from app.metrics import ERROR_COUNT, REQUEST_COUNT, REQUEST_DURATION

_TRACEPARENT_RE = re.compile(r"^[0-9a-f]{2}-([0-9a-f]{32})-[0-9a-f]{16}-[0-9a-f]{2}$")


def _parse_traceparent(value: str) -> str:
    match = _TRACEPARENT_RE.match(value.lower())
    return match.group(1) if match else ""


class ObservabilityMiddleware:
    """ASGI middleware providing correlation IDs, logging and metrics."""

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        start = time.perf_counter()
        headers = {k.decode(): v.decode() for k, v in scope.get("headers", [])}
        request_id = headers.get("x-request-id", "").strip() or uuid.uuid4().hex
        trace_id = _parse_traceparent(headers.get("traceparent", ""))
        status = 500

        async def send_wrapper(message: Message) -> None:
            nonlocal status
            if message["type"] == "http.response.start":
                status = message["status"]
                response_headers = list(message.get("headers", []))
                response_headers.append((b"x-request-id", request_id.encode()))
                message["headers"] = response_headers
            await send(message)

        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(request_id=request_id, trace_id=trace_id)
        logger = structlog.get_logger("demo-reviews-api")

        try:
            await self.app(scope, receive, send_wrapper)
        finally:
            duration = time.perf_counter() - start
            route = scope.get("route")
            route_path = getattr(route, "path", None) or scope.get("path", "")
            labels = {
                "method": scope["method"],
                "route": route_path,
                "status": str(status),
            }
            REQUEST_COUNT.labels(**labels).inc()
            REQUEST_DURATION.labels(**labels).observe(duration)
            if status >= 500:
                ERROR_COUNT.labels(**labels).inc()
            logger.info(
                "http request",
                method=scope["method"],
                route=route_path,
                path=scope.get("path", ""),
                status=status,
                duration_ms=round(duration * 1000, 2),
                remote_addr=scope.get("client", ["", 0])[0],
            )
