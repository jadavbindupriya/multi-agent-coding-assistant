# backend/api/integrations.py
"""MCP integration API - GitHub, Slack, Jira (Phase 7)."""

from fastapi import APIRouter, HTTPException

from backend.mcp.client import mcp_client
from backend.mcp.servers import github_server, slack_server, jira_server
from backend.models.schemas import (
    GitHubIssueRequest,
    SlackMessageRequest,
    JiraTaskRequest,
    IntegrationStatus,
)

router = APIRouter()


@router.get("/status", response_model=IntegrationStatus)
async def integration_status():
    """Check which integrations are configured."""
    return IntegrationStatus(
        github=github_server.available,
        slack=slack_server.available,
        jira=jira_server.available,
        available_tools=[t["function"]["name"] for t in mcp_client.list_tools()],
    )


@router.get("/github/repo/{owner}/{repo}")
async def read_github_repo(owner: str, repo: str, path: str = ""):
    """Read files from a GitHub repository."""
    result = github_server.read_repo(owner, repo, path)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.post("/github/issue")
async def create_github_issue(request: GitHubIssueRequest):
    """Create a GitHub issue."""
    result = github_server.create_issue(request.owner, request.repo, request.title, request.body)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.post("/slack/message")
async def post_slack_message(request: SlackMessageRequest):
    """Post a message to Slack."""
    result = slack_server.post_message(request.text, request.channel)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.post("/jira/task")
async def create_jira_task(request: JiraTaskRequest):
    """Create a Jira task."""
    result = jira_server.create_task(request.summary, request.description)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result
