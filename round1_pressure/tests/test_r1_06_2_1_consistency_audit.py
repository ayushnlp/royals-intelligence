"""
ROYALS INTELLIGENCE — TASK R1-06.2.1 AUDIT TEST SUITE
Test Module: test_r1_06_2_1_consistency_audit.py
Architecture: ROYALS INTELLIGENCE v4.1
Audit Focus: Independent verification of R1-06.2 remediation, candidate qualification,
             two-dimensional classification matrix, population hierarchy, float precision,
             and shortlist report consistency.
"""

from pathlib import Path
import pytest
import numpy as np
import pandas as pd


@pytest.fixture(scope="module")
def project_root() -> Path:
    return Path(__file__).resolve().parent.parent.parent


@pytest.fixture(scope="module")
def data_dir(project_root) -> Path:
    return project_root / "round1_pressure" / "data" / "processed"


@pytest.fixture(scope="module")
def reports_dir(project_root) -> Path:
    return project_root / "round1_pressure" / "reports"


@pytest.fixture(scope="module")
def batting_leaderboard(data_dir) -> pd.DataFrame:
    path = data_dir / "batting_leaderboard.parquet"
    assert path.exists(), f"Batting leaderboard missing at {path}"
    return pd.read_parquet(path)


@pytest.fixture(scope="module")
def bowling_leaderboard(data_dir) -> pd.DataFrame:
    path = data_dir / "bowling_leaderboard.parquet"
    assert path.exists(), f"Bowling leaderboard missing at {path}"
    return pd.read_parquet(path)


@pytest.fixture(scope="module")
def batting_intel(data_dir) -> pd.DataFrame:
    path = data_dir / "batting_intelligence.parquet"
    assert path.exists(), f"Batting intelligence missing at {path}"
    return pd.read_parquet(path)


@pytest.fixture(scope="module")
def bowling_intel(data_dir) -> pd.DataFrame:
    path = data_dir / "bowling_intelligence.parquet"
    assert path.exists(), f"Bowling intelligence missing at {path}"
    return pd.read_parquet(path)


# ==============================================================================
# 1. TWO-DIMENSIONAL CLASSIFICATION SYSTEM TESTS
# ==============================================================================

def test_two_dimensional_classification_batting_distribution(batting_leaderboard):
    """
    Verifies that all 278 qualified batters are partitioned into the 2D matrix
    with exact cell counts and zero unassigned or multi-assigned candidates.
    """
    df = batting_leaderboard
    assert len(df) == 278, f"Expected 278 qualified batters, got {len(df)}"

    ct = pd.crosstab(df["performance_evidence_status"], df["evidence_volume_tier"])

    # Positive conservative evidence (Nicholas Pooran, Donovan Ferreira)
    assert ct.loc["POSITIVE_CONSERVATIVE_EVIDENCE", "HIGH_VOLUME"] == 1
    assert ct.loc["POSITIVE_CONSERVATIVE_EVIDENCE", "MEDIUM_VOLUME"] == 1
    assert "LOW_VOLUME" not in ct.columns or ct.loc["POSITIVE_CONSERVATIVE_EVIDENCE"].get("LOW_VOLUME", 0) == 0
    assert (df["performance_evidence_status"] == "POSITIVE_CONSERVATIVE_EVIDENCE").sum() == 2

    # Negative conservative estimate (positive mean, non-positive lower bound)
    assert ct.loc["NEGATIVE_CONSERVATIVE_ESTIMATE", "HIGH_VOLUME"] == 13
    assert ct.loc["NEGATIVE_CONSERVATIVE_ESTIMATE", "MEDIUM_VOLUME"] == 4
    assert ct.loc["NEGATIVE_CONSERVATIVE_ESTIMATE", "LOW_VOLUME"] == 2
    assert (df["performance_evidence_status"] == "NEGATIVE_CONSERVATIVE_ESTIMATE").sum() == 19

    # Below baseline evidence
    assert ct.loc["BELOW_BASELINE_EVIDENCE", "HIGH_VOLUME"] == 22
    assert ct.loc["BELOW_BASELINE_EVIDENCE", "MEDIUM_VOLUME"] == 75
    assert ct.loc["BELOW_BASELINE_EVIDENCE", "LOW_VOLUME"] == 85
    assert (df["performance_evidence_status"] == "BELOW_BASELINE_EVIDENCE").sum() == 182

    # Inconclusive evidence
    assert ct.loc["INCONCLUSIVE_EVIDENCE", "HIGH_VOLUME"] == 18
    assert ct.loc["INCONCLUSIVE_EVIDENCE", "MEDIUM_VOLUME"] == 18
    assert ct.loc["INCONCLUSIVE_EVIDENCE", "LOW_VOLUME"] == 39
    assert (df["performance_evidence_status"] == "INCONCLUSIVE_EVIDENCE").sum() == 75

    # Total check
    assert ct.values.sum() == 278


