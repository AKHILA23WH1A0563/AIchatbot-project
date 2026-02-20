# app/services/ingestion_engine.py

from app.utils.pdf_extractor import extract_text_from_pdfs
from app.utils.url_extractor import extract_from_all_urls
from app.utils.cleaner import clean_text


def ingest_all_sources() -> str:
    pdf_text = extract_text_from_pdfs()
    url_text = extract_from_all_urls()

    combined = (pdf_text or "") + "\n\n" + (url_text or "")
    return clean_text(combined)
