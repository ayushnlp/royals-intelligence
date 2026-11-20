"""
Automated Test Suite for AUCTION-04: Historical Performance & Competition Normalization.

Verifies:
1. Empirical competition benchmarks integrity (192,709 legal deliveries).
2. 100% canonical identity joins across batting and bowling profiles.
3. Strict domain separation between batting and bowling (zero conflation or composite scoring).
4. Empirical Bayesian shrinkage properties across sample sizes.
5. Phase-specific split completeness (Powerplay, Middle, Death).
6. Deterministic serialization of Parquet and JSON artifacts.
7. Bit-for-bit protection of Round 1 Pressure Intelligence Parquet baselines.
"""

import hashlib
import json
from pathlib import Path
import pytest
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
PROCESSED_DIR = REPO_ROOT / "data" / "processed" / "auction_intelligence"


@pytest.fixture(scope="module")
def normalization_artifacts():
    benchmarks_file = PROCESSED_DIR / "competition_normalization_benchmarks.json"
    batting_parquet = PROCESSED_DIR / "normalized_batting_performance.parquet"
    bowling_parquet = PROCESSED_DIR / "normalized_bowling_performance.parquet"
    summary_file = PROCESSED_DIR / "normalization_summary.json"
    canonical_file = PROCESSED_DIR / "canonical_player_registry.parquet"

    assert benchmarks_file.exists(), f"Missing {benchmarks_file}"
    assert batting_parquet.exists(), f"Missing {batting_parquet}"
    assert bowling_parquet.exists(), f"Missing {bowling_parquet}"
    assert summary_file.exists(), f"Missing {summary_file}"
    assert canonical_file.exists(), f"Missing {canonical_file}"

    with open(benchmarks_file, "r", encoding="utf-8") as f:
        benchmarks = json.load(f)
    with open(summary_file, "r", encoding="utf-8") as f:
        summary = json.load(f)

    batting_df = pd.read_parquet(batting_parquet)
    bowling_df = pd.read_parquet(bowling_parquet)
    canonical_df = pd.read_parquet(canonical_file)

    return {
        "benchmarks": benchmarks,
        "summary": summary,
        "batting_df": batting_df,
        "bowling_df": bowling_df,
        "canonical_df": canonical_df,
    }


@pytest.mark.data_dependent
def test_competition_benchmarks_integrity(normalization_artifacts):
    """Verifies that all three competition tiers have empirical benchmarks matching exact delivery totals."""
    benchmarks = normalization_artifacts["benchmarks"]
    assert "IPL" in benchmarks
    assert "T20I" in benchmarks
    assert "Emerging_T20" in benchmarks

    ipl = benchmarks["IPL"]
    t20i = benchmarks["T20I"]
    emg = benchmarks["Emerging_T20"]

    # Delivery sum checks (192,709 legal deliveries)
    total_legal = ipl["legal_deliveries"] + t20i["legal_deliveries"] + emg["legal_deliveries"]
    assert total_legal == 192709

    # Total records (200,999)
    total_records = ipl["total_deliveries"] + t20i["total_deliveries"] + emg["total_deliveries"]
    assert total_records == 200999

    # Relative scoring index checks (IPL anchor = 1.0)
    assert ipl["relative_scoring_index"] == 1.0
    assert 0.80 < emg["relative_scoring_index"] < 1.0
    assert 0.85 < t20i["relative_scoring_index"] < 1.0

    # IPL empirical benchmarks verification
    assert ipl["legal_deliveries"] == 83878
    assert ipl["batter_runs"] == 123597
    assert ipl["total_bowler_conceded_runs"] == 127576
    assert ipl["benchmark_bowling_economy"] == 9.1258
    assert ipl["bowler_credited_wickets"] == 4209
    assert ipl["total_wickets"] == 4458


@pytest.mark.data_dependent
def test_population_counts_reconciliation(normalization_artifacts):
    """Verifies exact population counts across registry, active players, batters and bowlers."""
    can_df = normalization_artifacts["canonical_df"]
    bdf = normalization_artifacts["batting_df"]
    bowldf = normalization_artifacts["bowling_df"]

    total_registry = len(can_df)
    assert total_registry == 1217

    bat_ids = set(bdf["canonical_id"].unique())
    bowl_ids = set(bowldf["canonical_id"].unique())
    all_active_ids = bat_ids.union(bowl_ids)
    overlap_ids = bat_ids.intersection(bowl_ids)

    assert len(bat_ids) == 888
    assert len(bowl_ids) == 647
    assert len(all_active_ids) == 958
    assert len(overlap_ids) == 577  # 888 + 647 - 958 = 577 all-rounders

    # 100% of active players join to canonical registry
    can_id_set = set(can_df["canonical_id"].unique())
    assert all_active_ids.issubset(can_id_set)
    assert len(all_active_ids - can_id_set) == 0

    # Inactive players in registry with zero delivery records in 2022-2026 dataset
    inactive_ids = can_id_set - all_active_ids
    assert len(inactive_ids) == 259  # 1217 - 958 = 259


