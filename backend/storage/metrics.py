# backend/storage/metrics.py
"""Metrics and analytics storage."""

import json
import logging
import os
from datetime import datetime
from typing import Dict, List

from backend.config import settings

logger = logging.getLogger(__name__)


class MetricsStore:
    """Tracks agent performance, token usage, costs, and errors."""

    def __init__(self):
        self._metrics: List[dict] = []
        self._errors: List[dict] = []
        self._file = os.path.join(settings.DATA_DIR, "metrics.json")
        os.makedirs(settings.DATA_DIR, exist_ok=True)
        self._load()

    def _load(self):
        if os.path.exists(self._file):
            try:
                with open(self._file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self._metrics = data.get("metrics", [])
                    self._errors = data.get("errors", [])
            except Exception as e:
                logger.warning(f"Could not load metrics: {e}")

    def _save(self):
        try:
            with open(self._file, "w", encoding="utf-8") as f:
                json.dump({"metrics": self._metrics[-500:], "errors": self._errors[-200:]}, f, indent=2, default=str)
        except Exception as e:
            logger.warning(f"Could not save metrics: {e}")

    def record_task(self, task_id: str, agent_metrics: List[dict], total_tokens: int, execution_time: float):
        cost = (total_tokens / 1000) * settings.TOKEN_COST_PER_1K
        entry = {
            "task_id": task_id,
            "timestamp": datetime.now().isoformat(),
            "agents": agent_metrics,
            "total_tokens": total_tokens,
            "estimated_cost_usd": round(cost, 4),
            "execution_time": execution_time,
        }
        self._metrics.append(entry)
        self._save()

    def record_error(self, source: str, error: str, task_id: str = None):
        self._errors.append({
            "timestamp": datetime.now().isoformat(),
            "source": source,
            "error": error,
            "task_id": task_id,
        })
        self._save()

    def get_summary(self) -> dict:
        if not self._metrics:
            return {
                "total_tasks": 0,
                "total_tokens": 0,
                "total_cost_usd": 0.0,
                "avg_execution_time": 0.0,
                "agent_performance": {},
                "error_count": len(self._errors),
                "recent_errors": self._errors[-5:],
            }

        total_tokens = sum(m["total_tokens"] for m in self._metrics)
        total_cost = sum(m["estimated_cost_usd"] for m in self._metrics)
        avg_time = sum(m["execution_time"] for m in self._metrics) / len(self._metrics)

        agent_stats: Dict[str, dict] = {}
        for m in self._metrics:
            for agent in m.get("agents", []):
                name = agent["agent_name"]
                if name not in agent_stats:
                    agent_stats[name] = {"calls": 0, "total_tokens": 0, "total_time": 0.0, "failures": 0}
                agent_stats[name]["calls"] += 1
                agent_stats[name]["total_tokens"] += agent.get("tokens_used", 0)
                agent_stats[name]["total_time"] += agent.get("execution_time", 0)
                if not agent.get("success", True):
                    agent_stats[name]["failures"] += 1

        for name in agent_stats:
            stats = agent_stats[name]
            stats["avg_tokens"] = round(stats["total_tokens"] / stats["calls"], 1)
            stats["avg_time"] = round(stats["total_time"] / stats["calls"], 2)

        return {
            "total_tasks": len(self._metrics),
            "total_tokens": total_tokens,
            "total_cost_usd": round(total_cost, 4),
            "avg_execution_time": round(avg_time, 2),
            "agent_performance": agent_stats,
            "error_count": len(self._errors),
            "recent_errors": self._errors[-5:],
        }

    def get_recent_tasks(self, limit: int = 10) -> List[dict]:
        return list(reversed(self._metrics[-limit:]))


metrics_store = MetricsStore()
