#!/usr/bin/env python3
"""
Royals Intelligence - Standalone Round 1 Dataset QA Runner
Script: 01_load_qa.py
Focus: Pressure Performance Dataset Audit & Quality Assurance
"""

import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from round1_pressure.src.load_qa import DatasetQAEngine


def main():
    print("=" * 70)
    print("ROYALS INTELLIGENCE — ROUND 1 DATASET QA RUNNER (01_load_qa.py)")
    print("Objective: Identify the Most Reliable Players Under Pressure")
    print("=" * 70)

    engine = DatasetQAEngine()
    results = engine.run_full_qa()

    print(f"\n[SUCCESS] Audit completed successfully.")
    print(f"Status: {results['overall_status']}")
    print(f"Files Profiled: {len(results['profiles'])}")
    print(f"Deliveries Analyzed: {results['profiles']['ball_by_ball']['row_count']:,}")
    print(f"Matches Profiled: {results['profiles']['matches']['row_count']:,}")
    print(f"JSON output: {engine.outputs_dir / 'qa_summary.json'}")
    print(f"Report: {engine.reports_dir / 'data_quality_report.md'}")


if __name__ == "__main__":
    main()
