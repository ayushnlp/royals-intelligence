"""
Royals Intelligence - Configuration & Production Security Tests
Tests Workstream D requirements: production secrets cannot silently fall back to development defaults.
"""

import pytest
from app.core.config import Settings


@pytest.mark.environment
def test_development_configuration_allows_defaults():
    """Development environment must permit default local convenience credentials."""
    s = Settings(ENVIRONMENT="development")
    assert s.ENVIRONMENT == "development"
    assert s.SECRET_KEY == "development-secret-key-change-in-production-min-32-chars"
    assert s.SCOUT_ADMIN_API_KEY == "rr_scout_admin_secret_token_2026"
    assert s.LEAD_ANALYST_API_KEY == "rr_lead_analyst_secret_token_2026"


@pytest.mark.environment
def test_production_rejects_default_secret_key():
    """Production environment must reject default or short development SECRET_KEY."""
    with pytest.raises(ValueError) as excinfo:
        Settings(
            ENVIRONMENT="production",
            SECRET_KEY="development-secret-key-change-in-production-min-32-chars",
            SCOUT_ADMIN_API_KEY="custom_prod_admin_token_xyz_99",
            LEAD_ANALYST_API_KEY="custom_prod_analyst_token_abc_88",
        )
    assert "Insecure production configuration" in str(excinfo.value)
    assert "SECRET_KEY" in str(excinfo.value)


@pytest.mark.environment
def test_production_rejects_short_secret_key():
    """Production environment must reject SECRET_KEY with length < 32."""
    with pytest.raises(ValueError) as excinfo:
        Settings(
            ENVIRONMENT="production",
            SECRET_KEY="too-short-secret-key",
            SCOUT_ADMIN_API_KEY="custom_prod_admin_token_xyz_99",
            LEAD_ANALYST_API_KEY="custom_prod_analyst_token_abc_88",
        )
    assert "SECRET_KEY (must be unique and >= 32 characters)" in str(excinfo.value)


@pytest.mark.environment
def test_production_rejects_default_privileged_api_keys():
    """Production environment must reject default scout and analyst API keys."""
    with pytest.raises(ValueError) as excinfo:
        Settings(
            ENVIRONMENT="production",
            SECRET_KEY="a" * 32,
            SCOUT_ADMIN_API_KEY="rr_scout_admin_secret_token_2026",
            LEAD_ANALYST_API_KEY="rr_lead_analyst_secret_token_2026",
        )
    assert "SCOUT_ADMIN_API_KEY" in str(excinfo.value)
    assert "LEAD_ANALYST_API_KEY" in str(excinfo.value)


@pytest.mark.environment
def test_production_accepts_valid_secure_configuration():
    """Production environment must accept fully configured secure credentials."""
    s = Settings(
        ENVIRONMENT="production",
        SECRET_KEY="c" * 32,
        SCOUT_ADMIN_API_KEY="prod_scout_admin_unique_key_12345",
        LEAD_ANALYST_API_KEY="prod_lead_analyst_unique_key_67890",
    )
    assert s.ENVIRONMENT == "production"
    assert s.SECRET_KEY == "c" * 32
