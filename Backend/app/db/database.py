from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

client: AsyncIOMotorClient | None = None
db = None


# ============================================================
# 🔹 Connect to MongoDB
# ============================================================

async def connect_to_mongo():
    global client, db

    client = AsyncIOMotorClient(settings.MONGO_URI)
    db = client[settings.DB_NAME]

    print("✅ Connected to MongoDB")

    # ========================================================
    # 🔥 Optimized Indexes (Improves Retrieval Performance)
    # ========================================================

    # Unique chunk ID (prevents duplicate inserts)
    await db.chunks.create_index("chunk_id", unique=True)

    # Helps filter/search by document source
    await db.chunks.create_index("metadata.source")

    # Helps filter by file type if needed
    await db.chunks.create_index("metadata.file_type")

    print("📦 MongoDB indexes ensured")


# ============================================================
# 🔹 Close MongoDB Connection
# ============================================================

async def close_mongo_connection():
    global client

    if client:
        client.close()
        client = None
        print("🛑 MongoDB connection closed")


# ============================================================
# 🔹 Get Database Instance
# ============================================================

def get_db():
    return db