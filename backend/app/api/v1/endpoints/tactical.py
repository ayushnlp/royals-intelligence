"""
Royals Intelligence - Tactical Analytics REST API Endpoints
Stage 5 Core Tactical Analytics Service Router

Exposes official dataset-driven tactical capabilities:
- Phase-wise batting & bowling performance (Powerplay, Middle, Death)
- Shot stroke efficiency and dismissal risk (30 stroke categories)
- Handedness matchup matrices (RHB/LHB vs Pace/Spin)
- Bowling delivery variation and movement effectiveness (34 styles)
- Radar delivery release speed profiles with sensor quality safeguards
- Multi-dimensional player tactical profiles
- Death-overs finishers & containment rankings
- Direct head-to-head micro-battles
"""

from datetime import datetime, timezone
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.analytics.dataset_cricket_intelligence import (
    DatasetCricketIntelligenceEngine,
    TacticalPhaseSplit,
)
from app.schemas.tactical import (
    TacticalDatasetSummaryResponse,
    TacticalPhaseResponse,
    TacticalPhaseSplitItem,
    TacticalStrokesResponse,
    TacticalStrokeItem,
    HandednessMatrixResponse,
    HandednessSplitItem,
    DeliveryStylesResponse,
    DeliveryStyleItem,
    SpeedProfileResponse,
    SpeedBrackets,
    FastestBowlerItem,
    PlayerTacticalProfileResponse,
    DeathOversRankingResponse,
    DeathOverPerformerBattingItem,
    DeathOverPerformerBowlingItem,
    HeadToHeadMatchupResponse,
    PlayerLookupItem,
)
from app.core.logging import logger

router = APIRouter()

# Singleton cache for intelligence engine
_engine: Optional[DatasetCricketIntelligenceEngine] = None


def get_engine() -> DatasetCricketIntelligenceEngine:
    """Dependency provider returning singleton instance of DatasetCricketIntelligenceEngine."""
    global _engine
    if _engine is None:
        logger.info("Initializing DatasetCricketIntelligenceEngine for Tactical API...")
        _engine = DatasetCricketIntelligenceEngine()
        _engine.load_data()
        logger.info("DatasetCricketIntelligenceEngine loaded successfully.")
    return _engine


# ---------------------------------------------------------------------------
# 1. Dataset Tactical Summary
# ---------------------------------------------------------------------------

@router.get(
    "/summary",
    response_model=TacticalDatasetSummaryResponse,
    summary="Tactical Dataset Pack Summary",
    description="Returns aggregate metrics and empirical volume counts for the official Rajasthan Royals dataset.",
)
def get_dataset_tactical_summary(
    engine: DatasetCricketIntelligenceEngine = Depends(get_engine),
) -> TacticalDatasetSummaryResponse:
    try:
        summary = engine.get_dataset_summary()
        return TacticalDatasetSummaryResponse(
            total_deliveries=summary["total_deliveries"],
            legal_deliveries=summary["legal_deliveries"],
            total_matches_with_deliveries=summary["total_matches_with_deliveries"],
            total_unique_strikers=summary["total_unique_strikers"],
            total_unique_bowlers=summary["total_unique_bowlers"],
            total_runs_off_bat=summary["total_runs_off_bat"],
            total_wickets_fallen=summary["total_wickets_fallen"],
            total_bowler_wickets=summary["total_bowler_wickets"],
            overall_run_rate_per_6_balls=summary["overall_run_rate_per_6_balls"],
            valid_radar_speed_records=summary["valid_radar_speed_records"],
            data_provenance=summary.get("data_provenance", "Official Rajasthan Royals Round 1 Data Pack"),
            generated_at=datetime.now(timezone.utc).isoformat(),
        )
    except Exception as exc:
        logger.error(f"Failed to generate dataset summary: {exc}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate tactical dataset summary.",
        )


# ---------------------------------------------------------------------------
# 2. Phase-wise Performance (Powerplay, Middle, Death)
# ---------------------------------------------------------------------------

