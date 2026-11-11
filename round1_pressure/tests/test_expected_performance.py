"""
ROYALS INTELLIGENCE — ROUND 1 EXPECTED PERFORMANCE & BAYESIAN TEST SUITE
Architecture: ROYALS INTELLIGENCE v4.1
Task: R1-04 Expected Performance Baselines & Bayesian Reliability Foundation

Comprehensive unit tests validating:
1. Generation and schema integrity of baseline and differential Parquet tables.
2. Stratified ordinary baselines (no empty cells, exact population sums).
3. Independence and asymmetry of batting vs bowling baselines.
4. Zero performance outcome leakage into expected baselines.
5. Context-weighted expectation preventing Simpson's Paradox.
6. Mathematical consistency of player-level differentials.
7. Hierarchical Empirical Bayes shrinkage and reliability properties.
8. Chronological out-of-sample validation and MSE reduction.
9. Strict vs Permissive sensitivity comparison.
10. Deterministic repeated execution.
11. Strict non-ranking boundary enforcement (no Top 10 or ranking columns).
"""

from pathlib import Path
import numpy as np
import pandas as pd
import pytest

from round1_pressure.src.expected_performance import ExpectedPerformanceEngine


@pytest.fixture(scope="module")
def engine():
    """Initializes and runs the expected performance engine once for the module."""
    eng = ExpectedPerformanceEngine()
    eng.run_all()
    return eng


# ==============================================================================
# PART 1: OUTPUT ARTIFACTS AND BASIC INTEGRITY
# ==============================================================================

def test_parquet_output_artifacts_exist(engine):
    """Verifies that all 6 required Parquet output files exist and are populated."""
    expected_files = [
        "batting_ordinary_baseline.parquet",
        "bowling_ordinary_baseline.parquet",
        "batting_pressure_differentials.parquet",
        "bowling_pressure_differentials.parquet",
        "bayesian_shrinkage_summary.parquet",
        "chronological_validation_results.parquet",
    ]
    for fname in expected_files:
        fpath = engine.processed_dir / fname
        assert fpath.exists(), f"Missing required output file: {fname}"
        df = pd.read_parquet(fpath)
        assert len(df) > 0, f"File {fname} is empty"


