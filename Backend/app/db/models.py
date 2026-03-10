from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from bson import ObjectId


# ===== CHUNK MODEL =====
class ChunkMetadata(BaseModel):
    source: str  # filename or URL
    source_type: str  # "pdf", "website", "text"
    ingestion_date: datetime
    file_type: str  # "pdf", "html", etc.
    url: Optional[str] = None  # for websites


class Chunk(BaseModel):
    chunk_id: str
    content: str
    metadata: ChunkMetadata
    
    class Config:
        json_schema_extra = {
            "example": {
                "chunk_id": "file.pdf_chunk_001",
                "content": "This is the chunk content...",
                "metadata": {
                    "source": "file.pdf",
                    "source_type": "pdf",
                    "ingestion_date": "2026-02-27T10:00:00",
                    "file_type": "pdf",
                    "url": None
                }
            }
        }


# ===== DOCUMENT MODEL (for tracking source documents) =====
class Document(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: str(ObjectId()))
    source_name: str  # file.pdf or website URL
    source_type: str  # "pdf", "website"
    total_chunks: int
    ingestion_date: datetime
    status: str = "completed"  # completed, pending, failed
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "507f1f77bcf86cd799439011",
                "source_name": "travel_guide.pdf",
                "source_type": "pdf",
                "total_chunks": 15,
                "ingestion_date": "2026-02-27T10:00:00",
                "status": "completed"
            }
        }


# ===== INGESTION REPORT =====
class IngestionReport(BaseModel):
    total_chunks_created: int
    documents_processed: list[str]
    timestamp: datetime
    status: str


# ===== CHUNK RETRIEVAL FILTER =====
class ChunkFilter(BaseModel):
    source_type: Optional[str] = None  # Filter by "pdf" or "website"
    source_name: Optional[str] = None  # Filter by specific file
    limit: int = 10
    skip: int = 0
