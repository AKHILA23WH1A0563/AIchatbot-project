from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Import the AI service and routers
from app.services.ai_services import get_ai_response
from app.api.v1.router import api_router
from app.db.database import connect_to_mongo, close_mongo_connection

app = FastAPI(title="AI Travel Chatbot") 

# CORS Configuration for Frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the modular API routers
app.include_router(api_router)

# Database lifecycle management
@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()

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