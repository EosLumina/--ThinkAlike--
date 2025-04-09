import os
import secrets
from typing import Any, Dict, List, Optional, Union

# Fix the BaseSettings import and usage
from pydantic import BaseModel, Field, validator

# Use BaseModel instead of BaseSettings if that's causing problems
class Settings(BaseModel):
    """Application settings loaded from environment variables.

    Following ThinkAlike's emphasis on transparency and security,
    critical configuration items are loaded from environment
    rather than hardcoded in the codebase.
    """
    PROJECT_NAME: str = "ThinkAlike"
    API_V1_STR: str = "/api/v1"

    # Security settings
    SECRET_KEY: str = os.environ.get("SECRET_KEY", secrets.token_urlsafe(32))
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days

    # CORS settings
    BACKEND_CORS_ORIGINS: List[str] = []

    # Database settings
    DATABASE_URL: str = os.environ.get("DATABASE_URL", "sqlite:///./thinkalike.db")

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        """Parse CORS origins from comma-separated string to list."""
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