def test_two_dimensional_classification_bowling_distribution(bowling_leaderboard):
    """
    Verifies that all 239 qualified bowlers are partitioned into the 2D matrix
    with exact cell counts, confirming Bumrah and Narine outliers.
    """
    df = bowling_leaderboard
    assert len(df) == 239, f"Expected 239 qualified bowlers, got {len(df)}"

    # Zero bowlers achieve positive conservative runs saved
    assert (df["performance_evidence_status"] == "POSITIVE_CONSERVATIVE_EVIDENCE").sum() == 0

    # Exactly 1 bowler achieves negative conservative estimate (Jasprit Bumrah)
    neg_cons = df[df["performance_evidence_status"] == "NEGATIVE_CONSERVATIVE_ESTIMATE"]
    assert len(neg_cons) == 1
    assert neg_cons.iloc[0]["player_name"] == "Jasprit Bumrah"
    assert neg_cons.iloc[0]["evidence_volume_tier"] == "HIGH_VOLUME"

    # Exactly 1 bowler is inconclusive (Sunil Narine)
    inconc = df[df["performance_evidence_status"] == "INCONCLUSIVE_EVIDENCE"]
    assert len(inconc) == 1
    assert inconc.iloc[0]["player_name"] == "Sunil Narine"
    assert inconc.iloc[0]["evidence_volume_tier"] == "HIGH_VOLUME"

    # Exactly 237 bowlers exhibit below-baseline evidence
    below = df[df["performance_evidence_status"] == "BELOW_BASELINE_EVIDENCE"]
    assert len(below) == 237

    ct = pd.crosstab(df["performance_evidence_status"], df["evidence_volume_tier"])
    assert ct.loc["BELOW_BASELINE_EVIDENCE", "HIGH_VOLUME"] == 73
    assert ct.loc["BELOW_BASELINE_EVIDENCE", "MEDIUM_VOLUME"] == 86
    assert ct.loc["BELOW_BASELINE_EVIDENCE", "LOW_VOLUME"] == 78

    assert ct.values.sum() == 239


def test_non_qualified_population_partitioning(batting_intel, bowling_intel):
    """
    Verifies the non-qualified player universe (< 30 balls under pressure).
    Total evaluated: 824 batters and 596 bowlers.
    """
    assert len(batting_intel) == 824
    assert (batting_intel["is_qualified"] == True).sum() == 278
    assert (batting_intel["is_qualified"] == False).sum() == 546

    assert len(bowling_intel) == 596
    assert (bowling_intel["is_qualified"] == True).sum() == 239
    assert (bowling_intel["is_qualified"] == False).sum() == 357


# ==============================================================================
# 2. SAMPLE SIZE & CANDIDATE QUALIFICATION TESTS
# ==============================================================================

