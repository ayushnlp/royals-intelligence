"""
Royals Intelligence - RR Auction & Retention Intelligence
Pydantic Schemas for AUCTION-00: Foundation & Data Readiness.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class DatasetMetadata(BaseModel):
    """Metadata for a raw data asset in the Rajasthan Royals data pack."""
    name: str = Field(..., description="File name of the dataset")
    path: str = Field(..., description="Relative or absolute path")
    size_bytes: int = Field(..., description="File size in bytes")
    row_count: int = Field(..., description="Total number of rows")
    column_count: int = Field(..., description="Total number of columns")
    columns: List[str] = Field(..., description="List of column names")
    sha256: str = Field(..., description="SHA-256 checksum of raw file")


class DeliverySemanticsSummary(BaseModel):
    """Reconciliation of ball-by-ball delivery semantics."""
    total_rows: int = Field(200999, description="Total raw delivery records")
    legal_deliveries: int = Field(192709, description="Deliveries counting towards legal ball count")
    extras_deliveries: int = Field(8290, description="Deliveries not counting towards legal ball count")
    wides: int = Field(7714, description="Wide deliveries")
    no_balls: int = Field(576, description="No-ball deliveries (foot faults / oversteps)")
    total_runs_conceded: int = Field(..., description="Total runs conceded across all deliveries")
    total_wickets: int = Field(..., description="Total dismissals recorded")


class MatchCoverageSummary(BaseModel):
    """Reconciliation of match records."""
    total_matches: int = Field(883, description="Total match records in matches.csv")
    matches_with_balls: int = Field(867, description="Matches with recorded ball-by-ball deliveries")
    abandoned_or_no_result: int = Field(16, description="Matches abandoned or with no deliveries recorded")
    date_min: Optional[str] = Field(None, description="Earliest match date")
    date_max: Optional[str] = Field(None, description="Latest match date")
    competitions: List[str] = Field(default_factory=list, description="List of competitions present")


class RRSquadRoleBreakdown(BaseModel):
    """Role breakdown for Rajasthan Royals 2026 squad baseline."""
    bowlers: int = Field(12, description="Specialist Bowlers")
    all_rounders: int = Field(6, description="All-Rounders")
    batters: int = Field(5, description="Specialist Batters")
    wicketkeeper_batters: int = Field(4, description="Wicketkeeper-Batters")
    total_players: int = Field(27, description="Total player entries for RR in ipl_players.csv")


class RRSquadPlayerEntry(BaseModel):
    """Individual player record in the RR 2026 squad baseline."""
    player_id: int
    player_name: str
    role: str
    batting_style: str
    bowling_style: Optional[str] = None
    spin_type: Optional[str] = None
    disclaimer_flag: Optional[str] = None


class DataQualityIssue(BaseModel):
    """Tracked data quality issue."""
    issue_id: str
    dataset: str
    severity: str  # HIGH, MEDIUM, LOW, INFORMATIONAL
    description: str
    affected_rows: int
    resolution_status: str
    remediation_note: str


class FoundationDataIngestionReport(BaseModel):
    """Comprehensive AUCTION-00 data ingestion summary."""
    status: str = "SUCCESS"
    datasets: Dict[str, DatasetMetadata] = Field(default_factory=dict)
    delivery_semantics: DeliverySemanticsSummary
    match_coverage: MatchCoverageSummary
    rr_squad_summary: RRSquadRoleBreakdown
    data_quality_issues: List[DataQualityIssue] = Field(default_factory=list)
