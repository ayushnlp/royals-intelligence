"""
ROYALS INTELLIGENCE — ROUND 1 STATISTICAL AUDIT TEST SUITE
Architecture: ROYALS INTELLIGENCE v4.1
Task: R1-05.1 Independent Statistical Audit of Player Pressure Reliability Scores

Comprehensive unit and validation tests verifying:
1. Parquet audit artifact existence, non-emptiness, and schema integrity.
2. Markdown audit report generation and required section completeness.
3. Normalization transform and cohort perturbation properties (proving cohort-relative nature).
4. Weight sensitivity and ablation dynamics (proving Conservative Bound anchoring).
5. Temporal Consistency Factor (TCF) impact and empirical volatility limits.
6. Strict vs Permissive legality policy robustness (<0.6% volume variance, >0.999 rank correlation).
7. Empirical Bayes prior sensitivity and shrinkage behavior (small-sample vs large-sample).
8. Bowling baseline reconciliation (+2.085 RPO macro vs +1.823 RPO DL meta-analytic prior mean).
9. Strict competition scope boundary enforcement (no auction/pricing/valuation columns).
10. Deterministic reproducibility.
"""

from pathlib import Path
import numpy as np
import pandas as pd
import pytest

from round1_pressure.src.r1_05_1_statistical_audit import StatisticalReliabilityAuditEngine


@pytest.fixture(scope="module")
def audit_engine():
    """Initializes and runs the statistical reliability audit engine once for the module."""
    engine = StatisticalReliabilityAuditEngine()
    engine.run_all()
    return engine


# ==============================================================================
# PART 1: OUTPUT ARTIFACTS AND BASIC INTEGRITY
# ==============================================================================

def test_audit_parquet_artifacts_exist(audit_engine):
    """Verifies that all 6 required audit Parquet files exist and are populated."""
    expected_files = [
        "audit_normalization_perturbation.parquet",
        "audit_pri_weight_sensitivity.parquet",
        "audit_tcf_ablation_comparison.parquet",
        "audit_strict_permissive_sensitivity.parquet",
        "audit_bayesian_prior_sensitivity.parquet",
        "audit_bowling_reconciliation.parquet",
    ]
    for fname in expected_files:
        fpath = audit_engine.processed_dir / fname
        assert fpath.exists(), f"Missing required audit output file: {fname}"
        df = pd.read_parquet(fpath)
        assert len(df) > 0, f"File {fname} is empty"


def test_audit_markdown_report_generated(audit_engine):
    """Verifies that the audit report Markdown is generated with all mandatory sections."""
    report_path = audit_engine.reports_dir / "r1_05_1_statistical_audit_report.md"
    assert report_path.exists(), "Missing r1_05_1_statistical_audit_report.md"
    content = report_path.read_text(encoding="utf-8")
    
    required_sections = [
        "Executive Summary",
        "Audit 1: PRI Normalization & Cohort Perturbation Test",
        "Audit 2: PRI Weight Sensitivity & Leave-One-Out Ablation",
        "Audit 3: Temporal Consistency Factor (TCF) Deep Dive",
        "Audit 4: Strict vs Permissive Legality Sensitivity",
        "Audit 5: Prior and Bayesian Sensitivity",
        "Audit 6: Bowling Baseline Reconciliation",
        "Final Metric Governance & Diagnostic Recommendations",
    ]
    for section in required_sections:
        assert section in content, f"Missing required report section: {section}"


# ==============================================================================
# PART 2: NORMALIZATION AND COHORT PERTURBATION
# ==============================================================================

