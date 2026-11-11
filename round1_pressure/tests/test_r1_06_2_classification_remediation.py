"""
ROYALS INTELLIGENCE — ROUND 1 TASK R1-06.2 REMEDIATION TEST SUITE
Architecture: ROYALS INTELLIGENCE v4.1
Task: R1-06.2 Candidate Classification & Evidence Governance Remediation

Comprehensive test suite verifying all 16 remediation requirements:
1. Two-dimensional classification schema existence and completeness across Parquet datasets.
2. Dimension A mutual exclusivity and exhaustiveness (exact sums: 2+19+182+75=278 batters; 0+1+237+1=239 bowlers).
3. Dimension B mutual exclusivity and exhaustiveness across all qualified candidates.
4. Correct candidate qualification syntax logic (DEF-04 fix: >=60 balls OR (>=50 balls and >=10 matches)).
5. Positive conservative bound verification (Pooran & Ferreira only; 0 bowlers).
6. Candidates 3-12 classified as NEGATIVE_CONSERVATIVE_ESTIMATE (positive mean, conservative bound <= 0).
7. Separation of promising watchlist into EMERGING_HIGH_UPSIDE and ESTABLISHED_MARGINAL_PERFORMER (DEF-03 fix).
8. Bowling Bumrah benchmark (sole bowler with positive runs saved point estimate) and Narine inconclusive evidence.
9. Resolution of the 87 vs 88 bowling promising count discrepancy using full-precision unrounded floats.
10. Probability statement column and reference mean disclosures (prob_exceed_league_mean against mu).
11. Competition qualification exposure standard (DUAL_TOURNAMENT_QUALIFIED requiring >=30 in both).
12. Remediation report existence and completeness in reports dir and root dir.
13. Shortlist markdown reports updated with Two-Dimensional terminology.
14. Methodology markdown report completeness with Section 1.3 and reference disclosures.
15. Backward compatibility preservation (legacy_evidence_classification and evidence_classification columns).
16. Strict competition scope boundary (zero commercial/auction/purse/salary metrics).
"""

from pathlib import Path
import numpy as np
import pandas as pd
import pytest

PROCESSED_DIR = Path("round1_pressure/data/processed")
REPORTS_DIR = Path("round1_pressure/reports")
ROOT_DIR = Path(".")


# ==============================================================================
# PART 1: TWO-DIMENSIONAL CLASSIFICATION SCHEMA INTEGRITY
# ==============================================================================

def test_remediated_schema_integrity():
    """Verifies all remediated columns exist in intelligence and leaderboard datasets."""
    required_cols = [
        "performance_evidence_status",
        "evidence_volume_tier",
        "two_dimensional_classification",
        "watchlist_cohort",
        "is_candidate_qualified",
        "prob_exceed_league_mean",
        "competition_qualification",
    ]

    for fname in ["batting_leaderboard.parquet", "bowling_leaderboard.parquet"]:
        fpath = PROCESSED_DIR / fname
        assert fpath.exists(), f"Missing {fname}"
        df = pd.read_parquet(fpath)
        for col in required_cols:
            assert col in df.columns, f"Column '{col}' missing from {fname}"
            assert df[col].isna().sum() == 0, f"Column '{col}' has null values in {fname}"


# ==============================================================================
# PART 2: DIMENSION A MUTUAL EXCLUSIVITY & POPULATION COUNTS
# ==============================================================================

def test_batting_dimension_a_counts():
    """Verifies Batting Dimension A mutually exclusive and exhaustive counts."""
    df = pd.read_parquet(PROCESSED_DIR / "batting_leaderboard.parquet")
    assert len(df) == 278

    dim_a_counts = df["performance_evidence_status"].value_counts().to_dict()
    assert dim_a_counts.get("POSITIVE_CONSERVATIVE_EVIDENCE", 0) == 2
    assert dim_a_counts.get("NEGATIVE_CONSERVATIVE_ESTIMATE", 0) == 19
    assert dim_a_counts.get("BELOW_BASELINE_EVIDENCE", 0) == 182
    assert dim_a_counts.get("INCONCLUSIVE_EVIDENCE", 0) == 75
    assert sum(dim_a_counts.values()) == 278


