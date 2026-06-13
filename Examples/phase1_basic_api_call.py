"""
Phase 1: Your first API call to the Multi-Agent Coding Assistant.

Prerequisites:
    1. pip install -r requirements.txt
    2. Set OPENAI_API_KEY in .env
    3. python scripts/run_backend.py   (in another terminal)

Run:
    python Examples/phase1_basic_api_call.py
"""

import json
import sys

import requests

BASE_URL = "http://localhost:8000"


def main():
    print("=" * 60)
    print("Phase 1: Basic API Call")
    print("=" * 60)

    # Health check
    try:
        health = requests.get(f"{BASE_URL}/health", timeout=5)
        health.raise_for_status()
        print(f"\n✓ Backend healthy: {health.json()['status']}")
    except requests.ConnectionError:
        print("\n✗ Cannot connect to backend.")
        print("  Start it with: python scripts/run_backend.py")
        sys.exit(1)

    # Submit a coding task
    task = {
        "task": "Write a Python function called is_palindrome that checks if a string is a palindrome",
        "language": "python",
        "use_knowledge": False,
    }

    print(f"\nSubmitting task: {task['task'][:60]}...")
    response = requests.post(f"{BASE_URL}/api/solve", json=task, timeout=120)
    response.raise_for_status()
    data = response.json()

    print(f"\n✓ Task completed (ID: {data['task_id']})")
    print(f"  Tokens used: {data['total_tokens_used']}")
    print(f"  Execution time: {data['execution_time']}s")
    print(f"  Confidence: {data['confidence_score']}")
    print(f"  Estimated cost: ${data['estimated_cost_usd']:.4f}")

    print("\n--- Solution ---")
    print(data["solution"])

    print("\n--- Agent Outputs ---")
    for agent in data["agent_outputs"]:
        print(f"  {agent['agent_name']}: {agent['tokens_used']} tokens, {agent['execution_time']}s")

    print("\n--- Tests (preview) ---")
    print(data["tests"][:300] + ("..." if len(data["tests"]) > 300 else ""))


if __name__ == "__main__":
    main()
