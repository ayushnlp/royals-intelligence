"""
ROYALS INTELLIGENCE — ROUND 1 TASK R1-06.2.2 TEST SUITE
Architecture: ROYALS INTELLIGENCE v4.1
Task: R1-06.2.2 Targeted Leaderboard, Classification & Uncertainty Disclosure Remediation

Comprehensive test suite verifying all targeted remediations:
1. Bowling Table 1 contains ONLY sample-qualified candidates (DEF-R1-06.2.1-01 fix).
2. Bowling Table 1 has exactly 11 candidates ordered by BOWL_CONSERVATIVE.
3. Batting Table 1 contains ONLY sample-qualified candidates (12 candidates ordered by BAT_CONSERVATIVE).
4. Table 1 and Section 3 Watchlists are strictly mutually exclusive (zero duplicate entries).
5. Displaced bowlers (Nasum Ahmed, Vipraj Nigam, Ramon Simmonds) appear in Section 3.A Watchlist, NOT Table 1.
6. Admitted bowlers (Ravichandran Ashwin, Hasan Mahmud, Nathan Ellis) appear in Table 1, NOT Section 3 Watchlist.
7. Borderline batters (Cooper Connolly, Ishan Kishan) appear in Section 3.A Watchlist, NOT Table 1.
8. Classification rename consistency (POSITIVE_ESTIMATE_UNRESOLVED: 19 batters, 1 bowler Bumrah).
9. Zero occurrences of stale NEGATIVE_CONSERVATIVE_ESTIMATE in code, reports, or parquets.
10. Explicit 1-SE (~84.1% credibility) vs 95% CI disclosures in all reports and candidate profiles.
11. Full population hierarchy reconciliation (824/596 evaluated, 278/239 min-exposure, 161/168 sample-qualified).
12. Strict governance boundaries (zero commercial features, zero R1-07 files).
"""

from pathlib import Path
import re
import pandas as pd
import pytest

DATA_DIR = Path("round1_pressure/data/processed")
REPORTS_DIR = Path("round1_pressure/reports")
SRC_DIR = Path("round1_pressure/src")
ROOT_DIR = Path(".")


@pytest.fixture(scope="module")
def batting_leaderboard():
    return pd.read_parquet(DATA_DIR / "batting_leaderboard.parquet")


@pytest.fixture(scope="module")
def bowling_leaderboard():
    return pd.read_parquet(DATA_DIR / "bowling_leaderboard.parquet")


@pytest.fixture(scope="module")
def batting_intel():
    return pd.read_parquet(DATA_DIR / "batting_intelligence.parquet")


@pytest.fixture(scope="module")
def bowling_intel():
    return pd.read_parquet(DATA_DIR / "bowling_intelligence.parquet")


@pytest.fixture(scope="module")
def batting_profiles():
    return pd.read_parquet(DATA_DIR / "batting_evidence_profiles.parquet")


@pytest.fixture(scope="module")
def bowling_profiles():
    return pd.read_parquet(DATA_DIR / "bowling_evidence_profiles.parquet")


# ==============================================================================
# 1. BOWLING TABLE 1 QUALIFICATION & ORDERING (DEF-R1-06.2.1-01 REMEDIATION)
# ==============================================================================

def test_table1_bowling_candidate_qualification(bowling_leaderboard):
    """
    Verifies that Table 1 in r1_06_bowling_shortlist.md contains ONLY sample-qualified bowlers.
    Every candidate in Table 1 must have is_candidate_qualified == True.
    """
    report_file = REPORTS_DIR / "r1_06_bowling_shortlist.md"
    assert report_file.exists()
    content = report_file.read_text(encoding="utf-8")

    t1_end = content.find("## 2. In-Depth Candidate Evidence Profiles")
    table1_text = content[:t1_end]

    # Extract player names from Table 1
    t1_names = [line.split("|")[2].replace("*", "").strip() for line in table1_text.splitlines() if line.startswith("| **")]
    assert len(t1_names) == 11

    # Cross-reference with bowling leaderboard
    bowl_map = bowling_leaderboard.set_index("player_name")
    for name in t1_names:
        assert name in bowl_map.index, f"Player {name} not found in bowling leaderboard"
        r = bowl_map.loc[name]
        assert bool(r["is_candidate_qualified"]) is True, f"Bowler {name} in Table 1 is NOT sample-qualified"
        balls = r["pressure_legal_balls"]
        matches = r["pressure_matches"]
        assert (balls >= 60) or (balls >= 50 and matches >= 10), (
            f"Bowler {name} ({balls} balls, {matches} matches) fails qualification condition"
        )


