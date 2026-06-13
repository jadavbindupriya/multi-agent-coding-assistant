# scripts/setup_db.py
"""Initialize data directories, ChromaDB, and storage."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from backend.config import settings


def setup_database():
    """Set up data directories and vector store."""
    dirs = [
        settings.DATA_DIR,
        settings.CHROMA_PATH,
        settings.KNOWLEDGE_UPLOAD_DIR,
        "logs",
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)
        print(f"  OK {d}")

    try:
        from backend.rag.vector_store import vector_store
        count = vector_store.count()
        print(f"  OK ChromaDB initialized ({count} chunks)")
    except Exception as e:
        print(f"  WARN ChromaDB: {e} (will initialize on first use)")

    print("\nSetup complete. Configure .env for MCP integrations (GitHub, Slack, Jira).")


if __name__ == "__main__":
    print("Setting up data storage...\n")
    setup_database()
