# Multi-Agent Coding Assistant

A production-grade AI system that solves coding tasks using a 4-agent pipeline with RAG, tool calling, MCP integrations, enhanced testing, and analytics.

## Features

### Core Pipeline (Phases 1-4)
- **Multi-Agent Orchestration** - Planner → Coder → Reviewer → Tester
- **Real-time OpenAI Integration** - Direct GPT-4 API calls
- **Beautiful React UI** - Real-time agent execution display

### Phase 5: RAG Integration
- **ChromaDB** vector database for knowledge storage
- **Document upload** (.pdf, .txt, .md) via API and UI
- Agents search knowledge base before solving
- Example: "Check our coding standards before writing code"

### Phase 6: Tool Calling
- **npm package lookup** - Check if packages exist on npm
- **Code sandbox** - Execute Python code safely
- **Stack Overflow search** - Find coding solutions
- Coder agent uses tools automatically when helpful

### Phase 7: MCP Integration
- **GitHub** - Read repos, create issues
- **Slack** - Post results to channels
- **Jira** - Create tasks
- Configure via environment variables

### Phase 8: Enhanced Testing
- **Test execution** - Runs generated pytest tests
- **Property-based testing** - Hypothesis-style tests in generation
- **Edge case detection** - Identifies edge case coverage
- **Coverage reporting** - Line coverage analysis

### Phase 9: Monitoring & Analytics
- **Agent performance metrics** - Per-agent token and timing stats
- **Token usage tracking** - Total tokens across all tasks
- **Cost analysis** - Estimated USD cost per task
- **Error monitoring** - Tracked errors with source attribution

## Quick Start

### Backend

```bash
pip install -r requirements.txt
cp .env.example .env
# Add your OPENAI_API_KEY to .env
python scripts/setup_db.py
python scripts/run_backend.py
```

Backend: `http://localhost:8000`
API Docs: `http://localhost:8000/docs`

### Frontend

```bash
cd frontend
npm install
npm start
```

Frontend: `http://localhost:3000`

### Load Sample Knowledge

```bash
python scripts/ingest_docs.py data/
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/solve` | Submit coding task (with RAG + tools) |
| GET | `/api/status/{task_id}` | Check task status |
| POST | `/api/evaluate` | Evaluate solution quality |
| POST | `/api/knowledge/upload` | Upload document to knowledge base |
| POST | `/api/knowledge/search` | Search knowledge base |
| GET | `/api/knowledge/documents` | List indexed documents |
| GET | `/api/integrations/status` | Check MCP integration status |
| POST | `/api/integrations/github/issue` | Create GitHub issue |
| POST | `/api/integrations/slack/message` | Post to Slack |
| POST | `/api/integrations/jira/task` | Create Jira task |
| GET | `/api/analytics/summary` | System metrics and cost analysis |

## Configuration

See `.env.example` for all settings. Key integrations:

```env
GITHUB_TOKEN=ghp_...
SLACK_WEBHOOK_URL=https://hooks.slack.com/...
JIRA_URL=https://your-org.atlassian.net
JIRA_EMAIL=you@example.com
JIRA_API_TOKEN=...
```

## Architecture

```
React Frontend
├── Knowledge Panel (upload docs)
├── Analytics Panel (metrics)
└── Chat Interface (agent outputs)

FastAPI Backend
├── Orchestrator Pipeline
├── RAG (ChromaDB)
├── Tools (npm, sandbox, Stack Overflow)
├── MCP (GitHub, Slack, Jira)
├── Testing (runner + coverage)
└── Analytics (metrics store)
```

## Project Structure

```
├── backend/
│   ├── agents/          # Planner, Coder, Reviewer, Tester, Evaluator
│   ├── api/             # Routes, knowledge, integrations, analytics
│   ├── rag/             # ChromaDB vector store
│   ├── tools/           # Tool registry and implementations
│   ├── mcp/             # MCP client and service integrations
│   ├── testing/         # Test runner and coverage
│   ├── storage/         # Task and metrics persistence
│   ├── orchestrator/    # Pipeline orchestration
│   └── middleware/      # Request metrics
├── frontend/
│   └── src/components/  # Chat, Knowledge, Analytics panels
├── data/                # ChromaDB, uploads, metrics
└── scripts/             # Setup, ingest, run
```

## Requirements

- Python 3.11+
- Node.js 18+
- OpenAI API key

## License

MIT
