"""
Royals Intelligence - Async Database Session Engine
Provides async session generators and connection diagnostic checks.
"""

import time
from typing import AsyncGenerator, Dict, Any
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy import text
from app.core.config import settings
from app.core.logging import logger

# Initialize async SQLAlchemy engine with connection pool
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG and settings.ENVIRONMENT == "development",
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_timeout=settings.DB_POOL_TIMEOUT,
    pool_recycle=settings.DB_POOL_RECYCLE,
    pool_pre_ping=True,
)

# Async session factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency yielding a scoped asynchronous database session.
    Automatically handles rollback on uncaught exceptions and session closing.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as exc:
            await session.rollback()
            logger.error(f"Database session error: {exc}")
            raise
        finally:
            await session.close()


async def check_database_connection() -> Dict[str, Any]:
    """
    Performs a non-destructive active ping against the PostgreSQL server.
    Returns status and diagnostic details without interrupting API operations.
    """
    start_time = time.perf_counter()
    try:
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            val = result.scalar_one_or_none()
            latency_ms = round((time.perf_counter() - start_time) * 1000, 2)
            if val == 1:
                return {
                    "status": "connected",
                    "engine": "postgresql+asyncpg",
                    "latency_ms": latency_ms,
                    "pool_size": settings.DB_POOL_SIZE,
                }
            return {
                "status": "unhealthy",
                "engine": "postgresql+asyncpg",
                "detail": "Unexpected query result",
            }
    except Exception as exc:
        return {
            "status": "offline_or_unreachable",
            "engine": "postgresql+asyncpg",
            "detail": str(exc),
            "note": "PostgreSQL service is not running or credentials pending verification.",
        }
