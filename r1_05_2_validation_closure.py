"""
ROYALS INTELLIGENCE — TASK R1-05.2 VALIDATION CLOSURE RUNNER
Architecture: ROYALS INTELLIGENCE v4.1
Root-level runner for R1-05.2 Statistical Validation Closure & Methodology Reconciliation
"""

import sys
from pathlib import Path

# Ensure project root is in sys.path
root_dir = Path(__file__).resolve().parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from round1_pressure.src.r1_05_2_validation_closure import ValidationClosureEngine

if __name__ == "__main__":
    print("=" * 80)
    print("ROYALS INTELLIGENCE — TASK R1-05.2 STATISTICAL VALIDATION CLOSURE")
    print("Architecture: ROYALS INTELLIGENCE v4.1")
    print("=" * 80)
    
    engine = ValidationClosureEngine()
    engine.run_all()
    
    outputs = engine.save_parquet_outputs()
    print("\nSaved Parquet Datasets:")
    for name, path in outputs.items():
        print(f"  - {name}: {path}")
        
    report = engine.generate_markdown_report()
    print(f"\nGenerated Validation Closure Report: {report}")
    print("=" * 80)
    print("TASK R1-05.2 VALIDATION CLOSURE COMPLETED SUCCESSFULLY.")
    print("=" * 80)
