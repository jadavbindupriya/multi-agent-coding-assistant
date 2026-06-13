# Setup Guide

Step-by-step instructions to run the Multi-Agent Coding Assistant locally.

## Prerequisites

| Requirement | Version |
|-------------|---------|
| Python | 3.11+ |
| Node.js | 18+ |
| npm | 9+ |
| OpenAI API key | Required |

Optional integrations (GitHub, Slack, Jira) need their own tokens — the app runs without them.

## 1. Clone and install

```bash
git clone https://github.com/jadavbindupriya/multi-agent-coding-assistant.git
cd multi-agent-coding-assistant
```

### Backend dependencies

```bash
pip install -r requirements.txt
```

### Frontend dependencies

```bash
cd frontend
npm install
cd ..
```

## 2. Environment configuration

Copy the example env file and add your API key:

```bash
cp .env.example .env
```

Edit `.env` manually and set at minimum:

```env
OPENAI_API_KEY=sk-your-key-here
```

### All configuration options

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | — | OpenAI API key (required) |
| `CLAUDE_API_KEY` | — | Optional fallback key |
| `DEBUG` | `True` | FastAPI debug mode |
| `ENVIRONMENT` | `development` | Environment label |
| `DEFAULT_MODEL` | `gpt-4` | LLM model for all agents |
| `CHROMA_PATH` | `data/chroma` | ChromaDB storage path |
| `KNOWLEDGE_UPLOAD_DIR` | `data/uploads` | Uploaded document storage |
| `RAG_TOP_K` | `3` | Knowledge chunks retrieved per query |
| `EMBEDDING_MODEL` | `text-embedding-3-small` | OpenAI embedding model |
| `ENABLE_TOOLS` | `true` | Enable agent tool calling |
| `SANDBOX_TIMEOUT` | `10` | Python sandbox timeout (seconds) |
| `MAX_TOOL_ITERATIONS` | `3` | Max tool-call loops per agent |
| `GITHUB_TOKEN` | — | GitHub personal access token |
| `SLACK_WEBHOOK_URL` | — | Slack incoming webhook URL |
| `JIRA_URL` | — | Jira instance URL |
| `JIRA_EMAIL` | — | Jira account email |
| `JIRA_API_TOKEN` | — | Jira API token |
| `JIRA_PROJECT_KEY` | `PROJ` | Default Jira project key |
| `ENABLE_TEST_EXECUTION` | `true` | Run generated pytest tests |
| `COVERAGE_THRESHOLD` | `0.7` | Minimum coverage target (70%) |
| `DATA_DIR` | `data` | Metrics and task storage |
| `TOKEN_COST_PER_1K` | `0.03` | Cost estimate per 1K tokens (USD) |

## 3. Initialize data storage

Creates directories for ChromaDB, uploads, logs, and metrics:

```bash
python scripts/setup_db.py
```

Expected output:

```
Setting up data storage...

  OK data
  OK data/chroma
  OK data/uploads
  OK logs
  OK ChromaDB initialized (0 chunks)

Setup complete.
```

## 4. Load sample knowledge (optional)

Index coding standards and other docs into the RAG knowledge base:

```bash
python scripts/ingest_docs.py data/
```

Supported file types: `.txt`, `.md`, `.pdf`

You can also upload documents later via the UI **Knowledge Panel** or the `/api/knowledge/upload` endpoint.

## 5. Start the backend

```bash
python scripts/run_backend.py
```

| URL | Purpose |
|-----|---------|
| http://localhost:8000 | API root |
| http://localhost:8000/docs | Swagger UI (interactive API docs) |
| http://localhost:8000/health | Health check |

## 6. Start the frontend

In a separate terminal:

```bash
cd frontend
npm start
```

Frontend runs at **http://localhost:3000** and proxies API requests to port 8000.

## 7. Verify everything works

### Health check

```bash
curl http://localhost:8000/health
```

### Submit a test task

```bash
curl -X POST http://localhost:8000/api/solve \
  -H "Content-Type: application/json" \
  -d '{"task": "Write a Python function to reverse a string", "language": "python"}'
```

### Run backend tests

```bash
pytest backend/tests/ -v
```

## MCP integrations (optional)

### GitHub

1. Create a [Personal Access Token](https://github.com/settings/tokens) with `repo` scope
2. Add to `.env`: `GITHUB_TOKEN=ghp_...`
3. Verify: `GET /api/integrations/status`

### Slack

1. Create an [Incoming Webhook](https://api.slack.com/messaging/webhooks)
2. Add to `.env`: `SLACK_WEBHOOK_URL=https://hooks.slack.com/...`

### Jira

1. Generate an [API token](https://id.atlassian.com/manage-profile/security/api-tokens)
2. Set `JIRA_URL`, `JIRA_EMAIL`, `JIRA_API_TOKEN`, and `JIRA_PROJECT_KEY` in `.env`

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `No API keys found` warning | Set `OPENAI_API_KEY` in `.env` |
| ChromaDB errors on first run | Run `python scripts/setup_db.py` |
| Frontend can't reach API | Ensure backend is running on port 8000 |
| CORS errors | Backend allows all origins in development |
| PDF upload fails | Install `pypdf`: `pip install pypdf` |
| High token costs | Use `gpt-3.5-turbo` via `DEFAULT_MODEL` in `.env` |

## Production notes

- Set `DEBUG=False` and `ENVIRONMENT=production`
- Restrict CORS origins in `backend/main.py`
- Use a process manager (e.g. `gunicorn` with uvicorn workers) instead of `reload=True`
- Store secrets in a vault, not in `.env` committed to git
