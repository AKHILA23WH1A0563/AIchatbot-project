from app.db.database import get_db
from datetime import datetime, timezone


async def save_chat_history(
    user_id: str,
    session_id: str,
    query: str,
    response: str,
    sources: list[str]
):

    db = get_db()

    if db is None:
        return

    await db.chat_history.insert_one({
        "user_id": user_id,
        "session_id": session_id,
        "query": query,
        "response": response,
        "sources": sources,
        "timestamp": datetime.now(timezone.utc)
    })