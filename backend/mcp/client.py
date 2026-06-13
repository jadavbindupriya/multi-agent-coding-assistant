# backend/mcp/client.py
"""MCP client that bridges external services into the tool system."""

import json
import logging
from typing import Any, Callable, Dict, List

from backend.mcp.servers import github_server, slack_server, jira_server

logger = logging.getLogger(__name__)


class MCPClient:
    """Unified MCP-style client for GitHub, Slack, and Jira."""

    def __init__(self):
        self._tools: Dict[str, Callable] = {
            "github_read_repo": self._github_read_repo,
            "github_create_issue": self._github_create_issue,
            "slack_post_message": self._slack_post_message,
            "jira_create_task": self._jira_create_task,
        }

    def list_tools(self) -> List[dict]:
        tools = []
        if github_server.available:
            tools.extend([
                {
                    "type": "function",
                    "function": {
                        "name": "github_read_repo",
                        "description": "Read files from a GitHub repository",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "owner": {"type": "string"},
                                "repo": {"type": "string"},
                                "path": {"type": "string", "description": "File path (empty for listing)"},
                            },
                            "required": ["owner", "repo"],
                        },
                    },
                },
                {
                    "type": "function",
                    "function": {
                        "name": "github_create_issue",
                        "description": "Create a GitHub issue for a bug or feature",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "owner": {"type": "string"},
                                "repo": {"type": "string"},
                                "title": {"type": "string"},
                                "body": {"type": "string"},
                            },
                            "required": ["owner", "repo", "title", "body"],
                        },
                    },
                },
            ])
        if slack_server.available:
            tools.append({
                "type": "function",
                "function": {
                    "name": "slack_post_message",
                    "description": "Post a message to Slack",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "text": {"type": "string"},
                            "channel": {"type": "string"},
                        },
                        "required": ["text"],
                    },
                },
            })
        if jira_server.available:
            tools.append({
                "type": "function",
                "function": {
                    "name": "jira_create_task",
                    "description": "Create a Jira task",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "summary": {"type": "string"},
                            "description": {"type": "string"},
                        },
                        "required": ["summary", "description"],
                    },
                },
            })
        return tools

    def execute(self, name: str, arguments: dict) -> str:
        handler = self._tools.get(name)
        if not handler:
            return json.dumps({"error": f"Unknown MCP tool: {name}"})
        try:
            result = handler(**arguments)
            return json.dumps(result)
        except Exception as e:
            logger.error(f"MCP tool {name} failed: {e}")
            return json.dumps({"error": str(e)})

    def _github_read_repo(self, owner: str, repo: str, path: str = "") -> dict:
        return github_server.read_repo(owner, repo, path)

    def _github_create_issue(self, owner: str, repo: str, title: str, body: str) -> dict:
        return github_server.create_issue(owner, repo, title, body)

    def _slack_post_message(self, text: str, channel: str = None) -> dict:
        return slack_server.post_message(text, channel)

    def _jira_create_task(self, summary: str, description: str) -> dict:
        return jira_server.create_task(summary, description)

    def available_services(self) -> List[str]:
        services = []
        if github_server.available:
            services.append("github")
        if slack_server.available:
            services.append("slack")
        if jira_server.available:
            services.append("jira")
        return services


mcp_client = MCPClient()
