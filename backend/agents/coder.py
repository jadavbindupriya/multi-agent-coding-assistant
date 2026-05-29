# backend/agents/coder.py
"""
Coder Agent: Writes the actual code.
REAL implementation - Actually calls OpenAI API.
"""

from openai import OpenAI
from backend.config import settings
import logging

logger = logging.getLogger(__name__)

class CoderAgent:
    """
    Coder Agent that writes the actual implementation.
    
    Real implementation that calls OpenAI API.
    """
    
    def __init__(self):
        """Initialize with OpenAI client."""
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.DEFAULT_MODEL
        self.system_prompt = """You are an expert Python programmer.
Write clean, efficient, well-documented code.

Requirements:
1. Code MUST be correct and working
2. Use type hints
3. Add docstrings
4. Follow PEP 8
5. Handle edge cases
6. Make it readable

Return ONLY the code in a code block. No explanations."""
    
    def code(self, task: str, plan: str = "", language: str = "python") -> dict:
        """
        Generate code for a task.
        
        Args:
            task: The coding task
            plan: The planning steps (optional)
            language: Programming language
            
        Returns:
            dict with code, tokens_used, status
        """
        try:
            logger.info(f"💻 Coder: Writing code...")
            
            message = f"""Task: {task}
Language: {language}

{f'Plan to follow:' + chr(10) + plan if plan else ''}

Write the code to solve this task. Return ONLY the code."""
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                max_tokens=1500,
                temperature=0.3,  # Lower temperature for code = more consistent
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
            
            # Extract code from response
            code_text = response.choices[0].message.content
            tokens_used = response.usage.completion_tokens
            
            logger.info(f"✅ Coder: Generated code ({tokens_used} tokens)")
            
            return {
                "status": "success",
                "code": code_text,
                "tokens_used": tokens_used,
                "task": task
            }
            
        except Exception as e:
            logger.error(f"❌ Coder error: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "code": "",
                "tokens_used": 0,
                "task": task
            }


# Create singleton instance
coder = CoderAgent()