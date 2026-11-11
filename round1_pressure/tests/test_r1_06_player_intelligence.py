"""
ROYALS INTELLIGENCE — ROUND 1 PLAYER RELIABILITY INTELLIGENCE TEST SUITE
Architecture: ROYALS INTELLIGENCE v4.1
Task: R1-06 Evidence-Backed Player Reliability Intelligence & Ranking Engine

Comprehensive test suite verifying:
1. Artifact existence, non-emptiness, and schema integrity for all 10 Parquet datasets.
2. Markdown report generation and required section completeness across all 4 reports.
3. Primary diagnostic strict ordering (Batting descending on BAT_CONSERVATIVE, Bowling descending on BOWL_CONSERVATIVE).
4. Strict discipline separation (zero cross-discipline metric contamination).
5. Exact population qualification accounting (278+546=824 batters; 239+357=596 bowlers).
6. Evidence classification rule enforcement (12 STRONG_EVIDENCE batters, 11 STRONG_EVIDENCE bowlers).
7. Credible intervals and uncertainty preservation (ci_95_upper - ci_95_lower == 3.92 * posterior_se).
8. Dual-competition threshold compliance (minimum 30 balls in each before claiming dual reliability).
9. Sensitivity and robustness properties (N>=60 overlap, mean vs conservative correlation, TCF sensitivity).
10. Strict scope boundary enforcement (zero auction/pricing/salary/purse columns).
"""

from pathlib import Path
import numpy as np
import pandas as pd
import pytest

PROCESSED_DIR = Path("round1_pressure/data/processed")
REPORTS_DIR = Path("round1_pressure/reports")


# ==============================================================================
# PART 1: ARTIFACT EXISTENCE & SCHEMA INTEGRITY
# ==============================================================================

def test_r1_06_parquet_artifacts_exist():
    """Verifies that all 10 required R1-06 Parquet datasets exist and are non-empty."""
    expected_files = [
        ("batting_intelligence.parquet", 824),
        ("bowling_intelligence.parquet", 596),
        ("qualified_candidates.parquet", 517),
        ("non_qualified_candidates.parquet", 903),
        ("batting_leaderboard.parquet", 278),
        ("bowling_leaderboard.parquet", 239),
        ("batting_evidence_profiles.parquet", 278),
        ("bowling_evidence_profiles.parquet", 239),
        ("shortlist_robustness_comparison.parquet", 12),
        ("competition_candidate_views.parquet", 517),
    ]
    for fname, expected_len in expected_files:
        fpath = PROCESSED_DIR / fname
        assert fpath.exists(), f"Missing required Parquet file: {fname}"
        df = pd.read_parquet(fpath)
        assert len(df) == expected_len, f"File {fname} has length {len(df)}, expected {expected_len}"


def test_r1_06_markdown_reports_exist_and_complete():
    """Verifies that all 4 required Markdown reports exist and contain required sections."""
    reports = {
        "r1_06_player_intelligence_report.md": [
            "Executive Summary & Challenge Answers",
            "Which batters demonstrate the strongest evidence",
            "Which bowlers demonstrate the strongest evidence",
            "How much evidence supports each player",
            "How uncertain is each assessment",
            "Which players are promising but insufficiently established",
            "Why was a particular player included or excluded",
            "How stable is the shortlist under alternative assumptions",
        ],
        "r1_06_batting_shortlist.md": [
            "Executive Shortlist Overview",
            "Nicholas Pooran",
            "Donovan Ferreira",
            "Tim David",
            "Promising Candidates Watchlist",
        ],
        "r1_06_bowling_shortlist.md": [
            "Executive Shortlist Overview",
            "Jasprit Bumrah",
            "Sunil Narine",
            "Maheesh Theekshana",
            "Promising Candidates Watchlist",
        ],
        "r1_06_methodology_and_limitations.md": [
            "Governing Primary Diagnostic Methodology",
            "Conservative Lower Credible Bound",
            "Conservative Runs Saved per Over",
            "Qualification Framework & Non-Qualification Accounting",
            "Robustness & Shortlist Stability Findings",
            "Explicit Unresolved Limitations",
        ],
    }

    for fname, sections in reports.items():
        fpath = REPORTS_DIR / fname
        assert fpath.exists(), f"Missing report: {fname}"
        content = fpath.read_text(encoding="utf-8")
        assert len(content) > 1000, f"Report {fname} is suspiciously short"
        for section in sections:
            assert section.lower() in content.lower(), f"Section '{section}' missing from {fname}"


