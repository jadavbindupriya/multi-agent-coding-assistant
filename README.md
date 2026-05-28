# Multi-Agent Coding Assistant 🤖

A production-ready AI system where multiple specialized agents work together to solve coding tasks.

## 🎯 Project Goal

Build a system where:
- **Planner Agent** breaks down coding tasks
- **Coder Agent** writes the actual code
- **Reviewer Agent** checks for bugs and improvements
- **Tester Agent** creates and runs tests
- **RAG Agent** searches project documentation
- **Final Answer Agent** synthesizes everything

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- OpenAI API key or Claude API key

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/multi-agent-coding-assistant.git
cd multi-agent-coding-assistant

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your API keys
```

### Run Backend

```bash
python scripts/run_backend.py
```

API will be available at: `http://localhost:8000`
API Docs: `http://localhost:8000/docs`

## 📁 Project Structure
multi-agent-coding-assistant/
├── backend/          # FastAPI application
├── frontend/         # React UI (Phase 10)
├── docs/             # Documentation
├── examples/         # Learning materials
└── scripts/          # Utility scripts
## 🔄 Development Phases

- [x] Phase 1: GenAI Basics
- [x] Phase 2: FastAPI Backend
- [ ] Phase 3: Single-Agent Assistant
- [ ] Phase 4: Multi-Agent System
- [ ] Phase 5: RAG Integration
- [ ] Phase 6: Tool Calling
- [ ] Phase 7: MCP Integration
- [ ] Phase 8: Testing Agent
- [ ] Phase 9: Evaluation & Monitoring
- [ ] Phase 10: React Frontend
- [ ] Phase 11: Docker
- [ ] Phase 12: Deploy to Production
- [ ] Phase 13: Interview Preparation

## 🛠️ Tech Stack

- **Backend**: FastAPI + Python
- **Frontend**: React + TypeScript
- **LLM**: OpenAI GPT-4 / Claude
- **Orchestration**: LangGraph
- **Vector DB**: ChromaDB
- **Deployment**: Docker + Railway/Render

## 📚 Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [Setup Guide](docs/SETUP.md)
- [API Reference](docs/API.md)
- [Development](docs/DEVELOPMENT.md)

## 💡 Interview Talking Points

This project demonstrates:
- **GenAI**: Multi-agent systems, LLM orchestration, RAG
- **Backend**: FastAPI, async programming, API design
- **Architecture**: System design, agent coordination
- **DevOps**: Docker, deployment strategies

## 📝 License

MIT License - See LICENSE file

## 👤 Author

Bindu Priya - GenAI Engineer
