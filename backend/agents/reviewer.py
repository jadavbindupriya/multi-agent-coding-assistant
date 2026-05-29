# backend/agents/reviewer.py
"""
Reviewer Agent: Reviews code for quality, bugs, and improvements.
REAL implementation - Calls OpenAI API to analyze code.
"""

from openai import OpenAI
from backend.config import settings
import logging

logger = logging.getLogger(__name__)

class ReviewerAgent:
    """
    Reviewer Agent that analyzes code quality.
    
    Checks for:
    - Bugs and edge cases
    - Performance issues
    - Code style and readability
    - Security vulnerabilities
    - Best practices
    """
    
    def __init__(self):
        """Initialize with OpenAI client."""
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.DEFAULT_MODEL
        self.system_prompt = """You are an expert code reviewer.
Analyze code for:
1. Bugs and edge cases
2. Performance issues
3. Security vulnerabilities
4. Code style and readability
5. Best practices

Provide:
- Overall quality score (0-100)
- List of issues found
- Specific improvement suggestions
- Strengths of the code

Be concise but thorough."""
    
    def review(self, code: str, task: str = "") -> dict:
        """
        Review code for quality.
        
        Args:
            code: The code to review
            task: The original task (for context)
            
        Returns:
            dict with review, issues, suggestions, score
        """
        try:
            logger.info(f"🔍 Reviewer: Analyzing code quality...")
            
            message = f"""Task: {task}

Code to review:
```python
{code}
```

Provide a detailed code review."""
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                max_tokens=800,
                temperature=0.4,  # Lower temperature = more analytical
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
            
            review_text = response.choices[0].message.content
            tokens_used = response.usage.completion_tokens
            
            logger.info(f"✅ Reviewer: Completed review ({tokens_used} tokens)")
            
            return {
                "status": "success",
                "review": review_text,
                "tokens_used": tokens_used,
                "code": code[:100] + "..." if len(code) > 100 else code
            }
            
        except Exception as e:
            logger.error(f"❌ Reviewer error: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "review": "",
                "tokens_used": 0,
                "code": code[:100] + "..." if len(code) > 100 else code
            }


# Create singleton instance
reviewer = ReviewerAgent()