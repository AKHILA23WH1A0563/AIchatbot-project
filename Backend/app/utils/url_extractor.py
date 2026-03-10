import requests
from bs4 import BeautifulSoup

# -------------------------
# TRAVEL WEBSITE URLS
# -------------------------
TRAVEL_URLS = [
    "https://www.holidify.com/places/goa",
    "https://www.holidify.com/state/kerala",
    "https://www.holidify.com/places/manali",
    "https://www.holidify.com/places/ladakh",
    "https://www.incredibleindia.gov.in/en/destinations/goa.html",
]


# -------------------------
# EXTRACT TEXT FROM ONE URL
# -------------------------
def extract_text_from_url(url):
    """
    Extracts readable text from a website by removing ads, navigation,
    scripts, styles, and unnecessary HTML tags.
    """

    print(f"🌐 Extracting content from: {url}")

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Remove script, CSS, header/footer/navigation
        for tag in soup(["script", "style", "header", "footer", "nav", "aside"]):
            tag.decompose()

        # Try to find main content section
        main_content = None
        for id_name in ["main", "content", "article", "post", "page"]:
            main_content = soup.find(id=id_name)
            if main_content:
                break

        if not main_content:
            # fallback → use all content
            main_content = soup

        # extract text safely
        text = main_content.get_text(separator="\n", strip=True)

        # clean empty lines
        cleaned = [line.strip() for line in text.split("\n") if line.strip()]
        final_text = "\n".join(cleaned)

        return final_text

    except Exception as e:
        print(f"❌ Error while extracting from {url}: {e}")
        return ""


# -------------------------
# EXTRACT FROM ALL TRAVEL URLS
# -------------------------
def extract_from_all_urls():
    final_text = ""

    for url in TRAVEL_URLS:
        final_text += extract_text_from_url(url)
        final_text += "\n\n"

    return final_text
