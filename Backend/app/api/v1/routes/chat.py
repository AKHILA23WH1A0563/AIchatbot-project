from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.db.database import get_db
from bson import ObjectId
from datetime import datetime, timezone
from app.api.deps import get_current_user
from app.services.chat_history_service import save_chat_history

router = APIRouter()


# ================================
# Request Models
# ================================

class StartConversationRequest(BaseModel):
    participants: list[str]


class SendMessageRequest(BaseModel):
    conversationId: str
    text: str


# ================================
# Start Conversation
# ================================

@router.post("/start")
async def start_conversation(
    payload: StartConversationRequest,
    current_user: dict = Depends(get_current_user)
):

    if not payload.participants or len(payload.participants) < 1:
        raise HTTPException(status_code=400, detail="Participants required")

    db = get_db()

    if db is None:
        raise HTTPException(status_code=500, detail="Database not initialized")

    conversation = {
        "participants": payload.participants,
        "created_at": datetime.now(timezone.utc)
    }

    res = await db.conversations.insert_one(conversation)

    return {
        "message": "Conversation started",
        "conversationId": str(res.inserted_id)
    }


# ================================
# Send Message
# ================================

@router.post("/send")
async def send_message(
    payload: SendMessageRequest,
    current_user: dict = Depends(get_current_user)
):

    db = get_db()

    if db is None:
        raise HTTPException(status_code=500, detail="Database not initialized")

    # Convert ID
    try:
        conv_oid = ObjectId(payload.conversationId)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid conversationId")

    # Check conversation exists
    conversation = await db.conversations.find_one({"_id": conv_oid})

    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    # =============================
    # 1️⃣ Save USER message
    # =============================

    await db.messages.insert_one({
        "conversationId": conv_oid,
        "sender": current_user["email"],
        "text": payload.text,
        "created_at": datetime.now(timezone.utc)
    })

    # =============================
    # 2️⃣ AI RESPONSE (temporary)
    # =============================

    ai_response = "This is an AI generated response based on travel data."

    sources = [
        "air_india_baggage_policy.pdf"
    ]

    # =============================
    # 3️⃣ Save AI message
    # =============================

    await db.messages.insert_one({
        "conversationId": conv_oid,
        "sender": "AI",
        "text": ai_response,
        "created_at": datetime.now(timezone.utc)
    })

    # =============================
    # 4️⃣ Save Chat History
    # =============================

    await save_chat_history(
        user_id=current_user["email"],
        session_id=payload.conversationId,
        query=payload.text,
        response=ai_response,
        sources=sources
    )

    return {
        "response": ai_response,
        "sources": sources
    }


# ================================
# Get Conversation Messages
# ================================

@router.get("/messages/{conversation_id}")
async def get_messages(
    conversation_id: str,
    current_user: dict = Depends(get_current_user)
):

    db = get_db()

    if db is None:
        raise HTTPException(status_code=500, detail="Database not initialized")

    try:
        conv_oid = ObjectId(conversation_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid conversationId")

    cursor = db.messages.find({
        "conversationId": conv_oid
    }).sort("created_at", 1)

    messages = []

    async for msg in cursor:

        messages.append({
            "id": str(msg["_id"]),
            "sender": msg.get("sender"),
            "text": msg.get("text"),
            "createdAt": msg.get("created_at")
        })

    return messages