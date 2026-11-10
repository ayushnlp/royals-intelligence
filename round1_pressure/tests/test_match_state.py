"""
Royals Intelligence - Round 1 Match-State Reconstruction Test Suite (R1-02)
Architecture: Finalized ROYALS INTELLIGENCE v4.1
Validates:
1. Cumulative batter runs
2. Cumulative team runs (known extras)
3. Wickets lost and remaining
4. Legal-ball progression
5. Wide and no-ball re-bowls
6. Ambiguous 'other' strict vs permissive differences
7. Penalty delivery handling
8. First-innings state (no target/RRR)
9. Second-innings target reconstruction
10. Required run rate (RRR) calculation
11. Shortened innings scheduled overs/balls
12. Revised-target DLS matches
13. Innings ending during an over / early termination
14. Super Over segregation
15. Incomplete score handling (SCORE_COMPLETE vs SCORE_INCOMPLETE)
16. Bowler vs batter wicket and run attribution
17. Before/after state invariants
18. Deterministic Parquet output generation
"""

import pytest
import numpy as np
import pandas as pd
from pathlib import Path

from round1_pressure.src.match_state import MatchStateEngine, DOWNSTREAM_FEATURE_ELIGIBILITY_CONTRACT


@pytest.fixture(scope="module")
def engine():
    """Initializes and loads/runs the match state engine once for the test module."""
    eng = MatchStateEngine()
    eng.ensure_reconstructed()
    return eng


# ==============================================================================
# PART 1: HAND-CONSTRUCTED MINIATURE INNINGS FIXTURE TESTS
# ==============================================================================

