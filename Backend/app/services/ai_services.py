import os
import uuid
import sys
from datetime import datetime
from pypdf import PdfReader
from dotenv import load_dotenv
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
            try:
                reader = PdfReader(os.path.join(folder_path, file))
                text = " ".join([p.extract_text() for p in reader.pages if p.extract_text()])
                
                # Metadata Ingestion for Traceability
                documents.append({
                    "chunk_id": str(uuid.uuid4()),
                    "text": text,
                    "source": file,
                    "ingestion_date": datetime.now().isoformat()
                })
                print(f"✅ Loaded: {file}")
            except Exception as e: 
                print(f"⚠️ Error loading {file}: {e}")
                continue
    return documents

def get_ai_response(query: str):
    global knowledge_base, llm
    if not knowledge_base:
        knowledge_base = load_pdfs("data_source")
    if not llm:
        llm = ChatGroq(groq_api_key=GROQ_API_KEY, model_name="llama-3.1-8b-instant")

    # Basic keyword search logic
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

    try:
        interaction_id = str(uuid.uuid4())
        sources = list(set(relevant_sources))

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
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return {"reply": f"AI Error: {str(e)}", "metadata": {}}