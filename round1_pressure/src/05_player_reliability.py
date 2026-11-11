"""
ROYALS INTELLIGENCE — ROUND 1 EXPLAINABLE PLAYER PRESSURE RELIABILITY RUNNER
Task: R1-05 Explainable Player Pressure Reliability Scoring Engine

Standalone executable runner that loads all R1-03/R1-04 inputs, computes
explainable batting and bowling pressure reliability scores, evaluates
candidate scoring models, generates two-way all-rounder synthesis, saves
Parquet datasets, and produces the Markdown analytical report.
"""

import sys
import time
from pathlib import Path

# Add project root to path
base_dir = Path(__file__).resolve().parent.parent.parent
if str(base_dir) not in sys.path:
    sys.path.insert(0, str(base_dir))

from round1_pressure.src.player_reliability import PlayerReliabilityEngine


def main():
    print("=" * 80)
    print("ROYALS INTELLIGENCE — ROUND 1 PLAYER PRESSURE RELIABILITY SCORING RUNNER")
    print("Task: R1-05 Explainable Player Pressure Reliability Scoring Engine")
    print("=" * 80)

    start_time = time.time()
    engine = PlayerReliabilityEngine()

    print("[1/5] Loading processed datasets and Bayesian summaries...")
    engine.load_all_inputs()

    print("[2/5] Computing explainable batting pressure reliability scores...")
    engine.compute_batting_reliability()

    print("[3/5] Computing explainable bowling pressure reliability scores...")
    engine.compute_bowling_reliability()

    print("[4/5] Synthesizing all-rounder reliability & scoring model comparisons...")
    engine.compute_all_rounder_reliability()
    engine.compute_scoring_methodology_comparison()

    print("[5/5] Saving Parquet datasets and generating analytical report...")
    saved_paths = engine.save_parquet_outputs()
    report_path = engine.generate_markdown_report()

    elapsed = time.time() - start_time
    print("\n" + "=" * 80)
    print("[SUCCESS] Player Pressure Reliability Engine Complete!")
    print(f"Elapsed Time: {elapsed:.2f} seconds")
    print(f"Batters Evaluated: {len(engine.bat_reliability_df)} ({engine.bat_reliability_df['is_qualified'].sum()} qualified)")
    print(f"Bowlers Evaluated: {len(engine.bowl_reliability_df)} ({engine.bowl_reliability_df['is_qualified'].sum()} qualified)")
    print(f"All-Rounders Evaluated: {len(engine.all_rounder_df)} qualified in both")
    print("\nGenerated Parquet Datasets:")
    for name, p in saved_paths.items():
        print(f"  - {name}: {p}")
    print(f"\nAnalytical Report Generated: {report_path}")
    print("=" * 80)


if __name__ == "__main__":
    main()