def test_bowling_dimension_a_counts():
    """Verifies Bowling Dimension A mutually exclusive and exhaustive counts."""
    df = pd.read_parquet(PROCESSED_DIR / "bowling_leaderboard.parquet")
    assert len(df) == 239

    dim_a_counts = df["performance_evidence_status"].value_counts().to_dict()
    assert dim_a_counts.get("POSITIVE_CONSERVATIVE_EVIDENCE", 0) == 0
    assert dim_a_counts.get("NEGATIVE_CONSERVATIVE_ESTIMATE", 0) == 1
    assert dim_a_counts.get("INCONCLUSIVE_EVIDENCE", 0) == 1
    assert dim_a_counts.get("BELOW_BASELINE_EVIDENCE", 0) == 237
    assert sum(dim_a_counts.values()) == 239


# ==============================================================================
# PART 3: DIMENSION B EVIDENCE VOLUME TIERS
# ==============================================================================

def test_dimension_b_volume_tiers():
    """Verifies Dimension B volume tier thresholds across both disciplines."""
    for fname in ["batting_leaderboard.parquet", "bowling_leaderboard.parquet"]:
        df = pd.read_parquet(PROCESSED_DIR / fname)
        for _, r in df.iterrows():
            balls = r["pressure_legal_balls"]
            tier = r["evidence_volume_tier"]
            if balls >= 150:
                assert tier == "HIGH_VOLUME", f"Player {r['player_name']} has {balls} balls but tier is {tier}"
            elif balls >= 60:
                assert tier == "MEDIUM_VOLUME", f"Player {r['player_name']} has {balls} balls but tier is {tier}"
            elif balls >= 30:
                assert tier == "LOW_VOLUME", f"Player {r['player_name']} has {balls} balls but tier is {tier}"
            else:
                assert tier == "NO_QUALIFYING_EXPOSURE", f"Player {r['player_name']} has {balls} balls but tier is {tier}"


# ==============================================================================
# PART 4: DEF-04 CANDIDATE QUALIFICATION SYNTAX FIX
# ==============================================================================

def test_def_04_qualification_syntax_fix():
    """Verifies that candidates with >= 60 balls are qualified regardless of match count."""
    bat_df = pd.read_parquet(PROCESSED_DIR / "batting_leaderboard.parquet")
    bowl_df = pd.read_parquet(PROCESSED_DIR / "bowling_leaderboard.parquet")

    # Batters with >= 60 balls and < 10 matches must be is_candidate_qualified == True
    bat_sub = bat_df[(bat_df["pressure_legal_balls"] >= 60) & (bat_df["pressure_matches"] < 10)]
    assert len(bat_sub) == 13
    assert bat_sub["is_candidate_qualified"].all(), "Some batters with >=60 balls were not qualified"

    # Specific known batters
    porell = bat_df[bat_df["player_name"] == "Abishek Porel"].iloc[0]
    assert porell["pressure_legal_balls"] == 88
    assert porell["pressure_matches"] == 8
    assert porell["is_candidate_qualified"] == True

    zadran = bat_df[bat_df["player_name"] == "Ibrahim Zadran"].iloc[0]
    assert zadran["pressure_legal_balls"] == 112
    assert zadran["pressure_matches"] == 8
    assert zadran["is_candidate_qualified"] == True

    # Bowlers with >= 60 balls and < 10 matches must be is_candidate_qualified == True
    bowl_sub = bowl_df[(bowl_df["pressure_legal_balls"] >= 60) & (bowl_df["pressure_matches"] < 10)]
    assert len(bowl_sub) == 15
    assert bowl_sub["is_candidate_qualified"].all(), "Some bowlers with >=60 balls were not qualified"

    bravo = bowl_df[bowl_df["player_name"] == "Dwayne Bravo"].iloc[0]
    assert bravo["pressure_legal_balls"] == 92
    assert bravo["pressure_matches"] == 9
    assert bravo["is_candidate_qualified"] == True


# ==============================================================================
# PART 5: POSITIVE CONSERVATIVE BOUND VERIFICATION
# ==============================================================================