# ==============================================================================
# PART 2: PRIMARY DIAGNOSTIC ORDERING & METRIC GOVERNANCE
# ==============================================================================

def test_batting_leaderboard_strict_ordering():
    """Verifies Batting Leaderboard is strictly sorted by primary_diagnostic_value descending."""
    df = pd.read_parquet(PROCESSED_DIR / "batting_leaderboard.parquet")
    assert "primary_diagnostic_value" in df.columns
    assert (df["primary_diagnostic_name"] == "BAT_CONSERVATIVE").all()
    # Check strictly monotonic non-increasing
    vals = df["primary_diagnostic_value"].values
    assert np.all(np.diff(vals) <= 1e-6), "Batting leaderboard is not sorted descending"
    # Check official rank matches row order
    assert (df["rank"].values == np.arange(1, len(df) + 1)).all()
    # Check top candidate is Nicholas Pooran
    assert df.iloc[0]["player_name"] == "Nicholas Pooran"
    assert round(df.iloc[0]["primary_diagnostic_value"], 1) == 2.2


def test_bowling_leaderboard_strict_ordering():
    """Verifies Bowling Leaderboard is strictly sorted by primary_diagnostic_value descending."""
    df = pd.read_parquet(PROCESSED_DIR / "bowling_leaderboard.parquet")
    assert "primary_diagnostic_value" in df.columns
    assert (df["primary_diagnostic_name"] == "BOWL_CONSERVATIVE").all()
    # Check strictly monotonic non-increasing
    vals = df["primary_diagnostic_value"].values
    assert np.all(np.diff(vals) <= 1e-6), "Bowling leaderboard is not sorted descending"
    # Check official rank matches row order
    assert (df["rank"].values == np.arange(1, len(df) + 1)).all()
    # Check top candidate is Jasprit Bumrah
    assert df.iloc[0]["player_name"] == "Jasprit Bumrah"
    assert round(df.iloc[0]["primary_diagnostic_value"], 2) == -0.16


# ==============================================================================
# PART 3: DISCIPLINE SEPARATION
# ==============================================================================

def test_strict_discipline_separation():
    """Verifies no cross-discipline metric contamination in intelligence and leaderboards."""
    bat_df = pd.read_parquet(PROCESSED_DIR / "batting_intelligence.parquet")
    bowl_df = pd.read_parquet(PROCESSED_DIR / "bowling_intelligence.parquet")

    # Batting should not have bowling metrics
    bowling_specific_cols = [
        "observed_economy", "expected_economy", "diff_economy",
        "observed_wicket_pct", "diff_wicket_pct"
    ]
    for col in bowling_specific_cols:
        assert col not in bat_df.columns, f"Bowling column {col} contaminated batting intelligence"

    # Bowling should not have batting metrics
    batting_specific_cols = [
        "observed_strike_rate", "expected_strike_rate", "diff_strike_rate",
        "observed_dismissal_pct", "diff_dismissal_pct"
    ]
    for col in batting_specific_cols:
        assert col not in bowl_df.columns, f"Batting column {col} contaminated bowling intelligence"


# ==============================================================================
# PART 4: QUALIFICATION ACCOUNTING
# ==============================================================================

def test_population_qualification_accounting():
    """Verifies exact candidate counts across qualified and non-qualified populations."""
    bat_all = pd.read_parquet(PROCESSED_DIR / "batting_intelligence.parquet")
    bowl_all = pd.read_parquet(PROCESSED_DIR / "bowling_intelligence.parquet")
    qualified = pd.read_parquet(PROCESSED_DIR / "qualified_candidates.parquet")
    non_qualified = pd.read_parquet(PROCESSED_DIR / "non_qualified_candidates.parquet")

    # Batting population counts
    assert len(bat_all) == 824
    assert (bat_all["is_qualified"] == True).sum() == 278
    assert (bat_all["is_qualified"] == False).sum() == 546

    # Bowling population counts
    assert len(bowl_all) == 596
    assert (bowl_all["is_qualified"] == True).sum() == 239
    assert (bowl_all["is_qualified"] == False).sum() == 357

    # Combined tables
    assert len(qualified) == 278 + 239  # 517
    assert len(non_qualified) == 546 + 357  # 903

    # All non-qualified records must have a documented reason
    assert non_qualified["qualification_reason"].isna().sum() == 0
    assert (non_qualified["qualification_reason"].str.len() > 0).all()


# ==============================================================================
# PART 5: EVIDENCE CLASSIFICATION RULES
# ==============================================================================

