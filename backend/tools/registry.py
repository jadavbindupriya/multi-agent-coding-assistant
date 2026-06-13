# backend/tools/registry.py
"""Central tool registry for agent tool calling."""

import json
import logging
from typing import Any, Callable, Dict, List

from backend.tools.npm_lookup import lookup_npm_package
from backend.tools.code_sandbox import execute_python
from backend.tools.stackoverflow import search_stackoverflow
from backend.tools.mcp_adapter import get_mcp_openai_tools, execute_mcp_tool

logger = logging.getLogger(__name__)


class ToolRegistry:
    """Registry of tools available to agents."""

    def __init__(self):
        self._handlers: Dict[str, Callable] = {
            "lookup_npm_package": lookup_npm_package,
            "execute_python": execute_python,
            "search_stackoverflow": search_stackoverflow,
        }
        self._mcp_tools = {
            "github_read_repo", "github_create_issue",
            "slack_post_message", "jira_create_task",
        }

    def get_openai_tools(self) -> List[dict]:
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "lookup_npm_package",
                    "description": "Check if an npm package exists and get its info",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "package_name": {"type": "string", "description": "npm package name"},
                        },
                        "required": ["package_name"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "execute_python",
                    "description": "Execute Python code in a sandbox and return output",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "code": {"type": "string", "description": "Python code to run"},
                        },
                        "required": ["code"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "search_stackoverflow",
                    "description": "Search Stack Overflow for coding solutions",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string", "description": "Search query"},
                        },
                        "required": ["query"],
                    },
                },
            },
        ]
        tools.extend(get_mcp_openai_tools())
        return tools

    def execute(self, name: str, arguments: dict) -> str:
        if name in self._mcp_tools:
            return execute_mcp_tool(name, arguments)

        handler = self._handlers.get(name)
        if not handler:
            return json.dumps({"error": f"Unknown tool: {name}"})
        try:
            result = handler(**arguments)
            return json.dumps(result)
        except Exception as e:
            logger.error(f"Tool {name} failed: {e}")
            return json.dumps({"error": str(e)})


tool_registry = ToolRegistry()
