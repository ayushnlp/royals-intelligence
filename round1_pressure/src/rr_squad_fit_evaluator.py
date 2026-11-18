"""
Royals Intelligence - Stage R1-07.4 / Round 1 Final Submission
Rajasthan Royals Squad Fit Rating Evaluator & Weight Sensitivity Engine.

Computes multi-dimensional 0–100 squad fit ratings for shortlisted uncapped players
across 5 explicit dimensions and 4 sensitivity scenarios.
"""

from pathlib import Path
from typing import Dict, List, Any
import json
import pandas as pd
import numpy as np

BASE_DIR = Path(__file__).resolve().parent.parent.parent
PROCESSED_DIR = BASE_DIR / "round1_pressure" / "data" / "processed"

# Sensitivity Weight Scenarios
SCENARIOS = {
    "baseline": {
        "role_need": 0.30,
        "pressure_execution": 0.25,
        "phase_fit": 0.20,
        "complementarity": 0.15,
        "runway_value": 0.10,
    },
    "role_heavy": {
        "role_need": 0.40,
        "pressure_execution": 0.20,
        "phase_fit": 0.15,
        "complementarity": 0.15,
        "runway_value": 0.10,
    },
    "pressure_heavy": {
        "role_need": 0.20,
        "pressure_execution": 0.40,
        "phase_fit": 0.15,
        "complementarity": 0.15,
        "runway_value": 0.10,
    },
    "balanced": {
        "role_need": 0.20,
        "pressure_execution": 0.20,
        "phase_fit": 0.20,
        "complementarity": 0.20,
        "runway_value": 0.20,
    },
}

