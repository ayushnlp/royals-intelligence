"""
Royals Intelligence - Uncapped Player Intelligence REST API Endpoints
Provides dedicated endpoints for Indian Uncapped Batters & Bowlers leaderboards,
role-based performance profiles, and strict BCCI domestic eligibility auditing.
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.analytics.uncapped_pressure_intelligence import UncappedPressureIntelligenceService
from app.schemas.uncapped_pressure import (
    UncappedLeaderboardResponse,
    UncappedBattingItem,
    UncappedBowlingItem,
    UncappedOverviewResponse,
)
from app.core.logging import logger

router = APIRouter()

# Singleton cache for uncapped pressure service
_uncapped_service: Optional[UncappedPressureIntelligenceService] = None


def get_uncapped_service() -> UncappedPressureIntelligenceService:
    """Dependency provider returning singleton instance of UncappedPressureIntelligenceService."""
    global _uncapped_service
    if _uncapped_service is None:
        logger.info("Initializing UncappedPressureIntelligenceService...")
        _uncapped_service = UncappedPressureIntelligenceService()
        _uncapped_service.load_data()
        logger.info("UncappedPressureIntelligenceService initialized successfully.")
    return _uncapped_service


@router.get(
    "/overview",
    response_model=UncappedOverviewResponse,
    summary="Uncapped Talent Pool Overview",
    description="Returns aggregate counts of verified uncapped candidates meeting sample qualification gates.",
)
def get_uncapped_overview(
    service: UncappedPressureIntelligenceService = Depends(get_uncapped_service),
) -> UncappedOverviewResponse:
    try:
        data = service.get_uncapped_overview()
        return UncappedOverviewResponse(**data)
    except Exception as exc:
        logger.error(f"Failed to generate uncapped overview: {exc}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve uncapped overview diagnostics.",
        )


@router.get(
    "/leaderboards",
    response_model=UncappedLeaderboardResponse,
    summary="Uncapped Player Pressure Leaderboards",
    description="Returns ranked Uncapped Batters and Bowlers Under Pressure with strict BCCI eligibility auditing.",
)
def get_uncapped_leaderboards(
    discipline: str = Query("all", description="'all', 'batting', or 'bowling'"),
    limit: int = Query(10, ge=1, le=50, description="Number of candidates to return"),
    qualified_only: bool = Query(True, description="Filter for sample-qualified candidates (>= 60 balls)"),
    service: UncappedPressureIntelligenceService = Depends(get_uncapped_service),
) -> UncappedLeaderboardResponse:
    disc_norm = discipline.lower()
    if disc_norm not in ["all", "batting", "bowling"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid discipline '{discipline}'. Must be 'all', 'batting', or 'bowling'.",
        )

    batting_items = None
    if disc_norm in ["all", "batting"]:
        raw_bat = service.get_uncapped_batting_leaderboard(limit=limit, qualified_only=qualified_only)
        batting_items = [UncappedBattingItem(**item) for item in raw_bat]

    bowling_items = None
    if disc_norm in ["all", "bowling"]:
        raw_bowl = service.get_uncapped_bowling_leaderboard(limit=limit, qualified_only=qualified_only)
        bowling_items = [UncappedBowlingItem(**item) for item in raw_bowl]

    return UncappedLeaderboardResponse(
        discipline_filter=disc_norm,
        qualified_only=qualified_only,
        batting_count=len(batting_items) if batting_items else 0,
        bowling_count=len(bowling_items) if bowling_items else 0,
        batting_leaderboard=batting_items,
        bowling_leaderboard=bowling_items,
        sample_gate=">= 60 pressure deliveries (or >= 50 balls & 10 matches)",
        governing_statute="BCCI IPL Player Regulations 2025/2026",
        audit_date="2026-11-16",
    )


@router.get(
    "/eligibility/{player_id}",
    summary="Player Uncapped Eligibility Audit",
    description="Returns detailed BCCI eligibility audit for a specific player ID.",
)
def get_player_eligibility(
    player_id: int,
    player_name: str = Query("", description="Optional player name for fuzzy matching"),
    service: UncappedPressureIntelligenceService = Depends(get_uncapped_service),
):
    try:
        return service.check_eligibility(player_id, player_name)
    except Exception as exc:
        logger.error(f"Failed to check eligibility for player {player_id}: {exc}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to verify eligibility for player {player_id}.",
        )
