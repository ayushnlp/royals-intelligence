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
    min_balls: int = Query(60, ge=0, le=200, description="Minimum pressure deliveries threshold"),
    min_matches: int = Query(0, ge=0, le=100, description="Minimum pressure matches threshold (0 for All Matches)"),
    service: UncappedPressureIntelligenceService = Depends(get_uncapped_service),
) -> UncappedOverviewResponse:
    try:
        data = service.get_uncapped_overview(min_balls=min_balls, min_matches=min_matches)
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
    qualified_only: bool = Query(True, description="Filter for sample-qualified candidates (>= 60 balls default)"),
    min_balls: int = Query(60, ge=0, le=200, description="Minimum pressure deliveries threshold"),
    min_matches: int = Query(0, ge=0, le=100, description="Minimum pressure matches threshold (0 for All Matches)"),
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
        raw_bat = service.get_uncapped_batting_leaderboard(
            limit=limit,
            qualified_only=qualified_only,
            min_balls=min_balls,
            min_matches=min_matches,
        )
        batting_items = [UncappedBattingItem(**item) for item in raw_bat]

    bowling_items = None
    if disc_norm in ["all", "bowling"]:
        raw_bowl = service.get_uncapped_bowling_leaderboard(
            limit=limit,
            qualified_only=qualified_only,
            min_balls=min_balls,
            min_matches=min_matches,
        )
        bowling_items = [UncappedBowlingItem(**item) for item in raw_bowl]

    # Calculate talent pool and exclusions
    is_exploratory = bool(min_balls != 60 or min_matches > 0)
    all_bat = service.get_uncapped_batting_leaderboard(limit=500, qualified_only=False)
    all_bowl = service.get_uncapped_bowling_leaderboard(limit=500, qualified_only=False)

    if disc_norm == "batting":
        total_pool = len(all_bat)
        qualified_count = len(batting_items) if batting_items else 0
    elif disc_norm == "bowling":
        total_pool = len(all_bowl)
        qualified_count = len(bowling_items) if bowling_items else 0
    else:
        total_pool = len(all_bat) + len(all_bowl)
        qualified_count = (len(batting_items) if batting_items else 0) + (len(bowling_items) if bowling_items else 0)

    excluded_count = max(0, total_pool - qualified_count)

    if not is_exploratory:
        gate_desc = ">= 60 pressure deliveries (or >= 50 balls & 10 matches) [Official R1 Benchmark]"
    else:
        m_str = f" & >= {min_matches} matches" if min_matches > 0 else " & All Matches"
        gate_desc = f">= {min_balls} pressure deliveries{m_str} [Exploratory Scouting Filter]"

    return UncappedLeaderboardResponse(
        discipline_filter=disc_norm,
        qualified_only=qualified_only,
        batting_count=len(batting_items) if batting_items else 0,
        bowling_count=len(bowling_items) if bowling_items else 0,
        batting_leaderboard=batting_items,
        bowling_leaderboard=bowling_items,
        sample_gate=gate_desc,
        governing_statute="BCCI IPL Player Regulations 2025/2026",
        audit_date="2026-11-16",
        min_balls_applied=min_balls,
        min_matches_applied=min_matches,
        is_exploratory_filter=is_exploratory,
        excluded_count=excluded_count,
        total_pool_count=total_pool,
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
