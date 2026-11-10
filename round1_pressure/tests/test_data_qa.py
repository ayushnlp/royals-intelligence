"""
Royals Intelligence - Round 1 Data QA Test Suite
Validates dataset loading, missing-file handling, schema verification, duplicate checks,
player ID integrity, competition classification, Super Over isolation, extras code traps,
match-to-ball-by-ball relationships, and deterministic output generation.
"""

import os
import json
import tempfile
import pytest
import pandas as pd
from pathlib import Path

from round1_pressure.src.load_qa import DatasetQAEngine


@pytest.fixture(scope="module")
def qa_engine():
    """Initializes and runs the full QA engine once for the test module."""
    engine = DatasetQAEngine()
    engine.run_full_qa()
    return engine


def test_file_loading_all_expected_files_present(qa_engine):
    """Verifies all 6 required CSV files are present and loaded with non-zero rows."""
    expected = [
        "ball_by_ball",
        "matches",
        "competitions",
        "teams",
        "playing_eleven",
        "competition_team_player_mapping",
    ]
    for key in expected:
        assert key in qa_engine.datasets, f"Missing dataset: {key}"
        df = qa_engine.datasets[key]
        assert len(df) > 0, f"Dataset {key} is unexpectedly empty"

    assert len(qa_engine.datasets["ball_by_ball"]) == 200999
    assert len(qa_engine.datasets["matches"]) == 883
    assert len(qa_engine.datasets["competitions"]) == 141
    assert len(qa_engine.datasets["teams"]) == 353
    assert len(qa_engine.datasets["playing_eleven"]) == 28381
    assert len(qa_engine.datasets["competition_team_player_mapping"]) == 6413


