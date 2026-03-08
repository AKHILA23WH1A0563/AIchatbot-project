from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.api.deps import get_current_user
from app.services.session_service import (
    create_session,
    get_user_sessions,
    get_session_history,
    update_session,
    delete_session
)

router = APIRouter()

class CreateSessionRequest(BaseModel):
    session_name: str = "New Chat"

class UpdateSessionRequest(BaseModel):
    session_name: str

@router.post("/create")
async def create_new_session(
    request: CreateSessionRequest,
    current_user: dict = Depends(get_current_user)
):
    """Create a new chat session"""
    session = await create_session(
        user_id=current_user["email"],
        session_name=request.session_name
    )
    return {"message": "Session created", "session": session}

@router.get("/list")
async def list_sessions(current_user: dict = Depends(get_current_user)):
    """Get all sessions for current user"""
    sessions = await get_user_sessions(user_id=current_user["email"])
    return {"sessions": sessions}

@router.get("/{session_id}/history")
async def get_history(
    session_id: str,
    limit: int = 50,
    current_user: dict = Depends(get_current_user)
):
    """Get chat history for a specific session"""
    messages = await get_session_history(session_id=session_id, limit=limit)
    return {"session_id": session_id, "messages": messages}

@router.put("/{session_id}")
async def update_session_name(
    session_id: str,
    request: UpdateSessionRequest,
    current_user: dict = Depends(get_current_user)
):
    """Update session name"""
    await update_session(session_id=session_id, session_name=request.session_name)
    return {"message": "Session updated"}

@router.delete("/{session_id}")
async def delete_session_endpoint(
    session_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Delete a session and all its messages"""
    await delete_session(session_id=session_id)
    return {"message": "Session deleted"}
