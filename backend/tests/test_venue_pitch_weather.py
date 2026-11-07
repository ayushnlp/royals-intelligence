"""
Royals Intelligence - Venue, Pitch & Weather Intelligence Tests (Stage 4)
Unit and integration tests validating venue normalization, boundary dimensions,
pitch evidence analysis, Open-Meteo meteorological telemetry, match context, and uncapped scope guards.
"""

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient

from app.main import app as fastapi_app
from app.services.venue.venue_intelligence_service import VenueIntelligenceService, VERIFIED_VENUE_CATALOG
from app.services.venue.weather_intelligence_service import WeatherIntelligenceService
from app.services.venue.venue_match_context_engine import VenueMatchContextEngine
from app.acquisition.normalization.normalizer import CricketDataNormalizer


def test_venue_identity_and_alias_resolution():
    """Validates that stadium names and colloquial aliases map to canonical codes."""
    assert CricketDataNormalizer.normalize_venue("Sawai Mansingh Stadium") == "SMS_JAIPUR"
    assert CricketDataNormalizer.normalize_venue("Sawai Mansingh Stadium, Jaipur") == "SMS_JAIPUR"
    assert CricketDataNormalizer.normalize_venue("barsapara cricket stadium, guwahati") == "BARS_GUWAHATI"
    assert CricketDataNormalizer.normalize_venue("Wankhede Stadium, Mumbai") == "WANKHEDE_MUMBAI"
    assert CricketDataNormalizer.normalize_venue("Arun Jaitley Stadium, Delhi") == "JAITLEY_DELHI"
    assert CricketDataNormalizer.normalize_venue("feroz shah kotla") == "JAITLEY_DELHI"
    assert CricketDataNormalizer.normalize_venue("m chinnaswamy stadium") == "CHINNASWAMY_BLR"
    assert CricketDataNormalizer.normalize_venue("ma chidambaram stadium, chepauk") == "CHIDAMBARAM_CHENNAI"


def test_coordinate_validation_and_missing_attributes():
    """Validates that coordinates are authentic and unknown dimensions are represented as None."""
    sms = VERIFIED_VENUE_CATALOG["SMS_JAIPUR"]
    assert 26.0 <= sms["latitude"] <= 27.5
    assert 75.0 <= sms["longitude"] <= 76.5
    assert sms["is_rr_home"] is True
    assert sms["rr_venue_type"] == "Primary Home (SMS)"
    assert sms["boundary_dimensions"]["straight_m"] == 70.0
    assert sms["boundary_dimensions"]["is_verified"] is True

    # Test unknown venue alias returns None / unavailable
    unknown = VenueIntelligenceService.normalize_venue_code("Village Ground X")
    assert unknown == "Village Ground X"


@pytest.mark.asyncio
async def test_venue_scoring_aggregation_and_small_sample():
    """Tests venue scoring trends computation and small-sample limitation warnings."""
    # High sample venue (SMS Jaipur: 55 matches)
    sms_trends = await VenueIntelligenceService.get_venue_scoring_trends(None, "SMS_JAIPUR")
    assert sms_trends is not None
    assert sms_trends.matches_evaluated == 55
    assert sms_trends.avg_first_innings_score > 150.0
    assert sms_trends.avg_second_innings_score > 140.0
    assert sms_trends.sample_size_confidence == "HIGH"
    assert sms_trends.sample_size_warning is None
    assert "powerplay" in sms_trends.phase_scoring_rates

    # Lower sample venue (Mullanpur: 6 matches)
    mul_trends = await VenueIntelligenceService.get_venue_scoring_trends(None, "MULLANPUR_PBKS")
    assert mul_trends is not None
    assert mul_trends.matches_evaluated == 6
    assert mul_trends.sample_size_confidence == "MODERATE"
    assert mul_trends.sample_size_warning is not None
    assert "IPL 2024" in mul_trends.sample_size_warning or "sample size" in mul_trends.sample_size_warning.lower()


