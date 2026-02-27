import uuid
from datetime import datetime

def chunk_documents(documents, chunk_size=500, overlap=100):
    """
    documents = [
        {
            "text": "...",
            "source": "file.pdf",
            "file_type": "pdf"
        }
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
                "chunk_id": str(uuid.uuid4()),  # ✅ unique ID
                "content": chunk_text,          # ✅ matches embedding_service
                "metadata": {
                    "source": source,
                    "file_type": file_type,
                    "chunk_number": chunk_number,
                    "created_at": datetime.now().isoformat()
                }
            }

            all_chunks.append(chunk_data)

            start += (chunk_size - overlap)
            chunk_number += 1

    return all_chunks