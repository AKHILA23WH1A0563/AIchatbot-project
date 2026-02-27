import os
import uuid
from datetime import datetime
from pypdf import PdfReader

# This is the name your error says is missing!
def ingest_all_sources():
    data_source_path = "data_source" # Ensure this folder exists
    all_chunks = []

    if not os.path.exists(data_source_path):
        print(f"❌ Folder {data_source_path} not found!")
        return []

    for filename in os.listdir(data_source_path):
        if filename.endswith(".pdf"):
            path = os.path.join(data_source_path, filename)
            try:
                reader = PdfReader(path)
                text = ""
                for page in reader.pages:
                    text += page.extract_text()

                # --- METADATA MANAGEMENT LOGIC ---
                # We create a dictionary for the chunk with Unique ID and Timestamp
                chunk = {
                    "chunk_id": str(uuid.uuid4()),            # Requirement: Unique ID
                    "content": text,
                    "metadata": {
                        "source": filename,                   # Requirement: Traceability
                        "ingestion_date": datetime.now().isoformat(), # Requirement: Timestamp
                        "file_type": "pdf"
                    }
                }
                all_chunks.append(chunk)
                print(f"✅ Loaded: {filename}")

            except Exception as e:
                print(f"❌ Error loading {filename}: {e}")

    return all_chunks