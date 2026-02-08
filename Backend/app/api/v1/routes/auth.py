from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from app.db.database import get_db
from app.utils.helpers import hash_password, verify_password
from app.utils.jwt_helper import create_access_token

router = APIRouter()

class RegisterRequest(BaseModel):
    fullName: str
    email: EmailStr
    mobileNumber: str
    password: str
    confirmPassword: str

class LoginRequest(BaseModel):
    identifier: str
    password: str


@router.post("/register")
async def register(payload: RegisterRequest):
    db = get_db()
    if db is None:
        raise HTTPException(status_code=500, detail="DB not initialized")

    if payload.password != payload.confirmPassword:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    existing = await db.users.find_one({"email": payload.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")

    user_data = {
        "fullName": payload.fullName,
        "email": payload.email,
        "mobileNumber": payload.mobileNumber,
        "password": hash_password(payload.password),
    }

    await db.users.insert_one(user_data)
    return {"message": "User registered successfully"}


@router.post("/Login")
async def login(payload: LoginRequest):
    db = get_db()
    if db is None:
        raise HTTPException(status_code=500, detail="DB not initialized")

    user = await db.users.find_one({
        "$or": [
            {"email": payload.identifier},
            {"mobileNumber": payload.identifier}
        ]
    })

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(payload.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # 👉 Generate JWT Token
    token = create_access_token({
        "email": user["email"],
        "fullName": user["fullName"]
    })

    return {
        "message": "Login successful",
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": str(user["_id"]),
            "fullName": user["fullName"],
            "email": user["email"],
            "mobileNumber": user["mobileNumber"],
        }
    }
