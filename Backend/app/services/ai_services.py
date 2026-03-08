import os
import uuid
from datetime import datetime
from dotenv import load_dotenv
from app.services.vector_store import search_chunks_mmr
from app.services.query_rewriter import rewrite_query_with_history, filter_relevant_chunks

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

llm = None


def initialize_llm():
    global llm

    if llm is not None:
        return llm

    try:
        from langchain_groq import ChatGroq
        llm = ChatGroq(
            groq_api_key=GROQ_API_KEY,
            model_name="llama-3.1-8b-instant",
            temperature=0.2,
            max_tokens=400
        )
        print("✅ Using Groq LLM")
        return llm
    except Exception as e:
        print(f"⚠️ Groq failed: {e}")
        raise Exception("No LLM available. Check API keys.")


def get_ai_response(query: str, chat_history: list = None):
    try:
        llm = initialize_llm()
        
        if chat_history is None:
            chat_history = []

        greetings = ['hi', 'hello', 'hey', 'hii', 'hiii', 'greetings']
        thanks = ['thank you', 'thanks', 'thank u', 'thankyou', 'thx', 'ty']

        query_lower = query.lower().strip()

        if query_lower in greetings:
            return {
                "reply": "Hello! I'm your travel assistant. I can help you with:\n\n1. Flight and baggage information\n2. Travel destinations and tips\n3. Airport regulations and policies\n\nWhat would you like to know?",
                "metadata": {
                    "interaction_uuid": str(uuid.uuid4()),
                    "timestamp": datetime.now().isoformat(),
                    "sources_consulted": [],
                    "chunks_retrieved": 0,
                    "greeting": True
                }
            }

        if query_lower in thanks:
            return {
                "reply": "You're welcome! Is there anything else I can help you with regarding your travel plans?",
                "metadata": {
                    "interaction_uuid": str(uuid.uuid4()),
                    "timestamp": datetime.now().isoformat(),
                    "sources_consulted": [],
                    "chunks_retrieved": 0,
                    "thanks": True
                }
            }
        
        # Rewrite query using chat history
        rewritten_query = rewrite_query_with_history(query, chat_history)
        print(f"\n--- QUERY REWRITING ---")
        print(f"Original: {query}")
        print(f"Rewritten: {rewritten_query}")
        
        # Use MMR retrieval
        retrieved_chunks = search_chunks_mmr(rewritten_query, k=4, fetch_k=10)
        
        # Filter for relevance
        filtered_chunks = filter_relevant_chunks(retrieved_chunks, rewritten_query)

        print("\n--- RETRIEVED CHUNKS ---")
        for i, chunk in enumerate(filtered_chunks, 1):
            print(f"Chunk {i}: {chunk.get('metadata', {}).get('source', 'unknown')}")
            print(chunk.get("content", "")[:300])
            print("-" * 40)

        if not filtered_chunks:
            return {
                "reply": "Information not found in documents.",
                "metadata": {
                    "interaction_uuid": str(uuid.uuid4()),
                    "timestamp": datetime.now().isoformat(),
                    "sources_consulted": [],
                    "chunks_retrieved": 0,
                    "out_of_scope": True
                }
            }

        context_parts = []
        sources = set()

        for chunk in filtered_chunks:
            content = chunk.get("content", "")
            metadata = chunk.get("metadata", {})
            source = metadata.get("source", "unknown")

            sources.add(source)

            truncated_content = content[:1000] if len(content) > 1000 else content
            context_parts.append(f"[Source: {source}]\n{truncated_content}")

        combined_context = "\n\n".join(context_parts)
        
        # Build conversation history context
        history_context = ""
        if chat_history:
            history_context = "\n\nPREVIOUS CONVERSATION:\n"
            for msg in chat_history[-3:]:
                history_context += f"User: {msg.get('query', '')}\nAssistant: {msg.get('response', '')}\n"

        rag_prompt = f"""You are a helpful travel assistant. Answer using the context and conversation history.

IMPORTANT RULES:
1. Use information from CONTEXT below
2. Consider PREVIOUS CONVERSATION to understand follow-up questions
3. If answer is NOT in context, say: "Information not found in documents."
4. Be concise and direct
5. Use bullet points for lists

CONTEXT:
{combined_context}{history_context}

CURRENT QUESTION: {query}

ANSWER:"""

        response = llm.invoke(rag_prompt)

        interaction_id = str(uuid.uuid4())

        print(f"\n--- RAG METADATA LOG ---")
        print(f"ID: {interaction_id}")
        print(f"Query: {query}")
        print(f"Rewritten: {rewritten_query}")
        print(f"Chunks Retrieved: {len(filtered_chunks)}")
        print(f"Sources: {list(sources)}")
        print(f"------------------------\n")

        return {
            "reply": response.content,
            "metadata": {
                "interaction_uuid": interaction_id,
                "timestamp": datetime.now().isoformat(),
                "sources_consulted": list(sources),
                "chunks_retrieved": len(filtered_chunks),
                "similarity_scores": [c.get("similarity_score") for c in filtered_chunks],
                "out_of_scope": False
            }
        }

    except Exception as e:
        error_msg = str(e)
        print(f"❌ RAG Error: {error_msg}")

        if "rate_limit" in error_msg.lower() or "429" in error_msg:
            return {
                "reply": "I'm currently experiencing high demand. Please try again in a few minutes.",
                "metadata": {
                    "interaction_uuid": str(uuid.uuid4()),
                    "timestamp": datetime.now().isoformat(),
                    "error": "rate_limit_exceeded"
                }
            }

        return {
            "reply": "I encountered an error processing your question. Please try again.",
            "metadata": {
                "interaction_uuid": str(uuid.uuid4()),
                "timestamp": datetime.now().isoformat(),
                "error": error_msg
            }
        }
    











  