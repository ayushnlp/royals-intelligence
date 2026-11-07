"""
Royals Intelligence - Venue & Match Context Engine
Unifies stadium dimensions, pitch evidence, meteorological observations,
and match scoring variance into a single holistic context dossier.
"""

from typing import Optional, Dict, Any
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.core import MatchModel
from app.schemas.venue_api import MatchWeatherContextResponse, WeatherObservationItem
from app.services.venue.venue_intelligence_service import VenueIntelligenceService, VERIFIED_VENUE_CATALOG
from app.services.venue.weather_intelligence_service import WeatherIntelligenceService
from app.services.domestic.domestic_match_service import DomesticMatchService
from app.core.logging import logger


class VenueMatchContextEngine:
    """Enterprise context engine linking match fixtures to venue geometry and weather observations."""

    @classmethod
    async def get_match_context(
        cls,
        session: Optional[AsyncSession],
        match_id: str
    ) -> Optional[MatchWeatherContextResponse]:
        """
        Builds the unified match context:
        - Match venue & boundary parameters
        - Historical scoring expectations vs actual match performance
        - In-match weather progression (temperature drop, humidity rise, dew risk)
        - Pitch condition evidence and limitations
        """
        match_resp = await DomesticMatchService.get_match_detail(session, match_id)
        if not match_resp:
            return None

        v_code = VenueIntelligenceService.normalize_venue_code(match_resp.venue_name)
        v_data = VERIFIED_VENUE_CATALOG.get(v_code)
        v_name = v_data["name"] if v_data else match_resp.venue_name

        # Weather observations for match date
        weather_obs = await WeatherIntelligenceService.get_historical_weather(v_code, match_resp.match_date)

        # In-match temperature / humidity swings
        t_start = None
        t_end = None
        h_start = None
        h_end = None
        high_dew = False

        for obs in weather_obs:
            if obs.phase_in_match == "PRE_MATCH" or (obs.phase_in_match == "INNINGS_1" and t_start is None):
                t_start = obs.temperature_c
                h_start = obs.relative_humidity_pct
            if obs.phase_in_match == "INNINGS_2":
                t_end = obs.temperature_c
                h_end = obs.relative_humidity_pct
                if obs.dew_severity_risk == "HIGH_DEW_RISK":
                    high_dew = True

        t_swing = round(t_start - t_end, 1) if (t_start is not None and t_end is not None) else None
        h_swing = round(h_end - h_start, 1) if (h_start is not None and h_end is not None) else None

        if high_dew:
            dew_assessment = (
                f"High Dew Impact: Second innings humidity rose to {h_end:.1f}% with temperature drop of {t_swing}°C. "
                "Significant wet-ball conditions observed, reducing finger-spin purchase and providing seam skid advantage to chasing batters."
            )
        elif h_swing and h_swing > 15.0:
            dew_assessment = (
                f"Moderate Dew Impact: Second innings humidity increased by {h_swing:.1f}%. "
                "Minor surface slickness recorded in late death overs."
            )
        else:
            dew_assessment = "Low Dew Impact: Evening humidity remained stable with crisp ball grip maintained across both innings."

        # Venue scoring trends
        trends = await VenueIntelligenceService.get_venue_scoring_trends(session, v_code)
        scoring_ctx: Dict[str, Any] = {}
        if trends:
            actual_inn1 = match_resp.innings[0].total_runs if match_resp.innings else 0
            scoring_delta = round(actual_inn1 - trends.avg_first_innings_score, 1)
            scoring_ctx = {
                "venue_historical_avg_first_innings": trends.avg_first_innings_score,
                "venue_historical_avg_second_innings": trends.avg_second_innings_score,
                "actual_first_innings_score": actual_inn1,
                "first_innings_variance_from_par": scoring_delta,
                "variance_assessment": "ABOVE_VENUE_PAR" if scoring_delta > 10.0 else ("BELOW_VENUE_PAR" if scoring_delta < -10.0 else "PAR_SCORE"),
                "chase_win_rate_at_venue": trends.match_outcome_by_innings.get("chase_win_pct", 50.0),
            }

        # Pitch evidence summary
        pitch = await VenueIntelligenceService.get_pitch_evidence(session, v_code)
        pitch_sum = pitch.observed_statistical_summary if pitch else f"Pitch soil: {v_data.get('pitch_soil_type', 'Standard Turf') if v_data else 'Standard Turf'}"

        # Provenance: distinguish verified Cricsheet / BCCI data from sample fixtures
        is_seed = getattr(match_resp, "data_provenance", {}).get("is_fallback_data", False) or match_id.startswith("sample_") or match_id == "smat_2024_del_pun"

        return MatchWeatherContextResponse(
            match_id=match_id,
            match_date=match_resp.match_date,
            venue_code=v_code,
            venue_name=v_name,
            is_night_match=True,
            observations=weather_obs,
            dew_impact_assessment=dew_assessment,
            temperature_swing_c=t_swing,
            humidity_swing_pct=h_swing,
            historical_scoring_context=scoring_ctx,
            pitch_evidence_summary=pitch_sum,
            provenance={
                "weather_source": "Open-Meteo Archive (CC-BY 4.0)",
                "venue_source": "BCCI Stadium Directory / Survey of India",
                "match_provenance_type": "FALLBACK_FIXTURE" if is_seed else "VERIFIED_REAL_WORLD",
                "is_verified_real_world": not is_seed,
                "retrieved_at": datetime.now(timezone.utc).isoformat(),
            }
        )

