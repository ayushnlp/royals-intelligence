"""
Royals Intelligence - Core Cricket Data Contracts
Strict Pydantic models for competition entities, scorecards, and ball-by-ball deliveries.
Governs all ingested, validated, and normalized cricket data.
"""

from datetime import date, datetime
from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field, field_validator


class SourceReference(BaseModel):
    """Provenance tracking for any ingested record."""
    source_id: str = Field(..., description="Registered source identifier (e.g., 'cricsheet_open')")
    source_url_or_file: str = Field(..., description="Original URL or source file path")
    ingested_at: datetime = Field(..., description="Timestamp when the record was ingested")
    checksum_sha256: Optional[str] = Field(None, description="SHA-256 hash of raw source artifact")


class Competition(BaseModel):
    """Competition entity contract."""
    competition_id: str = Field(..., description="Canonical competition slug (e.g. 'ipl', 'smat', 'ranji')")
    name: str = Field(..., description="Full competition name (e.g. 'Indian Premier League')")
    competition_type: Literal["T20", "List A", "First Class", "T10"] = Field(..., description="Match format")
    governing_body: str = Field(default="BCCI")
    is_domestic: bool = Field(default=False)
    source_ref: SourceReference


class Season(BaseModel):
    """Season entity contract."""
    season_id: str = Field(..., description="Standardized season key (e.g., '2026', '2025', '2024')")
    competition_id: str
    year_start: int
    year_end: int
    is_active: bool = Field(default=False)


class Team(BaseModel):
    """Franchise or state team contract."""
    team_id: str = Field(..., description="Canonical team code (e.g. 'RR', 'CSK', 'MI', 'MUM', 'RAJ')")
    name: str = Field(..., description="Official full team name")
    short_name: str
    is_rr: bool = Field(default=False)
    primary_color: Optional[str] = None
    accent_color: Optional[str] = None
    aliases: List[str] = Field(default_factory=list)


class Venue(BaseModel):
    """Stadium and venue contract."""
    venue_id: str = Field(..., description="Unique venue code (e.g. 'SMS_JAIPUR')")
    name: str = Field(..., description="Standard venue name")
    city: str
    country: str = Field(default="India")
    is_rr_home: bool = Field(default=False)
    pitch_soil_type: Optional[str] = Field(None, description="Soil composition if known, else None")
    straight_boundary_m: Optional[float] = Field(None, description="Straight boundary dimension in meters")
    off_boundary_m: Optional[float] = Field(None, description="Off-side boundary dimension in meters")
    leg_boundary_m: Optional[float] = Field(None, description="Leg-side boundary dimension in meters")
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class Player(BaseModel):
    """Player demographic and profile contract."""
    player_id: str = Field(..., description="Canonical player identifier")
    full_name: str
    known_as: Optional[str] = None
    dob: Optional[date] = None
    nationality: str = Field(default="India")
    batting_hand: Optional[Literal["Right", "Left"]] = None
    bowling_style: Optional[str] = None
    primary_role: Optional[Literal["Batter", "Bowler", "All-Rounder", "Wicketkeeper"]] = None
    is_capped: bool = Field(default=False)
    source_registry_id: Optional[str] = None


class DismissalDetails(BaseModel):
    """Wicket dismissal event details."""
    kind: Literal[
        "bowled", "caught", "caught and bowled", "lbw", "stumped",
        "run out", "hit wicket", "retired hurt", "retired out", "obstructing the field", "timed out"
    ]
    player_out: str = Field(..., description="Name or identifier of the dismissed player")
    fielders: List[str] = Field(default_factory=list, description="Names of fielders involved")
    is_bowler_credited: bool = Field(default=True, description="True for bowled, caught, lbw, stumped, hit wicket")


class DeliveryExtras(BaseModel):
    """Breakdown of extras on a delivery."""
    wides: int = 0
    noballs: int = 0
    legbyes: int = 0
    byes: int = 0
    penalty: int = 0

    @property
    def total(self) -> int:
        return self.wides + self.noballs + self.legbyes + self.byes + self.penalty


