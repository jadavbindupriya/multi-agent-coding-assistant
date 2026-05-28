# backend/api/routes.py
"""
API routes/endpoints for the backend.

Each endpoint handles a specific request from the client.
"""

from fastapi import APIRouter, HTTPException
import uuid
from datetime import datetime

from backend.models.schemas import (
    SolveTaskRequest,
    SolveTaskResponse,
    AgentOutput,
    TaskStatusResponse,
    EvaluateResponseRequest,
    EvaluationResponse
)

# Create a router (like a controller)
router = APIRouter()

# ========================
# SOLVE TASK ENDPOINT
# ========================

@router.post("/solve")
async def solve_task(request: SolveTaskRequest):
    """
    Main endpoint: Solve a coding task using multi-agent system.
    
    This is where the magic happens (Phase 4 onwards).
    For now, returns a mock response.
    
    Args:
        request: SolveTaskRequest containing the task details
    
    Returns:
        SolveTaskResponse with solution, explanation, tests, etc
    
    Example Request:
    POST /api/solve
    {
        "task": "Write a function to reverse a string",
        "language": "python",
        "context": "Use async/await if possible"
    }
    
    Example Response:
    {
        "task_id": "abc123",
        "solution": "def reverse(s): return s[::-1]",
        ...
    }
    """
    
    try:
        # Generate unique task ID
        task_id = str(uuid.uuid4())
        
        # Validate input
        if len(request.task) > 5000:
            raise HTTPException(
                status_code=400,
                detail="Task too long. Max 5000 characters"
            )
        
        # PHASE 4: Here we'll call the multi-agent system
        # For now, return mock response
        
        solution = "def reverse_string(s: str) -> str:\n    return s[::-1]"
        explanation = "This function uses Python's slice notation [::-1] to reverse the string efficiently."
        tests = 'assert reverse_string("hello") == "olleh"\nassert reverse_string("") == ""'
        
        # Create mock agent outputs
        agent_outputs = [
            AgentOutput(
                agent_name="Planner",
                output="1. Understand requirement\n2. Write efficient solution\n3. Test edge cases",
                tokens_used=50,
                execution_time=0.5,
                success=True
            ),
            AgentOutput(
                agent_name="Coder",
                output=solution,
                tokens_used=100,
                execution_time=1.0,
                success=True
            ),
            AgentOutput(
                agent_name="Reviewer",
                output="Code is efficient (O(n) time, O(n) space). Good implementation.",
                tokens_used=60,
                execution_time=0.8,
                success=True
            ),
            AgentOutput(
                agent_name="Tester",
                output=tests,
                tokens_used=80,
                execution_time=0.6,
                success=True
            ),
        ]
        
        response = SolveTaskResponse(
            task_id=task_id,
            original_task=request.task,
            solution=solution,
            explanation=explanation,
            tests=tests,
            agent_outputs=agent_outputs,
            total_tokens_used=290,
            execution_time=3.0,
            confidence_score=0.95
        )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


# ========================
# STATUS ENDPOINT
# ========================

@router.get("/status/{task_id}")
async def get_task_status(task_id: str):
    """
    Get status of a task being processed.
    
    Example:
    GET /api/status/abc123
    
    Response:
    {
        "task_id": "abc123",
        "status": "processing",
        "current_agent": "Coder",
        "progress_percent": 50,
        "messages": ["Planner completed", "Coder running..."]
    }
    """
    
    # Mock response (Phase 4: real implementation)
    return TaskStatusResponse(
        task_id=task_id,
        status="completed",
        current_agent="Final Answer",
        progress_percent=100,
        messages=[
            "Planner analyzed the task",
            "Coder wrote the solution",
            "Reviewer checked the code",
            "Tester validated with tests"
        ]
    )


# ========================
# EVALUATE ENDPOINT
# ========================

@router.post("/evaluate")
async def evaluate_response(request: EvaluateResponseRequest):
    """
    Evaluate quality of a generated response.
    
    Returns quality score and feedback.
    
    Example Request:
    POST /api/evaluate
    {
        "response": "def reverse(s): return s[::-1]",
        "task": "Reverse a string",
        "criteria": ["correctness", "efficiency"]
    }
    
    Example Response:
    {
        "score": 0.95,
        "feedback": "Excellent solution using Python idioms",
        "strengths": ["Uses Python slice notation", "O(n) complexity"],
        "improvements": ["Could add docstring"]
    }
    """
    
    # Mock response (Phase 9: real implementation with evaluation agents)
    return EvaluationResponse(
        score=0.95,
        feedback="Excellent solution using Python idioms",
        strengths=[
            "Uses Python's idiomatic slice notation",
            "O(n) time complexity (optimal)",
            "Concise and readable"
        ],
        improvements=[
            "Could add type hints for clarity",
            "Consider adding docstring"
        ]
    )