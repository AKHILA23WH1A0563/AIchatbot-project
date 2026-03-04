import os
import uuid
from datetime import datetime
from typing import List, Dict, Any

from pypdf import PdfReader
from app.services.vector_store import upsert_chunks


# ============================================================
# 🔹 Data Source Path
# ============================================================

DATA_SOURCE_PATH = "data_source"


# ============================================================
# 🔹 PDF Ingestion
# ============================================================

def ingest_all_sources() -> List[Dict[str, Any]]:
    """
    Read all PDFs from the data_source folder and
    convert them into chunk objects with metadata.
    """

    all_chunks: List[Dict[str, Any]] = []

    if not os.path.exists(DATA_SOURCE_PATH):
        print(f"❌ Folder {DATA_SOURCE_PATH} not found!")
        return []

    for filename in os.listdir(DATA_SOURCE_PATH):

        if filename.lower().endswith(".pdf"):

            file_path = os.path.join(DATA_SOURCE_PATH, filename)

            try:
                reader = PdfReader(file_path)

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


# ============================================================
# 🔹 Ingest + Store in Vector DB
# ============================================================

def ingest_and_store_in_chroma():
    """
    1. Read PDFs from data_source
    2. Generate chunk metadata
    3. Store embeddings in ChromaDB
    """

    chunks = ingest_all_sources()

    if not chunks:
        print("⚠️ No chunks generated.")
        return

    print(f"🔄 Ingesting {len(chunks)} chunks into ChromaDB...")

    upsert_chunks(chunks)

    print("✅ All PDF embeddings stored successfully.")


# ============================================================
# 🔹 Run Directly
# ============================================================

if __name__ == "__main__":
    ingest_and_store_in_chroma()