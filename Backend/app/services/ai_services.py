import os
import uuid
from datetime import datetime
from dotenv import load_dotenv
from app.services.vector_store import search_chunks

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


def get_ai_response(query: str, top_k: int = 3):
    try:
        llm = initialize_llm()

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

        retrieved_chunks = search_chunks(query, top_k=top_k)

        print("\n--- RETRIEVED CHUNKS ---")
        for i, chunk in enumerate(retrieved_chunks, 1):
            print(f"Chunk {i}: {chunk.get('metadata', {}).get('source', 'unknown')}")
            print(chunk.get("content", "")[:300])
            print("-" * 40)

        if not retrieved_chunks:
            return {
                "reply": "I don't have enough information in the provided documents.",
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

        for chunk in retrieved_chunks:
            content = chunk.get("content", "")
            metadata = chunk.get("metadata", {})
            source = metadata.get("source", "unknown")

            sources.add(source)

            truncated_content = content[:1000] if len(content) > 1000 else content
            context_parts.append(f"[Source: {source}]\n{truncated_content}")

        combined_context = "\n\n".join(context_parts)

        rag_prompt = f"""You are a helpful travel assistant.

STRICT RULES:
- Answer ONLY from the provided context.
- Do NOT use outside knowledge.
- If the answer is not present in the context, say exactly:
"I don't have enough information in the provided documents."
- Keep the answer short, clear, and direct.
- Use numbered points only when needed.

Context:
{combined_context}

Question:
{query}

Answer:
"""

        response = llm.invoke(rag_prompt)

        interaction_id = str(uuid.uuid4())

        print(f"\n--- RAG METADATA LOG ---")
        print(f"ID: {interaction_id}")
        print(f"Query: {query}")
        print(f"Chunks Retrieved: {len(retrieved_chunks)}")
        print(f"Sources: {list(sources)}")
        print(f"------------------------\n")

        return {
            "reply": response.content,
            "metadata": {
                "interaction_uuid": interaction_id,
                "timestamp": datetime.now().isoformat(),
                "sources_consulted": list(sources),
                "chunks_retrieved": len(retrieved_chunks),
                "similarity_scores": [c.get("similarity_score") for c in retrieved_chunks],
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
    











  