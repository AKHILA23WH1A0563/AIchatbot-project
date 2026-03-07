# ============================================================
# main.py
# ============================================================

import os
import re
import random
from contextlib import asynccontextmanager
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, field_validator
from passlib.context import CryptContext
import uvicorn

# ============================================================
# Load Environment Variables
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, ".env")
load_dotenv(dotenv_path=ENV_PATH)

# ============================================================
# Local Imports
# ============================================================

from app.services.ai_services import get_ai_response, initialize_rag
from app.api.v1.router import api_router
from app.db.database import connect_to_mongo, close_mongo_connection

# ============================================================
# Password Hashing
# ============================================================

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password[:72])

def verify_password(plain, hashed):
    return pwd_context.verify(plain[:72], hashed)

# ============================================================
# Lifespan Events (Mongo + RAG Init)
# ============================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Application starting...")
    await connect_to_mongo()
    initialize_rag()
    yield
    print("🛑 Application shutting down...")
    await close_mongo_connection()

# ============================================================
# FastAPI App
# ============================================================

app = FastAPI(
    title="AI Chatbot Unified Backend",
    version="1.0.0",
    lifespan=lifespan
)

# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# Include Routers
# ============================================================

app.include_router(api_router, prefix="/api/v1")

# ============================================================
# Request Models
# ============================================================

class RegisterData(BaseModel):
    full_name: str
    email: EmailStr
    mobile_number: Optional[str] = ""  # optional now
    password: str
    confirm_password: str

    @field_validator("mobile_number")
    def validate_mobile_number(cls, value):
        if value:  # only validate if provided
            if not re.match(r"^\d{10}$", value):
                raise ValueError("Mobile must be exactly 10 digits")
        return value

    @field_validator("password")
    def validate_password(cls, value):
        pattern = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&]).{6,50}$'
        if not re.match(pattern, value):
            raise ValueError(
                "Password must be 6-50 chars & include letter, number, special char"
            )
        return value

class LoginData(BaseModel):
    identifier: str  # email or mobile_number
    password: str

class OTPVerifyData(BaseModel):
    email: EmailStr
    otp: str

class ChatRequest(BaseModel):
    message: str

# ============================================================
# Temporary Storage
# ============================================================

users_db = []
otp_storage = {}

# ============================================================
# Authentication Routes
# ============================================================

@app.post("/register")
async def register(data: RegisterData):
    existing = next((u for u in users_db if u["email"] == data.email), None)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    otp = str(random.randint(100000, 999999))
    otp_storage[data.email] = {
        "user_data": data.model_dump(),
        "otp": otp
    }

    print(f"📩 OTP for {data.email}: {otp}")
    return {"message": "OTP generated (check backend console)"}

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

@app.post("/login")
async def login(data: LoginData):
    user = next(
        (u for u in users_db if u["email"] == data.identifier or u["mobile_number"] == data.identifier),
        None
    )

    if user and verify_password(data.password, user["password"]):
        print(f"✅ Login successful: {data.identifier}")
        return {
            "message": "Login successful",
            "user": {"full_name": user["full_name"]}
        }

    raise HTTPException(status_code=401, detail="Invalid credentials")

# ============================================================
# Chat Route
# ============================================================

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        response = get_ai_response(request.message)
        return response
    except Exception as e:
        print(f"❌ AI Error: {e}")
        raise HTTPException(status_code=500, detail="AI service error")

# ============================================================
# Health Check
# ============================================================

@app.get("/")
async def root():
    return {"message": "Backend running 🚀"}

# ============================================================
# Run Server
# ============================================================

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)