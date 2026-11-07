"""
Royals Intelligence - Domestic Season & Match Intelligence API Schemas
Comprehensive Pydantic models for domestic competitions (SMAT, VHT, Ranji),
season listings, match scorecards, fall of wickets, partnerships, phase splits,
player match history, and non-composite all-round contribution profiles.
Strict Scope: UNCAPPED PLAYERS ONLY.
"""

from typing import List, Optional, Dict, Any
from datetime import date
from pydantic import BaseModel, Field


class CompetitionSeasonSummary(BaseModel):
    """Season overview for a domestic cricket competition."""
    competition_id: str
    competition_name: str
    competition_type: str  # 'T20', 'List A', 'First Class'
    governing_body: str = "BCCI"
    season: str
    is_domestic: bool = True
    match_count: int = 0
    teams_count: int = 0
    participating_teams: List[str] = Field(default_factory=list)
    has_ball_by_ball: bool = True
    validation_pass_rate: float = 100.0
    completeness_percentage: float = 100.0
    source_reference: str = "cricsheet_open / bcci"


class MatchSummaryItem(BaseModel):
    """High-level match item in a season fixture list."""
    match_id: str
    external_match_id: str
    competition_id: str
    season: str
    match_date: str
    match_number: Optional[int] = None
    home_team_code: str
    home_team_name: str
    away_team_code: str
    away_team_name: str
    venue_name: str
    venue_city: str
    winner_team_code: Optional[str] = None
    win_margin: Optional[str] = None
    result_outcome: str = "normal"
    has_ball_by_ball: bool = True


class BattingScorecardItem(BaseModel):
    """Granular batting performance row in a match scorecard."""
    player_id: str
    player_name: str
    is_uncapped: bool = True
    batting_position: int
    runs: int
    balls_faced: int
    fours: int = 0
    sixes: int = 0
    strike_rate: float = 0.0
    is_out: bool = True
    dismissal_kind: Optional[str] = None
    bowler_name: Optional[str] = None
    fielder_name: Optional[str] = None
    dot_balls: Optional[int] = None
    # Format-aware phase breakdown
    powerplay_runs: Optional[int] = 0
    powerplay_balls: Optional[int] = 0
    middle_runs: Optional[int] = 0
    middle_balls: Optional[int] = 0
    death_runs: Optional[int] = 0
    death_balls: Optional[int] = 0


class BowlingScorecardItem(BaseModel):
    """Granular bowling performance row in a match scorecard."""
    player_id: str
    player_name: str
    is_uncapped: bool = True
    overs: float
    legal_balls: int
    maidens: int = 0
    runs_conceded: int
    bowler_wickets: int = Field(..., description="Wickets credited to bowler. Excludes run-outs and retired hurt.")
    economy_rate: float
    dot_balls: Optional[int] = None
    wides: int = 0
    noballs: int = 0
    fours_conceded: Optional[int] = None
    sixes_conceded: Optional[int] = None
    # Phase splits
    powerplay_overs: Optional[float] = 0.0
    powerplay_wickets: Optional[int] = 0
    powerplay_runs: Optional[int] = 0
    death_overs: Optional[float] = 0.0
    death_wickets: Optional[int] = 0
    death_runs: Optional[int] = 0


class FallOfWicketItem(BaseModel):
    """Sequential record of a lost wicket during an innings."""
    wicket_number: int
    runs: int
    over_display: float  # e.g. 5.4
    batter_out_name: str
    batter_out_id: Optional[str] = None


class PartnershipItem(BaseModel):
    """Batting partnership statistics between two batters."""
    wicket_number: int
    runs: int
    balls: int
    batter_1_name: str
    batter_1_runs: int
    batter_1_balls: int
    batter_2_name: str
    batter_2_runs: int
    batter_2_balls: int
    is_unbroken: bool = False


class PhaseSummaryMetrics(BaseModel):
    """Phase-specific summary for an innings."""
    phase_name: str  # 'Powerplay', 'Middle', 'Death'
    overs_range: str  # e.g. '0.1 - 6.0'
    runs: int = 0
    wickets: int = 0
    run_rate: float = 0.0
    dot_ball_percentage: Optional[float] = None
    boundary_runs: int = 0


class OverProgressionItem(BaseModel):
    """Cumulative match progression point for worm and run-rate graphs."""
    over_number: int  # 1 to 20
    runs_in_over: int
    cumulative_runs: int
    wickets_in_over: int
    cumulative_wickets: int