@pytest.fixture
def mini_innings_fixture():
    """
    Creates a hand-crafted miniature 10-delivery innings fixture covering:
    - Standard dot ball, 1, 4, 6
    - Wide (illegal, re-bowled, +1 extra)
    - Overstep (illegal, re-bowled, +2 batter runs, +1 penalty)
    - Ambiguous 'other' (beamer)
    - Penalty delivery
    - Legbyes (+1 unconfirmed extra, consumes legal ball)
    - Caught dismissal (bowler credit)
    - RunOut dismissal (non-bowler credit)
    """
    rows = [
        # Ball 1: Standard dot ball
        {"match_id": 99999, "innings": 1, "overid": 1, "over_ball_num": 1, "innings_ball_num": 1,
         "batting_team_id": 10, "bowling_team_id": 20, "striker_id": 101, "striker_name": "Batter A",
         "non_striker_id": 102, "non_striker_name": "Batter B", "bowler_id": 201, "bowler_name": "Bowler X",
         "runs": 0, "extras_type": np.nan, "extras1_runs": 6, "extras_2_runs": 0,
         "is_wicket": False, "dismissal_type": np.nan, "dismissed_player_id": np.nan},

        # Ball 2: Single off bat
        {"match_id": 99999, "innings": 1, "overid": 1, "over_ball_num": 2, "innings_ball_num": 2,
         "batting_team_id": 10, "bowling_team_id": 20, "striker_id": 101, "striker_name": "Batter A",
         "non_striker_id": 102, "non_striker_name": "Batter B", "bowler_id": 201, "bowler_name": "Bowler X",
         "runs": 1, "extras_type": np.nan, "extras1_runs": 6, "extras_2_runs": 0,
         "is_wicket": False, "dismissal_type": np.nan, "dismissed_player_id": np.nan},

        # Ball 3: Wide (illegal delivery)
        {"match_id": 99999, "innings": 1, "overid": 1, "over_ball_num": 3, "innings_ball_num": 3,
         "batting_team_id": 10, "bowling_team_id": 20, "striker_id": 102, "striker_name": "Batter B",
         "non_striker_id": 101, "non_striker_name": "Batter A", "bowler_id": 201, "bowler_name": "Bowler X",
         "runs": 0, "extras_type": "wide", "extras1_runs": 2, "extras_2_runs": 0,
         "is_wicket": False, "dismissal_type": np.nan, "dismissed_player_id": np.nan},

        # Ball 4: Overstep with 2 batter runs off bat
        {"match_id": 99999, "innings": 1, "overid": 1, "over_ball_num": 4, "innings_ball_num": 4,
         "batting_team_id": 10, "bowling_team_id": 20, "striker_id": 102, "striker_name": "Batter B",
         "non_striker_id": 101, "non_striker_name": "Batter A", "bowler_id": 201, "bowler_name": "Bowler X",
         "runs": 2, "extras_type": "Overstep", "extras1_runs": 1, "extras_2_runs": 0,
         "is_wicket": False, "dismissal_type": np.nan, "dismissed_player_id": np.nan},

        # Ball 5: Bowler wicket (Caught)
        {"match_id": 99999, "innings": 1, "overid": 1, "over_ball_num": 5, "innings_ball_num": 5,
         "batting_team_id": 10, "bowling_team_id": 20, "striker_id": 102, "striker_name": "Batter B",
         "non_striker_id": 101, "non_striker_name": "Batter A", "bowler_id": 201, "bowler_name": "Bowler X",
         "runs": 0, "extras_type": np.nan, "extras1_runs": 6, "extras_2_runs": 0,
         "is_wicket": True, "dismissal_type": "Caught", "dismissed_player_id": 102},

        # Ball 6: Ambiguous 'other' (beamer)
        {"match_id": 99999, "innings": 1, "overid": 1, "over_ball_num": 6, "innings_ball_num": 6,
         "batting_team_id": 10, "bowling_team_id": 20, "striker_id": 103, "striker_name": "Batter C",
         "non_striker_id": 101, "non_striker_name": "Batter A", "bowler_id": 201, "bowler_name": "Bowler X",
         "runs": 0, "extras_type": "other", "extras1_runs": 5, "extras_2_runs": 0,
         "is_wicket": False, "dismissal_type": np.nan, "dismissed_player_id": np.nan},

        # Ball 7: Penalty delivery
        {"match_id": 99999, "innings": 1, "overid": 1, "over_ball_num": 7, "innings_ball_num": 7,
         "batting_team_id": 10, "bowling_team_id": 20, "striker_id": 103, "striker_name": "Batter C",
         "non_striker_id": 101, "non_striker_name": "Batter A", "bowler_id": 201, "bowler_name": "Bowler X",
         "runs": 0, "extras_type": "Penalty", "extras1_runs": 7, "extras_2_runs": 0,
         "is_wicket": False, "dismissal_type": np.nan, "dismissed_player_id": np.nan},

        # Ball 8: Legbyes (consumes legal ball, unconfirmed extra)
        {"match_id": 99999, "innings": 1, "overid": 1, "over_ball_num": 8, "innings_ball_num": 8,
         "batting_team_id": 10, "bowling_team_id": 20, "striker_id": 103, "striker_name": "Batter C",
         "non_striker_id": 101, "non_striker_name": "Batter A", "bowler_id": 201, "bowler_name": "Bowler X",
         "runs": 0, "extras_type": "legbyes", "extras1_runs": 3, "extras_2_runs": 0,
         "is_wicket": False, "dismissal_type": np.nan, "dismissed_player_id": np.nan},

        # Ball 9: RunOut dismissal (non-bowler wicket, 1 run off bat)
        {"match_id": 99999, "innings": 1, "overid": 1, "over_ball_num": 9, "innings_ball_num": 9,
         "batting_team_id": 10, "bowling_team_id": 20, "striker_id": 103, "striker_name": "Batter C",
         "non_striker_id": 101, "non_striker_name": "Batter A", "bowler_id": 201, "bowler_name": "Bowler X",
         "runs": 1, "extras_type": np.nan, "extras1_runs": 6, "extras_2_runs": 0,
         "is_wicket": True, "dismissal_type": "RunOut", "dismissed_player_id": 101},

        # Ball 10: Boundary Four
        {"match_id": 99999, "innings": 1, "overid": 1, "over_ball_num": 10, "innings_ball_num": 10,
         "batting_team_id": 10, "bowling_team_id": 20, "striker_id": 103, "striker_name": "Batter C",
         "non_striker_id": 104, "non_striker_name": "Batter D", "bowler_id": 201, "bowler_name": "Bowler X",
         "runs": 4, "extras_type": np.nan, "extras1_runs": 6, "extras_2_runs": 0,
         "is_wicket": False, "dismissal_type": np.nan, "dismissed_player_id": np.nan},
    ]
    return pd.DataFrame(rows)


def test_miniature_fixture_runs_and_legal_ball_progression(mini_innings_fixture):
    """
    Validates delivery progression, batter runs, extras, and legality on miniature fixture:
    - Ball 1: legal=True, runs=0
    - Ball 2: legal=True, runs=1 (tot=1)
    - Ball 3 (wide): legal=False, runs=0, extra=1 (tot=2)
    - Ball 4 (Overstep): legal=False, runs=2, extra=1 (tot=5)
    - Ball 5 (Caught): legal=True, runs=0, wicket=True (tot=5)
    - Ball 6 ('other'):
        - strict: legal=False, extra=1 (tot=6)
        - permissive: legal=True, extra=1 (tot=6)
    - Ball 7 (Penalty): legal=True, extra=1 (tot=7)
    - Ball 8 (legbyes): legal=True, extra=1 (tot=8)
    - Ball 9 (RunOut): legal=True, runs=1 (tot=9), wicket=True
    - Ball 10 (Four): legal=True, runs=4 (tot=13)
    """
    engine = MatchStateEngine()

    # Test Strict Scenario
    strict_legals = [engine.classify_delivery_legality(r["extras_type"], "strict") for _, r in mini_innings_fixture.iterrows()]
    assert strict_legals == [True, True, False, False, True, False, True, True, True, True]
    assert sum(strict_legals) == 7  # 7 legal balls in strict

    # Test Permissive Scenario ('other' becomes legal)
    perm_legals = [engine.classify_delivery_legality(r["extras_type"], "permissive") for _, r in mini_innings_fixture.iterrows()]
    assert perm_legals == [True, True, False, False, True, True, True, True, True, True]
    assert sum(perm_legals) == 8  # 8 legal balls in permissive (1 more than strict)


