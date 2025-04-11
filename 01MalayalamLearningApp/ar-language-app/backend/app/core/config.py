from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./db/app.db"
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    OMDB_API_KEY: str = os.getenv("OMDB_API_KEY", "")

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

__all__ = ["settings"]