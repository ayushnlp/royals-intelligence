"""
ROYALS INTELLIGENCE — ROUND 1 PRESSURE DETECTION TEST SUITE
Architecture: ROYALS INTELLIGENCE v4.1
Task: R1-03 Pressure Detection and Situation Classification Engine

Comprehensive unit tests validating:
1. Batting and bowling pressure independence and asymmetry.
2. Separation of pressure exposure (state_before) from performance outcomes.
3. Strict score uncertainty protection (exact RRR withheld on lower-bound / unresolved DLS).
4. Threshold quantile benchmarking and candidate definition profiling.
5. Strict vs Permissive scenario sensitivity.
6. Scope segregation (Super Overs, Emerging Tournaments).
7. Missing player identity guards and row-level uniqueness invariants.
8. Deterministic repeated execution.
"""

from pathlib import Path
import numpy as np
import pandas as pd
import pytest

from round1_pressure.src.pressure_detection import PressureDetectionEngine


@pytest.fixture(scope="module")
def engine():
    """Initializes and runs the pressure detection engine once for the test module."""
    eng = PressureDetectionEngine()
    eng.run_pressure_detection()
    return eng


# ==============================================================================
# PART 1: OUTPUT ARTIFACTS AND BASIC INTEGRITY
# ==============================================================================

def test_parquet_output_artifacts_exist(engine):
    """Verifies that all 6 required Parquet output files exist and are populated."""
    expected_files = [
        "batting_pressure_events_strict.parquet",
        "bowling_pressure_events_strict.parquet",
        "batting_pressure_events_permissive.parquet",
        "bowling_pressure_events_permissive.parquet",
        "pressure_definition_comparison.parquet",
        "pressure_coverage_summary.parquet",
    ]
    for fname in expected_files:
        fpath = engine.processed_dir / fname
        assert fpath.exists(), f"Missing required output file: {fname}"
        df = pd.read_parquet(fpath)
        assert len(df) > 0, f"File {fname} is empty"


