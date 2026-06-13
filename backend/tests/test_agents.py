# backend/tests/test_agents.py
"""Tests for AI agents."""

import pytest
from backend.agents.planner import planner
from backend.agents.coder import coder
from backend.tools.registry import tool_registry
from backend.tools.npm_lookup import lookup_npm_package
from backend.testing.runner import test_runner


class TestPlannerAgent:
    def test_planner_returns_dict(self):
        result = planner.plan("Write a hello world function")
        assert isinstance(result, dict)

    def test_planner_has_required_fields(self):
        result = planner.plan("Write a hello world function")
        assert "status" in result
        assert "plan" in result

    def test_planner_success_status(self):
        result = planner.plan("Write a hello world function")
        assert result["status"] in ["success", "error"]


class TestCoderAgent:
    def test_coder_returns_dict(self):
        result = coder.code("Write a hello world function")
        assert isinstance(result, dict)

    def test_coder_has_required_fields(self):
        result = coder.code("Write a hello world function")
        assert "status" in result
        assert "code" in result


class TestToolRegistry:
    def test_registry_has_tools(self):
        tools = tool_registry.get_openai_tools()
        names = [t["function"]["name"] for t in tools]
        assert "lookup_npm_package" in names
        assert "execute_python" in names
        assert "search_stackoverflow" in names

    def test_npm_lookup_not_found(self):
        result = lookup_npm_package("this-package-definitely-does-not-exist-xyz123")
        assert result["available"] is False


class TestRunner:
    def test_detect_edge_cases(self):
        code = "def test_empty(): pass\ndef test_raises(): pytest.raises(ValueError)"
        result = test_runner.run_tests("def f(): return 1", f"```python\n{code}\n```")
        assert "edge_cases_found" in result
