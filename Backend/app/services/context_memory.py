from app.db.database import get_db


async def get_recent_chat_history(user_id: str, session_id: str, limit: int = 5):
    db = get_db()

    if db is None:
        return []

    docs = await db.chat_history.find(
        {
            "user_id": user_id,
            "session_id": session_id
        },
        {
            "_id": 0,
            "query": 1,
            "response": 1,
            "timestamp": 1
        }
    ).sort("timestamp", -1).limit(limit).to_list(length=limit)

    docs.reverse()
    return docs


def format_chat_history(history_docs):
    if not history_docs:
        return ""

    lines = []
    for item in history_docs:
        query = item.get("query", "").strip()
        response = item.get("response", "").strip()

        if query:
            lines.append(f"User: {query}")
        if response:
            lines.append(f"Assistant: {response}")

    return "\n".join(lines)


def rewrite_query(current_query: str, history_docs):
    if not history_docs:
        return current_query

    last_query = history_docs[-1].get("query", "").strip()

    follow_up_words = [
        "it", "this", "that", "there", "those", "they", "them",
        "here", "these", "its", "their"
    ]

    words = current_query.lower().split()

    if any(word in words for word in follow_up_words) and last_query:
        return f"{last_query} {current_query}"

    return current_query


def trim_chat_history_by_token_limit(history_text: str, max_chars: int = 4000):
    if not history_text:
        return ""

    if len(history_text) <= max_chars:
        return history_text

    return history_text[-max_chars:]