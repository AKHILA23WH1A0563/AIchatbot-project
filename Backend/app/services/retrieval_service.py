from app.services.embedding_service import generate_embedding
from app.services.similarity import cosine_similarity


def retrieve_top_k(query: str, chunks: list, k: int = 3):
    """
    Retrieve top-k most similar chunks for a given query.
    
    Args:
        query (str)
        chunks (list): List of dicts with keys:
                       { "content": str, "embedding": list }
        k (int): number of top results

    Returns:
        list: top-k chunk dictionaries sorted by similarity
    """

    # 1️⃣ Generate query embedding
    query_embedding = generate_embedding(query)

    scored_chunks = []

    # 2️⃣ Compare with each chunk
    for chunk in chunks:
        chunk_embedding = chunk["embedding"]

        score = cosine_similarity(query_embedding, chunk_embedding)

        scored_chunks.append({
            "content": chunk["content"],
            "score": score
        })

    # 3️⃣ Sort by score descending
    scored_chunks.sort(key=lambda x: x["score"], reverse=True)

    # 4️⃣ Return top-k
    return scored_chunks[:k]