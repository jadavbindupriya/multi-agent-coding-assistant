# Multi-Agent Coding Assistant

A production-grade AI system that solves coding tasks using a 4-agent pipeline: Planner → Coder → Reviewer → Tester.

## Features

- **Multi-Agent Orchestration** - Sequential pipeline of specialized agents
- **Real-time OpenAI Integration** - Direct GPT-4 API calls
- **Token Tracking** - Monitor API usage and costs
- **Beautiful React UI** - Real-time agent execution display
- **Comprehensive Testing** - Automatic test generation
- **Code Review** - Automated quality validation

## Tech Stack

- **Backend**: FastAPI, Python 3.11, OpenAI API
- **Frontend**: React 18, Axios
- **Database**: PostgreSQL (planned)
- **Deployment**: Railway, Vercel (planned)

## Quick Start

### Backend

```bash
pip install -r requirements.txt
cp .env.example .env
# Add your OPENAI_API_KEY to .env
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

## API Endpoints

**POST /api/solve** - Submit coding task
```json
{"task": "Write a prime checker", "language": "python"}
```

**GET /api/status/{task_id}** - Check task status

**POST /api/evaluate** - Evaluate solution quality

## Architecture
FastAPI Backend
├── Planner Agent (task analysis)
├── Coder Agent (code generation)
├── Reviewer Agent (quality check)
└── Tester Agent (test generation)
React Frontend
└── Real-time display of all agents

## Project Structure
├── backend/
│   ├── agents/ (planner, coder, reviewer, tester)
│   ├── api/ (endpoints)
│   ├── models/ (data schemas)
│   └── main.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── services/
│   │   └── App.jsx
└── scripts/

## Example

Input: "Write function to check if number is prime"

Output:
- Planner: 150 tokens (6-step strategy)
- Coder: 124 tokens (optimized code)
- Reviewer: 442 tokens (quality feedback)
- Tester: 265 tokens (9 test cases)

**Total: 981 tokens**

## Requirements

- Python 3.11+
- Node.js 18+
- OpenAI API key

## License

MIT
