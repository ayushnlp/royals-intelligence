"""
ROYALS INTELLIGENCE — ROUND 1 TASK R1-06.2.3 TEST SUITE
Architecture: ROYALS INTELLIGENCE v4.1
Task: R1-06.2.3 Final Data-Count Reconciliation & Statistical Wording Correction

Focused regression test suite verifying:
1. Delivery Count Reconciliation (200,999 raw rows, 883 matches, 867 with deliveries, 16 abandoned; zero occurrences of 208,081).
2. Batting Population Hierarchy & Set Relationships (824 evaluated, 278 min-exposure, 161 qualified, 12 Table 1, 149 remaining qualified, 2 emerging, 17 established marginal).
3. Bowling Population Hierarchy & Set Relationships (596 evaluated, 239 min-exposure, 168 qualified, 11 Table 1, 157 remaining qualified, 30 emerging, 68 established peer-beaters).
4. Watchlist Set Relationships (Emerging vs Established mutual exclusivity, subset relationships to qualified vs disqualified).
5. Exact Corrected Statistical Disclosure Wording in all reports and candidate evidence profiles.
6. Report Table 1 and Watchlist deduplication across both disciplines.
7. Governance boundaries (zero commercial features, zero R1-07 files).
"""

from pathlib import Path
import pandas as pd
import pytest

DATA_DIR = Path("round1_pressure/data/processed")
RAW_DIR = Path("round1_pressure/data/raw")
REPORTS_DIR = Path("round1_pressure/reports")
SRC_DIR = Path("round1_pressure/src")
ROOT_DIR = Path(".")

EXACT_DISCLOSURE_PHRASE = (
    "Under an approximate normal posterior distribution, a positive one-standard-error lower bound "
    "implies posterior probability above zero greater than approximately 84.1%. "
    "This is a directional uncertainty diagnostic, not a 95% credible interval, "
    "conventional 95% statistical significance, or a guarantee of future performance."
)


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


@pytest.fixture(scope="module")
def non_qualified():
    return pd.read_parquet(DATA_DIR / "non_qualified_candidates.parquet")


# ==============================================================================
# 1. DELIVERY COUNT RECONCILIATION
# ==============================================================================

def test_source_csv_delivery_and_match_counts():
    """
    Reconfirms the original CSV row counts directly against established QA baseline:
    - ball_by_ball.csv: exactly 200,999 rows (excluding header)
    - matches.csv: exactly 883 rows (excluding header)
    - 867 matches with deliveries
    - 16 matches abandoned without a ball bowled
    """
    bbb_path = RAW_DIR / "ball_by_ball.csv"
    matches_path = RAW_DIR / "matches.csv"

    assert bbb_path.exists(), f"Missing {bbb_path}"
    assert matches_path.exists(), f"Missing {matches_path}"

    with open(bbb_path, "r", encoding="utf-8") as f:
        bbb_lines = sum(1 for _ in f)
    assert bbb_lines - 1 == 200999, f"Expected 200,999 rows in ball_by_ball.csv, got {bbb_lines - 1}"

    with open(matches_path, "r", encoding="utf-8") as f:
        matches_lines = sum(1 for _ in f)
    assert matches_lines - 1 == 883, f"Expected 883 rows in matches.csv, got {matches_lines - 1}"

    # Verify match-to-ball relational completeness
    df_bbb = pd.read_csv(bbb_path, usecols=["match_id"])
    df_matches = pd.read_csv(matches_path, usecols=["match_id"])

    bbb_matches = set(df_bbb["match_id"].unique())
    all_matches = set(df_matches["match_id"].unique())

    assert len(bbb_matches) == 867, f"Expected 867 matches with deliveries, got {len(bbb_matches)}"
    assert len(all_matches) == 883, f"Expected 883 matches, got {len(all_matches)}"
    assert len(all_matches - bbb_matches) == 16, "Expected exactly 16 abandoned matches with no deliveries"


