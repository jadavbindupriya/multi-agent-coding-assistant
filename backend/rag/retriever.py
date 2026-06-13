# backend/rag/retriever.py
"""Knowledge retrieval for agent context injection."""

import logging
from typing import Optional

from backend.rag.vector_store import vector_store
from backend.config import settings

logger = logging.getLogger(__name__)


class KnowledgeRetriever:
    """Retrieves relevant knowledge before agent execution."""

    def retrieve(self, query: str, top_k: Optional[int] = None) -> str:
        results = vector_store.search(query, top_k=top_k)
        if not results:
            return ""

        parts = []
        for i, item in enumerate(results, 1):
            parts.append(f"[{i}] Source: {item['source']}\n{item['content']}")
        return "\n\n".join(parts)

    def has_knowledge(self) -> bool:
        return vector_store.count() > 0


retriever = KnowledgeRetriever()
