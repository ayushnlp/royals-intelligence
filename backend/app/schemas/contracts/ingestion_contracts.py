"""
Royals Intelligence - Ingestion & Audit Data Contracts
Contracts governing Ingestion Runs, Dataset Manifests, Validation Reports, and Provenance.
"""

from datetime import datetime
from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field


class FileArtifactMetadata(BaseModel):
    """Metadata describing an acquired raw or processed file."""
    file_path: str
    file_name: str
    file_format: Literal["json", "csv", "parquet", "zip"]
    file_size_bytes: int
    checksum_sha256: str
    record_count: Optional[int] = None
    created_at: datetime


class ValidationErrorItem(BaseModel):
    """Individual record validation error."""
    record_identifier: str
    error_type: str
    message: str
    field_name: Optional[str] = None
    raw_value: Optional[Any] = None
    severity: Literal["CRITICAL", "WARNING"] = "CRITICAL"


class ValidationSummary(BaseModel):
    """Summary metrics of a dataset validation execution."""
    total_records: int
    valid_records: int
    rejected_records: int
    warning_count: int
    duplicate_records_detected: int
    validation_pass_rate: float = Field(
        default=100.0,
        description="Calculated as (valid_records / total_records) * 100"
    )
    completeness_percentage: float = Field(
        default=100.0,
        description="Dataset field completeness percentage (present required fields / total expected fields * 100)"
    )
    errors: List[ValidationErrorItem] = Field(default_factory=list)
    passed: bool


class IngestionRun(BaseModel):
    """Contract tracking an execution of the data acquisition pipeline."""
    run_id: str = Field(..., description="Unique run identifier (e.g. 'run_20261107_143000_abc123')")
    source_id: str
    competition_id: str
    season: str
    status: Literal["PENDING", "IN_PROGRESS", "COMPLETED", "FAILED", "PARTIALLY_COMPLETED"]
    started_at: datetime
    completed_at: Optional[datetime] = None
    duration_seconds: Optional[float] = None
    files_acquired: List[FileArtifactMetadata] = Field(default_factory=list)
    validation: Optional[ValidationSummary] = None
    error_message: Optional[str] = None
    idempotent_skips: int = Field(default=0, description="Count of identical files skipped via checksum")
    metadata: Dict[str, Any] = Field(default_factory=dict)


class DatasetManifest(BaseModel):
    """Provenance and lineage catalog for an acquired dataset."""
    dataset_id: str = Field(..., description="Unique dataset key (e.g. 'ipl_2024_ball_by_ball')")
    competition_id: str
    season: str
    source_id: str
    version: str = "1.0.0"
    created_at: datetime
    updated_at: datetime
    run_id: str
    raw_files: List[FileArtifactMetadata] = Field(default_factory=list)
    processed_parquet_paths: List[str] = Field(default_factory=list)
    total_matches: int = 0
    total_deliveries: int = 0
    total_players: int = 0
    validation_status: Literal["VALIDATED", "UNVALIDATED", "REJECTED"] = "UNVALIDATED"
    completeness_percentage: float = 0.0


class CompetitionCoverage(BaseModel):
    """Coverage audit for a single tournament / season."""
    competition_id: str
    competition_name: str
    season: str
    total_scheduled_matches: Optional[int] = None
    matches_acquired: int
    ball_by_ball_available: int
    scorecards_available: int
    squads_available: bool
    status: Literal["ACQUIRED", "PARTIALLY_ACQUIRED", "UNAVAILABLE", "MANUALLY_SUPPLIED"]
    data_gaps: List[str] = Field(default_factory=list)


class OverallCoverageReport(BaseModel):
    """Global system data coverage status."""
    generated_at: datetime
    primary_season: str = "IPL 2026"
    competitions: List[CompetitionCoverage] = Field(default_factory=list)
    total_matches_acquired: int = 0
    total_deliveries_indexed: int = 0
    total_players_registered: int = 0
    sources_active: int = 0