def test_candidate_qualification_def04_syntax_fix(batting_leaderboard, bowling_leaderboard):
    """
    Reconciles the DEF-04 syntax bug fix:
    Verifies that 13 batters and 15 bowlers with >=60 balls and <10 matches
    were properly admitted to sample qualification, moving candidate counts from
    148 -> 161 (batting) and 153 -> 168 (bowling).
    """
    bat = batting_leaderboard
    bowl = bowling_leaderboard

    # Old buggy condition: (balls >= 60 or (balls >= 50 and matches >= 10)) and matches >= 10
    old_bat = ((bat["pressure_legal_balls"] >= 60) | ((bat["pressure_legal_balls"] >= 50) & (bat["pressure_matches"] >= 10))) & (bat["pressure_matches"] >= 10)
    new_bat = (bat["pressure_legal_balls"] >= 60) | ((bat["pressure_legal_balls"] >= 50) & (bat["pressure_matches"] >= 10))

    old_bowl = ((bowl["pressure_legal_balls"] >= 60) | ((bowl["pressure_legal_balls"] >= 50) & (bowl["pressure_matches"] >= 10))) & (bowl["pressure_matches"] >= 10)
    new_bowl = (bowl["pressure_legal_balls"] >= 60) | ((bowl["pressure_legal_balls"] >= 50) & (bowl["pressure_matches"] >= 10))

    assert old_bat.sum() == 148
    assert new_bat.sum() == 161
    assert (new_bat.sum() - old_bat.sum()) == 13

    assert old_bowl.sum() == 153
    assert new_bowl.sum() == 168
    assert (new_bowl.sum() - old_bowl.sum()) == 15

    # Check that all newly admitted candidates have >=60 balls and <10 matches
    bat_newly_admitted = bat[~old_bat & new_bat]
    assert len(bat_newly_admitted) == 13
    assert (bat_newly_admitted["pressure_legal_balls"] >= 60).all()
    assert (bat_newly_admitted["pressure_matches"] < 10).all()

    bowl_newly_admitted = bowl[~old_bowl & new_bowl]
    assert len(bowl_newly_admitted) == 15
    assert (bowl_newly_admitted["pressure_legal_balls"] >= 60).all()
    assert (bowl_newly_admitted["pressure_matches"] < 10).all()


def test_borderline_candidates_connolly_and_kishan(batting_leaderboard):
    """
    Verifies that Cooper Connolly (50b, 4m) and Ishan Kishan (52b, 9m):
    1. Are minimum-exposure qualified (is_qualified == True).
    2. Are candidate-disqualified (is_candidate_qualified == False).
    3. Are assigned to EMERGING_HIGH_UPSIDE watchlist.
    4. Do not appear in Table 1 (ranks 13 and 33, Table 1 takes top 12).
    """
    df = batting_leaderboard

    connolly = df[df["player_name"] == "Cooper Connolly"].iloc[0]
    kishan = df[df["player_name"] == "Ishan Kishan"].iloc[0]

    assert connolly["pressure_legal_balls"] == 50
    assert connolly["pressure_matches"] == 4
    assert connolly["is_qualified"] == True
    assert connolly["is_candidate_qualified"] == False
    assert connolly["watchlist_cohort"] == "EMERGING_HIGH_UPSIDE"
    assert connolly["rank"] == 13  # Excluded from Top 12 Table 1

    assert kishan["pressure_legal_balls"] == 52
    assert kishan["pressure_matches"] == 9
    assert kishan["is_qualified"] == True
    assert kishan["is_candidate_qualified"] == False
    assert kishan["watchlist_cohort"] == "EMERGING_HIGH_UPSIDE"
    assert kishan["rank"] == 33  # Excluded from Top 12 Table 1


# ==============================================================================
# 3. STATISTICAL PRECISION & CREDIBILITY INTERVAL TESTS
# ==============================================================================