class InningsAnalysisResponse(BaseModel):
    """Comprehensive analysis of a single match innings."""
    match_id: str
    innings_number: int
    batting_team_code: str
    batting_team_name: str
    bowling_team_code: str
    bowling_team_name: str
    total_runs: int
    wickets: int
    overs_completed: float
    run_rate: float
    extras_total: int
    extras_breakdown: Dict[str, int] = Field(default_factory=dict)
    batting_scorecards: List[BattingScorecardItem] = Field(default_factory=list)
    bowling_scorecards: List[BowlingScorecardItem] = Field(default_factory=list)
    fall_of_wickets: List[FallOfWicketItem] = Field(default_factory=list)
    partnerships: List[PartnershipItem] = Field(default_factory=list)
    phase_summaries: List[PhaseSummaryMetrics] = Field(default_factory=list)
    scoring_progression: List[OverProgressionItem] = Field(default_factory=list)


class MatchScorecardResponse(BaseModel):
    """Complete match scorecard with context, team details, and innings summaries."""
    match_id: str
    external_match_id: str
    competition_id: str
    competition_name: str
    competition_type: str
    season: str
    match_date: str
    venue_name: str
    venue_city: str
    pitch_soil_type: Optional[str] = None
    home_team: Dict[str, Any]
    away_team: Dict[str, Any]
    toss_winner_code: Optional[str] = None
    toss_decision: Optional[str] = None
    winner_team_code: Optional[str] = None
    win_margin: Optional[str] = None
    player_of_match: Optional[str] = None
    innings: List[InningsAnalysisResponse] = Field(default_factory=list)
    data_provenance: Dict[str, Any] = Field(default_factory=dict)


class PlayerDomesticSeasonStats(BaseModel):
    """Season batting and bowling statistics for an uncapped cricketer."""
    competition_id: str
    competition_name: str
    competition_type: str
    season: str
    team_name: str
    matches: int = 0
    # Batting metrics
    innings_batted: int = 0
    runs: int = 0
    balls_faced: int = 0
    not_outs: int = 0
    batting_average: Optional[float] = None
    strike_rate: float = 0.0
    fours: int = 0
    sixes: int = 0
    boundary_percentage: float = 0.0
    dot_ball_percentage: Optional[float] = None
    balls_per_boundary: Optional[float] = None
    high_score: int = 0
    high_score_not_out: bool = False
    scores_30_plus: int = 0
    fifties: int = 0
    hundreds: int = 0
    # Bowling metrics
    innings_bowled: int = 0
    overs_bowled: float = 0.0
    legal_balls: int = 0
    maidens: int = 0
    runs_conceded: int = 0
    bowler_wickets: int = 0
    bowling_average: Optional[float] = None
    bowling_economy: float = 0.0
    bowling_strike_rate: Optional[float] = None
    dot_balls_bowled: Optional[int] = None
    # Fielding
    catches: int = 0
    run_outs: int = 0


class PlayerMatchHistoryItem(BaseModel):
    """Item in a chronological domestic match history log."""
    match_id: str
    match_date: str
    competition_id: str
    competition_name: str
    season: str
    opponent_team: str
    venue_name: str
    role_in_match: str = "Playing XI"
    # Batting in match
    batting_runs: Optional[int] = None
    batting_balls: Optional[int] = None
    batting_strike_rate: Optional[float] = None
    is_out: Optional[bool] = None
    dismissal_kind: Optional[str] = None
    # Bowling in match
    bowling_overs: Optional[float] = None
    bowling_maidens: Optional[int] = None
    bowling_runs: Optional[int] = None
    bowler_wickets: Optional[int] = None
    bowling_economy: Optional[float] = None
    # Fielding
    catches: int = 0
    run_outs: int = 0
    is_player_of_match: bool = False


class PlayerPhaseSplitDetail(BaseModel):
    """Detailed phase split for a player in a competition."""
    phase: str  # 'Powerplay', 'Middle', 'Death'
    overs_range: str
    batting_runs: int = 0
    batting_balls: int = 0
    batting_strike_rate: float = 0.0
    batting_fours: int = 0
    batting_sixes: int = 0
    batting_dot_percentage: Optional[float] = None
    batting_dismissals: int = 0
    bowling_overs: float = 0.0
    bowling_legal_balls: int = 0
    bowling_runs_conceded: int = 0
    bowler_wickets: int = 0
    bowling_economy: float = 0.0
    bowling_dot_percentage: Optional[float] = None


class AllRoundContributionResponse(BaseModel):
    """
    Transparent dual-discipline summary for uncapped players with batting and bowling contributions.
    Rule: Never creates arbitrary or speculative composite ratings; preserves independent components.
    """
    player_id: str
    full_name: str
    canonical_id: str
    eligibility_status: str
    primary_role: str
    domestic_team: Optional[str] = None
    sample_size: Dict[str, int] = Field(
        ...,
        description="Sample size transparency: total matches, innings batted, overs bowled"
    )
    batting_summary: Dict[str, Any]
    bowling_summary: Dict[str, Any]
    fielding_summary: Dict[str, Any]
    role_archetype_context: str = Field(
        ...,
        description="Qualitative role classification based on evidence (e.g. 'Finishing Batter & Part-Time Off-Spinner')"
    )
    has_sufficient_sample: bool = True

