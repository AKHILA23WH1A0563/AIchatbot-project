import uuid
from datetime import datetime
from typing import List, Optional
from app.db.database import get_db

async def create_session(user_id: str, session_name: str = "New Chat") -> dict:
    """Create a new chat session"""
    db = get_db()
    
    session_id = str(uuid.uuid4())
    session_data = {
        "session_id": session_id,
        "user_id": user_id,
        "session_name": session_name,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "message_count": 0
    }
    
    await db.sessions.insert_one(session_data)
    
    return {
        "session_id": session_id,
        "session_name": session_name,
        "created_at": session_data["created_at"].isoformat()
    }

async def get_user_sessions(user_id: str) -> List[dict]:
    """Get all sessions for a user"""
    db = get_db()
    
    cursor = db.sessions.find({"user_id": user_id}).sort("updated_at", -1)
    sessions = []
    
    async for session in cursor:
        sessions.append({
            "session_id": session["session_id"],
            "session_name": session["session_name"],
            "created_at": session["created_at"].isoformat(),
            "updated_at": session["updated_at"].isoformat(),
            "message_count": session.get("message_count", 0)
        })
    
    return sessions

async def get_session_history(session_id: str, limit: int = 50) -> List[dict]:
    """Get chat history for a specific session"""
    db = get_db()
    
    cursor = db.chat_history.find({"session_id": session_id}).sort("timestamp", 1).limit(limit)
    messages = []
    
    async for msg in cursor:
        messages.append({
            "query": msg["query"],
            "response": msg["response"],
            "timestamp": msg["timestamp"].isoformat(),
            "sources": msg.get("sources", [])
        })
    
    return messages

async def update_session(session_id: str, session_name: Optional[str] = None):
    """Update session details"""
    db = get_db()
    
    update_data = {"updated_at": datetime.utcnow()}
    if session_name:
        update_data["session_name"] = session_name
    
    await db.sessions.update_one(
        {"session_id": session_id},
        {"$set": update_data}
    )

async def delete_session(session_id: str):
    """Delete a session and its messages"""
    db = get_db()
    
    # Delete all messages in the session
    await db.chat_history.delete_many({"session_id": session_id})
    
    # Delete the session
    await db.sessions.delete_one({"session_id": session_id})

async def increment_message_count(session_id: str):
    """Increment message count for a session"""
    db = get_db()
    
    await db.sessions.update_one(
        {"session_id": session_id},
        {
            "$inc": {"message_count": 1},
            "$set": {"updated_at": datetime.utcnow()}
        }
    )
