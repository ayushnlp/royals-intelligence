#!/usr/bin/env python3
"""
Royals Intelligence - Match Ingestion CLI Script
Executes data acquisition, structural & cricket validation, normalization, and Parquet storage.
"""

import sys
import argparse
from pathlib import Path

# Add backend to Python path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR / "backend"))

from app.acquisition.orchestration.orchestrator import orchestrator
from app.acquisition.registry import source_registry


def main():
    parser = argparse.ArgumentParser(description="Ingest cricket match files into Royals Intelligence.")
    parser.add_argument(
        "--source-id",
        type=str,
        default="cricsheet_open",
        help="Registered source identifier (default: cricsheet_open)",
    )
    parser.add_argument(
        "--competition",
        type=str,
        default="ipl",
        help="Competition identifier (default: ipl)",
    )
    parser.add_argument(
        "--season",
        type=str,
        default="2024",
        help="Season identifier (default: 2024)",
    )
    parser.add_argument(
        "--input-dir",
        type=str,
        default="data/raw/public/samples",
        help="Directory containing raw JSON match files",
    )

    args = parser.parse_args()
    input_path = ROOT_DIR / args.input_dir

    if not input_path.exists():
        print(f"Error: Input directory '{input_path}' does not exist.")
        sys.exit(1)

    json_files = list(input_path.glob("*.json"))
    if not json_files:
        print(f"No JSON match files found in '{input_path}'.")
        sys.exit(0)

    print("=" * 65)
    print("ROYALS INTELLIGENCE — DATA ACQUISITION & INGESTION ENGINE")
    print("=" * 65)
    print(f"Source ID       : {args.source_id}")
    print(f"Competition     : {args.competition}")
    print(f"Season          : {args.season}")
    print(f"Match Files     : {len(json_files)} discovered")
    print("-" * 65)

    run = orchestrator.ingest_match_files(
        source_id=args.source_id,
        competition_id=args.competition,
        season=args.season,
        file_paths=json_files,
    )

    print(f"Run ID          : {run.run_id}")
    print(f"Status          : {run.status}")
    print(f"Duration        : {run.duration_seconds}s")
    print(f"Idempotent Skips: {run.idempotent_skips}")

    if run.validation:
        val = run.validation
        print(f"Validation      : {'PASSED' if val.passed else 'FAILED'}")
        print(f"Completeness    : {val.completeness_percentage}%")
        print(f"Total Checks    : {val.total_records}")
        print(f"Valid Checks    : {val.valid_records}")
        print(f"Errors/Warnings : {val.rejected_records} errors, {val.warning_count} warnings")

    print(f"Matches Indexed : {run.metadata.get('matches_processed', 0)}")
    print(f"Deliveries Parquet: {run.metadata.get('deliveries_indexed', 0)} rows")
    print("=" * 65)


if __name__ == "__main__":
    main()