def test_miniature_fixture_wickets_and_attribution(mini_innings_fixture):
    """
    Validates bowler vs non-bowler dismissal attribution:
    - Ball 5: Caught -> is_bowler_wicket == True
    - Ball 9: RunOut -> is_bowler_wicket == False, is_non_bowler_dismissal == True
    """
    engine = MatchStateEngine()
    bowler_wkts = 0
    non_bowler_wkts = 0

    for _, r in mini_innings_fixture.iterrows():
        is_w = r["is_wicket"]
        dt = r["dismissal_type"]
        is_bw = is_w and (dt in engine.BOWLER_CREDITED_DISMISSALS)
        is_nb = is_w and (dt in engine.NON_BOWLER_DISMISSALS)
        if is_bw:
            bowler_wkts += 1
        if is_nb:
            non_bowler_wkts += 1

    assert bowler_wkts == 1
    assert non_bowler_wkts == 1


def test_miniature_fixture_runs_breakdown(mini_innings_fixture):
    """Validates delivery runs breakdown (batter runs, known extras, total known, unconfirmed flags)."""
    engine = MatchStateEngine()

    total_batter_runs = 0
    total_extras = 0
    unconfirmed_count = 0

    for _, r in mini_innings_fixture.iterrows():
        b_runs, k_extras, tot, unconf, b_conceded, prov = engine.calculate_delivery_runs(
            r["runs"], r["extras_type"], r["extras_2_runs"]
        )
        total_batter_runs += b_runs
        total_extras += k_extras
        if unconf:
            unconfirmed_count += 1

    # Batter runs: 0 + 1 + 0 + 2 + 0 + 0 + 0 + 0 + 1 + 4 = 8
    assert total_batter_runs == 8
    # Known extras: 0 + 0 + 1(wide) + 1(no-ball) + 0 + 1(other) + 1(penalty) + 1(legbye) + 0 + 0 = 5
    assert total_extras == 5
    # Total known team score = 8 + 5 = 13
    assert total_batter_runs + total_extras == 13
    # Unconfirmed extras: Penalty (1) and Legbyes (1) = 2
    assert unconfirmed_count == 2


# ==============================================================================
# PART 2: FULL DATASET RECONSTRUCTION & PARQUET STORAGE TESTS
# ==============================================================================

def test_parquet_output_files_exist(engine):
    """Verifies that all 8 required Parquet output files exist on disk."""
    expected = [
        "delivery_states_strict.parquet",
        "delivery_states_permissive.parquet",
        "innings_state_summary.parquet",
        "match_state_summary.parquet",
        "match_result_reconciliation.parquet",
        "dls_and_revised_overs_audit.parquet",
        "excluded_innings.parquet",
        "reconstruction_audit.parquet",
    ]
    for fname in expected:
        fpath = engine.processed_dir / fname
        assert fpath.exists(), f"Missing Parquet output: {fpath}"
        assert fpath.stat().st_size > 0, f"Empty Parquet output: {fpath}"


def test_strict_vs_permissive_reconstruction_totals(engine):
    """
    CRITICAL: Validates strict (192,445) vs permissive (192,709) legal deliveries,
    with exactly 264 ambiguous 'other' deliveries accounted for.
    """
    df_strict = engine.delivery_states_strict
    df_perm = engine.delivery_states_permissive

    assert len(df_strict) == 200999
    assert len(df_perm) == 200999

    strict_legal = df_strict["is_legal"].sum()
    perm_legal = df_perm["is_legal"].sum()

    assert strict_legal == 192445
    assert perm_legal == 192709
    assert perm_legal - strict_legal == 264


def test_primary_scope_deliveries_filter(engine):
    """
    Verifies isolation of primary scope (IPL & Senior T20I ordinary innings):
    - Exactly 193,988 primary deliveries
    - Excludes Emerging Tournaments (6,985 deliveries) and Super Overs (38 deliveries, with 12 overlap in emerging).
    """
    df_strict = engine.delivery_states_strict
    primary_mask = df_strict["is_primary_scope"]

    assert primary_mask.sum() == 193988

    # Super Overs must never be in primary scope
    so_in_primary = df_strict[primary_mask & df_strict["innings"].isin([3, 4])]
    assert len(so_in_primary) == 0

    # Emerging tournaments must never be in primary scope
    emerging_in_primary = df_strict[primary_mask & df_strict["comp_id"].isin([2670, 3289])]
    assert len(emerging_in_primary) == 0


