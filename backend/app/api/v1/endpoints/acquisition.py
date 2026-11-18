"""
Royals Intelligence - Data Acquisition API Endpoints
Provides source registry inspection, ingestion orchestration, dataset manifests, coverage audits, and manual upload.
"""

from typing import List, Optional
from pathlib import Path
import json

from fastapi import APIRouter, HTTPException, UploadFile, File, Form, status, Query
from app.acquisition.registry import source_registry
from app.acquisition.orchestration.orchestrator import orchestrator
from app.acquisition.validation.validator import CricketDataValidator
from app.acquisition.storage.raw_storage import RawStorageManager
from app.core.config import get_repo_root
from app.core.logging import logger

from app.schemas.acquisition_api import (
    SourceSummary,
    SourceDetailResponse,
    SourceHealthResponse,
    StartIngestionRunRequest,
    UploadDatasetResponse,
)
from app.schemas.contracts.ingestion_contracts import (
    IngestionRun,
    DatasetManifest,
    OverallCoverageReport,
)

router = APIRouter()
MAX_UPLOAD_SIZE_BYTES = 20 * 1024 * 1024  # 20 MB max file size
ALLOWED_EXTENSIONS = {".json", ".csv"}


# --- 1. Source Discovery & Evaluation ---

@router.get("/sources", response_model=List[SourceSummary], summary="List Registered Cricket Data Sources")
async def list_sources(
    tier: Optional[str] = Query(None, description="Filter by reliability tier: TIER_1, TIER_2, TIER_3, TIER_4"),
    category: Optional[str] = Query(None, description="Filter by category substring"),
):
    """Returns catalog of registered sources with reliability tiers, legal licensing, and access methods."""
    sources = source_registry.list_sources(tier=tier, category=category)
    return [
        SourceSummary(
            source_id=s["source_id"],
            name=s["name"],
            tier=s["tier"],
            category=s["category"],
            status=s.get("status", "unknown"),
            update_frequency=s.get("update_frequency", "unknown"),
            access_method=s.get("access_method", "unknown"),
            licensing=s.get("licensing", {}),
            reliability_assessment=s.get("reliability_assessment", "unknown"),
        )
        for s in sources
    ]


@router.get("/sources/{source_id}", response_model=SourceDetailResponse, summary="Get Data Source Specifications")
async def get_source_details(source_id: str):
    """Detailed metadata for a specific cricket data source including known gaps and terms."""
    s = source_registry.get_source(source_id)
    if not s:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Source with id '{source_id}' not found in registry.",
        )
    return SourceDetailResponse(**s)


@router.get("/sources/{source_id}/health", response_model=SourceHealthResponse, summary="Probe Data Source Availability")
async def get_source_health(source_id: str):
    """Probes source operational health, rate-limits, and connectivity mode."""
    s = source_registry.get_source(source_id)
    if not s:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Source with id '{source_id}' not found.",
        )
    diag = source_registry.check_source_availability(source_id)
    return SourceHealthResponse(
        source_id=source_id,
        name=s["name"],
        tier=s["tier"],
        status=diag.get("status", "UNKNOWN"),
        is_accessible=diag.get("is_accessible", False),
        access_method=s.get("access_method"),
        rate_limits=s.get("rate_limits"),
        details=diag,
    )


# --- 2. Ingestion Run Management ---

@router.get("/runs", response_model=List[IngestionRun], summary="List Ingestion Runs")
@router.get("/ingestion-runs", response_model=List[IngestionRun], summary="List Ingestion Runs (Compatibility Alias)")
async def list_ingestion_runs(limit: int = Query(50, ge=1, le=100)):
    """Returns recent data acquisition runs with validation metrics and durations."""
    return orchestrator.list_runs(limit=limit)


@router.get("/runs/{run_id}", response_model=IngestionRun, summary="Get Ingestion Run Status")
async def get_ingestion_run(run_id: str):
    """Retrieves full execution summary, error logs, and validation details for an ingestion run."""
    run = orchestrator.get_run(run_id)
    if not run:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ingestion run '{run_id}' not found.",
        )
    return run


