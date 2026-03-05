
import re
import unicodedata


def clean_text(text: str) -> str:
    if not text:
        return ""

    # Normalize unicode (fix weird characters)
    text = unicodedata.normalize("NFKC", text)

    # Convert Windows/Mac line endings to \n
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Remove null bytes and zero-width chars
    text = text.replace("\x00", "")
    text = re.sub(r"[\u200B-\u200D\uFEFF]", "", text)

    # Remove repeated underscores / hyphens / equals lines (common in PDFs)
    text = re.sub(r"^[\s_\-=]{4,}$", "", text, flags=re.MULTILINE)

    # Remove "Page X" or "Page X of Y" lines
    text = re.sub(r"^\s*page\s+\d+(\s+of\s+\d+)?\s*$", "", text, flags=re.IGNORECASE | re.MULTILINE)

    # Remove standalone page numbers (only digits)
    text = re.sub(r"^\s*\d{1,4}\s*$", "", text, flags=re.MULTILINE)

    # Collapse excessive spaces/tabs
    text = re.sub(r"[ \t]+", " ", text)

    # Trim spaces around newlines
    text = re.sub(r" *\n *", "\n", text)

    # Remove too many blank lines (keep max 1 empty line)
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Remove lines that are extremely short noise (e.g., single punctuation)
    lines = []
    for line in text.split("\n"):
        s = line.strip()
        if not s:
            lines.append("")
            continue
        if len(s) <= 1 and re.fullmatch(r"[\W_]", s):
            continue
        lines.append(s)

    cleaned = "\n".join(lines).strip()
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)

    return cleaned