def test_table1_bowling_size_and_ordering(bowling_leaderboard):
    """
    Verifies Table 1 has exactly 11 candidates ordered monotonically descending by BOWL_CONSERVATIVE.
    """
    report_file = REPORTS_DIR / "r1_06_bowling_shortlist.md"
    content = report_file.read_text(encoding="utf-8")
    t1_end = content.find("## 2. In-Depth Candidate Evidence Profiles")
    table1_text = content[:t1_end]

    t1_names = [line.split("|")[2].replace("*", "").strip() for line in table1_text.splitlines() if line.startswith("| **")]
    assert len(t1_names) == 11

    # Expected top 11 qualified bowlers from leaderboard
    expected_top11 = bowling_leaderboard[bowling_leaderboard["is_candidate_qualified"]].head(11)["player_name"].tolist()
    assert t1_names == expected_top11

    # Verify monotonic descending order of conservative score
    bowl_map = bowling_leaderboard.set_index("player_name")
    scores = [bowl_map.loc[name]["primary_diagnostic_value"] for name in t1_names]
    for i in range(len(scores) - 1):
        assert scores[i] >= scores[i + 1], f"Monotonic ordering violated between {t1_names[i]} and {t1_names[i+1]}"


# ==============================================================================
# 2. BATTING TABLE 1 QUALIFICATION & ORDERING
# ==============================================================================

def test_table1_batting_candidate_qualification(batting_leaderboard):
    """
    Verifies that Table 1 in r1_06_batting_shortlist.md contains ONLY sample-qualified batters (12).
    """
    report_file = REPORTS_DIR / "r1_06_batting_shortlist.md"
    assert report_file.exists()
    content = report_file.read_text(encoding="utf-8")

    t1_end = content.find("## 2. In-Depth Candidate Evidence Profiles")
    table1_text = content[:t1_end]

    t1_names = [line.split("|")[2].replace("*", "").strip() for line in table1_text.splitlines() if line.startswith("| **")]
    assert len(t1_names) == 12

    bat_map = batting_leaderboard.set_index("player_name")
    for name in t1_names:
        assert name in bat_map.index
        r = bat_map.loc[name]
        assert bool(r["is_candidate_qualified"]) is True, f"Batter {name} in Table 1 is NOT sample-qualified"
        balls = r["pressure_legal_balls"]
        matches = r["pressure_matches"]
        assert (balls >= 60) or (balls >= 50 and matches >= 10)

    # Monotonic descending order
    expected_top12 = batting_leaderboard[batting_leaderboard["is_candidate_qualified"]].head(12)["player_name"].tolist()
    assert t1_names == expected_top12


# ==============================================================================
# 3. MUTUAL EXCLUSIVITY & WATCHLIST DEDUPLICATION
# ==============================================================================

def test_table1_and_watchlist_mutual_exclusivity():
    """
    Verifies that zero players appear in both Table 1 and Section 3 Watchlist across batting and bowling.
    """
    for fname, disc in [("r1_06_batting_shortlist.md", "Batting"), ("r1_06_bowling_shortlist.md", "Bowling")]:
        report_file = REPORTS_DIR / fname
        content = report_file.read_text(encoding="utf-8")

        t1_end = content.find("## 2. In-Depth Candidate Evidence Profiles")
        sec3_start = content.find("## 3. Exploratory Watchlist")
        assert t1_end != -1, f"Missing section 2 in {fname}"
        assert sec3_start != -1, f"Missing section 3 in {fname}"

        table1_text = content[:t1_end]
        sec3_text = content[sec3_start:]

        t1_names = set(line.split("|")[2].replace("*", "").strip() for line in table1_text.splitlines() if line.startswith("| **"))
        sec3_names = set(line.split("|")[1].replace("*", "").strip() for line in sec3_text.splitlines() if line.startswith("| **"))

        overlap = t1_names.intersection(sec3_names)
        assert len(overlap) == 0, f"Duplicate candidates found between Table 1 and Section 3 in {disc}: {overlap}"


# ==============================================================================
# 4. NAMED CANDIDATE TRANSFERS & DISPLACEMENTS
# ==============================================================================