@router.post("/runs", response_model=IngestionRun, status_code=status.HTTP_201_CREATED, summary="Trigger Ingestion Run")
async def trigger_ingestion_run(req: StartIngestionRunRequest):
    """
    Triggers an authorized acquisition run over specified source and tournament dataset.
    """
    repo_root = get_repo_root()
    input_path = repo_root / (req.input_dir or "data/raw/public/samples")
    if not input_path.exists():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Specified input directory '{req.input_dir}' does not exist on disk.",
        )

    json_files = list(input_path.glob("*.json"))
    if not json_files:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No JSON match files found in '{req.input_dir}'.",
        )

    try:
        run = orchestrator.ingest_match_files(
            source_id=req.source_id,
            competition_id=req.competition_id,
            season=req.season,
            file_paths=json_files,
        )
        return run
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as exc:
        logger.error(f"Error executing ingestion run: {exc}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))


# --- 3. Dataset Manifests & Provenance ---

@router.get("/datasets", response_model=List[DatasetManifest], summary="List Acquired Dataset Manifests")
async def list_datasets():
    """Lists acquired dataset catalogs with versioning and validation status."""
    return orchestrator.list_manifests()


@router.get("/datasets/{dataset_id}", response_model=DatasetManifest, summary="Get Dataset Manifest Details")
async def get_dataset(dataset_id: str):
    """Returns provenance metadata, raw file checksums, and Parquet partition paths for a dataset."""
    manifest = orchestrator.get_manifest(dataset_id)
    if not manifest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dataset manifest '{dataset_id}' not found.",
        )
    return manifest


# --- 4. Dataset Coverage Audit ---

@router.get("/coverage", response_model=OverallCoverageReport, summary="Get Platform Data Coverage Report")
async def get_coverage_report():
    """Audits tournament coverage across IPL 2026, domestic tournaments, and historical ball-by-ball stores."""
    return orchestrator.get_coverage_report()


# --- 5. Compliant Manual Dataset Upload ---

@router.post("/upload", response_model=UploadDatasetResponse, summary="Upload Manual Structured Dataset")
async def upload_manual_dataset(
    file: UploadFile = File(...),
    competition_id: str = Form("ipl"),
    season: str = Form("2024"),
):
    """
    Accepts authorized structured JSON/CSV files with file-size limits, SHA-256 hashing, and validation.
    """
    file_ext = Path(file.filename or "").suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type '{file_ext}'. Allowed formats: {ALLOWED_EXTENSIONS}",
        )

    content = await file.read()
    if len(content) > MAX_UPLOAD_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File exceeds maximum upload limit of {MAX_UPLOAD_SIZE_BYTES // (1024*1024)} MB.",
        )

    raw_storage = RawStorageManager()
    subfolder = f"manual/{competition_id}/{season}"
    filename = file.filename or f"upload_{season}{file_ext}"

    metadata, is_new = raw_storage.store_raw_bytes(
        content=content,
        subfolder=subfolder,
        filename=filename,
        file_format=file_ext.lstrip("."),
    )

    validation_summary = None
    if file_ext == ".json":
        try:
            parsed = json.loads(content.decode("utf-8"))
            if isinstance(parsed, dict) and "info" in parsed and "innings" in parsed:
                validation_summary = CricketDataValidator.validate_cricsheet_match_dict(
                    parsed, Path(filename).stem
                )
        except Exception as e:
            logger.warning(f"Uploaded file {filename} is not valid Cricsheet JSON: {e}")

    msg = "Dataset successfully uploaded and SHA-256 verified." if is_new else "Identical dataset already stored (idempotent skip)."

    return UploadDatasetResponse(
        filename=metadata.file_name,
        file_format=metadata.file_format,
        file_size_bytes=metadata.file_size_bytes,
        checksum_sha256=metadata.checksum_sha256,
        stored_path=metadata.file_path,
        is_duplicate=(not is_new),
        validation=validation_summary,
        message=msg,
    )

