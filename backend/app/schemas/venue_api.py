"""
Royals Intelligence - Venue, Pitch & Weather API Contracts
Pydantic v2 schemas for Venue Intelligence, Pitch Diagnostics,
Meteorological Telemetry, and Uncapped Player Venue Performance.
"""

from datetime import datetime, date, timezone
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class BoundaryDimensions(BaseModel):
    """Reliably measured boundary dimensions in meters. Explicitly None if unavailable."""
    straight_m: Optional[float] = Field(None, description="Straight boundary from stumps in meters")
    off_boundary_m: Optional[float] = Field(None, description="Square off-side boundary in meters")
    leg_boundary_m: Optional[float] = Field(None, description="Square leg-side boundary in meters")
    dimension_source: Optional[str] = Field(None, description="BCCI official venue measurement, stadium architectural plans, or None")
    is_verified: bool = False
    status: str = Field(default="UNAVAILABLE", description="'VERIFIED', 'PARTIALLY_AVAILABLE', 'UNAVAILABLE'")


class VenueSummaryItem(BaseModel):
    """Normalized overview of a cricket stadium / venue."""
    venue_id: str
    venue_code: str
    name: str
    city: str
    state: Optional[str] = None
    country: str = "India"
    is_rr_home: bool = False
    rr_venue_type: str = "Neutral"  # 'Primary Home (SMS)', 'Secondary Home (Guwahati)', 'Neutral'
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    coordinates_source: Optional[str] = None
    altitude_m: Optional[float] = None
    pitch_soil_type: Optional[str] = None
    matches_hosted_count: int = 0
    competitions_hosted: List[str] = Field(default_factory=list)
    data_completeness_pct: float = 100.0


class VenueDetailResponse(BaseModel):
    """Comprehensive stadium profile with boundary geometry, surface, and provenance."""
    venue_id: str
    venue_code: str
    name: str
    city: str
    state: Optional[str] = None
    country: str = "India"
    is_rr_home: bool = False
    rr_venue_type: str = "Neutral"
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    coordinates_source: Optional[str] = None
    altitude_m: Optional[float] = None
    pitch_soil_type: Optional[str] = None
    aliases: List[str] = Field(default_factory=list)
    boundary_dimensions: BoundaryDimensions
    surface_details: Dict[str, Any] = Field(default_factory=dict)
    stadium_capacity: Optional[int] = None
    floodlights_certified: bool = True
    matches_hosted_count: int = 0
    competitions_hosted: List[str] = Field(default_factory=list)
    provenance: Dict[str, Any] = Field(default_factory=dict)


class VenueScoringTrendsResponse(BaseModel):
    """Historical match scoring aggregates, toss patterns, and phase leverage."""
    venue_code: str
    venue_name: str
    matches_evaluated: int
    date_range_evaluated: str
    avg_first_innings_score: float
    avg_second_innings_score: float
    highest_total_recorded: int
    highest_total_match: Optional[str] = None
    lowest_total_recorded: int
    lowest_total_match: Optional[str] = None
    toss_decision_stats: Dict[str, float] = Field(
        default_factory=dict,
        description="Percentage of toss winners choosing bat vs field"
    )
    match_outcome_by_innings: Dict[str, float] = Field(
        default_factory=dict,
        description="Win percentage for defending (batting first) vs chasing (batting second)"
    )
    avg_wickets_per_innings: float
    phase_scoring_rates: Dict[str, float] = Field(
        default_factory=dict,
        description="Average run rates for Powerplay, Middle, and Death overs"
    )
    sample_size_confidence: str = Field(
        default="HIGH",
        description="'HIGH' (>=10 matches), 'MODERATE' (5-9 matches), 'LOW_SAMPLE' (<5 matches)"
    )
    sample_size_warning: Optional[str] = None
    is_fallback_data: bool = False


