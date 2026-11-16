"""
Royals Intelligence - Pressure Analytics API Schemas
Pydantic v2 data models for Round 1 Pressure Analytics Endpoints
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class PressureOverviewResponse(BaseModel):
    """Aggregate overview of the Round 1 Pressure evaluation environment."""
    challenge_title: str = "SupeRR Selector Season 2: Most Reliable Players Under Pressure"
    governing_dataset: str = "Official Rajasthan Royals Round 1 Competition Data Pack"
    total_deliveries: int = 200999
    legal_deliveries: int = 192709
    matches_with_deliveries: int = 867
    reconciled_abandoned_matches: int = 16
    total_competitions: int = 141
    strict_pressure_bowling_balls: int = 37014
    strict_pressure_batting_balls: int = 31163
    permissive_pressure_bowling_balls: int = 47820
    permissive_pressure_batting_balls: int = 40518
    death_overs_bowling_pressure_share_pct: float = 87.28
    death_overs_batting_pressure_share_pct: float = 78.95
    total_evaluated_batters: int = 278
    total_evaluated_bowlers: int = 239
    sample_qualification_threshold: str = ">= 60 pressure balls (or >= 50 balls across >= 10 matches)"
    governing_ranking_methodology: str = "Empirical Bayes Shrinkage with 1-SE Conservative Lower Credible Bound"
    data_provenance: str = "Official Rajasthan Royals Round 1 Data Pack"


class PressureLeaderboardBattingItem(BaseModel):
    """Batting leaderboard item ranked by Conservative PRI."""
    rank: int
    player_id: int
    player_name: str
    discipline: str = "batting"
    is_qualified: bool = True
    qualification_status: str
    conservative_pri: float = Field(..., description="1-SE Conservative lower credible bound in Strike Rate pts")
    posterior_mean: float = Field(..., description="Bayesian posterior mean performance differential (theta)")
    posterior_se: float = Field(..., description="Posterior standard error (uncertainty)")
    ci_95_lower: float
    ci_95_upper: float
    ci_95_width: float
    shrinkage_weight: float
    prob_exceed_baseline: float
    prob_exceed_league_mean: float
    observed_strike_rate: float
    expected_strike_rate: float
    diff_strike_rate: float
    observed_boundary_pct: float
    diff_boundary_pct: float
    observed_dot_pct: float
    diff_dot_pct: float
    observed_dismissal_pct: float
    diff_dismissal_pct: float
    pressure_legal_balls: int
    pressure_matches: int
    pressure_seasons: int
    ipl_legal_balls: int
    t20i_legal_balls: int
    competition_qualification: str
    uncertainty_level: str
    evidence_volume_tier: str
    evidence_classification: str
    two_dimensional_classification: str
    explainability_summary: str


class PressureLeaderboardBowlingItem(BaseModel):
    """Bowling leaderboard item ranked by Conservative Runs Saved."""
    rank: int
    player_id: int
    player_name: str
    discipline: str = "bowling"
    is_qualified: bool = True
    qualification_status: str
    conservative_runs_saved: float = Field(..., description="1-SE Conservative lower bound runs saved per 6 balls")
    posterior_mean: float = Field(..., description="Bayesian posterior mean economy difference (RPO)")
    posterior_se: float = Field(..., description="Posterior standard error (uncertainty)")
    ci_95_lower: float
    ci_95_upper: float
    ci_95_width: float
    shrinkage_weight: float
    prob_exceed_baseline: float
    prob_exceed_league_mean: float
    observed_economy: float
    expected_economy: float
    diff_economy: float
    observed_wicket_pct: float
    diff_wicket_pct: float
    observed_dot_pct: float
    diff_dot_pct: float
    observed_boundary_pct: float
    diff_boundary_pct: float
    pressure_legal_balls: int
    pressure_matches: int
    pressure_seasons: int
    ipl_legal_balls: int
    t20i_legal_balls: int
    competition_qualification: str
    uncertainty_level: str
    evidence_volume_tier: str
    evidence_classification: str
    two_dimensional_classification: str
    explainability_summary: str


class PressureLeaderboardResponse(BaseModel):
    """Unified response containing Batting and Bowling leaderboards."""
    discipline_filter: str = "all"
    qualified_only: bool = True
    batting_count: int = 0
    bowling_count: int = 0
    batting_leaderboard: Optional[List[PressureLeaderboardBattingItem]] = None
    bowling_leaderboard: Optional[List[PressureLeaderboardBowlingItem]] = None
    data_provenance: str = "Official Rajasthan Royals Round 1 Data Pack"


class CandidateEvidenceQuestions(BaseModel):
    """The 11 empirical evidence and methodology answers from the formal shortlist report."""
    q1_why_considered: str
    q2_pressure_deliveries: str
    q3_matches_and_seasons: str
    q4_observed_performance: str
    q5_expected_performance: str
    q6_conservative_diagnostic: str
    q7_posterior_uncertainty: str
    q8_credible_interval: str
    q9_competition_support: str
    q10_major_limitations: str
    q11_sensitivity_to_assumptions: str


class CandidateEvidenceProfileResponse(BaseModel):
    """Comprehensive candidate evidence dossier for an individual player."""
    player_id: int
    player_name: str
    discipline: str
    rank: int
    governing_metric_name: str
    governing_metric_value: float
    posterior_mean: float
    posterior_se: float
    ci_95_lower: float
    ci_95_upper: float
    ci_95_width: float
    shrinkage_weight: float
    pressure_legal_balls: int
    pressure_matches: int
    ipl_legal_balls: int
    t20i_legal_balls: int
    competition_qualification: str
    two_dimensional_classification: str
    evidence_classification: str
    uncertainty_level: str
    evidence_questions: CandidateEvidenceQuestions
    data_provenance: str = "Official Rajasthan Royals Round 1 Data Pack"


class PressureMethodologyResponse(BaseModel):
    """Structured methodology information detailing models, formulas, and baselines."""
    challenge_objective: str
    pressure_definition: Dict[str, Any]
    baseline_strata_12_cell: List[str]
    bayesian_shrinkage_formulation: Dict[str, str]
    conservative_pri_formula: Dict[str, str]
    qualification_criteria: Dict[str, Any]
    limitations: List[str]
    data_provenance: str = "Official Rajasthan Royals Round 1 Data Pack"
