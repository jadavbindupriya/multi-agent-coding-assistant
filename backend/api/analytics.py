# backend/api/analytics.py
"""Analytics and monitoring API (Phase 9)."""

from fastapi import APIRouter

from backend.storage.metrics import metrics_store
from backend.storage.tasks import task_store
from backend.middleware.metrics import get_request_metrics
router = APIRouter()


@router.get("/summary")
async def get_analytics_summary():
    """Get system performance metrics, token usage, and cost analysis."""
    summary = metrics_store.get_summary()
    return {**summary, "request_metrics": get_request_metrics()}


@router.get("/tasks/recent")
async def get_recent_tasks():
    """Get recent task execution records."""
    return {
        "tasks": task_store.list_recent(20),
        "metrics": metrics_store.get_recent_tasks(10),
    }


@router.get("/errors")
async def get_errors():
    """Get recent errors for monitoring."""
    summary = metrics_store.get_summary()
    return {"error_count": summary["error_count"], "recent_errors": summary["recent_errors"]}
