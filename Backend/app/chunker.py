# ============================================================
# 🔹 Text Chunker Utility
# Responsible for splitting documents into overlapping chunks
# ============================================================

import uuid
from datetime import datetime
from typing import List, Dict, Any


def chunk_documents(
    documents: List[Dict[str, Any]],
    chunk_size: int = 500,
    overlap: int = 100,
) -> List[Dict[str, Any]]:
    """
    Chunks documents into smaller overlapping pieces for vector embedding.

    Expected input format:
    documents = [
        {
            "text": "Extracted text here...",
            "source": "filename.pdf",
            "file_type": "pdf"
        }
    ]
    """

    all_chunks: List[Dict[str, Any]] = []

    for doc in documents:
        words = doc["text"].split()

        source = doc.get("source", "unknown")
        file_type = doc.get("file_type", "unknown")

        start = 0
        chunk_number = 1

        while start < len(words):
            end = start + chunk_size
            chunk_words = words[start:end]

            chunk_text = " ".join(chunk_words)

            chunk_data = {
                "chunk_id": str(uuid.uuid4()),  # ✅ Unique ID
                "content": chunk_text,          # ✅ Used by embedding service
                "metadata": {
                    "source": source,
                    "file_type": file_type,
                    "chunk_number": chunk_number,
                    "created_at": datetime.now().isoformat(),
                },
            }

            all_chunks.append(chunk_data)

            # Move start forward with overlap
            start += (chunk_size - overlap)
            chunk_number += 1

    return all_chunks