import os
from PyPDF2 import PdfReader

PDF_DIR = "data/pdfs"


def extract_text_from_pdf(pdf_name: str) -> str:
    """
    Dummy PDF text extractor
    Reads PDF from data/pdfs directory
    """

    pdf_path = os.path.join(PDF_DIR, pdf_name)

    if not os.path.exists(pdf_path):
        return ""

    text = ""

    try:
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            text += page.extract_text() or ""
    except Exception:
        return ""

    return text.strip()