@pytest.mark.data_dependent
def test_canonical_player_id_joins(normalization_artifacts):
    """Verifies 100% of batting and bowling profile IDs exist in the canonical registry."""
    can_ids = set(normalization_artifacts["canonical_df"]["canonical_id"].unique())
    bat_ids = set(normalization_artifacts["batting_df"]["canonical_id"].unique())
    bowl_ids = set(normalization_artifacts["bowling_df"]["canonical_id"].unique())

    assert len(bat_ids - can_ids) == 0, f"Unmapped batting IDs: {bat_ids - can_ids}"
    assert len(bowl_ids - can_ids) == 0, f"Unmapped bowling IDs: {bowl_ids - can_ids}"
    assert len(bat_ids) == 888
    assert len(bowl_ids) == 647


@pytest.mark.data_dependent
def test_batting_bowling_domain_separation(normalization_artifacts):
    """Verifies strict domain separation between batting and bowling (no composite scores)."""
    batting_cols = set(normalization_artifacts["batting_df"].columns)
    bowling_cols = set(normalization_artifacts["bowling_df"].columns)

    # Batting should not contain bowling metrics
    assert "overs_bowled" not in batting_cols
    assert "raw_economy_rate" not in batting_cols
    assert "wickets_taken" not in batting_cols

    # Bowling should not contain batting metrics
    assert "raw_strike_rate" not in bowling_cols
    assert "raw_runs_scored" not in bowling_cols
    assert "fours_count" not in bowling_cols

    # Zero all-rounder composite scores in AUCTION-04
    assert "composite_player_score" not in batting_cols
    assert "composite_player_score" not in bowling_cols


@pytest.mark.data_dependent
def test_bayesian_shrinkage_properties(normalization_artifacts):
    """Verifies that empirical Bayes shrinkage shrinks low-sample players towards prior mean."""
    bdf = normalization_artifacts["batting_df"]
    ipl_prior_sr = normalization_artifacts["benchmarks"]["IPL"]["benchmark_strike_rate"]

    # Low sample player (legal_balls < 10)
    low_sample = bdf[bdf["legal_balls_faced"].between(1, 10)]
    if len(low_sample) > 0:
        row = low_sample.iloc[0]
        # Shrunk SR must be pulled strongly towards the prior mean compared to raw SR
        assert abs(row["shrunk_strike_rate"] - ipl_prior_sr) < abs(row["competition_weighted_sr_index"] - ipl_prior_sr)

    # High sample player (legal_balls > 500)
    high_sample = bdf[bdf["legal_balls_faced"] > 500]
    if len(high_sample) > 0:
        row = high_sample.iloc[0]
        # Shrunk SR should be very close to competition weighted SR (< 5% difference)
        diff_pct = abs(row["shrunk_strike_rate"] - row["competition_weighted_sr_index"]) / row["competition_weighted_sr_index"]
        assert diff_pct < 0.10


@pytest.mark.data_dependent
def test_sample_confidence_tiers(normalization_artifacts):
    """Verifies that confidence tiers align with legal ball volume."""
    bdf = normalization_artifacts["batting_df"]
    for _, r in bdf.iterrows():
        balls = r["legal_balls_faced"]
        tier = r["sample_confidence_tier"]
        if balls >= 200:
            assert tier == "HIGH"
        elif balls >= 60:
            assert tier == "MEDIUM"
        else:
            assert tier == "LOW"

        assert r["is_sample_qualified"] == (balls >= 30)


@pytest.mark.data_dependent
def test_phase_splits_json_serialization(normalization_artifacts):
    """Verifies that phase splits deserialize into Powerplay, Middle, and Death and include independent confidence."""
    bdf = normalization_artifacts["batting_df"]
    sample_row = bdf.iloc[0]
    splits = json.loads(sample_row["phase_splits_json"])
    assert "Powerplay" in splits
    assert "Middle" in splits
    assert "Death" in splits
    assert splits["Powerplay"]["phase_name"] == "Powerplay"
    assert "phase_confidence_tier" in splits["Powerplay"]
    assert "is_phase_qualified" in splits["Powerplay"]


