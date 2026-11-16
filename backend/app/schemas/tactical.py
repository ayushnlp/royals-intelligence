"""
Royals Intelligence - Tactical Analytics API Schemas
Pydantic v2 data models for Dataset-Driven Tactical Analytics Endpoints (Stage 5)
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class TacticalDatasetSummaryResponse(BaseModel):
    """Overall dataset pack tactical summary metrics."""
    total_deliveries: int = Field(..., description="Total ball-by-ball delivery records")
    legal_deliveries: int = Field(..., description="Legal deliveries excluding wides and oversteps")
    total_matches_with_deliveries: int = Field(..., description="Matches with recorded deliveries")
    total_unique_strikers: int = Field(..., description="Unique batters facing deliveries")
    total_unique_bowlers: int = Field(..., description="Unique bowlers delivering balls")
    total_runs_off_bat: int = Field(..., description="Total runs scored off the bat")
    total_wickets_fallen: int = Field(..., description="Total wickets fallen")
    total_bowler_wickets: int = Field(..., description="Wickets credited to bowlers (excluding run outs, etc.)")
    overall_run_rate_per_6_balls: float = Field(..., description="Tournament-wide run rate per 6 legal balls")
    valid_radar_speed_records: int = Field(..., description="Deliveries with validated radar release telemetry")
    data_provenance: str = Field("Official Rajasthan Royals Round 1 Data Pack", description="Source data provenance")
    generated_at: str = Field(..., description="ISO 8601 generation timestamp")


class TacticalPhaseSplitItem(BaseModel):
    """Performance metrics segregated by match phase."""
    phase: str
    total_balls: int = 0
    legal_balls: int = 0
    runs: int = 0
    wickets: int = 0
    strike_rate: Optional[float] = None
    economy_rate: Optional[float] = None
    average: Optional[float] = None
    dot_ball_percentage: float = 0.0
    boundary_percentage: float = 0.0
    balls_per_wicket: Optional[float] = None


class TacticalPhaseResponse(BaseModel):
    """Phase-wise performance breakdown response."""
    striker_id: Optional[int] = None
    striker_name: Optional[str] = None
    bowler_id: Optional[int] = None
    bowler_name: Optional[str] = None
    phases: Dict[str, TacticalPhaseSplitItem]
    data_provenance: str = "Official Rajasthan Royals Round 1 Data Pack"


class TacticalStrokeItem(BaseModel):
    """Efficiency and risk metrics for a specific shot stroke."""
    stroke: str
    deliveries_faced: int
    runs_scored: int
    dismissals: int
    runs_per_shot: float
    dismissal_rate_pct: float
    boundary_pct: float


class TacticalStrokesResponse(BaseModel):
    """Stroke-wise batting efficiency response."""
    striker_id: Optional[int] = None
    striker_name: Optional[str] = None
    total_strokes_analyzed: int
    strokes: List[TacticalStrokeItem]
    data_provenance: str = "Official Rajasthan Royals Round 1 Data Pack"


class HandednessSplitItem(BaseModel):
    """4-way cross-split of batter stance and bowling style."""
    batting_type: str
    pace_or_spin: str
    balls_faced: int
    runs_scored: int
    wickets: int
    strike_rate: float
    economy_rate: float
    bowling_average: Optional[float] = None
    boundary_pct: float
    dot_pct: float


class HandednessMatrixResponse(BaseModel):
    """Batter handedness versus bowling style matrix response."""
    striker_id: Optional[int] = None
    striker_name: Optional[str] = None
    bowler_id: Optional[int] = None
    bowler_name: Optional[str] = None
    matrix: List[HandednessSplitItem]
    data_provenance: str = "Official Rajasthan Royals Round 1 Data Pack"


class DeliveryStyleItem(BaseModel):
    """Effectiveness for a bowling delivery variation style."""
    delivery_style: str
    deliveries_bowled: int
    runs_conceded: int
    wickets: int
    dot_balls: int
    economy_rate: float
    bowling_average: Optional[float] = None
    dot_ball_pct: float


class DeliveryStylesResponse(BaseModel):
    """Delivery variation effectiveness response."""
    bowler_id: Optional[int] = None
    bowler_name: Optional[str] = None
    total_styles_analyzed: int
    styles: List[DeliveryStyleItem]
    data_provenance: str = "Official Rajasthan Royals Round 1 Data Pack"


class SpeedBrackets(BaseModel):
    """Counts across speed ranges."""
    slow_under_110: int = 0
    medium_110_to_125: int = 0
    fast_medium_125_to_140: int = 0
    express_over_140: int = 0


class FastestBowlerItem(BaseModel):
    """Fastest bowler summary item."""
    bowler_id: int
    bowler_name: str
    valid_deliveries: int
    mean_speed_kmh: float
    max_speed_kmh: float
    express_balls_count: int


class SpeedProfileResponse(BaseModel):
    """Bowling release speed profile with sensor-quality safeguards."""
    bowler_id: Optional[int] = None
    bowler_name: Optional[str] = None
    total_deliveries: Optional[int] = None
    overall_valid_speed_deliveries: Optional[int] = None
    valid_speed_deliveries: Optional[int] = None
    speed_coverage_pct: float
    mean_speed_kmh: Optional[float] = None
    median_speed_kmh: Optional[float] = None
    min_speed_kmh: Optional[float] = None
    max_speed_kmh: Optional[float] = None
    std_speed_kmh: Optional[float] = None
    speed_brackets: Optional[SpeedBrackets] = None
    top_fastest_bowlers: Optional[List[FastestBowlerItem]] = None
    sensor_safeguards_applied: bool = True
    data_quality_note: str = Field(..., description="Documentation of sensor cleaning and calibration")
    data_provenance: str = "Official Rajasthan Royals Round 1 Data Pack"


class PlayerTacticalProfileResponse(BaseModel):
    """Comprehensive multi-dimensional player tactical profile."""
    player_id: int
    player_name: str
    is_batter: bool
    is_bowler: bool
    batting_profile: Optional[Dict[str, Any]] = None
    bowling_profile: Optional[Dict[str, Any]] = None
    data_provenance: str = "Official Rajasthan Royals Round 1 Data Pack"


class DeathOverPerformerBattingItem(BaseModel):
    """Top death overs batter ranking item."""
    striker_id: int
    striker_name: str
    runs: int
    balls: int
    fours: int
    sixes: int
    strike_rate: float
    boundary_pct: float
    dot_pct: float


class DeathOverPerformerBowlingItem(BaseModel):
    """Top death overs bowler ranking item."""
    bowler_id: int
    bowler_name: str
    bowling_type: str
    legal_balls: int
    runs: int
    wickets: int
    economy: float
    average: Optional[float] = None
    dot_pct: float


class DeathOversRankingResponse(BaseModel):
    """Rankings for death phase (overs 16–20) performance."""
    discipline: str
    min_balls_threshold: int
    batting_finishers: Optional[List[DeathOverPerformerBattingItem]] = None
    bowling_containment: Optional[List[DeathOverPerformerBowlingItem]] = None
    data_provenance: str = "Official Rajasthan Royals Round 1 Data Pack"


class HeadToHeadMatchupResponse(BaseModel):
    """Batter vs Bowler head-to-head micro-battle response."""
    striker_id: int
    striker_name: str
    bowler_id: int
    bowler_name: str
    balls_faced: int
    legal_balls: int
    runs_scored: int
    dismissals: int
    fours: int
    sixes: int
    dot_balls: int
    strike_rate: float
    dot_ball_pct: float
    boundary_pct: float
    data_provenance: str = "Official Rajasthan Royals Round 1 Data Pack"


class PlayerLookupItem(BaseModel):
    """Player item for search and autocomplete selectors."""
    player_id: int
    player_name: str
    is_batter: bool = False
    is_bowler: bool = False
    total_deliveries: int = 0

