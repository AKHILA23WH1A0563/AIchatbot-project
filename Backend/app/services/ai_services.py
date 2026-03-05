import os
import uuid
from datetime import datetime
from dotenv import load_dotenv
from app.services.vector_store import search_chunks

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

llm = None

def initialize_llm():
    """Initialize LLM with fallback options"""
    global llm
    
    if llm is not None:
        return llm
    
    try:
        # Try Groq first (fastest)
        from langchain_groq import ChatGroq
        llm = ChatGroq(
            groq_api_key=GROQ_API_KEY, 
            model_name="llama-3.1-8b-instant",
            temperature=0.5,
            max_tokens=350
        )
        print("✅ Using Groq LLM")
        return llm
    except Exception as e:
        print(f"⚠️ Groq failed: {e}")
        # Fallback to Hugging Face (free)
        try:
            from langchain_huggingface import HuggingFaceEndpoint
            llm = HuggingFaceEndpoint(
                repo_id="mistralai/Mistral-7B-Instruct-v0.2",
                temperature=0.7,
                max_new_tokens=500
            )
            print("✅ Using HuggingFace LLM (fallback)")
            return llm
        except:
            raise Exception("No LLM available. Check API keys.")

def get_ai_response(query: str, top_k: int = 3):
    """
    RAG-based AI response using semantic search and LLM.
    
    Args:
        query: User question
        top_k: Number of relevant chunks to retrieve (default: 3 for speed)
        
    Returns:
        dict with reply and metadata
    """
    
    try:
        # Initialize LLM
        llm = initialize_llm()
        
        # Handle simple greetings without RAG
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
        
        # 1. Semantic Retrieval from Vector DB
        retrieved_chunks = search_chunks(query, top_k=3)
        
        if not retrieved_chunks:
            return {
                "reply": "I don't have information about that in my knowledge base. I can help you with:\n\n1. Flight and baggage policies\n2. Travel destinations in India\n3. Airport regulations\n\nPlease ask a specific question about these topics.",
                "metadata": {
                    "interaction_uuid": str(uuid.uuid4()),
                    "timestamp": datetime.now().isoformat(),
                    "sources_consulted": [],
                    "chunks_retrieved": 0,
                    "out_of_scope": True
                }
            }
        
        # 2. Context Injection - Build structured RAG prompt
        context_parts = []
        sources = set()
        
        for i, chunk in enumerate(retrieved_chunks, 1):
            content = chunk.get("content", "")
            metadata = chunk.get("metadata", {})
            source = metadata.get("source", "unknown")
            similarity = chunk.get("similarity_score", 0)
            
            sources.add(source)
            # Limit chunk size to reduce tokens
            truncated_content = content[:600] if len(content) > 600 else content
            context_parts.append(f"[Source: {source}]\n{truncated_content}")
        
        combined_context = "\n\n".join(context_parts)
        
        # 3. Structured RAG Prompt Format - Better formatting
        rag_prompt = f"""You are a helpful travel assistant. Answer the question using the context provided.

Rules:
- Answer directly and clearly
- Use numbered lists when listing multiple items
- If information is not in the context, say: "I don't have that specific information in my knowledge base."
- Be conversational and helpful
- Understand user intent (e.g., "fine" can mean "okay" or "details")

Context:
{combined_context}

Question: {query}

Answer:"""
        
        # 4. LLM-Based Answer Generation
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
        
        # Handle rate limit specifically
        if "rate_limit" in error_msg.lower() or "429" in error_msg:
            return {
                "reply": "I'm currently experiencing high demand. Please try again in a few minutes. In the meantime, you can ask about travel destinations, baggage policies, or flight regulations.",
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