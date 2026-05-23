import os
import uuid
from datetime import datetime
from typing import List, Dict, Any

from app.chunker import chunk_documents
from app.services.vector_store import upsert_chunks

DATA_SOURCE_PATH = "data_source"

def extract_text_from_pdf(path: str) -> str:
    """Extract text using pymupdf (fitz) with pypdf as fallback."""
    text = ""

    # Try pymupdf first — handles more PDF types
    try:
        import fitz
        doc = fitz.open(path)
        for page in doc:
            text += page.get_text()
        doc.close()
        if text.strip():
            return text
    except Exception as e:
        print(f"  pymupdf failed for {path}: {e}")

    # Fallback to pypdf
    try:
        from pypdf import PdfReader
        reader = PdfReader(path)
        for page in reader.pages:
            page_text = page.extract_text() or ""
            text += page_text
    except Exception as e:
        print(f"  pypdf fallback failed for {path}: {e}")

    return text


def ingest_and_store_in_chroma():
    all_documents = []

    if not os.path.exists(DATA_SOURCE_PATH):
        print(f"Folder {DATA_SOURCE_PATH} not found!")
        return

    for filename in os.listdir(DATA_SOURCE_PATH):
        if not filename.lower().endswith(".pdf"):
            continue

        path = os.path.join(DATA_SOURCE_PATH, filename)
        print(f"Loading: {filename}")

        text = extract_text_from_pdf(path)

        if not text.strip():
            print(f"  ⚠️  No text extracted from {filename} (may be a scanned image PDF)")
            continue

        word_count = len(text.split())
        print(f"  ✅ Extracted {word_count} words")

        all_documents.append({
            "text": text,
            "source": filename,
            "file_type": "pdf"
        })

    if not all_documents:
        print("No documents extracted. Nothing to store.")
        return

    # Use chunker with smaller chunks for better retrieval precision
    chunks = chunk_documents(all_documents, chunk_size=300, overlap=50)
    print(f"\n✅ Total chunks created: {len(chunks)}")

    for doc in all_documents:
        doc_chunks = [c for c in chunks if c["metadata"]["source"] == doc["source"]]
        print(f"  {doc['source']}: {len(doc_chunks)} chunks")

    print("\nStoring chunks in ChromaDB...")
    upsert_chunks(chunks)
    print(f"✅ Done. {len(chunks)} chunks stored in ChromaDB.")


if __name__ == "__main__":
    ingest_and_store_in_chroma()


# Alias for backward compatibility with knowledge.py
def ingest_all_sources():
    all_documents = []

    if not os.path.exists(DATA_SOURCE_PATH):
        print(f"Folder {DATA_SOURCE_PATH} not found!")
        return []

    for filename in os.listdir(DATA_SOURCE_PATH):
        if not filename.lower().endswith(".pdf"):
            continue

        path = os.path.join(DATA_SOURCE_PATH, filename)
        text = extract_text_from_pdf(path)

        if not text.strip():
            continue

        all_documents.append({
            "text": text,
            "source": filename,
            "file_type": "pdf"
        })

    return chunk_documents(all_documents, chunk_size=300, overlap=50)
