# backend/models/schemas.py
"""Pydantic schemas for request/response validation."""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


# ========================
# REQUEST SCHEMAS
# ========================

class SolveTaskRequest(BaseModel):
    task: str = Field(..., min_length=1, max_length=5000)
    language: str = Field(default="python")
    context: Optional[str] = Field(default=None)
    model: Optional[str] = Field(default="gpt-4")
    use_knowledge: bool = Field(default=True, description="Search knowledge base before solving")


class EvaluateResponseRequest(BaseModel):
    response: str
    task: str
    criteria: Optional[List[str]] = Field(default=["correctness", "readability"])


class GitHubIssueRequest(BaseModel):
    owner: str
    repo: str
    title: str
    body: str


class SlackMessageRequest(BaseModel):
    text: str
    channel: Optional[str] = None


class JiraTaskRequest(BaseModel):
    summary: str
    description: str


class KnowledgeSearchRequest(BaseModel):
    query: str
    top_k: Optional[int] = 3


# ========================
# RESPONSE SCHEMAS
# ========================

class AgentOutput(BaseModel):
    agent_name: str
    output: str
    tokens_used: int
    execution_time: float
    success: bool = True
    tool_calls: List[Dict[str, Any]] = Field(default_factory=list)


class TestExecutionResult(BaseModel):
    passed: bool
    total: int
    passed_count: int
    failed_count: int
    output: str
    edge_cases_found: List[str] = Field(default_factory=list)
    has_property_tests: bool = False


class CoverageResult(BaseModel):
    coverage_percent: float
    lines_covered: int
    lines_total: int
    meets_threshold: bool
    report: Optional[str] = None


class SolveTaskResponse(BaseModel):
    task_id: str
    original_task: str
    solution: str
    explanation: str
    tests: str
    agent_outputs: List[AgentOutput]
    total_tokens_used: int
    execution_time: float
    confidence_score: float = Field(ge=0.0, le=1.0)
    knowledge_used: bool = False
    test_execution: Optional[TestExecutionResult] = None
    coverage: Optional[CoverageResult] = None
    estimated_cost_usd: float = 0.0


class TaskStatusResponse(BaseModel):
    task_id: str
    status: str
    current_agent: str
    progress_percent: int
    messages: List[str]


class EvaluationResponse(BaseModel):
    score: float = Field(ge=0.0, le=1.0)
    feedback: str
    strengths: List[str]
    improvements: List[str]


class KnowledgeUploadResponse(BaseModel):
    filename: str
    chunks_indexed: int
    message: str


class KnowledgeDocument(BaseModel):
    source: str
    chunks: int


class KnowledgeSearchResult(BaseModel):
    content: str
    source: str
    distance: float


class AnalyticsSummary(BaseModel):
    total_tasks: int
    total_tokens: int
    total_cost_usd: float
    avg_execution_time: float
    agent_performance: Dict[str, Any]
    error_count: int
    recent_errors: List[Dict[str, Any]]


class IntegrationStatus(BaseModel):
    github: bool
    slack: bool
    jira: bool
    available_tools: List[str]