class PitchEvidenceAnalysisResponse(BaseModel):
    """
    Evidence-backed pitch conditions analysis.
    Important: Distinguishes observed statistical patterns from subjective pitch reports.
    Never claims deterministic future behavior based purely on historical averages.
    """
    venue_code: str
    venue_name: str
    pitch_soil_type: str
    observed_pace_vs_spin: Dict[str, Any] = Field(
        default_factory=dict,
        description="Wicket share percentage, economy rate comparison, and average for pace vs spin"
    )
    boundary_patterns: Dict[str, float] = Field(
        default_factory=dict,
        description="Percentage of total runs scored in boundaries (4s and 6s), boundaries per match"
    )
    dot_ball_patterns: Dict[str, float] = Field(
        default_factory=dict,
        description="Percentage of deliveries resulting in zero runs (dot balls)"
    )
    wickets_per_match: float
    conditions_evidence_classification: str = Field(
        default="Balanced / True Bounce",
        description="Empirical classification: 'Pace-Friendly', 'Spin-Friendly', 'Batting Paradise', 'Balanced / True Bounce', 'Bowling Dominant'"
    )
    observed_statistical_summary: str
    expert_reported_summary: Optional[str] = None
    sample_matches_evaluated: int
    deliveries_evaluated: int
    date_range_evaluated: str
    evidence_confidence: str = Field(
        default="HIGH",
        description="'HIGH', 'MODERATE', or 'LOW_SAMPLE'"
    )
    limitations_disclaimer: str = Field(
        default="Observed tendencies reflect historical conditions across evaluated match samples and must not be taken as a deterministic forecast for future fixtures."
    )
    is_fallback_data: bool = False


class WeatherObservationItem(BaseModel):
    """Meteorological telemetry record from Open-Meteo CC-BY 4.0 data stream."""
    venue_code: str
    observation_time: str
    phase_in_match: str = "MATCH_START"  # 'PRE_MATCH', 'INNINGS_1', 'INNINGS_2', 'POST_MATCH'
    temperature_c: float
    relative_humidity_pct: float
    dew_point_c: float
    dew_severity_risk: str = "LOW"  # 'LOW', 'MODERATE', 'HIGH_DEW_RISK'
    precipitation_mm: float = 0.0
    wind_speed_kph: float = 0.0
    wind_direction_deg: float = 0.0
    wind_direction_compass: str = "N"
    cloud_cover_pct: float = 0.0
    weather_condition: str = "Clear"
    is_forecast: bool = False
    source_attribution: str = "Weather data by Open-Meteo.com under CC-BY 4.0"
    retrieval_timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    reliability: str = "HIGH"


class MatchWeatherContextResponse(BaseModel):
    """Complete environmental, pitch, and historical venue context for a match fixture."""
    match_id: str
    match_date: str
    venue_code: str
    venue_name: str
    is_night_match: bool = True
    observations: List[WeatherObservationItem] = Field(default_factory=list)
    dew_impact_assessment: str
    temperature_swing_c: Optional[float] = None
    humidity_swing_pct: Optional[float] = None
    historical_scoring_context: Dict[str, Any] = Field(default_factory=dict)
    pitch_evidence_summary: str
    provenance: Dict[str, Any] = Field(default_factory=dict)


class WeatherSourceStatusResponse(BaseModel):
    """Health, licensing, and operational status of Open-Meteo weather integration."""
    source_id: str = "open_meteo_historical"
    source_name: str = "Open-Meteo Weather Archive & Forecast API"
    tier: str = "TIER_1"
    status: str = "OPERATIONAL"
    is_accessible: bool = True
    licensing: Dict[str, str] = Field(default_factory=lambda: {
        "license_name": "Creative Commons Attribution 4.0 International (CC-BY 4.0)",
        "commercial_use_permitted": "true",
        "attribution_required": "true",
        "attribution_text": "Weather data by Open-Meteo.com under CC-BY 4.0"
    })
    api_endpoint: str = "https://archive-api.open-meteo.com/v1/archive"
    rate_limit_policy: str = "Free tier up to 10,000 daily API calls with local persistent caching"
    cached_records_count: int = 0
    last_verified_timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class UncappedPlayerVenuePerformanceResponse(BaseModel):
    """
    Evidence-based performance summary for a verified uncapped player at a specific venue.
    Scope rule: Never evaluates senior international capped players.
    """
    player_id: str
    player_name: str
    is_uncapped: bool = True
    eligibility_status: str = "CONFIRMED_UNCAPPED"
    venue_code: str
    venue_name: str
    matches_at_venue: int = 0
    batting_at_venue: Dict[str, Any] = Field(default_factory=dict)
    bowling_at_venue: Dict[str, Any] = Field(default_factory=dict)
    sample_size_confidence: str = Field(
        default="MODERATE",
        description="'HIGH' (>=5 inn), 'MODERATE' (2-4 inn), 'LOW_SAMPLE' (1 inn)"
    )
    sample_size_warning: Optional[str] = None
    role_archetype: str
