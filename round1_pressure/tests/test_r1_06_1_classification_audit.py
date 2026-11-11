"""
ROYALS INTELLIGENCE — ROUND 1 CANDIDATE CLASSIFICATION AUDIT TEST SUITE
Architecture: ROYALS INTELLIGENCE v4.1
Task: R1-06.1 Independent Candidate Classification & Statistical Interpretation Audit

Comprehensive audit test suite verifying:
1. Audit deliverable report existence and required section completeness.
2. Population qualification accounting (824 batters, 596 bowlers; zero drops).
3. Evidence classification rules audit (12 Strong Batters, 11 Strong Bowlers, 4 Moderate Batters).
4. Conservative bound verification (only 2 batters with positive bound; zero bowlers with positive bound).
5. Promising candidate selection audit (9 promising batters, 87 promising bowlers).
6. Probability exceedance formula verification (P(Beat Peers) equals Phi((theta - mu_prior) / SE)).
7. Competition exposure and intra-player divergence verification.
8. Strict governance scope boundaries (no commercial/auction metrics).
"""

from pathlib import Path
import numpy as np
import pandas as pd
import pytest
from scipy import stats

PROCESSED_DIR = Path("round1_pressure/data/processed")
REPORTS_DIR = Path("round1_pressure/reports")


# ==============================================================================
# PART 1: AUDIT DELIVERABLE REPORTS EXISTENCE & COMPLETENESS
# ==============================================================================

def test_audit_reports_exist_and_complete():
    """Verifies that all 3 audit Markdown reports exist and contain critical audit sections."""
    reports = {
        "r1_06_1_classification_audit.md": [
            "Candidate Classification & Evidence Tier Independent Audit",
            "Executive Summary & Audit Mandate",
            "Exact Decision Rules Implemented in Code",
            "Evaluation of the `STRONG_EVIDENCE` Label",
            "Audit of `PROMISING_CANDIDATE` Selection",
            "Audit Recommendations & Proposed Classification Hierarchy",
        ],
        "r1_06_1_probability_audit.md": [
            "Probability Outputs & Statistical Exceedance Independent Audit",
            "Executive Summary: The \"100% P(Beat Peers)\" Investigation",
            "Mathematical Formulations & Code Tracing",
            "Dissecting the Batting Z-Scores Across the Shortlist",
            "Dissecting the Bowling Z-Scores Across the Shortlist",
            "Audit Recommendations on Probability Presentation",
        ],
        "r1_06_1_recommendations.md": [
            "Prioritized Defects & R1-06.2 Remediation Recommendations",
            "Official Audit Verdict",
            "PASS WITH LIMITATIONS",
            "Prioritized Defects Register",
            "Detailed Specifications for Task R1-06.2 Remediation",
            "Two-Dimensional Candidate Classification Framework",
        ],
    }

    for fname, sections in reports.items():
        # Check in round1_pressure/reports/
        fpath = REPORTS_DIR / fname
        assert fpath.exists(), f"Missing audit report in reports dir: {fname}"
        content = fpath.read_text(encoding="utf-8")
        assert len(content) > 1500, f"Audit report {fname} is incomplete"
        for sec in sections:
            assert sec.lower() in content.lower(), f"Missing section '{sec}' in {fname}"


# ==============================================================================
# PART 2: POPULATION QUALIFICATION ACCOUNTING AUDIT
# ==============================================================================

def test_population_accounting_audit():
    """Verifies exact population accounting across evaluated and qualified datasets."""
    bat_intel = pd.read_parquet(PROCESSED_DIR / "batting_intelligence.parquet")
    bowl_intel = pd.read_parquet(PROCESSED_DIR / "bowling_intelligence.parquet")
    qual = pd.read_parquet(PROCESSED_DIR / "qualified_candidates.parquet")
    non_qual = pd.read_parquet(PROCESSED_DIR / "non_qualified_candidates.parquet")

    # Batters
    assert len(bat_intel) == 824
    assert bat_intel["player_id"].nunique() == 824
    assert (bat_intel["is_qualified"] == True).sum() == 278
    assert (bat_intel["is_qualified"] == False).sum() == 546
    assert (bat_intel["pressure_legal_balls"] >= 30).sum() == 278

    # Bowlers
    assert len(bowl_intel) == 596
    assert bowl_intel["player_id"].nunique() == 596
    assert (bowl_intel["is_qualified"] == True).sum() == 239
    assert (bowl_intel["is_qualified"] == False).sum() == 357
    assert (bowl_intel["pressure_legal_balls"] >= 30).sum() == 239

    # Combined tables
    assert len(qual) == 517
    assert len(non_qual) == 903
    assert len(qual) + len(non_qual) == 824 + 596

    # Zero silent drops: 100% of non-qualified candidates have a non-empty reason
    assert non_qual["qualification_reason"].isna().sum() == 0
    assert (non_qual["qualification_reason"].str.len() > 10).all()


