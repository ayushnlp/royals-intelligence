"""
Royals Intelligence - Stage R1-07.4 / Round 1 Final Submission
Supplementary Uncapped Indian Domestic Intelligence Extractor.

This module extracts and verifies the Top 10 uncapped Indian domestic batters and bowlers
under pressure from the protected Round 1 leaderboards and AUCTION-02 eligibility ledger.
"""

from pathlib import Path
from typing import Dict, List, Set, Any, Tuple, Optional
import json
import pandas as pd
import numpy as np

# Root directories
BASE_DIR = Path(__file__).resolve().parent.parent.parent
PROCESSED_DIR = BASE_DIR / "round1_pressure" / "data" / "processed"
AUCTION_DATA_DIR = BASE_DIR / "data" / "processed" / "auction_intelligence"
RAW_DATA_DIR = BASE_DIR / "data" / "raw" / "rajasthan_royals" / "round_1_data_pack"

# Explicit Senior Overseas Players (to prevent misclassification of overseas franchise stars)
OVERSEAS_INTERNATIONAL_PLAYERS: Set[str] = {
    "Sunil Narine", "Dwayne Bravo", "Kieron Pollard", "Andre Russell", "Shimron Hetmyer",
    "Nicholas Pooran", "David Miller", "Quinton de Kock", "Kagiso Rabada", "Anrich Nortje",
    "Lungi Ngidi", "Tabraiz Shamsi", "Keshav Maharaj", "Trent Boult", "Tim Southee",
    "Lockie Ferguson", "Mitchell Santner", "Glenn Phillips", "Kane Williamson", "Devon Conway",
    "Pat Cummins", "Mitchell Starc", "Josh Hazlewood", "Adam Zampa", "Glenn Maxwell",
    "Marcus Stoinis", "Travis Head", "David Warner", "Steve Smith", "Mitchell Marsh",
    "Jos Buttler", "Liam Livingstone", "Sam Curran", "Jofra Archer", "Mark Wood",
    "Reece Topley", "Adil Rashid", "Moeen Ali", "Jonny Bairstow", "Phil Salt",
    "Harry Brook", "Will Jacks", "Wanindu Hasaranga", "Maheesh Theekshana", "Matheesha Pathirana",
    "Dushmantha Chameera", "Dilshan Madushanka", "Nuwan Thushara", "Rashid Khan",
    "Noor Ahmad", "Fazalhaq Farooqi", "Naveen-ul-Haq", "Mujeeb Ur Rahman", "Mohammad Nabi",
    "Azmatullah Omarzai", "Mustafizur Rahman", "Shakib Al Hasan", "Taskin Ahmed",
    "Shoriful Islam", "Litton Das", "Rishad Hossain", "Towhid Hridoy", "Nasum Ahmed",
    "Hasan Mahmud", "Tanzim Hasan Sakib", "Sikandar Raza", "Richard Ngarava", "Blessing Muzarabani",
    "Josh Little", "Paul Stirling", "Mark Adair", "Curtis Campher", "Lorcan Tucker",
    "Harry Tector", "Ramon Simmonds", "Nathan Ellis", "Spencer Johnson", "Jhye Richardson",
    "Sean Abbott", "Ben Dwarshuis", "Daniel Sams", "Riley Meredith", "Jason Behrendorff",
    "Lance Morris", "Matthew Short", "Tim David", "Cameron Green", "Aaron Hardie",
    "Cooper Connolly", "Ashton Turner", "Ashton Agar", "Tanveer Sangha", "Matthew Kuhnemann",
    "Haris Rauf", "Shaheen Shah Afridi", "Shaheen Afridi", "Naseem Shah", "Shadab Khan",
    "Mohammad Rizwan", "Babar Azam", "Fakhar Zaman", "Iftikhar Ahmed", "Imad Wasim",
    "Mohammad Amir", "Usman Khan", "Roston Chase", "Sherfane Rutherford", "Romario Shepherd",
    "Alzarri Joseph", "Gudakesh Motie", "Akeal Hosein", "Shamar Joseph", "Obed McCoy",
    "Oshane Thomas", "Fabian Allen", "Kyle Mayers", "Shai Hope", "Brandon King",
    "Johnson Charles", "Evin Lewis", "Rovman Powell", "Donovan Ferreira", "Tristan Stubbs",
    "Heinrich Klaasen", "Aiden Markram", "Dewald Brevis", "Nandre Burger", "Gerald Coetzee",
    "Marco Jansen", "Lizaad Williams", "Bjorn Fortuin", "Wiaan Mulder", "Matthew Breetzke",
    "Ryan Rickelton", "Kwena Maphaka", "Ottneil Baartman", "Andile Phehlukwayo",
    "Corbin Bosch", "George Linde", "Senuran Muthusamy", "Sisanda Magala", "Wayne Parnell",
    "Andrew Tye", "Jason Holder", "Mujeeb-ur-Rahman", "Faf du Plessis"
}