def test_positive_conservative_bound_verification():
    """Verifies that Nicholas Pooran and Donovan Ferreira are the ONLY positive conservative bound batters."""
    df = pd.read_parquet(PROCESSED_DIR / "batting_leaderboard.parquet")
    pos_cand = df[df["performance_evidence_status"] == "POSITIVE_CONSERVATIVE_EVIDENCE"]
    assert len(pos_cand) == 2
    pos_names = set(pos_cand["player_name"])
    assert pos_names == {"Nicholas Pooran", "Donovan Ferreira"}

    for _, r in pos_cand.iterrows():
        assert r["primary_diagnostic_value"] > 0.0
        assert r["posterior_mean"] > 0.0
        assert r["watchlist_cohort"] == "CONFIRMED_POSITIVE_RELIABILITY"


# ==============================================================================
# PART 6: CANDIDATES 3-12 CLASSIFICATION REMEDIATION
# ==============================================================================

def test_candidates_3_through_12_remediation():
    """Verifies that batters #3 through #12 have NEGATIVE_CONSERVATIVE_ESTIMATE."""
    df = pd.read_parquet(PROCESSED_DIR / "batting_leaderboard.parquet")
    sub_10 = df.iloc[2:12]  # Ranks 3 through 12
    for _, r in sub_10.iterrows():
        assert r["performance_evidence_status"] == "NEGATIVE_CONSERVATIVE_ESTIMATE"
        assert r["primary_diagnostic_value"] <= 0.0
        assert r["posterior_mean"] > 0.0

    # Check key candidate names
    names = set(sub_10["player_name"])
    assert "Tim David" in names
    assert "Dinesh Karthik" in names
    assert "Ashutosh Sharma" in names
    assert "Marcus Stoinis" in names


# ==============================================================================
# PART 7: PROMISING WATCHLIST COHORT SEPARATION (DEF-03)
# ==============================================================================

def test_watchlist_cohort_separation():
    """Verifies separation into EMERGING_HIGH_UPSIDE and ESTABLISHED_MARGINAL_PERFORMER."""
    df = pd.read_parquet(PROCESSED_DIR / "batting_leaderboard.parquet")

    emerging = df[df["watchlist_cohort"] == "EMERGING_HIGH_UPSIDE"]
    assert len(emerging) == 2
    emerging_names = set(emerging["player_name"])
    assert emerging_names == {"Cooper Connolly", "Ishan Kishan"}
    for _, r in emerging.iterrows():
        assert 30 <= r["pressure_legal_balls"] < 60
        assert r["posterior_mean"] > 0.0

    established = df[df["watchlist_cohort"] == "ESTABLISHED_MARGINAL_PERFORMER"]
    assert len(established) == 17
    estab_names = set(established["player_name"])
    assert "Andre Russell" in estab_names
    assert "Suryakumar Yadav" in estab_names
    assert "Rahul Tewatia" in estab_names
    assert "Shashank Singh" in estab_names
    for _, r in established.iterrows():
        assert r["pressure_legal_balls"] >= 60
        assert r["posterior_mean"] > 0.0
        assert r["primary_diagnostic_value"] <= 0.0


# ==============================================================================
# PART 8: BOWLING BENCHMARKS (BUMRAH & NARINE)
# ==============================================================================

def test_bowling_benchmarks():
    """Verifies Jasprit Bumrah and Sunil Narine exact remediated classifications."""
    df = pd.read_parquet(PROCESSED_DIR / "bowling_leaderboard.parquet")

    # Bumrah
    bumrah = df[df["player_name"] == "Jasprit Bumrah"].iloc[0]
    assert bumrah["rank"] == 1
    assert bumrah["performance_evidence_status"] == "NEGATIVE_CONSERVATIVE_ESTIMATE"
    assert bumrah["evidence_volume_tier"] == "HIGH_VOLUME"
    assert bumrah["watchlist_cohort"] == "OUTPERFORMING_BASELINE_ESTIMATE"
    assert bumrah["posterior_mean"] < 0.0  # Concedes fewer runs under pressure than ordinary baseline
    assert bumrah["primary_diagnostic_value"] <= 0.0  # Conservative lower bound <= 0

    # Narine
    narine = df[df["player_name"] == "Sunil Narine"].iloc[0]
    assert narine["rank"] == 2
    assert narine["performance_evidence_status"] == "INCONCLUSIVE_EVIDENCE"
    assert narine["evidence_volume_tier"] == "HIGH_VOLUME"
    assert narine["posterior_mean"] > 0.0
    runs_saved_upper = -narine["posterior_mean"] + narine["posterior_se"]
    assert runs_saved_upper >= 0.0  # 1-sigma interval spans across zero