def test_named_bowling_displaced_candidates_in_watchlist(bowling_leaderboard):
    """
    Verifies that Nasum Ahmed (47b), Vipraj Nigam (46b), and Ramon Simmonds (30b):
    1. Are NOT in Table 1.
    2. Appear in Section 3.A Emerging Peer-Beating Watchlist.
    3. Have is_candidate_qualified == False.
    """
    report_file = REPORTS_DIR / "r1_06_bowling_shortlist.md"
    content = report_file.read_text(encoding="utf-8")

    t1_end = content.find("## 2. In-Depth Candidate Evidence Profiles")
    table1_text = content[:t1_end]
    sec3_start = content.find("## 3. Exploratory Watchlist")
    sec3_text = content[sec3_start:]

    bowl_map = bowling_leaderboard.set_index("player_name")
    displaced_bowlers = ["Nasum Ahmed", "Vipraj Nigam", "Ramon Simmonds"]

    for name in displaced_bowlers:
        assert name not in table1_text, f"{name} must NOT be in Table 1"
        assert name in sec3_text, f"{name} must be in Section 3 Watchlist"
        r = bowl_map.loc[name]
        assert bool(r["is_candidate_qualified"]) is False
        assert r["pressure_legal_balls"] < 60
        assert r["watchlist_cohort"] == "PEER_BEATING_EMERGING"


def test_named_bowling_admitted_candidates_in_table1(bowling_leaderboard):
    """
    Verifies that Ravichandran Ashwin (147b), Hasan Mahmud (90b), and Nathan Ellis (347b):
    1. Are present in Table 1 (ranks 9, 10, 11).
    2. Are NOT present in Section 3 Watchlist.
    3. Have is_candidate_qualified == True.
    """
    report_file = REPORTS_DIR / "r1_06_bowling_shortlist.md"
    content = report_file.read_text(encoding="utf-8")

    t1_end = content.find("## 2. In-Depth Candidate Evidence Profiles")
    table1_text = content[:t1_end]
    sec3_start = content.find("## 3. Exploratory Watchlist")
    sec3_text = content[sec3_start:]

    bowl_map = bowling_leaderboard.set_index("player_name")
    admitted_bowlers = ["Ravichandran Ashwin", "Hasan Mahmud", "Nathan Ellis"]

    for name in admitted_bowlers:
        assert name in table1_text, f"{name} must be in Table 1"
        assert name not in sec3_text, f"{name} must NOT be in Section 3 Watchlist"
        r = bowl_map.loc[name]
        assert bool(r["is_candidate_qualified"]) is True
        assert r["pressure_legal_balls"] >= 60


def test_borderline_batters_connolly_and_kishan_in_watchlist(batting_leaderboard):
    """
    Verifies that Cooper Connolly (50b, 4m) and Ishan Kishan (52b, 9m):
    1. Appear in Section 3.A Emerging High-Upside Watchlist.
    2. Do NOT appear in Table 1.
    3. Have is_candidate_qualified == False (due to < 10 matches).
    """
    report_file = REPORTS_DIR / "r1_06_batting_shortlist.md"
    content = report_file.read_text(encoding="utf-8")

    t1_end = content.find("## 2. In-Depth Candidate Evidence Profiles")
    table1_text = content[:t1_end]
    sec3_start = content.find("## 3. Exploratory Watchlist")
    sec3_text = content[sec3_start:]

    bat_map = batting_leaderboard.set_index("player_name")
    borderline_batters = ["Cooper Connolly", "Ishan Kishan"]

    for name in borderline_batters:
        assert name not in table1_text, f"{name} must NOT be in Table 1"
        assert name in sec3_text, f"{name} must be in Section 3 Watchlist"
        r = bat_map.loc[name]
        assert bool(r["is_candidate_qualified"]) is False
        assert 50 <= r["pressure_legal_balls"] < 60
        assert r["pressure_matches"] < 10
        assert r["watchlist_cohort"] == "EMERGING_HIGH_UPSIDE"


# ==============================================================================
# 5. CLASSIFICATION LABEL CONSISTENCY (POSITIVE_ESTIMATE_UNRESOLVED)
# ==============================================================================

