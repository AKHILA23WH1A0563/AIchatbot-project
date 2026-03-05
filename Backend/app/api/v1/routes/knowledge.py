from fastapi import APIRouter, HTTPException
from datetime import datetime
from app.db.database import get_db
from app.services.ingestion_engine import ingest_all_sources
from app.utils.cleaner import clean_text
from app.services.embedding_service import (
    embed_chunks,
    semantic_search,
    get_embedding_stats
)

router = APIRouter()


@router.post("/ingest")
async def ingest_documents():
    db = get_db()
    if db is None:
        raise HTTPException(status_code=500, detail="Database not initialized")

    try:
        chunks = ingest_all_sources()

        if not chunks:
            return {"message": "No PDFs found", "total_chunks": 0}

        chunks_with_embeddings = embed_chunks(chunks)

        chunks_collection = db.chunks
        documents_collection = db.documents

        inserted = 0
        failed = 0
        processed_sources = set()

        for chunk in chunks_with_embeddings:
            chunk_data = {
                "chunk_id": chunk.get("chunk_id"),
                "content": clean_text(chunk.get("content", "")),
                "metadata": chunk.get("metadata", {}),
                "embedding": chunk.get("embedding"),
                "embedding_dimension": chunk.get("embedding_dimension"),
                "created_at": datetime.now().isoformat()
            }

            if chunk.get("embedding") is None:
                failed += 1

            await chunks_collection.insert_one(chunk_data)
            inserted += 1
            processed_sources.add(chunk["metadata"]["source"])

        for source in processed_sources:
            source_chunks = [
                c for c in chunks_with_embeddings
                if c["metadata"]["source"] == source
            ]

            await documents_collection.insert_one({
                "source_name": source,
                "source_type": source_chunks[0]["metadata"]["file_type"],
                "total_chunks": len(source_chunks),
                "ingestion_date": datetime.now().isoformat(),
                "status": "completed"
            })

        return {
            "message": "Ingestion completed",
            "total_chunks_created": inserted,
            "chunks_with_embeddings": inserted - failed,
            "embedding_failed": failed,
            "documents_processed": list(processed_sources)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/chunks")
async def get_chunks(limit: int = 10, skip: int = 0):
    db = get_db()
    if db is None:
        raise HTTPException(status_code=500, detail="Database not initialized")

    cursor = db.chunks.find().skip(skip).limit(limit)
    chunks = await cursor.to_list(length=limit)

    for chunk in chunks:
        chunk["_id"] = str(chunk["_id"])

    total = await db.chunks.count_documents({})

    return {
        "chunks": chunks,
        "total": total,
        "limit": limit,
        "skip": skip
    }


@router.get("/chunks/{chunk_id}")
async def get_chunk_by_id(chunk_id: str):
    db = get_db()
    if db is None:
        raise HTTPException(status_code=500, detail="Database not initialized")

    chunk = await db.chunks.find_one({"chunk_id": chunk_id})

    if not chunk:
        raise HTTPException(status_code=404, detail="Chunk not found")

    chunk["_id"] = str(chunk["_id"])
    return chunk


@router.get("/documents")
async def get_documents():
    db = get_db()
    if db is None:
        raise HTTPException(status_code=500, detail="Database not initialized")

    cursor = db.documents.find()
    docs = await cursor.to_list(length=1000)

    for doc in docs:
        doc["_id"] = str(doc["_id"])

    return {"documents": docs, "total": len(docs)}


@router.post("/search")
async def semantic_search_endpoint(query: str, top_k: int = 5):
    db = get_db()
    if db is None:
        raise HTTPException(status_code=500, detail="Database not initialized")

    cursor = db.chunks.find(
        {"embedding": {"$exists": True, "$ne": None}},
        {"chunk_id": 1, "content": 1, "metadata": 1, "embedding": 1}
    ).limit(500)

    chunks = await cursor.to_list(length=500)

    if not chunks:
        return {"query": query, "results": []}

    results = semantic_search(query, chunks, top_k)

    return {
        "query": query,
        "results_count": len(results),
        "results": results
    }


@router.get("/embedding-stats")
async def get_embedding_stats_endpoint():
    return get_embedding_stats()