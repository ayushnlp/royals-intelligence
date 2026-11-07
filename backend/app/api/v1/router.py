"""
Royals Intelligence - API v1 Master Router
Aggregates all version 1 route modules.
"""

from fastapi import APIRouter
from app.api.v1.endpoints import health, acquisition, players, analytics, proprietary

api_router = APIRouter()

# Health and diagnostic routes
api_router.include_router(health.router, tags=["Health & Diagnostics"])

# Data Acquisition Engine routes
api_router.include_router(acquisition.router, prefix="/acquisition", tags=["Data Acquisition"])

# Uncapped Players & Eligibility routes (Stage 2)
api_router.include_router(players.router, prefix="/players", tags=["Uncapped Players"])

# Analytics Foundation routes (Stage 2)
api_router.include_router(analytics.router, prefix="/analytics", tags=["Analytics Foundation"])

# RR Proprietary Data Pack & Scouting routes (Stage 2)
api_router.include_router(proprietary.router, prefix="/proprietary", tags=["RR Proprietary Scouting"])
