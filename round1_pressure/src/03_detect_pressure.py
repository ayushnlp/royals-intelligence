"""
ROYALS INTELLIGENCE — ROUND 1 PRESSURE DETECTION RUNNER
Architecture: ROYALS INTELLIGENCE v4.1
Task: R1-03 Pressure Detection Runner

Command-line entry point to execute deterministic pressure detection across
all deliveries, generating all processed Parquet files and the Markdown analytical report.
"""

import sys
import time
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from round1_pressure.src.pressure_detection import PressureDetectionEngine


def main():
    print("=" * 80)
    print("ROYALS INTELLIGENCE — ROUND 1 PRESSURE DETECTION RUNNER")
    print("Task: R1-03 Pressure Detection and Situation Classification Engine")
    print("=" * 80)

    t0 = time.time()
    engine = PressureDetectionEngine()
    results = engine.run_pressure_detection()
    elapsed = time.time() - t0

    print("\n" + "=" * 80)
    print("[SUCCESS] Pressure Detection & Situation Classification Complete!")
    print(f"Elapsed Time: {elapsed:.2f} seconds")
    print(f"Primary Scope Deliveries Analyzed: {results['primary_scope_deliveries']:,}")
    print(f"Batting Pressure Deliveries (Composite High): {results['batting_pressure_deliveries']:,} ({results['batting_unique_players']} unique batters)")
    print(f"Bowling Pressure Deliveries (Composite High): {results['bowling_pressure_deliveries']:,} ({results['bowling_unique_players']} unique bowlers)")
    print("\nGenerated Parquet Artifacts:")
    for name, path in results["saved_paths"].items():
        print(f"  - {name}: {path}")
    print(f"\nReport Generated: {results['report_path']}")
    print("=" * 80)


if __name__ == "__main__":
    main()
