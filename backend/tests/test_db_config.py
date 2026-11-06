"""
Royals Intelligence - Database Engine & Base Configuration Tests
"""

import pytest
from app.db.base import Base
from app.db.session import engine, check_database_connection


def test_declarative_base_instantiation():
    assert Base.metadata is not None
    # Verify no tables exist in Stage 0
    assert len(Base.metadata.tables) == 0


def test_async_engine_configuration():
    assert engine.url.drivername == "postgresql+asyncpg"
    assert engine.pool is not None


@pytest.mark.asyncio
async def test_db_check_graceful_handling():
    # Calling check_database_connection should return structured dict without crashing
    health = await check_database_connection()
    assert isinstance(health, dict)
    assert "status" in health
    assert health["engine"] == "postgresql+asyncpg"
