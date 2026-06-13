# backend/rag/vector_store.py
"""ChromaDB vector store for document knowledge base."""

import hashlib
import logging
import os
from pathlib import Path
from typing import List, Optional

from backend.config import settings

logger = logging.getLogger(__name__)

_collection = None
_client = None


def _get_client():
    global _client
    if _client is None:
        import chromadb
        os.makedirs(settings.CHROMA_PATH, exist_ok=True)
        _client = chromadb.PersistentClient(path=settings.CHROMA_PATH)
    return _client


def _get_collection():
    global _collection
    if _collection is None:
        from chromadb.utils import embedding_functions

        ef = embedding_functions.OpenAIEmbeddingFunction(
            api_key=settings.OPENAI_API_KEY,
            model_name=settings.EMBEDDING_MODEL,
        )
        _collection = _get_client().get_or_create_collection(
            name="knowledge_base",
            embedding_function=ef,
            metadata={"description": "Coding standards and project docs"},
        )
    return _collection


def _chunk_text(text: str, chunk_size: int = 800, overlap: int = 100) -> List[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return [c.strip() for c in chunks if c.strip()]


def _doc_id(source: str, chunk_index: int, content: str) -> str:
    raw = f"{source}:{chunk_index}:{content[:50]}"
    return hashlib.md5(raw.encode()).hexdigest()


class VectorStore:
    """Manages document ingestion and vector search via ChromaDB."""

    def add_document(self, content: str, source: str, metadata: Optional[dict] = None) -> int:
        chunks = _chunk_text(content)
        if not chunks:
            return 0

        ids = []
        documents = []
        metadatas = []
        for i, chunk in enumerate(chunks):
            ids.append(_doc_id(source, i, chunk))
            documents.append(chunk)
            meta = {"source": source, "chunk_index": i}
            if metadata:
                meta.update(metadata)
            metadatas.append(meta)

        collection = _get_collection()
        collection.upsert(ids=ids, documents=documents, metadatas=metadatas)
        logger.info(f"Indexed {len(chunks)} chunks from {source}")
        return len(chunks)

    def search(self, query: str, top_k: Optional[int] = None) -> List[dict]:
        top_k = top_k or settings.RAG_TOP_K
        collection = _get_collection()
        if collection.count() == 0:
            return []

        results = collection.query(query_texts=[query], n_results=min(top_k, collection.count()))
        items = []
        for i, doc in enumerate(results["documents"][0]):
            items.append({
                "content": doc,
                "source": results["metadatas"][0][i].get("source", "unknown"),
                "distance": results["distances"][0][i] if results.get("distances") else 0,
            })
        return items

    def list_documents(self) -> List[dict]:
        collection = _get_collection()
        if collection.count() == 0:
            return []

        data = collection.get()
        sources = {}
        for meta in data.get("metadatas", []):
            src = meta.get("source", "unknown")
            sources[src] = sources.get(src, 0) + 1
        return [{"source": k, "chunks": v} for k, v in sources.items()]

    def delete_document(self, source: str) -> int:
        collection = _get_collection()
        data = collection.get(where={"source": source})
        ids = data.get("ids", [])
        if ids:
            collection.delete(ids=ids)
        return len(ids)

    def count(self) -> int:
        return _get_collection().count()


vector_store = VectorStore()
