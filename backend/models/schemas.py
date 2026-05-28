# backend/models/schemas.py
"""
Pydantic schemas for request/response validation.

Pydantic = Data validation library
Why use it?
- Automatic validation (wrong types rejected)
- Auto-generates API documentation
- Type checking at runtime
"""

from pydantic import BaseModel, Field
from typing import Optional, List

# ========================
# REQUEST SCHEMAS (Client → Server)
# ========================

class SolveTaskRequest(BaseModel):
    """Schema for when a user submits a coding task."""
    
    task: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="The coding task to solve"
    )
    
    language: str = Field(
        default="python",
        description="Programming language (python, javascript, go, etc)"
    )
    
    context: Optional[str] = Field(
        default=None,
        description="Optional project context (coding standards, frameworks used, etc)"
    )
    
    model: Optional[str] = Field(
        default="gpt-4",
        description="Which LLM model to use"
    )


class EvaluateResponseRequest(BaseModel):
    """Schema for evaluating agent response quality."""
    
    response: str = Field(
        ...,
        description="The agent's response to evaluate"
    )
    
    task: str = Field(
        ...,
        description="Original task"
    )
    
    criteria: Optional[List[str]] = Field(
        default=["correctness", "readability"],
        description="What to evaluate"
    )


# ========================
# RESPONSE SCHEMAS (Server → Client)
# ========================

class AgentOutput(BaseModel):
    """Output from a single agent."""
    
    agent_name: str = Field(description="Name of the agent (Planner, Coder, etc)")
    output: str = Field(description="The agent's actual output")
    tokens_used: int = Field(description="Tokens used for this agent")
    execution_time: float = Field(description="How long it took in seconds")
    success: bool = Field(default=True, description="Did the agent complete successfully?")


class SolveTaskResponse(BaseModel):
    """Final response to a solve task request."""
    
    task_id: str = Field(description="Unique ID for this task (for tracking)")
    original_task: str = Field(description="The task that was requested")
    solution: str = Field(description="The final solution/code")
    explanation: str = Field(description="Explanation of the solution")
    tests: str = Field(description="Test code for the solution")
    agent_outputs: List[AgentOutput] = Field(description="Intermediate outputs from each agent")
    total_tokens_used: int = Field(description="Total tokens used across all agents")
    execution_time: float = Field(description="Total time in seconds")
    confidence_score: float = Field(
        ge=0.0,
        le=1.0,
        description="How confident are we in this solution (0-1)"
    )


class TaskStatusResponse(BaseModel):
    """Status of a task currently being processed."""
    
    task_id: str = Field(description="Task ID")
    status: str = Field(description="pending, processing, completed, failed")
    current_agent: str = Field(description="Which agent is currently working")
    progress_percent: int = Field(description="0-100% progress")
    messages: List[str] = Field(description="Status messages/logs")


class EvaluationResponse(BaseModel):
    """Response from evaluating a solution."""
    
    score: float = Field(
        ge=0.0,
        le=1.0,
        description="Quality score 0-1"
    )
    
    feedback: str = Field(description="Detailed feedback")
    strengths: List[str] = Field(description="What's good about the solution")
    improvements: List[str] = Field(description="What could be better")