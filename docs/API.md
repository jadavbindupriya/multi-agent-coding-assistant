# API Reference

Base URL: `http://localhost:8000`

Interactive docs: http://localhost:8000/docs

---

## System endpoints

### `GET /`

Returns API metadata.

**Response 200:**

```json
{
  "name": "Multi-Agent Coding Assistant",
  "version": "0.2.0",
  "description": "AI system with RAG, tool calling, MCP integrations, enhanced testing, and analytics",
  "docs": "/docs",
  "features": ["RAG", "Tool Calling", "MCP", "Enhanced Testing", "Analytics"]
}
```

### `GET /health`

Health check with feature flags.

**Response 200:**

```json
{
  "status": "healthy",
  "timestamp": "2026-06-13T10:00:00",
  "environment": "development",
  "features": {
    "rag": true,
    "tools": true,
    "test_execution": true,
    "mcp_services": ["github", "slack"]
  }
}
```

---

## Tasks (`/api`)

### `POST /api/solve`

Submit a coding task to the multi-agent pipeline.

**Request body:**

```json
{
  "task": "Write a Python function to check if a number is prime",
  "language": "python",
  "context": "Use type hints and docstrings",
  "model": "gpt-4",
  "use_knowledge": true
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `task` | string | Yes | Coding task (1–5000 chars) |
| `language` | string | No | Target language (default: `python`) |
| `context` | string | No | Extra project context |
| `model` | string | No | OpenAI model override |
| `use_knowledge` | boolean | No | Search RAG knowledge base (default: `true`) |

**Response 200:**

```json
{
  "task_id": "a1b2c3d4-...",
  "original_task": "Write a Python function...",
  "solution": "def is_prime(n: int) -> bool:\n    ...",
  "explanation": "Solved using 4 specialized agents...",
  "tests": "import pytest\n\ndef test_is_prime():...",
  "agent_outputs": [
    {
      "agent_name": "Planner",
      "output": "1. Define function signature...",
      "tokens_used": 245,
      "execution_time": 1.2,
      "success": true,
      "tool_calls": []
    }
  ],
  "total_tokens_used": 1850,
  "execution_time": 12.5,
  "confidence_score": 0.9,
  "knowledge_used": true,
  "test_execution": {
    "passed": true,
    "total": 5,
    "passed_count": 5,
    "failed_count": 0,
    "output": "...",
    "edge_cases_found": ["n=0", "n=1", "large_prime"],
    "has_property_tests": true
  },
  "coverage": {
    "coverage_percent": 0.85,
    "lines_covered": 17,
    "lines_total": 20,
    "meets_threshold": true,
    "report": "..."
  },
  "estimated_cost_usd": 0.0555
}
```

**Errors:**

| Status | Cause |
|--------|-------|
| 400 | Task exceeds 5000 characters |
| 500 | Agent pipeline failure |

---

### `GET /api/status/{task_id}`

Get real-time progress of a running or completed task.

**Response 200:**

```json
{
  "task_id": "a1b2c3d4-...",
  "status": "running",
  "current_agent": "Coder",
  "progress_percent": 35,
  "messages": [
    "Retrieved knowledge from documentation",
    "Planner completed"
  ]
}
```

**Errors:**

| Status | Cause |
|--------|-------|
| 404 | Task ID not found |

---

### `POST /api/evaluate`

Evaluate an existing solution using the Evaluator agent.

**Request body:**

```json
{
  "response": "def add(a, b): return a + b",
  "task": "Write an addition function",
  "criteria": ["correctness", "readability", "edge_cases"]
}
```

**Response 200:**

```json
{
  "score": 0.82,
  "feedback": "The solution is correct but lacks type hints...",
  "strengths": ["Simple and readable", "Correct logic"],
  "improvements": ["Add type hints", "Handle non-numeric input"]
}
```

---

## Knowledge (`/api/knowledge`)

### `POST /api/knowledge/upload`

Upload a document to the RAG knowledge base.

**Request:** `multipart/form-data` with `file` field.

Supported types: `.txt`, `.md`, `.pdf`

**Response 200:**

```json
{
  "filename": "coding_standards.md",
  "chunks_indexed": 12,
  "message": "Indexed 12 chunks from coding_standards.md"
}
```

**Errors:**

| Status | Cause |
|--------|-------|
| 400 | Unsupported file type or PDF parse failure |

---

### `POST /api/knowledge/search`

Semantic search over indexed documents.

**Request body:**

```json
{
  "query": "naming conventions for Python functions",
  "top_k": 3
}
```

**Response 200:**

```json
[
  {
    "content": "Functions should use snake_case naming...",
    "source": "coding_standards.md",
    "distance": 0.23
  }
]
```

---

### `GET /api/knowledge/documents`

List all indexed documents.

**Response 200:**

```json
[
  {
    "source": "coding_standards.md",
    "chunks": 12
  }
]
```

---

### `DELETE /api/knowledge/documents/{source}`

Remove a document and all its chunks from the knowledge base.

**Response 200:**

```json
{
  "message": "Deleted 12 chunks from coding_standards.md"
}
```

---

### `GET /api/knowledge/status`

Knowledge base summary.

**Response 200:**

```json
{
  "document_count": 2,
  "total_chunks": 24,
  "has_knowledge": true
}
```

---

## Integrations (`/api/integrations`)

Requires corresponding tokens in `.env`. Check availability first.

### `GET /api/integrations/status`

**Response 200:**

```json
{
  "github": true,
  "slack": false,
  "jira": false,
  "available_tools": [
    "github_read_repo",
    "github_create_issue",
    "lookup_npm_package",
    "execute_python",
    "search_stackoverflow"
  ]
}
```

---

### `GET /api/integrations/github/repo/{owner}/{repo}`

Read files from a GitHub repository.

**Query params:**

| Param | Description |
|-------|-------------|
| `path` | File or directory path (optional) |

**Response 200:**

```json
{
  "name": "README.md",
  "content": "# Project\n...",
  "encoding": "base64"
}
```

---

### `POST /api/integrations/github/issue`

Create a GitHub issue.

**Request body:**

```json
{
  "owner": "jadavbindupriya",
  "repo": "multi-agent-coding-assistant",
  "title": "Bug: test failure on edge case",
  "body": "The prime checker fails for n=2..."
}
```

**Response 200:**

```json
{
  "number": 42,
  "url": "https://github.com/jadavbindupriya/multi-agent-coding-assistant/issues/42"
}
```

---

### `POST /api/integrations/slack/message`

Post a message to Slack via webhook.

**Request body:**

```json
{
  "text": "Task completed: prime number checker",
  "channel": "#coding-assistant"
}
```

---

### `POST /api/integrations/jira/task`

Create a Jira task.

**Request body:**

```json
{
  "summary": "Implement email validator",
  "description": "Generated by Multi-Agent Coding Assistant.\n\nSee solution in task output."
}
```

---

## Analytics (`/api/analytics`)

### `GET /api/analytics/summary`

System-wide performance metrics.

**Response 200:**

```json
{
  "total_tasks": 15,
  "total_tokens": 28500,
  "total_cost_usd": 0.855,
  "avg_execution_time": 11.3,
  "agent_performance": {
    "Planner": { "avg_tokens": 250, "avg_time": 1.5, "count": 15 },
    "Coder": { "avg_tokens": 800, "avg_time": 5.2, "count": 15 }
  },
  "error_count": 1,
  "recent_errors": [
    { "agent": "Coder", "error": "Rate limit exceeded", "task_id": "..." }
  ],
  "request_metrics": {
    "total_requests": 120,
    "avg_latency_ms": 45
  }
}
```

---

### `GET /api/analytics/tasks/recent`

Recent task records.

**Response 200:**

```json
{
  "tasks": [
    {
      "task_id": "...",
      "status": "completed",
      "task": "Write a prime checker..."
    }
  ],
  "metrics": [...]
}
```

---

### `GET /api/analytics/errors`

Recent error log.

**Response 200:**

```json
{
  "error_count": 1,
  "recent_errors": [
    { "agent": "Planner", "error": "...", "task_id": "...", "timestamp": "..." }
  ]
}
```

---

## Error format

All HTTP errors return:

```json
{
  "error": "Request failed",
  "detail": "Human-readable error message",
  "code": 400
}
```

## Rate and size limits

| Limit | Value |
|-------|-------|
| Max task length | 5000 characters |
| Max tool iterations | 3 (configurable) |
| Sandbox timeout | 10 seconds (configurable) |
| RAG top-K | 3 chunks (configurable) |

## Authentication

The API has no built-in authentication in development. For production, add API key middleware or OAuth before exposing publicly.