def test_bowling_prior_mean_reconciliation_exact_floats(bowling_leaderboard):
    """
    Verifies the reconciliation of Sakib Hussain and Riley Meredith against
    the exact prior mean mu = 1.822755960207317 RPO:
    - Sakib Hussain is < 1.82 unrounded (1.8177) and < mu.
    - Riley Meredith is > 1.82 unrounded (1.8217) and < mu.
    - Both round to 1.82 at 2 decimals.
    - Exactly 100 bowlers have posterior_mean < mu.
    """
    df = bowling_leaderboard
    prior_mean = 1.822755960207317

    sakib = df[df["player_name"] == "Sakib Hussain"].iloc[0]
    meredith = df[df["player_name"] == "Riley Meredith"].iloc[0]

    assert sakib["posterior_mean"] < 1.82
    assert sakib["posterior_mean"] < prior_mean
    assert round(sakib["posterior_mean"], 2) == 1.82

    assert meredith["posterior_mean"] > 1.82
    assert meredith["posterior_mean"] < prior_mean
    assert round(meredith["posterior_mean"], 2) == 1.82

    # Verify exact count of bowlers beating league pressure prior mean
    beating_prior = (df["posterior_mean"] < prior_mean).sum()
    assert beating_prior == 100

    # Decomposed: Bumrah (1) + Narine (1) + 98 peer-beaters (68 established + 30 emerging)
    assert (df["watchlist_cohort"] == "PEER_BEATING_ESTABLISHED").sum() == 68
    assert (df["watchlist_cohort"] == "PEER_BEATING_EMERGING").sum() == 30
    assert (df["watchlist_cohort"] == "OUTPERFORMING_BASELINE_ESTIMATE").sum() == 1
    assert (df["watchlist_cohort"] == "INCONCLUSIVE").sum() == 1
    assert (df["watchlist_cohort"] == "BELOW_BASELINE").sum() == 139


def test_1_se_vs_95_ci_empirical_behavior(batting_leaderboard, bowling_leaderboard):
    """
    Empirically verifies the relationship between 1-SE bounds and 95% CIs:
    - Batting: Pooran and Ferreira have 95% CIs that span zero.
    - Batting Below Baseline (182): 115 strictly below 0 under 95% CI; 67 span zero.
    - Bowling: Bumrah and Narine have 95% CIs that span zero.
    - Bowling Below Baseline (237): 226 strictly positive economy inflation under 95% CI; 11 span zero.
    """
    bat = batting_leaderboard
    bowl = bowling_leaderboard

    # Positive conservative batters
    pooran = bat[bat["player_name"] == "Nicholas Pooran"].iloc[0]
    ferreira = bat[bat["player_name"] == "Donovan Ferreira"].iloc[0]

    assert pooran["primary_diagnostic_value"] > 0
    assert pooran["ci_95_lower"] < 0 and pooran["ci_95_upper"] > 0  # Spans zero!

    assert ferreira["primary_diagnostic_value"] > 0
    assert ferreira["ci_95_lower"] < 0 and ferreira["ci_95_upper"] > 0  # Spans zero!

    # Batting Below Baseline
    below_bat = bat[bat["performance_evidence_status"] == "BELOW_BASELINE_EVIDENCE"]
    assert len(below_bat) == 182
    assert (below_bat["ci_95_upper"] < 0).sum() == 115
    assert (below_bat["ci_95_upper"] >= 0).sum() == 67

    # Bowling Outliers
    bumrah = bowl[bowl["player_name"] == "Jasprit Bumrah"].iloc[0]
    narine = bowl[bowl["player_name"] == "Sunil Narine"].iloc[0]

    assert bumrah["ci_95_lower"] < 0 and bumrah["ci_95_upper"] > 0  # Spans zero
    assert narine["ci_95_lower"] < 0 and narine["ci_95_upper"] > 0  # Spans zero

    # Bowling Below Baseline
    below_bowl = bowl[bowl["performance_evidence_status"] == "BELOW_BASELINE_EVIDENCE"]
    assert len(below_bowl) == 237
    assert (below_bowl["ci_95_lower"] > 0).sum() == 226
    assert (below_bowl["ci_95_lower"] <= 0).sum() == 11


# ==============================================================================
# 4. REPORT CONSISTENCY & DEFECT VERIFICATION
# ==============================================================================

