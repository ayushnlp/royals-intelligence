"""
Royals Intelligence - Venue & Pitch Intelligence Endpoints
FastAPI v1 endpoints for stadium directories, boundary geometry,
scoring trends, pitch evidence, and uncapped player venue tracking.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.venue_api import (
    VenueSummaryItem,
    VenueDetailResponse,
    VenueScoringTrendsResponse,
    PitchEvidenceAnalysisResponse,
    UncappedPlayerVenuePerformanceResponse,
)
from app.services.venue.venue_intelligence_service import VenueIntelligenceService
from app.services.domestic.domestic_season_service import DomesticSeasonService

router = APIRouter()


@router.get(
    "",
    response_model=List[VenueSummaryItem],
    summary="List all registered cricket venues",
    description="Returns normalized stadium profiles, geographic coordinates, and match hosting totals."
)
async def list_venues(
    rr_only: bool = Query(False, description="Filter for Rajasthan Royals home venues (SMS Jaipur and Barsapara Guwahati)"),
    db: Optional[AsyncSession] = Depends(get_db)
):
    try:
        return await VenueIntelligenceService.list_venues(db, is_rr_only=rr_only)
    except Exception as exc:
        # Fallback without active DB session
        return await VenueIntelligenceService.list_venues(None, is_rr_only=rr_only)


@router.get(
    "/{venue_id}",
    response_model=VenueDetailResponse,
    summary="Get venue details and boundary geometry",
    description="Retrieves official measured boundary dimensions, soil details, capacity, and provenance."
)
async def get_venue_detail(
    venue_id: str,
    db: Optional[AsyncSession] = Depends(get_db)
):
    venue = None
    try:
        venue = await VenueIntelligenceService.get_venue_detail(db, venue_id)
    except Exception:
        venue = await VenueIntelligenceService.get_venue_detail(None, venue_id)

    if not venue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Venue '{venue_id}' not found in registered stadium catalog."
        )
    return venue


@router.get(
    "/{venue_id}/scoring-trends",
    response_model=VenueScoringTrendsResponse,
    summary="Get venue historical scoring trends",
    description="Returns 1st/2nd innings averages, toss correlations, and phase-wise run rates."
)
async def get_venue_scoring_trends(
    venue_id: str,
    db: Optional[AsyncSession] = Depends(get_db)
):
    trends = None
    try:
        trends = await VenueIntelligenceService.get_venue_scoring_trends(db, venue_id)
    except Exception:
        trends = await VenueIntelligenceService.get_venue_scoring_trends(None, venue_id)

    if not trends:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Scoring trends for venue '{venue_id}' could not be computed."
        )
    return trends


@router.get(
    "/{venue_id}/pitch-analysis",
    response_model=PitchEvidenceAnalysisResponse,
    summary="Get evidence-backed pitch analysis",
    description="Computes pace vs spin wicket shares, economy rates, boundary percentages, and empirical conditions."
)
async def get_pitch_evidence(
    venue_id: str,
    db: Optional[AsyncSession] = Depends(get_db)
):
    evidence = None
    try:
        evidence = await VenueIntelligenceService.get_pitch_evidence(db, venue_id)
    except Exception:
        evidence = await VenueIntelligenceService.get_pitch_evidence(None, venue_id)

    if not evidence:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pitch evidence for venue '{venue_id}' could not be evaluated."
        )
    return evidence


@router.get(
    "/{venue_id}/player-performance",
    response_model=UncappedPlayerVenuePerformanceResponse,
    summary="Get uncapped player track record at venue",
    description="Evaluates batting and bowling performance for an uncapped player at this stadium. Scope: UNCAPPED ONLY."
)
async def get_player_venue_performance(
    venue_id: str,
    player_id: str = Query(..., description="Canonical ID of the verified uncapped player"),
    db: Optional[AsyncSession] = Depends(get_db)
):
    try:
        perf = await VenueIntelligenceService.get_uncapped_player_venue_performance(db, venue_id, player_id)
    except PermissionError as perm_err:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(perm_err)
        )
    except Exception:
        perf = await VenueIntelligenceService.get_uncapped_player_venue_performance(None, venue_id, player_id)

    if not perf:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Performance records for player '{player_id}' at venue '{venue_id}' not found."
        )
    return perf
