from pypdf import PdfReader
import os

def load_pdfs(folder_path):
    documents = []

    for file in os.listdir(folder_path):
        if file.endswith(".pdf"):
            file_path = os.path.join(folder_path, file)
            reader = PdfReader(file_path)
            text = ""

            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"

            documents.append({
                "text": text,
                "source": file
            })

            print(f"✅ Loaded: {file}")

    return documents