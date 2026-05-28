# scripts/run_backend.py
"""
Entry point to run the FastAPI server.

Run this file to start the backend:
    python scripts/run_backend.py
"""

import uvicorn
import sys
import os

# Add parent directory to path so we can import backend module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Starting Multi-Agent Coding Assistant Backend")
    print("=" * 60)
    print("\n📍 API will be available at: http://localhost:8000")
    print("📚 API Docs at: http://localhost:8000/docs")
    print("🛑 Press CTRL+C to stop the server\n")
    
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )