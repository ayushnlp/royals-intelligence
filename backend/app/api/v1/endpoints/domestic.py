"""
Royals Intelligence - Domestic Season & Match Intelligence API Endpoints
Provides high-performance endpoints for domestic tournament directories,
season matches, detailed scorecards, fall of wickets, partnerships,
phase summaries, and uncapped player domestic performance tracking.
Strict Scope: UNCAPPED PLAYERS ONLY.
"""

from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.services.domestic.domestic_match_service import DomesticMatchService
from app.services.domestic.domestic_season_service import DomesticSeasonService
from app.schemas.domestic_api import (
    CompetitionSeasonSummary,
    MatchSummaryItem,
    MatchScorecardResponse,
    InningsAnalysisResponse,
    PlayerDomesticSeasonStats,
    PlayerMatchHistoryItem,
    PlayerPhaseSplitDetail,
    AllRoundContributionResponse,
    DomesticPlayerSummary,
    PaginatedDomesticPlayersResponse,
)
from app.core.logging import logger

router = APIRouter()


@router.get("/players", response_model=PaginatedDomesticPlayersResponse, summary="Dynamic Uncapped Player Discovery & Directory")
async def list_domestic_players(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=500, description="Items per page"),
    search: Optional[str] = Query(None, description="Search by player name or key"),
    eligibility_status: Optional[str] = Query("ALL", description="Filter by eligibility state: VERIFIED_UNCAPPED, PENDING_VERIFICATION, VERIFIED_CAPPED, ALL"),
    role: Optional[str] = Query(None, description="Filter by role (Batter, Bowler, All-rounder, Wicketkeeper-Batter)"),
    team: Optional[str] = Query(None, description="Filter by team or franchise"),
    competition: Optional[str] = Query(None, description="Filter by competition"),
    season: Optional[str] = Query(None, description="Filter by season"),
    db: Optional[AsyncSession] = Depends(get_db),
):
    """
    Discovers all eligible uncapped and domestic Indian player candidates with canonical identity,
    audited eligibility state, match counts, and statistical coverage flags.
    Strict Scope: Indian domestic prospects with verified uncapped or pending status.
    """
    items, total = await DomesticSeasonService.list_domestic_players(
        session=db,
        page=page,
        page_size=page_size,
        search=search,
        eligibility_status=eligibility_status,
        role=role,
        team=team,
        competition=competition,
        season=season,
    )
    total_pages = (total + page_size - 1) // page_size if total > 0 else 1
    return PaginatedDomesticPlayersResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        filters_applied={
            "search": search,
            "eligibility_status": eligibility_status,
            "role": role,
            "team": team,
            "competition": competition,
            "season": season,
        }
    )



@router.get("/competitions", response_model=List[CompetitionSeasonSummary], summary="Directory of Domestic Competitions & Seasons")
async def list_domestic_competitions(
    db: Optional[AsyncSession] = Depends(get_db),
):
    """
    Returns available domestic cricket tournaments (SMAT, VHT, Ranji, DPL, UP T20)
    with format specifications, match counts, coverage, and provenance tracking.
    """
    return await DomesticSeasonService.list_competitions(db)


@router.get("/seasons/{competition_id}/{season}/matches", response_model=Dict[str, Any], summary="List Season Matches with Filtering & Pagination")
async def list_season_matches(
    competition_id: str,
    season: str,
    team_code: Optional[str] = Query(None, description="Filter by team code (e.g. DEL, PUN, MP, RAJ)"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    db: Optional[AsyncSession] = Depends(get_db),
):
    """
    Retrieves season match listings with scores, venues, outcomes, and ball-by-ball availability flags.
    """
    matches, total = await DomesticSeasonService.list_season_matches(
        session=db,
        competition_id=competition_id.lower(),
        season=season,
        team_code=team_code,
        page=page,
        page_size=page_size,
    )
    return {
        "competition_id": competition_id,
        "season": season,
        "page": page,
        "page_size": page_size,
        "total_matches": total,
        "total_pages": (total + page_size - 1) // page_size if total > 0 else 1,
        "matches": matches,
    }


@router.get("/seasons/{competition_id}/{season}/summary", response_model=Dict[str, Any], summary="Get Domestic Season Overview & Standings")
async def get_season_summary(
    competition_id: str,
    season: str,
    db: Optional[AsyncSession] = Depends(get_db),
):
    """
    Returns domestic season aggregate telemetry: participating teams, standings,
    run-rate benchmarks, and data quality metrics.
    """
    return await DomesticSeasonService.get_season_summary(db, competition_id.lower(), season)


@router.get("/matches/{match_id}", response_model=MatchScorecardResponse, summary="Get Full Match Scorecard & Context")
async def get_match_detail(
    match_id: str,
    db: Optional[AsyncSession] = Depends(get_db),
):
    """
    Retrieves full match scorecard including team details, venue, toss,
    batting & bowling scorecards, fall of wickets, partnerships, and phase metrics.
    """
    match_resp = await DomesticMatchService.get_match_detail(db, match_id)
    if not match_resp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Match '{match_id}' not found in domestic match records."
        )
    return match_resp


@router.get("/matches/{match_id}/innings/{innings_number}", response_model=InningsAnalysisResponse, summary="Deep Innings Breakdown & Progression")
async def get_innings_analysis(
    match_id: str,
    innings_number: int,
    db: Optional[AsyncSession] = Depends(get_db),
):
    """
    Retrieves detailed breakdown of a single innings:
    Batting & bowling scorecards, fall of wickets (FoW), partnerships, phase summaries,
    and cumulative over progression (worm telemetry).
    """
    if innings_number not in [1, 2, 3, 4]:
        raise HTTPException(status_code=400, detail="Innings number must be between 1 and 4.")

    inn_resp = await DomesticMatchService.get_innings_analysis(db, match_id, innings_number)
    if not inn_resp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Innings {innings_number} for match '{match_id}' not found."
        )
    return inn_resp


@router.get("/players/{player_id}/season-stats", response_model=List[PlayerDomesticSeasonStats], summary="Player Domestic Season Statistics")
async def get_player_domestic_season_stats(
    player_id: str,
    competition_id: Optional[str] = Query(None, description="Filter by competition (e.g. smat, vht, ranji, dpl)"),
    db: Optional[AsyncSession] = Depends(get_db),
):
    """
    Calculates season batting and bowling statistics for an uncapped cricketer.
    Strictly restricted to UNCAPPED PLAYERS ONLY.
    """
    try:
        return await DomesticSeasonService.get_player_season_stats(
            session=db,
            player_id=player_id,
            competition_id=competition_id.lower() if competition_id else None,
        )
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc))


@router.get("/players/{player_id}/match-history", response_model=Dict[str, Any], summary="Player Chronological Domestic Match History")
async def get_player_match_history(
    player_id: str,
    competition_id: Optional[str] = Query(None, description="Filter by competition"),
    season: Optional[str] = Query(None, description="Filter by season (e.g. 2024)"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=50, description="Items per page"),
    db: Optional[AsyncSession] = Depends(get_db),
):
    """
    Retrieves chronological domestic match appearances for an uncapped cricketer
    showing opponent, venue, and both batting and bowling performance in each match.
    """
    try:
        history, total = await DomesticSeasonService.get_player_match_history(
            session=db,
            player_id=player_id,
            competition_id=competition_id.lower() if competition_id else None,
            season=season,
            page=page,
            page_size=page_size,
        )
        return {
            "player_id": player_id,
            "page": page,
            "page_size": page_size,
            "total_matches": total,
            "total_pages": (total + page_size - 1) // page_size if total > 0 else 1,
            "matches": history,
        }
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc))


@router.get("/players/{player_id}/phase-splits", response_model=List[PlayerPhaseSplitDetail], summary="Player Powerplay, Middle, Death Phase Splits")
async def get_player_phase_splits(
    player_id: str,
    competition_id: Optional[str] = Query(None, description="Filter by competition (e.g. smat)"),
    db: Optional[AsyncSession] = Depends(get_db),
):
    """
    Provides granular phase-by-phase breakdown (Powerplay, Middle, Death)
    for batting strike rates, dot percentages, and bowling economy.
    """
    try:
        return await DomesticSeasonService.get_player_phase_splits(
            session=db,
            player_id=player_id,
            competition_id=competition_id.lower() if competition_id else None,
        )
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc))


@router.get("/players/{player_id}/all-round-summary", response_model=AllRoundContributionResponse, summary="All-Round Contribution Profile (Separate Disciplines)")
async def get_player_all_round_contribution(
    player_id: str,
    db: Optional[AsyncSession] = Depends(get_db),
):
    """
    Produces transparent dual-contribution analysis for uncapped cricketers.
    Strictly avoids arbitrary composite scores; reports batting, bowling, and fielding components separately.
    """
    try:
        return await DomesticSeasonService.get_player_all_round_contribution(
            session=db,
            player_id=player_id,
        )
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc))