def test_evidence_classification_rules():
    """Verifies classification counts and eligibility requirements."""
    bat_lead = pd.read_parquet(PROCESSED_DIR / "batting_leaderboard.parquet")
    bowl_lead = pd.read_parquet(PROCESSED_DIR / "bowling_leaderboard.parquet")

    strong_bat = bat_lead[bat_lead["evidence_classification"] == "STRONG_EVIDENCE"]
    assert len(strong_bat) == 12, f"Expected exactly 12 STRONG_EVIDENCE batters, found {len(strong_bat)}"

    # All strong batters must have positive posterior mean and conservative bound >= -10.0
    assert (strong_bat["posterior_mean"] >= 0.0).all()
    assert (strong_bat["primary_diagnostic_value"] >= -10.0).all()
    # All strong batters must meet sample volume criteria
    vol_cond_bat = (strong_bat["pressure_legal_balls"] >= 60) | (
        (strong_bat["pressure_legal_balls"] >= 50) & (strong_bat["pressure_matches"] >= 10)
    )
    assert vol_cond_bat.all()

    strong_bowl = bowl_lead[bowl_lead["evidence_classification"] == "STRONG_EVIDENCE"]
    assert len(strong_bowl) == 11, f"Expected exactly 11 STRONG_EVIDENCE bowlers, found {len(strong_bowl)}"

    # All strong bowlers must have conservative bound >= -1.75
    assert (strong_bowl["primary_diagnostic_value"] >= -1.75).all()
    vol_cond_bowl = (strong_bowl["pressure_legal_balls"] >= 60) | (
        (strong_bowl["pressure_legal_balls"] >= 50) & (strong_bowl["pressure_matches"] >= 10)
    )
    assert vol_cond_bowl.all()


# ==============================================================================
# PART 6: POSTERIOR UNCERTAINTY & CREDIBLE INTERVALS
# ==============================================================================

def test_posterior_uncertainty_and_credible_intervals():
    """Verifies that 95% Credible Intervals equal theta_hat +/- 1.96 * posterior_se."""
    bat_lead = pd.read_parquet(PROCESSED_DIR / "batting_leaderboard.parquet")
    bowl_lead = pd.read_parquet(PROCESSED_DIR / "bowling_leaderboard.parquet")

    # Batting interval check
    for _, row in bat_lead.iterrows():
        expected_lower = row["posterior_mean"] - 1.96 * row["posterior_se"]
        expected_upper = row["posterior_mean"] + 1.96 * row["posterior_se"]
        assert np.isclose(row["ci_95_lower"], expected_lower, atol=0.1)
        assert np.isclose(row["ci_95_upper"], expected_upper, atol=0.1)
        assert np.isclose(row["ci_95_width"], 3.92 * row["posterior_se"], atol=0.2)
        assert 0.0 <= row["prob_exceed_baseline"] <= 1.0
        assert 0.0 <= row["prob_exceed_peers"] <= 1.0

    # Bowling interval check
    for _, row in bowl_lead.iterrows():
        expected_lower = row["posterior_mean"] - 1.96 * row["posterior_se"]
        expected_upper = row["posterior_mean"] + 1.96 * row["posterior_se"]
        assert np.isclose(row["ci_95_lower"], expected_lower, atol=0.1)
        assert np.isclose(row["ci_95_upper"], expected_upper, atol=0.1)
        assert np.isclose(row["ci_95_width"], 3.92 * row["posterior_se"], atol=0.2)
        assert 0.0 <= row["prob_exceed_baseline"] <= 1.0
        assert 0.0 <= row["prob_exceed_peers"] <= 1.0


# ==============================================================================
# PART 7: DUAL-COMPETITION EVIDENCE THRESHOLD
# ==============================================================================

