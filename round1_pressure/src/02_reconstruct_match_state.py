#!/usr/bin/env python3
"""
Royals Intelligence - Standalone Match-State Reconstruction Runner
Script: 02_reconstruct_match_state.py
Task: R1-02 Delivery-Level Match-State Reconstruction
"""

import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from round1_pressure.src.match_state import MatchStateEngine


def main():
    print("=" * 75)
    print("ROYALS INTELLIGENCE — ROUND 1 MATCH-STATE RECONSTRUCTION RUNNER")
    print("Objective: Delivery-Level State Immediately Before & After Every Ball")
    print("=" * 75)

    engine = MatchStateEngine()
    results = engine.run_reconstruction()

    print("\n[SUCCESS] Match-state reconstruction completed successfully.")
    print(f"Status: {results['status']}")
    print(f"Total Deliveries Accounted For: {results['strict_deliveries']:,}")
    print(f"Scenario A (Strict) Legal Deliveries: {results['strict_legal_deliveries']:,}")
    print(f"Scenario B (Permissive) Legal Deliveries: {results['permissive_legal_deliveries']:,}")
    print(f"Primary Scope Deliveries: {results['primary_deliveries']:,}")
    print(f"Innings Processed: {results['innings_count']:,}")
    print(f"Matches Processed: {results['matches_count']:,}")
    print(f"Excluded Records: {results['excluded_records']:,}")
    print(f"Audit Report: {results['report_path']}")


if __name__ == "__main__":
    main()
