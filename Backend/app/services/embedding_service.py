import logging
from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer
import torch

# Configure logging
logger = logging.getLogger("embeddings")
logger.setLevel(logging.INFO)

# Use a simple, lightweight embedding model (good for travel chatbot)
# All-MiniLM-L6-v2 is fast and effective (384 dimensions)
MODEL_NAME = "all-MiniLM-L6-v2"

# Global model instance (loaded once)
embedding_model = None


def load_embedding_model():
    """
    Load the embedding model once and cache it.
    Uses a lightweight transformer model optimized for semantic similarity.
    """
    global embedding_model
    
    if embedding_model is not None:
        return embedding_model
    
    try:
        logger.info(f"🔄 Loading embedding model: {MODEL_NAME}")
        embedding_model = SentenceTransformer(MODEL_NAME)
        logger.info(f"✅ Embedding model loaded successfully")
        return embedding_model
    except Exception as e:
        logger.error(f"❌ Failed to load embedding model: {str(e)}")
        raise


def generate_embedding(text: str) -> List[float]:
    """
    Generate a single embedding vector for text.
    
    Args:
        text: The text to embed
        
    Returns:
        A list of float values representing the embedding vector
    """
    if not text or not isinstance(text, str):
        logger.warning("⚠️  Empty or invalid text provided for embedding")
        return None
    
    try:
        model = load_embedding_model()
        
        # Normalize text
        text = text.strip()
        if not text:
            return None
        
        # Generate embedding
        embedding = model.encode(text, convert_to_tensor=False)
        
        # Convert to list of floats
        return embedding.tolist()
        
    except Exception as e:
        logger.error(f"❌ Error generating embedding for text: {str(e)}")
        return None


def generate_batch_embeddings(texts: List[str], batch_size: int = 32) -> List[dict]:
    """
    Generate embeddings for multiple texts in batches (efficient).
    
    Args:
        texts: List of text strings to embed
        batch_size: Number of texts to process at once (default 32)
        
    Returns:
        List of dicts with text and embedding: 
        [{"text": "...", "embedding": [...], "success": True}]
    """
    if not texts:
        logger.warning("⚠️  No texts provided for batch embedding")
        return []
    
    results = []
    
    try:
        model = load_embedding_model()
        
        # Clean and validate texts
        clean_texts = []
        text_indices = []
        
        for idx, text in enumerate(texts):
            if text and isinstance(text, str):
                clean_text = text.strip()
                if clean_text:
                    clean_texts.append(clean_text)
                    text_indices.append(idx)
        
        if not clean_texts:
            logger.warning("⚠️  No valid texts after cleaning")
            return []
        
        logger.info(f"🔄 Generating embeddings for {len(clean_texts)} texts (batch_size={batch_size})")
        
        # Generate embeddings in batches
        embeddings = model.encode(
            clean_texts,
            batch_size=batch_size,
            convert_to_tensor=False,
            show_progress_bar=False
        )
        
        # Combine results
        for i, (original_idx, text) in enumerate(zip(text_indices, clean_texts)):
            results.append({
                "index": original_idx,
                "text": text,
                "embedding": embeddings[i].tolist(),
                "success": True,
                "dimension": len(embeddings[i])
            })
        
        logger.info(f"✅ Successfully generated {len(results)} embeddings")
        return results
        
    except Exception as e:
        logger.error(f"❌ Batch embedding generation failed: {str(e)}")
        # Return failed results for all texts
        return [
            {"text": t, "embedding": None, "success": False, "error": str(e)}
            for t in texts
        ]


def embed_chunks(chunks: List[dict]) -> List[dict]:
    """
    Add embeddings to a list of chunks.
    
    Args:
        chunks: List of chunk dicts with "content" field
        
    Returns:
        Chunks with added "embedding" field
    """
    if not chunks:
        return []
    
    try:
        # Extract content from chunks
        contents = [chunk.get("content", "") for chunk in chunks]
        
        # Generate embeddings in batch
        embedding_results = generate_batch_embeddings(contents)
        
        # Map embeddings back to chunks
        for i, chunk in enumerate(chunks):
            if i < len(embedding_results) and embedding_results[i]["success"]:
                chunk["embedding"] = embedding_results[i]["embedding"]
                chunk["embedding_dimension"] = embedding_results[i]["dimension"]
            else:
                logger.warning(f"⚠️  Failed to embed chunk {i}")
                chunk["embedding"] = None
        
        return chunks
        
    except Exception as e:
        logger.error(f"❌ Error embedding chunks: {str(e)}")
        return chunks


def semantic_search(query: str, chunk_embeddings: List[dict], top_k: int = 5) -> List[dict]:
    """
    Find chunks most similar to a query using semantic similarity.
    Uses cosine similarity between query embedding and chunk embeddings.
    
    Args:
        query: Query text
        chunk_embeddings: List of chunks with embeddings
        top_k: Number of top results to return
        
    Returns:
        Top K most similar chunks sorted by similarity score
    """
    if not query or not chunk_embeddings:
        logger.warning("⚠️  Empty query or chunks for semantic search")
        return []
    
    try:
        # Generate query embedding
        query_embedding = generate_embedding(query)
        if query_embedding is None:
            logger.error("❌ Failed to generate query embedding")
            return []
        
        # Calculate cosine similarity with all chunk embeddings
        query_vec = np.array(query_embedding)
        results = []
        
        for chunk in chunk_embeddings:
            if "embedding" in chunk and chunk["embedding"] is not None:
                chunk_vec = np.array(chunk["embedding"])
                
                # Cosine similarity = dot product / (norm1 * norm2)
                similarity = np.dot(query_vec, chunk_vec) / (
                    np.linalg.norm(query_vec) * np.linalg.norm(chunk_vec)
                )
                
                results.append({
                    "chunk_id": chunk.get("chunk_id"),
                    "content": chunk.get("content"),
                    "metadata": chunk.get("metadata"),
                    "similarity_score": float(similarity)
                })
        
        # Sort by similarity and return top K
        results.sort(key=lambda x: x["similarity_score"], reverse=True)
        
        logger.info(f"✅ Semantic search found {len(results[:top_k])} similar chunks")
        return results[:top_k]
        
    except Exception as e:
        logger.error(f"❌ Semantic search failed: {str(e)}")
        return []


def get_embedding_stats() -> dict:
    """Get information about the embedding model."""
    try:
        model = load_embedding_model()
        return {
            "model_name": MODEL_NAME,
            "embedding_dimension": 384,  # all-MiniLM-L6-v2 produces 384-dim embeddings
            "model_type": "sentence-transformer",
            "status": "ready"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }
