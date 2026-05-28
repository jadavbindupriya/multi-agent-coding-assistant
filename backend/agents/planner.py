# backend/agents/planner.py
"""
Planner Agent: Breaks down coding tasks into steps.

Role: Analyze a task and create a plan
Input: Coding task description
Output: Step-by-step plan to solve it
"""

from openai import OpenAI
from backend.config import settings

class PlannerAgent:
    """
    Planner Agent that breaks down tasks into steps.
    
    Interview Question: "What does the Planner Agent do?"
    Answer: "It takes a coding task and breaks it down into smaller,
    manageable steps. This helps other agents understand the approach
    before implementation."
    """
    
    def __init__(self):
        """Initialize the Planner Agent with OpenAI client."""
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.DEFAULT_MODEL
        self.system_prompt = """You are an expert task planner.
Your job is to break down complex coding tasks into clear, sequential steps.

For each task:
1. Understand what the user is asking
2. Identify the main components needed
3. Break it into logical steps
4. Consider edge cases
5. List all steps clearly

Be concise but thorough."""
    
    async def plan(self, task: str, language: str = "python") -> dict:
        """
        Break down a task into steps.
        
        Args:
            task: The coding task description
            language: Programming language to use
            
        Returns:
            dict with steps and metadata
        """
        try:
            message = f"""Task: {task}
Language: {language}

Please break this task down into clear, actionable steps."""
            
            response = self.client.messages.create(
                model=self.model,
                max_tokens=500,
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
            
            # Extract the plan
            plan_text = response.content[0].text
            
            return {
                "status": "success",
                "plan": plan_text,
                "tokens_used": response.usage.completion_tokens,
                "task": task
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "task": task
            }


# Create a singleton instance
planner = PlannerAgent()