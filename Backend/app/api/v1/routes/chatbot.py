from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from bson import ObjectId
from datetime import datetime
from app.db.database import get_db
from app.api.deps import get_current_user
from app.services.ai_services import get_ai_response

router = APIRouter()

class ChatbotMessageRequest(BaseModel):
    conversationId: str
    text: str

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

    # RAG-based AI response with semantic search
    ai_result = get_ai_response(payload.text)
    bot_reply = ai_result.get("reply", "Sorry, I couldn't process your request.")
    metadata = ai_result.get("metadata", {})

    # Save bot reply with metadata
    await db.messages.insert_one({
        "conversationId": conv_oid,
        "sender": "bot",
        "text": bot_reply,
        "metadata": metadata,
        "created_at": datetime.utcnow()
    })

    return {
        "conversationId": payload.conversationId,
        "sender": "bot",
        "reply": bot_reply,
        "metadata": metadata
    }