# Explicit Rubric Dimensions & Scoring for Uncapped Batters
BATTER_EVALUATIONS: Dict[int, Dict[str, Any]] = {
    8101: {  # Ashutosh Sharma
        "role_need": 95.0,
        "pressure_execution": 94.0,
        "phase_fit": 95.0,
        "complementarity": 88.0,
        "runway_value": 90.0,
        "tactical_rationale": "Elite death finisher (overs 16-20). Fills RR's critical domestic finishing vacancy behind Hetmyer/Parag. Enables playing an extra overseas bowler.",
        "primary_role": "Lower-Order Finisher (Overs 16-20)",
        "batting_hand": "Right-hand bat",
    },
    2756: {  # Shashank Singh
        "role_need": 92.0,
        "pressure_execution": 86.0,
        "phase_fit": 90.0,
        "complementarity": 85.0,
        "runway_value": 80.0,
        "tactical_rationale": "High-composure middle/death counter-attacker. Proven ability to rescue collapses under high chase pressure.",
        "primary_role": "Middle-to-Lower Order Accelerator",
        "batting_hand": "Right-hand bat",
    },
    3926: {  # Rahul Tewatia
        "role_need": 88.0,
        "pressure_execution": 85.0,
        "phase_fit": 92.0,
        "complementarity": 90.0,
        "runway_value": 75.0,
        "tactical_rationale": "Proven IPL match-winner under extreme death pressure. Left-hand bat + leg-spin utility complements RR squad balance.",
        "primary_role": "Finishing All-Rounder (LH Bat / Leg Break)",
        "batting_hand": "Left-hand bat",
    },
    47370: {  # Aniket Verma
        "role_need": 68.0,
        "pressure_execution": 68.0,
        "phase_fit": 70.0,
        "complementarity": 72.0,
        "runway_value": 85.0,
        "tactical_rationale": "Young domestic talent with high raw ceiling, but limited sample in top-tier franchise death overs.",
        "primary_role": "Developmental Middle-Order Batter",
        "batting_hand": "Right-hand bat",
    },
    6460: {  # Ayush Badoni
        "role_need": 78.0,
        "pressure_execution": 62.0,
        "phase_fit": 75.0,
        "complementarity": 82.0,
        "runway_value": 88.0,
        "tactical_rationale": "Adaptable middle-order floater and spin player, but primary diagnostic indicates negative pressure delta in death phases.",
        "primary_role": "Middle-Order Floater / Spin Stabilizer",
        "batting_hand": "Right-hand bat",
    },
    4821: {  # Mahipal Lomror
        "role_need": 72.0,
        "pressure_execution": 58.0,
        "phase_fit": 72.0,
        "complementarity": 80.0,
        "runway_value": 82.0,
        "tactical_rationale": "Left-handed spin hitter with past RR familiarity, but negative pressure delta and moderate consistency.",
        "primary_role": "Middle-Order Left-Hand Spin Striker",
        "batting_hand": "Left-hand bat",
    },
    7446: {  # Abdul Samad
        "role_need": 80.0,
        "pressure_execution": 55.0,
        "phase_fit": 82.0,
        "complementarity": 78.0,
        "runway_value": 85.0,
        "tactical_rationale": "High-batting-speed boundary hitter, but persistent dot-ball accumulation and negative empirical pressure metric.",
        "primary_role": "Lower-Order Power Hitter",
        "batting_hand": "Right-hand bat",
    },
    3782: {  # M Shahrukh Khan
        "role_need": 80.0,
        "pressure_execution": 54.0,
        "phase_fit": 80.0,
        "complementarity": 78.0,
        "runway_value": 78.0,
        "tactical_rationale": "Designated finisher with power against pace, but high dismissal rate under extreme pressure situations.",
        "primary_role": "Lower-Order Power Striker",
        "batting_hand": "Right-hand bat",
    },
    25139: {  # Shubham Dubey
        "role_need": 82.0,
        "pressure_execution": 54.0,
        "phase_fit": 78.0,
        "complementarity": 85.0,
        "runway_value": 86.0,
        "tactical_rationale": "Already in RR roster; left-handed middle-order finisher. Strong squad continuity and domestic synergy.",
        "primary_role": "Left-Handed Middle/Death Finisher",
        "batting_hand": "Left-hand bat",
    },
    8238: {  # Sameer Rizvi (Exploratory Reserve)
        "role_need": 74.0,
        "pressure_execution": 52.0,
        "phase_fit": 70.0,
        "complementarity": 75.0,
        "runway_value": 90.0,
        "tactical_rationale": "High-ceiling U23 spin-hitter, strong development asset, though sample size under extreme IPL pressure remains low.",
        "primary_role": "Developmental Middle-Order Spin Striker",
        "batting_hand": "Right-hand bat",
    },
    6467: {  # Anuj Rawat
        "role_need": 84.0,
        "pressure_execution": 54.0,
        "phase_fit": 78.0,
        "complementarity": 84.0,
        "runway_value": 84.0,
        "tactical_rationale": "Left-handed wicketkeeper-batter, aggressive middle-to-death striker. Fills domestic middle-order finishing depth and backup keeper slot behind Samson.",
        "primary_role": "Wicketkeeper / Middle-Order Finisher",
        "batting_hand": "Left-hand bat",
    },
    19714: {  # Abishek Porel
        "role_need": 80.0,
        "pressure_execution": 52.0,
        "phase_fit": 74.0,
        "complementarity": 80.0,
        "runway_value": 92.0,
        "tactical_rationale": "Dynamic young left-handed wicketkeeper-batter. Strong top-to-middle order versatility with high multi-year runway value.",
        "primary_role": "Top/Middle Order Dynamic Striker (WK)",
        "batting_hand": "Left-hand bat",
    },
}

