"""
Comprehensive API examples for the Multi-Agent Coding Assistant.

Covers: solve, status, evaluate, knowledge, integrations, and analytics.

Prerequisites:
    1. pip install -r requirements.txt
    2. Set OPENAI_API_KEY in .env
    3. python scripts/run_backend.py
    4. Optional: python scripts/setup_db.py && python scripts/ingest_docs.py data/

Run:
    python Examples/example_api_calls.py
"""

import json
import sys
import time

import requests

BASE_URL = "http://localhost:8000"


def section(title: str):
    print(f"\n{'=' * 60}")
    print(title)
    print("=" * 60)


def get(path: str):
    r = requests.get(f"{BASE_URL}{path}", timeout=30)
    r.raise_for_status()
    return r.json()


def post(path: str, payload: dict):
    r = requests.post(f"{BASE_URL}{path}", json=payload, timeout=120)
    r.raise_for_status()
    return r.json()


def example_health():
    section("Health Check")
    data = get("/health")
    print(json.dumps(data, indent=2))


def example_solve():
    section("Solve a Coding Task")
    data = post("/api/solve", {
        "task": "Write a Python function to find the factorial of a number",
        "language": "python",
        "context": "Use recursion with a base case",
        "use_knowledge": True,
    })
    print(f"Task ID: {data['task_id']}")
    print(f"Confidence: {data['confidence_score']}")
    print(f"Knowledge used: {data['knowledge_used']}")
    print(f"Solution preview:\n{data['solution'][:400]}...")
    return data["task_id"]


def example_status(task_id: str):
    section("Task Status")
    data = get(f"/api/status/{task_id}")
    print(json.dumps(data, indent=2))


def example_evaluate():
    section("Evaluate a Solution")
    data = post("/api/evaluate", {
        "response": "def add(a, b):\n    return a + b",
        "task": "Write a function that adds two numbers",
        "criteria": ["correctness", "readability", "edge_cases"],
    })
    print(f"Score: {data['score']}")
    print(f"Feedback: {data['feedback']}")
    print(f"Strengths: {data['strengths']}")
    print(f"Improvements: {data['improvements']}")


def example_knowledge():
    section("Knowledge Base")
    status = get("/api/knowledge/status")
    print(f"Documents: {status['document_count']}, Chunks: {status['total_chunks']}")

    docs = get("/api/knowledge/documents")
    if docs:
        print("Indexed documents:")
        for doc in docs:
            print(f"  - {doc['source']} ({doc['chunks']} chunks)")
    else:
        print("No documents indexed. Run: python scripts/ingest_docs.py data/")

    results = post("/api/knowledge/search", {
        "query": "Python naming conventions",
        "top_k": 2,
    })
    if results:
        print(f"\nSearch results ({len(results)}):")
        for r in results:
            print(f"  [{r['source']}] {r['content'][:80]}...")
    else:
        print("\nNo search results (knowledge base may be empty).")


def example_integrations():
    section("Integrations Status")
    data = get("/api/integrations/status")
    print(f"GitHub: {'✓' if data['github'] else '✗ (set GITHUB_TOKEN in .env)'}")
    print(f"Slack:  {'✓' if data['slack'] else '✗ (set SLACK_WEBHOOK_URL in .env)'}")
    print(f"Jira:   {'✓' if data['jira'] else '✗ (set JIRA_* vars in .env)'}")
    print(f"Available tools: {', '.join(data['available_tools'])}")


def example_analytics():
    section("Analytics Summary")
    data = get("/api/analytics/summary")
    print(f"Total tasks: {data['total_tasks']}")
    print(f"Total tokens: {data['total_tokens']}")
    print(f"Total cost: ${data['total_cost_usd']:.4f}")
    print(f"Avg execution time: {data['avg_execution_time']:.1f}s")
    print(f"Errors: {data['error_count']}")


def main():
    print("Multi-Agent Coding Assistant — API Examples")
    print(f"Backend: {BASE_URL}")

    try:
        requests.get(f"{BASE_URL}/health", timeout=5).raise_for_status()
    except requests.ConnectionError:
        print("\n✗ Backend not running. Start with: python scripts/run_backend.py")
        sys.exit(1)

    example_health()
    task_id = example_solve()
    example_status(task_id)
    example_evaluate()
    example_knowledge()
    example_integrations()
    example_analytics()

    section("Done")
    print("See docs/API.md for full endpoint reference.")


if __name__ == "__main__":
    main()
