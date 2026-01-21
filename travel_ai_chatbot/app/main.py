from fastapi import FastAPI
from app.api.v1.routes import chat, pdfs
from app.db.database import connect_to_mongo, close_mongo_connection

app = FastAPI(title="Travel AI Chatbot")

# Include API routers
app.include_router(chat.router, prefix="/api/v1", tags=["Chat"])
app.include_router(pdfs.router, prefix="/api/v1", tags=["PDFs"])

# Startup and shutdown events
@app.on_event("startup")
async def startup():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown():
    await close_mongo_connection()

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Travel AI Chatbot running"}
