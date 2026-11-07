"""
Royals Intelligence - Weather & Environmental Endpoints
FastAPI v1 endpoints for Open-Meteo CC-BY 4.0 historical observations,
match-date weather context, evening dew risk, and fixture forecasts.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.venue_api import (
    WeatherObservationItem,
    MatchWeatherContextResponse,
    WeatherSourceStatusResponse,
)
from app.services.venue.weather_intelligence_service import WeatherIntelligenceService
from app.services.venue.venue_match_context_engine import VenueMatchContextEngine

router = APIRouter()


@router.get(
    "/match/{match_id}",
    response_model=MatchWeatherContextResponse,
    summary="Get match weather context and dew telemetry",
    description="Returns pre-match and in-match meteorological observations, dew severity risk, and scoring variance."
)
async def get_match_weather_context(
    match_id: str,
    db: Optional[AsyncSession] = Depends(get_db)
):
    ctx = None
    try:
        ctx = await VenueMatchContextEngine.get_match_context(db, match_id)
    except Exception:
        ctx = await VenueMatchContextEngine.get_match_context(None, match_id)

    if not ctx:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Match weather context for fixture '{match_id}' could not be computed."
        )
    return ctx


@router.get(
    "/historical",
    response_model=List[WeatherObservationItem],
    summary="Get historical weather observations",
    description="Retrieves hourly observations (temp, humidity, dew point, wind) for a venue and date from Open-Meteo."
)
async def get_historical_weather(
    venue_code: str = Query(..., description="Canonical stadium code (e.g., 'SMS_JAIPUR')"),
    match_date: str = Query(..., description="Match date in YYYY-MM-DD format")
):
    return await WeatherIntelligenceService.get_historical_weather(venue_code, match_date)


@router.get(
    "/forecast",
    response_model=List[WeatherObservationItem],
    summary="Get meteorological forecast for future fixtures",
    description="Retrieves forecasted evening conditions. Strictly tagged with is_forecast=True and reliability='FORECAST_PROJECTION'."
)
async def get_weather_forecast(
    venue_code: str = Query(..., description="Canonical stadium code (e.g., 'SMS_JAIPUR')"),
    days_ahead: int = Query(7, ge=1, le=16, description="Days ahead to forecast (1 to 16)")
):
    return await WeatherIntelligenceService.get_forecast_weather(venue_code, days_ahead=days_ahead)


@router.get(
    "/source-status",
    response_model=WeatherSourceStatusResponse,
    summary="Get Open-Meteo integration health and licensing status",
    description="Audits Open-Meteo CC-BY 4.0 operational health, attribution requirements, and rate limit telemetry."
)
async def get_weather_source_status():
    return await WeatherIntelligenceService.get_source_status()