# Explicit Rubric Dimensions & Scoring for Uncapped Bowlers
BOWLER_EVALUATIONS: Dict[int, Dict[str, Any]] = {
    8746: {  # Vaibhav Arora
        "role_need": 92.0,
        "pressure_execution": 88.0,
        "phase_fit": 92.0,
        "complementarity": 88.0,
        "runway_value": 88.0,
        "tactical_rationale": "Elite domestic seam option. Excellent new-ball swing + disciplined death overs. Directly covers RR pace depth without using an overseas slot.",
        "primary_role": "Powerplay & Death Seamer",
        "bowling_type": "Right-arm fast-medium",
    },
    6669: {  # Mohsin Khan
        "role_need": 94.0,
        "pressure_execution": 84.0,
        "phase_fit": 90.0,
        "complementarity": 95.0,
        "runway_value": 85.0,
        "tactical_rationale": "Left-arm pace with steep bounce. Perfect tactical complement to Sandeep Sharma's right-arm swing; fills crucial left-arm pace void.",
        "primary_role": "Left-Arm Fast-Medium (PP & Death)",
        "bowling_type": "Left-arm fast-medium",
    },
    8177: {  # Akash Madhwal
        "role_need": 88.0,
        "pressure_execution": 84.0,
        "phase_fit": 95.0,
        "complementarity": 84.0,
        "runway_value": 82.0,
        "tactical_rationale": "Specialist death-overs yorker bowler. Proven high-pressure match-winner in IPL playoff scenarios.",
        "primary_role": "Death Overs Yorker Specialist",
        "bowling_type": "Right-arm medium-fast",
    },
    6237: {  # Manimaran Siddharth
        "role_need": 85.0,
        "pressure_execution": 82.0,
        "phase_fit": 88.0,
        "complementarity": 90.0,
        "runway_value": 84.0,
        "tactical_rationale": "Powerplay left-arm orthodox spinner. Elite dot-ball control and high containment against top-order right-handers; complements Bishnoi.",
        "primary_role": "Powerplay Spin Specialist (Slow Left-Arm)",
        "bowling_type": "Slow left-arm orthodox",
    },
    36982: {  # Suyash Sharma
        "role_need": 82.0,
        "pressure_execution": 80.0,
        "phase_fit": 82.0,
        "complementarity": 85.0,
        "runway_value": 92.0,
        "tactical_rationale": "Rapid leg-break and googly with deceptive trajectory. High strike-rate middle-overs weapon with immense multi-year runway.",
        "primary_role": "Attacking Middle-Overs Leg Spinner",
        "bowling_type": "Right-arm leg break / googly",
    },
    7327: {  # Rasikh Salam
        "role_need": 84.0,
        "pressure_execution": 80.0,
        "phase_fit": 86.0,
        "complementarity": 82.0,
        "runway_value": 85.0,
        "tactical_rationale": "Skilled change-of-pace seamer. Effective back-of-the-hand slower balls and hard lengths in death overs.",
        "primary_role": "Death Overs Seamer (Change of Pace)",
        "bowling_type": "Right-arm medium-fast",
    },
    23467: {  # Gurjapneet Singh
        "role_need": 85.0,
        "pressure_execution": 78.0,
        "phase_fit": 82.0,
        "complementarity": 92.0,
        "runway_value": 88.0,
        "tactical_rationale": "Tall left-arm seamer offering high release point and natural angle across right-handers; high tactical upside.",
        "primary_role": "Developmental Left-Arm Fast-Medium",
        "bowling_type": "Left-arm fast-medium",
    },
    25132: {  # Praful Hinge
        "role_need": 75.0,
        "pressure_execution": 76.0,
        "phase_fit": 78.0,
        "complementarity": 78.0,
        "runway_value": 82.0,
        "tactical_rationale": "Domestic seam bowler with disciplined lengths, though unproven in high-stakes franchise playoffs.",
        "primary_role": "Squad Seam Depth",
        "bowling_type": "Right-arm medium",
    },
    35318: {  # Sakib Hussain
        "role_need": 78.0,
        "pressure_execution": 74.0,
        "phase_fit": 80.0,
        "complementarity": 80.0,
        "runway_value": 88.0,
        "tactical_rationale": "Out-and-out raw pace prospect from Bihar. Capable of hitting 145+ km/h; high long-term ceiling.",
        "primary_role": "Express Pace Development Prospect",
        "bowling_type": "Right-arm fast",
    },
    6671: {  # Lalit Yadav (Exploratory Reserve)
        "role_need": 70.0,
        "pressure_execution": 72.0,
        "phase_fit": 72.0,
        "complementarity": 75.0,
        "runway_value": 78.0,
        "tactical_rationale": "Off-spinning utility all-rounder. Solid squad depth, though RR already features Parag and Jadeja in spin all-round roles.",
        "primary_role": "Utility Spin All-Rounder (Off Break)",
        "bowling_type": "Right-arm off break",
    },
    7325: {  # Harpreet Brar
        "role_need": 86.0,
        "pressure_execution": 76.0,
        "phase_fit": 84.0,
        "complementarity": 90.0,
        "runway_value": 82.0,
        "tactical_rationale": "Disciplined left-arm orthodox spinner and lower-order striker. High economy control against top-order right-handers; strong complementary matchup asset.",
        "primary_role": "Slow Left-Arm Orthodox Containment & Striker",
        "bowling_type": "Slow left-arm orthodox",
    },
    8530: {  # Kartik Tyagi
        "role_need": 86.0,
        "pressure_execution": 76.0,
        "phase_fit": 86.0,
        "complementarity": 84.0,
        "runway_value": 86.0,
        "tactical_rationale": "High-pace right-arm seamer (145+ km/h) with previous RR familiarity. Sharp yorkers and reverse swing execution in death overs.",
        "primary_role": "Express Pace & Death Yorker Specialist",
        "bowling_type": "Right-arm fast",
    },
    58134: {  # Digvesh Rathi
        "role_need": 74.0,
        "pressure_execution": 74.0,
        "phase_fit": 78.0,
        "complementarity": 78.0,
        "runway_value": 85.0,
        "tactical_rationale": "Attacking domestic leg-spinner with quick arm speed and googly variations. Provides squad wrist-spin depth.",
        "primary_role": "Attacking Wrist Spinner (Leg Break)",
        "bowling_type": "Right-arm leg break",
    },
}


