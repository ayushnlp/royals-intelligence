"""
Royals Intelligence - Data Acquisition API Schemas
Pydantic schemas for API v1 acquisition endpoints.
"""

from typing import List, Optional, Dict, Any, Literal
from datetime import datetime
from pydantic import BaseModel, Field
from app.schemas.contracts.ingestion_contracts import (
    IngestionRun,
    DatasetManifest,
    OverallCoverageReport,
    ValidationSummary,
)


class SourceSummary(BaseModel):
    source_id: str
    name: str
    tier: str
    category: str
    status: str
    update_frequency: str
    access_method: str
    licensing: Dict[str, Any]
    reliability_assessment: str


class SourceDetailResponse(BaseModel):
    source_id: str
    name: str
    url: str
    tier: str
    status: str
    category: str
    coverage: Dict[str, Any]
    update_frequency: str
    access_method: str
    authentication: str
    licensing: Dict[str, Any]
    rate_limits: str
    reliability_assessment: str
    known_gaps: List[str]
    last_verified: str


class SourceHealthResponse(BaseModel):
    source_id: str
    name: str
    tier: str
    status: str
    is_accessible: bool
    access_method: Optional[str] = None
    rate_limits: Optional[str] = None
    details: Optional[Dict[str, Any]] = None


class StartIngestionRunRequest(BaseModel):
    source_id: str = Field(..., description="Registered source identifier (e.g., 'cricsheet_open')")
    competition_id: str = Field(default="ipl", description="Competition slug (e.g., 'ipl', 'smat')")
    season: str = Field(default="2024", description="Season identifier (e.g., '2024', '2025')")
    input_dir: Optional[str] = Field(
        default="data/raw/public/samples",
        description="Relative path to raw source directory"
    )


class UploadDatasetResponse(BaseModel):
    filename: str
    file_format: str
    file_size_bytes: int
    checksum_sha256: str
    stored_path: str
    is_duplicate: bool
    validation: Optional[ValidationSummary] = None
    message: str

