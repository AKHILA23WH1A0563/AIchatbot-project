from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from bson import ObjectId
from datetime import datetime
from app.db.database import get_db
from app.api.deps import get_current_user

router = APIRouter()

class ChatbotMessageRequest(BaseModel):
    conversationId: str
    text: str

def travel_logic(query: str) -> str:
    q = query.lower()

    if "paris" in q:
        return "Paris: Visit Eiffel Tower, Louvre, Arc de Triomphe!"
    if "flight" in q:
        return "Check Skyscanner or Google Flights for the cheapest flights."

    return "I didn't understand your question. Try asking differently!"

@router.post("/message")
async def chatbot_message(
    payload: ChatbotMessageRequest,
    current_user: dict = Depends(get_current_user)
):
    db = get_db()
    if db is None:

        raise HTTPException(status_code=500, detail="DB not initialized")

    try:
        conv_oid = ObjectId(payload.conversationId)
    except:
        raise HTTPException(status_code=400, detail="Invalid conversationId")

    conversation = await db.conversations.find_one({"_id": conv_oid})
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    # Save user message
    await db.messages.insert_one({
        "conversationId": conv_oid,
        "sender": current_user["email"],
        "text": payload.text,
        "created_at": datetime.utcnow()
    })

    bot_reply = travel_logic(payload.text)

    # Save bot reply
    await db.messages.insert_one({
        "conversationId": conv_oid,
        "sender": "bot",
        "text": bot_reply,
        "created_at": datetime.utcnow()
    })

    return {
        "conversationId": payload.conversationId,
        "sender": "bot",
        "reply": bot_reply
    }