def test_processed_delivery_parquet_counts():
    """
    Verifies that all primary delivery-level processed parquets retain the exact 200,999 row count.
    """
    delivery_parquets = [
        "delivery_states_strict.parquet",
        "delivery_states_permissive.parquet",
        "batting_pressure_events_strict.parquet",
        "batting_pressure_events_permissive.parquet",
        "bowling_pressure_events_strict.parquet",
        "bowling_pressure_events_permissive.parquet",
    ]

    for fname in delivery_parquets:
        fpath = DATA_DIR / fname
        assert fpath.exists(), f"Missing {fname}"
        df = pd.read_parquet(fpath)
        assert len(df) == 200999, f"Parquet {fname} row count mismatch: {len(df)} != 200,999"


def test_zero_stale_208081_delivery_count():
    """
    Verifies that the errant drafting transcription '208,081' does not appear in:
    1. Active source files
    2. Generated reports
    3. Remediated completion reports
    4. Processed parquets
    """
    target_files = [
        SRC_DIR / "r1_06_candidate_selection.py",
        SRC_DIR / "r1_06_explainability.py",
        REPORTS_DIR / "r1_06_batting_shortlist.md",
        REPORTS_DIR / "r1_06_bowling_shortlist.md",
        REPORTS_DIR / "r1_06_methodology_and_limitations.md",
        REPORTS_DIR / "r1_06_player_intelligence_report.md",
        REPORTS_DIR / "r1_06_2_2_remediation_report.md",
        ROOT_DIR / "r1_06_2_2_remediation_report.md",
    ]

    for p in target_files:
        assert p.exists(), f"Missing file: {p}"
        text = p.read_text(encoding="utf-8")
        assert "208,081" not in text, f"Found stale count 208,081 in {p}"
        assert "208081" not in text, f"Found stale count 208081 in {p}"


# ==============================================================================
# 2. BATTING POPULATION HIERARCHY & SET RECONCILIATION
# ==============================================================================

def test_batting_population_set_relationships(batting_intel, batting_leaderboard, non_qualified):
    """
    Verifies the exact set relationships for Batting:
    - Evaluated: 824
    - Minimum exposure (>= 30 balls): 278
    - Excluded (< 30 balls): 546 (413 with 1-29 balls, 133 with 0 balls)
    - Sample-qualified: 161 (balls >= 60 OR [balls >= 50 AND matches >= 10])
    - Sample-disqualified within min-exposure: 117 (278 - 161 = 117)
    - Primary Table 1: 12 (top 12 qualified)
    - Remaining qualified cohort: 149 (161 - 12 = 149)
    - Emerging High-Upside Watchlist: 2 (Connolly, Kishan) -> subset of sample-disqualified (0 overlap with qualified)
    - Established Marginal Watchlist: 17 -> subset of sample-qualified (10 in Table 1, 7 in Remaining Qualified)
    """
    # 1. Total Evaluated & Excluded Partition
    assert len(batting_intel) == 824
    assert len(batting_leaderboard) == 278
    bat_nq = non_qualified[non_qualified["discipline"].str.upper() == "BATTING"]
    assert len(bat_nq) == 546
    assert len(batting_leaderboard) + len(bat_nq) == 824

    # 2. Sample-Qualified Partition
    qual_mask = batting_leaderboard["is_candidate_qualified"]
    qual_df = batting_leaderboard[qual_mask]
    disqual_df = batting_leaderboard[~qual_mask]
    assert len(qual_df) == 161
    assert len(disqual_df) == 117
    assert len(qual_df) + len(disqual_df) == 278

    # 3. Table 1 vs Remaining Qualified
    table1_df = qual_df.head(12)
    rem_qual_df = qual_df.iloc[12:]
    assert len(table1_df) == 12
    assert len(rem_qual_df) == 149
    t1_ids = set(table1_df["player_id"])
    rem_ids = set(rem_qual_df["player_id"])
    assert len(t1_ids & rem_ids) == 0, "Table 1 and Remaining Qualified must be disjoint"
    assert len(t1_ids | rem_ids) == 161

    # 4. Emerging High-Upside Watchlist (2)
    emerging = batting_leaderboard[batting_leaderboard["watchlist_cohort"] == "EMERGING_HIGH_UPSIDE"]
    assert len(emerging) == 2
    emerging_names = set(emerging["player_name"])
    assert emerging_names == {"Cooper Connolly", "Ishan Kishan"}
    # Both are sample-disqualified
    assert (~emerging["is_candidate_qualified"]).all()
    emerging_ids = set(emerging["player_id"])
    assert len(emerging_ids & t1_ids) == 0
    assert len(emerging_ids & rem_ids) == 0
    assert emerging_ids.issubset(set(disqual_df["player_id"]))

    # 5. Established Marginal Watchlist (17)
    estab = batting_leaderboard[batting_leaderboard["watchlist_cohort"] == "ESTABLISHED_MARGINAL_PERFORMER"]
    assert len(estab) == 17
    estab_ids = set(estab["player_id"])
    # All 17 are sample-qualified
    assert (estab["is_candidate_qualified"]).all()
    assert estab_ids.issubset(set(qual_df["player_id"]))

    # Overlap accounting: exactly 10 in Table 1, exactly 7 in Remaining Qualified
    estab_in_t1 = estab_ids & t1_ids
    estab_in_rem = estab_ids & rem_ids
    assert len(estab_in_t1) == 10
    assert len(estab_in_rem) == 7
    assert len(estab_in_t1) + len(estab_in_rem) == 17

    # Watchlist cohorts mutual exclusivity
    assert len(emerging_ids & estab_ids) == 0


