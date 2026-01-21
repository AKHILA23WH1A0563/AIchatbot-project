from app.services.pdf_service import extract_text_from_pdf
from app.services.scraper_service import scrape_website
from app.db.database import save_chat


async def handle_chat(query: str, session_id: str):
    """
    Core chat logic
    """

    response = "Information not found"

    # PDF-based query
    if query.endswith(".pdf"):
        pdf_text = extract_text_from_pdf(query)
        if pdf_text:
            response = pdf_text[:300]

    # URL-based query
    elif query.startswith("http"):
        scraped_text = scrape_website(query)
        if scraped_text:
            response = scraped_text

    # Dummy fallback
    else:
        response = f"Travel info for: {query}"

    await save_chat(query, response, session_id)

    return {"response": response}
