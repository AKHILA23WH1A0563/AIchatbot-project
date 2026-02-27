from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Import the AI service function
from app.services.ai_services import get_ai_response

app = FastAPI(title="AI Travel Chatbot") 

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def read_root():
    return {"status": "✅ Backend is Running"}

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        full_response = get_ai_response(request.message)
        return full_response 
    except Exception as e:
        return {"reply": f"Error: {str(e)}", "metadata": {}}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)