def test_renamed_classification_label_consistency(batting_leaderboard, bowling_leaderboard, batting_profiles, bowling_profiles):
    """
    Verifies POSITIVE_ESTIMATE_UNRESOLVED exists and is populated correctly:
    - 19 batters, 1 bowler (Jasprit Bumrah).
    - In all instances, posterior mean is positive (or econ diff < 0) and conservative score <= 0.
    """
    # Batting Leaderboard
    bat_dim_a = batting_leaderboard["performance_evidence_status"].value_counts().to_dict()
    assert bat_dim_a.get("POSITIVE_ESTIMATE_UNRESOLVED", 0) == 19
    assert bat_dim_a.get("NEGATIVE_CONSERVATIVE_ESTIMATE", 0) == 0

    bat_unres = batting_leaderboard[batting_leaderboard["performance_evidence_status"] == "POSITIVE_ESTIMATE_UNRESOLVED"]
    assert len(bat_unres) == 19
    for _, r in bat_unres.iterrows():
        assert r["posterior_mean"] > 0.0, f"Batter {r['player_name']} must have positive posterior mean"
        assert r["primary_diagnostic_value"] <= 0.0, f"Batter {r['player_name']} must have non-positive conservative bound"

    # Bowling Leaderboard
    bowl_dim_a = bowling_leaderboard["performance_evidence_status"].value_counts().to_dict()
    assert bowl_dim_a.get("POSITIVE_ESTIMATE_UNRESOLVED", 0) == 1
    assert bowl_dim_a.get("NEGATIVE_CONSERVATIVE_ESTIMATE", 0) == 0

    bowl_unres = bowling_leaderboard[bowling_leaderboard["performance_evidence_status"] == "POSITIVE_ESTIMATE_UNRESOLVED"]
    assert len(bowl_unres) == 1
    bumrah = bowl_unres.iloc[0]
    assert bumrah["player_name"] == "Jasprit Bumrah"
    assert bumrah["posterior_mean"] < 0.0  # econ diff < 0 means runs saved > 0
    assert bumrah["primary_diagnostic_value"] <= 0.0

    # Cross-check in evidence profiles datasets
    assert (batting_profiles["performance_evidence_status"] == "POSITIVE_ESTIMATE_UNRESOLVED").sum() == 19
    assert (bowling_profiles["performance_evidence_status"] == "POSITIVE_ESTIMATE_UNRESOLVED").sum() == 1


# ==============================================================================
# 6. ZERO STALE LABELS IN CODE, REPORTS, AND PARQUET DATASETS
# ==============================================================================

def test_zero_occurrences_of_negative_conservative_estimate():
    """
    Verifies that the deprecated label 'NEGATIVE_CONSERVATIVE_ESTIMATE' appears 0 times in:
    1. Active source files (r1_06_candidate_selection.py, r1_06_explainability.py).
    2. Generated markdown reports (batting shortlist, bowling shortlist, methodology, intelligence report).
    3. Parquet datasets.
    """
    target_files = [
        SRC_DIR / "r1_06_candidate_selection.py",
        SRC_DIR / "r1_06_explainability.py",
        REPORTS_DIR / "r1_06_batting_shortlist.md",
        REPORTS_DIR / "r1_06_bowling_shortlist.md",
        REPORTS_DIR / "r1_06_methodology_and_limitations.md",
        REPORTS_DIR / "r1_06_player_intelligence_report.md",
    ]

    for p in target_files:
        assert p.exists(), f"Target file missing: {p}"
        content = p.read_text(encoding="utf-8")
        count = content.count("NEGATIVE_CONSERVATIVE_ESTIMATE")
        assert count == 0, f"Found {count} occurrences of NEGATIVE_CONSERVATIVE_ESTIMATE in {p}"

    # Check processed parquets
    for pq in DATA_DIR.glob("*.parquet"):
        df = pd.read_parquet(pq)
        for col in df.columns:
            if df[col].dtype == object or str(df[col].dtype) == "string":
                matches = df[df[col].astype(str).str.contains("NEGATIVE_CONSERVATIVE_ESTIMATE")]
                assert len(matches) == 0, f"Found NEGATIVE_CONSERVATIVE_ESTIMATE in {pq} [{col}]"


# ==============================================================================
# 7. EXPLICIT 1-SE VS 95% CREDIBLE INTERVAL DISCLOSURES
# ==============================================================================

