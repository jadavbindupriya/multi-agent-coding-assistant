# backend/agents/coder.py
"""Coder Agent with RAG and tool calling support."""

import logging
from typing import Optional

from backend.agents.base import BaseAgent
from backend.config import settings

logger = logging.getLogger(__name__)


class CoderAgent(BaseAgent):
    """Writes code using plans, knowledge base, and external tools."""

    def __init__(self):
        super().__init__(
            "You are an expert programmer. Write clean, efficient, well-documented code. "
            "Use type hints, docstrings, and handle edge cases. "
            "You have tools to look up npm packages, search Stack Overflow, and run Python code. "
            "Use tools when helpful (e.g. check if a package exists on npm). "
            "Return ONLY the final code in a code block."
        )

    def code(
        self,
        task: str,
        plan: str = "",
        language: str = "python",
        knowledge: str = "",
        context: Optional[str] = None,
    ) -> dict:
        try:
            logger.info("💻 Coder: Writing code...")
            rag_context = self.build_rag_context(knowledge, context)
            message = f"""Task: {task}
Language: {language}
{f'Plan to follow:{chr(10)}{plan}' if plan else ''}
{rag_context}

Write the code to solve this task. Use tools if needed. Return ONLY the code."""
            if settings.ENABLE_TOOLS:
                result = self._chat_with_tools(message, max_tokens=1500, temperature=0.3)
            else:
                result = self._chat(message, max_tokens=1500, temperature=0.3)
                result["tool_calls"] = []

            logger.info(f"✅ Coder: Generated code ({result['tokens_used']} tokens)")
            return {
                "status": "success",
                "code": result["content"],
                "tokens_used": result["tokens_used"],
                "tool_calls": result.get("tool_calls", []),
                "task": task,
            }
        except Exception as e:
            logger.error(f"❌ Coder error: {e}")
            return {"status": "error", "error": str(e), "code": "", "tokens_used": 0, "task": task}


coder = CoderAgent()
