# backend/agents/coder.py
"""
Coder Agent: Writes the actual code solution.

Role: Generate working code
Input: Task description and planning steps
Output: Clean, working code
"""

from openai import OpenAI
from backend.config import settings

class CoderAgent:
    """
    Coder Agent that writes the actual implementation.
    
    Interview Question: "How do you ensure the code is correct?"
    Answer: "The Coder Agent uses specific system prompts to prioritize
    correctness, readability, and efficiency. Later, the Reviewer Agent
    validates it, and the Tester Agent runs tests."
    """
    
    def __init__(self):
        """Initialize the Coder Agent with OpenAI client."""
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.DEFAULT_MODEL
        self.system_prompt = """You are an expert Python programmer.
Write clean, efficient, well-documented code.

Requirements:
1. Code must be correct and tested
2. Use type hints for clarity
3. Include docstrings for functions
4. Follow Python best practices (PEP 8)
5. Handle edge cases
6. Make it readable and maintainable

Only return the code, no explanations."""
    
    async def code(self, task: str, plan: str = "", language: str = "python") -> dict:
        """
        Generate code for a task.
        
        Args:
            task: The coding task description
            plan: The planning steps (optional)
            language: Programming language to use
            
        Returns:
            dict with code and metadata
        """
        try:
            message = f"""Task: {task}
Language: {language}

{f'Plan: {plan}' if plan else ''}

Write the code to solve this task."""
            
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1000,
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
            
            # Extract the code
            code_text = response.content[0].text
            
            return {
                "status": "success",
                "code": code_text,
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
coder = CoderAgent()