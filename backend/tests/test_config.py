"""
Royals Intelligence - Configuration & Environment Tests
"""

from app.core.config import settings


def test_settings_loaded():
    assert settings.PROJECT_NAME == "Royals Intelligence"
    assert settings.API_V1_PREFIX == "/api/v1"
    assert settings.POSTGRES_USER is not None
    assert "postgresql+asyncpg://" in settings.DATABASE_URL
    assert isinstance(settings.BACKEND_CORS_ORIGINS, list)
    assert len(settings.BACKEND_CORS_ORIGINS) > 0


def test_cors_settings():
    assert any("localhost" in origin for origin in settings.BACKEND_CORS_ORIGINS)


def test_database_url_normalization():
    from app.core.config import Settings
    from app.db.session import get_async_database_url

    test_cases = [
        ("postgres://user:pass@host:5432/db", "postgresql+asyncpg://user:pass@host:5432/db"),
        ("postgresql://user:pass@host:5432/db", "postgresql+asyncpg://user:pass@host:5432/db"),
        ("postgresql+psycopg2://user:pass@host:5432/db", "postgresql+asyncpg://user:pass@host:5432/db"),
        ("postgresql+asyncpg://user:pass@host:5432/db", "postgresql+asyncpg://user:pass@host:5432/db"),
        ("sqlite+aiosqlite:///:memory:", "sqlite+aiosqlite:///:memory:"),
    ]

    for raw_url, expected in test_cases:
        # Test Pydantic Settings validator
        s = Settings(DATABASE_URL=raw_url)
        assert s.DATABASE_URL == expected, f"Failed for {raw_url}: got {s.DATABASE_URL}"

        # Test session helper
        assert get_async_database_url(raw_url) == expected
