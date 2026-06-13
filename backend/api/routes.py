# backend/api/routes.py
"""Core API routes for task solving, status, and evaluation."""

from fastapi import APIRouter, HTTPException

from backend.models.schemas import (
    SolveTaskRequest,
    SolveTaskResponse,
    AgentOutput,
    TaskStatusResponse,
    EvaluateResponseRequest,
    EvaluationResponse,
    TestExecutionResult,
    CoverageResult,
)
from backend.orchestrator.pipeline import pipeline
from backend.storage.tasks import task_store
from backend.agents.evaluator import evaluator

router = APIRouter()


@router.post("/solve", response_model=SolveTaskResponse)
async def solve_task(request: SolveTaskRequest):
    """Multi-agent pipeline with RAG, tools, testing, and analytics."""
    try:
        if len(request.task) > 5000:
            raise HTTPException(status_code=400, detail="Task too long. Max 5000 characters")

        result = pipeline.run(
            task=request.task,
            language=request.language,
            context=request.context,
            use_knowledge=request.use_knowledge,
        )

        if result["status"] == "error":
            raise HTTPException(status_code=500, detail=result["error"])

        agent_outputs = [
            AgentOutput(
                agent_name=a["agent_name"],
                output=a["output"],
                tokens_used=a["tokens_used"],
                execution_time=a["execution_time"],
                success=a["success"],
                tool_calls=a.get("tool_calls", []),
            )
            for a in result["agent_outputs"]
        ]

        test_exec = None
        if result.get("test_execution"):
            test_exec = TestExecutionResult(**result["test_execution"])

        coverage = None
        if result.get("coverage"):
            coverage = CoverageResult(**result["coverage"])

        return SolveTaskResponse(
            task_id=result["task_id"],
            original_task=result["original_task"],
            solution=result["solution"],
            explanation=result["explanation"],
            tests=result["tests"],
            agent_outputs=agent_outputs,
            total_tokens_used=result["total_tokens_used"],
            execution_time=result["execution_time"],
            confidence_score=result["confidence_score"],
            knowledge_used=result.get("knowledge_used", False),
            test_execution=test_exec,
            coverage=coverage,
            estimated_cost_usd=result.get("estimated_cost_usd", 0.0),
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/status/{task_id}", response_model=TaskStatusResponse)
async def get_task_status(task_id: str):
    """Get real-time status of a task from the task store."""
    task = task_store.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskStatusResponse(
        task_id=task["task_id"],
        status=task["status"],
        current_agent=task["current_agent"],
        progress_percent=task["progress_percent"],
        messages=task["messages"],
    )


@router.post("/evaluate", response_model=EvaluationResponse)
async def evaluate_response(request: EvaluateResponseRequest):
    """Evaluate solution quality using the evaluator agent."""
    result = evaluator.evaluate(request.response, request.task, request.criteria)
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["error"])
    return EvaluationResponse(
        score=result["score"],
        feedback=result["feedback"],
        strengths=result["strengths"],
        improvements=result["improvements"],
    )
