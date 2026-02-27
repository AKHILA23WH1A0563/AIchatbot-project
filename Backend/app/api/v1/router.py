from fastapi import APIRouter
from app.api.v1.routes import auth, chat, travel, pdfs, chatbot, knowledge

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(chat.router, prefix="/chat", tags=["Chat"])
api_router.include_router(travel.router, prefix="/travel", tags=["Travel"])
api_router.include_router(pdfs.router, prefix="/pdfs", tags=["PDFs"])
api_router.include_router(chatbot.router, prefix="/chatbot", tags=["Chatbot"])
api_router.include_router(knowledge.router, prefix="/knowledge", tags=["Knowledge Base"])