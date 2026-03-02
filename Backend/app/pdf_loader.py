from pypdf import PdfReader
import os

def load_pdfs(folder_path):
    documents = []

    # Ensure the folder exists to avoid crashes
    if not os.path.exists(folder_path):
        print(f"❌ Error: Folder {folder_path} not found.")
        return documents

    for file in os.listdir(folder_path):
        if file.endswith(".pdf"):
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
                    "file_type": "pdf"  # Added this to match your chunker's metadata
                })

                print(f"✅ Loaded: {file}")
            except Exception as e:
                print(f"⚠️ Could not read {file}: {str(e)}")

    return documents