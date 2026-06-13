# Architecture

System design overview for the Multi-Agent Coding Assistant.

## High-level overview

```
┌─────────────────────────────────────────────────────────────┐
│                    React Frontend (:3000)                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │ Chat UI      │  │ Knowledge    │  │ Analytics Panel  │  │
│  │ (agents)     │  │ Panel        │  │ (metrics/cost)   │  │
│  └──────┬───────┘  └──────┬───────┘  └────────┬─────────┘  │
└─────────┼─────────────────┼───────────────────┼──────────────┘
          │                 │                   │
          ▼                 ▼                   ▼
┌─────────────────────────────────────────────────────────────┐
│                  FastAPI Backend (:8000)                     │
│  ┌─────────┐ ┌──────────┐ ┌──────────────┐ ┌────────────┐ │
│  │ /api    │ │/knowledge│ │/integrations │ │ /analytics │ │
│  └────┬────┘ └────┬─────┘ └──────┬───────┘ └─────┬──────┘ │
│       │           │              │               │        │
│       ▼           ▼              ▼               ▼        │
│  ┌─────────────────────────────────────────────────────┐  │
│  │              Orchestrator Pipeline                   │  │
│  │  Planner → Coder → Reviewer → Tester                │  │
│  └─────────────────────────────────────────────────────┘  │
│       │           │              │               │        │
│       ▼           ▼              ▼               ▼        │
│  ┌────────┐  ┌─────────┐  ┌──────────┐  ┌──────────────┐  │
│  │ OpenAI │  │ChromaDB │  │   MCP    │  │ Metrics Store│  │
│  │  API   │  │  (RAG)  │  │ Services │  │ + Task Store │  │
│  └────────┘  └─────────┘  └──────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Core design principles

1. **Specialized agents** — Each agent has a focused role and system prompt; the orchestrator chains them sequentially.
2. **Shared infrastructure** — `BaseAgent` provides LLM calls, RAG context injection, and tool calling for all agents.
3. **Optional features** — RAG, tools, test execution, and MCP integrations degrade gracefully when unconfigured.
4. **Observable pipeline** — Every task is tracked in the task store with per-agent progress, tokens, and timing.

## Agent pipeline

When a user submits a task via `POST /api/solve`, the orchestrator runs:

```
User Task
    │
    ▼
┌───────────┐     Retrieve relevant docs from ChromaDB (if enabled)
│  RAG      │────────────────────────────────────────────┐
└───────────┘                                            │
    │                                                    ▼
    ▼                                          Knowledge context
┌───────────┐
│  Planner  │  Breaks task into step-by-step plan
└─────┬─────┘
      ▼
┌───────────┐
│   Coder   │  Writes solution; may call tools (npm, sandbox, SO, MCP)
└─────┬─────┘
      ▼
┌───────────┐
│ Reviewer  │  Reviews code quality, security, correctness
└─────┬─────┘
      ▼
┌───────────┐
│  Tester   │  Generates pytest tests + property-based cases
└─────┬─────┘
      ▼
┌───────────┐
│ Test Run  │  Executes tests, computes coverage (if enabled)
└─────┬─────┘
      ▼
  Final Response (solution, tests, metrics, confidence score)
```

### Progress tracking

| Step | Agent | Progress % |
|------|-------|------------|
| 1 | Planner | 10% |
| 2 | Coder | 35% |
| 3 | Reviewer | 60% |
| 4 | Tester | 80% |
| 5 | Complete | 100% |

Status is queryable via `GET /api/status/{task_id}`.

### Confidence score

Computed heuristically (0.0–1.0):

- Base: 0.75
- +0.10 if review mentions "excellent" or "good"
- +0.10 if all tests pass
- +0.05 if coverage meets `COVERAGE_THRESHOLD`

## Component details

### Agents (`backend/agents/`)

| Agent | Responsibility | Tool calling |
|-------|----------------|--------------|
| Planner | Decompose task into actionable steps | No |
| Coder | Generate code solution | Yes |
| Reviewer | Code review and feedback | No |
| Tester | Generate pytest + property tests | No |
| Evaluator | Score arbitrary responses (separate endpoint) | No |

All agents use OpenAI via `BaseAgent._chat()` or `_chat_with_tools()`.

### RAG layer (`backend/rag/`)

- **VectorStore** — ChromaDB persistent client; OpenAI embeddings (`text-embedding-3-small`)
- **Chunking** — 800-character chunks with 100-character overlap
- **Retriever** — Semantic search; top-K results injected into agent prompts
- **Storage** — `data/chroma/` (vectors), `data/uploads/` (raw files)

### Tool system (`backend/tools/`)

```
Coder Agent
    │
    ▼
