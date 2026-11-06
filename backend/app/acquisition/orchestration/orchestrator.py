"""
Royals Intelligence - Ingestion Orchestrator
Coordinates end-to-end ingestion runs: fetching, storage, validation, normalization, and manifests.
"""

import json
import time
import uuid
from pathlib import Path
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional

from app.schemas.contracts.ingestion_contracts import (
    IngestionRun,
    DatasetManifest,
    FileArtifactMetadata,
    ValidationSummary,
    OverallCoverageReport,
    CompetitionCoverage,
)
from app.schemas.contracts.cricket_contracts import SourceReference
from app.acquisition.registry import source_registry
from app.acquisition.storage.raw_storage import RawStorageManager
from app.acquisition.validation.validator import CricketDataValidator
from app.acquisition.normalization.normalizer import CricketDataNormalizer
from app.acquisition.storage.parquet_store import ParquetStorageManager
from app.core.logging import logger
from app.core.config import get_repo_root


class IngestionOrchestrator:
    """Coordinates data acquisition pipeline executions, provenance manifests, and coverage reports."""

    def __init__(
        self,
        raw_storage: Optional[RawStorageManager] = None,
        parquet_storage: Optional[ParquetStorageManager] = None,
        metadata_dir: Optional[Path] = None,
    ):
        root_dir = get_repo_root()
        self.raw_storage = raw_storage or RawStorageManager(root_dir / "data" / "raw")
        self.parquet_storage = parquet_storage or ParquetStorageManager(root_dir / "data" / "processed")
        self.metadata_dir = metadata_dir or (root_dir / "data" / "metadata")
        
        self.runs_dir = self.metadata_dir / "runs"
        self.manifests_dir = self.metadata_dir / "manifests"
        self.coverage_dir = self.metadata_dir / "coverage"
        self.runs_dir.mkdir(parents=True, exist_ok=True)
        self.manifests_dir.mkdir(parents=True, exist_ok=True)
        self.coverage_dir.mkdir(parents=True, exist_ok=True)

    def generate_run_id(self, source_id: str) -> str:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        short_uuid = uuid.uuid4().hex[:6]
        return f"run_{source_id}_{timestamp}_{short_uuid}"

    def get_run(self, run_id: str) -> Optional[IngestionRun]:
        run_file = self.runs_dir / f"{run_id}.json"
        if not run_file.exists():
            return None
        try:
            with open(run_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return IngestionRun(**data)
        except Exception as e:
            logger.error(f"Error reading ingestion run file {run_file}: {e}")
            return None

    def list_runs(self, limit: int = 50) -> List[IngestionRun]:
        runs: List[IngestionRun] = []
        for file in sorted(self.runs_dir.glob("run_*.json"), key=lambda p: p.stat().st_mtime, reverse=True)[:limit]:
            try:
                with open(file, "r", encoding="utf-8") as f:
                    runs.append(IngestionRun(**json.load(f)))
            except Exception as e:
                logger.error(f"Error loading run file {file}: {e}")
        return runs

    def save_run(self, run: IngestionRun) -> None:
        run_file = self.runs_dir / f"{run.run_id}.json"
        with open(run_file, "w", encoding="utf-8") as f:
            f.write(run.model_dump_json(indent=2))

    def ingest_match_files(
        self,
        source_id: str,
        competition_id: str,
        season: str,
        file_paths: List[Path],
    ) -> IngestionRun:
        """
        Executes a complete ingestion run over a list of raw Cricsheet JSON match files.
        """
        start_time = time.perf_counter()
        started_at = datetime.now(timezone.utc)
        run_id = self.generate_run_id(source_id)

        source_info = source_registry.get_source(source_id)
        if not source_info:
            raise ValueError(f"Unregistered source_id: '{source_id}'")

        run = IngestionRun(
            run_id=run_id,
            source_id=source_id,
            competition_id=competition_id,
            season=season,
            status="IN_PROGRESS",
            started_at=started_at,
        )
        self.save_run(run)

        acquired_files: List[FileArtifactMetadata] = []
        all_deliveries: List[Dict[str, Any]] = []
        all_matches: List[Dict[str, Any]] = []
        aggregated_validation = ValidationSummary(
            total_records=0,
            valid_records=0,
            rejected_records=0,
            warning_count=0,
            duplicate_records_detected=0,
            completeness_percentage=100.0,
            passed=True,
        )

        idempotent_skips = 0

        try:
            for file_path in file_paths:
                if not file_path.exists():
                    logger.warning(f"File not found: {file_path}")
                    continue

                # 1. Store into raw partitions and calculate SHA-256
                raw_meta, is_new = self.raw_storage.store_raw_file(
                    source_path=file_path,
                    subfolder=f"matches/{competition_id}/{season}",
                    target_filename=file_path.name,
                )
                if not is_new:
                    idempotent_skips += 1

                # 2. Parse JSON
                with open(file_path, "r", encoding="utf-8") as f:
                    try:
                        raw_match_data = json.load(f)
                    except json.JSONDecodeError as e:
                        logger.error(f"Malformed JSON in {file_path}: {e}")
                        continue

                match_id = file_path.stem
                raw_meta.record_count = 1
                acquired_files.append(raw_meta)

                # 3. Validation
                val_summary = CricketDataValidator.validate_cricsheet_match_dict(raw_match_data, match_id)
                aggregated_validation.total_records += val_summary.total_records
                aggregated_validation.valid_records += val_summary.valid_records
                aggregated_validation.rejected_records += val_summary.rejected_records
                aggregated_validation.warning_count += val_summary.warning_count
                aggregated_validation.duplicate_records_detected += val_summary.duplicate_records_detected
                aggregated_validation.errors.extend(val_summary.errors[:5])  # Cap sample errors

                if not val_summary.passed:
                    aggregated_validation.passed = False
                    logger.warning(f"Validation failed for {match_id}: {val_summary.rejected_records} errors.")
                    continue

                # 4. Normalization
                source_ref = SourceReference(
                    source_id=source_id,
                    source_url_or_file=str(file_path),
                    ingested_at=started_at,
                    checksum_sha256=raw_meta.checksum_sha256,
                )

                deliveries = CricketDataNormalizer.flatten_match_deliveries(raw_match_data, match_id, source_ref)
                match_summary = CricketDataNormalizer.extract_match_summary(raw_match_data, match_id, source_ref)

                all_deliveries.extend(deliveries)
                all_matches.append(match_summary)

            # 5. Columnar Parquet Export
            parquet_paths: List[str] = []
            if all_deliveries:
                p_path = self.parquet_storage.write_deliveries_parquet(all_deliveries, season)
                parquet_paths.append(str(p_path))

            if all_matches:
                m_path = self.parquet_storage.write_matches_parquet(all_matches)
                parquet_paths.append(str(m_path))

            # Recalculate completeness
            if aggregated_validation.total_records > 0:
                aggregated_validation.completeness_percentage = round(
                    (aggregated_validation.valid_records / aggregated_validation.total_records) * 100, 2
                )

            duration = round(time.perf_counter() - start_time, 2)
            run.completed_at = datetime.now(timezone.utc)
            run.duration_seconds = duration
            run.status = "COMPLETED" if aggregated_validation.passed else "PARTIALLY_COMPLETED"
            run.files_acquired = acquired_files
            run.validation = aggregated_validation
            run.idempotent_skips = idempotent_skips
            run.metadata = {
                "matches_processed": len(all_matches),
                "deliveries_indexed": len(all_deliveries),
                "parquet_files": parquet_paths,
            }

            self.save_run(run)

            # 6. Save Dataset Manifest
            manifest = DatasetManifest(
                dataset_id=f"{competition_id}_{season}_ball_by_ball",
                competition_id=competition_id,
                season=season,
                source_id=source_id,
                version="1.0.0",
                created_at=started_at,
                updated_at=datetime.now(timezone.utc),
                run_id=run_id,
                raw_files=acquired_files,
                processed_parquet_paths=parquet_paths,
                total_matches=len(all_matches),
                total_deliveries=len(all_deliveries),
                validation_status="VALIDATED" if aggregated_validation.passed else "REJECTED",
                completeness_percentage=aggregated_validation.completeness_percentage,
            )
            self._save_manifest(manifest)
            self.update_coverage_report()

            return run

        except Exception as exc:
            logger.error(f"Ingestion run {run_id} failed catastrophically: {exc}", exc_info=True)
            run.status = "FAILED"
            run.completed_at = datetime.now(timezone.utc)
            run.duration_seconds = round(time.perf_counter() - start_time, 2)
            run.error_message = str(exc)
            self.save_run(run)
            return run

    def _save_manifest(self, manifest: DatasetManifest) -> None:
        manifest_path = self.manifests_dir / f"{manifest.dataset_id}.json"
        with open(manifest_path, "w", encoding="utf-8") as f:
            f.write(manifest.model_dump_json(indent=2))

    def list_manifests(self) -> List[DatasetManifest]:
        manifests: List[DatasetManifest] = []
        for file in self.manifests_dir.glob("*.json"):
            try:
                with open(file, "r", encoding="utf-8") as f:
                    manifests.append(DatasetManifest(**json.load(f)))
            except Exception as e:
                logger.error(f"Error loading manifest {file}: {e}")
        return manifests

    def get_manifest(self, dataset_id: str) -> Optional[DatasetManifest]:
        manifest_path = self.manifests_dir / f"{dataset_id}.json"
        if not manifest_path.exists():
            return None
        try:
            with open(manifest_path, "r", encoding="utf-8") as f:
                return DatasetManifest(**json.load(f))
        except Exception as e:
            logger.error(f"Error loading manifest {manifest_path}: {e}")
            return None

    def update_coverage_report(self) -> OverallCoverageReport:
        """Calculates global dataset coverage across tournaments and IPL 2026."""
        stats = self.parquet_storage.get_storage_stats()
        manifests = self.list_manifests()

        # Competition breakdowns
        comp_map: Dict[str, CompetitionCoverage] = {}

        # Default IPL 2026 target
        comp_map["ipl_2026"] = CompetitionCoverage(
            competition_id="ipl",
            competition_name="Indian Premier League",
            season="2026",
            total_scheduled_matches=74,
            matches_acquired=0,
            ball_by_ball_available=0,
            scorecards_available=0,
            squads_available=True,  # Retained squads announced
            status="PARTIALLY_ACQUIRED",
            data_gaps=["In-season 2026 live match deliveries commence with tournament kickoff."]
        )

        for m in manifests:
            cid = f"{m.competition_id}_{m.season}"
            comp_map[cid] = CompetitionCoverage(
                competition_id=m.competition_id,
                competition_name="Indian Premier League" if m.competition_id == "ipl" else m.competition_id.upper(),
                season=m.season,
                matches_acquired=m.total_matches,
                ball_by_ball_available=m.total_deliveries,
                scorecards_available=m.total_matches,
                squads_available=True,
                status="ACQUIRED" if m.total_matches > 0 else "UNAVAILABLE",
                data_gaps=[]
            )

        report = OverallCoverageReport(
            generated_at=datetime.now(timezone.utc),
            primary_season="IPL 2026",
            competitions=list(comp_map.values()),
            total_matches_acquired=stats["total_matches_indexed"],
            total_deliveries_indexed=stats["total_deliveries_indexed"],
            total_players_registered=0,
            sources_active=len(source_registry.list_sources()),
        )

        coverage_file = self.coverage_dir / "coverage_report.json"
        with open(coverage_file, "w", encoding="utf-8") as f:
            f.write(report.model_dump_json(indent=2))

        return report

    def get_coverage_report(self) -> OverallCoverageReport:
        coverage_file = self.coverage_dir / "coverage_report.json"
        if coverage_file.exists():
            try:
                with open(coverage_file, "r", encoding="utf-8") as f:
                    return OverallCoverageReport(**json.load(f))
            except Exception as e:
                logger.error(f"Error reading coverage report {coverage_file}: {e}")
        return self.update_coverage_report()


# Singleton orchestrator
orchestrator = IngestionOrchestrator()
