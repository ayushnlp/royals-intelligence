"""
ROYALS INTELLIGENCE — ROUND 1 PLAYER PRESSURE RELIABILITY TEST SUITE
Architecture: ROYALS INTELLIGENCE v4.1
Task: R1-05 Explainable Player Pressure Reliability Scoring Engine

Comprehensive unit tests validating:
1. Parquet output artifact existence, non-emptiness, and schema integrity.
2. Markdown report generation and required section completeness.
3. Canonical player ID preservation, uniqueness, and non-null guarantees.
4. Complete independence and separation of batting and bowling tables.
5. Monotonicity and mathematical constraints of conservative credibility bounds.
6. Probability calibration and boundary properties of posterior exceedance metrics.
7. Temporal Consistency Factor (TCF) bounds and properties.
8. Multi-dimensional Composite Pressure Reliability Index (PRI) boundary constraints.
9. All-rounder two-way synthesis, metric preservation, and harmonic-vs-arithmetic inequality.
10. Full explainability evidence record completeness and content accuracy.
11. Pairwise scoring methodology agreement (Spearman rank correlations).
12. Strict scope boundary enforcement (no auction/pricing/valuation columns).
13. Deterministic reproducibility across repeated executions.
"""

from pathlib import Path
import numpy as np
import pandas as pd
import pytest

from round1_pressure.src.player_reliability import PlayerReliabilityEngine


@pytest.fixture(scope="module")
def engine():
    """Initializes and runs the player reliability engine once for the test module."""
    eng = PlayerReliabilityEngine()
    eng.run_all()
    return eng


# ==============================================================================
# PART 1: OUTPUT ARTIFACTS AND BASIC INTEGRITY
# ==============================================================================

def test_parquet_output_artifacts_exist(engine):
    """Verifies that all 4 required Parquet output files exist and are populated."""
    expected_files = [
        "batting_pressure_reliability.parquet",
        "bowling_pressure_reliability.parquet",
        "all_rounder_pressure_reliability.parquet",
        "scoring_methodology_comparison.parquet",
    ]
    for fname in expected_files:
        fpath = engine.processed_dir / fname
        assert fpath.exists(), f"Missing required output file: {fname}"
        df = pd.read_parquet(fpath)
        assert len(df) > 0, f"File {fname} is empty"