@router.get(
    "/phases",
    response_model=TacticalPhaseResponse,
    summary="Phase-wise Batting & Bowling Splits",
    description="Returns Powerplay (overs 1-6), Middle (7-15), and Death (16-20) metrics overall or for an individual player.",
)
def get_phase_performance(
    striker_id: Optional[int] = Query(None, description="Optional batter player ID"),
    bowler_id: Optional[int] = Query(None, description="Optional bowler player ID"),
    phase: Optional[str] = Query(None, description="Filter for specific phase: 'Powerplay', 'Middle', or 'Death'"),
    engine: DatasetCricketIntelligenceEngine = Depends(get_engine),
) -> TacticalPhaseResponse:
    if striker_id is not None and bowler_id is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot filter by both striker_id and bowler_id simultaneously in phase splits.",
        )

    if phase and phase not in ["Powerplay", "Middle", "Death"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid phase '{phase}'. Must be 'Powerplay', 'Middle', or 'Death'.",
        )

    striker_name = None
    if striker_id is not None:
        if not engine.is_known_player(striker_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Batter ID {striker_id} not found in official dataset.",
            )
        striker_name = engine.get_player_name(striker_id)

    bowler_name = None
    if bowler_id is not None:
        if not engine.is_known_player(bowler_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Bowler ID {bowler_id} not found in official dataset.",
            )
        bowler_name = engine.get_player_name(bowler_id)

    raw_splits = engine.get_phase_splits(striker_id=striker_id, bowler_id=bowler_id, phase=phase)

    phase_items: dict[str, TacticalPhaseSplitItem] = {}
    for p_name, p_data in raw_splits.items():
        phase_items[p_name] = TacticalPhaseSplitItem(
            phase=p_data.phase,
            total_balls=p_data.total_balls,
            legal_balls=p_data.legal_balls,
            runs=p_data.runs,
            wickets=p_data.wickets,
            strike_rate=p_data.strike_rate,
            economy_rate=p_data.economy_rate,
            average=p_data.average,
            dot_ball_percentage=p_data.dot_ball_percentage,
            boundary_percentage=p_data.boundary_percentage,
            balls_per_wicket=p_data.balls_per_wicket,
        )

    return TacticalPhaseResponse(
        striker_id=striker_id,
        striker_name=striker_name,
        bowler_id=bowler_id,
        bowler_name=bowler_name,
        phases=phase_items,
    )


# ---------------------------------------------------------------------------
# 3. Stroke-wise Batting Efficiency
# ---------------------------------------------------------------------------

@router.get(
    "/strokes",
    response_model=TacticalStrokesResponse,
    summary="Stroke-wise Batting Efficiency & Dismissal Risk",
    description="Evaluates tactical productivity and wicket threat across all 30 shot stroke categories.",
)
def get_stroke_efficiency(
    striker_id: Optional[int] = Query(None, description="Optional batter player ID to profile"),
    stroke: Optional[str] = Query(None, description="Optional specific stroke type to query"),
    min_balls: int = Query(50, ge=1, le=10000, description="Minimum deliveries faced qualification threshold"),
    engine: DatasetCricketIntelligenceEngine = Depends(get_engine),
) -> TacticalStrokesResponse:
    striker_name = None
    if striker_id is not None:
        if not engine.is_known_player(striker_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Batter ID {striker_id} not found in official dataset.",
            )
        striker_name = engine.get_player_name(striker_id)
        # Use lower threshold for individual player queries if not explicitly increased
        if min_balls == 50:
            min_balls = 1

    strokes = engine.get_top_strokes(min_balls=min_balls, striker_id=striker_id, stroke_name=stroke)

    items = [
        TacticalStrokeItem(
            stroke=s.stroke,
            deliveries_faced=s.deliveries_faced,
            runs_scored=s.runs_scored,
            dismissals=s.dismissals,
            runs_per_shot=s.runs_per_shot,
            dismissal_rate_pct=s.dismissal_rate_pct,
            boundary_pct=s.boundary_pct,
        )
        for s in strokes
    ]

    return TacticalStrokesResponse(
        striker_id=striker_id,
        striker_name=striker_name,
        total_strokes_analyzed=len(items),
        strokes=items,
    )


# ---------------------------------------------------------------------------
# 4. Batter Handedness vs Bowling Style Matrix
# ---------------------------------------------------------------------------

@router.get(
    "/handedness",
    response_model=HandednessMatrixResponse,
    summary="Handedness Matchup Matrix (RHB/LHB vs Pace/Spin)",
    description="Cross-references batter handedness against pace/spin bowling disciplines.",
)
def get_handedness_matrix(
    batting_type: Optional[str] = Query(None, description="'RHB' or 'LHB'"),
    pace_or_spin: Optional[str] = Query(None, description="'Pace' or 'Spin'"),
    striker_id: Optional[int] = Query(None, description="Optional batter player ID"),
    bowler_id: Optional[int] = Query(None, description="Optional bowler player ID"),
    engine: DatasetCricketIntelligenceEngine = Depends(get_engine),
) -> HandednessMatrixResponse:
    if batting_type and batting_type.upper() not in ["RHB", "LHB"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid batting_type '{batting_type}'. Must be 'RHB' or 'LHB'.",
        )

    if pace_or_spin and pace_or_spin.capitalize() not in ["Pace", "Spin"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid pace_or_spin '{pace_or_spin}'. Must be 'Pace' or 'Spin'.",
        )

    striker_name = None
    if striker_id is not None:
        if not engine.is_known_player(striker_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Batter ID {striker_id} not found in official dataset.",
            )
        striker_name = engine.get_player_name(striker_id)

    bowler_name = None
    if bowler_id is not None:
        if not engine.is_known_player(bowler_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Bowler ID {bowler_id} not found in official dataset.",
            )
        bowler_name = engine.get_player_name(bowler_id)

    btype_norm = batting_type.upper() if batting_type else None
    ps_norm = pace_or_spin.capitalize() if pace_or_spin else None

    matrix = engine.get_handedness_matrix(
        striker_id=striker_id,
        bowler_id=bowler_id,
        batting_type=btype_norm,
        pace_or_spin=ps_norm,
    )

    items = [
        HandednessSplitItem(
            batting_type=m.batting_type,
            pace_or_spin=m.pace_or_spin,
            balls_faced=m.balls_faced,
            runs_scored=m.runs_scored,
            wickets=m.wickets,
            strike_rate=m.strike_rate,
            economy_rate=m.economy_rate,
            bowling_average=m.bowling_average,
            boundary_pct=m.boundary_pct,
            dot_pct=m.dot_pct,
        )
        for m in matrix
    ]

    return HandednessMatrixResponse(
        striker_id=striker_id,
        striker_name=striker_name,
        bowler_id=bowler_id,
        bowler_name=bowler_name,
        matrix=items,
    )


# ---------------------------------------------------------------------------
# 5. Delivery Variation & Style Effectiveness
# ---------------------------------------------------------------------------

@router.get(
    "/variations",
    response_model=DeliveryStylesResponse,
    summary="Bowling Delivery Variation Effectiveness",
    description="Profiles economy and wicket-taking threat across 34 bowling delivery styles and seam/spin variations.",
)
def get_delivery_variations(
    bowler_id: Optional[int] = Query(None, description="Optional bowler player ID to profile"),
    delivery_style: Optional[str] = Query(None, description="Optional delivery style filter"),
    min_balls: int = Query(50, ge=1, le=10000, description="Minimum legal deliveries bowled qualification"),
    engine: DatasetCricketIntelligenceEngine = Depends(get_engine),
) -> DeliveryStylesResponse:
    bowler_name = None
    if bowler_id is not None:
        if not engine.is_known_player(bowler_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Bowler ID {bowler_id} not found in official dataset.",
            )
        bowler_name = engine.get_player_name(bowler_id)
        if min_balls == 50:
            min_balls = 1

    styles = engine.get_top_delivery_styles(
        min_balls=min_balls,
        bowler_id=bowler_id,
        delivery_style_name=delivery_style,
    )

    items = [
        DeliveryStyleItem(
            delivery_style=s.delivery_style,
            deliveries_bowled=s.deliveries_bowled,
            runs_conceded=s.runs_conceded,
            wickets=s.wickets,
            dot_balls=s.dot_balls,
            economy_rate=s.economy_rate,
            bowling_average=s.bowling_average,
            dot_ball_pct=s.dot_ball_pct,
        )
        for s in styles
    ]

    return DeliveryStylesResponse(
        bowler_id=bowler_id,
        bowler_name=bowler_name,
        total_styles_analyzed=len(items),
        styles=items,
    )


# ---------------------------------------------------------------------------
# 6. Bowling Release Speed Profiles
# ---------------------------------------------------------------------------

@router.get(
    "/speed-profiles",
    response_model=SpeedProfileResponse,
    summary="Bowling Speed Profiles & Radar Sensor Safeguards",
    description="Extracts radar release velocity with sensor calibration safeguards, express pace counts, and speed distributions.",
)
def get_speed_profiles(
    bowler_id: Optional[int] = Query(None, description="Optional bowler player ID"),
    min_balls: int = Query(30, ge=1, le=5000, description="Minimum valid radar deliveries for qualification"),
    top_n: int = Query(10, ge=1, le=50, description="Number of fastest bowlers to return"),
    engine: DatasetCricketIntelligenceEngine = Depends(get_engine),
) -> SpeedProfileResponse:
    if bowler_id is not None and not engine.is_known_player(bowler_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Bowler ID {bowler_id} not found in official dataset.",
        )

    data = engine.get_bowling_speed_profile(bowler_id=bowler_id, min_balls=min_balls, top_n=top_n)

    brackets_obj = None
    if "speed_brackets" in data and data["speed_brackets"]:
        brackets_obj = SpeedBrackets(**data["speed_brackets"])

    top_fastest = None
    if "top_fastest_bowlers" in data and data["top_fastest_bowlers"]:
        top_fastest = [FastestBowlerItem(**b) for b in data["top_fastest_bowlers"]]

    return SpeedProfileResponse(
        bowler_id=data.get("bowler_id"),
        bowler_name=data.get("bowler_name"),
        total_deliveries=data.get("total_deliveries"),
        overall_valid_speed_deliveries=data.get("overall_valid_speed_deliveries"),
        valid_speed_deliveries=data.get("valid_speed_deliveries"),
        speed_coverage_pct=data["speed_coverage_pct"],
        mean_speed_kmh=data.get("mean_speed_kmh"),
        median_speed_kmh=data.get("median_speed_kmh"),
        min_speed_kmh=data.get("min_speed_kmh"),
        max_speed_kmh=data.get("max_speed_kmh"),
        std_speed_kmh=data.get("std_speed_kmh"),
        speed_brackets=brackets_obj,
        top_fastest_bowlers=top_fastest,
        sensor_safeguards_applied=data.get("sensor_safeguards_applied", True),
        data_quality_note=data.get("data_quality_note", "Governed sensor calibration applied."),
    )


# ---------------------------------------------------------------------------
# 7. Player Comprehensive Tactical Profile
# ---------------------------------------------------------------------------

@router.get(
    "/players/{player_id}",
    response_model=PlayerTacticalProfileResponse,
    summary="Player Multi-Dimensional Tactical Profile",
    description="Synthesizes batting and bowling phase splits, shot stroke breakdown, handedness matrix, and speed profile.",
)
def get_player_tactical_profile(
    player_id: int,
    engine: DatasetCricketIntelligenceEngine = Depends(get_engine),
) -> PlayerTacticalProfileResponse:
    if not engine.is_known_player(player_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Player ID {player_id} not found in official dataset.",
        )

    profile = engine.get_player_tactical_profile(player_id=player_id)
    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tactical profile could not be assembled for player ID {player_id}.",
        )

    return PlayerTacticalProfileResponse(
        player_id=profile["player_id"],
        player_name=profile["player_name"],
        is_batter=profile["is_batter"],
        is_bowler=profile["is_bowler"],
        batting_profile=profile["batting_profile"],
        bowling_profile=profile["bowling_profile"],
    )


# ---------------------------------------------------------------------------
# 8. Death Overs (16–20) Rankings
# ---------------------------------------------------------------------------

