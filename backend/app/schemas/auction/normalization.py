"""
Pydantic schemas for AUCTION-04: Historical Performance and Competition Normalization.
Ensures strict independence between batting and bowling domains, with full uncertainty quantification.
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, List


class CompetitionBenchmark(BaseModel):
    """Empirical statistical benchmarks for a competition tier."""
    competition_tier: str = Field(..., description="Competition tier identifier (IPL, T20I, Emerging_T20)")
    total_deliveries: int = Field(..., description="Total delivery records")
    legal_deliveries: int = Field(..., description="Legal deliveries (excluding wides and no-balls)")
    total_runs: int = Field(..., description="Total confirmed runs (bat runs + confirmed extras)")
    batter_runs: int = Field(..., description="Runs scored off the bat")
    total_bowler_conceded_runs: int = Field(..., description="Total runs conceded by bowlers (bat runs + wide/noball extras)")
    total_wickets: int = Field(..., description="Total wickets fallen")
    bowler_credited_wickets: int = Field(..., description="Wickets credited to bowlers (excludes run-outs & retirements)")
    
    # Baseline environment rates
    benchmark_run_rate: float = Field(..., description="Average match run rate per 6 legal balls (total runs / legal balls * 6)")
    benchmark_bowling_economy: float = Field(..., description="Average bowler-conceded economy rate per 6 legal balls (conceded / legal balls * 6)")
    benchmark_strike_rate: float = Field(..., description="Average batter strike rate per 100 legal balls")
    benchmark_boundary_pct: float = Field(..., description="Percentage of legal balls resulting in 4s or 6s")
    benchmark_dot_pct: float = Field(..., description="Percentage of legal balls with 0 runs")
    benchmark_wickets_per_ball: float = Field(..., description="Wickets taken per legal ball")
    benchmark_runs_per_wicket: float = Field(..., description="Average runs scored per dismissal")
    
    # Empirical competition scoring environment index (relative to IPL = 1.000)
    # Strictly labelled as descriptive scoring-environment statistics, not unvalidated competition-strength multipliers
    relative_scoring_index: float = Field(..., description="Descriptive scoring-environment rate index vs IPL anchor (not an unvalidated competition-strength multiplier)")
    relative_boundary_index: float = Field(..., description="Descriptive scoring-environment boundary rate index vs IPL anchor")


class PhaseBattingSplit(BaseModel):
    """Phase-specific batting performance profile with independent exposure evaluation."""
    phase_name: str = Field(..., description="Powerplay (0-5), Middle (6-14), Death (15-19)")
    balls_faced: int = Field(..., description="Legal balls faced in phase")
    runs_scored: int = Field(..., description="Runs scored off bat in phase")
    dismissals: int = Field(..., description="Dismissals in phase")
    strike_rate: float = Field(..., description="Phase-specific strike rate")
    dot_pct: float = Field(..., description="Phase dot-ball percentage")
    boundary_pct: float = Field(..., description="Phase boundary percentage")
    phase_confidence_tier: str = Field(..., description="Independent phase confidence tier: HIGH (>=60 balls in phase), MEDIUM (20-59 balls in phase), LOW (<20 balls in phase)")
    is_phase_qualified: bool = Field(..., description="Meets minimum phase qualification threshold (>= 20 balls in phase)")


class PhaseBowlingSplit(BaseModel):
    """Phase-specific bowling performance profile with independent exposure evaluation."""
    phase_name: str = Field(..., description="Powerplay (0-5), Middle (6-14), Death (15-19)")
    balls_bowled: int = Field(..., description="Legal balls bowled in phase")
    runs_conceded: int = Field(..., description="Runs conceded in phase (bat runs + wide/noball extras)")
    wickets_taken: int = Field(..., description="Bowler-credited wickets taken in phase")
    economy_rate: float = Field(..., description="Phase-specific economy rate")
    dot_pct: float = Field(..., description="Phase dot-ball percentage")
    boundary_pct: float = Field(..., description="Phase boundary concession percentage")
    phase_confidence_tier: str = Field(..., description="Independent phase confidence tier: HIGH (>=60 balls in phase), MEDIUM (20-59 balls in phase), LOW (<20 balls in phase)")
    is_phase_qualified: bool = Field(..., description="Meets minimum phase qualification threshold (>= 20 balls in phase)")


class NormalizedBattingProfile(BaseModel):
    """Independently evaluated normalized batting profile for a canonical player."""
    canonical_id: int = Field(..., description="Stable internal player ID from AUCTION-01")
    canonical_key: str = Field(..., description="Canonical player key (e.g. RR-PLAYER-06819)")
    canonical_name: str = Field(..., description="Canonical player name")
    
    # Raw aggregate performance
    total_matches: int = Field(..., description="Matches with batting involvement")
    innings_batted: int = Field(..., description="Total innings batted")
    legal_balls_faced: int = Field(..., description="Total legal deliveries faced")
    raw_runs_scored: int = Field(..., description="Total runs scored off bat")
    dismissals: int = Field(..., description="Total dismissals recorded")
    fours_count: int = Field(..., description="Total 4s hit")
    sixes_count: int = Field(..., description="Total 6s hit")
    dots_faced: int = Field(..., description="Total dot balls faced")
    
    # Raw rates
    raw_strike_rate: float = Field(..., description="Raw career strike rate")
    raw_batting_average: Optional[float] = Field(None, description="Raw batting average (runs / dismissals)")
    boundary_pct: float = Field(..., description="Boundary frequency percentage")
    dot_pct: float = Field(..., description="Dot ball percentage")
    
    # Competition-normalized metrics
    competition_weighted_sr_index: float = Field(..., description="Weighted strike rate adjusted for competition environments")
    shrunk_strike_rate: float = Field(..., description="Empirical Bayes shrunk strike rate using provisional m=60 legal balls toward IPL benchmark prior")
    normalized_scoring_efficiency: float = Field(..., description="Percentile efficiency score relative to IPL benchmark")
    
    # Uncertainty & sample sufficiency
    sample_confidence_tier: str = Field(..., description="HIGH (>=200 balls), MEDIUM (>=60 balls), LOW (<60 balls)")
    is_sample_qualified: bool = Field(..., description="Meets minimum evaluation threshold (>= 30 balls faced)")
    
    # Phase breakdown
    phase_splits: Dict[str, PhaseBattingSplit] = Field(default_factory=dict, description="Phase-specific batting splits")


class NormalizedBowlingProfile(BaseModel):
    """Independently evaluated normalized bowling profile for a canonical player."""
    canonical_id: int = Field(..., description="Stable internal player ID from AUCTION-01")
    canonical_key: str = Field(..., description="Canonical player key (e.g. RR-PLAYER-02411)")
    canonical_name: str = Field(..., description="Canonical player name")
    
    # Raw aggregate performance
    total_matches: int = Field(..., description="Matches with bowling involvement")
    innings_bowled: int = Field(..., description="Total innings bowled")
    legal_balls_bowled: int = Field(..., description="Total legal balls bowled")
    overs_bowled: float = Field(..., description="Legal overs bowled (balls / 6)")
    raw_runs_conceded: int = Field(..., description="Total runs conceded off bowling")
    wickets_taken: int = Field(..., description="Total wickets taken (bowler credits)")
    dots_bowled: int = Field(..., description="Total dot balls bowled")
    boundaries_conceded: int = Field(..., description="Total 4s and 6s conceded")
    
    # Raw rates
    raw_economy_rate: float = Field(..., description="Raw career economy rate (runs / overs)")
    raw_bowling_strike_rate: Optional[float] = Field(None, description="Balls bowled per wicket")
    raw_bowling_average: Optional[float] = Field(None, description="Runs conceded per wicket")
    dot_pct: float = Field(..., description="Dot ball frequency percentage")
    boundary_conceded_pct: float = Field(..., description="Boundary concession percentage")
    
    # Competition-normalized metrics
    competition_weighted_economy_index: float = Field(..., description="Economy adjusted for competition environments")
    shrunk_economy_rate: float = Field(..., description="Empirical Bayes shrunk economy rate using provisional m=60 legal balls toward IPL benchmark prior")
    normalized_economy_efficiency: float = Field(..., description="Percentile efficiency score relative to IPL benchmark")
    
    # Uncertainty & sample sufficiency
    sample_confidence_tier: str = Field(..., description="HIGH (>=200 balls), MEDIUM (>=60 balls), LOW (<60 balls)")
    is_sample_qualified: bool = Field(..., description="Meets minimum evaluation threshold (>= 30 balls bowled)")
    
    # Phase breakdown
    phase_splits: Dict[str, PhaseBowlingSplit] = Field(default_factory=dict, description="Phase-specific bowling splits")


class NormalizationSummary(BaseModel):
    """Macro summary of AUCTION-04 dataset normalization execution."""
    total_canonical_players: int = Field(..., description="Total canonical players in registry (1,217)")
    total_ball_by_ball_deliveries: int = Field(..., description="Total delivery records audited (200,999)")
    total_legal_deliveries: int = Field(..., description="Total legal deliveries (192,709)")
    total_matches_audited: int = Field(..., description="Total matches audited (883)")
    
    # Batting universe
    total_batters_evaluated: int = Field(..., description="Players with batting delivery records")
    qualified_batters_count: int = Field(..., description="Batters meeting qualification threshold (>=30 balls)")
    
    # Bowling universe
    total_bowlers_evaluated: int = Field(..., description="Players with bowling delivery records")
    qualified_bowlers_count: int = Field(..., description="Bowlers meeting qualification threshold (>=30 balls)")
    
    # Competition benchmarks
    benchmarks: Dict[str, CompetitionBenchmark] = Field(..., description="Benchmarks by competition tier")
    audit_stage: str = Field(default="AUCTION-04")
    governance_notes: str = Field(default="Batting and bowling profiles strictly separated. Empirical shrinkage applied.")
