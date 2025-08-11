from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    HUGGINGFACE_API_KEY: str = ""
    DATABASE_URL: str = "sqlite:///./cascade.db"
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    PORT: int = 8000
    
    class Config:
        env_file = ".env"

settings = Settings()