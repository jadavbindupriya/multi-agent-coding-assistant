# backend/agents/tester.py
"""Tester Agent with property-based testing and edge case detection."""

import logging

from backend.agents.base import BaseAgent

logger = logging.getLogger(__name__)


class TesterAgent(BaseAgent):
    """Generates comprehensive tests including property-based and edge cases."""

    def __init__(self):
        super().__init__(
            "You are an expert test engineer. Generate comprehensive pytest test cases.\n"
            "Requirements:\n"
            "1. Unit tests for each function\n"
            "2. Edge cases: empty inputs, None, negative values, large inputs, unicode\n"
            "3. Error handling tests with pytest.raises\n"
            "4. Property-based tests using hypothesis where appropriate (@given decorator)\n"
            "5. Integration tests if applicable\n"
            "Return ONLY the test code in a code block."
        )

    def test(self, code: str, task: str = "") -> dict:
        try:
            logger.info("🧪 Tester: Generating test cases...")
            message = f"""Task: {task}

Code to test:
```python
{code}
```

Write comprehensive pytest tests with edge cases and property-based tests where useful."""
            result = self._chat(message, max_tokens=1200, temperature=0.3)
            logger.info(f"✅ Tester: Generated tests ({result['tokens_used']} tokens)")
            return {
                "status": "success",
                "tests": result["content"],
                "tokens_used": result["tokens_used"],
            }
        except Exception as e:
            logger.error(f"❌ Tester error: {e}")
            return {"status": "error", "error": str(e), "tests": "", "tokens_used": 0}


tester = TesterAgent()
