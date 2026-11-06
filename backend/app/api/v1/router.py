"""
Royals Intelligence - API v1 Master Router
Aggregates all version 1 route modules.
"""

from fastapi import APIRouter
from app.api.v1.endpoints import health, acquisition

api_router = APIRouter()

# Health and diagnostic routes
api_router.include_router(health.router, tags=["Health & Diagnostics"])

# Data Acquisition Engine routes
api_router.include_router(acquisition.router, prefix="/acquisition", tags=["Data Acquisition"])