def compute_squad_fit_ratings() -> pd.DataFrame:
    """Computes squad fit ratings across all 4 scenarios for the 20 shortlisted uncapped players."""
    bat_shortlist = pd.read_parquet(PROCESSED_DIR / "uncapped_batting_shortlist.parquet")
    bowl_shortlist = pd.read_parquet(PROCESSED_DIR / "uncapped_bowling_shortlist.parquet")

    records: List[Dict[str, Any]] = []

    # Process Batters
    for _, row in bat_shortlist.iterrows():
        pid = int(row["player_id"])
        eval_data = BATTER_EVALUATIONS.get(pid, {})
        rn = eval_data.get("role_need", 70.0)
        pe = eval_data.get("pressure_execution", 60.0)
        pf = eval_data.get("phase_fit", 70.0)
        sc = eval_data.get("complementarity", 70.0)
        rv = eval_data.get("runway_value", 75.0)

        # Compute scenario scores
        scores = {}
        for sname, w in SCENARIOS.items():
            score = (
                rn * w["role_need"]
                + pe * w["pressure_execution"]
                + pf * w["phase_fit"]
                + sc * w["complementarity"]
                + rv * w["runway_value"]
            )
            scores[f"score_{sname}"] = round(score, 2)

        records.append({
            "player_id": pid,
            "player_name": row["player_name"],
            "discipline": "Batting",
            "uncapped_rank": int(row["uncapped_rank"]),
            "primary_role": eval_data.get("primary_role", "Batter"),
            "skill_attribute": eval_data.get("batting_hand", "Right-hand bat"),
            "eligibility_status": row["eligibility_status"],
            "primary_diagnostic_name": row["primary_diagnostic_name"],
            "primary_diagnostic_value": row["primary_diagnostic_value"],
            "score_role_need": rn,
            "score_pressure_execution": pe,
            "score_phase_fit": pf,
            "score_complementarity": sc,
            "score_runway_value": rv,
            "rr_fit_rating": scores["score_baseline"],
            "score_role_heavy": scores["score_role_heavy"],
            "score_pressure_heavy": scores["score_pressure_heavy"],
            "score_balanced": scores["score_balanced"],
            "tactical_rationale": eval_data.get("tactical_rationale", ""),
        })

    # Process Bowlers
    for _, row in bowl_shortlist.iterrows():
        pid = int(row["player_id"])
        eval_data = BOWLER_EVALUATIONS.get(pid, {})
        rn = eval_data.get("role_need", 75.0)
        pe = eval_data.get("pressure_execution", 75.0)
        pf = eval_data.get("phase_fit", 75.0)
        sc = eval_data.get("complementarity", 75.0)
        rv = eval_data.get("runway_value", 80.0)

        # Compute scenario scores
        scores = {}
        for sname, w in SCENARIOS.items():
            score = (
                rn * w["role_need"]
                + pe * w["pressure_execution"]
                + pf * w["phase_fit"]
                + sc * w["complementarity"]
                + rv * w["runway_value"]
            )
            scores[f"score_{sname}"] = round(score, 2)

        records.append({
            "player_id": pid,
            "player_name": row["player_name"],
            "discipline": "Bowling",
            "uncapped_rank": int(row["uncapped_rank"]),
            "primary_role": eval_data.get("primary_role", "Bowler"),
            "skill_attribute": eval_data.get("bowling_type", "Right-arm medium"),
            "eligibility_status": row["eligibility_status"],
            "primary_diagnostic_name": row["primary_diagnostic_name"],
            "primary_diagnostic_value": row["primary_diagnostic_value"],
            "score_role_need": rn,
            "score_pressure_execution": pe,
            "score_phase_fit": pf,
            "score_complementarity": sc,
            "score_runway_value": rv,
            "rr_fit_rating": scores["score_baseline"],
            "score_role_heavy": scores["score_role_heavy"],
            "score_pressure_heavy": scores["score_pressure_heavy"],
            "score_balanced": scores["score_balanced"],
            "tactical_rationale": eval_data.get("tactical_rationale", ""),
        })

    df = pd.DataFrame(records)
    # Assign fit ranks within discipline
    df["fit_rank_discipline"] = df.groupby("discipline")["rr_fit_rating"].rank(ascending=False, method="min").astype(int)
    # Overall fit rank
    df["fit_rank_overall"] = df["rr_fit_rating"].rank(ascending=False, method="min").astype(int)

    return df


