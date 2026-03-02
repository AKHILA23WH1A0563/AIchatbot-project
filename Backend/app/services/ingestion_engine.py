import os
import uuid
from datetime import datetime
from typing import List, Dict, Any

from pypdf import PdfReader
from app.services.vector_store import upsert_chunks 

DATA_SOURCE_PATH = "data_source"

def ingest_all_sources() -> List[Dict[str, Any]]:
    data_source_path = DATA_SOURCE_PATH
    all_chunks: List[Dict[str, Any]] = []

    if not os.path.exists(data_source_path):
        print(f"❌ Folder {data_source_path} not found!")
        return []

    for filename in os.listdir(data_source_path):
        if filename.lower().endswith(".pdf"):
            path = os.path.join(data_source_path, filename)
            try:
                reader = PdfReader(path)
                text = ""
                for page in reader.pages:
                    page_text = page.extract_text() or ""
                    text += page_text

                chunk = {
                    "chunk_id": str(uuid.uuid4()),   
                    "content": text,                 
                    "metadata": {
                        "source": filename,
                        "ingestion_date": datetime.now().isoformat(),
                        "file_type": "pdf",
                    },
                }
                all_chunks.append(chunk)
                print(f"✅ Loaded: {filename}")

            except Exception as e:
                print(f"❌ Error loading {filename}: {e}")

    return all_chunks

def ingest_and_store_in_chroma():
    """
    1) Read all PDFs from data_source
    2) Build chunk dicts (id, content, metadata)
    3) Pass to upsert_chunks for embeddings and ChromaDB storage
    """
    chunks = ingest_all_sources()
    if not chunks:
        print("⚠️ No chunks generated, nothing to store in Chroma.")
        return

    print(f"🔄 Ingesting {len(chunks)} PDF chunks into ChromaDB...")
    upsert_chunks(chunks)   
    print("✅ All PDF embeddings stored in ChromaDB.")

if __name__ == "__main__":
    ingest_and_store_in_chroma()