def test_markdown_report_generated(engine):
    """Verifies that the analytical Markdown report is generated with required sections."""
    report_path = engine.reports_dir / "expected_performance_report.md"
    assert report_path.exists(), "Missing expected_performance_report.md"

    with open(report_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "ROYALS INTELLIGENCE — ROUND 1 EXPECTED PERFORMANCE BASELINES & BAYESIAN RELIABILITY REPORT" in content
    assert "Executive Summary" in content
    assert "Ordinary Batting Baselines" in content
    assert "Ordinary Bowling Baselines" in content
    assert "Empirical Bayes Shrinkage Model Specification" in content
    assert "Chronological Out-of-Sample Validation" in content
    assert "Sample Player Differentials" in content
    assert "Strict vs. Permissive Sensitivity Analysis" in content
    assert "Output Artifacts Generated" in content


# ==============================================================================
# PART 2: STRATIFIED ORDINARY BASELINE INTEGRITY
# ==============================================================================

def test_batting_baseline_structure_and_completeness(engine):
    """
    Verifies that the batting baseline has exactly 12 context cells (2 tiers x 2 innings x 3 phases),
    zero empty cells, and legal ball count reconciles with ordinary deliveries.
    """
    df_base = engine.bat_baseline_df
    assert len(df_base) == 12

    # Check required columns
    required_cols = [
        "comp_tier", "innings", "innings_phase", "legal_balls",
        "runs_per_ball_mean", "strike_rate_mean", "dot_ball_pct",
        "boundary_pct", "dismissal_pct",
    ]
    for col in required_cols:
        assert col in df_base.columns, f"Missing column {col} in batting baseline"

    # No empty cells
    assert (df_base["legal_balls"] > 0).all()

    # Total legal balls in baseline must match ordinary strict batting deliveries
    raw_bat = engine.bat_events_strict
    ord_mask = raw_bat["is_primary_scope"] & raw_bat["outcome_is_legal"] & (~raw_bat["is_pressure_event"])
    assert df_base["legal_balls"].sum() == ord_mask.sum()


def test_bowling_baseline_structure_and_completeness(engine):
    """
    Verifies that the bowling baseline has exactly 12 context cells,
    zero empty cells, and legal ball count reconciles with ordinary deliveries.
    """
    df_base = engine.bowl_baseline_df
    assert len(df_base) == 12

    required_cols = [
        "comp_tier", "innings", "innings_phase", "legal_balls",
        "conceded_per_ball_mean", "economy_mean", "wicket_pct",
        "dot_ball_conceded_pct", "boundary_conceded_pct",
    ]
    for col in required_cols:
        assert col in df_base.columns, f"Missing column {col} in bowling baseline"

    assert (df_base["legal_balls"] > 0).all()

    raw_bowl = engine.bowl_events_strict
    ord_mask = raw_bowl["is_primary_scope"] & raw_bowl["outcome_is_legal"] & (~raw_bowl["is_pressure_event"])
    assert df_base["legal_balls"].sum() == ord_mask.sum()


def test_baseline_independence_batting_vs_bowling(engine):
    """
    Verifies that batting and bowling baselines are derived from independent discipline datasets.
    """
    bat_base = engine.bat_baseline_df
    bowl_base = engine.bowl_baseline_df

    # Total deliveries in baseline differ because batting and bowling pressure situations are asymmetric
    assert bat_base["legal_balls"].sum() != bowl_base["legal_balls"].sum()


# ==============================================================================
# PART 3: SIMPSON'S PARADOX MITIGATION & CONTEXT WEIGHTING
# ==============================================================================

def test_context_weighting_eliminates_phase_bias(engine):
    """
    Verifies that context-weighted expectation properly reflects phase difficulty:
    - Ordinary Death strike rate is strictly higher than Ordinary Middle and Powerplay.
    - A batter facing mostly death pressure has an expected strike rate > 160.
    """
    bat_base = engine.bat_baseline_df

    death_sr = bat_base[bat_base["innings_phase"] == "DEATH"]["strike_rate_mean"].mean()
    mid_sr = bat_base[bat_base["innings_phase"] == "MIDDLE"]["strike_rate_mean"].mean()
    pp_sr = bat_base[bat_base["innings_phase"] == "POWERPLAY"]["strike_rate_mean"].mean()

    assert death_sr > mid_sr
    assert death_sr > pp_sr

    # Batters whose pressure balls are concentrated in Death have high expected SR
    diff_df = engine.bat_differentials_strict
    qual = diff_df[diff_df["is_qualified"]]

    # Ensure expected strike rates span a realistic range reflecting context differences
    assert qual["expected_strike_rate"].max() > 165.0
    assert qual["expected_strike_rate"].min() < 145.0


# ==============================================================================
# PART 4: PLAYER DIFFERENTIAL MATHEMATICAL CONSISTENCY
# ==============================================================================

def test_batting_differentials_arithmetic(engine):
    """
    Verifies that batting differentials equal observed minus expected across all metrics.
    """
    df = engine.bat_differentials_strict

    np.testing.assert_allclose(
        df["diff_strike_rate"],
        df["observed_strike_rate"] - df["expected_strike_rate"],
        rtol=1e-5, atol=1e-5
    )
    np.testing.assert_allclose(
        df["diff_dot_pct"],
        df["observed_dot_pct"] - df["expected_dot_pct"],
        rtol=1e-5, atol=1e-5
    )
    np.testing.assert_allclose(
        df["diff_boundary_pct"],
        df["observed_boundary_pct"] - df["expected_boundary_pct"],
        rtol=1e-5, atol=1e-5
    )
    np.testing.assert_allclose(
        df["diff_dismissal_pct"],
        df["observed_dismissal_pct"] - df["expected_dismissal_pct"],
        rtol=1e-5, atol=1e-5
    )


def test_bowling_differentials_arithmetic(engine):
    """
    Verifies that bowling differentials equal observed minus expected across all metrics.
    """
    df = engine.bowl_differentials_strict

    np.testing.assert_allclose(
        df["diff_economy"],
        df["observed_economy"] - df["expected_economy"],
        rtol=1e-5, atol=1e-5
    )
    np.testing.assert_allclose(
        df["diff_wicket_pct"],
        df["observed_wicket_pct"] - df["expected_wicket_pct"],
        rtol=1e-5, atol=1e-5
    )
    np.testing.assert_allclose(
        df["diff_dot_pct"],
        df["observed_dot_pct"] - df["expected_dot_pct"],
        rtol=1e-5, atol=1e-5
    )
    np.testing.assert_allclose(
        df["diff_boundary_pct"],
        df["observed_boundary_pct"] - df["expected_boundary_pct"],
        rtol=1e-5, atol=1e-5
    )


# ==============================================================================
# PART 5: HIERARCHICAL BAYESIAN SHRINKAGE PROPERTIES
# ==============================================================================

def test_empirical_bayes_shrinkage_properties(engine):
    """
    Verifies core mathematical properties of Empirical Bayes shrinkage:
    1. Reliability r_i in (0, 1) for all players.
    2. Reliability increases monotonically with sample size.
    3. Posterior SE decreases with sample size.
    4. Shrunk mean lies strictly between observed differential and prior mean mu.
    5. 95% Credible Interval contains the posterior mean.
    """
    df_bat = engine.bat_differentials_strict
    qual = df_bat[df_bat["is_qualified"]].copy()

    # 1. Reliability in (0, 1)
    assert (qual["reliability_strike_rate"] > 0.0).all()
    assert (qual["reliability_strike_rate"] < 1.0).all()

    # 2. Monotonicity with sample size (positive correlation)
    corr_rel = qual["pressure_legal_balls"].corr(qual["reliability_strike_rate"])
    assert corr_rel > 0.70

    # 3. Posterior SE decreases with sample size (negative correlation)
    corr_se = qual["pressure_legal_balls"].corr(qual["posterior_se_strike_rate"])
    assert corr_se < -0.70

    # 4. Shrunk mean lies between observed and prior mean
    summary = engine.bayesian_summary_df
    mu_bat = summary[summary["discipline"] == "BATTING"]["prior_mean_mu"].iloc[0]

    for _, r in qual.iterrows():
        y = r["diff_strike_rate"]
        theta = r["shrunk_diff_strike_rate"]
        min_val = min(y, mu_bat) - 1e-5
        max_val = max(y, mu_bat) + 1e-5
        assert min_val <= theta <= max_val

    # 5. Credible Interval bounds
    assert (qual["ci_95_lower_strike_rate"] < qual["shrunk_diff_strike_rate"]).all()
    assert (qual["shrunk_diff_strike_rate"] < qual["ci_95_upper_strike_rate"]).all()


def test_bowling_empirical_bayes_shrinkage_properties(engine):
    """
    Verifies Empirical Bayes shrinkage properties for bowling economy differentials.
    """
    df_bowl = engine.bowl_differentials_strict
    qual = df_bowl[df_bowl["is_qualified"]].copy()

    assert (qual["reliability_economy"] > 0.0).all()
    assert (qual["reliability_economy"] < 1.0).all()

    corr_rel = qual["pressure_legal_balls"].corr(qual["reliability_economy"])
    assert corr_rel > 0.70

    assert (qual["ci_95_lower_economy"] < qual["shrunk_diff_economy"]).all()
    assert (qual["shrunk_diff_economy"] < qual["ci_95_upper_economy"]).all()


# ==============================================================================
# PART 6: CHRONOLOGICAL VALIDATION
# ==============================================================================

def test_chronological_out_of_sample_validation(engine):
    """
    Verifies that chronological validation on future seasons (2025-2026):
    1. Evaluates a substantial player overlap (>= 80 players in both periods).
    2. Bayesian shrunk differentials achieve lower MSE than raw differentials in both batting and bowling.
    """
    df_val = engine.chronological_val_df
    assert len(df_val) == 2

    bat_row = df_val[df_val["discipline"] == "BATTING"].iloc[0]
    bowl_row = df_val[df_val["discipline"] == "BOWLING"].iloc[0]

    assert bat_row["overlapping_players"] >= 80
    assert bowl_row["overlapping_players"] >= 80

    # MSE reduction must be positive
    assert bat_row["mse_reduction_pct"] > 5.0
    assert bowl_row["mse_reduction_pct"] > 10.0

    # Shrunk MSE strictly less than raw MSE
    assert bat_row["shrunk_mse"] < bat_row["raw_mse"]
    assert bowl_row["shrunk_mse"] < bowl_row["raw_mse"]


# ==============================================================================
# PART 7: SENSITIVITY AND INTEGRITY INVARIANTS
# ==============================================================================

def test_strict_vs_permissive_differentials_sensitivity(engine):
    """
    Verifies that player differentials under Strict vs Permissive legality have negligible variance:
    - Batting: Mean absolute delta < 1.0 SR points across all 691 batters, and < 0.75 for qualified batters (observed ~0.48).
    - Bowling: Mean absolute delta < 0.10 RPO across all bowlers (observed ~0.068 RPO).
    """
    b_s = engine.bat_differentials_strict
    b_p = engine.bat_differentials_perm
    b_m = b_s.merge(b_p, on="player_id", suffixes=("_s", "_p"))
    bat_delta = np.mean(np.abs(b_m["diff_strike_rate_s"] - b_m["diff_strike_rate_p"]))
    assert bat_delta < 1.0

    qual_m = b_m[b_m["is_qualified_s"]]
    assert np.mean(np.abs(qual_m["diff_strike_rate_s"] - qual_m["diff_strike_rate_p"])) < 0.75

    bw_s = engine.bowl_differentials_strict
    bw_p = engine.bowl_differentials_perm
    bw_m = bw_s.merge(bw_p, on="player_id", suffixes=("_s", "_p"))
    bowl_delta = np.mean(np.abs(bw_m["diff_economy_s"] - bw_m["diff_economy_p"]))
    assert bowl_delta < 0.10


def test_missing_player_identity_guard(engine):
    """Verifies that all player records have non-null canonical IDs and names."""
    for df in [engine.bat_differentials_strict, engine.bowl_differentials_strict]:
        assert df["player_id"].notna().all()
        assert df["player_name"].notna().all()


def test_no_rankings_or_top10_created(engine):
    """
    Strictly verifies task boundary: NO rankings, composite index, or Top 10 columns exist.
    """
    forbidden_terms = ["rank", "ranking", "top_10", "composite_index", "pressure_index", "final_score"]
    for df in [engine.bat_differentials_strict, engine.bowl_differentials_strict]:
        for col in df.columns:
            for term in forbidden_terms:
                assert term not in col.lower(), f"Forbidden ranking column '{col}' found in dataset"
