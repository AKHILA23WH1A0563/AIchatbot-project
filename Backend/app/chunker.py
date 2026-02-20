import uuid

def chunk_documents(documents, chunk_size=500, overlap=100):
    """
    documents = [
        {"text": "...", "source": "file.pdf"}
    ]
    """

    all_chunks = []

    for doc in documents:
        words = doc["text"].split()
        source = doc["source"]

        start = 0
        chunk_number = 1

        while start < len(words):
            end = start + chunk_size
            chunk_words = words[start:end]

            chunk_text = " ".join(chunk_words)

            chunk_data = {
                "chunk_id": f"{source}_chunk_{chunk_number}",
                "text": chunk_text,
                "source": source
            }

            all_chunks.append(chunk_data)

            start += (chunk_size - overlap)
            chunk_number += 1

    return all_chunks