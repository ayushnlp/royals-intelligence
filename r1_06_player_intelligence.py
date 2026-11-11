"""
ROYALS INTELLIGENCE — TASK R1-06 PLAYER INTELLIGENCE RUNNER
Architecture: ROYALS INTELLIGENCE v4.1
Root-level master runner for R1-06 Evidence-Backed Player Reliability Intelligence & Ranking Engine
"""

import sys
from pathlib import Path

# Ensure project root is in sys.path
root_dir = Path(__file__).resolve().parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from round1_pressure.src.r1_06_player_intelligence import PlayerIntelligenceEngine
from round1_pressure.src.r1_06_candidate_selection import CandidateSelectionEngine
from round1_pressure.src.r1_06_explainability import ExplainabilityEngine

if __name__ == "__main__":
    print("=" * 80)
    print("ROYALS INTELLIGENCE — TASK R1-06 PLAYER RELIABILITY INTELLIGENCE & RANKING")
    print("Architecture: ROYALS INTELLIGENCE v4.1")
    print("=" * 80)

    # Step 1: Intelligence Engine
    print("\n[Step 1/3] Generating comprehensive batting and bowling intelligence...")
    intel_engine = PlayerIntelligenceEngine()
    intel_engine.run_all()
    intel_outputs = intel_engine.save_intelligence_datasets()
    for name, p in intel_outputs.items():
        print(f"  - {name}: {p}")

    # Step 2: Candidate Selection & Leaderboard Engine
    print("\n[Step 2/3] Generating official leaderboards, shortlists, and robustness analysis...")
    selection_engine = CandidateSelectionEngine(
        batting_intel_df=intel_engine.batting_intelligence_df,
        bowling_intel_df=intel_engine.bowling_intelligence_df,
    )
    selection_engine.run_all()
    selection_outputs = selection_engine.save_selection_datasets()
    for name, p in selection_outputs.items():
        print(f"  - {name}: {p}")

    # Step 3: Explainability & Reporting Engine
    print("\n[Step 3/3] Generating deterministic evidence profiles and analytical reports...")
    explain_engine = ExplainabilityEngine(
        bat_leaderboard_df=selection_engine.bat_leaderboard_df,
        bowl_leaderboard_df=selection_engine.bowl_leaderboard_df,
        robustness_df=selection_engine.shortlist_robustness_df,
    )
    explain_engine.build_all_profiles()
    report_outputs = explain_engine.generate_all_reports()
    for name, p in report_outputs.items():
        print(f"  - {name}: {p}")

    print("\n" + "=" * 80)
    print("TASK R1-06 COMPLETED SUCCESSFULLY.")
    print("=" * 80)
