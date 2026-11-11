"""
ROYALS INTELLIGENCE — ROUND 1 EXPECTED PERFORMANCE RUNNER
Task: R1-04 Expected Performance Baselines & Bayesian Reliability Foundation

Standalone executable runner that loads pressure datasets, builds stratified ordinary
baselines, computes player differentials under pressure, fits hierarchical empirical
Bayes shrinkage, executes chronological validation, saves Parquet datasets, and generates
the Markdown analytical report.
"""

import sys
import time
from pathlib import Path

# Add project root to path
base_dir = Path(__file__).resolve().parent.parent.parent
if str(base_dir) not in sys.path:
    sys.path.insert(0, str(base_dir))

from round1_pressure.src.expected_performance import ExpectedPerformanceEngine


def main():
    print("=" * 80)
    print("ROYALS INTELLIGENCE — ROUND 1 EXPECTED PERFORMANCE & BAYESIAN RUNNER")
    print("Task: R1-04 Expected Performance Baselines & Bayesian Reliability Foundation")
    print("=" * 80)

    start_time = time.time()
    engine = ExpectedPerformanceEngine()

    print("[1/5] Loading pressure classification datasets...")
    engine.load_pressure_datasets()

    print("[2/5] Building stratified ordinary baselines (Batting & Bowling)...")
    engine.build_ordinary_batting_baseline(engine.bat_events_strict)
    engine.build_ordinary_bowling_baseline(engine.bowl_events_strict)

    print("[3/5] Computing player differentials & Empirical Bayes shrinkage...")
    engine.bat_differentials_strict = engine.compute_batting_differentials(
        engine.bat_events_strict, engine.bat_baseline_df
    )
    engine.bowl_differentials_strict = engine.compute_bowling_differentials(
        engine.bowl_events_strict, engine.bowl_baseline_df
    )

    # Permissive scenario for sensitivity analysis
    base_bat_perm = engine.build_ordinary_batting_baseline(engine.bat_events_perm)
    base_bowl_perm = engine.build_ordinary_bowling_baseline(engine.bowl_events_perm)
    engine.bat_differentials_perm = engine.compute_batting_differentials(
        engine.bat_events_perm, base_bat_perm
    )
    engine.bowl_differentials_perm = engine.compute_bowling_differentials(
        engine.bowl_events_perm, base_bowl_perm
    )

    print("[4/5] Executing Chronological Out-of-Sample Validation & Hyperparameter Summary...")
    engine.build_bayesian_hyperparameter_summary()
    engine.run_chronological_validation()
    engine.compute_qualification_sensitivity()

    print("[5/5] Saving Parquet Output Datasets & Generating Report...")
    saved_paths = engine.save_parquet_outputs()
    report_path = engine.generate_markdown_report()

    elapsed = time.time() - start_time
    print("\n" + "=" * 80)
    print("[SUCCESS] Expected Performance & Bayesian Modeling Complete!")
    print(f"Elapsed Time: {elapsed:.2f} seconds")
    print(f"Batting Players Evaluated: {len(engine.bat_differentials_strict)} ({engine.bat_differentials_strict['is_qualified'].sum()} qualified)")
    print(f"Bowling Players Evaluated: {len(engine.bowl_differentials_strict)} ({engine.bowl_differentials_strict['is_qualified'].sum()} qualified)")
    print("\nGenerated Parquet Datasets:")
    for name, p in saved_paths.items():
        print(f"  - {name}: {p}")
    print(f"\nAnalytical Report Generated: {report_path}")
    print("=" * 80)


if __name__ == "__main__":
    main()

