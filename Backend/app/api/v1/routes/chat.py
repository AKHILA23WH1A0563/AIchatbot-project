from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.db.database import get_db
from bson import ObjectId
from datetime import datetime
from app.api.deps import get_current_user

router = APIRouter()

class StartConversationRequest(BaseModel):
    participants: list[str]

class SendMessageRequest(BaseModel):
    conversationId: str
    text: str  # sender will be taken from token


@router.post("/start")
async def start_conversation(
    payload: StartConversationRequest,
    current_user: dict = Depends(get_current_user)
):
    if not payload.participants or len(payload.participants) < 2:
        raise HTTPException(status_code=400, detail="At least two participants required")

    db = get_db()
    if db is None:
        raise HTTPException(status_code=500, detail="DB not initialized")

    res = await db.conversations.insert_one({
        "participants": payload.participants,
        "created_at": datetime.utcnow(),
    })

    return {"message": "Conversation started", "conversationId": str(res.inserted_id)}


@router.post("/send")
async def send_message(
    payload: SendMessageRequest,
    current_user: dict = Depends(get_current_user)
):
    db = get_db()
    if db is None:
        raise HTTPException(status_code=500, detail="DB not initialized")

    try:
        conv_oid = ObjectId(payload.conversationId)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid conversationId")

    conversation = await db.conversations.find_one({"_id": conv_oid})
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    await db.messages.insert_one({
        "conversationId": conv_oid,
        "sender": current_user["email"],  # token user only
        "text": payload.text,
        "created_at": datetime.utcnow(),
    })

    return {"message": "Message sent"}


@router.get("/messages/{conversation_id}")
async def get_messages(
    conversation_id: str,
    current_user: dict = Depends(get_current_user)
):
    db = get_db()
    if db is None:
        raise HTTPException(status_code=500, detail="DB not initialized")

    try:
        conv_oid = ObjectId(conversation_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid conversationId")

    cursor = db.messages.find({"conversationId": conv_oid}).sort("created_at", 1)

    result = []
    async for msg in cursor:
        result.append({
            "id": str(msg["_id"]),
            "sender": str(msg.get("sender")),
            "text": msg.get("text"),
            "createdAt": msg.get("created_at"),
        })

    return result