@router.get(
    "/death-overs",
    response_model=DeathOversRankingResponse,
    summary="Death Overs (16–20) Elite Rankings",
    description="Ranks elite death overs finishers by strike rate and death overs bowlers by containment economy.",
)
def get_death_overs_rankings(
    discipline: str = Query("all", description="'all', 'batting', or 'bowling'"),
    min_balls: int = Query(100, ge=1, le=5000, description="Minimum balls faced/bowled in overs 16-20"),
    limit: int = Query(10, ge=1, le=50, description="Maximum ranking entries to return"),
    engine: DatasetCricketIntelligenceEngine = Depends(get_engine),
) -> DeathOversRankingResponse:
    disc_norm = discipline.lower()
    if disc_norm not in ["all", "batting", "bowling"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid discipline '{discipline}'. Must be 'all', 'batting', or 'bowling'.",
        )

    batting_items = None
    if disc_norm in ["all", "batting"]:
        raw_bat = engine.get_top_death_batters(min_balls=min_balls, top_n=limit)
        batting_items = [
            DeathOverPerformerBattingItem(
                striker_id=int(r["striker_id"]),
                striker_name=str(r["striker_name"]),
                runs=int(r["runs"]),
                balls=int(r["balls"]),
                fours=int(r["fours"]),
                sixes=int(r["sixes"]),
                strike_rate=float(r["strike_rate"]),
                boundary_pct=float(r["boundary_pct"]),
                dot_pct=float(r["dot_pct"]),
            )
            for r in raw_bat
        ]

    bowling_items = None
    if disc_norm in ["all", "bowling"]:
        raw_bowl = engine.get_top_death_bowlers(min_balls=min_balls, top_n=limit)
        bowling_items = [
            DeathOverPerformerBowlingItem(
                bowler_id=int(r["bowler_id"]),
                bowler_name=str(r["bowler_name"]),
                bowling_type=str(r["bowling_type"]),
                legal_balls=int(r["legal_balls"]),
                runs=int(r["runs"]),
                wickets=int(r["wickets"]),
                economy=float(r["economy"]),
                average=float(r["average"]) if r["average"] is not None and not (isinstance(r["average"], float) and r["average"] != r["average"]) else None,
                dot_pct=float(r["dot_pct"]),
            )
            for r in raw_bowl
        ]

    return DeathOversRankingResponse(
        discipline=disc_norm,
        min_balls_threshold=min_balls,
        batting_finishers=batting_items,
        bowling_containment=bowling_items,
    )


# ---------------------------------------------------------------------------
# 9. Batter vs Bowler Head-to-Head Micro-Battles
# ---------------------------------------------------------------------------

@router.get(
    "/matchups",
    response_model=HeadToHeadMatchupResponse,
    summary="Head-to-Head Micro-Battle",
    description="Extracts direct historical head-to-head empirical metrics between a striker and bowler.",
)
def get_head_to_head_matchup(
    striker_id: int = Query(..., description="Striker batter player ID"),
    bowler_id: int = Query(..., description="Bowler player ID"),
    engine: DatasetCricketIntelligenceEngine = Depends(get_engine),
) -> HeadToHeadMatchupResponse:
    if not engine.is_known_player(striker_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Batter ID {striker_id} not found in official dataset.",
        )

    if not engine.is_known_player(bowler_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Bowler ID {bowler_id} not found in official dataset.",
        )

    h2h = engine.get_head_to_head(striker_id=striker_id, bowler_id=bowler_id)
    if h2h is None:
        striker_name = engine.get_player_name(striker_id) or "Unknown Batter"
        bowler_name = engine.get_player_name(bowler_id) or "Unknown Bowler"
        return HeadToHeadMatchupResponse(
            striker_id=striker_id,
            striker_name=striker_name,
            bowler_id=bowler_id,
            bowler_name=bowler_name,
            balls_faced=0,
            legal_balls=0,
            runs_scored=0,
            dismissals=0,
            fours=0,
            sixes=0,
            dot_balls=0,
            strike_rate=0.0,
            dot_ball_pct=0.0,
            boundary_pct=0.0,
        )

    return HeadToHeadMatchupResponse(
        striker_id=h2h.striker_id,
        striker_name=h2h.striker_name,
        bowler_id=h2h.bowler_id,
        bowler_name=h2h.bowler_name,
        balls_faced=h2h.balls_faced,
        legal_balls=h2h.legal_balls,
        runs_scored=h2h.runs_scored,
        dismissals=h2h.dismissals,
        fours=h2h.fours,
        sixes=h2h.sixes,
        dot_balls=h2h.dot_balls,
        strike_rate=h2h.strike_rate,
        dot_ball_pct=h2h.dot_ball_pct,
        boundary_pct=h2h.boundary_pct,
    )


# ---------------------------------------------------------------------------
# 10. Player Search & Autocomplete
# ---------------------------------------------------------------------------

@router.get(
    "/players",
    response_model=List[PlayerLookupItem],
    summary="Search Players in Official Dataset",
    description="Returns matching players with batter/bowler flags for interactive selectors and profiles.",
)
def search_players(
    query: str = Query("", description="Search term for player name"),
    limit: int = Query(25, ge=1, le=100, description="Maximum players to return"),
    engine: DatasetCricketIntelligenceEngine = Depends(get_engine),
) -> List[PlayerLookupItem]:
    raw_players = engine.search_players(query=query, limit=limit)
    return [PlayerLookupItem(**p) for p in raw_players]

