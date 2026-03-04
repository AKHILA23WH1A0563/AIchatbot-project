# ============================================================
# 🔹 Text Chunker Utility
# Responsible for splitting large text into overlapping chunks
# ============================================================

def chunk_text(text, chunk_size=500, overlap=100):
    """
    Splits text into chunks with overlap.

    Parameters:
    - text (str): Full cleaned text
    - chunk_size (int): Number of words per chunk
    - overlap (int): Number of overlapping words

    Returns:
    - List of chunk strings
    """

    words = text.split()
    chunks = []

    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk_words = words[start:end]

        chunk = " ".join(chunk_words)
        chunks.append(chunk)

        start += (chunk_size - overlap)

    return chunks