import os
from PyPDF2 import PdfReader
from dotenv import load_dotenv

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq

# ============================================
# 🔹 Load Environment Variables
# ============================================

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("❌ GROQ_API_KEY not found in .env file")

# ============================================
# 🔹 GLOBAL VARIABLES
# ============================================

vector_db = None
llm = None

# ============================================
# 🔹 STEP 1: Load PDFs
# ============================================

def load_pdfs(folder_path="data_source"):
    documents = []

    if not os.path.exists(folder_path):
        print("❌ data_source folder not found!")
        return documents

    for file in os.listdir(folder_path):
        if file.endswith(".pdf"):
            file_path = os.path.join(folder_path, file)
            try:
                reader = PdfReader(file_path)
                text = ""

                for page in reader.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + "\n"

                documents.append({
                    "text": text,
                    "source": file
                })

                print(f"✅ Loaded: {file}")

            except Exception as e:
                print(f"❌ Error reading {file}: {e}")

    print(f"📄 Total PDFs loaded: {len(documents)}")
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

    if not chunks:
        print("⚠ No chunks found! Make sure PDFs are in the 'data_source' folder.")
        return

    texts = [chunk["text"] for chunk in chunks]
    metadatas = [
        {"chunk_id": chunk["chunk_id"], "source": chunk["source"]}
        for chunk in chunks
    ]

    # ✅ Local embeddings (No API cost)
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    print("⏳ Building vector database (this may take a moment)...")

    vector_db = FAISS.from_texts(
        texts=texts,
        embedding=embeddings,
        metadatas=metadatas
    )

    # ✅ FIXED: Using Llama 3.1 8B (Llama 3 8B is decommissioned)
    llm = ChatGroq(
        groq_api_key=GROQ_API_KEY,
        temperature=0,
        model_name="llama-3.1-8b-instant" 
    )

    print("✅ RAG system initialized successfully")

# ============================================
# 🔹 STEP 4: Get AI Response
# ============================================

def get_ai_response(query: str):
    global vector_db, llm

    # Auto-initialize if the system hasn't started yet
    if not vector_db or not llm:
        initialize_rag()
        if not vector_db or not llm:
            return "Error: RAG system could not be initialized."

    # Search for top 3 relevant chunks
    docs = vector_db.similarity_search(query, k=3)

    if not docs:
        return "I couldn't find relevant information in the documents."

    context = "\n\n".join([doc.page_content for doc in docs])

    prompt = f"""
You are a professional travel assistant. 

Answer the user's question using ONLY the context provided below. 
If the information is not in the context, politely explain that you don't have that specific information.

Context:
{context}

Question:
{query}

Helpful Answer:
"""

    try:
        response = llm.invoke(prompt)
        return response.content

    except Exception as e:
        print(f"❌ LLM Error: {e}")
        return "I'm having trouble connecting to the AI right now. Please try again in a moment."