# backend/tools/stackoverflow.py
"""Search Stack Overflow for coding solutions."""

import logging
import requests

logger = logging.getLogger(__name__)


def search_stackoverflow(query: str, max_results: int = 3) -> dict:
    """Search Stack Overflow via the public API."""
    try:
        url = "https://api.stackexchange.com/2.3/search/advanced"
        params = {
            "order": "desc",
            "sort": "relevance",
            "q": query,
            "site": "stackoverflow",
            "pagesize": max_results,
            "filter": "withbody",
        }
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        results = []
        for item in data.get("items", []):
            body = item.get("body", "")[:500]
            results.append({
                "title": item.get("title", ""),
                "link": item.get("link", ""),
                "score": item.get("score", 0),
                "is_answered": item.get("is_answered", False),
                "excerpt": body,
            })
        return {"query": query, "results": results, "total": len(results)}
    except Exception as e:
        logger.error(f"Stack Overflow search failed: {e}")
        return {"query": query, "results": [], "error": str(e)}
