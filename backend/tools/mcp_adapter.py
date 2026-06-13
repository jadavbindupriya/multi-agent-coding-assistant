# backend/tools/mcp_adapter.py
"""Adapter to expose MCP tools through the tool registry."""

from backend.mcp.client import mcp_client


def get_mcp_openai_tools():
    return mcp_client.list_tools()


def execute_mcp_tool(name: str, arguments: dict) -> str:
    return mcp_client.execute(name, arguments)