# ==============================================================================
# PART 3: STRONG EVIDENCE STATISTICAL EVALUATION
# ==============================================================================

def test_strong_evidence_conservative_bound_breakdown():
    """Verifies that only 2 batters and 0 bowlers establish positive conservative bounds."""
    bat_lead = pd.read_parquet(PROCESSED_DIR / "batting_leaderboard.parquet")
    bowl_lead = pd.read_parquet(PROCESSED_DIR / "bowling_leaderboard.parquet")

    strong_bat = bat_lead[bat_lead["evidence_classification"] == "STRONG_EVIDENCE"]
    assert len(strong_bat) == 12

    # Exactly 2 batters have positive conservative bound
    pos_cons_bat = strong_bat[strong_bat["primary_diagnostic_value"] > 0]
    assert len(pos_cons_bat) == 2
    pos_bat_names = set(pos_cons_bat["player_name"])
    assert pos_bat_names == {"Nicholas Pooran", "Donovan Ferreira"}

    # Exactly 10 batters have negative conservative bound
    neg_cons_bat = strong_bat[strong_bat["primary_diagnostic_value"] <= 0]
    assert len(neg_cons_bat) == 10
    # All 10 have positive posterior mean despite negative conservative bound
    assert (neg_cons_bat["posterior_mean"] >= 0.0).all()

    # Bowling audit
    strong_bowl = bowl_lead[bowl_lead["evidence_classification"] == "STRONG_EVIDENCE"]
    assert len(strong_bowl) == 11

    # Exactly 0 bowlers have positive conservative runs saved
    pos_cons_bowl = strong_bowl[strong_bowl["primary_diagnostic_value"] > 0]
    assert len(pos_cons_bowl) == 0

    # Exactly 1 bowler has negative posterior mean economy diff (Bumrah)
    neg_mean_bowl = strong_bowl[strong_bowl["posterior_mean"] < 0]
    assert len(neg_mean_bowl) == 1
    assert neg_mean_bowl.iloc[0]["player_name"] == "Jasprit Bumrah"


# ==============================================================================
# PART 4: AUDIT PROMISING CANDIDATE SELECTION
# ==============================================================================

def test_promising_candidate_selection_audit():
    """Verifies rules producing the 9 promising batters and 87 promising bowlers."""
    bat_lead = pd.read_parquet(PROCESSED_DIR / "batting_leaderboard.parquet")
    bowl_lead = pd.read_parquet(PROCESSED_DIR / "bowling_leaderboard.parquet")

    prom_bat = bat_lead[bat_lead["evidence_classification"] == "PROMISING_CANDIDATE"]
    assert len(prom_bat) == 9

    # Verify high-volume veterans exist in promising list (audit defect DEF-03)
    prom_names = set(prom_bat["player_name"])
    assert "Andre Russell" in prom_names
    assert "Suryakumar Yadav" in prom_names
    assert "Rahul Tewatia" in prom_names
    assert "Shashank Singh" in prom_names

    # Check Russell has 294 pressure balls
    russell = prom_bat[prom_bat["player_name"] == "Andre Russell"].iloc[0]
    assert russell["pressure_legal_balls"] == 294
    assert russell["pressure_matches"] >= 25

    # Check bowling promising count in parquet is exactly 87
    prom_bowl = bowl_lead[bowl_lead["evidence_classification"] == "PROMISING_CANDIDATE"]
    assert len(prom_bowl) == 87

    # Verify Riley Meredith and Sakib Hussain are at boundary 1.82
    meredith = bowl_lead[bowl_lead["player_name"] == "Riley Meredith"].iloc[0]
    assert meredith["posterior_mean"] == 1.82
    assert meredith["evidence_classification"] == "NEGATIVE_EVIDENCE"


# ==============================================================================
# PART 5: UNDOCUMENTED MODERATE EVIDENCE AUDIT
# ==============================================================================

