"""
Royals Intelligence - Application Configuration
Uses Pydantic BaseSettings for strong typing and environment parsing.
"""

import os
from typing import List, Union, Optional
from pathlib import Path
from pydantic import field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


def get_repo_root() -> Path:
    """
    Deterministically resolves monorepo root across local development,
    Docker containers, and cloud deployment environments.
    """
    env_root = os.environ.get("ROYALS_REPO_ROOT")
    if env_root and Path(env_root).exists():
        return Path(env_root).resolve()

    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / "README.md").exists() and (parent / "backend").exists():
            return parent
        if (parent / "round1_pressure").exists() and (parent / "data").exists():
            return parent

    # Fallbacks for Docker (/app) or isolated backend root
    for parent in current.parents:
        if (parent / "data" / "runtime_assets").exists():
            return parent

    return current.parents[2]  # Fallback: backend/app/core -> backend -> root


def resolve_asset_path(relative_path: Union[str, Path], required: bool = True) -> Path:
    """
    Deterministically resolves a dataset asset path across monorepo root,
    packaged runtime assets, Docker container paths, and local environments.
    Fails explicitly with a descriptive RuntimeError if required=True and file is missing.
    """
    rel = Path(relative_path)
    root = get_repo_root()
    cwd = Path.cwd()
    filename = rel.name

    data_env = os.environ.get("DATA_DIR")
    candidates = [
        root / rel,
        cwd / rel,
        root / "backend" / rel,
        cwd / "backend" / rel,
        root / "round1_pressure" / "data" / "processed" / filename,
        cwd / "round1_pressure" / "data" / "processed" / filename,
        root / "backend" / "data" / "runtime_assets" / filename,
        root / "data" / "runtime_assets" / filename,
        cwd / "data" / "runtime_assets" / filename,
        Path("/app") / rel,
        Path("/app/round1_pressure/data/processed") / filename,
        Path("/app/data/runtime_assets") / filename,
        Path("/data") / rel,
        Path("/data/pressure") / filename,
        Path("/data") / filename,
        Path("/etc/secrets") / filename,
        Path("/var/data") / rel,
        Path("/var/data/pressure") / filename,
        Path("/var/data") / filename,
    ]
    if data_env:
        candidates.insert(0, Path(data_env) / rel)
        candidates.insert(1, Path(data_env) / "pressure" / filename)
        candidates.insert(2, Path(data_env) / filename)

    for candidate in candidates:
        if candidate.exists():
            return candidate

    if required:
        searched = "\n  - ".join(str(c) for c in candidates[:6])
        raise RuntimeError(
            f"CRITICAL: Required dataset asset '{rel}' not found.\n"
            f"Searched locations include:\n  - {searched}\n"
            f"Ensure runtime datasets are properly hydrated or packaged."
        )

    return candidates[0]


class Settings(BaseSettings):
    # Base Application Metadata
    PROJECT_NAME: str = "Royals Intelligence"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    API_V1_PREFIX: str = "/api/v1"
    APP_VERSION: str = "0.1.0-diag-1"
    SECRET_KEY: str = "development-secret-key-change-in-production-min-32-chars"
    
    # Server-Side Security & Proprietary Credentials (never client-asserted)
    SCOUT_ADMIN_API_KEY: Optional[str] = None
    LEAD_ANALYST_API_KEY: Optional[str] = None

    # Server Binding
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # CORS Configuration
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
        "https://royals-intelligence.vercel.app",
        "https://royals-intelligence-api.onrender.com",
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

    @model_validator(mode="after")
    def validate_production_security(self) -> "Settings":
        """Ensures that default development credentials and secrets cannot run in production."""
        if self.ENVIRONMENT.lower() == "production":
            insecure_items: List[str] = []
            if self.SECRET_KEY == "development-secret-key-change-in-production-min-32-chars" or len(self.SECRET_KEY) < 32:
                insecure_items.append("SECRET_KEY (must be unique and >= 32 characters)")
            if not self.SCOUT_ADMIN_API_KEY or self.SCOUT_ADMIN_API_KEY == "rr_scout_admin_secret_token_2026":
                insecure_items.append("SCOUT_ADMIN_API_KEY (must be explicitly configured with a secure non-default secret)")
            if not self.LEAD_ANALYST_API_KEY or self.LEAD_ANALYST_API_KEY == "rr_lead_analyst_secret_token_2026":
                insecure_items.append("LEAD_ANALYST_API_KEY (must be explicitly configured with a secure non-default secret)")
            
            if insecure_items:
                raise ValueError(
                    f"Insecure production configuration: Privileged keys and secrets must be explicitly configured "
                    f"in production environment. Insecure keys: {', '.join(insecure_items)}"
                )
        return self

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()
