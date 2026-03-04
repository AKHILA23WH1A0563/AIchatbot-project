import os
import uuid
import sys
from unittest.mock import MagicMock
from datetime import datetime
from PyPDF2 import PdfReader
from dotenv import load_dotenv

# Shield against broken Windows DLLs
sys.modules["torch"] = MagicMock()
sys.modules["transformers"] = MagicMock()

from langchain_groq import ChatGroq

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

knowledge_base = []
llm = None

def load_pdfs(folder_path="data_source"):
    documents = []
    if not os.path.exists(folder_path):
        print(f"❌ Folder {folder_path} not found!")
        return documents
    for file in os.listdir(folder_path):
        if file.endswith(".pdf"):
<<<<<<< HEAD
=======
            file_path = os.path.join(folder_path, file)

>>>>>>> e1bfd89 (Completed full project implementation)
            try:
                reader = PdfReader(os.path.join(folder_path, file))
                text = " ".join([p.extract_text() for p in reader.pages if p.extract_text()])
                
                # --- USER STORY 3: INGESTION METADATA ---
                documents.append({
                    "chunk_id": str(uuid.uuid4()),                # Unique ID
                    "text": text,
                    "source": file,                               # Traceability
                    "ingestion_date": datetime.now().isoformat()  # Timestamp
                })
                print(f"✅ Loaded: {file}")
            except Exception as e: 
                print(f"⚠️ Error loading {file}: {e}")
                continue
    return documents

<<<<<<< HEAD
=======

# ============================================
# 🔹 STEP 2: Chunk Documents
# ============================================

def chunk_documents(documents, chunk_size=500, overlap=100):
    all_chunks = []

    for doc in documents:
        words = doc["text"].split()
        source = doc["source"]

        start = 0
        chunk_number = 1

        while start < len(words):
            end = start + chunk_size
            chunk_words = words[start:end]

            chunk_text = " ".join(chunk_words)

            chunk_data = {
                "chunk_id": f"{source}_chunk_{chunk_number}",
                "text": chunk_text,
                "source": source
            }

            all_chunks.append(chunk_data)

            start += (chunk_size - overlap)
            chunk_number += 1

    print(f"📦 Total chunks created: {len(all_chunks)}")
    return all_chunks


# ============================================
# 🔹 STEP 3: Initialize RAG
# ============================================

def initialize_rag():
    global vector_db, llm

    print("🚀 Initializing RAG system...")

    documents = load_pdfs("data_source")
    chunks = chunk_documents(documents)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    if chunks:
        texts = [chunk["text"] for chunk in chunks]
        metadatas = [
            {
                "chunk_id": chunk["chunk_id"],
                "source": chunk["source"]
            }
            for chunk in chunks
        ]

        print("⏳ Building vector database...")

        vector_db = FAISS.from_texts(
            texts=texts,
            embedding=embeddings,
            metadatas=metadatas
        )
    else:
        print("⚠ No documents found. Running in AI-only mode.")
        vector_db = None

    llm = ChatGroq(
        groq_api_key=GROQ_API_KEY,
        temperature=0.2,  # Lower temperature for grounded answers
        model_name="llama-3.1-8b-instant"
    )

    print("✅ RAG system initialized successfully")


# ============================================
# 🔹 STEP 4: Structured RAG Prompt Builder (US-8 Core)
# ============================================

def build_rag_prompt(question, retrieved_docs):
    """
    Build structured RAG prompt for context injection.
    Ensures grounded and hallucination-free responses.
    """

    context_text = "\n\n".join(
        [f"[Source: {doc.metadata.get('source')}]\n{doc.page_content}"
         for doc in retrieved_docs]
    )

    prompt = f"""
You are a professional AI assistant.

IMPORTANT INSTRUCTIONS:
- Answer ONLY using the provided document context.
- Do NOT use outside knowledge.
- If the answer is not found in the context, say:
  "I don't have enough information in the provided documents."
- Keep the answer clear, structured, and professional.

=======================
DOCUMENT CONTEXT:
=======================
{context_text}

=======================
USER QUESTION:
=======================
{question}

=======================
FINAL ANSWER:
=======================
"""

    return prompt


# ============================================
# 🔹 STEP 5: Get AI Response (Updated RAG Core)
# ============================================

>>>>>>> e1bfd89 (Completed full project implementation)
def get_ai_response(query: str):
    global knowledge_base, llm
    if not knowledge_base:
        knowledge_base = load_pdfs("data_source")
    if not llm:
        llm = ChatGroq(groq_api_key=GROQ_API_KEY, model_name="llama-3.1-8b-instant")

<<<<<<< HEAD
    # Search logic
    query_words = query.lower().split()
    relevant_sources = []
    combined_context = ""

    for doc in knowledge_base:
        if any(word in doc["text"].lower() for word in query_words):
            combined_context += doc["text"][:2000] + "\n\n"
            relevant_sources.append(doc["source"])

    if not combined_context and knowledge_base:
        combined_context = knowledge_base[0]["text"][:4000]
        relevant_sources = [knowledge_base[0]["source"]]

    # --- START OF THE TRY BLOCK ---
    try:
        interaction_id = str(uuid.uuid4())
        sources = list(set(relevant_sources))
=======
    if not llm:
        initialize_rag()

    try:
        # 🔎 Retrieve top 3 documents
        retrieved_docs = []

        if vector_db:
            docs_with_scores = vector_db.similarity_search_with_score(query, k=3)

            print("\n--- Similarity Scores ---")
            for doc, score in docs_with_scores:
                print("Score:", score)

            # Keep reasonably relevant matches
            retrieved_docs = [
                doc for doc, score in docs_with_scores if score < 1.5
            ]

        # ============================================
        # ✅ STRICT RAG MODE (Context Injection)
        # ============================================

        if retrieved_docs:
            prompt = build_rag_prompt(query, retrieved_docs)
        else:
            # If no documents matched → safe fallback
            prompt = f"""
You are a professional assistant.

No relevant documents were found.
Inform the user politely that the system does not have sufficient document information to answer this question.

Question:
{query}
"""

        response = llm.invoke(prompt)

        return response.content
>>>>>>> e1bfd89 (Completed full project implementation)

        # THIS PRINT STATEMENT CREATES THE LOG YOU NEED
        print(f"\n--- METADATA LOG ---")
        print(f"ID: {interaction_id}")
        print(f"Sources: {sources}")
        print(f"-------------------\n")

        prompt = f"Using this context:\n{combined_context}\n\nQuestion: {query}"
        response = llm.invoke(prompt)

        return {
            "reply": response.content,
            "metadata": {
                "interaction_uuid": interaction_id,
                "timestamp": datetime.now().isoformat(),
                "sources_consulted": sources
            }
        }
    # --- YOU WERE MISSING THIS PART BELOW ---
    except Exception as e:
<<<<<<< HEAD
        print(f"❌ Error: {str(e)}")
        return {"reply": f"AI Error: {str(e)}", "metadata": {}}
=======
        print(f"❌ LLM Error: {e}")
        return "I'm having trouble connecting to the AI right now. Please try again."
>>>>>>> e1bfd89 (Completed full project implementation)
