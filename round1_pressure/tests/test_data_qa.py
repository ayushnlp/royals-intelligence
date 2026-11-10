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
    """Verifies that non-bowler dismissals (run outs, retire out, obstructing) are separated from bowler wickets."""
    b_audit = qa_engine.qa_results["cricket_traps"]["bowling_attribution"]
    assert b_audit["total_wickets_flagged"] == 10881
    assert b_audit["bowler_credited_wickets"] == 10272
    assert b_audit["non_bowler_dismissals"] == 609
    assert b_audit["bowler_credited_wickets"] + b_audit["non_bowler_dismissals"] == 10881

    # Verify specific counts
    dt_counts = b_audit["dismissal_type_counts"]
    assert dt_counts["Caught"] == 7557
    assert dt_counts["Bowled"] == 1775
    assert dt_counts["LBW"] == 709
    assert dt_counts["RunOut"] == 600
    assert dt_counts["Stump"] == 214
    assert dt_counts["Hit Wicket"] == 17
    assert dt_counts["Retire Out"] == 6


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