# ==============================================================================
# PART 9: RESOLUTION OF 87 VS 88 BOWLING PROMISINGS (UNROUNDED FLOATS)
# ==============================================================================

def test_resolution_of_87_vs_88_bowling_discrepancy():
    """Verifies unrounded float analysis for Sakib Hussain and Riley Meredith."""
    df = pd.read_parquet(PROCESSED_DIR / "bowling_leaderboard.parquet")

    sakib = df[df["player_name"] == "Sakib Hussain"].iloc[0]
    meredith = df[df["player_name"] == "Riley Meredith"].iloc[0]

    # Sakib Hussain unrounded mean is strictly below 1.82
    assert sakib["posterior_mean"] < 1.82
    assert np.isclose(sakib["posterior_mean"], 1.817738, atol=1e-4)

    # Riley Meredith unrounded mean is strictly above 1.82
    assert meredith["posterior_mean"] > 1.82
    assert np.isclose(meredith["posterior_mean"], 1.821739, atol=1e-4)

    # True Bayesian shrinkage prior mean is 1.82275596
    prior_mu = 1.822755960207317
    assert sakib["posterior_mean"] < prior_mu
    assert meredith["posterior_mean"] < prior_mu


# ==============================================================================
# PART 10: PROBABILITY STATEMENTS & REFERENCE PRIOR MEANS
# ==============================================================================

def test_probability_statements_and_prior_means():
    """Verifies prob_exceed_league_mean exists and values are mathematically sound."""
    for fname in ["batting_leaderboard.parquet", "bowling_leaderboard.parquet"]:
        df = pd.read_parquet(PROCESSED_DIR / fname)
        assert "prob_exceed_league_mean" in df.columns
        assert (df["prob_exceed_league_mean"] >= 0.0).all()
        assert (df["prob_exceed_league_mean"] <= 1.0).all()
        assert np.isclose(df["prob_exceed_league_mean"], df["prob_exceed_peers"]).all()


# ==============================================================================
# PART 11: COMPETITION QUALIFICATION EXPOSURE STANDARD (DEF-05)
# ==============================================================================

def test_competition_qualification_exposure():
    """Verifies DUAL_TOURNAMENT_QUALIFIED requires >=30 balls in both competitions."""
    views = pd.read_parquet(PROCESSED_DIR / "competition_candidate_views.parquet")
    assert "competition_qualification" in views.columns

    dual = views[views["competition_qualification"] == "DUAL_TOURNAMENT_QUALIFIED"]
    assert len(dual) > 0
    for _, r in dual.iterrows():
        assert r["ipl_pressure_balls"] >= 30, f"{r['player_name']} has <30 IPL balls"
        assert r["t20i_pressure_balls"] >= 30, f"{r['player_name']} has <30 T20I balls"

    ferreira = views[views["player_name"] == "Donovan Ferreira"].iloc[0]
    assert ferreira["competition_qualification"] == "IPL_QUALIFIED"
    assert ferreira["t20i_pressure_balls"] == 29

    narine = views[views["player_name"] == "Sunil Narine"].iloc[0]
    assert narine["competition_qualification"] == "IPL_QUALIFIED"
    assert narine["t20i_pressure_balls"] == 0


# ==============================================================================
# PART 12: REMEDIATION REPORT COMPLETENESS
# ==============================================================================

