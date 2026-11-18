"""
Royals Intelligence - Application Configuration
Uses Pydantic BaseSettings for strong typing and environment parsing.
"""

from typing import List, Union
from pathlib import Path
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


def get_repo_root() -> Path:
    """Finds monorepo root by locating README.md and backend directory."""
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / "README.md").exists() and (parent / "backend").exists():
            return parent
    return current.parents[2]  # Fallback: backend/app/core -> backend -> root


class Settings(BaseSettings):
    # Base Application Metadata
    PROJECT_NAME: str = "Royals Intelligence"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    API_V1_PREFIX: str = "/api/v1"
    APP_VERSION: str = "0.1.0-stage0"
    SECRET_KEY: str = "development-secret-key-change-in-production-min-32-chars"
    
    # Server-Side Security & Proprietary Credentials (never client-asserted)
    SCOUT_ADMIN_API_KEY: str = "rr_scout_admin_secret_token_2026"
    LEAD_ANALYST_API_KEY: str = "rr_lead_analyst_secret_token_2026"

    # Server Binding
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # CORS Configuration
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
    ]

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # Database Configuration (PostgreSQL with AsyncPG)
    POSTGRES_USER: str = "royals_admin"
    POSTGRES_PASSWORD: str = "royals_secure_dev_password"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "royals_intelligence_db"
    
    # Fully resolved async database URI
    DATABASE_URL: str = (
        "postgresql+asyncpg://royals_admin:royals_secure_dev_password@localhost:5432/royals_intelligence_db"
    )

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def assemble_database_url(cls, v: str) -> str:
        if not v or not isinstance(v, str):
            return v
        # Render and standard PostgreSQL URLs often start with postgres:// or postgresql://
        # Because we use SQLAlchemy async engine, we must ensure the asyncpg driver is specified.
        if v.startswith("postgres://"):
            return v.replace("postgres://", "postgresql+asyncpg://", 1)
        elif v.startswith("postgresql://") and not v.startswith("postgresql+"):
            return v.replace("postgresql://", "postgresql+asyncpg://", 1)
        elif v.startswith("postgresql+psycopg2://"):
            return v.replace("postgresql+psycopg2://", "postgresql+asyncpg://", 1)
        elif v.startswith("postgresql+psycopg://"):
            return v.replace("postgresql+psycopg://", "postgresql+asyncpg://", 1)
        return v

    # Database Connection Pool Parameters
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20
    DB_POOL_TIMEOUT: int = 30
    DB_POOL_RECYCLE: int = 1800

    # Redis Configuration
    REDIS_URL: str = "redis://localhost:6379/0"

    # Storage Paths
    DATA_RAW_DIR: str = "../data/raw"
    DATA_PROCESSED_DIR: str = "../data/processed"
    DATA_EXTERNAL_DIR: str = "../data/external"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()
