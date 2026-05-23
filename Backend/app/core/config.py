from typing import Optional # Add this import at the top
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    MONGO_URI: str
    DB_NAME: str = "chat_db"

    JWT_SECRET: str = "supersecret"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60
    
    GROQ_API_KEY: str
    
    OPENAI_API_KEY: Optional[str] = None
    GOOGLE_CLIENT_ID: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file=".env", 
        extra="ignore"
    )

settings = Settings()