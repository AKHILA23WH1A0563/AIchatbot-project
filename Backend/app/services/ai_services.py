import os
import uuid
from datetime import datetime
from dotenv import load_dotenv
from pypdf import PdfReader

from langchain_groq import ChatGroq
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# ============================================
# 🔹 Load Environment Variables
# ============================================

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

knowledge_base = []
vector_db = None
llm = None


# ============================================
# 🔹 STEP 1: Load PDFs (User Story 3 - Metadata)
# ============================================

def load_pdfs(folder_path="data_source"):
    documents = []

    if not os.path.exists(folder_path):
        print(f"❌ Folder {folder_path} not found!")
        return documents

    for file in os.listdir(folder_path):
        if file.endswith(".pdf"):
            try:
                reader = PdfReader(os.path.join(folder_path, file))
                text = " ".join(
                    [page.extract_text() for page in reader.pages if page.extract_text()]
                )

                documents.append({
                    "doc_id": str(uuid.uuid4()),
                    "text": text,
                    "source": file,
                    "ingestion_date": datetime.now().isoformat()
                })

                print(f"✅ Loaded: {file}")

            except Exception as e:
                print(f"⚠️ Error loading {file}: {e}")

    return documents


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
            chunk_text = " ".join(words[start:end])

            all_chunks.append({
                "chunk_id": f"{source}_chunk_{chunk_number}",
                "text": chunk_text,
                "source": source,
                "doc_id": doc["doc_id"]
            })

            start += (chunk_size - overlap)
            chunk_number += 1

    print(f"📦 Total chunks created: {len(all_chunks)}")
    return all_chunks


# ============================================
# 🔹 STEP 3: Initialize RAG System
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
                "source": chunk["source"],
                "doc_id": chunk["doc_id"]
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
        print("⚠ No documents found. Running AI-only mode.")
        vector_db = None

    llm = ChatGroq(
        groq_api_key=GROQ_API_KEY,
        temperature=0.2,
        model_name="llama-3.1-8b-instant"
    )

    print("✅ RAG system initialized successfully")


# ============================================
# 🔹 STEP 4: Structured RAG Prompt (Strict Mode)
# ============================================

def build_rag_prompt(question, retrieved_docs):
    context_text = "\n\n".join(
        [
            f"[Source: {doc.metadata.get('source')}]\n{doc.page_content}"
            for doc in retrieved_docs
        ]
    )

    prompt = f"""
You are a professional AI assistant.

IMPORTANT RULES:
- Answer ONLY using the provided document context.
- Do NOT use outside knowledge.
- If answer is not found in context, say:
  "I don't have enough information in the provided documents."

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
# 🔹 STEP 5: Get AI Response (Final Combined Version)
# ============================================

def get_ai_response(query: str):
    global vector_db, llm

    if not llm:
        initialize_rag()

    interaction_id = str(uuid.uuid4())
    timestamp = datetime.now().isoformat()

    retrieved_docs = []
    sources = []

    try:
        # 🔎 Retrieve top 3 similar chunks
        if vector_db:
            docs_with_scores = vector_db.similarity_search_with_score(query, k=3)

            print("\n--- Similarity Scores ---")
            for doc, score in docs_with_scores:
                print(f"Score: {score}")
            
            retrieved_docs = [
                doc for doc, score in docs_with_scores if score < 1.5
            ]

            sources = list(set([doc.metadata.get("source") for doc in retrieved_docs]))

        # Strict RAG Mode
        if retrieved_docs:
            prompt = build_rag_prompt(query, retrieved_docs)
            response = llm.invoke(prompt)
            reply_text = response.content
        else:
            reply_text = "I don't have enough information in the provided documents."

        # 🧾 METADATA LOG (Your feature retained)
        print("\n--- METADATA LOG ---")
        print(f"Interaction ID: {interaction_id}")
        print(f"Timestamp: {timestamp}")
        print(f"Sources Consulted: {sources}")
        print("--------------------\n")

        return {
            "reply": reply_text,
            "metadata": {
                "interaction_uuid": interaction_id,
                "timestamp": timestamp,
                "sources_consulted": sources
            }
        }

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return {
            "reply": f"AI Error: {str(e)}",
            "metadata": {}
        }