def test_markdown_report_generated(engine):
    """Verifies that the analytical Markdown report is generated and contains required sections."""
    report_path = engine.reports_dir / "pressure_detection_report.md"
    assert report_path.exists(), "Missing pressure_detection_report.md"

    with open(report_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "ROYALS INTELLIGENCE — ROUND 1 PRESSURE DETECTION & SITUATION CLASSIFICATION REPORT" in content
    assert "Executive Summary" in content
    assert "Mathematical Framework & Candidate Definitions" in content
    assert "Threshold Selection Rationale & Empirical Benchmarks" in content
    assert "Coverage Summary (Recommended Definitions)" in content
    assert "Strict vs. Permissive Sensitivity Analysis" in content
    assert "Score Uncertainty Handling & Dimensions Preserved" in content
    assert "Limitations & Recommendations for Subsequent Tasks" in content


def test_row_count_and_primary_scope_invariants(engine):
    """
    Verifies that total delivery count matches 200,999 across all event files,
    and primary scope contains exactly 193,988 deliveries.
    """
    df_bat = engine.batting_events_strict
    df_bowl = engine.bowling_events_strict

    assert len(df_bat) == 200999
    assert len(df_bowl) == 200999
    assert df_bat["is_primary_scope"].sum() == 193988
    assert df_bowl["is_primary_scope"].sum() == 193988


# ==============================================================================
# PART 2: INDEPENDENCE AND ASYMMETRY OF BATTING VS BOWLING PRESSURE
# ==============================================================================

def test_batting_and_bowling_pressure_independence(engine):
    """
    Verifies that batting and bowling pressure situations are modeled independently.
    In many deliveries, the batter is pressured while the bowler is not (e.g. 120/8 chasing 160),
    or the bowler is pressured while the batter is not (e.g. 170/2 chasing 180 in death overs).
    """
    df_bat = engine.batting_events_strict[engine.batting_events_strict["is_primary_scope"]]
    df_bowl = engine.bowling_events_strict[engine.bowling_events_strict["is_primary_scope"]]

    bat_pres = df_bat["is_pressure_event"]
    bowl_pres = df_bowl["is_pressure_event"]

    # Total counts must not be artificially forced to equal each other
    assert bat_pres.sum() != bowl_pres.sum()
    assert bat_pres.sum() == 33005
    assert bowl_pres.sum() == 39436

    # Both batting-only pressure and bowling-only pressure must exist
    bat_only = bat_pres & (~bowl_pres)
    bowl_only = bowl_pres & (~bat_pres)

    assert bat_only.sum() > 0, "No batting-only pressure deliveries found"
    assert bowl_only.sum() > 0, "No bowling-only pressure deliveries found"


def test_death_overs_asymmetry_chase(engine):
    """
    Verifies domain truth: Death overs with high wickets in hand (>= 6)
    exert severe pressure on the BOWLER (boundary hazard), but NOT on the BATTER.
    """
    df_bat = engine.batting_events_strict
    df_bowl = engine.bowling_events_strict

    # Delivery where wickets remaining in death is 7
    cond_death_w7 = (df_bat["is_primary_scope"]) & (df_bat["innings_phase"] == "DEATH") & (df_bat["wickets_remaining_before"] >= 7)
    sub_bat = df_bat[cond_death_w7]
    sub_bowl = df_bowl[cond_death_w7]

    assert len(sub_bat) > 0
    # Bowler is flagged under assault pressure
    assert (sub_bowl["is_bowl_assault_high_wickets_death"] == True).all()
    # Batter is NOT flagged under death finite wickets pressure
    assert (sub_bat["is_bat_death_accel_w5"] == False).all()


# ==============================================================================
# PART 3: ZERO PERFORMANCE LEAKAGE INVARIANT
# ==============================================================================

def test_zero_leakage_of_performance_outcomes_into_pressure_classification(engine):
    """
    Verifies that pressure detection relies EXCLUSIVELY on situational state BEFORE the delivery.
    Mutating performance outcome variables (runs off bat, wicket fallen, runs conceded)
    must have ZERO effect on whether the delivery is classified as pressure.
    """
    df_strict = engine.delivery_states_strict.copy()

    # Synthetic test slice of 100 deliveries
    test_slice = df_strict.head(100).copy()

    # Classify baseline
    bat_orig = engine.classify_batting_pressure(test_slice)
    bowl_orig = engine.classify_bowling_pressure(test_slice)

    # Mutate performance outcomes completely: invert wickets and 10x runs
    mutated_slice = test_slice.copy()
    mutated_slice["runs"] = 6
    mutated_slice["is_wicket"] = True
    mutated_slice["delivery_bowler_conceded_runs"] = 25
    mutated_slice["is_bowler_wicket"] = True

    bat_mutated = engine.classify_batting_pressure(mutated_slice)
    bowl_mutated = engine.classify_bowling_pressure(mutated_slice)

    # Assert 100% identity in pressure classification flags
    assert (bat_orig["is_pressure_event"] == bat_mutated["is_pressure_event"]).all()
    assert (bat_orig["is_bat_composite_high"] == bat_mutated["is_bat_composite_high"]).all()
    assert (bowl_orig["is_pressure_event"] == bowl_mutated["is_pressure_event"]).all()
    assert (bowl_orig["is_bowl_composite_high"] == bowl_mutated["is_bowl_composite_high"]).all()


# ==============================================================================
# PART 4: STRICT SCORE UNCERTAINTY PROTECTION (R1-02.3 CONTRACT)
# ==============================================================================

def test_exact_rrr_chase_pressure_withheld_on_lower_bound_scores(engine):
    """
    Verifies that score-dependent chase pressure (BAT_CHASE_RRR) is strictly
    restricted to deliveries with EXACT scores and exact targets.
    Deliveries with LOWER_BOUND_ONLY must NEVER receive exact RRR pressure.
    """
    df_bat = engine.batting_events_strict[engine.batting_events_strict["is_primary_scope"]]

    lower_bound_delivs = df_bat[df_bat["score_reconstruction_status"] == "LOWER_BOUND_ONLY"]
    assert len(lower_bound_delivs) > 0

    # Strict withholding of exact chase definitions
    assert (lower_bound_delivs["is_bat_chase_rrr_p75"] == False).all()
    assert (lower_bound_delivs["is_bat_chase_rrr_p85"] == False).all()
    assert (lower_bound_delivs["is_bat_chase_rrr_p90"] == False).all()

    # Dimensions withheld must explicitly state exact score, target, and RRR
    lower_bound_inn2 = lower_bound_delivs[lower_bound_delivs["innings"] == 2]
    assert (lower_bound_inn2["dimensions_withheld"].str.contains("EXACT_SCORE,EXACT_TARGET,EXACT_RRR")).all()


def test_unresolved_dls_matches_withhold_exact_chase_pressure(engine):
    """
    Verifies that the 4 unresolved DLS matches (20182, 23674, 24822, 28334)
    strictly withhold exact chase pressure metrics (target_is_exact == False),
    while preserving valid score-independent pressure (death overs, wickets in hand).
    """
    df_bat = engine.batting_events_strict
    df_bowl = engine.bowling_events_strict

    unres_mids = [20182, 23674, 24822, 28334]
    unres_bat = df_bat[df_bat["match_id"].isin(unres_mids)]
    unres_bowl = df_bowl[df_bowl["match_id"].isin(unres_mids)]

    assert len(unres_bat) > 0

    # Target is never exact
    assert (unres_bat["target_is_exact"] == False).all()
    assert (unres_bat["is_bat_chase_rrr_p85"] == False).all()
    assert (unres_bowl["is_bowl_defend_tight_death_p85"] == False).all()

    # But score-independent structural pressure remains active where valid
    unres_death = unres_bat[(unres_bat["innings_phase"] == "DEATH") & (unres_bat["wickets_remaining_before"] <= 5)]
    assert len(unres_death) > 0
    assert (unres_death["is_bat_death_accel_w5"] == True).all()


def test_first_innings_deliveries_handle_chase_metrics_properly(engine):
    """
    Verifies that in Innings 1, target and RRR dimensions are documented as not applicable,
    and chase pressure flags are strictly False.
    """
    df_bat = engine.batting_events_strict[engine.batting_events_strict["is_primary_scope"]]
    inn1 = df_bat[df_bat["innings"] == 1]

    assert len(inn1) > 0
    assert (inn1["is_bat_chase_rrr_p75"] == False).all()
    assert (inn1["is_bat_chase_rrr_p85"] == False).all()
    assert (inn1["dimensions_withheld"].str.contains("TARGET_NOT_APPLICABLE_INN1,RRR_NOT_APPLICABLE_INN1")).all()


# ==============================================================================
# PART 5: SCOPE SEGREGATION AND EXCLUSION
# ==============================================================================

def test_super_overs_excluded_from_primary_pressure_rankings(engine):
    """
    Verifies that Super Overs (innings 3 & 4) are excluded from primary rankings
    (is_primary_scope == False) and cataloged appropriately.
    """
    df_bat = engine.batting_events_strict
    so_delivs = df_bat[df_bat["innings"].isin([3, 4])]

    assert len(so_delivs) == 38
    assert (so_delivs["is_primary_scope"] == False).all()

    # Primary tournament Super Overs (IPL / T20I) are marked EXCLUDED_SUPER_OVER
    primary_so = so_delivs[~so_delivs["comp_id"].isin([2670, 3289])]
    assert len(primary_so) == 26
    assert (primary_so["exclusion_reason"] == "EXCLUDED_SUPER_OVER").all()


def test_emerging_tournaments_excluded_from_primary_pressure_rankings(engine):
    """
    Verifies that Emerging Tournaments (comp_ids 2670 and 3289) are cataloged with
    exclusion_reason 'EXCLUDED_EMERGING_TOURNAMENT' and is_primary_scope == False.
    """
    df_bat = engine.batting_events_strict
    emerging = df_bat[df_bat["comp_id"].isin([2670, 3289])]

    assert len(emerging) == 6985
    assert (emerging["is_primary_scope"] == False).all()
    assert (emerging["exclusion_reason"] == "EXCLUDED_EMERGING_TOURNAMENT").all()


# ==============================================================================
# PART 6: STRICT VS PERMISSIVE SENSITIVITY
# ==============================================================================

def test_strict_vs_permissive_pressure_sensitivity(engine):
    """
    Verifies that the 259 ambiguous 'other' deliveries in primary scope
    produce minimal and documented variance between Strict and Permissive scenarios (< 0.1%).
    """
    bat_strict = engine.batting_events_strict[engine.batting_events_strict["is_primary_scope"]]
    bat_perm = engine.batting_events_permissive[engine.batting_events_permissive["is_primary_scope"]]

    b_strict_count = bat_strict["is_pressure_event"].sum()
    b_perm_count = bat_perm["is_pressure_event"].sum()

    diff_bat = abs(b_perm_count - b_strict_count)
    assert diff_bat <= 50, f"Batting pressure scenario sensitivity variance too high: {diff_bat}"

    bowl_strict = engine.bowling_events_strict[engine.bowling_events_strict["is_primary_scope"]]
    bowl_perm = engine.bowling_events_permissive[engine.bowling_events_permissive["is_primary_scope"]]

    bw_strict_count = bowl_strict["is_pressure_event"].sum()
    bw_perm_count = bowl_perm["is_pressure_event"].sum()

    diff_bowl = abs(bw_perm_count - bw_strict_count)
    assert diff_bowl <= 100, f"Bowling pressure scenario sensitivity variance too high: {diff_bowl}"
    assert (diff_bowl / len(bowl_strict)) < 0.001, "Variance exceeds 0.1% threshold"


# ==============================================================================
# PART 7: COVERAGE AND CANDIDATE DEFINITION MATRIX
# ==============================================================================

def test_definition_comparison_table_structure(engine):
    """
    Verifies that pressure_definition_comparison.parquet contains all required profiling fields
    for every candidate definition across Batting and Bowling.
    """
    df_comp = engine.comparison_df
    assert len(df_comp) == 22  # 11 batting + 11 bowling definitions

    required_cols = [
        "definition_id",
        "discipline",
        "threshold_level",
        "scope_type",
        "mathematical_rule",
        "threshold_selection_method",
        "eligible_deliveries",
        "percentage_of_primary_scope",
        "unique_matches",
        "unique_players",
        "ipl_deliveries",
        "t20i_deliveries",
        "missing_data_rate_pct",
        "score_completeness_dependency",
        "known_biases_limitations",
        "recommendation_status",
    ]
    for col in required_cols:
        assert col in df_comp.columns, f"Missing column {col} in comparison table"

    # All definitions must have valid positive delivery counts
    assert (df_comp["eligible_deliveries"] > 0).all()
    assert (df_comp["unique_matches"] > 0).all()
    assert (df_comp["unique_players"] > 0).all()


def test_coverage_summary_table_structure(engine):
    """
    Verifies that pressure_coverage_summary.parquet breaks down primary pressure
    across Tournament Tier, Innings, Phase, and Score Completeness.
    """
    df_cov = engine.coverage_summary_df
    assert len(df_cov) >= 9

    dims = set(df_cov["dimension"].unique())
    assert "Tournament Tier" in dims
    assert "Innings" in dims
    assert "Innings Phase" in dims
    assert "Score Completeness" in dims

    # Verify both IPL and T20I are covered with healthy percentages (15-25%)
    ipl_row = df_cov[(df_cov["dimension"] == "Tournament Tier") & (df_cov["dimension_value"] == "IPL")].iloc[0]
    t20i_row = df_cov[(df_cov["dimension"] == "Tournament Tier") & (df_cov["dimension_value"] == "Senior T20I")].iloc[0]

    assert 14.0 <= ipl_row["batting_pressure_percentage"] <= 20.0
    assert 15.0 <= t20i_row["batting_pressure_percentage"] <= 22.0
    assert 18.0 <= ipl_row["bowling_pressure_percentage"] <= 25.0
    assert 16.0 <= t20i_row["bowling_pressure_percentage"] <= 22.0


# ==============================================================================
# PART 8: MISSING PLAYER IDENTITY GUARDS & ROW-LEVEL UNIQUENESS
# ==============================================================================

def test_missing_player_identity_guard(engine):
    """
    Verifies that every primary scope delivery has a valid non-null canonical player_id
    for both batter and bowler.
    """
    df_bat = engine.batting_events_strict[engine.batting_events_strict["is_primary_scope"]]
    df_bowl = engine.bowling_events_strict[engine.bowling_events_strict["is_primary_scope"]]

    assert df_bat["player_id"].notna().all()
    assert df_bat["striker_id"].notna().all()
    assert df_bowl["player_id"].notna().all()
    assert df_bowl["bowler_id"].notna().all()


def test_no_duplicate_delivery_events(engine):
    """
    Verifies that there are no duplicate delivery events in either batting or bowling datasets.
    Key: (match_id, innings, delivery_seq_num).
    """
    df_bat = engine.batting_events_strict
    df_bowl = engine.bowling_events_strict

    assert df_bat.duplicated(subset=["match_id", "innings", "delivery_seq_num"]).sum() == 0
    assert df_bowl.duplicated(subset=["match_id", "innings", "delivery_seq_num"]).sum() == 0


def test_deterministic_repeated_runs(engine):
    """
    Verifies that running pressure classification repeatedly produces mathematically identical outputs.
    """
    slice_sample = engine.delivery_states_strict.sample(500, random_state=42).copy()

    run1_bat = engine.classify_batting_pressure(slice_sample)
    run2_bat = engine.classify_batting_pressure(slice_sample)

    assert (run1_bat["is_pressure_event"] == run2_bat["is_pressure_event"]).all()
    assert (run1_bat["pressure_definition_id"] == run2_bat["pressure_definition_id"]).all()
    assert (run1_bat["dimensions_available"] == run2_bat["dimensions_available"]).all()
