# backend/agents/planner.py
"""
Planner Agent: Breaks down coding tasks into steps.
REAL implementation - Actually calls OpenAI API.
"""

from openai import OpenAI
from backend.config import settings
import logging

logger = logging.getLogger(__name__)

class PlannerAgent:
    """
    Planner Agent that breaks down tasks into steps.
    
    Real implementation that calls OpenAI API.
    """
    
    def __init__(self):
        """Initialize with OpenAI client."""
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.DEFAULT_MODEL
        self.system_prompt = """You are an expert task planner.
Your job is to break down coding tasks into clear, sequential steps.

For each task:
1. Understand the requirement
2. Identify key components
3. Break into logical steps
4. Consider edge cases
5. List all steps clearly

Be concise. Return ONLY the steps, no extra text."""
    
    def plan(self, task: str, language: str = "python") -> dict:
        """
        Break down a task into steps.
        
        Args:
            task: The coding task
            language: Programming language
            
        Returns:
            dict with plan, tokens_used, status
        """
        try:
            logger.info(f"🤖 Planner: Analyzing task...")
            
            message = f"""Task: {task}
Language: {language}

Break this into clear steps."""
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                max_tokens=500,
                temperature=settings.DEFAULT_TEMPERATURE,
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
            
            # Extract plan from response
            plan_text = response.choices[0].message.content
            tokens_used = response.usage.completion_tokens
            
            logger.info(f"✅ Planner: Got plan ({tokens_used} tokens)")
            
            return {
                "status": "success",
                "plan": plan_text,
                "tokens_used": tokens_used,
                "task": task
            }
            
        except Exception as e:
            logger.error(f"❌ Planner error: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "plan": "",
                "tokens_used": 0,
                "task": task
            }


# Create singleton instance
planner = PlannerAgent()