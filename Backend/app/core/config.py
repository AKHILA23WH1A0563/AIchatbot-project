from typing import Optional # Add this import at the top
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    MONGO_URI: str
    DB_NAME: str = "chat_db"

    JWT_SECRET: str = "supersecret"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60
    
    GROQ_API_KEY: str
    
    # Change this line to make it optional
    # This prevents the "Field required" crash if the key isn't in your .env
    OPENAI_API_KEY: Optional[str] = None 

    model_config = SettingsConfigDict(
        env_file=".env", 
        extra="ignore"
    )

settings = Settings()