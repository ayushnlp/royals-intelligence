"""
ROYALS INTELLIGENCE — TASK R1-05.1 INDEPENDENT STATISTICAL AUDIT RUNNER
Architecture: ROYALS INTELLIGENCE v4.1
"""

import sys
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from round1_pressure.src.r1_05_1_statistical_audit import StatisticalReliabilityAuditEngine

if __name__ == "__main__":
    print("=" * 80)
    print("ROYALS INTELLIGENCE — TASK R1-05.1 INDEPENDENT STATISTICAL AUDIT")
    print("Architecture: ROYALS INTELLIGENCE v4.1")
    print("=" * 80)
    engine = StatisticalReliabilityAuditEngine()
    engine.run_all()
    saved = engine.save_parquet_outputs()
    print("\nSaved Parquet Datasets:")
    for k, p in saved.items():
        print(f"  - {k}: {p}")
    rep = engine.generate_markdown_report()
    print(f"\nGenerated Audit Report: {rep}")
    print("=" * 80)
    print("TASK R1-05.1 AUDIT COMPLETED SUCCESSFULLY.")
    print("=" * 80)