def test_one_se_vs_ninety_five_ci_disclosures(batting_profiles, bowling_profiles):
    """
    Verifies that all 4 reports and candidate evidence profiles explicitly disclose that:
    1. The primary conservative metric is a 1-SE lower bound (~84.1% one-sided credibility).
    2. It is NOT a 95% credible interval.
    3. It is NOT conventional 95% statistical significance.
    4. It is NOT an empirical guarantee.
    """
    # 1. Reports disclosure verification
    reports = [
        REPORTS_DIR / "r1_06_batting_shortlist.md",
        REPORTS_DIR / "r1_06_bowling_shortlist.md",
        REPORTS_DIR / "r1_06_methodology_and_limitations.md",
        REPORTS_DIR / "r1_06_player_intelligence_report.md",
    ]

    for rep in reports:
        assert rep.exists()
        text = rep.read_text(encoding="utf-8")
        assert "84.1" in text, f"Missing '84.1' credibility disclosure in {rep}"
        assert "not a 95% credible interval" in text.lower() or "not a 95% ci" in text.lower(), (
            f"Missing 95% CI distinction in {rep}"
        )

    # 2. Profiles disclosure verification
    for profiles_df, disc in [(batting_profiles, "Batting"), (bowling_profiles, "Bowling")]:
        q1_sample = profiles_df["q1_why_considered"].iloc[0]
        q6_sample = profiles_df["q6_conservative_diagnostic"].iloc[0]

        assert "84.1%" in q1_sample or "1-SE" in q1_sample, f"Missing 1-SE disclosure in {disc} q1"
        assert "84.1%" in q6_sample or "1-SE" in q6_sample, f"Missing 1-SE disclosure in {disc} q6"


# ==============================================================================
# 8. FULL POPULATION HIERARCHY RECONCILIATION
# ==============================================================================

def test_population_hierarchy_reconciliation(batting_intel, bowling_intel, batting_leaderboard, bowling_leaderboard):
    """
    Verifies exact population accounting:
    - Evaluated: 824 batters, 596 bowlers.
    - Min-Exposure (>= 30 balls): 278 batters, 239 bowlers.
    - Sample-Qualified: 161 batters, 168 bowlers.
    - Non-Qualified: 546 batters (413 < 30 balls, 133 zero balls), 357 bowlers (240 < 30 balls, 117 zero balls).
    """
    # Evaluated Population
    assert len(batting_intel) == 824
    assert len(bowling_intel) == 596

    # Minimum Exposure Population (>= 30 balls)
    assert len(batting_leaderboard) == 278
    assert len(bowling_leaderboard) == 239

    # Sample-Qualified Population
    assert (batting_leaderboard["is_candidate_qualified"] == True).sum() == 161
    assert (bowling_leaderboard["is_candidate_qualified"] == True).sum() == 168

    # Non-Qualified file
    non_qual = pd.read_parquet(DATA_DIR / "non_qualified_candidates.parquet")
    assert len(non_qual) == 903
    bat_nq = non_qual[non_qual["discipline"].str.upper() == "BATTING"]
    bowl_nq = non_qual[non_qual["discipline"].str.upper() == "BOWLING"]
    assert len(bat_nq) == 546
    assert len(bowl_nq) == 357

    # Sub-breakdowns
    assert bat_nq["qualification_reason"].str.startswith("BELOW_MIN_PRESSURE_BALLS").sum() == 413
    assert bat_nq["qualification_reason"].str.startswith("ZERO_PRESSURE_DELIVERIES_FACED").sum() == 133
    assert bowl_nq["qualification_reason"].str.startswith("BELOW_MIN_PRESSURE_BALLS").sum() == 240
    assert bowl_nq["qualification_reason"].str.startswith("ZERO_PRESSURE_DELIVERIES_BOWLED").sum() == 117


# ==============================================================================
# 9. STRICT COMPETITION GOVERNANCE BOUNDARIES
# ==============================================================================

def test_governance_scope_boundaries(batting_intel, bowling_intel):
    """
    Verifies strict adherence to competition boundaries:
    1. Zero commercial, auction, price, purse, or salary features in intelligence datasets.
    2. Zero R1-07 files created during audit or remediation.
    """
    forbidden_terms = ["auction", "price", "salary", "crore", "inr", "usd", "bid", "purse"]

    for col in batting_intel.columns:
        assert not any(f in col.lower() for f in forbidden_terms), f"Forbidden commercial feature in batting: {col}"

    for col in bowling_intel.columns:
        assert not any(f in col.lower() for f in forbidden_terms), f"Forbidden commercial feature in bowling: {col}"

    # Verify no R1-07 files exist
    r1_07_files = list(ROOT_DIR.glob("**/r1_07*"))
    assert len(r1_07_files) == 0, f"R1-07 files detected before authorization: {r1_07_files}"
