# backend/agents/tester.py
"""
Tester Agent: Generates test cases for code.
REAL implementation - Calls OpenAI API to create tests.
"""

from openai import OpenAI
from backend.config import settings
import logging

logger = logging.getLogger(__name__)

class TesterAgent:
    """
    Tester Agent that generates test cases.
    
    Creates:
    - Unit tests for each function
    - Edge case tests
    - Error handling tests
    - Integration tests (if applicable)
    """
    
    def __init__(self):
        """Initialize with OpenAI client."""
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.DEFAULT_MODEL
        self.system_prompt = """You are an expert test engineer.
Generate comprehensive test cases for the given code.

Test requirements:
1. Unit tests for each function
2. Edge cases (empty inputs, null, very large inputs)
3. Error handling tests
4. Normal operation tests
5. Use pytest format

Return ONLY the test code in a code block. No explanations."""
    
    def test(self, code: str, task: str = "") -> dict:
        """
        Generate test cases for code.
        
        Args:
            code: The code to test
            task: The original task (for context)
            
        Returns:
            dict with tests and tokens_used
        """
        try:
            logger.info(f"🧪 Tester: Generating test cases...")
            
            message = f"""Task: {task}

Code to test:
```python
{code}
```

Write comprehensive pytest test cases."""
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                max_tokens=1000,
                temperature=0.3,  # Lower temperature = more structured
                messages=[
                    {
                        "role": "system",
                        "content": self.system_prompt
                    },
                    {
                        "role": "user",
                        "content": message
                    }
                ]
            )
            
            tests_text = response.choices[0].message.content
            tokens_used = response.usage.completion_tokens
            
            logger.info(f"✅ Tester: Generated tests ({tokens_used} tokens)")
            
            return {
                "status": "success",
                "tests": tests_text,
                "tokens_used": tokens_used,
                "code": code[:100] + "..." if len(code) > 100 else code
            }
            
        except Exception as e:
            logger.error(f"❌ Tester error: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "tests": "",
                "tokens_used": 0,
                "code": code[:100] + "..." if len(code) > 100 else code
            }


# Create singleton instance
tester = TesterAgent()