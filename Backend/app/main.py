import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# ============================================
# 🔹 Load Environment Variables
# ============================================

#load_dotenv()
import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, "..", ".env")

load_dotenv(dotenv_path=ENV_PATH)
#print("OPENAI KEY:", os.getenv("OPENAI_API_KEY"))  # ✅ For testing only (remove later)

# ============================================
# 🔹 Local Imports
# ============================================

from app.api.v1.router import api_router
from app.api.v1.routes.ask_routes import router as ask_router
from app.db.database import connect_to_mongo, close_mongo_connection
from app.services.ai_services import get_ai_response, initialize_rag


# ============================================
# 🔹 Lifespan (Startup & Shutdown)
# ============================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("✅ Application is starting up...")

    # Connect MongoDB
    await connect_to_mongo()

    # Initialize RAG system
    initialize_rag()

    yield

    print("🛑 Application is shutting down...")
    await close_mongo_connection()


# ============================================
# 🔹 FastAPI App
# ============================================

app = FastAPI(
    title="AI Chatbot Unified Backend",
    lifespan=lifespan
)


# ============================================
# 🔹 Middleware
# ============================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================
# 🔹 Request Models
# ============================================

class RegisterData(BaseModel):
    full_name: str
    email: str
    mobile: str | None = None
    password: str


class LoginData(BaseModel):
    email: str
    password: str


class ChatRequest(BaseModel):
    message: str


# ============================================
# 🔹 Temporary In-Memory User DB
# ============================================

users_db = []


# ============================================
# 🔹 Routers
# ============================================

app.include_router(api_router, prefix="/api/v1")
app.include_router(ask_router, prefix="/api")


# ============================================
# 🔹 Auth Routes
# ============================================

@app.post("/register")
async def register(data: RegisterData):
    users_db.append(data.model_dump())
    print(f"✅ Received registration for: {data.email}")
    return {"message": "User registered successfully"}


@app.post("/login")
async def login(data: LoginData):
    user = next((u for u in users_db if u["email"] == data.email), None)

    if user and user["password"] == data.password:
        print(f"✅ Login successful for: {data.email}")
        return {
            "message": "Login successful",
            "full_name": user["full_name"]
        }

    raise HTTPException(status_code=401, detail="Invalid email or password")


# ============================================
# 🔹 Chat Route (RAG Powered)
# ============================================

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        answer = get_ai_response(request.message)
        return {"reply": answer}

    except Exception as e:
        print(f"❌ AI Error: {e}")
        return {"reply": "I'm having trouble answering right now."}


# ============================================
# 🔹 Health Check
# ============================================

@app.get("/")
def root():
    return {"message": "Backend running 🚀"}