# Known Capped Indian Internationals (Historical & Current across Test/ODI/T20I)
CAPPED_INDIAN_INTERNATIONALS: Set[str] = {
    "Jasprit Bumrah", "Mohammed Shami", "Mohammed Siraj", "Bhuvneshwar Kumar", "Umesh Yadav",
    "Ishant Sharma", "Deepak Chahar", "Shardul Thakur", "Navdeep Saini", "T Natarajan",
    "Prasidh Krishna", "Avesh Khan", "Arshdeep Singh", "Umran Malik", "Kuldeep Sen",
    "Shivam Mavi", "Mukesh Kumar", "Akash Deep", "Harshit Rana", "Mayank Yadav",
    "Chetan Sakariya", "Sandeep Sharma", "Jaydev Unadkat", "Khaleel Ahmed", "Varun Aaron",
    "Mohit Sharma", "Siddarth Kaul", "Barinder Sran", "Rishi Dhawan", "Ravichandran Ashwin",
    "Ravindra Jadeja", "Axar Patel", "Yuzvendra Chahal", "Kuldeep Yadav", "Rahul Chahar",
    "Ravi Bishnoi", "Varun Chakaravarthy", "Washington Sundar", "Shahbaz Ahmed",
    "Ravisrinivasan Sai Kishore", "Krunal Pandya", "Hardik Pandya", "Shivam Dube",
    "Nitish Kumar Reddy", "Nitish Reddy", "Vijay Shankar", "Venkatesh Iyer", "Piyush Chawla",
    "Amit Mishra", "Karn Sharma", "Mayank Markande", "Harbhajan Singh", "Virat Kohli",
    "Rohit Sharma", "KL Rahul", "Lokesh Rahul", "Shikhar Dhawan", "Ajinkya Rahane",
    "Cheteshwar Pujara", "Shreyas Iyer", "Suryakumar Yadav", "Rishabh Pant", "Sanju Samson",
    "Ishan Kishan", "Dinesh Karthik", "MS Dhoni", "Mahendra Singh Dhoni", "Robin Uthappa",
    "Ambati Rayudu", "Manish Pandey", "Kedar Jadhav", "Karun Nair", "Hanuma Vihari",
    "Prithvi Shaw", "Mayank Agarwal", "Devdutt Padikkal", "Ruturaj Gaikwad", "Shubman Gill",
    "Yashasvi Jaiswal", "Rinku Singh", "Tilak Varma", "Namboori Tilak Varma", "Jitesh Sharma",
    "Dhruv Jurel", "Sarfaraz Khan", "Rajat Patidar", "Abhishek Sharma", "Sai Sudharsan",
    "Nitish Rana", "Mandeep Singh", "Faiz Fazal", "Naman Dhir", "Ramandeep Singh",
    "Vipraj Nigam"
}


