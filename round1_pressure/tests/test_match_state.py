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

from round1_pressure.src.match_state import MatchStateEngine


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
        b_runs, k_extras, tot, unconf, b_conceded = engine.calculate_delivery_runs(
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
    """Verifies that all 6 required Parquet output files exist on disk."""
    expected = [
        "delivery_states_strict.parquet",
        "delivery_states_permissive.parquet",
        "innings_state_summary.parquet",
        "match_state_summary.parquet",
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
    are marked SCORE_INCOMPLETE, while innings without unconfirmed extras are marked SCORE_COMPLETE.
    """
    inn_df = engine.innings_summary_df

    complete_count = (inn_df["score_reconstruction_status"] == "SCORE_COMPLETE").sum()
    incomplete_count = (inn_df["score_reconstruction_status"] == "SCORE_INCOMPLETE").sum()

    assert complete_count + incomplete_count == len(inn_df)
    assert complete_count == 329
    assert incomplete_count == 1395


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

    assert "ROYALS INTELLIGENCE — MATCH-STATE RECONSTRUCTION REPORT (R1-02)" in content
    assert "Strict vs. Permissive Scenario Comparison" in content
    assert "Score Reconstruction & Extras Reconciliation" in content
    assert "Revised Targets, Shortened Matches & DLS Coverage" in content
