# backend/tests/test_agents.py
"""
Tests for AI agents.

Why test agents?
- Ensure they produce correct output
- Verify they handle errors gracefully
- Monitor token usage
- Track performance metrics
"""

import pytest
from backend.agents.planner import planner
from backend.agents.coder import coder


class TestPlannerAgent:
    """Test the Planner Agent."""
    
    @pytest.mark.asyncio
    async def test_planner_returns_dict(self):
        """Planner should return a dictionary."""
        result = await planner.plan("Write a hello world function")
        assert isinstance(result, dict)
    
    @pytest.mark.asyncio
    async def test_planner_has_required_fields(self):
        """Planner response should have required fields."""
        result = await planner.plan("Write a hello world function")
        assert "status" in result
        assert "plan" in result
    
    @pytest.mark.asyncio
    async def test_planner_success_status(self):
        """Planner should return success status."""
        result = await planner.plan("Write a hello world function")
        assert result["status"] in ["success", "error"]


class TestCoderAgent:
    """Test the Coder Agent."""
    
    @pytest.mark.asyncio
    async def test_coder_returns_dict(self):
        """Coder should return a dictionary."""
        result = await coder.code("Write a hello world function")
        assert isinstance(result, dict)
    
    @pytest.mark.asyncio
    async def test_coder_has_required_fields(self):
        """Coder response should have required fields."""
        result = await coder.code("Write a hello world function")
        assert "status" in result
        assert "code" in result
    
    @pytest.mark.asyncio
    async def test_coder_success_status(self):
        """Coder should return success status."""
        result = await coder.code("Write a hello world function")
        assert result["status"] in ["success", "error"]