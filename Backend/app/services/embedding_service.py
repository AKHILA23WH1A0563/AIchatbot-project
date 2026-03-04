import logging
from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer

# ============================================================
# 🔹 Logging Configuration
# ============================================================

logger = logging.getLogger("embeddings")
logger.setLevel(logging.INFO)

# ============================================================
# 🔹 Model Configuration
# ============================================================

MODEL_NAME = "all-MiniLM-L6-v2"
embedding_model = None  # Global cached model


# ============================================================
# 🔹 Load Embedding Model (Singleton)
# ============================================================

def load_embedding_model():
    """
    Load embedding model once and reuse.
    """
    global embedding_model

    if embedding_model is not None:
        return embedding_model

    try:
        logger.info(f"🔄 Loading embedding model: {MODEL_NAME}")
        embedding_model = SentenceTransformer(MODEL_NAME)
        logger.info("✅ Embedding model loaded successfully")
        return embedding_model
    except Exception as e:
        logger.error(f"❌ Failed to load embedding model: {str(e)}")
        raise


# ============================================================
# 🔹 Generate Single Embedding
# ============================================================

def generate_embedding(text: str) -> List[float] | None:
    """
    Generate embedding for a single text.
    """
    if not text or not isinstance(text, str):
        logger.warning("⚠️ Invalid text provided for embedding")
        return None

    try:
        model = load_embedding_model()
        text = text.strip()

        if not text:
            return None

        embedding = model.encode(text, convert_to_tensor=False)
        return embedding.tolist()

    except Exception as e:
        logger.error(f"❌ Embedding generation failed: {str(e)}")
        return None


# ============================================================
# 🔹 Generate Batch Embeddings (Efficient)
# ============================================================

def generate_batch_embeddings(texts: List[str], batch_size: int = 32) -> List[List[float]]:
    """
    Generate embeddings for multiple texts.
    """
    if not texts:
        logger.warning("⚠️ No texts provided for batch embedding")
        return []

    try:
        model = load_embedding_model()

        clean_texts = [
            t.strip()
            for t in texts
            if t and isinstance(t, str) and t.strip()
        ]

        if not clean_texts:
            return []

        logger.info(f"🔄 Generating embeddings for {len(clean_texts)} texts")

        embeddings = model.encode(
            clean_texts,
            batch_size=batch_size,
            convert_to_tensor=False,
            show_progress_bar=False
        )

        return [emb.tolist() for emb in embeddings]

    except Exception as e:
        logger.error(f"❌ Batch embedding failed: {str(e)}")
        return []


# ============================================================
# 🔹 Embed Chunks (For Vector Store)
# ============================================================

def embed_chunks(chunks: List[dict]) -> List[dict]:
    """
    Generate embeddings for chunk dictionaries.

    Each chunk must contain:
    {
        "chunk_id": "...",
        "content": "...",
        "metadata": {...}
    }

    Returns:
    [
        {
            "chunk_id": "...",
            "content": "...",
            "metadata": {...},
            "embedding": [...]
        }
    ]
    """

    if not chunks:
        logger.warning("⚠️ No chunks provided for embedding")
        return []

    try:
        texts = [chunk.get("content", "") for chunk in chunks]

        embeddings = generate_batch_embeddings(texts)

        if not embeddings:
            return []

        embedded_chunks = []

        for chunk, embedding in zip(chunks, embeddings):
            embedded_chunks.append({
                "chunk_id": chunk.get("chunk_id"),
                "content": chunk.get("content"),
                "metadata": chunk.get("metadata", {}),
                "embedding": embedding
            })

        logger.info(f"✅ Successfully embedded {len(embedded_chunks)} chunks")
        return embedded_chunks

    except Exception as e:
        logger.error(f"❌ embed_chunks failed: {str(e)}")
        return []


# ============================================================
# 🔹 Semantic Search (Cosine Similarity)
# ============================================================

def semantic_search(query: str, chunks: List[dict], top_k: int = 5) -> List[dict]:
    """
    Perform semantic similarity search on chunk list.

    Each chunk must contain:
    {
        "chunk_id": "...",
        "content": "...",
        "embedding": [...]
    }
    """

    if not query or not chunks:
        return []

    try:
        query_embedding = generate_embedding(query)
        if query_embedding is None:
            return []

        query_vec = np.array(query_embedding)
        results = []

        for chunk in chunks:
            if "embedding" in chunk and chunk["embedding"] is not None:
                chunk_vec = np.array(chunk["embedding"])

                similarity = np.dot(query_vec, chunk_vec) / (
                    np.linalg.norm(query_vec) * np.linalg.norm(chunk_vec)
                )

                results.append({
                    "chunk_id": chunk.get("chunk_id"),
                    "content": chunk.get("content"),
                    "metadata": chunk.get("metadata"),
                    "similarity_score": float(similarity)
                })

        results.sort(key=lambda x: x["similarity_score"], reverse=True)
        return results[:top_k]

    except Exception as e:
        logger.error(f"❌ Semantic search failed: {str(e)}")
        return []


# ============================================================
# 🔹 Model Info
# ============================================================

def get_embedding_stats() -> dict:
    """
    Return embedding model information.
    """
    try:
        load_embedding_model()
        return {
            "model_name": MODEL_NAME,
            "embedding_dimension": 384,
            "model_type": "sentence-transformer",
            "status": "ready"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }