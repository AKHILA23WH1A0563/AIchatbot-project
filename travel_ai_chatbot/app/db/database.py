import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = "travel_ai_chatbot"

client: AsyncIOMotorClient | None = None
db = None

async def connect_to_mongo():
    global client, db
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    print("✅ MongoDB connected")

async def close_mongo_connection():
    if client:
        client.close()
        print("❌ MongoDB connection closed")

async def save_chat(query: str, response: str, session_id: str = "default"):
    if db:
        await db.chats.insert_one({
            "session_id": session_id,
            "query": query,
            "response": response
        })