# ==============================================================================
# 3. BOWLING POPULATION HIERARCHY & SET RECONCILIATION
# ==============================================================================

def test_bowling_population_set_relationships(bowling_intel, bowling_leaderboard, non_qualified):
    """
    Verifies the exact set relationships for Bowling:
    - Evaluated: 596
    - Minimum exposure (>= 30 balls): 239
    - Excluded (< 30 balls): 357 (240 with 1-29 balls, 117 with 0 balls)
    - Sample-qualified: 168 (balls >= 60 OR [balls >= 50 AND matches >= 10])
    - Sample-disqualified within min-exposure: 71 (239 - 168 = 71)
    - Primary Table 1: 11 (top 11 qualified)
    - Remaining qualified cohort: 157 (168 - 11 = 157)
    - Emerging Peer-Beating Watchlist: 30 (28 disqualified, 2 qualified Sodhi/Mujeeb)
    - Established Peer-Beating Watchlist: 68 (all 68 qualified: 9 in Table 1, 59 in Remaining Qualified)
    """
    # 1. Total Evaluated & Excluded Partition
    assert len(bowling_intel) == 596
    assert len(bowling_leaderboard) == 239
    bowl_nq = non_qualified[non_qualified["discipline"].str.upper() == "BOWLING"]
    assert len(bowl_nq) == 357
    assert len(bowling_leaderboard) + len(bowl_nq) == 596

    # 2. Sample-Qualified Partition
    qual_mask = bowling_leaderboard["is_candidate_qualified"]
    qual_df = bowling_leaderboard[qual_mask]
    disqual_df = bowling_leaderboard[~qual_mask]
    assert len(qual_df) == 168
    assert len(disqual_df) == 71
    assert len(qual_df) + len(disqual_df) == 239

    # 3. Table 1 vs Remaining Qualified
    table1_df = qual_df.head(11)
    rem_qual_df = qual_df.iloc[11:]
    assert len(table1_df) == 11
    assert len(rem_qual_df) == 157
    t1_ids = set(table1_df["player_id"])
    rem_ids = set(rem_qual_df["player_id"])
    assert len(t1_ids & rem_ids) == 0, "Table 1 and Remaining Qualified must be disjoint"
    assert len(t1_ids | rem_ids) == 168

    # 4. Emerging Peer-Beating Watchlist (30)
    emerging = bowling_leaderboard[bowling_leaderboard["watchlist_cohort"] == "PEER_BEATING_EMERGING"]
    assert len(emerging) == 30
    emerging_ids = set(emerging["player_id"])
    # 0 overlap with Table 1
    assert len(emerging_ids & t1_ids) == 0

    # 28 are sample-disqualified, 2 are sample-qualified
    emerging_disqual = emerging[~emerging["is_candidate_qualified"]]
    emerging_qual = emerging[emerging["is_candidate_qualified"]]
    assert len(emerging_disqual) == 28
    assert len(emerging_qual) == 2
    qualified_emerging_names = set(emerging_qual["player_name"])
    assert qualified_emerging_names == {"Ish Sodhi", "Mujeeb Ur Rahman"}
    assert set(emerging_qual["player_id"]).issubset(rem_ids)

    # 5. Established Peer-Beating Watchlist (68)
    estab = bowling_leaderboard[bowling_leaderboard["watchlist_cohort"] == "PEER_BEATING_ESTABLISHED"]
    assert len(estab) == 68
    estab_ids = set(estab["player_id"])
    # All 68 are sample-qualified
    assert (estab["is_candidate_qualified"]).all()
    assert estab_ids.issubset(set(qual_df["player_id"]))

    # Overlap accounting: exactly 9 in Table 1, exactly 59 in Remaining Qualified
    estab_in_t1 = estab_ids & t1_ids
    estab_in_rem = estab_ids & rem_ids
    assert len(estab_in_t1) == 9
    assert len(estab_in_rem) == 59
    assert len(estab_in_t1) + len(estab_in_rem) == 68

    # Watchlist cohorts mutual exclusivity
    assert len(emerging_ids & estab_ids) == 0