def save_squad_fit_outputs(df: pd.DataFrame):
    """Saves Parquet, CSV, and JSON outputs."""
    p_parquet = PROCESSED_DIR / "rr_squad_fit_ratings.parquet"
    p_csv = PROCESSED_DIR / "rr_squad_fit_ratings.csv"
    p_json = PROCESSED_DIR / "rr_squad_fit_ratings.json"

    df.to_parquet(p_parquet, index=False)
    df.to_csv(p_csv, index=False)
    with open(p_json, "w", encoding="utf-8") as f:
        json.dump(df.to_dict(orient="records"), f, indent=2)

    print(f"Exported Rajasthan Royals Squad Fit Ratings to {p_parquet}")


if __name__ == "__main__":
    df_fit = compute_squad_fit_ratings()
    save_squad_fit_outputs(df_fit)
    print("\n=== TOP 5 RR SQUAD FIT BATTERS ===")
    print(df_fit[df_fit["discipline"] == "Batting"].sort_values("rr_fit_rating", ascending=False)[
        ["fit_rank_discipline", "player_name", "rr_fit_rating", "score_role_need", "score_pressure_execution", "primary_role"]
    ].head(5).to_string())
    print("\n=== TOP 5 RR SQUAD FIT BOWLERS ===")
    print(df_fit[df_fit["discipline"] == "Bowling"].sort_values("rr_fit_rating", ascending=False)[
        ["fit_rank_discipline", "player_name", "rr_fit_rating", "score_role_need", "score_pressure_execution", "primary_role"]
    ].head(5).to_string())
