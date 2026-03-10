import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.ingestion_engine import ingest_and_store_in_chroma

if __name__ == "__main__":
    print("Starting data ingestion...")
    ingest_and_store_in_chroma()
    print("Data ingestion completed!")