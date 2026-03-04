<<<<<<< HEAD
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Import the AI service function
from app.services.ai_services import get_ai_response

app = FastAPI(title="AI Travel Chatbot") 
=======
# ============================================================
# 🔹 Imports
# ============================================================

import os
import re
import random
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, field_validator
from passlib.context import CryptContext
import uvicorn

# ============================================================
# 🔹 Password Hashing Setup
# ============================================================

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    password = password[:72]   # bcrypt safety
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    plain = plain[:72]
    return pwd_context.verify(plain, hashed)

# ============================================================
# 🔹 Load Environment Variables
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, ".env")
load_dotenv(dotenv_path=ENV_PATH)

# ============================================================
# 🔹 Local Imports
# ============================================================

from app.api.v1.router import api_router
from app.api.v1.routes.ask_routes import router as ask_router
from app.db.database import connect_to_mongo, close_mongo_connection
from app.services.ai_services import get_ai_response, initialize_rag

# ============================================================
# 🔹 Lifespan Events
# ============================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("✅ Application starting...")
    await connect_to_mongo()
    initialize_rag()
    yield
    print("🛑 Application shutting down...")
    await close_mongo_connection()

# ============================================================
# 🔹 FastAPI App Initialization
# ============================================================

app = FastAPI(
    title="AI Chatbot Unified Backend",
    version="1.0.0",
    lifespan=lifespan
)

# ============================================================
# 🔹 CORS Middleware
# ============================================================
>>>>>>> e1bfd89 (Completed full project implementation)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

<<<<<<< HEAD
class ChatRequest(BaseModel):
    message: str

@app.get("/")
def read_root():
    return {"status": "✅ Backend is Running"}
=======
# ============================================================
# 🔹 Request Models with Validation
# ============================================================

class RegisterData(BaseModel):
    full_name: str
    email: EmailStr   # ✅ Accepts ANY valid email
    mobile: str
    password: str

    # ✅ 10 digit mobile validation
    @field_validator("mobile")
    def validate_mobile(cls, value):
        if not re.match(r"^\d{10}$", value):
            raise ValueError("Mobile number must be exactly 10 digits")
        return value

    # ✅ Strong password validation
    @field_validator("password")
    def validate_password(cls, value):
        pattern = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&]).{6,50}$'
        if not re.match(pattern, value):
            raise ValueError(
                "Password must be 6-50 characters and include letter, number & special character"
            )
        return value


class LoginData(BaseModel):
    email: EmailStr
    password: str


class OTPVerifyData(BaseModel):
    email: EmailStr
    otp: str


class ChatRequest(BaseModel):
    message: str

# ============================================================
# 🔹 Temporary Storage (Replace with Mongo Later)
# ============================================================

users_db = []
otp_storage = {}

# ============================================================
# 🔹 Include Routers
# ============================================================

app.include_router(api_router, prefix="/api/v1")
app.include_router(ask_router, prefix="/api")

# ============================================================
# 🔹 Authentication Routes
# ============================================================

# ------------------------------------------------------------
# 🔹 Register → Generates OTP
# ------------------------------------------------------------
@app.post("/register")
async def register(data: RegisterData):

    existing_user = next((u for u in users_db if u["email"] == data.email), None)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    otp = str(random.randint(100000, 999999))

    otp_storage[data.email] = {
        "user_data": data.model_dump(),
        "otp": otp
    }

    print(f"📩 OTP for {data.email}: {otp}")

    return {"message": "OTP sent (check backend console for now)"}


# ------------------------------------------------------------
# 🔹 Verify OTP → Final Registration
# ------------------------------------------------------------
@app.post("/verify-otp")
async def verify_otp(data: OTPVerifyData):

    record = otp_storage.get(data.email)

    if not record:
        raise HTTPException(status_code=400, detail="No OTP request found")

    if record["otp"] != data.otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    user_data = record["user_data"]

    user_data["password"] = hash_password(user_data["password"])

    users_db.append(user_data)

    del otp_storage[data.email]

    print(f"✅ Registered user: {data.email}")

    return {"message": "User registered successfully"}


# ------------------------------------------------------------
# 🔹 Login
# ------------------------------------------------------------
@app.post("/login")
async def login(data: LoginData):

    user = next((u for u in users_db if u["email"] == data.email), None)

    if user and verify_password(data.password, user["password"]):
        print(f"✅ Login successful: {data.email}")
        return {
            "message": "Login successful",
            "full_name": user["full_name"]
        }

    raise HTTPException(status_code=401, detail="Invalid email or password")


# ============================================================
# 🔹 Chat Route (RAG Powered)
# ============================================================
>>>>>>> e1bfd89 (Completed full project implementation)

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
<<<<<<< HEAD
        full_response = get_ai_response(request.message)
        return full_response 
    except Exception as e:
        return {"reply": f"Error: {str(e)}", "metadata": {}}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
=======
        answer = get_ai_response(request.message)
        return {"reply": answer}
    except Exception as e:
        print(f"❌ AI Error: {e}")
        raise HTTPException(status_code=500, detail="AI service error")


# ============================================================
# 🔹 Health Check
# ============================================================

@app.get("/")
async def root():
    return {"message": "Backend running 🚀"}


# ============================================================
# 🔹 Run Server
# ============================================================

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
>>>>>>> e1bfd89 (Completed full project implementation)