def test_remediation_reports_exist_and_complete():
    """Verifies r1_06_2_remediation_report.md exists and contains all required sections."""
    required_sections = [
        "Executive Summary & Governance Mandate",
        "Remediated Two-Dimensional Candidate Classification System",
        "DIMENSION A: PERFORMANCE EVIDENCE STATUS",
        "DIMENSION B: EVIDENCE VOLUME TIER",
        "Batting Population Reconciliation",
        "Bowling Population Reconciliation",
        "Key Candidate Classification Transitions",
        "Nicholas Pooran and Donovan Ferreira",
        "Resolution of the 87 vs. 88 Bowling Promising Discrepancy",
        "Candidate Sample Qualification Syntax Bug Fix",
        "Probability Statements & Reference Mean Disclosures",
        "Competition Qualification vs. Skill Transferability",
        "Strict Governance Scope Verification",
    ]

    for p in [REPORTS_DIR / "r1_06_2_remediation_report.md", ROOT_DIR / "r1_06_2_remediation_report.md"]:
        assert p.exists(), f"Missing report at {p}"
        content = p.read_text(encoding="utf-8")
        assert len(content) > 3000, f"Report {p} is too short"
        for sec in required_sections:
            assert sec.lower() in content.lower(), f"Missing section '{sec}' in {p}"


# ==============================================================================
# PART 13: UPDATED SHORTLIST MARKDOWN REPORTS
# ==============================================================================

def test_updated_shortlist_markdown_reports():
    """Verifies shortlist markdown reports contain remediated terminology."""
    bat_rep = (REPORTS_DIR / "r1_06_batting_shortlist.md").read_text(encoding="utf-8")
    assert "Two-Dimensional Classification System" in bat_rep
    assert "POSITIVE_CONSERVATIVE_EVIDENCE" in bat_rep
    assert "NEGATIVE_CONSERVATIVE_ESTIMATE" in bat_rep
    assert "EMERGING_HIGH_UPSIDE" in bat_rep
    assert "ESTABLISHED_MARGINAL_PERFORMER" in bat_rep
    assert "-34.24 SR pts" in bat_rep

    bowl_rep = (REPORTS_DIR / "r1_06_bowling_shortlist.md").read_text(encoding="utf-8")
    assert "Two-Dimensional Classification System" in bowl_rep
    assert "NEGATIVE_CONSERVATIVE_ESTIMATE" in bowl_rep
    assert "INCONCLUSIVE_EVIDENCE" in bowl_rep
    assert "Resolution of the 87 vs 88 Bowling Promising Discrepancy" in bowl_rep
    assert "+1.82 RPO" in bowl_rep


# ==============================================================================
# PART 14: METHODOLOGY REPORT UPDATED COMPLETENESS
# ==============================================================================

def test_methodology_report_updated_completeness():
    """Verifies methodology report contains Section 1.3 and remediated disclosures."""
    meth_rep = (REPORTS_DIR / "r1_06_methodology_and_limitations.md").read_text(encoding="utf-8")
    assert "Two-Dimensional Candidate Classification System" in meth_rep
    assert "Candidate Sample Qualification Logic (DEF-04 Fix)" in meth_rep
    assert "Competition Exposure vs Skill Transferability" in meth_rep
    assert "Probability Disclosures & Reference Prior Means" in meth_rep


# ==============================================================================
# PART 15: BACKWARD COMPATIBILITY PRESERVATION
# ==============================================================================

def test_backward_compatibility_preserved():
    """Verifies legacy columns exist and are consistent with previous audits."""
    bat_df = pd.read_parquet(PROCESSED_DIR / "batting_leaderboard.parquet")
    bowl_df = pd.read_parquet(PROCESSED_DIR / "bowling_leaderboard.parquet")

    assert "legacy_evidence_classification" in bat_df.columns
    assert "evidence_classification" in bat_df.columns
    assert (bat_df["legacy_evidence_classification"] == bat_df["evidence_classification"]).all()

    assert (bat_df["evidence_classification"] == "STRONG_EVIDENCE").sum() == 12
    assert (bowl_df["evidence_classification"] == "STRONG_EVIDENCE").sum() == 11


# ==============================================================================
# PART 16: STRICT COMPETITION SCOPE BOUNDARY
# ==============================================================================

def test_strict_scope_boundaries_across_all_outputs():
    """Verifies zero commercial, price, purse, or auction metrics across all datasets."""
    forbidden = ["auction", "price", "salary", "crore", "purse", "bid", "valuation"]

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
            for term in forbidden:
                assert term not in str(col).lower(), f"Forbidden term '{term}' found in column '{col}' of {fname}"

