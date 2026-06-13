# Phase 1: Basics

Getting started with the Multi-Agent Coding Assistant API.

## What Phase 1 covers

- Starting the backend server
- Making your first API call
- Understanding the 4-agent pipeline response

## Prerequisites

1. Python 3.11+ installed
2. Dependencies installed: `pip install -r requirements.txt`
3. `.env` file with `OPENAI_API_KEY` set
4. Backend running: `python scripts/run_backend.py`

## The 4-agent pipeline

When you submit a task, four specialized agents work in sequence:

| Agent | Role |
|-------|------|
| **Planner** | Breaks the task into steps |
| **Coder** | Writes the solution code |
| **Reviewer** | Reviews quality and correctness |
| **Tester** | Generates pytest test cases |

## Your first request

### Using curl

```bash
curl -X POST http://localhost:8000/api/solve \
  -H "Content-Type: application/json" \
  -d "{\"task\": \"Write a Python function to reverse a string\", \"language\": \"python\"}"
```

### Using Python

See `phase1_basic_api_call.py` in this folder for a runnable script.

## Response fields

| Field | Description |
|-------|-------------|
| `task_id` | Unique ID for tracking progress |
| `solution` | Generated code |
| `tests` | Generated pytest tests |
| `agent_outputs` | Output from each agent with token usage |
| `confidence_score` | Quality estimate (0.0–1.0) |
| `total_tokens_used` | Total OpenAI tokens consumed |
| `estimated_cost_usd` | Approximate API cost |

## Check task status

```bash
curl http://localhost:8000/api/status/{task_id}
```

## Health check

```bash
curl http://localhost:8000/health
```

## Interactive API docs

Open http://localhost:8000/docs in your browser to try all endpoints with Swagger UI.

## Next steps

- **Phase 5+**: Upload docs to the knowledge base (`POST /api/knowledge/upload`)
- **Examples**: See `example_api_calls.py` for knowledge, integrations, and analytics
- **Full docs**: See `docs/API.md` and `docs/SETUP.md`
