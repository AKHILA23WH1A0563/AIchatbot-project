import re
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from app.db.database import get_db
from app.utils.helpers import hash_password, verify_password
from app.utils.jwt_helper import create_access_token
from app.core.config import settings

router = APIRouter()

def validate_password(password: str):
    errors = []
    if len(password) < 8:
        errors.append("at least 8 characters")
    if not re.search(r"[A-Z]", password):
        errors.append("one uppercase letter")
    if not re.search(r"[a-z]", password):
        errors.append("one lowercase letter")
    if not re.search(r"\d", password):
        errors.append("one number")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        errors.append("one special character")
    return errors

class RegisterRequest(BaseModel):
    fullName: str
    email: EmailStr
    mobileNumber: str = ""
    password: str
    confirmPassword: str

class LoginRequest(BaseModel):
    identifier: str
    password: str

class GoogleAuthRequest(BaseModel):
    credential: str  # Google ID token (JWT) from GSI callback

@router.post("/register")
async def register(payload: RegisterRequest):
    db = get_db()
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection failed. Please try again later.")

    if payload.password != payload.confirmPassword:
        raise HTTPException(status_code=400, detail="Passwords do not match.")

    errors = validate_password(payload.password)
    if errors:
        raise HTTPException(status_code=400, detail=f"Password must contain: {', '.join(errors)}.")

    existing = await db.users.find_one({"email": payload.email})
    if existing:
        raise HTTPException(status_code=400, detail="An account with this email already exists. Please log in.")

    await db.users.insert_one({
        "fullName": payload.fullName,
        "email": payload.email,
        "mobileNumber": payload.mobileNumber,
        "password": hash_password(payload.password),
    })
    return {"message": "Account created successfully!"}

@router.post("/login")
async def login(payload: LoginRequest):
    db = get_db()
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection failed. Please try again later.")

    user = await db.users.find_one({
        "$or": [
            {"email": payload.identifier},
            {"mobileNumber": payload.identifier}
        ]
    })

    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password. Please try again.")

    if not user.get("password"):
        raise HTTPException(status_code=400, detail="This account uses Google sign-in. Please use the 'Sign in with Google' button.")

    if not verify_password(payload.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password. Please try again.")

    token = create_access_token({"email": user["email"], "fullName": user["fullName"]})

    return {
        "message": "Login successful",
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": str(user["_id"]),
            "fullName": user["fullName"],
            "email": user["email"],
            "mobileNumber": user.get("mobileNumber", ""),
        }
    }

@router.post("/google")
async def google_auth(payload: GoogleAuthRequest):
    db = get_db()
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection failed. Please try again later.")

    if not settings.GOOGLE_CLIENT_ID:
        raise HTTPException(status_code=500, detail="Google authentication is not configured on the server.")

    try:
        id_info = id_token.verify_oauth2_token(
            payload.credential,
            google_requests.Request(),
            settings.GOOGLE_CLIENT_ID
        )
    except ValueError as e:
        print(f"[Google Auth Error] {e}")
        raise HTTPException(status_code=401, detail="Google sign-in failed: token verification error. Ensure your Client ID is correct and try again.")

    email = id_info.get("email")
    full_name = id_info.get("name", email)

    if not email:
        raise HTTPException(status_code=400, detail="Could not retrieve your email from Google. Please try another sign-in method.")

    user = await db.users.find_one({"email": email})
    if not user:
        result = await db.users.insert_one({
            "fullName": full_name,
            "email": email,
            "mobileNumber": "",
            "password": "",
            "google_auth": True
        })
        user = await db.users.find_one({"_id": result.inserted_id})

    token = create_access_token({"email": email, "fullName": full_name})

    return {
        "message": "Google sign-in successful",
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": str(user["_id"]),
            "fullName": full_name,
            "email": email,
            "mobileNumber": user.get("mobileNumber", ""),
        }
    }
