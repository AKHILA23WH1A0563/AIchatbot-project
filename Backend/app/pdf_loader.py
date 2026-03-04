from pypdf import PdfReader
import os


def load_pdfs(folder_path):
    """
    Loads all PDF files from a folder and returns
    a list of document dictionaries.

    Output format:
    [
        {
            "text": "...",
            "source": "file.pdf",
            "file_type": "pdf"
        }
    ]
    """

    documents = []

    # ✅ Ensure folder exists
    if not os.path.exists(folder_path):
        print(f"❌ Error: Folder {folder_path} not found.")
        return documents

    for file in os.listdir(folder_path):

        # ✅ Case insensitive check
        if file.lower().endswith(".pdf"):

            file_path = os.path.join(folder_path, file)

            try:
                reader = PdfReader(file_path)
                text = ""

                for page in reader.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + "\n"

                documents.append({
                    "text": text,
                    "source": file,
                    "file_type": "pdf"
                })

                print(f"✅ Loaded: {file}")

            except Exception as e:
                print(f"⚠️ Could not read {file}: {str(e)}")

    return documents