@pytest.mark.asyncio
async def test_pitch_evidence_provenance_and_classification():
    """Tests pace vs spin calculations, empirical classifications, and limitations disclaimer."""
    # Chepauk (Spin-friendly, 46% spin wickets)
    chepauk = await VenueIntelligenceService.get_pitch_evidence(None, "CHIDAMBARAM_CHENNAI")
    assert chepauk is not None
    assert chepauk.conditions_evidence_classification == "Spin-Friendly"
    assert chepauk.observed_pace_vs_spin["spin_wickets_share_pct"] == 46.0
    assert chepauk.observed_pace_vs_spin["pace_wickets_share_pct"] + chepauk.observed_pace_vs_spin["spin_wickets_share_pct"] == 100.0
    assert chepauk.dot_ball_patterns["dot_ball_pct"] > 30.0
    assert chepauk.limitations_disclaimer is not None
    assert "deterministic" in chepauk.limitations_disclaimer.lower()

    # Chinnaswamy (Batting Paradise, avg 1st inn > 180)
    chinnaswamy = await VenueIntelligenceService.get_pitch_evidence(None, "CHINNASWAMY_BLR")
    assert chinnaswamy is not None
    assert chinnaswamy.conditions_evidence_classification == "Batting Paradise"
    assert chinnaswamy.boundary_patterns["boundary_runs_pct"] > 60.0


@pytest.mark.asyncio
async def test_historical_weather_vs_forecast_distinction():
    """Verifies that historical observations and future forecasts are strictly segregated."""
    # Historical observations
    hist = await WeatherIntelligenceService.get_historical_weather("SMS_JAIPUR", "2024-04-06")
    assert len(hist) > 0
    for obs in hist:
        assert obs.is_forecast is False
        assert obs.venue_code == "SMS_JAIPUR"
        assert "Open-Meteo" in obs.source_attribution
        assert "CC-BY 4.0" in obs.source_attribution

    # Forecast projections
    forecast = await WeatherIntelligenceService.get_forecast_weather("SMS_JAIPUR", days_ahead=3)
    assert len(forecast) > 0
    for fc in forecast:
        assert fc.is_forecast is True
        assert fc.reliability == "FORECAST_PROJECTION"


@pytest.mark.asyncio
async def test_weather_dew_risk_calculation():
    """Verifies empirical calculation of evening dew risk."""
    # High dew condition (Humidity >= 70% or depression <= 3)
    high_dew = WeatherIntelligenceService._calculate_dew_risk(temp=25.0, humidity=75.0, dew_point=23.0)
    assert high_dew == "HIGH_DEW_RISK"

    # Moderate dew condition
    mod_dew = WeatherIntelligenceService._calculate_dew_risk(temp=28.0, humidity=60.0, dew_point=19.0)
    assert mod_dew == "MODERATE"

    # Low dew condition
    low_dew = WeatherIntelligenceService._calculate_dew_risk(temp=35.0, humidity=35.0, dew_point=12.0)
    assert low_dew == "LOW"


@pytest.mark.asyncio
async def test_match_to_venue_context_engine():
    """Tests unifying match records with venue geometry, pitch evidence, and in-match weather."""
    ctx = await VenueMatchContextEngine.get_match_context(None, "smat_2024_del_pun")
    assert ctx is not None
    assert ctx.match_id == "smat_2024_del_pun"
    assert ctx.venue_code in ["JAITLEY_DELHI", "SMS_JAIPUR"]
    assert len(ctx.observations) > 0
    assert ctx.dew_impact_assessment is not None
    assert ctx.provenance["weather_source"] == "Open-Meteo Archive (CC-BY 4.0)"
    assert "first_innings_variance_from_par" in ctx.historical_scoring_context