def test_moderate_evidence_audit():
    """Verifies the 4 MODERATE_EVIDENCE batters and 0 MODERATE_EVIDENCE bowlers."""
    bat_lead = pd.read_parquet(PROCESSED_DIR / "batting_leaderboard.parquet")
    bowl_lead = pd.read_parquet(PROCESSED_DIR / "bowling_leaderboard.parquet")

    mod_bat = bat_lead[bat_lead["evidence_classification"] == "MODERATE_EVIDENCE"]
    assert len(mod_bat) == 4
    mod_bat_names = set(mod_bat["player_name"])
    assert mod_bat_names == {
        "Namboori Tilak Varma",
        "Romario Shepherd",
        "Rashid Khan",
        "Hardik Pandya",
    }
    # All 4 have negative posterior mean and conservative bound >= -15.0
    assert (mod_bat["posterior_mean"] <= 0.0).all()
    assert (mod_bat["primary_diagnostic_value"] >= -15.0).all()

    # Zero moderate bowlers
    mod_bowl = bowl_lead[bowl_lead["evidence_classification"] == "MODERATE_EVIDENCE"]
    assert len(mod_bowl) == 0


# ==============================================================================
# PART 6: PROBABILITY EXCEEDANCE FORMULA & Z-SCORE RECONSTRUCTION
# ==============================================================================

def test_probability_exceedance_formula_reconstruction():
    """Independently verifies that P(Beat Peers) equals Phi((theta - mu_prior) / SE)."""
    bat_lead = pd.read_parquet(PROCESSED_DIR / "batting_leaderboard.parquet")
    bowl_lead = pd.read_parquet(PROCESSED_DIR / "bowling_leaderboard.parquet")
    bayesian_summary = pd.read_parquet(PROCESSED_DIR / "bayesian_shrinkage_summary.parquet")

    mu_b = bayesian_summary[bayesian_summary["discipline"] == "BATTING"]["prior_mean_mu"].iloc[0]
    assert np.isclose(mu_b, -34.2384, atol=1e-3)

    mu_bw = bayesian_summary[bayesian_summary["discipline"] == "BOWLING"]["prior_mean_mu"].iloc[0]
    assert np.isclose(mu_bw, 1.8228, atol=1e-3)

    # Batting exceedance reconstruction
    for _, row in bat_lead.head(12).iterrows():
        expected_z = (row["posterior_mean"] - mu_b) / row["posterior_se"]
        expected_p_peer = stats.norm.cdf(expected_z)
        assert np.isclose(row["prob_exceed_peers"], expected_p_peer, atol=0.01)
        # All shortlisted batters exceed 99% probability
        assert row["prob_exceed_peers"] >= 0.99

    # Bowling exceedance reconstruction
    for _, row in bowl_lead.head(11).iterrows():
        expected_z = (mu_bw - row["posterior_mean"]) / row["posterior_se"]
        expected_p_peer = stats.norm.cdf(expected_z)
        assert np.isclose(row["prob_exceed_peers"], expected_p_peer, atol=0.01)
        assert row["prob_exceed_peers"] >= 0.88


# ==============================================================================
# PART 7: COMPETITION EXPOSURE & CROSS-TOURNAMENT DIVERGENCE AUDIT
# ==============================================================================

def test_competition_views_and_divergence_audit():
    """Verifies 30-ball threshold enforcement and exposes intra-player tournament divergence."""
    views = pd.read_parquet(PROCESSED_DIR / "competition_candidate_views.parquet")

    dual_candidates = views[views["competition_segment"] == "DUAL_COMPETITION_PROVEN"]
    assert len(dual_candidates) == 110

    for _, row in dual_candidates.iterrows():
        assert row["ipl_pressure_balls"] >= 30
        assert row["t20i_pressure_balls"] >= 30

    # Expose intra-player divergence in Sherfane Rutherford (DEF-05)
    rutherford = dual_candidates[dual_candidates["player_name"] == "Sherfane Rutherford"].iloc[0]
    ipl_cons = rutherford["ipl_conservative_metric"]
    t20i_cons = rutherford["t20i_conservative_metric"]
    assert ipl_cons < -50.0  # -52.95 in IPL
    assert t20i_cons > 10.0   # +11.39 in T20I
    # Divergence exceeds 60 SR points
    assert abs(t20i_cons - ipl_cons) > 60.0


# ==============================================================================
# PART 8: STRICT GOVERNANCE SCOPE BOUNDARIES
# ==============================================================================

def test_strict_governance_scope_boundaries():
    """Verifies no commercial, auction, purse, or bid terminology in any artifact."""
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
                assert term not in str(col).lower(), f"Forbidden term '{term}' in {fname} col '{col}'"
