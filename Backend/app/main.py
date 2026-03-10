from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn
import uuid
from datetime import datetime

from app.api.v1.router import api_router
from app.api.v1.routes import auth
from app.db.database import connect_to_mongo, close_mongo_connection, get_db
from app.services.ai_services import get_ai_response

app = FastAPI(title="AI Travel Chatbot") 

# CORS Configuration for Frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the modular API routers with /api/v1 prefix
app.include_router(api_router, prefix="/api/v1")

# Add auth routes without prefix for frontend compatibility
app.include_router(auth.router, prefix="/auth", tags=["Auth"])

# Database lifecycle management
@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()

from typing import Optional

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    user_id: Optional[str] = "anonymous"

@app.get("/")
def read_root():
    return {"status": "✅ Backend is Running"}

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        db = get_db()
        
        session_id = request.session_id or str(uuid.uuid4())
        user_id = request.user_id
        
        # Retrieve last 5 messages for context
        history_cursor = db.chat_history.find({
            "user_id": user_id,
            "session_id": session_id
        }).sort("timestamp", -1).limit(5)
        
        history_messages = []
        async for msg in history_cursor:
            history_messages.append({
                "query": msg["query"],
                "response": msg["response"]
            })
        
        history_messages.reverse()
        
        # Get AI response with chat history
        full_response = get_ai_response(request.message, chat_history=history_messages)
        
        # Save to MongoDB
        await db.chat_history.insert_one({
            "user_id": user_id,
            "session_id": session_id,
            "query": request.message,
            "response": full_response.get("reply", ""),
            "sources": full_response.get("metadata", {}).get("sources_consulted", []),
            "timestamp": datetime.utcnow()
        })
        
        return {
            "reply": full_response.get("reply"),
            "metadata": full_response.get("metadata", {}),
            "session_id": session_id,
            "history_count": len(history_messages)
        }
        
    except Exception as e:
        return {"reply": f"Error: {str(e)}", "metadata": {}, "session_id": session_id}

@app.get("/chat/history/{session_id}")
async def get_chat_history(session_id: str, limit: int = 50):
    """Get chat history for a session"""
    try:
        db = get_db()
        cursor = db.chat_history.find({"session_id": session_id}).sort("timestamp", 1).limit(limit)
        
        messages = []
        async for msg in cursor:
            messages.append({
                "query": msg["query"],
                "response": msg["response"],
                "sources": msg.get("sources", []),
                "timestamp": msg["timestamp"].isoformat()
            })
        
        return {"session_id": session_id, "messages": messages, "count": len(messages)}
    except Exception as e:
        return {"error": str(e)}

@app.get("/chat/sessions/{user_id}")
async def get_user_sessions(user_id: str):
    """Get all sessions for a user"""
    try:
        db = get_db()
        pipeline = [
            {"$match": {"user_id": user_id}},
            {"$group": {
                "_id": "$session_id",
                "last_message": {"$last": "$timestamp"},
                "message_count": {"$sum": 1},
                "first_query": {"$first": "$query"}
            }},
            {"$sort": {"last_message": -1}}
        ]
        
        sessions = []
        async for session in db.chat_history.aggregate(pipeline):
            sessions.append({
                "session_id": session["_id"],
                "last_message": session["last_message"].isoformat(),
                "message_count": session["message_count"],
                "preview": session["first_query"][:50] + "..." if len(session["first_query"]) > 50 else session["first_query"]
            })
        
        return {"user_id": user_id, "sessions": sessions, "count": len(sessions)}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)