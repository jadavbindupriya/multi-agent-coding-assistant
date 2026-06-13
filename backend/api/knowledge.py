# backend/api/knowledge.py
"""Knowledge base API - document upload and search (Phase 5)."""

import os
from pathlib import Path

from fastapi import APIRouter, HTTPException, UploadFile, File

from backend.config import settings
from backend.rag.vector_store import vector_store
from backend.rag.retriever import retriever
from backend.models.schemas import (
    KnowledgeUploadResponse,
    KnowledgeDocument,
    KnowledgeSearchRequest,
    KnowledgeSearchResult,
)

router = APIRouter()

ALLOWED_EXTENSIONS = {".txt", ".md", ".pdf"}


def _extract_text(filename: str, content: bytes) -> str:
    ext = Path(filename).suffix.lower()
    if ext in (".txt", ".md"):
        return content.decode("utf-8", errors="replace")
    if ext == ".pdf":
        try:
            from pypdf import PdfReader
            import io
            reader = PdfReader(io.BytesIO(content))
            return "\n".join(page.extract_text() or "" for page in reader.pages)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to parse PDF: {e}")
    raise HTTPException(status_code=400, detail=f"Unsupported file type: {ext}")


@router.post("/upload", response_model=KnowledgeUploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """Upload a document (.pdf, .txt, .md) to the knowledge base."""
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Allowed types: {', '.join(ALLOWED_EXTENSIONS)}")

    content = await file.read()
    text = _extract_text(file.filename, content)

    os.makedirs(settings.KNOWLEDGE_UPLOAD_DIR, exist_ok=True)
    save_path = os.path.join(settings.KNOWLEDGE_UPLOAD_DIR, file.filename)
    with open(save_path, "wb") as f:
        f.write(content)

    chunks = vector_store.add_document(text, source=file.filename, metadata={"type": ext})
    return KnowledgeUploadResponse(
        filename=file.filename,
        chunks_indexed=chunks,
        message=f"Indexed {chunks} chunks from {file.filename}",
    )


@router.post("/search", response_model=list[KnowledgeSearchResult])
async def search_knowledge(request: KnowledgeSearchRequest):
    """Search the knowledge base."""
    results = vector_store.search(request.query, top_k=request.top_k)
    return [KnowledgeSearchResult(**r) for r in results]


@router.get("/documents", response_model=list[KnowledgeDocument])
async def list_documents():
    """List all indexed documents."""
    docs = vector_store.list_documents()
    return [KnowledgeDocument(**d) for d in docs]


@router.delete("/documents/{source:path}")
async def delete_document(source: str):
    """Remove a document from the knowledge base."""
    deleted = vector_store.delete_document(source)
    if deleted == 0:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"message": f"Deleted {deleted} chunks from {source}"}


@router.get("/status")
async def knowledge_status():
    """Get knowledge base status."""
    return {
        "document_count": len(vector_store.list_documents()),
        "total_chunks": vector_store.count(),
        "has_knowledge": retriever.has_knowledge(),
    }
