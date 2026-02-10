from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


# Existing local imports
from app.api.v1.router import api_router
from app.db.database import connect_to_mongo, close_mongo_connection
from app.services.ai_services import get_ai_response

# 1. Lifespan Context Manager (Replaces Startup/Shutdown Events)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # This code runs before the application starts receiving requests
    print("✅ Application is starting up...")
    await connect_to_mongo()
    
    yield  # This is where the application lives and handles requests
    
    # This code runs when the application is shutting down
    print("🛑 Application is shutting down...")
    await close_mongo_connection()

# 2. FastAPI Instance with Lifespan
app = FastAPI(title="AI Chatbot Unified Backend", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Data Models
class RegisterData(BaseModel):
    full_name: str
    email: str
    mobile: str = None
    password: str

class LoginData(BaseModel): 
    email: str
    password: str

class ChatRequest(BaseModel):
    message: str

# 4. Temporary database
users_db = []

# 5. Existing Routers
app.include_router(api_router, prefix="/api/v1")

# 6. Integration Routes
@app.post("/register")
async def register(data: RegisterData):
    users_db.append(data.dict()) 
    print(f"✅ Received registration for: {data.email}")
    return {"message": "User registered successfully"}

@app.post("/login")
async def login(data: LoginData):
    user = next((u for u in users_db if u["email"] == data.email), None)
    if user and user["password"] == data.password:
        print(f"✅ Login successful for: {data.email}")
        return {"message": "Login successful", "full_name": user["full_name"]}
    raise HTTPException(status_code=401, detail="Invalid email or password")

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        # Calls the actual AI logic which reads your PDFs
        answer = get_ai_response(request.message)
        return {"reply": answer}
    except Exception as e:
        print(f"❌ AI Error: {e}")
        return {"reply": "I'm having trouble reading my travel files right now."}