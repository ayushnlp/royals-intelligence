#!/usr/bin/env python3
"""
Royals Intelligence - Dataset Availability Verification Script
Checks whether required proprietary competition datasets (~68.2 MB) are present on disk.
Used by CI workflows and local test runners to determine if Groups B (data_dependent)
and C (data_integrity) can be executed.
"""

import sys
import os
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

# Minimum required files for Groups B & C execution
REQUIRED_DATASETS = [
    ROOT_DIR / "data" / "raw" / "rajasthan_royals" / "round_1_data_pack" / "ball_by_ball.csv",
    ROOT_DIR / "data" / "raw" / "rajasthan_royals" / "round_1_data_pack" / "matches.csv",
    ROOT_DIR / "data" / "raw" / "rajasthan_royals" / "round_1_data_pack" / "competition_team_player_mapping.csv",
    ROOT_DIR / "round1_pressure" / "data" / "processed" / "batting_leaderboard.parquet",
    ROOT_DIR / "round1_pressure" / "data" / "processed" / "bowling_leaderboard.parquet",
    ROOT_DIR / "data" / "processed" / "auction_intelligence" / "canonical_player_registry.parquet",
]


def check_dataset_availability():
    missing = [p for p in REQUIRED_DATASETS if not p.exists()]
    return len(missing) == 0, missing


def main():
    is_available, missing = check_dataset_availability()
    github_output = os.environ.get("GITHUB_OUTPUT")
    github_summary = os.environ.get("GITHUB_STEP_SUMMARY")

    if is_available:
        print("=" * 70)
        print("DATASET AVAILABILITY: HYDRATED AND VERIFIED")
        print("All required proprietary datasets and Parquet baselines are present.")
        print("Authorized to run:")
        print("  - Group B: Data-Dependent Integration Tests (103 tests)")
        print("  - Group C: Protected Dataset Integrity Tests (10 tests)")
        print("=" * 70)

        if github_output:
            with open(github_output, "a") as f:
                f.write("hydrated=true\n")
        return 0
    else:
        print("=" * 70)
        print("DATASET AVAILABILITY: NOT HYDRATED / BLOCKED")
        print("Proprietary competition datasets (~68.2 MB) are excluded by .gitignore")
        print("and not present in this runner environment.")
        print(f"Missing sample paths ({len(missing)} of {len(REQUIRED_DATASETS)} checked):")
        for m in missing[:4]:
            print(f"  - {m.relative_to(ROOT_DIR)}")
        print("\nTest Execution Impact:")
        print("  - Group A (Unit & Environment): 83 tests can run normally.")
        print("  - Group B (Data-Dependent):    103 tests BLOCKED (Hydration required)")
        print("  - Group C (Data Integrity):     10 tests BLOCKED (Hydration required)")
        print("=" * 70)

        if github_output:
            with open(github_output, "a") as f:
                f.write("hydrated=false\n")

        if github_summary:
            with open(github_summary, "a") as f:
                f.write("### ⚠️ Integration Tests Gated: Dataset Hydration Required\n\n")
                f.write("Proprietary competition datasets (~68.2 MB) are excluded by `.gitignore` ")
                f.write("and are not present in this runner environment (e.g. fork PR or missing credentials).\n\n")
                f.write("| Test Group | Test Count | Status |\n")
                f.write("| :--- | :---: | :--- |\n")
                f.write("| **Group A (Unit & Environment)** | **83** | **READY / EXECUTED** |\n")
                f.write("| **Group B (Data-Dependent Integration)** | **103** | **BLOCKED (Hydration Required)** |\n")
                f.write("| **Group C (Protected Integrity)** | **10** | **BLOCKED (Hydration Required)** |\n\n")
                f.write("> **Note:** Tests are not silently skipped. Integration and integrity suites require authenticated dataset hydration.\n")

        # In strict check mode, return non-zero
        if "--strict" in sys.argv:
            return 1
        return 0


if __name__ == "__main__":
    sys.exit(main())
