from app.services.context_memory import (
    get_recent_chat_history,
    format_chat_history,
    rewrite_query,
    trim_chat_history_by_token_limit
)
from app.services.ai_services import generate_answer
from app.services.chat_history_service import save_chat_history


async def handle_chat(user_id: str, session_id: str, query: str):
    history_docs = await get_recent_chat_history(
        user_id=user_id,
        session_id=session_id,
        limit=5
    )

    chat_history = format_chat_history(history_docs)
    chat_history = trim_chat_history_by_token_limit(chat_history, max_chars=4000)

    rewritten_query = rewrite_query(query, history_docs)

    result = generate_answer(
        query=rewritten_query,
        chat_history=chat_history,
        top_k=3
    )

    final_response = result["reply"]
    sources = result["metadata"].get("sources_consulted", [])

    await save_chat_history(
        user_id=user_id,
        session_id=session_id,
        query=query,
        response=final_response,
        sources=sources
    )

    return {
        "query": query,
        "rewritten_query": rewritten_query,
        "response": final_response,
        "sources": sources
    }