def load_eligibility_sources() -> Tuple[pd.DataFrame, pd.DataFrame, Set[int]]:
    """Loads canonical registry, eligibility ledger, and overseas player IDs."""
    ledger_path = AUCTION_DATA_DIR / "senior_international_eligibility_ledger.parquet"
    registry_path = AUCTION_DATA_DIR / "canonical_player_registry.parquet"
    mapping_path = RAW_DATA_DIR / "competition_team_player_mapping.csv"

    ledger_df = pd.read_parquet(ledger_path)
    registry_df = pd.read_parquet(registry_path)
    mapping_df = pd.read_csv(mapping_path)

    # Compile set of overseas player IDs from international competition mappings
    intl_teams = {
        "Australia", "England", "South Africa", "New Zealand", "West Indies",
        "Pakistan", "Sri Lanka", "Afghanistan", "Bangladesh", "Ireland", "Zimbabwe",
        "Netherlands", "Scotland", "Namibia", "Nepal", "United Arab Emirates", "Oman",
        "Canada", "United States Of America", "Singapore", "Hong Kong", "Kuwait", "Japan"
    }
    overseas_pids: Set[int] = set(mapping_df[mapping_df["team_name"].isin(intl_teams)]["player_id"].unique())

    # Augment with registry and ledger overseas annotations
    for _, r in ledger_df.iterrows():
        notes = f"{r.get('reviewer_notes', '')} {r.get('test_evidence_notes', '')} {r.get('t20i_evidence_notes', '')}"
        if "Overseas player" in notes:
            overseas_pids.add(int(r["canonical_id"]))

    for _, r in registry_df.iterrows():
        notes = f"{r.get('cap_evidence_notes', '')} {r.get('conflict_notes', '')}"
        if "Overseas" in notes:
            overseas_pids.add(int(r["canonical_id"]))

    return ledger_df, registry_df, overseas_pids


def extract_top10_uncapped_batters(strict_only: bool = True) -> pd.DataFrame:
    """Extracts the top 10 verified/pending uncapped Indian domestic batters."""
    bat_lb = pd.read_parquet(PROCESSED_DIR / "batting_leaderboard.parquet")
    ledger_df, registry_df, overseas_pids = load_eligibility_sources()
    led_lookup = ledger_df.set_index("canonical_id")["final_eligibility_state"].to_dict()

    candidates: List[Dict[str, Any]] = []
    # Rank order in leaderboard is descending by primary_diagnostic_value
    for _, row in bat_lb[bat_lb["is_qualified"] == True].sort_values("rank", ascending=True).iterrows():
        pid = int(row["player_id"])
        pname = str(row["player_name"]).strip()

        # Exclusions: Overseas stars, capped Indian internationals, or ledger-certified capped
        if pname in OVERSEAS_INTERNATIONAL_PLAYERS or pid in overseas_pids:
            continue
        if pname in CAPPED_INDIAN_INTERNATIONALS:
            continue
        led_status = led_lookup.get(pid, "UNKNOWN")
        if led_status == "VERIFIED_CAPPED":
            continue

        cand_qual = bool(row.get("is_candidate_qualified", False))
        if strict_only and not cand_qual:
            continue

        candidates.append({
            "uncapped_rank": len(candidates) + 1,
            "overall_rank": int(row["rank"]),
            "player_id": pid,
            "player_name": pname,
            "discipline": "Batting",
            "primary_diagnostic_name": row["primary_diagnostic_name"],
            "primary_diagnostic_value": float(row["primary_diagnostic_value"]),
            "posterior_mean": float(row["posterior_mean"]),
            "posterior_se": float(row["posterior_se"]),
            "ci_95_lower": float(row["ci_95_lower"]),
            "ci_95_upper": float(row["ci_95_upper"]),
            "ci_95_width": float(row["ci_95_width"]),
            "observed_strike_rate": float(row["observed_strike_rate"]),
            "expected_strike_rate": float(row["expected_strike_rate"]),
            "diff_strike_rate": float(row["diff_strike_rate"]),
            "diff_boundary_pct": float(row["diff_boundary_pct"]),
            "diff_dot_pct": float(row["diff_dot_pct"]),
            "diff_dismissal_pct": float(row["diff_dismissal_pct"]),
            "pressure_legal_balls": int(row["pressure_legal_balls"]),
            "pressure_matches": int(row["pressure_matches"]),
            "is_candidate_qualified": cand_qual,
            "evidence_volume_tier": str(row["evidence_volume_tier"]),
            "evidence_classification": str(row["evidence_classification"]),
            "eligibility_status": led_status,
            "senior_caps_count": 0,
            "domestic_association": get_domestic_association(pid, pname),
        })

        if len(candidates) >= 10:
            break

    df = pd.DataFrame(candidates)
    return df