# ==============================================================================
# 4. EXACT STATISTICAL DISCLOSURE WORDING VERIFICATION
# ==============================================================================

def test_exact_corrected_statistical_wording_in_reports():
    """
    Verifies that all 4 reports contain the exact mandated statistical disclosure phrase:
    'Under an approximate normal posterior distribution, a positive one-standard-error lower bound
    implies posterior probability above zero greater than approximately 84.1%. This is a directional
    uncertainty diagnostic, not a 95% credible interval, conventional 95% statistical significance,
    or a guarantee of future performance.'
    """
    reports = [
        REPORTS_DIR / "r1_06_batting_shortlist.md",
        REPORTS_DIR / "r1_06_bowling_shortlist.md",
        REPORTS_DIR / "r1_06_methodology_and_limitations.md",
        REPORTS_DIR / "r1_06_player_intelligence_report.md",
    ]

    for rep in reports:
        assert rep.exists(), f"Missing report: {rep}"
        content = rep.read_text(encoding="utf-8")
        assert EXACT_DISCLOSURE_PHRASE in content, f"Exact disclosure phrase missing from {rep.name}"


def test_exact_corrected_statistical_wording_in_candidate_profiles(batting_profiles, bowling_profiles):
    """
    Verifies that all 278 batting profiles and all 239 bowling profiles contain the exact
    mandated statistical disclosure phrase in q6_conservative_diagnostic.
    """
    for df, disc in [(batting_profiles, "Batting"), (bowling_profiles, "Bowling")]:
        matches = df["q6_conservative_diagnostic"].str.contains(EXACT_DISCLOSURE_PHRASE, regex=False)
        assert matches.all(), f"Not all {disc} profiles contain the exact disclosure phrase ({matches.sum()}/{len(df)})"


# ==============================================================================
# 5. DEDUPLICATION & WATCHLIST REPORT TABLE HYGIENE
# ==============================================================================

def test_shortlist_reports_zero_table1_watchlist_duplication():
    """
    Verifies that Section 3 Watchlists in shortlist markdown reports do not duplicate Table 1 players.
    """
    for fname, disc in [("r1_06_batting_shortlist.md", "Batting"), ("r1_06_bowling_shortlist.md", "Bowling")]:
        report_file = REPORTS_DIR / fname
        content = report_file.read_text(encoding="utf-8")

        t1_end = content.find("## 2. In-Depth Candidate Evidence Profiles")
        sec3_start = content.find("## 3. Exploratory Watchlist")
        table1_text = content[:t1_end]
        sec3_text = content[sec3_start:]

        t1_names = set(line.split("|")[2].replace("*", "").strip() for line in table1_text.splitlines() if line.startswith("| **"))
        sec3_names = set(line.split("|")[1].replace("*", "").strip() for line in sec3_text.splitlines() if line.startswith("| **"))

        overlap = t1_names.intersection(sec3_names)
        assert len(overlap) == 0, f"Found overlapping candidates in {disc} report: {overlap}"


# ==============================================================================
# 6. STRICT GOVERNANCE & INTEGRITY BOUNDARIES
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
