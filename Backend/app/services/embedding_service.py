from sentence_transformers import SentenceTransformer
import logging

# Load model once (very important)
# Lightweight and good for demo
model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embedding(text: str) -> list:
    """
    Generate embedding vector for given text.

    Args:
        text (str): Input text

    Returns:
        list: Embedding vector as list of floats
    """
    try:
        if not text or not text.strip():
            logging.warning("Empty text received for embedding.")
            return []

        # Clean text
        cleaned_text = text.strip()

        # Generate embedding
        embedding = model.encode(cleaned_text)

        return embedding.tolist()

    except Exception as e:
        logging.error(f"Embedding generation failed: {str(e)}")
        return []