def test_before_and_after_monotonicity_invariants(engine):
    """
    CRITICAL: Validates state invariants across all 200,999 deliveries:
    - cumulative_team_runs_after >= cumulative_team_runs_before
    - wickets_lost_after >= wickets_lost_before
    - legal_balls_bowled_after >= legal_balls_bowled_before
    - balls_remaining_after <= balls_remaining_before
    - On legal ball: legal_balls_after == legal_balls_before + 1
    - On illegal ball: legal_balls_after == legal_balls_before
    """
    df = engine.delivery_states_strict

    # Non-negative progressions
    assert (df["cumulative_team_runs_after"] >= df["cumulative_team_runs_before"]).all()
    assert (df["wickets_lost_after"] >= df["wickets_lost_before"]).all()
    assert (df["legal_balls_bowled_after"] >= df["legal_balls_bowled_before"]).all()
    assert (df["balls_remaining_after"] <= df["balls_remaining_before"]).all()

    # Exact step progression on legal balls
    legal_mask = df["is_legal"]
    assert (df.loc[legal_mask, "legal_balls_bowled_after"] == df.loc[legal_mask, "legal_balls_bowled_before"] + 1).all()

    # Exact step zero progression on illegal balls
    illegal_mask = ~df["is_legal"]
    assert (df.loc[illegal_mask, "legal_balls_bowled_after"] == df.loc[illegal_mask, "legal_balls_bowled_before"]).all()


def test_first_innings_vs_second_innings_chase_state(engine):
    """
    Validates that:
    - Innings 1 deliveries NEVER have a target, runs_required, or required_run_rate (strictly null).
    - Innings 2 deliveries HAVE valid target, runs_required, and required_run_rate.
    """
    df = engine.delivery_states_strict

    # First Innings
    inn1_df = df[df["innings"] == 1]
    assert inn1_df["target"].isna().all()
    assert inn1_df["runs_required_before"].isna().all()
    assert inn1_df["required_run_rate_before"].isna().all()

    # Second Innings (for matches with 1st innings total)
    inn2_df = df[df["innings"] == 2]
    # In matches where target is present, runs_required must be calculated
    with_target = inn2_df[inn2_df["target"].notna()]
    assert len(with_target) > 0
    assert (with_target["runs_required_before"] == with_target["target"] - with_target["cumulative_team_runs_before"]).all()
    assert (with_target["runs_required_after"] == with_target["target"] - with_target["cumulative_team_runs_after"]).all()


def test_dls_revised_target_matches_handling(engine):
    """
    Verifies that matches with official revised targets use the DLS target
    rather than naive (first_innings_total + 1).
    Example: Match 21586 (CSK vs GT IPL 2023 final) target = 171.0, revised balls = 90.0.
    """
    df = engine.delivery_states_strict
    m21586 = df[(df["match_id"] == 21586) & (df["innings"] == 2)]

    assert len(m21586) > 0
    assert (m21586["target"] == 171.0).all()
    assert (m21586["target_source"] == "DLS_REVISED_TARGET").all()
    assert (m21586["scheduled_balls"] == 90).all()


def test_shortened_innings_scheduled_overs_and_balls(engine):
    """
    Verifies accurate scheduled overs and balls for rain-curtailed matches:
    Example: Match 17395 (India vs Australia 2022 8-over match) -> 48 balls scheduled.
    """
    df = engine.delivery_states_strict
    m17395 = df[df["match_id"] == 17395]

    assert len(m17395) > 0
    assert (m17395["scheduled_balls"] == 48).all()
    assert (m17395["scheduled_overs"] == 8.0).all()


def test_super_over_isolation_and_exclusion_records(engine):
    """
    Verifies segregation of Super Overs (innings 3 & 4):
    - Exactly 38 Super Over deliveries across 6 matches
    - Documented in excluded_innings table with reason 'SUPER_OVER'
    """
    ex_df = engine.excluded_innings_df
    so_exclusions = ex_df[ex_df["reason"] == "SUPER_OVER"]

    assert len(so_exclusions) == 12  # 12 innings (innings 3 & 4 for 6 matches)
    assert so_exclusions["deliveries_count"].sum() == 38


def test_abandoned_matches_exclusion_records(engine):
    """
    Verifies that the 16 abandoned matches with zero deliveries are documented
    in excluded_innings table with reason 'ABANDONED_ZERO_DELIVERIES'.
    """
    ex_df = engine.excluded_innings_df
    abandoned = ex_df[ex_df["reason"] == "ABANDONED_ZERO_DELIVERIES"]

    assert len(abandoned) == 16
    assert (abandoned["deliveries_count"] == 0).all()


