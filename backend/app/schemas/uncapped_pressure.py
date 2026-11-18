"""
Royals Intelligence - Uncapped Pressure Analytics Schemas
Pydantic data models for Indian Uncapped Player intelligence leaderboards,
eligibility auditing, and role-based performance profiles.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class UncappedBattingItem(BaseModel):
    uncapped_rank: int = Field(..., description="Uncapped leaderboard rank")
    overall_r1_rank: int = Field(..., description="Overall Round 1 challenge rank")
    player_id: int
    player_name: str
    franchise: str
    tactical_role: str
    conservative_pri: float = Field(..., description="Conservative PRI (1-SE Lower Credible Bound in SR pts)")
    posterior_mean: float
    posterior_se: float
    ci_95_lower: float
    ci_95_upper: float
    pressure_legal_balls: int
    pressure_matches: int
    observed_strike_rate: float
    observed_boundary_pct: float
    observed_dot_pct: float
    eligibility_status: str
    eligibility_reason: str
    verification_source: str
    verification_date: str
    is_official_r1_qualified: Optional[bool] = True
    meets_active_gate: Optional[bool] = True


class UncappedBowlingItem(BaseModel):
    uncapped_rank: int = Field(..., description="Uncapped leaderboard rank")
    overall_r1_rank: int = Field(..., description="Overall Round 1 challenge rank")
    player_id: int
    player_name: str
    franchise: str
    tactical_role: str
    conservative_runs_saved: float = Field(..., description="Conservative Runs Saved per 6 balls (RPO)")
    posterior_mean: float
    posterior_se: float
    ci_95_lower: float
    ci_95_upper: float
    pressure_legal_balls: int
    pressure_matches: int
    observed_economy: float
    observed_wicket_pct: float
    observed_dot_pct: float
    eligibility_status: str
    eligibility_reason: str
    verification_source: str
    verification_date: str
    is_official_r1_qualified: Optional[bool] = True
    meets_active_gate: Optional[bool] = True


class UncappedLeaderboardResponse(BaseModel):
    discipline_filter: str
    qualified_only: bool
    batting_count: int
    bowling_count: int
    batting_leaderboard: Optional[List[UncappedBattingItem]] = None
    bowling_leaderboard: Optional[List[UncappedBowlingItem]] = None
    sample_gate: str
    governing_statute: str
    audit_date: str
    min_balls_applied: Optional[int] = 60
    min_matches_applied: Optional[int] = 0
    is_exploratory_filter: Optional[bool] = False
    excluded_count: Optional[int] = 0
    total_pool_count: Optional[int] = 0


class UncappedOverviewResponse(BaseModel):
    total_verified_uncapped_batters: int
    total_verified_uncapped_bowlers: int
    top_uncapped_batter: Optional[str] = None
    top_uncapped_bowler: Optional[str] = None
    sample_gate_applied: str
    governing_statute: str
    audit_date: str
    min_balls_applied: Optional[int] = 60
    min_matches_applied: Optional[int] = 0
    is_exploratory_filter: Optional[bool] = False
    total_pool_batters: Optional[int] = 30
    total_pool_bowlers: Optional[int] = 22
    excluded_batters_count: Optional[int] = 0
    excluded_bowlers_count: Optional[int] = 0
