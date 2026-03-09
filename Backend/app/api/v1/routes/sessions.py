from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.api.deps import get_current_user
from app.services.session_service import (
    create_session,
    get_user_sessions,
    get_session_history,
    update_session,
    delete_session
)

router = APIRouter()


# Request Models
class CreateSessionRequest(BaseModel):
    session_name: str = "New Chat"


class UpdateSessionRequest(BaseModel):
    session_name: str


# Create new chat session
@router.post("/create")
async def create_new_session(
    request: CreateSessionRequest,
    current_user: dict = Depends(get_current_user)
):
    session = await create_session(
        user_id=current_user["email"],
        session_name=request.session_name
    )

    return {
        "message": "Session created",
        "session": session
    }


# Get all sessions of the logged-in user
@router.get("/list")
async def list_sessions(
    current_user: dict = Depends(get_current_user)
):
    sessions = await get_user_sessions(
        user_id=current_user["email"]
    )

    return {
        "sessions": sessions
    }


# Get chat history of a session (User Story 13)
@router.get("/{session_id}/history")
async def get_history(
    session_id: str,
    limit: int = 50,
    page: int = 1,
    current_user: dict = Depends(get_current_user)
):
    messages = await get_session_history(
        session_id=session_id,
        limit=limit,
        page=page
    )

    return {
        "session_id": session_id,
        "messages": messages
    }


# Update session name
@router.put("/{session_id}")
async def update_session_name(
    session_id: str,
    request: UpdateSessionRequest,
    current_user: dict = Depends(get_current_user)
):
    await update_session(
        session_id=session_id,
        session_name=request.session_name
    )

    return {
        "message": "Session updated"
    }


# Delete session and all its messages (User Story 14)
@router.delete("/sessions/{session_id}")
async def delete_session_endpoint(
    session_id: str,
    current_user: dict = Depends(get_current_user)
):
    await delete_session(session_id=session_id)

    return {
        "message": "Session deleted successfully"
    }