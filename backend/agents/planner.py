# backend/agents/planner.py
"""Planner Agent with RAG knowledge injection."""

import logging
from typing import Optional

from backend.agents.base import BaseAgent

logger = logging.getLogger(__name__)


class PlannerAgent(BaseAgent):
    """Breaks down coding tasks into steps, using knowledge base when available."""

    def __init__(self):
        super().__init__(
            "You are an expert task planner. Break down coding tasks into clear, "
            "sequential steps. If coding standards or documentation are provided, "
            "follow them. Consider edge cases. Return ONLY the steps."
        )

    def plan(
        self,
        task: str,
        language: str = "python",
        knowledge: str = "",
        context: Optional[str] = None,
    ) -> dict:
        try:
            logger.info("🤖 Planner: Analyzing task...")
            rag_context = self.build_rag_context(knowledge, context)
            message = f"""Task: {task}
Language: {language}
{rag_context}

Break this into clear steps."""
            result = self._chat(message, max_tokens=500, temperature=0.7)
            logger.info(f"✅ Planner: Got plan ({result['tokens_used']} tokens)")
            return {
                "status": "success",
                "plan": result["content"],
                "tokens_used": result["tokens_used"],
                "task": task,
            }
        except Exception as e:
            logger.error(f"❌ Planner error: {e}")
            return {"status": "error", "error": str(e), "plan": "", "tokens_used": 0, "task": task}


planner = PlannerAgent()