def test_missing_file_handling():
    """Verifies graceful and clear FileNotFoundError when a dataset file or directory is missing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        engine = DatasetQAEngine(data_dir=tmpdir)
        with pytest.raises(FileNotFoundError) as exc_info:
            engine.load_datasets()
        assert "Required dataset file missing" in str(exc_info.value)

    engine_nonexistent = DatasetQAEngine(data_dir="/non/existent/path/at/all")
    with pytest.raises(FileNotFoundError):
        engine_nonexistent.load_datasets()


def test_schema_validation(qa_engine):
    """Verifies that all required columns are present in each dataset."""
    profiles = qa_engine.qa_results["profiles"]

    # Verify ball_by_ball columns
    bbb_cols = set(profiles["ball_by_ball"]["columns"])
    critical_bbb_cols = {
        "match_id", "innings", "overid", "over_ball_num", "runs",
        "is_wicket", "dismissal_type", "extras_type", "extras1_runs",
        "extras_2_runs", "striker_id", "bowler_id", "bowl_speed"
    }
    assert critical_bbb_cols.issubset(bbb_cols), f"Missing critical BBB columns: {critical_bbb_cols - bbb_cols}"

    # Verify matches columns
    matches_cols = set(profiles["matches"]["columns"])
    critical_matches_cols = {
        "match_id", "comp_id", "match_date", "home_team", "away_team",
        "result", "revised_target", "first_inn_revised_overs", "second_inn_revised_overs"
    }
    assert critical_matches_cols.issubset(matches_cols)


def test_duplicate_detection(qa_engine):
    """Verifies duplicate row detection across all datasets."""
    profiles = qa_engine.qa_results["profiles"]
    for key, p in profiles.items():
        assert "exact_duplicate_rows" in p
        # None of the core primary files should have wholesale duplicate rows
        assert p["exact_duplicate_rows"] == 0, f"Unexpected duplicate rows found in {key}"


def test_player_id_integrity_no_merge_on_display_name(qa_engine):
    """
    CRITICAL: Validates that player_id is the sole canonical key and that names are NOT unique.
    Asserts detection of individuals sharing the same name (e.g. Abdul Samad, Rashid Khan).
    """
    p_audit = qa_engine.qa_results["cricket_traps"]["player_identity_audit"]
    assert p_audit["names_with_multiple_player_ids_count"] == 7

    multi_names = p_audit["names_with_multiple_player_ids"]
    assert "Abdul Samad" in multi_names
    assert "Rashid Khan" in multi_names
    assert len(multi_names["Abdul Samad"]) == 2  # ID 7446 (India/SRH) vs 6922 (Pakistan)
    assert len(multi_names["Rashid Khan"]) == 2  # ID 4722 (Afghanistan/GT) vs 20172 (UAE)

    # Asserts that player_ids never map to multiple names
    assert p_audit["ids_with_multiple_names_count"] == 0


def test_competition_classification_ipl_t20i_emerging(qa_engine):
    """Verifies accurate classification of IPL, Senior T20I, and Emerging/A-team competitions."""
    c_audit = qa_engine.qa_results["cricket_traps"]["competitions_classification"]
    assert c_audit["ipl_matches"] == 371
    assert c_audit["t20i_matches"] == 482
    assert c_audit["emerging_matches"] == 30
    assert c_audit["ipl_matches"] + c_audit["t20i_matches"] + c_audit["emerging_matches"] == 883


def test_super_over_identification(qa_engine):
    """Verifies segregation of Super Overs (innings 3 & 4) from ordinary innings (1 & 2)."""
    so_audit = qa_engine.qa_results["cricket_traps"]["innings_and_super_overs"]
    assert so_audit["super_over_deliveries_total"] == 38
    assert so_audit["super_over_matches_count"] == 6
    assert set(so_audit["super_over_match_ids"]) == {34429, 40725, 45512, 48027, 48029, 50359}
    assert int(so_audit["deliveries_per_innings"]["1"]) == 105727
    assert int(so_audit["deliveries_per_innings"]["2"]) == 95234


def test_ambiguous_extras_and_code_trap(qa_engine):
    """
    CRITICAL: Validates that extras1_runs is a categorical code (1-7), NOT run values.
    Asserts that wide and legbye rows have runs=0 (batter runs off bat).
    """
    e_audit = qa_engine.qa_results["cricket_traps"]["extras_trap"]
    assert e_audit["is_extras1_runs_categorical_code"] is True

    # 6 maps to NONE extras
    assert e_audit["extras1_runs_crosstab"]["NONE"]["6"] == 189167
    # 2 maps to wide
    assert e_audit["extras1_runs_crosstab"]["wide"]["2"] == 7714
    # 3 maps to legbyes
    assert e_audit["extras1_runs_crosstab"]["legbyes"]["3"] == 2748
    # 1 maps to Overstep
    assert e_audit["extras1_runs_crosstab"]["Overstep"]["1"] == 576

    # Verify runs on wides is 100% zero
    assert e_audit["runs_on_wides"] == {"0": 7714}


def test_missing_match_to_ball_by_ball_relationships(qa_engine):
    """Verifies identification of exactly 16 matches without ball-by-ball deliveries (100% abandoned)."""
    ref_m = qa_engine.qa_results["referential_integrity"]["matches_to_ball_by_ball"]
    assert ref_m["matches_without_deliveries_count"] == 16
    assert ref_m["total_matches"] == 883
    assert ref_m["matches_with_deliveries"] == 867

    # Assert that all 16 matches without deliveries had result 'Match Abandoned'
    results_map = ref_m["matches_without_deliveries_results"]
    assert results_map == {"Match Abandoned": 16}


def test_bowling_attribution_dismissal_credit(qa_engine):
    """
    Verifies that non-bowler dismissals (run outs, retire out, obstructing) are separated from bowler wickets,
    and validates spelling normalization ('Obstracting the field' -> 'Obstructing the field').
    """
    b_audit = qa_engine.qa_results["cricket_traps"]["bowling_attribution"]
    assert b_audit["total_wickets_flagged"] == 10881
    assert b_audit["bowler_credited_wickets"] == 10272
    assert b_audit["non_bowler_dismissals"] == 609
    assert b_audit["bowler_credited_wickets"] + b_audit["non_bowler_dismissals"] == 10881

    # Verify raw counts
    raw_counts = b_audit["raw_dismissal_counts"]
    assert raw_counts["Caught"] == 7557
    assert raw_counts["Bowled"] == 1775
    assert raw_counts["LBW"] == 709
    assert raw_counts["RunOut"] == 600
    assert raw_counts["Stump"] == 214
    assert raw_counts["Hit Wicket"] == 17
    assert raw_counts["Retire Out"] == 6
    assert raw_counts["Obstracting the field"] == 2
    assert raw_counts["Obstructing the field"] == 1

    # Verify normalized counts
    norm_counts = b_audit["normalized_dismissal_counts"]
    assert norm_counts["Obstructing the field"] == 3
    assert "Obstracting the field" not in norm_counts

    # Unknown dismissals guard
    assert b_audit["unknown_dismissals_treated_as_bowler_credit"] is False


def test_delivery_legality_evidence_based_counts(qa_engine):
    """
    CRITICAL (R1-01.1): Validates evidence-based delivery legality classification.
    Confirmed Legal: Standard (189,167) + legbyes (2,748) + byes (529) + Penalty (1) = 192,445.
    Confirmed Illegal: wide (7,714) + Overstep (576) = 8,290.
    Ambiguous / Unresolved: other (264).
    Dual metrics: Strict Legal (192,445) vs Permissive Legal (192,709).
    """
    leg_audit = qa_engine.qa_results["cricket_traps"]["delivery_legality_and_sequence_audit"]
    assert leg_audit["total_deliveries"] == 200999
    assert leg_audit["confirmed_legal_deliveries"] == 192445
    assert leg_audit["confirmed_illegal_deliveries"] == 8290
    assert leg_audit["ambiguous_deliveries"] == 264
    assert leg_audit["strict_legal_deliveries_count"] == 192445
    assert leg_audit["permissive_legal_deliveries_count"] == 192709
    assert leg_audit["unresolved_deliveries_count"] == 264


def test_penalty_delivery_investigation(qa_engine):
    """
    Validates that the single Penalty extras delivery (Match 16753, Inn 2, Over 6, Ball 4)
    occurred in an over with exactly 6 balls bowled, consuming a legal ball without re-bowl.
    """
    leg_audit = qa_engine.qa_results["cricket_traps"]["delivery_legality_and_sequence_audit"]
    cats = leg_audit["category_breakdown"]
    assert cats["Penalty"]["count"] == 1
    assert cats["Penalty"]["legal"] == 1
    assert cats["Penalty"]["illegal"] == 0
    assert cats["Penalty"]["ambiguous"] == 0
    assert leg_audit["sequence_evidence"]["penalty_delivery_over_total_balls"] == 6


def test_other_deliveries_sequence_and_style_investigation(qa_engine):
    """
    Validates sequence and domain investigation of the 264 'other' extras deliveries:
    - 253 occurred in completed overs that required 7+ balls (re-bowled).
    - 11 occurred in early-terminated final overs (10 target chased mid-over, 1 Super Over).
    - Delivery styles: 116 beamers, 72 high full tosses, 16 bouncers.
    - Zero bowled, caught, or LBW dismissals.
    - Explicitly retained as ambiguous/unresolved rather than forcing a single classification.
    """
    leg_audit = qa_engine.qa_results["cricket_traps"]["delivery_legality_and_sequence_audit"]
    cats = leg_audit["category_breakdown"]
    assert cats["other"]["count"] == 264
    assert cats["other"]["ambiguous"] == 264
    assert cats["other"]["legal"] == 0
    assert cats["other"]["illegal"] == 0

    seq = leg_audit["sequence_evidence"]
    assert seq["other_in_completed_overs_with_6_legal_balls"] == 253
    assert seq["other_in_uncompleted_final_overs"] == 11
    styles = seq["delivery_style_distribution_on_other"]
    assert styles["Beamer"] == 116
    assert styles["Full Toss"] == 72
    assert styles["Bouncer"] == 16


def test_unknown_dismissal_guard():
    """Verifies that unlisted / unknown dismissal types are safely rejected from bowler wicket credit."""
    engine = DatasetQAEngine()
    unknown_types = ["Timed Out", "Handled Ball", "Unknown", "custom_dismissal"]
    for ut in unknown_types:
        norm = engine.DISMISSAL_SPELLING_CORRECTIONS.get(ut, ut)
        assert norm not in engine.BOWLER_CREDITED_DISMISSALS, f"Unknown dismissal '{ut}' must not be credited to bowler"


def test_deterministic_qa_outputs_generated(qa_engine):
    """Verifies that machine-readable JSON and human-readable Markdown outputs exist and are populated."""
    json_path = qa_engine.outputs_dir / "qa_summary.json"
    report_path = qa_engine.reports_dir / "data_quality_report.md"

    assert json_path.exists()
    assert report_path.exists()

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert data["overall_status"] == "DATASET_QA_PASSED_WITH_CRITICAL_TRAPS_DOCUMENTED"
    assert len(data["profiles"]) == 6

    with open(report_path, "r", encoding="utf-8") as f:
        md_content = f.read()
    assert "ROYALS INTELLIGENCE — ROUND 1 DATA QUALITY" in md_content
    assert "Trap A: Extras Code Trap" in md_content
    assert "Trap B: Legal Delivery Counting" in md_content
    assert "Evidence-Based Cricket Delivery Classification" in md_content
    assert "Full Delivery Classification Evidence Table" in md_content

