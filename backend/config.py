# backend/config.py
"""Configuration settings for the backend."""

import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Centralized application settings."""

    # API Keys
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    CLAUDE_API_KEY: str = os.getenv("CLAUDE_API_KEY", "")

    # FastAPI
    API_TITLE: str = "Multi-Agent Coding Assistant"
    API_VERSION: str = "0.2.0"
    API_DESCRIPTION: str = (
        "AI system with RAG, tool calling, MCP integrations, "
        "enhanced testing, and analytics"
    )

    # Server
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

    # Model
    DEFAULT_MODEL: str = os.getenv("DEFAULT_MODEL", "gpt-4")
    DEFAULT_TEMPERATURE: float = float(os.getenv("DEFAULT_TEMPERATURE", "0.7"))
    DEFAULT_MAX_TOKENS: int = int(os.getenv("DEFAULT_MAX_TOKENS", "1000"))
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", "logs/app.log")

    # Validation
    MAX_TASK_LENGTH: int = 5000
    MAX_RESPONSE_TIME: int = 60

    # Phase 5: RAG
    CHROMA_PATH: str = os.getenv("CHROMA_PATH", "data/chroma")
    KNOWLEDGE_UPLOAD_DIR: str = os.getenv("KNOWLEDGE_UPLOAD_DIR", "data/uploads")
    RAG_TOP_K: int = int(os.getenv("RAG_TOP_K", "3"))

    # Phase 6: Tool Calling
    ENABLE_TOOLS: bool = os.getenv("ENABLE_TOOLS", "true").lower() == "true"
    SANDBOX_TIMEOUT: int = int(os.getenv("SANDBOX_TIMEOUT", "10"))
    MAX_TOOL_ITERATIONS: int = int(os.getenv("MAX_TOOL_ITERATIONS", "3"))

    # Phase 7: MCP / Integrations
    GITHUB_TOKEN: str = os.getenv("GITHUB_TOKEN", "")
    SLACK_WEBHOOK_URL: str = os.getenv("SLACK_WEBHOOK_URL", "")
    JIRA_URL: str = os.getenv("JIRA_URL", "")
    JIRA_EMAIL: str = os.getenv("JIRA_EMAIL", "")
    JIRA_API_TOKEN: str = os.getenv("JIRA_API_TOKEN", "")
    JIRA_PROJECT_KEY: str = os.getenv("JIRA_PROJECT_KEY", "PROJ")

    # Phase 8: Testing
    ENABLE_TEST_EXECUTION: bool = os.getenv("ENABLE_TEST_EXECUTION", "true").lower() == "true"
    COVERAGE_THRESHOLD: float = float(os.getenv("COVERAGE_THRESHOLD", "0.7"))

    # Phase 9: Monitoring
    DATA_DIR: str = os.getenv("DATA_DIR", "data")
    TOKEN_COST_PER_1K: float = float(os.getenv("TOKEN_COST_PER_1K", "0.03"))


settings = Settings()

if not settings.OPENAI_API_KEY and not settings.CLAUDE_API_KEY:
    print("⚠️  WARNING: No API keys found in .env file!")
    print("   Set OPENAI_API_KEY or CLAUDE_API_KEY in your .env file")
