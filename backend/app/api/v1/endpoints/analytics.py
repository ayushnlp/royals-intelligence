"""
Royals Intelligence - Uncapped Analytics API Endpoints
Provides batting and bowling career aggregates, phase breakdowns (Powerplay, Middle, Death),
and recent-form window queries.
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.analytics.uncapped_analytics_service import (
    UncappedAnalyticsService,
    BattingAggregates,
    BowlingAggregates,
    RecentFormWindow,
    PhaseMetrics,
)
from app.core.logging import logger

router = APIRouter()

# Fallback analytics seeds for cold/offline DB
MOCK_BATTING_AGGREGATES = {
    "uncapped_rr_01": BattingAggregates(
        player_id="uncapped_rr_01",
        innings_count=14,
        runs=354,
        balls_faced=215,
        fours=28,
        sixes=21,
        strike_rate=164.65,
        batting_average=44.25,
        dismissals=8,
        dot_balls=62,
        dot_ball_percentage=28.84,
        boundary_percentage=67.23,
        high_score=68,
        phase_splits={
            "Powerplay": PhaseMetrics(phase="Powerplay", runs=42, balls=32, strike_rate=131.25),
            "Middle": PhaseMetrics(phase="Middle", runs=112, balls=78, strike_rate=143.59),
            "Death": PhaseMetrics(phase="Death", runs=200, balls=105, strike_rate=190.48),
        }
    ),
    "uncapped_rr_04": BattingAggregates(
        player_id="uncapped_rr_04",
        innings_count=10,
        runs=410,
        balls_faced=230,
        fours=44,
        sixes=26,
        strike_rate=178.26,
        batting_average=41.0,
        dismissals=10,
        dot_balls=75,
        dot_ball_percentage=32.61,
        boundary_percentage=80.98,
        high_score=120,
        phase_splits={
            "Powerplay": PhaseMetrics(phase="Powerplay", runs=260, balls=138, strike_rate=188.41),
            "Middle": PhaseMetrics(phase="Middle", runs=125, balls=78, strike_rate=160.26),
            "Death": PhaseMetrics(phase="Death", runs=25, balls=14, strike_rate=178.57),
        }
    ),
}

MOCK_BOWLING_AGGREGATES = {
    "uncapped_rr_03": BowlingAggregates(
        player_id="uncapped_rr_03",
        innings_count=13,
        overs=48.2,
        legal_balls=290,
        runs_conceded=435,
        wickets=19,
        economy_rate=9.0,
        bowling_average=22.89,
        bowling_strike_rate=15.26,
        dot_balls=112,
        dot_ball_percentage=38.62,
        phase_splits={
            "Powerplay": PhaseMetrics(phase="Powerplay", runs=145, balls=108, wickets=6, economy_rate=8.06),
            "Middle": PhaseMetrics(phase="Middle", runs=90, balls=60, wickets=4, economy_rate=9.0),
            "Death": PhaseMetrics(phase="Death", runs=200, balls=122, wickets=9, economy_rate=9.84),
        }
    )
}


@router.get("/players/{player_id}/batting", response_model=BattingAggregates, summary="Player Batting Career & Phase Aggregates")
async def get_player_batting(
    player_id: str,
    competition_id: Optional[str] = Query(None, description="Filter by competition (e.g. smat, ipl)"),
    season_id: Optional[str] = Query(None, description="Filter by season (e.g. 2024, 2025)"),
    db: Optional[AsyncSession] = Depends(get_db),
):
    """Calculates batting totals, averages, strike rates, dot %, boundary %, and Powerplay/Middle/Death splits."""
    try:
        if db:
            aggs = await UncappedAnalyticsService.get_player_batting_aggregates(
                session=db,
                player_id=player_id,
                competition_id=competition_id,
                season_id=season_id,
            )
            if aggs.innings_count > 0:
                return aggs
    except Exception as exc:
        logger.warning(f"Database batting aggregate calculation failed: {exc}")

    # Fallback to mock
    if player_id in MOCK_BATTING_AGGREGATES:
        return MOCK_BATTING_AGGREGATES[player_id]

    # Return clean empty aggregates
    return BattingAggregates(player_id=player_id)


@router.get("/players/{player_id}/bowling", response_model=BowlingAggregates, summary="Player Bowling Career & Phase Aggregates")
async def get_player_bowling(
    player_id: str,
    competition_id: Optional[str] = Query(None, description="Filter by competition"),
    season_id: Optional[str] = Query(None, description="Filter by season"),
    db: Optional[AsyncSession] = Depends(get_db),
):
    """Calculates bowling totals, economy rate, bowling average, bowling strike rate, and phase splits."""
    try:
        if db:
            aggs = await UncappedAnalyticsService.get_player_bowling_aggregates(
                session=db,
                player_id=player_id,
                competition_id=competition_id,
                season_id=season_id,
            )
            if aggs.innings_count > 0:
                return aggs
    except Exception as exc:
        logger.warning(f"Database bowling aggregate calculation failed: {exc}")

    if player_id in MOCK_BOWLING_AGGREGATES:
        return MOCK_BOWLING_AGGREGATES[player_id]

    return BowlingAggregates(player_id=player_id)


@router.get("/players/{player_id}/recent-form", response_model=RecentFormWindow, summary="Player Recent Form Window")
async def get_player_recent_form(
    player_id: str,
    last_n: int = Query(5, ge=1, le=20, description="Window size (number of recent innings)"),
    discipline: str = Query("batting", description="'batting' or 'bowling'"),
    db: Optional[AsyncSession] = Depends(get_db),
):
    """Chronological recent form tracker across recent domestic fixtures."""
    try:
        if db:
            return await UncappedAnalyticsService.get_recent_form(
                session=db,
                player_id=player_id,
                last_n=last_n,
                discipline=discipline,
            )
    except Exception as exc:
        logger.warning(f"Recent form DB query failed: {exc}")

    # Fallback response
    return RecentFormWindow(
        player_id=player_id,
        window_size=last_n,
        innings_evaluated=0,
        aggregate_metric_summary=f"No recent {discipline} match scorecards recorded in current window."
    )
