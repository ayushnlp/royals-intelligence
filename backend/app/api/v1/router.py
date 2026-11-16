"""
Royals Intelligence - API v1 Master Router
Aggregates all version 1 route modules.
"""

from fastapi import APIRouter
from app.api.v1.endpoints import (
    health,
    acquisition,
    players,
    analytics,
    proprietary,
    domestic,
    venues,
    weather,
    tactical,
    pressure,
)

api_router = APIRouter()

# Health and diagnostic routes
api_router.include_router(health.router, tags=["Health & Diagnostics"])

# Round 1 Pressure Analytics routes (SupeRR Selector Challenge)
api_router.include_router(pressure.router, prefix="/analytics/pressure", tags=["Round 1 Pressure Analytics"])

# Data Acquisition Engine routes
api_router.include_router(acquisition.router, prefix="/acquisition", tags=["Data Acquisition"])

# Uncapped Players & Eligibility routes (Stage 2)
api_router.include_router(players.router, prefix="/players", tags=["Uncapped Players"])

# Analytics Foundation routes (Stage 2)
api_router.include_router(analytics.router, prefix="/analytics", tags=["Analytics Foundation"])

# Tactical Cricket Intelligence routes (Stage 5)
api_router.include_router(tactical.router, prefix="/analytics/tactical", tags=["Tactical Cricket Intelligence"])

# RR Proprietary Data Pack & Scouting routes (Stage 2)
api_router.include_router(proprietary.router, prefix="/proprietary", tags=["RR Proprietary Scouting"])

# Domestic Season & Match Intelligence routes (Stage 3)
api_router.include_router(domestic.router, prefix="/domestic", tags=["Domestic Season & Match Intelligence"])

# Venue & Pitch Intelligence routes (Stage 4)
api_router.include_router(venues.router, prefix="/venues", tags=["Venue & Pitch Intelligence"])

# Weather & Environmental Telemetry routes (Stage 4)
api_router.include_router(weather.router, prefix="/weather", tags=["Weather & Environmental Telemetry"])
