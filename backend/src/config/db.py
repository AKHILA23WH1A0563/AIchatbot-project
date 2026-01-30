# db.py
from mongoengine import connect, Document, StringField
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/chat_db")

def connect_db():
    print("🔄 Connecting to MongoDB...")
    connect(host=MONGO_URI)

# Optional: export a placeholder object `db` for old imports
db = {"connect": connect_db}  # now `from config.db import db` works
