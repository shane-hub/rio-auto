from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Rio Auto"
    API_V1_STR: str = "/api/v1"
    
    # Database
    # Default to SQLite for local development without Docker
    DATABASE_URL: str = "sqlite+aiosqlite:///./rio_auto.db"
    
    # Celery
    # Default to memory/eager for local development without Redis
    CELERY_BROKER_URL: str = "memory://"
    CELERY_RESULT_BACKEND: str = "db+sqlite:///./celery_results.sqlite"
    CELERY_TASK_ALWAYS_EAGER: bool = True
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
