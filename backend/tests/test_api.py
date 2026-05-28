# backend/tests/test_api.py
"""
Tests for API endpoints.

Why test?
- Ensure code works as expected
- Catch bugs early
- Document expected behavior
- Build confidence in deployments
"""

import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

class TestHealthEndpoint:
    """Test the health check endpoint."""
    
    def test_health_returns_200(self):
        """Health endpoint should return 200 status."""
        response = client.get("/health")
        assert response.status_code == 200
    
    def test_health_returns_healthy(self):
        """Health endpoint should return 'healthy' status."""
        response = client.get("/health")
        data = response.json()
        assert data["status"] == "healthy"


class TestRootEndpoint:
    """Test the root endpoint."""
    
    def test_root_returns_200(self):
        """Root endpoint should return 200 status."""
        response = client.get("/")
        assert response.status_code == 200
    
    def test_root_returns_api_info(self):
        """Root endpoint should return API information."""
        response = client.get("/")
        data = response.json()
        assert "name" in data
        assert "version" in data
        assert "docs" in data


class TestSolveEndpoint:
    """Test the solve task endpoint."""
    
    def test_solve_with_valid_task(self):
        """Solve endpoint should accept valid task."""
        payload = {
            "task": "Write a function to reverse a string",
            "language": "python"
        }
        response = client.post("/api/solve", json=payload)
        assert response.status_code == 200
    
    def test_solve_returns_required_fields(self):
        """Solve endpoint should return required fields."""
        payload = {
            "task": "Write a function to reverse a string",
            "language": "python"
        }
        response = client.post("/api/solve", json=payload)
        data = response.json()
        
        required_fields = [
            "task_id", "original_task", "solution", 
            "explanation", "tests", "agent_outputs"
        ]
        for field in required_fields:
            assert field in data
    
    def test_solve_with_empty_task(self):
        """Solve endpoint should reject empty task."""
        payload = {
            "task": "",
            "language": "python"
        }
        response = client.post("/api/solve", json=payload)
        assert response.status_code == 422  # Validation error


class TestStatusEndpoint:
    """Test the status endpoint."""
    
    def test_status_returns_task_status(self):
        """Status endpoint should return task status."""
        response = client.get("/api/status/test-task-123")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "task_id" in data


class TestEvaluateEndpoint:
    """Test the evaluate endpoint."""
    
    def test_evaluate_with_valid_data(self):
        """Evaluate endpoint should accept valid data."""
        payload = {
            "response": "def reverse(s): return s[::-1]",
            "task": "Reverse a string",
            "criteria": ["correctness", "efficiency"]
        }
        response = client.post("/api/evaluate", json=payload)
        assert response.status_code == 200
    
    def test_evaluate_returns_score(self):
        """Evaluate endpoint should return quality score."""
        payload = {
            "response": "def reverse(s): return s[::-1]",
            "task": "Reverse a string"
        }
        response = client.post("/api/evaluate", json=payload)
        data = response.json()
        assert "score" in data
        assert 0 <= data["score"] <= 1