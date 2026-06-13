# backend/mcp/servers.py
"""MCP-style service integrations: GitHub, Slack, Jira."""

import base64
import logging
from typing import Optional

import requests

from backend.config import settings

logger = logging.getLogger(__name__)


class GitHubServer:
    """GitHub integration for repo access and issue creation."""

    def __init__(self):
        self.token = settings.GITHUB_TOKEN
        self.base_url = "https://api.github.com"

    @property
    def available(self) -> bool:
        return bool(self.token)

    def _headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json",
        }

    def read_repo(self, owner: str, repo: str, path: str = "") -> dict:
        if not self.available:
            return {"error": "GitHub token not configured"}
        try:
            url = f"{self.base_url}/repos/{owner}/{repo}/contents/{path}"
            resp = requests.get(url, headers=self._headers(), timeout=15)
            resp.raise_for_status()
            data = resp.json()
            if isinstance(data, list):
                return {"files": [f["name"] for f in data[:20]]}
            content = base64.b64decode(data["content"]).decode("utf-8", errors="replace")
            return {"path": data["path"], "content": content[:5000]}
        except Exception as e:
            return {"error": str(e)}

    def create_issue(self, owner: str, repo: str, title: str, body: str) -> dict:
        if not self.available:
            return {"error": "GitHub token not configured"}
        try:
            url = f"{self.base_url}/repos/{owner}/{repo}/issues"
            resp = requests.post(
                url,
                headers=self._headers(),
                json={"title": title, "body": body},
                timeout=15,
            )
            resp.raise_for_status()
            data = resp.json()
            return {"issue_number": data["number"], "url": data["html_url"], "title": data["title"]}
        except Exception as e:
            return {"error": str(e)}


class SlackServer:
    """Slack integration for posting results."""

    def __init__(self):
        self.webhook_url = settings.SLACK_WEBHOOK_URL

    @property
    def available(self) -> bool:
        return bool(self.webhook_url)

    def post_message(self, text: str, channel: Optional[str] = None) -> dict:
        if not self.available:
            return {"error": "Slack webhook not configured"}
        try:
            payload = {"text": text}
            if channel:
                payload["channel"] = channel
            resp = requests.post(self.webhook_url, json=payload, timeout=10)
            return {"success": resp.status_code == 200, "status_code": resp.status_code}
        except Exception as e:
            return {"error": str(e)}


class JiraServer:
    """Jira integration for task creation."""

    def __init__(self):
        self.url = settings.JIRA_URL.rstrip("/")
        self.email = settings.JIRA_EMAIL
        self.token = settings.JIRA_API_TOKEN
        self.project_key = settings.JIRA_PROJECT_KEY

    @property
    def available(self) -> bool:
        return bool(self.url and self.email and self.token)

    def _auth(self) -> tuple:
        return (self.email, self.token)

    def create_task(self, summary: str, description: str, issue_type: str = "Task") -> dict:
        if not self.available:
            return {"error": "Jira credentials not configured"}
        try:
            url = f"{self.url}/rest/api/3/issue"
            payload = {
                "fields": {
                    "project": {"key": self.project_key},
                    "summary": summary,
                    "description": {
                        "type": "doc",
                        "version": 1,
                        "content": [
                            {
                                "type": "paragraph",
                                "content": [{"type": "text", "text": description}],
                            }
                        ],
                    },
                    "issuetype": {"name": issue_type},
                }
            }
            resp = requests.post(url, json=payload, auth=self._auth(), timeout=15)
            resp.raise_for_status()
            data = resp.json()
            return {"issue_key": data["key"], "id": data["id"]}
        except Exception as e:
            return {"error": str(e)}


github_server = GitHubServer()
slack_server = SlackServer()
jira_server = JiraServer()
