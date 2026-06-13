# scripts/ingest_docs.py
"""Batch ingest documents into the knowledge base."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pathlib import Path
from backend.rag.vector_store import vector_store


def ingest_directory(directory: str):
    """Ingest all .txt, .md, .pdf files from a directory."""
    path = Path(directory)
    if not path.exists():
        print(f"Directory not found: {directory}")
        return

    extensions = {".txt", ".md", ".pdf"}
    total = 0
    for file in path.iterdir():
        if file.suffix.lower() not in extensions:
            continue
        content = file.read_text(encoding="utf-8", errors="replace") if file.suffix != ".pdf" else ""
        if file.suffix == ".pdf":
            try:
                from pypdf import PdfReader
                reader = PdfReader(str(file))
                content = "\n".join(page.extract_text() or "" for page in reader.pages)
            except Exception as e:
                print(f"  ✗ {file.name}: {e}")
                continue
        chunks = vector_store.add_document(content, source=file.name)
        print(f"  ✓ {file.name}: {chunks} chunks")
        total += chunks

    print(f"\nTotal: {total} chunks indexed from {directory}")


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "data/uploads"
    print(f"Ingesting documents from {target}...\n")
    ingest_directory(target)
