# backend/storage/tasks.py
"""In-memory task store with JSON persistence."""

import json
import logging
import os
from datetime import datetime
from typing import Dict, List, Optional

from backend.config import settings

logger = logging.getLogger(__name__)


class TaskStore:
    """Stores task execution state for status tracking."""

    def __init__(self):
        self._tasks: Dict[str, dict] = {}
        self._file = os.path.join(settings.DATA_DIR, "tasks.json")
        os.makedirs(settings.DATA_DIR, exist_ok=True)
        self._load()

    def _load(self):
        if os.path.exists(self._file):
            try:
                with open(self._file, "r", encoding="utf-8") as f:
                    self._tasks = json.load(f)
            except Exception as e:
                logger.warning(f"Could not load tasks: {e}")

    def _save(self):
        try:
            with open(self._file, "w", encoding="utf-8") as f:
                json.dump(self._tasks, f, indent=2, default=str)
        except Exception as e:
            logger.warning(f"Could not save tasks: {e}")

    def create(self, task_id: str, task_text: str) -> dict:
        record = {
            "task_id": task_id,
            "task": task_text,
            "status": "processing",
            "current_agent": "Planner",
            "progress_percent": 0,
            "messages": ["Task started"],
            "created_at": datetime.now().isoformat(),
            "completed_at": None,
            "agent_outputs": [],
            "total_tokens": 0,
            "execution_time": 0.0,
            "errors": [],
        }
        self._tasks[task_id] = record
        self._save()
        return record

    def update(self, task_id: str, **kwargs):
        if task_id in self._tasks:
            self._tasks[task_id].update(kwargs)
            self._save()

    def add_message(self, task_id: str, message: str):
        if task_id in self._tasks:
            self._tasks[task_id]["messages"].append(message)
            self._save()

    def complete(self, task_id: str, result: dict):
        if task_id in self._tasks:
            self._tasks[task_id].update({
                "status": "completed",
                "current_agent": "Done",
                "progress_percent": 100,
                "completed_at": datetime.now().isoformat(),
                **result,
            })
            self._save()

    def fail(self, task_id: str, error: str):
        if task_id in self._tasks:
            self._tasks[task_id].update({
                "status": "failed",
                "errors": self._tasks[task_id].get("errors", []) + [error],
            })
            self._save()

    def get(self, task_id: str) -> Optional[dict]:
        return self._tasks.get(task_id)

    def list_recent(self, limit: int = 20) -> List[dict]:
        tasks = sorted(
            self._tasks.values(),
            key=lambda t: t.get("created_at", ""),
            reverse=True,
        )
        return tasks[:limit]


task_store = TaskStore()
