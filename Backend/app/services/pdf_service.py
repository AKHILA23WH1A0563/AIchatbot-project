import pypdf
import os

def extract_text_from_pdfs():
    # This finds the main folder (AI_CHATBOT_BACKEND) automatically
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    folder_path = os.path.join(base_dir, "data_source")
    
    print(f"🔍 Checking for PDFs in: {folder_path}") # Check your terminal for this!
    
    combined_text = ""
    
    if not os.path.exists(folder_path):
        print(f"❌ Error: Folder NOT found at {folder_path}")
        return ""

    try:
        files = os.listdir(folder_path)
        print(f"📂 Files found: {files}") # This confirms your PDF is seen

        for filename in files:
            if filename.lower().endswith(".pdf"):
                file_path = os.path.join(folder_path, filename)
                reader = pypdf.PdfReader(file_path)
                for page in reader.pages:
                    text = page.extract_text()
                    if text:
                        combined_text += text + "\n"
    except Exception as e:
        print(f"❌ Error during PDF extraction: {e}")
                
    return combined_text