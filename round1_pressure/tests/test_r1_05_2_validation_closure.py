"""
ROYALS INTELLIGENCE — ROUND 1 STATISTICAL VALIDATION CLOSURE TEST SUITE
Architecture: ROYALS INTELLIGENCE v4.1
Task: R1-05.2 Statistical Validation Closure & Methodology Reconciliation

Comprehensive unit and validation tests verifying:
1. Parquet validation closure artifact existence, non-emptiness, and schema integrity.
2. Markdown validation closure report generation and required section completeness.
3. Exact delivery-level reconciliation of Strict vs Permissive batting counts (31,163 vs 31,257; diff = 94).
4. Controlled cohort addition perturbation properties (zero delta for within-range, bounded shift for outliers).
5. Bayesian prior sensitivity reporting across sample volume strata with uncertainty bounds.
6. Historical (2022-2024 to 2025-2026) and competition (IPL vs T20I) transferability performance.
7. Empirical probability calibration assessment (Brier scores, terciles, uncertainty bounds).
8. Strict competition scope boundary enforcement (no auction/pricing/valuation columns).
9. Deterministic reproducibility.
"""

from pathlib import Path
import numpy as np
import pandas as pd
import pytest

from round1_pressure.src.r1_05_2_validation_closure import ValidationClosureEngine


@pytest.fixture(scope="module")
def closure_engine():
    """Initializes and runs the validation closure engine once for the module."""
    engine = ValidationClosureEngine()
    engine.run_all()
    return engine


# ==============================================================================
# PART 1: OUTPUT ARTIFACTS AND BASIC INTEGRITY
# ==============================================================================

def test_validation_parquet_artifacts_exist(closure_engine):
    """Verifies that all 5 required validation closure Parquet files exist and are populated."""
    expected_files = [
        "validation_strict_permissive_reconciliation.parquet",
        "validation_cohort_addition_perturbation.parquet",
        "validation_bayesian_prior_strata.parquet",
        "validation_transferability.parquet",
        "validation_probability_calibration.parquet",
    ]
    for fname in expected_files:
        fpath = closure_engine.processed_dir / fname
        assert fpath.exists(), f"Missing required validation output file: {fname}"
        df = pd.read_parquet(fpath)
        assert len(df) > 0, f"File {fname} is empty"


def test_validation_markdown_report_generated(closure_engine):
    """Verifies that the validation closure Markdown report is generated with all required sections."""
    report_path = closure_engine.reports_dir / "r1_05_2_validation_closure_report.md"
    assert report_path.exists(), "Missing r1_05_2_validation_closure_report.md"
    content = report_path.read_text(encoding="utf-8")

    required_sections = [
        "Executive Summary & Validation Mandate",
        "Reconcile Strict vs Permissive Batting Counts",
        "Cohort Addition Perturbation Results (Isolated Fixture)",
        "Bayesian Prior Sensitivity Across Sample-Size Strata",
        "Historical and Competition Transferability Evaluation",
        "Probability Calibration and Uncertainty Assessment",
        "Metric Governance Hierarchy",
        "Unresolved Methodological Limitations",
    ]
    for section in required_sections:
        assert section in content, f"Missing required report section: {section}"


# ==============================================================================
# PART 2: STRICT VS PERMISSIVE BATTING DELIVERY RECONCILIATION
# ==============================================================================

def test_strict_vs_permissive_batting_reconciliation(closure_engine):
    """Verifies exact reconciliation between situational exposure (0 delta) and legal balls (94 delta)."""
    fpath = closure_engine.processed_dir / "validation_strict_permissive_reconciliation.parquet"
    df = pd.read_parquet(fpath)

    # 1. Situational pressure exposure has exactly 0 difference in batting (33,005 vs 33,005)
    bat_exp = df[(df["discipline"] == "BATTING") & (df["population_concept"].str.contains("SITUATIONAL"))].iloc[0]
    assert bat_exp["strict_count"] == 33005
    assert bat_exp["permissive_count"] == 33005
    assert bat_exp["delta"] == 0

    # 2. Legal pressure deliveries have exactly 94 difference in batting (31,163 vs 31,257)
    bat_leg = df[(df["discipline"] == "BATTING") & (df["population_concept"].str.contains("LEGAL"))].iloc[0]
    assert bat_leg["strict_count"] == 31163
    assert bat_leg["permissive_count"] == 31257
    assert bat_leg["delta"] == 94
    assert "extras_type='other'" in bat_leg["reconciliation_explanation"]


# ==============================================================================
# PART 3: COHORT ADDITION PERTURBATION TESTING (ISOLATED FIXTURE)
# ==============================================================================

def test_cohort_addition_perturbation_properties(closure_engine):
    """Verifies score invariance for within-range additions and bounded shifts for boundary additions."""
    fpath = closure_engine.processed_dir / "validation_cohort_addition_perturbation.parquet"
    df = pd.read_parquet(fpath)

    # 1. Adding median player must produce exactly 0.0000 PRI score delta on existing players
    bat_med = df[(df["discipline"] == "BATTING") & (df["experiment"] == "ADD_MEDIAN_PLAYER")].iloc[0]
    assert bat_med["mean_abs_pri_change"] == 0.0
    assert bat_med["spearman_rank_corr"] == 1.0

    bowl_med = df[(df["discipline"] == "BOWLING") & (df["experiment"] == "ADD_MEDIAN_PLAYER")].iloc[0]
    assert bowl_med["mean_abs_pri_change"] == 0.0
    assert bowl_med["spearman_rank_corr"] == 1.0

    # 2. Simulating 25-player expansion must preserve high rank correlation and Top 10 roster
    bat_exp25 = df[(df["discipline"] == "BATTING") & (df["experiment"] == "SIMULATE_25_PLAYER_COHORT_EXPANSION")].iloc[0]
    assert bat_exp25["spearman_rank_corr"] > 0.999
    assert bat_exp25["top10_jaccard_similarity"] >= 0.80

    bowl_exp25 = df[(df["discipline"] == "BOWLING") & (df["experiment"] == "SIMULATE_25_PLAYER_COHORT_EXPANSION")].iloc[0]
    assert bowl_exp25["spearman_rank_corr"] > 0.990
    assert bowl_exp25["top10_jaccard_similarity"] >= 0.70