def test_dual_competition_evidence_threshold():
    """Verifies that candidates classified as 'DUAL_COMPETITION_PROVEN' have >= 30 balls in BOTH IPL and T20I."""
    views = pd.read_parquet(PROCESSED_DIR / "competition_candidate_views.parquet")

    both_candidates = views[views["competition_segment"] == "DUAL_COMPETITION_PROVEN"]
    for _, row in both_candidates.iterrows():
        assert row["ipl_pressure_balls"] >= 30, f"{row['player_name']} has {row['ipl_pressure_balls']} IPL balls (<30) but marked DUAL"
        assert row["t20i_pressure_balls"] >= 30, f"{row['player_name']} has {row['t20i_pressure_balls']} T20I balls (<30) but marked DUAL"

    # Verify key expected dual candidates
    both_names = set(both_candidates["player_name"].values)
    assert "Nicholas Pooran" in both_names
    assert "Jasprit Bumrah" in both_names
    assert "Maheesh Theekshana" in both_names
    assert "Matheesha Pathirana" in both_names

    # Donovan Ferreira has 55 IPL balls and 29 T20I balls (<30 in T20I), so must be IPL_PROVEN
    ferreira = views[views["player_name"] == "Donovan Ferreira"].iloc[0]
    assert ferreira["competition_segment"] == "IPL_PROVEN"
    assert ferreira["t20i_pressure_balls"] == 29

    # Sunil Narine must NOT be in DUAL (0 T20I balls)
    narine = views[views["player_name"] == "Sunil Narine"].iloc[0]
    assert narine["competition_segment"] == "IPL_PROVEN"
    assert narine["t20i_pressure_balls"] == 0


# ==============================================================================
# PART 8: SENSITIVITY AND ROBUSTNESS PROPERTIES
# ==============================================================================

def test_shortlist_robustness_properties():
    """Verifies sensitivity metrics from shortlist_robustness_comparison."""
    df = pd.read_parquet(PROCESSED_DIR / "shortlist_robustness_comparison.parquet")
    assert len(df) == 12

    # Check batting N>=60 filter maintains 10/10 overlap
    bat_n60 = df[(df["discipline"] == "BATTING") & (df["configuration_test"] == "SAMPLE_THRESHOLD_GE_60_BALLS")].iloc[0]
    assert bat_n60["top10_membership_overlap"] == "10 / 10"
    assert bat_n60["top10_jaccard_similarity"] == 1.0

    # Check PRI with TCF drops significantly in overlap (confirming experimental status)
    tcf_row = df[(df["discipline"] == "BATTING") & (df["configuration_test"] == "EXPERIMENTAL_PRI_WITH_TCF")].iloc[0]
    assert tcf_row["top10_jaccard_similarity"] <= 0.35


# ==============================================================================
# PART 9: EVIDENCE PROFILES COMPLETENESS
# ==============================================================================

def test_evidence_profiles_completeness():
    """Verifies that all 278 qualified batters and 239 qualified bowlers have complete evidence profiles."""
    bat_prof = pd.read_parquet(PROCESSED_DIR / "batting_evidence_profiles.parquet")
    bowl_prof = pd.read_parquet(PROCESSED_DIR / "bowling_evidence_profiles.parquet")

    assert len(bat_prof) == 278
    assert len(bowl_prof) == 239

    # Check presence of question answers
    q_cols = [
        "q1_why_considered", "q2_pressure_deliveries", "q3_matches_and_seasons",
        "q4_observed_performance", "q5_expected_performance", "q6_conservative_diagnostic",
        "q7_posterior_uncertainty", "q8_credible_interval", "q9_competition_support",
        "q10_major_limitations", "q11_sensitivity_to_assumptions"
    ]
    for col in q_cols:
        assert col in bat_prof.columns, f"Missing {col} in batting profiles"
        assert col in bowl_prof.columns, f"Missing {col} in bowling profiles"
        assert bat_prof[col].isna().sum() == 0, f"NaN values in batting {col}"
        assert bowl_prof[col].isna().sum() == 0, f"NaN values in bowling {col}"
        assert (bat_prof[col].str.len() > 5).all()
        assert (bowl_prof[col].str.len() > 5).all()


# ==============================================================================
# PART 10: STRICT COMPETITION SCOPE BOUNDARY
# ==============================================================================

def test_strict_competition_scope_boundary():
    """Verifies no auction, price, salary, purse, or bid metrics exist in any output."""
    forbidden_terms = ["auction", "price", "salary", "crore", "purse", "bid", "valuation"]

    parquet_files = [
        "batting_intelligence.parquet",
        "bowling_intelligence.parquet",
        "qualified_candidates.parquet",
        "non_qualified_candidates.parquet",
        "batting_leaderboard.parquet",
        "bowling_leaderboard.parquet",
        "batting_evidence_profiles.parquet",
        "bowling_evidence_profiles.parquet",
        "shortlist_robustness_comparison.parquet",
        "competition_candidate_views.parquet",
    ]

    for fname in parquet_files:
        df = pd.read_parquet(PROCESSED_DIR / fname)
        for col in df.columns:
            col_lower = str(col).lower()
            for term in forbidden_terms:
                assert term not in col_lower, f"Forbidden term '{term}' found in column '{col}' of {fname}"
