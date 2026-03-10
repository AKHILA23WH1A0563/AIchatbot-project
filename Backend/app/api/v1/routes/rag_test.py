from fastapi import APIRouter
from pydantic import BaseModel
from app.services.ai_services import get_ai_response

router = APIRouter()

class RAGTestRequest(BaseModel):
    question: str
    top_k: int = 3

@router.post("/test")
def test_rag(req: RAGTestRequest):
    """
    Test endpoint to verify RAG pipeline is working.
    Returns AI response with metadata showing sources and similarity scores.
    """
    result = get_ai_response(req.question, top_k=req.top_k)
    return {
        "question": req.question,
        "answer": result.get("reply"),
        "metadata": result.get("metadata"),
        "status": "success"
    }

@router.get("/health")
def rag_health():
    """Check if RAG system is ready"""
    return {
        "status": "ready",
        "message": "RAG pipeline operational",
        "components": {
            "vector_db": "ChromaDB",
            "embedding_model": "all-MiniLM-L6-v2",
            "llm": "llama-3.1-8b-instant (Groq - Fast)"
        }
    }
