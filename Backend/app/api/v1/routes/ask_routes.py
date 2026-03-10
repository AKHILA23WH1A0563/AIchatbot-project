from fastapi import APIRouter
from pydantic import BaseModel

from app.services.ingestion_engine import ingest_all_sources

router = APIRouter()

class AskRequest(BaseModel):
    question: str

@router.post("/ask")
def ask(req: AskRequest):
    context = ingest_all_sources()
    return {
        "question": req.question,
        "context_preview": context[:800]
    }
