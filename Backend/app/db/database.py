from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

client: AsyncIOMotorClient | None = None
db = None


async def connect_to_mongo():
    global client, db

    client = AsyncIOMotorClient(settings.MONGO_URI)
    db = client[settings.DB_NAME]

    # RAG indexes
    await db.chunks.create_index("chunk_id", unique=True)
    await db.chunks.create_index("metadata.source")
    await db.chunks.create_index("metadata.file_type")

    # Chat history indexes
    await db.chat_history.create_index("user_id")
    await db.chat_history.create_index("session_id")
    await db.chat_history.create_index("timestamp")

    print("✅ MongoDB connected and indexes created")


async def close_mongo_connection():
    global client

    if client:
        client.close()
        client = None


def get_db():
    return db