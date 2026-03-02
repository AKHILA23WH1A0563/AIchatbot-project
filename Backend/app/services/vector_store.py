# vector_store.py

import logging
from typing import List, Dict, Any
import chromadb
from chromadb.config import Settings

# ✅ correct import path for your project
from app.services.embedding_service import generate_embedding, embed_chunks

logger = logging.getLogger("vector_store")
logger.setLevel(logging.INFO)

CHROMA_PATH = "./chroma_db"              # folder where Chroma will store data
DEFAULT_COLLECTION_NAME = "travel_chunks"

_chroma_client = None


def get_chroma_client() -> chromadb.Client:
    """Create / reuse a persistent Chroma client."""
    global _chroma_client
    if _chroma_client is not None:
        return _chroma_client

    logger.info(f"🔄 Initializing Chroma PersistentClient at: {CHROMA_PATH}")
    _chroma_client = chromadb.PersistentClient(
        path=CHROMA_PATH,
        settings=Settings(anonymized_telemetry=False),
    )
    logger.info("✅ Chroma client ready")
    return _chroma_client


def get_collection(name: str = DEFAULT_COLLECTION_NAME):
    """Create or get a collection (like a table for your chunks)."""
    client = get_chroma_client()
    collection = client.get_or_create_collection(
        name=name,
        metadata={"description": "Travel chatbot knowledge chunks"},
    )
    return collection


def upsert_chunks(
    chunks: List[Dict[str, Any]],
    collection_name: str = DEFAULT_COLLECTION_NAME,
) -> None:
    """
    Store/update chunks in Chroma.

    Each chunk should be like:
    {
      "chunk_id": "1" (optional, will auto-generate if missing),
      "content": "some text",
      "metadata": {...}  # optional
    }
    """
    if not chunks:
        logger.warning("⚠️ No chunks passed to upsert_chunks")
        return

    # Ensure embeddings exist for each chunk
    logger.info("🔄 Generating embeddings for chunks before storing in Chroma")
    chunks = embed_chunks(chunks)

    ids = []
    docs = []
    metas = []
    embs = []

    for i, ch in enumerate(chunks):
        content = ch.get("content", "")
        emb = ch.get("embedding")

        if not content or emb is None:
            logger.warning(f"⚠️ Skipping chunk {i} (missing content or embedding)")
            continue

        cid = ch.get("chunk_id") or f"chunk_{i}"
        ids.append(str(cid))
        docs.append(content)
        metas.append(ch.get("metadata", {}))
        embs.append(emb)

    if not ids:
        logger.warning("⚠️ No valid chunks to store in Chroma")
        return

    collection = get_collection(collection_name)
    logger.info(f"🔄 Upserting {len(ids)} chunks into collection '{collection_name}'")

    # Upsert = insert or update if id already exists
    collection.upsert(
        ids=ids,
        documents=docs,
        metadatas=metas,
        embeddings=embs,
    )

    logger.info(f"✅ Stored {len(ids)} chunks in Chroma")


def search_chunks(
    query: str,
    top_k: int = 5,
    collection_name: str = DEFAULT_COLLECTION_NAME,
) -> List[Dict[str, Any]]:
    """
    Semantic search over chunks stored in Chroma.
    Returns top_k most similar chunks.
    """
    if not query:
        logger.warning("⚠️ Empty query passed to search_chunks")
        return []

    # 1) embed query using same model
    q_emb = generate_embedding(query)
    if q_emb is None:
        logger.error("❌ Failed to generate query embedding")
        return []

    # 2) query Chroma
    collection = get_collection(collection_name)

    res = collection.query(
        query_embeddings=[q_emb],
        n_results=top_k,
        include=["documents", "metadatas",  "distances"],
    )

    ids = res.get("ids")[0]
    docs = res.get("documents", [[]])[0]
    metas = res.get("metadatas", [[]])[0]
    dists = res.get("distances", [[]])[0]

    # Convert distances to similarity (optional)
    out = []
    for cid, doc, meta, dist in zip(ids, docs, metas, dists):
        distance = float(dist)
        similarity = 1.0 / (1.0 + distance)
        out.append(
            {
                "chunk_id": cid,
                "content": doc,
                "metadata": meta,
                "distance": distance,
                "similarity_score": similarity,
            }
        )

    logger.info(f"✅ Found {len(out)} results for query: {query!r}")
    return out


# ------------------ 🔍 SELF-TEST BLOCK ------------------ #

if __name__ == "__main__":
    # Show logs in console
    logging.basicConfig(level=logging.INFO)

    from pprint import pprint

    logger.info("🚀 Running vector_store self-test")

    test_chunks = [
        {
            "chunk_id": "1",
            "content": "Goa is famous for its beautiful beaches.",
            "metadata": {"city": "Goa", "country": "India"},
        },
        {
            "chunk_id": "2",
            "content": "Delhi has many historical monuments and can get very hot in summer.",
            "metadata": {"city": "Delhi", "country": "India"},
        },
    ]

    upsert_chunks(test_chunks)

    results = search_chunks("Which place has beaches?", top_k=2)
    pprint(results)

    logger.info("✅ Self-test finished")