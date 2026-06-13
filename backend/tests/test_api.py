# backend/tests/test_api.py
"""Tests for API endpoints."""

import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


class TestHealthEndpoint:
    def test_health_returns_200(self):
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_returns_healthy(self):
        data = client.get("/health").json()
        assert data["status"] == "healthy"
        assert "features" in data


class TestRootEndpoint:
    def test_root_returns_api_info(self):
        data = client.get("/").json()
        assert "name" in data
        assert "features" in data


class TestKnowledgeEndpoint:
    def test_knowledge_status(self):
        response = client.get("/api/knowledge/status")
        assert response.status_code == 200
        data = response.json()
        assert "total_chunks" in data

    def test_list_documents(self):
        response = client.get("/api/knowledge/documents")
        assert response.status_code == 200


class TestIntegrationsEndpoint:
    def test_integration_status(self):
        response = client.get("/api/integrations/status")
        assert response.status_code == 200
        data = response.json()
        assert "github" in data
        assert "slack" in data
        assert "jira" in data


class TestAnalyticsEndpoint:
    def test_analytics_summary(self):
        response = client.get("/api/analytics/summary")
        assert response.status_code == 200
        data = response.json()
        assert "total_tasks" in data


class TestSolveEndpoint:
    def test_solve_with_empty_task(self):
        response = client.post("/api/solve", json={"task": "", "language": "python"})
        assert response.status_code == 422


class TestStatusEndpoint:
    def test_status_not_found(self):
        response = client.get("/api/status/nonexistent-task-id")
        assert response.status_code == 404
