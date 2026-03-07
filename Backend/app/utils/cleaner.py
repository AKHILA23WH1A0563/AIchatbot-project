import re
import unicodedata


def clean_text(text: str) -> str:
    if not text:
        return ""

    # Normalize unicode characters
    text = unicodedata.normalize("NFKC", text)

    # Fix line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Remove null bytes / zero width chars
    text = text.replace("\x00", "")
    text = re.sub(r"[\u200B-\u200D\uFEFF]", "", text)

    # Remove long divider lines from PDFs
    text = re.sub(r"^[\s_\-=]{4,}$", "", text, flags=re.MULTILINE)

    # Remove page headers like "Page 3 of 10"
    text = re.sub(r"^\s*page\s+\d+(\s+of\s+\d+)?\s*$",
                  "", text, flags=re.IGNORECASE | re.MULTILINE)

    # Remove standalone page numbers
    text = re.sub(r"^\s*\d{1,4}\s*$", "", text, flags=re.MULTILINE)

    # Fix bullet points that got merged
    text = re.sub(r"\s*(\d+\.)\s*", r"\n\1 ", text)

    # Fix bullet symbols
    text = text.replace("•", "\n• ")

    # Remove extra spaces
    text = re.sub(r"[ \t]+", " ", text)

    # Clean spaces around line breaks
    text = re.sub(r" *\n *", "\n", text)

    # Remove too many blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Remove noise lines
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

    # Final cleanup
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)

    return cleaned