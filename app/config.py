from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    DATABASE_URL: str = "postgresql://user:password@localhost:5432/backend_db"

    SECRET_KEY: str = ""
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    DEBUG: bool = True
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Трамплин API"

    MINIO_ENDPOINT: str = "localhost:9000"
    MINIO_ACCESS_KEY: str = ""
    MINIO_SECRET_KEY: str = ""
    MINIO_BUCKET: str = "tramplin"
    MINIO_SECURE: bool = False
    MINIO_PUBLIC_URL: str = ""

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

if not settings.DEBUG and not settings.SECRET_KEY:
    raise RuntimeError("SECRET_KEY must be set in production (DEBUG=False)")
