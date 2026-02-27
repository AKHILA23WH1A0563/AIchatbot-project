from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class ChatRequest(BaseModel):
    query: str
    session_id: str = "default"

@router.post("/chat")
async def travel_chat(request: ChatRequest):
    query = request.query.lower()

    if "paris" in query:
        response = "Paris: Eiffel Tower, Louvre Museum. Best hotels: Ritz, Le Meurice."
    elif "flight" in query:
        response = "Flights: Check Skyscanner or Google Flights for best deals."
    else:
        response = "Information not found"

    return {"query": request.query, "response": response}
