from groq import Groq
from app.core.config import settings
from app.services.pdf_service import extract_text_from_pdfs

client = Groq(api_key=settings.GROQ_API_KEY)

def get_ai_response(user_query: str) -> str:
    try:
        context = extract_text_from_pdfs()
        if not context:
            return "No travel documents found in data_source."

        filtered_context = context[:6000]

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "Answer only from context. If not found say: Not found in the document."},
                {"role": "user", "content": f"Context: {filtered_context}\n\nQuestion: {user_query}"}
            ],
            temperature=0.3,
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"AI Service Error: {str(e)}"
