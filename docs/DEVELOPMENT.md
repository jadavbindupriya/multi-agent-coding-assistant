# Development Guide

How to work on the codebase, extend agents, add tools, and run tests.

## Project layout

```
multi_agent_coding_assistant/
├── backend/
│   ├── agents/          # LLM agents (Planner, Coder, Reviewer, Tester, Evaluator)
│   ├── api/             # FastAPI route modules
│   ├── mcp/             # GitHub, Slack, Jira integrations
│   ├── middleware/      # Request metrics middleware
│   ├── models/          # Pydantic request/response schemas
│   ├── orchestrator/    # Multi-agent pipeline
│   ├── rag/             # ChromaDB vector store and retriever
│   ├── storage/         # Task store and metrics persistence
│   ├── testing/         # Test runner and coverage analyzer
│   ├── tools/           # Agent tool implementations
│   ├── tests/           # pytest test suite
│   ├── config.py        # Settings from environment
│   └── main.py          # FastAPI app entry point
├── frontend/
│   └── src/
│       ├── components/  # Chat, Knowledge, Analytics panels
│       └── services/      # API client (axios)
├── data/                  # ChromaDB, uploads, metrics (gitignored runtime data)
├── docs/                  # This documentation
└── scripts/               # setup_db, ingest_docs, run_backend
```

## Local development workflow

### 1. Start backend with hot reload

```bash
python scripts/run_backend.py
```

Uvicorn runs with `reload=True`, so Python file changes restart the server automatically.

### 2. Start frontend dev server

```bash
cd frontend
npm start
```

React hot-reloads on save. API calls proxy to `http://localhost:8000` via `package.json` `"proxy"` setting.

### 3. Run tests after changes

```bash
# All backend tests
pytest backend/tests/ -v

# With coverage
pytest backend/tests/ --cov=backend --cov-report=term-missing

# Single file
pytest backend/tests/test_api.py -v
```

## Adding a new agent

1. Create `backend/agents/my_agent.py` extending patterns from existing agents
2. Use `BaseAgent` from `backend/agents/base.py` for shared LLM and tool-calling logic
3. Return a consistent dict: `{"status": "success"|"error", "tokens_used": int, ...}`
4. Register the agent in `backend/orchestrator/pipeline.py` at the desired step
5. Update `task_store` progress percentages in the pipeline
6. Add tests in `backend/tests/test_agents.py`

### BaseAgent methods

| Method | Use case |
|--------|----------|
| `_chat()` | Simple single-turn LLM call |
| `_chat_with_tools()` | Multi-turn with OpenAI function calling |
| `build_rag_context()` | Combine knowledge base + user context |

Example agent skeleton:

```python
from backend.agents.base import BaseAgent

class MyAgent(BaseAgent):
    def __init__(self):
        super().__init__(system_prompt="You are a specialist agent...")

    def run(self, input_data: str, knowledge: str = "") -> dict:
        context = self.build_rag_context(knowledge)
        prompt = f"{context}\n\nTask:\n{input_data}" if context else input_data
        result = self._chat(prompt)
        return {
            "status": "success",
            "output": result["content"],
            "tokens_used": result["tokens_used"],
        }

my_agent = MyAgent()
```

## Adding a new tool

1. Implement the handler in `backend/tools/my_tool.py`
2. Register it in `backend/tools/registry.py`:
   - Add to `_handlers` dict
   - Add OpenAI function schema in `get_openai_tools()`
3. Tools are available to the **Coder** agent via `_chat_with_tools()`

Existing built-in tools:

| Tool | File | Purpose |
|------|------|---------|
| `lookup_npm_package` | `npm_lookup.py` | Query npm registry |
| `execute_python` | `code_sandbox.py` | Run Python in subprocess sandbox |
| `search_stackoverflow` | `stackoverflow.py` | Search Stack Overflow API |

MCP tools (`github_*`, `slack_*`, `jira_*`) are wired through `mcp_adapter.py`.

## Adding a new API endpoint

1. Add Pydantic schemas in `backend/models/schemas.py`
2. Create or extend a router in `backend/api/`
3. Register the router in `backend/main.py` with `app.include_router()`
4. Add tests in `backend/tests/test_api.py`

## RAG / knowledge base

- **Ingestion**: `vector_store.add_document()` chunks text (800 chars, 100 overlap) and embeds via OpenAI
- **Retrieval**: `retriever.retrieve()` searches ChromaDB before the Planner runs
- **Disable per request**: pass `"use_knowledge": false` in `/api/solve`

To re-index documents:

```bash
python scripts/ingest_docs.py path/to/docs/
```

## Frontend development

Key components:

| Component | File | Purpose |
|-----------|------|---------|
| `App.jsx` | Main layout, task submission |
| `Message.jsx` | Agent output display |
| `KnowledgePanel.jsx` | Document upload and search |
| `AnalyticsPanel.jsx` | Metrics dashboard |
| `api.js` | Axios API client |

The frontend talks to these backend prefixes:

- `/api/solve`, `/api/status`, `/api/evaluate`
- `/api/knowledge/*`
- `/api/integrations/*`
- `/api/analytics/*`

## Code style and conventions

- Python: module docstrings, type hints where practical, logging via `logging.getLogger(__name__)`
- API errors: raise `HTTPException` with clear `detail` messages
- Agent results: always include `status`, `tokens_used`; use `"error"` key on failure
- Config: all settings go through `backend/config.py` — do not read `os.getenv()` elsewhere
- Tests: use `TestClient` from FastAPI; mock external APIs where needed

## Debugging tips

| Symptom | Where to look |
|---------|---------------|
| Agent returns empty output | Check `OPENAI_API_KEY` and `DEFAULT_MODEL` |
| Tools not invoked | Verify `ENABLE_TOOLS=true` in `.env` |
| Knowledge not used | Run ingest script; check `/api/knowledge/status` |
| Tests fail to execute | Check `ENABLE_TEST_EXECUTION` and sandbox permissions |
| Integration unavailable | Check `/api/integrations/status` and `.env` tokens |
| High latency | Review per-agent `execution_time` in solve response |

Enable verbose logging:

```env
LOG_LEVEL=DEBUG
```

Logs write to stdout and optionally `logs/app.log`.

## Git workflow

```bash
git checkout -b feature/my-change
# make changes, run tests
pytest backend/tests/ -v
git add .
git commit -m "Describe your change"
git push -u origin feature/my-change
```

Do not commit `.env`, `data/chroma/`, `node_modules/`, or uploaded files — they are in `.gitignore`.
