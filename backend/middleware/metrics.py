# backend/middleware/metrics.py
"""Request metrics middleware."""

import logging
import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

logger = logging.getLogger(__name__)

_request_count = 0
_total_latency = 0.0
_error_count = 0


class MetricsMiddleware(BaseHTTPMiddleware):
    """Tracks request count, latency, and errors."""

    async def dispatch(self, request: Request, call_next):
        global _request_count, _total_latency, _error_count
        start = time.perf_counter()
        _request_count += 1

        try:
            response = await call_next(request)
            if response.status_code >= 400:
                _error_count += 1
            return response
        except Exception:
            _error_count += 1
            raise
        finally:
            elapsed = time.perf_counter() - start
            _total_latency += elapsed
            logger.debug(f"{request.method} {request.url.path} - {elapsed:.3f}s")


def get_request_metrics() -> dict:
    avg_latency = _total_latency / _request_count if _request_count else 0
    return {
        "request_count": _request_count,
        "error_count": _error_count,
        "avg_latency_seconds": round(avg_latency, 3),
    }
