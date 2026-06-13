# backend/agents/reviewer.py
"""Reviewer Agent with knowledge base awareness."""

import logging
from typing import Optional

from backend.agents.base import BaseAgent

logger = logging.getLogger(__name__)


class ReviewerAgent(BaseAgent):
    """Reviews code quality against standards and best practices."""

    def __init__(self):
        super().__init__(
            "You are an expert code reviewer. Check for correctness, efficiency, "
            "readability, security issues, and adherence to coding standards. "
            "If coding standards are provided, verify compliance. "
            "Provide constructive feedback with specific improvements."
        )

    def review(self, code: str, task: str = "", knowledge: str = "") -> dict:
        try:
            logger.info("🔍 Reviewer: Reviewing code...")
            rag_context = self.build_rag_context(knowledge)
            message = f"""Task: {task}
{rag_context}

Code to review:
```python
{code}
```

Provide a thorough code review."""
            result = self._chat(message, max_tokens=800, temperature=0.4)
            logger.info(f"✅ Reviewer: Review complete ({result['tokens_used']} tokens)")
            return {
                "status": "success",
                "review": result["content"],
                "tokens_used": result["tokens_used"],
            }
        except Exception as e:
            logger.error(f"❌ Reviewer error: {e}")
            return {"status": "error", "error": str(e), "review": "", "tokens_used": 0}


reviewer = ReviewerAgent()