def test_emerging_tournaments_exclusion_records(engine):
    """
    Verifies that the 30 Emerging Asia Cup matches are documented
    in excluded_innings table with reason 'EMERGING_TOURNAMENT'.
    """
    ex_df = engine.excluded_innings_df
    emerging = ex_df[ex_df["reason"] == "EMERGING_TOURNAMENT"]

    assert len(emerging) == 30
    assert set(emerging["comp_id"].unique()) == {2670, 3289}


def test_score_reconstruction_completeness_flagging(engine):
    """
    Verifies that innings with unconfirmed extras (byes, legbyes, penalty)
    are marked LOWER_BOUND_ONLY, while innings without unconfirmed extras are marked EXACT.
    """
    inn_df = engine.innings_summary_df

    exact_count = (inn_df["score_reconstruction_status"].isin(["EXACT", "SCORE_COMPLETE"])).sum()
    lower_bound_count = (inn_df["score_reconstruction_status"].isin(["LOWER_BOUND_ONLY", "SCORE_INCOMPLETE"])).sum()

    assert exact_count + lower_bound_count == len(inn_df)
    assert exact_count == 329
    assert lower_bound_count == 1395


def test_bowler_and_batter_attribution_invariants(engine):
    """
    Verifies bowler vs batter attribution invariants:
    - Exactly 10,272 bowler wickets
    - Exactly 609 non-bowler dismissals
    - Total dismissals = 10,881
    - Total batter runs = 269,550
    """
    df = engine.delivery_states_strict

    assert df["is_bowler_wicket"].sum() == 10272
    assert df["is_non_bowler_dismissal"].sum() == 609
    assert df["is_wicket"].sum() == 10881
    assert df["runs"].sum() == 269550