def test_bowling_shortlist_table1_defect_verification(reports_dir):
    """
    Audit Defect Verification: DEF-R1-06.2.1-01.
    Verifies that in r1_06_bowling_shortlist.md:
    Table 1 currently contains Nasum Ahmed, Vipraj Nigam, and Ramon Simmonds
    because self.bowl_leaderboard.head(11) was selected without filtering for
    is_candidate_qualified.
    Verifies that all three are duplicated in Section 3 Watchlist.
    """
    report_file = reports_dir / "r1_06_bowling_shortlist.md"
    assert report_file.exists(), f"Bowling shortlist missing at {report_file}"
    content = report_file.read_text(encoding="utf-8")

    # Locate Table 1 and Section 3
    assert "### Bowling Leaderboard (Top 11 Candidates):" in content
    assert "## 3. Promising Candidates Watchlist" in content

    t1_end = content.find("## 2. In-Depth Candidate Evidence Profiles")
    table1_text = content[:t1_end]
    watchlist_text = content[t1_end:]

    # Confirm that Nasum Ahmed, Vipraj Nigam, and Ramon Simmonds are present in Table 1
    assert "Nasum Ahmed" in table1_text, "Nasum Ahmed expected in Table 1 under DEF-R1-06.2.1-01"
    assert "Vipraj Nigam" in table1_text, "Vipraj Nigam expected in Table 1 under DEF-R1-06.2.1-01"
    assert "Ramon Simmonds" in table1_text, "Ramon Simmonds expected in Table 1 under DEF-R1-06.2.1-01"

    # Confirm that all 3 also appear in the Watchlist (duplication defect)
    assert "Nasum Ahmed" in watchlist_text, "Nasum Ahmed duplicated in Watchlist"
    assert "Vipraj Nigam" in watchlist_text, "Vipraj Nigam duplicated in Watchlist"
    assert "Ramon Simmonds" in watchlist_text, "Ramon Simmonds duplicated in Watchlist"


def test_batting_shortlist_table1_clean_qualification(reports_dir, batting_leaderboard):
    """
    Verifies that in r1_06_batting_shortlist.md:
    All 12 batters in Table 1 have is_candidate_qualified == True,
    and none are duplicated in Section 3 Watchlist.
    """
    report_file = reports_dir / "r1_06_batting_shortlist.md"
    assert report_file.exists(), f"Batting shortlist missing at {report_file}"
    content = report_file.read_text(encoding="utf-8")

    t1_end = content.find("## 2. In-Depth Candidate Evidence Profiles")
    table1_text = content[:t1_end]
    watchlist_text = content[t1_end:]

    top_12 = batting_leaderboard.head(12)
    assert (top_12["is_candidate_qualified"] == True).all()

    # Verify no Top 12 batter appears in Section 3 Watchlist
    for name in top_12["player_name"]:
        assert name in table1_text
        assert f"| {name} |" not in watchlist_text


# ==============================================================================
# 5. GOVERNANCE & INTEGRITY CONSTRAINTS
# ==============================================================================

def test_governance_scope_boundaries(batting_intel, bowling_intel, project_root):
    """
    Verifies strict adherence to competition boundaries:
    1. Zero commercial, auction, price, or salary features in intelligence datasets.
    2. Zero R1-07 files created during audit.
    """
    forbidden_terms = ["auction", "price", "salary", "crore", "inr", "usd", "bid"]

    for col in batting_intel.columns:
        assert not any(f in col.lower() for f in forbidden_terms), f"Forbidden commercial feature in batting: {col}"

    for col in bowling_intel.columns:
        assert not any(f in col.lower() for f in forbidden_terms), f"Forbidden commercial feature in bowling: {col}"

    # Verify no R1-07 files exist
    r1_07_files = list(project_root.glob("**/r1_07*"))
    assert len(r1_07_files) == 0, f"R1-07 files detected before completion: {r1_07_files}"
