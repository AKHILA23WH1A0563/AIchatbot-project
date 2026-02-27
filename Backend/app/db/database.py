from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

client: AsyncIOMotorClient | None = None
db = None


async def connect_to_mongo():
    global client, db
    client = AsyncIOMotorClient(settings.MONGO_URI)
    db = client[settings.DB_NAME]

    # 🔥 Optimized indexes for fast retrieval
    await db.chunks.create_index("chunk_id", unique=True)
    await db.chunks.create_index("metadata.source")
    await db.chunks.create_index("metadata.file_type")


async def close_mongo_connection():
    global client
    if client:
        client.close()
        client = None


def get_db():
    return db