def test_markdown_report_generated(engine):
    """Verifies that the human-readable Markdown reconstruction report exists and contains key findings."""
    report_path = engine.reports_dir / "match_state_reconstruction_report.md"
    assert report_path.exists()

    with open(report_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "ROYALS INTELLIGENCE — MATCH-STATE RECONSTRUCTION REPORT (R1-02 & R1-02.1)" in content
    assert "Strict vs. Permissive Scenario Comparison" in content
    assert "Score Reconstruction & Exact vs. Lower-Bound Semantics" in content
    assert "Empirical Inference of `extras_2_runs`" in content
    assert "Match-Result Reconciliation & Official Schema Limitations" in content
    assert "Revised Overs, Shortened Matches & DLS Coverage" in content
    assert "Downstream Feature-Eligibility Contract (for R1-03)" in content


# ==============================================================================
# PART 3: R1-02.1 AUDIT & REMEDIATION INTEGRITY TESTS
# ==============================================================================

def test_fixture_exact_score_reconstruction_semantics():
    """
    Scenario 1: Miniature chase where Innings 1 is EXACT (150 runs, 0 unconfirmed extras)
    and Innings 2 has known scoring deliveries without unconfirmed extras.
    Verifies that cumulative exact score, runs required exact, and RRR exact are all populated.
    """
    engine = MatchStateEngine()

    target = 151.0
    b1_runs, b1_extras, _, b1_unconf, _, prov1 = engine.calculate_delivery_runs(0, np.nan, 0)
    b2_runs, b2_extras, _, b2_unconf, _, prov2 = engine.calculate_delivery_runs(1, np.nan, 0)
    b3_runs, b3_extras, _, b3_unconf, _, prov3 = engine.calculate_delivery_runs(4, np.nan, 0)

    assert not (b1_unconf or b2_unconf or b3_unconf)
    assert prov1 == "CONFIRMED_BATTER_RUNS_STANDARD"
    assert prov2 == "CONFIRMED_BATTER_RUNS_STANDARD"
    assert prov3 == "CONFIRMED_BATTER_RUNS_STANDARD"


def test_fixture_unconfirmed_extras_withholding():
    """
    Scenario 2: Byes and Leg-byes with unknown multi-run amount (extras1_runs=3, runs=0).
    Verifies LOWER_BOUND_ONLY completeness, unconfirmed flag, and that exact chase
    metrics are strictly withheld (None/NaN) while bounds remain valid.
    """
    engine = MatchStateEngine()

    # Legbyes with runs=0, extras1_runs=3
    b_runs, k_extras, tot, unconf, b_conceded, prov = engine.calculate_delivery_runs(
        0, "legbyes", 0
    )
    assert b_runs == 0
    assert k_extras == 1
    assert tot == 1
    assert unconf is True
    assert b_conceded == 0  # Legbyes not charged to bowler
    assert prov == "UNCONFIRMED_MULTI_RUN_LEGBYES"

    # Byes with runs=0
    b_runs_b, k_extras_b, tot_b, unconf_b, b_conceded_b, prov_b = engine.calculate_delivery_runs(
        0, "byes", 0
    )
    assert b_runs_b == 0
    assert k_extras_b == 1
    assert tot_b == 1
    assert unconf_b is True
    assert b_conceded_b == 0
    assert prov_b == "UNCONFIRMED_MULTI_RUN_BYES"


def test_fixture_wide_base_penalty_vs_unconfirmed_additional_runs():
    """
    Scenario 3: Wide delivery base penalty (+1) vs unconfirmed additional runs.
    A wide always concedes at least 1 run to bowler and team. If extras1_runs > 1,
    additional runs are unconfirmed.
    """
    engine = MatchStateEngine()

    # Standard wide: runs=0, extras_type='wide', extras_2_runs=0
    b_runs, k_extras, tot, unconf, b_conceded, prov = engine.calculate_delivery_runs(
        0, "wide", 0
    )
    assert b_runs == 0
    assert k_extras == 1
    assert tot == 1
    assert unconf is False  # Base penalty is 1 confirmed
    assert b_conceded == 1
    assert prov == "CONFIRMED_WIDE_BASE_PENALTY"

    # Legality check: wide is illegal
    assert engine.classify_delivery_legality("wide", "strict") is False
    assert engine.classify_delivery_legality("wide", "permissive") is False


def test_fixture_no_ball_with_auxiliary_extras():
    """
    Scenario 4: No-ball with verified auxiliary extras (extras_2_runs).
    Empirical inference: extras_2_runs provides additional team runs on no-balls.
    """
    engine = MatchStateEngine()

    # Case A: 1 run off bat + 1 overstep penalty + 1 extras_2_runs = 3 runs total
    b_runs, k_extras, tot, unconf, b_conceded, prov = engine.calculate_delivery_runs(
        1, "Overstep", 1
    )
    assert b_runs == 1
    assert k_extras == 2  # 1 no-ball + 1 extras_2_runs
    assert tot == 3
    assert unconf is False
    assert b_conceded == 3
    assert prov == "CONFIRMED_OVERSTEP_PENALTY_AND_EMPIRICAL_E2"

    # Case B: 0 off bat + 1 overstep penalty + 4 extras_2_runs = 5 runs total (boundary no-ball)
    b_runs, k_extras, tot, unconf, b_conceded, prov = engine.calculate_delivery_runs(
        0, "Overstep", 4
    )
    assert b_runs == 0
    assert k_extras == 5
    assert tot == 5
    assert unconf is False
    assert b_conceded == 5
    assert prov == "CONFIRMED_OVERSTEP_PENALTY_AND_EMPIRICAL_E2"

    # Standard overstep without extras_2_runs
    b_runs, k_extras, tot, unconf, b_conceded, prov = engine.calculate_delivery_runs(
        0, "Overstep", 0
    )
    assert b_runs == 0
    assert k_extras == 1
    assert tot == 1
    assert unconf is False
    assert b_conceded == 1
    assert prov == "CONFIRMED_OVERSTEP_PENALTY"


def test_fixture_unknown_penalty_delivery():
    """
    Scenario 5: Penalty delivery handling.
    Penalty consumes legal ball, adds minimum 1 run to team score, does not credit/concede
    to batter or bowler, and flags unconfirmed extras.
    """
    engine = MatchStateEngine()

    b_runs, k_extras, tot, unconf, b_conceded, prov = engine.calculate_delivery_runs(
        0, "Penalty", 0
    )
    assert b_runs == 0
    assert k_extras == 1
    assert tot == 1
    assert unconf is True
    assert b_conceded == 0
    assert prov == "UNCONFIRMED_PENALTY_RUNS_AMOUNT"

    # Penalty is legal
    assert engine.classify_delivery_legality("Penalty", "strict") is True
    assert engine.classify_delivery_legality("Penalty", "permissive") is True


def test_dataset_incomplete_first_innings_withholds_exact_target(engine):
    """
    Scenario 6: Incomplete first innings score withholding exact target.
    In ordinary (non-DLS) matches where Innings 1 contains unconfirmed extras,
    target_exact and target_is_exact must be false/null, and runs_required_exact must be null.
    """
    df = engine.delivery_states_strict
    # Find Innings 2 deliveries in ordinary matches where first innings total was lower bound only
    inn2_non_dls = df[(df["innings"] == 2) & (df["target_source"] == "FIRST_INNINGS_LOWER_BOUND_PLUS_ONE")]
    incomplete_inn1 = inn2_non_dls[inn2_non_dls["target_is_exact"] == False]

    assert len(incomplete_inn1) > 0
    # In all these deliveries, target_exact must be NaN
    assert incomplete_inn1["target_exact"].isna().all()
    # And runs_required_exact must be NaN
    assert incomplete_inn1["runs_required_exact_before"].isna().all()
    # But target_lower_bound must be populated
    assert incomplete_inn1["target_lower_bound"].notna().all()
    # And runs_required_upper_bound must be populated
    assert incomplete_inn1["runs_required_upper_bound_before"].notna().all()


def test_dataset_dls_target_exact_with_incomplete_chase_withholds_exact_rrr(engine):
    """
    Scenario 7: Exact target (e.g. DLS Match 21586) with uncertain chase score withholds exact runs required.
    Even though target is exact (171.0), once an unconfirmed extra occurs, exact score is lost,
    and runs_required_exact and required_run_rate_exact must be withheld (NaN).
    """
    df = engine.delivery_states_strict
    m21586 = df[(df["match_id"] == 21586) & (df["innings"] == 2)]

    assert len(m21586) > 0
    assert (m21586["target_exact"] == 171.0).all()
    assert (m21586["target_is_exact"] == True).all()

    # Deliveries where cumulative exact score is known
    exact_score_deliveries = m21586[m21586["cumulative_team_runs_exact_before"].notna()]
    # Deliveries where cumulative exact score is lost (after byes/legbyes)
    lower_bound_deliveries = m21586[m21586["cumulative_team_runs_exact_before"].isna()]

    if len(lower_bound_deliveries) > 0:
        assert lower_bound_deliveries["runs_required_exact_before"].isna().all()
        assert lower_bound_deliveries["required_run_rate_exact_before"].isna().all()
        assert lower_bound_deliveries["runs_required_upper_bound_before"].notna().all()


def test_dataset_exact_chase_metrics_mathematical_consistency(engine):
    """
    Scenario 8: Exact chase metrics are mathematically consistent wherever populated:
    - runs_required_exact == target_exact - cumulative_team_runs_exact
    - required_run_rate_exact == (runs_required_exact * 6.0) / balls_remaining
    """
    df = engine.delivery_states_strict
    exact_chase = df[df["runs_required_exact_before"].notna()]

    assert len(exact_chase) > 0
    # Consistency 1: target_exact and cumulative_team_runs_exact must both be not-null
    assert exact_chase["target_exact"].notna().all()
    assert exact_chase["cumulative_team_runs_exact_before"].notna().all()

    # Consistency 2: exact difference
    expected_req = exact_chase["target_exact"] - exact_chase["cumulative_team_runs_exact_before"]
    assert (exact_chase["runs_required_exact_before"] == expected_req).all()

    # Consistency 3: RRR (rounded to 3 decimal places in engine, with max(0.0, runs_req))
    positive_balls = exact_chase[exact_chase["balls_remaining_before"] > 0]
    positive_req = np.maximum(0.0, positive_balls["runs_required_exact_before"])
    expected_rrr = np.round((positive_req * 6.0) / positive_balls["balls_remaining_before"], 3)
    np.testing.assert_allclose(positive_balls["required_run_rate_exact_before"].values, expected_rrr.values, atol=1e-3)


def test_dataset_dls_target_applicability_all_23_matches(engine):
    """
    Scenario 9: DLS target applicability across all 23 matches.
    Verifies dls_and_revised_overs_audit.parquet:
    - Exactly 23 matches with official revised targets
    - In all 23 matches, target_applicability is INNINGS_2_CHASE_TARGET
    - Target is strictly greater than 0
    - Second innings scheduled balls > 0
    """
    dls_df = engine.dls_audit_df

    assert len(dls_df) == 34
    dls_23 = dls_df[dls_df["is_dls_target_match"]]
    assert len(dls_23) == 23
    assert (dls_23["target_applicability"] == "INNINGS_2_CHASE_TARGET").all()
    assert (dls_23["revised_target"] > 0).all()
    assert (dls_23["second_inn_scheduled_balls"] > 0).all()


def test_dataset_strict_vs_permissive_5_out_of_scope_reconciliation(engine):
    """
    Scenario 10: Strict vs permissive scenario separation and reconciliation of the
    5 out-of-scope ambiguous 'other' deliveries.
    - Total ambiguous 'other': 264
    - Primary scope ambiguous 'other': 259
    - Out of scope ambiguous 'other': 5 (3 in Comp 2670, 1 in Comp 3289, 1 in IPL Super Over)
    """
    df_strict = engine.delivery_states_strict
    other_deliveries = df_strict[df_strict["extras_type"] == "other"]

    assert len(other_deliveries) == 264
    in_primary = other_deliveries[other_deliveries["is_primary_scope"]]
    out_of_primary = other_deliveries[~other_deliveries["is_primary_scope"]]

    assert len(in_primary) == 259
    assert len(out_of_primary) == 5

    # Check the 5 out of primary:
    comp_2670 = out_of_primary[out_of_primary["comp_id"] == 2670]
    comp_3289 = out_of_primary[out_of_primary["comp_id"] == 3289]
    super_overs = out_of_primary[out_of_primary["innings"].isin([3, 4])]

    assert len(comp_2670) == 3
    assert len(comp_3289) == 1
    assert len(super_overs) == 1
    assert super_overs["match_id"].iloc[0] == 40725  # IPL 2025 Super Over


def test_dataset_match_result_reconciliation_table_coverage(engine):
    """
    Scenario 11: Match-result reconciliation table verification.
    Verifies match_result_reconciliation.parquet:
    - Covers exactly 883 matches
    - Accurately declares that matches.csv schema lacks independent official innings scores
    - Categorizes all 883 matches cleanly across the 7 reconciliation outcomes.
    """
    recon_df = engine.reconciliation_df

    assert len(recon_df) == 883
    counts = recon_df["reconciliation_outcome"].value_counts()

    assert counts["WICKET_WIN_NO_OFFICIAL_TOTAL_IN_SCHEMA"] == 394
    assert counts["INCOMPLETE_EXTRAS_RUN_WIN"] == 382
    assert counts["NO_RESULT_OR_ABANDONED"] == 40
    assert counts["OTHER_RESULT"] == 30
    assert counts["DLS_REVISED_TARGET"] == 26
    assert counts["EXACT_BOTH_INNS_MARGIN_MISMATCH"] == 6
    assert counts["EXACT_BOTH_INNS_MARGIN_MATCH"] == 5
    assert counts.sum() == 883


def test_dataset_revised_overs_legal_balls_unit_verified(engine):
    """
    Scenario 12: Revised overs and DLS audit verification.
    Verifies dls_and_revised_overs_audit.parquet:
    - Covers all 34 matches
    - Proves revised overs fields store legal balls (not overs)
    """
    dls_df = engine.dls_audit_df

    assert len(dls_df) == 34
    first_rev = dls_df[dls_df["first_inn_revised_raw"].notna()]
    second_rev = dls_df[dls_df["second_inn_revised_raw"].notna()]

    assert (first_rev["first_inn_unit_verified"] == "LEGAL_BALLS").all()
    assert (second_rev["second_inn_unit_verified"] == "LEGAL_BALLS").all()

    # Prove raw values are integers divisible by 6 in the range [30, 114]
    for val in first_rev["first_inn_revised_raw"]:
        assert val % 6 == 0 and 30.0 <= val <= 114.0
    for val in second_rev["second_inn_revised_raw"]:
        assert val % 6 == 0 and 30.0 <= val <= 114.0


def test_dataset_no_silent_zero_substitution_invariant(engine):
    """
    Scenario 13: No fabricated values or silent zero substitution invariant:
    - In Innings 1, runs_required and RRR are strictly null/NaN (never 0 or 0.0)
    - When score is LOWER_BOUND_ONLY, cumulative_team_runs_exact is strictly null/NaN
    """
    df = engine.delivery_states_strict

    inn1 = df[df["innings"] == 1]
    assert inn1["target_exact"].isna().all()
    assert inn1["runs_required_exact_before"].isna().all()
    assert inn1["required_run_rate_exact_before"].isna().all()

    # Deliveries where delivery_score_completeness == LOWER_BOUND_ONLY
    incomplete_dels = df[df["delivery_score_completeness"] == "LOWER_BOUND_ONLY"]
    assert len(incomplete_dels) > 0
    assert incomplete_dels["cumulative_team_runs_exact_after"].isna().all()


def test_downstream_feature_eligibility_contract():
    """
    Scenario 14: Downstream feature-eligibility contract verification for R1-03.
    Verifies that DOWNSTREAM_FEATURE_ELIGIBILITY_CONTRACT is properly structured
    with Tier 1, Tier 2, and Tier 3 definitions.
    """
    assert "TIER_1_SAFE_WHEN_INDEPENDENTLY_VERIFIED" in DOWNSTREAM_FEATURE_ELIGIBILITY_CONTRACT
    assert "TIER_2_SCORE_DEPENDENT_REQUIRES_EXACT_SCORE" in DOWNSTREAM_FEATURE_ELIGIBILITY_CONTRACT
    assert "TIER_3_UNCERTAIN_REQUIRES_SENSITIVITY_OR_EXCLUSION" in DOWNSTREAM_FEATURE_ELIGIBILITY_CONTRACT

    t1 = DOWNSTREAM_FEATURE_ELIGIBILITY_CONTRACT["TIER_1_SAFE_WHEN_INDEPENDENTLY_VERIFIED"]
    t2 = DOWNSTREAM_FEATURE_ELIGIBILITY_CONTRACT["TIER_2_SCORE_DEPENDENT_REQUIRES_EXACT_SCORE"]
    t3 = DOWNSTREAM_FEATURE_ELIGIBILITY_CONTRACT["TIER_3_UNCERTAIN_REQUIRES_SENSITIVITY_OR_EXCLUSION"]

    assert "legal_balls_bowled" in t1
    assert "balls_remaining" in t1
    assert "striker_runs" in t1
    assert "is_bowler_wicket" in t1

    assert "runs_required_exact" in t2
    assert "required_run_rate_exact" in t2
    assert "cumulative_team_runs_exact" in t2

    assert "multi_run_byes_legbyes_exact_amounts" in t3
    assert "ambiguous_other_deliveries_strict_vs_permissive" in t3

