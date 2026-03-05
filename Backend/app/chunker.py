import uuid
from datetime import datetime

def chunk_documents(documents, chunk_size=500, overlap=100):
    """
    Chunks documents into smaller pieces for vector embedding.
    Expected input format:
    documents = [
        {"text": "Extracted text here...", "source": "filename.pdf", "file_type": "pdf"}
    ]
    """
    all_chunks = []

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
                "chunk_id": str(uuid.uuid4()),  # ✅ Unique ID for each chunk
                "content": chunk_text,          # ✅ Key used by embedding_service
                "metadata": {                   # ✅ Grouped metadata for Vector DB
                    "source": source,
                    "file_type": file_type,
                    "chunk_number": chunk_number,
                    "created_at": datetime.now().isoformat()
                }
            }

            all_chunks.append(chunk_data)

            # Move start forward, keeping the specified overlap
            start += (chunk_size - overlap)
            chunk_number += 1

    return all_chunks