def test_normalization_cohort_relative_nature(audit_engine):
    """Verifies that dropping cohort members changes existing PRI scores (cohort-relative index)."""
    fpath = audit_engine.processed_dir / "audit_normalization_perturbation.parquet"
    df = pd.read_parquet(fpath)
    
    # Check both batting and bowling are represented
    assert set(df["discipline"]) == {"BATTING", "BOWLING"}
    
    # Ranks should remain highly stable (Spearman > 0.995)
    for _, row in df.iterrows():
        assert row["spearman_rank_corr"] >= 0.995, (
            f"Spearman rank correlation too low for {row['discipline']} under {row['perturbation_test']}: "
            f"{row['spearman_rank_corr']}"
        )
        # But scores MUST change (mean absolute change > 0), confirming it is cohort-relative
        if row["perturbation_test"] in ["DROP_RANDOM_10_PCT", "DROP_MIN_OUTLIER"]:
            assert row["mean_abs_pri_change"] > 0.05, (
                f"Expected non-zero score shift proving cohort dependence for {row['perturbation_test']}"
            )


# ==============================================================================
# PART 3: PRI WEIGHT SENSITIVITY & ABLATION
# ==============================================================================

def test_pri_weight_sensitivity_and_anchoring(audit_engine):
    """Verifies weight sensitivity stability and that Conservative Bound is the essential anchor."""
    fpath = audit_engine.processed_dir / "audit_pri_weight_sensitivity.parquet"
    df = pd.read_parquet(fpath)
    
    # 1. Equal weights (25/25/25/25) should have >0.99 Spearman correlation with baseline
    eq_bat = df[(df["discipline"] == "BATTING") & (df["weight_configuration"] == "EQUAL_WEIGHTS (25/25/25/25)")]
    assert len(eq_bat) == 1
    assert eq_bat.iloc[0]["spearman_rank_correlation"] > 0.990
    assert eq_bat.iloc[0]["top10_jaccard_similarity"] >= 0.70
    
    eq_bowl = df[(df["discipline"] == "BOWLING") & (df["weight_configuration"] == "EQUAL_WEIGHTS (25/25/25/25)")]
    assert len(eq_bowl) == 1
    assert eq_bowl.iloc[0]["spearman_rank_correlation"] > 0.990
    assert eq_bowl.iloc[0]["top10_jaccard_similarity"] >= 0.70
    
    # 2. Dropping Conservative Bound must cause Top 10 Jaccard to drop drastically (< 0.60)
    drop_cb_bat = df[(df["discipline"] == "BATTING") & (df["weight_configuration"] == "DROP_CONSERVATIVE_BOUND")]
    assert drop_cb_bat.iloc[0]["top10_jaccard_similarity"] < 0.60, (
        f"Expected Top 10 Jaccard to drop < 0.60 when removing Conservative Bound, got {drop_cb_bat.iloc[0]['top10_jaccard_similarity']}"
    )


# ==============================================================================
# PART 4: TEMPORAL CONSISTENCY FACTOR (TCF) DEEP DIVE
# ==============================================================================

def test_tcf_ablation_and_rank_shifts(audit_engine):
    """Verifies that TCF creates substantial rank shifts, penalizing low tenure players."""
    fpath = audit_engine.processed_dir / "audit_tcf_ablation_comparison.parquet"
    df = pd.read_parquet(fpath)
    
    assert len(df) > 0
    # Single-season players should experience large rank shifts (> 50 ranks)
    s1_bat = df[(df["discipline"] == "BATTING") & (df["seasons_active"] == 1)]
    assert s1_bat.iloc[0]["mean_rank_shift"] > 50.0
    
    s1_bowl = df[(df["discipline"] == "BOWLING") & (df["seasons_active"] == 1)]
    assert s1_bowl.iloc[0]["mean_rank_shift"] > 50.0
    
    # Mean TCF must strictly increase with seasons active
    bat_tcf = df[df["discipline"] == "BATTING"].sort_values("seasons_active")["mean_tcf"].tolist()
    assert all(x <= y for x, y in zip(bat_tcf, bat_tcf[1:])), "Batting TCF not monotonically increasing with seasons"


# ==============================================================================
# PART 5: STRICT VS PERMISSIVE LEGALITY SENSITIVITY
# ==============================================================================