class BallByBallDelivery(BaseModel):
    """
    Granular single delivery contract.
    Strict rule: Never fabricate delivery classifications (yorker, slower ball, cutter).
    Only assign if supported by source data; otherwise set to None.
    """
    match_id: str
    innings_number: int = Field(..., ge=1, le=4)
    over_number: int = Field(..., ge=0, le=49, description="0-indexed over (0 = 1st over)")
    ball_in_over: int = Field(..., ge=1, description="Delivery sequence within the over (1-6+)")
    over_display: float = Field(..., description="e.g. 0.1 for first ball, 19.6 for last ball")
    phase: Literal["Powerplay", "Middle", "Death"]
    batting_team: str
    bowling_team: str
    striker: str
    non_striker: str
    bowler: str
    batter_runs: int = Field(..., ge=0, le=6)
    extras: DeliveryExtras = Field(default_factory=DeliveryExtras)
    total_runs: int = Field(..., ge=0, le=12)
    is_legal: bool = Field(default=True)
    is_boundary_four: bool = Field(default=False)
    is_boundary_six: bool = Field(default=False)
    is_dot_ball: bool = Field(default=False)
    is_wicket: bool = Field(default=False)
    dismissal: Optional[DismissalDetails] = None
    
    # Telemetry fields: strictly Optional[float/str], default None (NEVER FABRICATED)
    release_speed_kph: Optional[float] = Field(None, description="Radar speed if provided by telemetry, else None")
    delivery_classification: Optional[str] = Field(
        None,
        description="e.g., 'yorker', 'bouncer', 'slower ball' ONLY if explicit source classification exists; otherwise None"
    )
    shot_type: Optional[str] = Field(None, description="Shot classification if in source telemetry, else None")
    source_ref: SourceReference

    @field_validator("total_runs", mode="after")
    @classmethod
    def validate_total_runs(cls, v: int, info) -> int:
        batter_runs = info.data.get("batter_runs", 0)
        extras = info.data.get("extras", DeliveryExtras())
        calculated = batter_runs + extras.total
        if v != calculated:
            raise ValueError(f"total_runs ({v}) must equal batter_runs ({batter_runs}) + extras ({extras.total})")
        return v


class BattingScorecard(BaseModel):
    """Summary batting record for a player in a match."""
    match_id: str
    innings_number: int
    player_name: str
    batting_position: int
    runs: int
    balls_faced: int
    fours: int = 0
    sixes: int = 0
    strike_rate: float
    is_out: bool = True
    dismissal_kind: Optional[str] = None
    bowler_name: Optional[str] = None
    fielder_name: Optional[str] = None
    dot_balls: Optional[int] = None


class BowlingScorecard(BaseModel):
    """Summary bowling record for a player in a match."""
    match_id: str
    innings_number: int
    bowler_name: str
    overs: float
    legal_balls: int
    maidens: int = 0
    runs_conceded: int
    wickets: int
    economy_rate: float
    dot_balls: Optional[int] = None
    wides: int = 0
    noballs: int = 0


class PlayerParticipation(BaseModel):
    """Player match participation record (Playing XI, Impact Player, Sub)."""
    match_id: str
    player_name: str
    team_name: str
    role_in_match: Literal["Playing XI", "Impact Player Used", "Unused Substitute", "Captain", "Wicketkeeper"]
    is_impact_player_in: bool = False
    is_impact_player_out: bool = False
    substituted_at_over: Optional[float] = None


class Innings(BaseModel):
    """Innings aggregate contract."""
    innings_number: int
    batting_team: str
    bowling_team: str
    total_runs: int
    wickets: int
    overs_completed: float
    is_declared_or_all_out: bool = False
    extras_total: int = 0
    deliveries_count: int


class MatchResult(BaseModel):
    """Outcome and margin contract."""
    winner: Optional[str] = None  # None for tie/no result/abandoned
    winner_team_code: Optional[str] = None
    win_by_runs: Optional[int] = None
    win_by_wickets: Optional[int] = None
    is_tie: bool = False
    is_super_over: bool = False
    method: Optional[str] = Field(None, description="e.g. 'DLS' if Duckworth-Lewis-Stern applied")
    outcome_summary: str


class Match(BaseModel):
    """Match level comprehensive contract."""
    match_id: str
    competition_id: str
    season: str
    match_date: date
    venue: str
    city: Optional[str] = None
    team1: str
    team2: str
    toss_winner: str
    toss_decision: Literal["bat", "field"]
    result: MatchResult
    player_of_match: Optional[str] = None
    innings: List[Innings] = Field(default_factory=list)
    source_ref: SourceReference