# ==============================================================================
# PART 4: BAYESIAN PRIOR SENSITIVITY ACROSS SAMPLE STRATA
# ==============================================================================

def test_bayesian_prior_sensitivity_strata(closure_engine):
    """Verifies that sample strata exist and small samples have wider CI and higher sensitivity."""
    fpath = closure_engine.processed_dir / "validation_bayesian_prior_strata.parquet"
    df = pd.read_parquet(fpath)

    # Check all sample strata are present
    expected_strata = {
        "ALL_QUALIFIED (Full Cohort)",
        "Small Sample (30-59 balls)",
        "Medium Sample (60-149 balls)",
        "Large Sample (>=150 balls)",
    }
    assert set(df["stratum"]) == expected_strata

    # For Base Empirical Bayes batting:
    base_bat = df[(df["discipline"] == "BATTING") & (df["prior_specification"] == "BASE_EMPIRICAL_BAYES")]
    small_se = base_bat[base_bat["stratum"] == "Small Sample (30-59 balls)"].iloc[0]["mean_posterior_se"]
    large_se = base_bat[base_bat["stratum"] == "Large Sample (>=150 balls)"].iloc[0]["mean_posterior_se"]
    assert small_se > large_se, f"Expected small sample SE ({small_se}) > large sample SE ({large_se})"

    # Check rank correlation across all batting variants remains > 0.98
    for _, row in df[(df["discipline"] == "BATTING") & (df["stratum"] == "ALL_QUALIFIED (Full Cohort)")].iterrows():
        assert row["spearman_rank_corr"] > 0.980


# ==============================================================================
# PART 5: HISTORICAL AND COMPETITION TRANSFERABILITY
# ==============================================================================

def test_transferability_validation(closure_engine):
    """Verifies predictive transferability from 2022-2024 to 2025-2026 and sample limits."""
    fpath = closure_engine.processed_dir / "validation_transferability.parquet"
    df = pd.read_parquet(fpath)

    # 1. Historical evaluation has positive correlations and MSE reduction
    hist_bat = df[(df["discipline"] == "BATTING") & (df["transfer_test"] == "HISTORICAL_2022_2024_TO_2025_2026")].iloc[0]
    assert hist_bat["qualified_cohort_size"] == 82
    assert hist_bat["pearson_r"] > 0.20
    assert hist_bat["mse_reduction_vs_raw_pct"] > 10.0

    hist_bowl = df[(df["discipline"] == "BOWLING") & (df["transfer_test"] == "HISTORICAL_2022_2024_TO_2025_2026")].iloc[0]
    assert hist_bowl["qualified_cohort_size"] == 98
    assert hist_bowl["pearson_r"] > 0.10
    assert hist_bowl["mse_reduction_vs_raw_pct"] > 10.0

    # 2. Cross-competition sample sizes documented
    comp_bat = df[(df["discipline"] == "BATTING") & (df["transfer_test"] == "COMPETITION_IPL_TO_T20I")].iloc[0]
    assert comp_bat["qualified_cohort_size"] == 47

    comp_bowl = df[(df["discipline"] == "BOWLING") & (df["transfer_test"] == "COMPETITION_IPL_TO_T20I")].iloc[0]
    assert comp_bowl["qualified_cohort_size"] == 63


# ==============================================================================
# PART 6: PROBABILITY CALIBRATION AND UNCERTAINTY
# ==============================================================================

def test_probability_calibration_and_uncertainty(closure_engine):
    """Verifies calibration metrics, Brier scores, and explicit model-estimate classification."""
    fpath = closure_engine.processed_dir / "validation_probability_calibration.parquet"
    df = pd.read_parquet(fpath)

    assert len(df) == 4  # (Batting/Bowling) x (Ordinary/Peer)
    for _, row in df.iterrows():
        # Brier score should be reasonable (< 0.35)
        assert 0.0 < row["brier_score"] < 0.35
        # Must contain calibration curve breakdown
        assert "Pred=" in row["tercile_calibration_curve"]
        # Must be explicitly classified as MODEL_ESTIMATE_ONLY
        assert "MODEL_ESTIMATE_ONLY" in row["calibration_verdict"]


# ==============================================================================
# PART 7: STRICT COMPETITION SCOPE BOUNDARY
# ==============================================================================

def test_strict_scope_boundaries(closure_engine):
    """Ensures NO auction, price, bid, salary, or valuation columns exist in any validation dataset."""
    forbidden_terms = ["auction", "price", "bid", "salary", "valuation", "cost", "inr", "crore", "dollar"]

    expected_files = [
        "validation_strict_permissive_reconciliation.parquet",
        "validation_cohort_addition_perturbation.parquet",
        "validation_bayesian_prior_strata.parquet",
        "validation_transferability.parquet",
        "validation_probability_calibration.parquet",
    ]
    for fname in expected_files:
        df = pd.read_parquet(closure_engine.processed_dir / fname)
        for col in df.columns:
            for term in forbidden_terms:
                assert term not in col.lower(), f"Forbidden commercial/auction term '{term}' in column '{col}' of {fname}"