def extract_top10_uncapped_bowlers(strict_only: bool = True) -> pd.DataFrame:
    """Extracts the top 10 verified/pending uncapped Indian domestic bowlers."""
    bowl_lb = pd.read_parquet(PROCESSED_DIR / "bowling_leaderboard.parquet")
    ledger_df, registry_df, overseas_pids = load_eligibility_sources()
    led_lookup = ledger_df.set_index("canonical_id")["final_eligibility_state"].to_dict()

    candidates: List[Dict[str, Any]] = []
    # Rank order in leaderboard is ascending by rank (Bumrah #1, etc.)
    for _, row in bowl_lb[bowl_lb["is_qualified"] == True].sort_values("rank", ascending=True).iterrows():
        pid = int(row["player_id"])
        pname = str(row["player_name"]).strip()

        # Exclusions: Overseas stars, capped Indian internationals, or ledger-certified capped
        if pname in OVERSEAS_INTERNATIONAL_PLAYERS or pid in overseas_pids:
            continue
        if pname in CAPPED_INDIAN_INTERNATIONALS:
            continue
        led_status = led_lookup.get(pid, "UNKNOWN")
        if led_status == "VERIFIED_CAPPED":
            continue

        cand_qual = bool(row.get("is_candidate_qualified", False))
        if strict_only and not cand_qual:
            continue

        candidates.append({
            "uncapped_rank": len(candidates) + 1,
            "overall_rank": int(row["rank"]),
            "player_id": pid,
            "player_name": pname,
            "discipline": "Bowling",
            "primary_diagnostic_name": row["primary_diagnostic_name"],
            "primary_diagnostic_value": float(row["primary_diagnostic_value"]),
            "posterior_mean": float(row["posterior_mean"]),
            "posterior_se": float(row["posterior_se"]),
            "ci_95_lower": float(row["ci_95_lower"]),
            "ci_95_upper": float(row["ci_95_upper"]),
            "ci_95_width": float(row["ci_95_width"]),
            "observed_economy": float(row["observed_economy"]),
            "expected_economy": float(row["expected_economy"]),
            "diff_economy": float(row["diff_economy"]),
            "diff_wicket_pct": float(row["diff_wicket_pct"]),
            "diff_dot_pct": float(row["diff_dot_pct"]),
            "diff_boundary_pct": float(row["diff_boundary_pct"]),
            "pressure_legal_balls": int(row["pressure_legal_balls"]),
            "pressure_matches": int(row["pressure_matches"]),
            "is_candidate_qualified": cand_qual,
            "evidence_volume_tier": str(row["evidence_volume_tier"]),
            "evidence_classification": str(row["evidence_classification"]),
            "eligibility_status": led_status,
            "senior_caps_count": 0,
            "domestic_association": get_domestic_association(pid, pname),
        })

        if len(candidates) >= 10:
            break

    df = pd.DataFrame(candidates)
    return df


def extract_exploratory_uncapped_reserves(discipline: str = "all") -> pd.DataFrame:
    """Extracts exploratory uncapped reserves (30 <= balls < 60 without 10 matches) with estimation disclosures."""
    ledger_df, registry_df, overseas_pids = load_eligibility_sources()
    led_lookup = ledger_df.set_index("canonical_id")["final_eligibility_state"].to_dict()

    reserves = []
    datasets = []
    if discipline in ("all", "batting"):
        datasets.append(("Batting", pd.read_parquet(PROCESSED_DIR / "batting_leaderboard.parquet")))
    if discipline in ("all", "bowling"):
        datasets.append(("Bowling", pd.read_parquet(PROCESSED_DIR / "bowling_leaderboard.parquet")))

    for disc, lb in datasets:
        for _, row in lb[lb["is_qualified"] == True].sort_values("rank", ascending=True).iterrows():
            pid = int(row["player_id"])
            pname = str(row["player_name"]).strip()
            if pname in OVERSEAS_INTERNATIONAL_PLAYERS or pid in overseas_pids or pname in CAPPED_INDIAN_INTERNATIONALS:
                continue
            if led_lookup.get(pid, "UNKNOWN") == "VERIFIED_CAPPED":
                continue
            cand_qual = bool(row.get("is_candidate_qualified", False))
            if cand_qual:
                continue  # Skip strictly qualified candidates

            reserves.append({
                "discipline": disc,
                "overall_rank": int(row["rank"]),
                "player_id": pid,
                "player_name": pname,
                "pressure_legal_balls": int(row["pressure_legal_balls"]),
                "pressure_matches": int(row["pressure_matches"]),
                "evidence_volume_tier": str(row["evidence_volume_tier"]),
                "primary_diagnostic_name": row["primary_diagnostic_name"],
                "primary_diagnostic_value": float(row["primary_diagnostic_value"]),
                "posterior_mean": float(row["posterior_mean"]),
                "posterior_se": float(row["posterior_se"]),
                "domestic_association": get_domestic_association(pid, pname),
                "qualification_category": "EXPLORATORY_RESERVE (<50 balls / <10 matches)",
                "sampling_uncertainty_note": f"High estimation variance (SE={float(row['posterior_se']):.2f}) due to limited pressure sample ({int(row['pressure_legal_balls'])} balls). Subject to small-sample shrinkage bias."
            })

    return pd.DataFrame(reserves)

    df = pd.DataFrame(candidates)
    return df