ToolRegistry.get_openai_tools()
    │
    ├── lookup_npm_package
    ├── execute_python      (subprocess sandbox, timeout-limited)
    ├── search_stackoverflow
    └── MCP tools (if configured)
            ├── github_read_repo
            ├── github_create_issue
            ├── slack_post_message
            └── jira_create_task
```

Tool calls loop up to `MAX_TOOL_ITERATIONS` times per Coder invocation.

### MCP integrations (`backend/mcp/`)

| Service | Config | Capabilities |
|---------|--------|--------------|
| GitHub | `GITHUB_TOKEN` | Read repo files, create issues |
| Slack | `SLACK_WEBHOOK_URL` | Post messages |
| Jira | `JIRA_URL`, `JIRA_EMAIL`, `JIRA_API_TOKEN` | Create tasks |

`mcp_client` exposes available services at startup and in `/health`.

### Testing layer (`backend/testing/`)

- **TestRunner** — Writes solution + tests to temp files, runs pytest
- **CoverageAnalyzer** — Line coverage via `pytest-cov`; compares against `COVERAGE_THRESHOLD`
- **Property tests** — Tester agent generates Hypothesis-style edge-case tests

### Storage (`backend/storage/`)

| Store | Purpose | Persistence |
|-------|---------|-------------|
| `task_store` | In-memory task status and messages | Session (in-memory) |
| `metrics_store` | Per-agent tokens, timing, errors | JSON files in `data/` |

### Middleware (`backend/middleware/`)

`MetricsMiddleware` tracks HTTP request counts and latencies, exposed in `/api/analytics/summary`.

## API module structure

| Module | Prefix | Tag |
|--------|--------|-----|
| `routes.py` | `/api` | tasks |
| `knowledge.py` | `/api/knowledge` | knowledge |
| `integrations.py` | `/api/integrations` | integrations |
| `analytics.py` | `/api/analytics` | analytics |

## Data flow example

**Request:** "Write a function to validate email addresses following our coding standards"

1. RAG retrieves chunks from `sample_coding_standards.md`
2. Planner creates a plan referencing naming conventions from docs
3. Coder writes the function; may call `execute_python` to verify
4. Reviewer checks against standards and best practices
5. Tester generates unit tests including edge cases (`""`, invalid formats)
6. Test runner executes pytest; coverage analyzer reports 85%
7. Response includes solution, tests, agent outputs, cost estimate

## Phase map

| Phase | Feature | Key files |
|-------|---------|-----------|
| 1–4 | Core 4-agent pipeline | `agents/`, `orchestrator/pipeline.py` |
| 5 | RAG / knowledge base | `rag/`, `api/knowledge.py` |
| 6 | Tool calling | `tools/`, `agents/base.py` |
| 7 | MCP integrations | `mcp/`, `api/integrations.py` |
| 8 | Test execution + coverage | `testing/` |
| 9 | Analytics + monitoring | `storage/metrics.py`, `api/analytics.py` |

## Security considerations

- API keys loaded from `.env` only — never hardcoded
- Python sandbox runs in subprocess with timeout; not a full isolation boundary
- CORS is open (`*`) in development — restrict for production
- Uploaded files stored locally in `data/uploads/` — validate file types server-side
- GitHub/Jira tokens should use minimum required scopes

## Scalability notes

Current architecture is single-process and in-memory for task tracking. For production scale:

- Replace in-memory `task_store` with Redis or a database
- Run multiple uvicorn workers behind a load balancer
- Use async task queue (Celery, RQ) for long-running solve requests
- Externalize ChromaDB to a managed vector database if document volume grows