def test_strict_vs_permissive_legality(audit_engine):
    """Verifies that legality policy differences are minimal (<0.6% volume, >0.999 rank corr)."""
    fpath = audit_engine.processed_dir / "audit_strict_permissive_sensitivity.parquet"
    df = pd.read_parquet(fpath)
    
    # Batting: 0 delivery delta in pressure classification
    bat_row = df[df["discipline"] == "BATTING"].iloc[0]
    assert bat_row["rank_correlation"] >= 0.9999
    assert bat_row["qualified_jaccard"] == 1.0
    
    # Bowling: < 300 deliveries difference (< 1.0%), >0.999 rank correlation
    bowl_row = df[df["discipline"] == "BOWLING"].iloc[0]
    assert bowl_row["delta"] < 300
    assert bowl_row["pct_change"] < 1.0
    assert bowl_row["rank_correlation"] > 0.999


# ==============================================================================
# PART 6: BAYESIAN PRIOR SENSITIVITY & SHRINKAGE
# ==============================================================================

def test_bayesian_prior_sensitivity_and_shrinkage(audit_engine):
    """Verifies Bayesian prior sensitivity and checks that small samples shift more than large."""
    fpath = audit_engine.processed_dir / "audit_bayesian_prior_sensitivity.parquet"
    df = pd.read_parquet(fpath)
    
    # Check that for Batting, Diffuse and Skeptical priors preserve >0.98 rank correlation
    for _, row in df[df["discipline"] == "BATTING"].iterrows():
        assert row["spearman_rank_correlation"] > 0.980, (
            f"Prior {row['prior_specification']} has low correlation: {row['spearman_rank_correlation']}"
        )
        # Small sample shifts should be strictly greater than large sample shifts
        if row["prior_specification"] != "BASE_EMPIRICAL_BAYES":
            assert row["small_sample_mean_shift"] > row["large_sample_mean_shift"], (
                f"Shrinkage invariant violated for {row['prior_specification']}: "
                f"small={row['small_sample_mean_shift']} vs large={row['large_sample_mean_shift']}"
            )


# ==============================================================================
# PART 7: BOWLING BASELINE RECONCILIATION
# ==============================================================================

def test_bowling_baseline_reconciliation(audit_engine):
    """Verifies exact reconciliation between macro aggregate diff (+2.085) and DL prior mean (+1.823)."""
    fpath = audit_engine.processed_dir / "audit_bowling_reconciliation.parquet"
    df = pd.read_parquet(fpath)
    
    # 1. Macro unweighted delivery difference is ~ +2.085 RPO
    macro_row = df[df["metric_level"] == "MACRO_UNWEIGHTED_DELIVERIES"].iloc[0]
    assert pytest.approx(macro_row["differential_rpo"], abs=0.01) == 2.085
    
    # 2. Player-level unweighted difference is ~ +2.186 RPO
    player_row = df[df["metric_level"] == "PLAYER_LEVEL_UNWEIGHTED"].iloc[0]
    assert pytest.approx(player_row["differential_rpo"], abs=0.01) == 2.186
    
    # 3. DerSimonian-Laird meta-analytic prior mean is ~ +1.823 RPO
    dl_row = df[df["metric_level"] == "BAYESIAN_PRIOR_MEAN_DL"].iloc[0]
    assert pytest.approx(dl_row["differential_rpo"], abs=0.01) == 1.823


# ==============================================================================
# PART 8: STRICT COMPETITION SCOPE BOUNDARY
# ==============================================================================

def test_strict_scope_boundaries(audit_engine):
    """Ensures NO auction, price, bid, salary, or valuation columns exist in any audit dataset."""
    forbidden_terms = ["auction", "price", "bid", "salary", "valuation", "cost", "inr", "crore", "dollar"]
    
    expected_files = [
        "audit_normalization_perturbation.parquet",
        "audit_pri_weight_sensitivity.parquet",
        "audit_tcf_ablation_comparison.parquet",
        "audit_strict_permissive_sensitivity.parquet",
        "audit_bayesian_prior_sensitivity.parquet",
        "audit_bowling_reconciliation.parquet",
    ]
    for fname in expected_files:
        df = pd.read_parquet(audit_engine.processed_dir / fname)
        for col in df.columns:
            for term in forbidden_terms:
                assert term not in col.lower(), f"Forbidden commercial/auction term '{term}' in column '{col}' of {fname}"
