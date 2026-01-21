from fastapi import APIRouter
import os

router = APIRouter()

PDF_DIR = "app/data/pdfs"

@router.get("/pdfs")
def list_pdfs():
    """
    List all available PDF files from data/pdfs directory
    """
    if not os.path.exists(PDF_DIR):
        return {
            "message": "PDF directory not found",
            "pdfs": []
        }

    pdf_files = [
        file for file in os.listdir(PDF_DIR)
        if file.endswith(".pdf")
    ]

    return {
        "count": len(pdf_files),
        "pdfs": pdf_files
    }