def test_markdown_report_generated(engine):
    """Verifies that the analytical Markdown report is generated with all required sections."""
    report_path = engine.reports_dir / "player_reliability_report.md"
    assert report_path.exists(), "Missing player_reliability_report.md"

    with open(report_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "ROYALS INTELLIGENCE — ROUND 1 EXPLAINABLE PLAYER PRESSURE RELIABILITY REPORT" in content
    assert "Executive Summary & Methodological Governance" in content
    assert "Mathematical Scoring Framework & Candidate Models" in content
    assert "Pairwise Methodological Agreement (Spearman Rank Correlations)" in content
    assert "Top Qualified Batters Under Pressure (Diagnostic Profile)" in content
    assert "Top Qualified Bowlers Under Pressure (Diagnostic Profile)" in content
    assert "All-Rounder Reliability (Two-Way Qualified Diagnostic)" in content
    assert "Sample Player Explainability Evidence Records" in content
    assert "Output Artifacts Generated" in content


# ==============================================================================
# PART 2: CANONICAL PLAYER ID PRESERVATION & SEPARATION
# ==============================================================================

def test_canonical_player_id_preservation_and_uniqueness(engine):
    """Verifies canonical player_id is preserved, non-null, integer, and unique in all tables."""
    for df, name in [
        (engine.bat_reliability_df, "Batting Reliability"),
        (engine.bowl_reliability_df, "Bowling Reliability"),
        (engine.all_rounder_df, "All-Rounder Reliability"),
    ]:
        assert "player_id" in df.columns, f"{name} missing player_id"
        assert df["player_id"].isnull().sum() == 0, f"{name} has null player_id"
        assert df["player_id"].duplicated().sum() == 0, f"{name} has duplicate player_id"
        assert pd.api.types.is_integer_dtype(df["player_id"]), f"{name} player_id must be integer"
        assert "player_name" in df.columns, f"{name} missing player_name"
        assert df["player_name"].isnull().sum() == 0, f"{name} has null player_name"


def test_separation_of_batting_and_bowling_tables(engine):
    """Verifies that batting and bowling tables maintain strict separation of discipline metrics."""
    b_df = engine.bat_reliability_df
    bw_df = engine.bowl_reliability_df

    # Batting table should not have bowling-specific differential columns
    assert "shrunk_diff_strike_rate" in b_df.columns
    assert "shrunk_diff_economy" not in b_df.columns
    assert "observed_runs" in b_df.columns
    assert "observed_conceded" not in b_df.columns

    # Bowling table should not have batting-specific differential columns
    assert "shrunk_diff_economy" in bw_df.columns
    assert "shrunk_diff_strike_rate" not in bw_df.columns
    assert "observed_conceded" in bw_df.columns
    assert "observed_runs" not in bw_df.columns


def test_population_counts_match_r1_04(engine):
    """Verifies that player counts and qualification numbers strictly match R1-04 baselines."""
    # R1-04 established 691 batters (278 qualified) and 479 bowlers (239 qualified)
    assert len(engine.bat_reliability_df) == 691
    assert engine.bat_reliability_df["is_qualified"].sum() == 278

    assert len(engine.bowl_reliability_df) == 479
    assert engine.bowl_reliability_df["is_qualified"].sum() == 239


# ==============================================================================
# PART 3: MATHEMATICAL SCORING CONSTRAINTS & MONOTONICITY
# ==============================================================================

def test_batting_conservative_bounds_monotonicity(engine):
    """
    Verifies that for all batters:
    score_conservative_95 <= score_conservative_bound <= shrunk_diff_strike_rate.
    """
    b_df = engine.bat_reliability_df
    diff = b_df["shrunk_diff_strike_rate"]
    se = b_df["posterior_se_strike_rate"]
    bound_84 = b_df["score_conservative_bound"]
    bound_95 = b_df["score_conservative_95"]

    # Mathematical identity check
    np.testing.assert_allclose(bound_84, diff - 1.0 * se, rtol=1e-5)
    np.testing.assert_allclose(bound_95, diff - 1.645 * se, rtol=1e-5)

    # Monotonicity check
    assert (bound_95 <= bound_84 + 1e-9).all()
    assert (bound_84 <= diff + 1e-9).all()


def test_bowling_conservative_bounds_monotonicity(engine):
    """
    Verifies that for all bowlers:
    score_conservative_95 <= score_conservative_bound <= (-shrunk_diff_economy).
    """
    bw_df = engine.bowl_reliability_df
    diff = bw_df["shrunk_diff_economy"]
    se = bw_df["posterior_se_economy"]
    bound_84 = bw_df["score_conservative_bound"]
    bound_95 = bw_df["score_conservative_95"]

    # Mathematical identity check: runs saved = -diff - k * se
    np.testing.assert_allclose(bound_84, -diff - 1.0 * se, rtol=1e-5)
    np.testing.assert_allclose(bound_95, -diff - 1.645 * se, rtol=1e-5)

    # Monotonicity check
    assert (bound_95 <= bound_84 + 1e-9).all()
    assert (bound_84 <= -diff + 1e-9).all()


def test_posterior_exceedance_probabilities_boundaries(engine):
    """Verifies that all exceedance probabilities are strictly bounded within [0, 1]."""
    for df, name in [
        (engine.bat_reliability_df, "Batting"),
        (engine.bowl_reliability_df, "Bowling"),
    ]:
        p_base = df["prob_exceed_baseline"]
        p_peer = df["prob_exceed_peer_mean"]

        assert (p_base >= 0.0).all() and (p_base <= 1.0).all(), f"{name} p_exceed_baseline outside [0, 1]"
        assert (p_peer >= 0.0).all() and (p_peer <= 1.0).all(), f"{name} p_exceed_peer_mean outside [0, 1]"
        assert p_base.isnull().sum() == 0, f"{name} has NaN in p_exceed_baseline"
        assert p_peer.isnull().sum() == 0, f"{name} has NaN in p_exceed_peer_mean"


def test_temporal_consistency_score_properties(engine):
    """
    Verifies that Temporal Consistency Score (TCF) is bounded in [0.40, 1.00]
    and properly scales with seasons active.
    """
    for df, name in [
        (engine.bat_reliability_df, "Batting"),
        (engine.bowl_reliability_df, "Bowling"),
    ]:
        tcf = df["temporal_consistency_score"]
        assert (tcf >= 0.40).all() and (tcf <= 1.00).all(), f"{name} TCF outside [0.40, 1.00]"
        assert tcf.isnull().sum() == 0, f"{name} has NaN in TCF"

        # Check that players with >= 4 seasons have higher average TCF than players with 1 season
        tcf_4plus = df[df["pressure_seasons"] >= 4]["temporal_consistency_score"]
        tcf_1 = df[df["pressure_seasons"] == 1]["temporal_consistency_score"]
        assert tcf_4plus.mean() > tcf_1.mean(), f"{name} TCF does not reward multi-season span"


def test_composite_pri_bounds_and_qualification(engine):
    """
    Verifies that Composite PRI is bounded in [0, 100] for qualified players
    and is NaN for unqualified players.
    """
    for df, name in [
        (engine.bat_reliability_df, "Batting"),
        (engine.bowl_reliability_df, "Bowling"),
    ]:
        qual = df[df["is_qualified"]]
        unqual = df[~df["is_qualified"]]

        # Qualified players must have valid PRI in [0, 100]
        assert qual["composite_pri"].isnull().sum() == 0, f"{name} qualified has NaN PRI"
        assert (qual["composite_pri"] >= 0.0).all() and (qual["composite_pri"] <= 100.0).all(), f"{name} PRI out of bounds"
        assert qual["composite_pri"].min() == 0.0, f"{name} scaled PRI min should be 0.0"
        assert qual["composite_pri"].max() == 100.0, f"{name} scaled PRI max should be 100.0"

        # Unqualified players must have NaN PRI (to prevent naive rankings on small samples)
        assert unqual["composite_pri"].isnull().all(), f"{name} unqualified should have NaN PRI"


# ==============================================================================
# PART 4: ALL-ROUNDER SYNTHESIS & METHODOLOGY AGREEMENT
# ==============================================================================

def test_all_rounder_synthesis_properties(engine):
    """
    Verifies all-rounder synthesis:
    1. Exactly 139 two-way qualified players.
    2. Preserves independent discipline metrics.
    3. Correct harmonic mean formula.
    4. Harmonic PRI <= Arithmetic PRI (AM-HM inequality).
    """
    ar_df = engine.all_rounder_df
    assert len(ar_df) == 139, f"Expected 139 two-way qualified players, got {len(ar_df)}"

    # Required preserved columns
    required_cols = [
        "player_id", "player_name", "bat_balls", "bat_matches", "bat_seasons",
        "bat_score_conservative", "bat_composite_pri", "bat_prob_exceed_peers",
        "bowl_balls", "bowl_matches", "bowl_seasons",
        "bowl_score_conservative", "bowl_composite_pri", "bowl_prob_exceed_peers",
        "all_rounder_harmonic_pri", "all_rounder_arithmetic_pri",
    ]
    for col in required_cols:
        assert col in ar_df.columns, f"Missing all-rounder column {col}"

    # Verify all players in all-rounder table met the 30-ball threshold in both disciplines
    assert (ar_df["bat_balls"] >= 30).all()
    assert (ar_df["bowl_balls"] >= 30).all()

    # Verify harmonic formula: 2 * (bat * bowl) / (bat + bowl)
    bat_pri = ar_df["bat_composite_pri"]
    bowl_pri = ar_df["bowl_composite_pri"]
    expected_hm = 2.0 * (bat_pri * bowl_pri) / (bat_pri + bowl_pri)
    np.testing.assert_allclose(ar_df["all_rounder_harmonic_pri"], expected_hm, rtol=1e-5)

    # Verify arithmetic formula: 0.5 * bat + 0.5 * bowl
    expected_am = 0.5 * bat_pri + 0.5 * bowl_pri
    np.testing.assert_allclose(ar_df["all_rounder_arithmetic_pri"], expected_am, rtol=1e-5)

    # AM-HM inequality: Harmonic Mean <= Arithmetic Mean (with tiny numerical epsilon)
    assert (ar_df["all_rounder_harmonic_pri"] <= ar_df["all_rounder_arithmetic_pri"] + 1e-9).all()


def test_scoring_methodology_comparison_agreement(engine):
    """
    Verifies that pairwise Spearman rank correlations across candidate models
    show strong positive alignment (> 0.50, mostly > 0.75).
    """
    sc_df = engine.scoring_comparison_df
    assert len(sc_df) == 50  # 5 models * 5 models * 2 disciplines

    # Check identical pairs have correlation 1.0
    self_pairs = sc_df[sc_df["score_metric_1"] == sc_df["score_metric_2"]]
    assert len(self_pairs) == 10
    np.testing.assert_allclose(self_pairs["spearman_rank_correlation"], 1.0, atol=1e-4)

    # Check batting correlations between candidate models
    b_sc = sc_df[sc_df["discipline"] == "BATTING"]
    # All batting correlations between candidate scores should be positive and >= 0.70
    assert (b_sc["spearman_rank_correlation"] >= 0.70).all()

    # Check bowling correlations
    bw_sc = sc_df[sc_df["discipline"] == "BOWLING"]
    # Bowling conservative bound and conservative 95 should correlate very highly (> 0.95)
    r_cons = bw_sc[
        (bw_sc["score_metric_1"] == "score_conservative_bound") &
        (bw_sc["score_metric_2"] == "score_conservative_95")
    ]["spearman_rank_correlation"].iloc[0]
    assert r_cons > 0.95


# ==============================================================================
# PART 5: EXPLAINABILITY AND STRICT SCOPE GOVERNANCE
# ==============================================================================

def test_explainability_records_completeness(engine):
    """Verifies that every player in batting and bowling tables has a valid explainability record."""
    for df, name, is_bat in [
        (engine.bat_reliability_df, "Batting", True),
        (engine.bowl_reliability_df, "Bowling", False),
    ]:
        assert "evidence_record" in df.columns
        assert df["evidence_record"].isnull().sum() == 0
        assert (df["evidence_record"].str.len() > 50).all()

        # Check sample string content
        sample_rec = df["evidence_record"].iloc[0]
        if is_bat:
            assert "pressure balls" in sample_rec
            assert "Expected SR" in sample_rec
            assert "Observed SR" in sample_rec
            assert "Empirical Bayes posterior" in sample_rec
            assert "Conservative 84% lower bound" in sample_rec
        else:
            assert "pressure balls" in sample_rec
            assert "Expected Econ" in sample_rec
            assert "Observed Econ" in sample_rec
            assert "Empirical Bayes posterior" in sample_rec
            assert "Conservative 84% runs saved" in sample_rec


def test_strict_scope_boundaries_enforced(engine):
    """
    CRITICAL GOVERNANCE TEST:
    Verifies that NO forbidden auction, price, valuation, or squad-fit columns
    exist in any parquet output or generated dataframe.
    """
    forbidden_terms = ["auction", "price", "valuation", "purse", "cost", "salary", "bid"]

    for df, name in [
        (engine.bat_reliability_df, "batting_pressure_reliability"),
        (engine.bowl_reliability_df, "bowling_pressure_reliability"),
        (engine.all_rounder_df, "all_rounder_pressure_reliability"),
        (engine.scoring_comparison_df, "scoring_methodology_comparison"),
    ]:
        for col in df.columns:
            for term in forbidden_terms:
                assert term not in col.lower(), f"Forbidden term '{term}' found in column '{col}' of {name}"


def test_deterministic_reproducibility(engine):
    """
    Verifies that running reliability calculations twice on identical inputs
    produces bitwise-identical results.
    """
    eng2 = PlayerReliabilityEngine()
    eng2.run_all()

    pd.testing.assert_frame_equal(engine.bat_reliability_df, eng2.bat_reliability_df)
    pd.testing.assert_frame_equal(engine.bowl_reliability_df, eng2.bowl_reliability_df)
    pd.testing.assert_frame_equal(engine.all_rounder_df, eng2.all_rounder_df)
    pd.testing.assert_frame_equal(engine.scoring_comparison_df, eng2.scoring_comparison_df)

