# backend/agents/evaluator.py
"""Evaluator agent for solution quality assessment."""

import json
import logging

from backend.agents.base import BaseAgent

logger = logging.getLogger(__name__)


class EvaluatorAgent(BaseAgent):
    """Evaluates solution quality against criteria."""

    def __init__(self):
        super().__init__(
            "You are an expert code evaluator. Assess solutions on correctness, "
            "readability, efficiency, and best practices. Return JSON with keys: "
            "score (0-1), feedback, strengths (list), improvements (list)."
        )

    def evaluate(self, response: str, task: str, criteria: list = None) -> dict:
        criteria = criteria or ["correctness", "readability", "efficiency"]
        try:
            message = f"""Task: {task}
Criteria: {', '.join(criteria)}

Solution to evaluate:
```
{response}
```

Return ONLY valid JSON with score, feedback, strengths, improvements."""
            result = self._chat(message, max_tokens=600, temperature=0.3)
            text = result["content"]

            start = text.find("{")
            end = text.rfind("}") + 1
            if start >= 0 and end > start:
                parsed = json.loads(text[start:end])
                return {
                    "status": "success",
                    "score": float(parsed.get("score", 0.8)),
                    "feedback": parsed.get("feedback", ""),
                    "strengths": parsed.get("strengths", []),
                    "improvements": parsed.get("improvements", []),
                    "tokens_used": result["tokens_used"],
                }
            return {
                "status": "success",
                "score": 0.8,
                "feedback": text,
                "strengths": ["Solution provided"],
                "improvements": [],
                "tokens_used": result["tokens_used"],
            }
        except Exception as e:
            logger.error(f"Evaluator error: {e}")
            return {
                "status": "error",
                "error": str(e),
                "score": 0.0,
                "feedback": "",
                "strengths": [],
                "improvements": [],
                "tokens_used": 0,
            }


evaluator = EvaluatorAgent()
