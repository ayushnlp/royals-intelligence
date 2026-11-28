"""
Royals Intelligence - Pressure Analytics REST API Endpoints
Serves official Round 1 Pressure Analytics: Top 10 Batters, Top 10 Bowlers,
Candidate Evidence Profiles, and Bayesian Reliability Diagnostics.
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.analytics.pressure_intelligence import PressureIntelligenceEngine
from app.schemas.pressure import (
    PressureOverviewResponse,
    PressureLeaderboardResponse,
    PressureLeaderboardBattingItem,
    PressureLeaderboardBowlingItem,
    CandidateEvidenceProfileResponse,
    CandidateEvidenceQuestions,
    PressureMethodologyResponse,
)
from app.core.logging import logger

router = APIRouter()

# Singleton cache for pressure intelligence engine
_engine: Optional[PressureIntelligenceEngine] = None


def get_pressure_engine() -> PressureIntelligenceEngine:
    """Dependency provider returning singleton instance of PressureIntelligenceEngine."""
    global _engine
    if _engine is None:
        logger.info("Initializing PressureIntelligenceEngine...")
        engine = PressureIntelligenceEngine()
        try:
            engine.load_data()
        except FileNotFoundError as exc:
            logger.error(f"Pressure Intelligence unavailable due to missing dataset assets: {exc}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Pressure Intelligence datasets offline or unmounted. Verify runtime assets in DATA_DIR: {exc}",
            )
        _engine = engine
        logger.info("PressureIntelligenceEngine initialized successfully.")
    return _engine


# ---------------------------------------------------------------------------
# 1. Round 1 Pressure Overview
# ---------------------------------------------------------------------------

@router.get(
    "/overview",
    response_model=PressureOverviewResponse,
    summary="Round 1 Pressure Challenge Overview",
    description="Returns global volume metrics, strict vs permissive coverage, and death overs concentration.",
)
def get_pressure_overview(
    engine: PressureIntelligenceEngine = Depends(get_pressure_engine),
) -> PressureOverviewResponse:
    try:
        data = engine.get_overview()
        return PressureOverviewResponse(**data)
    except Exception as exc:
        logger.error(f"Failed to generate pressure overview: {exc}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve pressure overview parameters.",
        )


# ---------------------------------------------------------------------------
# 2. Official Batting & Bowling Leaderboards
# ---------------------------------------------------------------------------

@router.get(
    "/leaderboards",
    response_model=PressureLeaderboardResponse,
    summary="Official Round 1 Pressure Leaderboards",
    description="Returns sealed Top 10 Batters and Top 10 Bowlers Under Pressure with Conservative PRI and Bayesian credible regions.",
)
def get_pressure_leaderboards(
    discipline: str = Query("all", description="'all', 'batting', or 'bowling'"),
    limit: int = Query(10, ge=1, le=50, description="Number of ranked candidates to return"),
    qualified_only: bool = Query(True, description="Filter for sample-qualified candidates only"),
    engine: PressureIntelligenceEngine = Depends(get_pressure_engine),
) -> PressureLeaderboardResponse:
    disc_norm = discipline.lower()
    if disc_norm not in ["all", "batting", "bowling"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid discipline '{discipline}'. Must be 'all', 'batting', or 'bowling'.",
        )

    batting_items = None
    if disc_norm in ["all", "batting"]:
        raw_bat = engine.get_batting_leaderboard(limit=limit, qualified_only=qualified_only)
        batting_items = [PressureLeaderboardBattingItem(**item) for item in raw_bat]

    bowling_items = None
    if disc_norm in ["all", "bowling"]:
        raw_bowl = engine.get_bowling_leaderboard(limit=limit, qualified_only=qualified_only)
        bowling_items = [PressureLeaderboardBowlingItem(**item) for item in raw_bowl]

    return PressureLeaderboardResponse(
        discipline_filter=disc_norm,
        qualified_only=qualified_only,
        batting_count=len(batting_items) if batting_items else 0,
        bowling_count=len(bowling_items) if bowling_items else 0,
        batting_leaderboard=batting_items,
        bowling_leaderboard=bowling_items,
    )


# ---------------------------------------------------------------------------
# 3. Individual Candidate Evidence Profile
# ---------------------------------------------------------------------------

@router.get(
    "/candidates/{player_id}",
    response_model=CandidateEvidenceProfileResponse,
    summary="Candidate Evidence Dossier",
    description="Extracts the candidate evidence profile and answers to the 11 methodology questions.",
)
def get_candidate_profile(
    player_id: int,
    discipline: Optional[str] = Query(None, description="Optional 'batting' or 'bowling'"),
    engine: PressureIntelligenceEngine = Depends(get_pressure_engine),
) -> CandidateEvidenceProfileResponse:
    if discipline and discipline.lower() not in ["batting", "bowling"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid discipline '{discipline}'. Must be 'batting' or 'bowling'.",
        )

    data = engine.get_candidate_profile(player_id=player_id, discipline=discipline.lower() if discipline else None)
    if data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No candidate evidence profile found for player ID {player_id}.",
        )

    q_data = data["evidence_questions"]
    questions_obj = CandidateEvidenceQuestions(**q_data)

    return CandidateEvidenceProfileResponse(
        player_id=data["player_id"],
        player_name=data["player_name"],
        discipline=data["discipline"],
        rank=data["rank"],
        governing_metric_name=data["governing_metric_name"],
        governing_metric_value=data["governing_metric_value"],
        posterior_mean=data["posterior_mean"],
        posterior_se=data["posterior_se"],
        ci_95_lower=data["ci_95_lower"],
        ci_95_upper=data["ci_95_upper"],
        ci_95_width=data["ci_95_width"],
        shrinkage_weight=data["shrinkage_weight"],
        pressure_legal_balls=data["pressure_legal_balls"],
        pressure_matches=data["pressure_matches"],
        ipl_legal_balls=data["ipl_legal_balls"],
        t20i_legal_balls=data["t20i_legal_balls"],
        competition_qualification=data["competition_qualification"],
        two_dimensional_classification=data["two_dimensional_classification"],
        evidence_classification=data["evidence_classification"],
        uncertainty_level=data["uncertainty_level"],
        evidence_questions=questions_obj,
    )


# ---------------------------------------------------------------------------
# 4. Methodology & Baseline Strata
# ---------------------------------------------------------------------------

@router.get(
    "/methodology",
    response_model=PressureMethodologyResponse,
    summary="Methodology & Model Specifications",
    description="Returns formulas for the 12-cell baseline matrix, empirical Bayes shrinkage, and Conservative PRI.",
)
def get_pressure_methodology(
    engine: PressureIntelligenceEngine = Depends(get_pressure_engine),
) -> PressureMethodologyResponse:
    data = engine.get_methodology()
    return PressureMethodologyResponse(**data)