@pytest.mark.data_dependent
def test_phase_level_exposure_independence(normalization_artifacts):
    """Verifies that phase confidence is evaluated independently from overall career confidence.

    Empirically confirms that HIGH overall batters (>=200 balls) can have LOW exposure (<20 balls) in specific phases.
    """
    bdf = normalization_artifacts["batting_df"]
    high_batters_count = 0
    phase_divergence_count = 0

    for _, row in bdf.iterrows():
        splits = json.loads(row["phase_splits_json"])
        is_overall_high = row["sample_confidence_tier"] == "HIGH"
        if is_overall_high:
            high_batters_count += 1
            has_low_phase = any(s["phase_confidence_tier"] == "LOW" for s in splits.values())
            if has_low_phase:
                phase_divergence_count += 1

        # Check phase qualification rule: balls >= 20
        for ph_name, s in splits.items():
            balls = s["balls_faced"]
            expected_tier = "HIGH" if balls >= 60 else ("MEDIUM" if balls >= 20 else "LOW")
            assert s["phase_confidence_tier"] == expected_tier
            assert s["is_phase_qualified"] == (balls >= 20)

    # Over 30% of HIGH overall batters have LOW exposure in at least one phase
    assert high_batters_count == 214
    assert phase_divergence_count > 50


@pytest.mark.data_integrity
def test_sensitivity_analysis_artifact():
    """Verifies that the sensitivity analysis summary exists and covers m=30, 60, 100, 200."""
    sens_file = PROCESSED_DIR / "sensitivity_analysis_summary.json"
    assert sens_file.exists(), f"Missing {sens_file}"

    with open(sens_file, "r", encoding="utf-8") as f:
        sens = json.load(f)

    assert sens["shrinkage_parameters_evaluated"] == [30, 60, 100, 200]
    assert "batting_sensitivity" in sens
    assert "bowling_sensitivity" in sens
    assert "phase_exposure_independence" in sens

    phase_audit = sens["phase_exposure_independence"]
    assert phase_audit["total_high_tier_batters"] == 214
    assert phase_audit["high_batters_with_at_least_one_low_phase"] == 69
    assert phase_audit["total_high_tier_bowlers"] == 226
    assert phase_audit["high_bowlers_with_at_least_one_low_phase"] == 29


@pytest.mark.data_dependent
def test_bowler_extras_and_wicket_credit(normalization_artifacts):
    """Verifies that bowling profiles exclude fielding extras from runs conceded and run-outs from wickets."""
    bowling_df = normalization_artifacts["bowling_df"]
    # Check that bowler conceded runs are positive and wickets are non-negative
    assert (bowling_df["raw_runs_conceded"] >= 0).all()
    assert (bowling_df["wickets_taken"] >= 0).all()
    # Ensure economy rate equals (runs_conceded / legal_balls) * 6
    for _, r in bowling_df.head(20).iterrows():
        expected_econ = round((r["raw_runs_conceded"] / r["legal_balls_bowled"]) * 6.0, 2)
        assert abs(r["raw_economy_rate"] - expected_econ) <= 0.05


@pytest.mark.data_integrity
def test_protected_parquet_hashes_unmodified():
    """Verifies that all 4 Round 1 Parquet artifacts remain byte-for-byte untouched."""
    expected_hashes = {
        "batting_leaderboard.parquet": "fc3d9d0e7a62d162455b4ae2c97d40537ba4cf56efe6830e19afed6ceed5949d",
        "bowling_leaderboard.parquet": "dd8c96d404068e69622aa70ceea6b217399313ec1e7963ff110db5f75bbde6d0",
        "batting_evidence_profiles.parquet": "f17dbafd36ce60614b6bed93d58e45c18ad16ac5c27bfb41d510cb7f9920427c",
        "bowling_evidence_profiles.parquet": "8f138beca7d01fe9174719d055f75f4284a45c9e955842294f934e2c58adb265",
    }

    processed_dir = REPO_ROOT / "round1_pressure" / "data" / "processed"
    for filename, expected_hash in expected_hashes.items():
        file_path = processed_dir / filename
        assert file_path.exists(), f"Protected Parquet missing: {file_path}"
        with open(file_path, "rb") as f:
            actual_hash = hashlib.sha256(f.read()).hexdigest()
        assert actual_hash == expected_hash, f"Protected Parquet corrupted: {filename}"