@pytest.mark.asyncio
async def test_uncapped_player_venue_filtering_and_scope_guard():
    """Validates uncapped prospect venue performance and ensures capped player queries are forbidden."""
    # Valid uncapped prospect
    ashutosh = await VenueIntelligenceService.get_uncapped_player_venue_performance(None, "SMS_JAIPUR", "uncapped_rr_01")
    assert ashutosh is not None
    assert ashutosh.player_name == "Ashutosh Sharma"
    assert ashutosh.is_uncapped is True
    assert ashutosh.batting_at_venue["runs"] > 0
    assert ashutosh.batting_at_venue["death_sr"] > 180.0
    assert "Death-Overs" in ashutosh.role_archetype

    # Capped senior player must raise PermissionError (Scope Rule)
    with pytest.raises(PermissionError) as exc_info:
        await VenueIntelligenceService.get_uncapped_player_venue_performance(None, "SMS_JAIPUR", "virat_kohli")
    assert "UNCAPPED PLAYERS ONLY" in str(exc_info.value)


def test_venue_and_weather_endpoints_integration():
    """Integration test verifying all FastAPI REST endpoints under /api/v1/venues and /api/v1/weather."""
    client = TestClient(fastapi_app)

    # 1. List venues
    res = client.get("/api/v1/venues")
    assert res.status_code == 200
    venues = res.json()
    assert len(venues) >= 7
    codes = [v["venue_code"] for v in venues]
    assert "SMS_JAIPUR" in codes
    assert "BARS_GUWAHATI" in codes

    # 2. RR-only filter
    res_rr = client.get("/api/v1/venues?rr_only=true")
    assert res_rr.status_code == 200
    rr_venues = res_rr.json()
    assert len(rr_venues) == 2
    assert all(v["is_rr_home"] is True for v in rr_venues)

    # 3. Venue detail
    res_detail = client.get("/api/v1/venues/SMS_JAIPUR")
    assert res_detail.status_code == 200
    detail = res_detail.json()
    assert detail["name"] == "Sawai Mansingh Stadium"
    assert detail["boundary_dimensions"]["straight_m"] == 70.0
    assert detail["boundary_dimensions"]["is_verified"] is True

    # 4. Scoring trends
    res_trends = client.get("/api/v1/venues/SMS_JAIPUR/scoring-trends")
    assert res_trends.status_code == 200
    trends = res_trends.json()
    assert trends["avg_first_innings_score"] > 150.0

    # 5. Pitch analysis
    res_pitch = client.get("/api/v1/venues/WANKHEDE_MUMBAI/pitch-analysis")
    assert res_pitch.status_code == 200
    pitch = res_pitch.json()
    assert pitch["pitch_soil_type"] == "Red Soil"
    assert pitch["observed_pace_vs_spin"]["pace_wickets_share_pct"] > 60.0

    # 6. Uncapped player venue performance
    res_player = client.get("/api/v1/venues/SMS_JAIPUR/player-performance?player_id=uncapped_rr_01")
    assert res_player.status_code == 200
    player_perf = res_player.json()
    assert player_perf["player_name"] == "Ashutosh Sharma"

    # 7. Uncapped scope guard via endpoint (Forbidden 403 for capped international player)
    res_capped = client.get("/api/v1/venues/SMS_JAIPUR/player-performance?player_id=virat_kohli")
    assert res_capped.status_code == 403

    # 8. Weather match context
    res_mweather = client.get("/api/v1/weather/match/smat_2024_del_pun")
    assert res_mweather.status_code == 200
    m_ctx = res_mweather.json()
    assert m_ctx["provenance"]["weather_source"] == "Open-Meteo Archive (CC-BY 4.0)"

    # 9. Historical weather
    res_hweather = client.get("/api/v1/weather/historical?venue_code=SMS_JAIPUR&match_date=2024-04-06")
    assert res_hweather.status_code == 200
    assert len(res_hweather.json()) > 0

    # 10. Forecast weather
    res_fweather = client.get("/api/v1/weather/forecast?venue_code=SMS_JAIPUR&days_ahead=3")
    assert res_fweather.status_code == 200
    assert all(item["is_forecast"] is True for item in res_fweather.json())

    # 11. Weather source status
    res_status = client.get("/api/v1/weather/source-status")
    assert res_status.status_code == 200
    status_data = res_status.json()
    assert status_data["source_id"] == "open_meteo_historical"
    assert "CC-BY 4.0" in status_data["licensing"]["license_name"]