def get_domestic_association(pid: int, name: str) -> str:
    """Returns the Indian domestic association / franchise background for reporting."""
    mapping = {
        8101: "Railways / PBKS",
        2756: "Chhattisgarh / PBKS",
        3926: "Haryana / GT",
        47370: "Madhya Pradesh",
        6460: "Delhi / LSG",
        4821: "Rajasthan / RCB",
        7446: "Jammu & Kashmir / SRH",
        3782: "Tamil Nadu / GT",
        25139: "Vidarbha / RR",
        8238: "Uttar Pradesh / CSK",
        6237: "Tamil Nadu / LSG",
        8746: "Himachal Pradesh / KKR",
        23467: "Tamil Nadu / CSK",
        36982: "Delhi / KKR",
        8177: "Uttarakhand / MI",
        25132: "Maharashtra",
        7327: "Jammu & Kashmir / DC",
        6669: "Uttar Pradesh / LSG",
        35318: "Bihar / KKR",
        6671: "Delhi / DC",
        27964: "Haryana / MI",
        4487: "Karnataka / RCB",
    }
    return mapping.get(pid, "Indian Domestic")


def save_shortlists(bat_df: pd.DataFrame, bowl_df: pd.DataFrame, reserves_df: Optional[pd.DataFrame] = None):
    """Saves Parquet, CSV, and JSON representations in round1_pressure/data/processed."""
    # Batting
    bat_parquet = PROCESSED_DIR / "uncapped_batting_shortlist.parquet"
    bat_csv = PROCESSED_DIR / "uncapped_batting_shortlist.csv"
    bat_json = PROCESSED_DIR / "uncapped_batting_shortlist.json"
    bat_df.to_parquet(bat_parquet, index=False)
    bat_df.to_csv(bat_csv, index=False)
    with open(bat_json, "w", encoding="utf-8") as f:
        json.dump(bat_df.to_dict(orient="records"), f, indent=2)

    # Bowling
    bowl_parquet = PROCESSED_DIR / "uncapped_bowling_shortlist.parquet"
    bowl_csv = PROCESSED_DIR / "uncapped_bowling_shortlist.csv"
    bowl_json = PROCESSED_DIR / "uncapped_bowling_shortlist.json"
    bowl_df.to_parquet(bowl_parquet, index=False)
    bowl_df.to_csv(bowl_csv, index=False)
    with open(bowl_json, "w", encoding="utf-8") as f:
        json.dump(bowl_df.to_dict(orient="records"), f, indent=2)

    if reserves_df is not None:
        res_parquet = PROCESSED_DIR / "uncapped_exploratory_reserves.parquet"
        res_csv = PROCESSED_DIR / "uncapped_exploratory_reserves.csv"
        res_json = PROCESSED_DIR / "uncapped_exploratory_reserves.json"
        reserves_df.to_parquet(res_parquet, index=False)
        reserves_df.to_csv(res_csv, index=False)
        with open(res_json, "w", encoding="utf-8") as f:
            json.dump(reserves_df.to_dict(orient="records"), f, indent=2)
        print(f"Exported Exploratory Uncapped Reserves to {res_parquet}")

    print(f"Exported Top 10 uncapped batters to {bat_parquet}")
    print(f"Exported Top 10 uncapped bowlers to {bowl_parquet}")


if __name__ == "__main__":
    bat_df = extract_top10_uncapped_batters()
    bowl_df = extract_top10_uncapped_bowlers()
    reserves_df = extract_exploratory_uncapped_reserves()
    save_shortlists(bat_df, bowl_df, reserves_df)
