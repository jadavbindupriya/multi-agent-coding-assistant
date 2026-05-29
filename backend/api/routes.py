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
    MULTI-AGENT implementation: Planner → Coder → Reviewer → Tester
    
    Complete orchestration of 4 specialized agents.
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
        
        print(f"\n{'='*60}")
        print(f"📋 TASK: {request.task[:50]}...")
        print(f"{'='*60}\n")
        
        # ==================== PLANNER AGENT ====================
        from backend.agents.planner import planner
        planner_result = planner.plan(request.task, request.language)
        
        if planner_result["status"] == "error":
            raise HTTPException(
                status_code=500,
                detail=f"Planner error: {planner_result['error']}"
            )
        
        plan = planner_result["plan"]
        planner_tokens = planner_result["tokens_used"]
        
        print(f"📍 PLAN:\n{plan}\n")
        
        # ==================== CODER AGENT ====================
        from backend.agents.coder import coder
        coder_result = coder.code(request.task, plan, request.language)
        
        if coder_result["status"] == "error":
            raise HTTPException(
                status_code=500,
                detail=f"Coder error: {coder_result['error']}"
            )
        
        solution = coder_result["code"]
        coder_tokens = coder_result["tokens_used"]
        
        print(f"💻 SOLUTION:\n{solution}\n")
        
        # ==================== REVIEWER AGENT ====================
        from backend.agents.reviewer import reviewer
        reviewer_result = reviewer.review(solution, request.task)
        
        if reviewer_result["status"] == "error":
            raise HTTPException(
                status_code=500,
                detail=f"Reviewer error: {reviewer_result['error']}"
            )
        
        review = reviewer_result["review"]
        reviewer_tokens = reviewer_result["tokens_used"]
        
        print(f"🔍 REVIEW:\n{review}\n")
        
        # ==================== TESTER AGENT ====================
        from backend.agents.tester import tester
        tester_result = tester.test(solution, request.task)
        
        if tester_result["status"] == "error":
            raise HTTPException(
                status_code=500,
                detail=f"Tester error: {tester_result['error']}"
            )
        
        tests = tester_result["tests"]
        tester_tokens = tester_result["tokens_used"]
        
        print(f"🧪 TESTS:\n{tests}\n")
        
        # ==================== CREATE RESPONSE ====================
        
        # Create agent outputs with all 4 agents
        agent_outputs = [
            AgentOutput(
                agent_name="Planner",
                output=plan,
                tokens_used=planner_tokens,
                execution_time=0.5,
                success=True
            ),
            AgentOutput(
                agent_name="Coder",
                output=solution,
                tokens_used=coder_tokens,
                execution_time=1.0,
                success=True
            ),
            AgentOutput(
                agent_name="Reviewer",
                output=review,
                tokens_used=reviewer_tokens,
                execution_time=0.8,
                success=True
            ),
            AgentOutput(
                agent_name="Tester",
                output=tests,
                tokens_used=tester_tokens,
                execution_time=0.7,
                success=True
            ),
        ]
        
        total_tokens = planner_tokens + coder_tokens + reviewer_tokens + tester_tokens
        
        response = SolveTaskResponse(
            task_id=task_id,
            original_task=request.task,
            solution=solution,
            explanation=f"Solved using 4 specialized agents. Planner analyzed, Coder implemented, Reviewer validated, Tester created tests.",
            tests=tests,
            agent_outputs=agent_outputs,
            total_tokens_used=total_tokens,
            execution_time=3.0,
            confidence_score=0.90
        )
        
        print(f"✅ COMPLETE: Task {task_id}")
        print(f"   Total tokens: {total_tokens}")
        print(f"   Agents: Planner → Coder → Reviewer → Tester\n")
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ ERROR: {str(e)}\n")
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