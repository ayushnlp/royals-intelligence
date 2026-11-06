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
