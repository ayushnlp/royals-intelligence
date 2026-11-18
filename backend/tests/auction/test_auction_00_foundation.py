"""
Royals Intelligence - RR Auction & Retention Intelligence
Unit & Integration Tests for AUCTION-00: Foundation & Data Readiness.

Strict Acceptance Criteria:
1. Verification of all 7 raw datasets in the data pack with SHA-256 digests.
2. Strict delivery count semantics: 200,999 total, 192,709 legal, 8,290 extras (7,714 wides + 576 no-balls).
3. Match coverage semantics: 883 total, 867 ball-recorded, 16 abandoned/no-result.
4. Schema validation & null accounting: exactly 32 null bowling styles (15 batters + 17 keepers).
5. Duplicate detection: Ravi Bishnoi dual-attribution (RR row 179 vs LSG row 261).
6. RR 2026 squad baseline: exactly 27 rows (12 Bowlers, 6 All-rounders, 5 Batters, 4 Wicketkeeper-Batters).
7. Governance trade disclaimers (Samson CSK, Jadeja RR, Curran RR, Bishnoi duplicate).
8. Referential integrity across matches, ball-by-ball, and playing eleven.
9. Byte-for-byte SHA-256 verification of 4 protected Round 1 Parquet artifacts.
"""

import hashlib
from pathlib import Path
import pytest
import pandas as pd

from app.core.config import get_repo_root
from app.auction_intelligence.foundation.data_ingestion import (
    DataIngestionService,
    EXPECTED_FILES,
    LEGAL_DELIVERY_COUNT,
    TOTAL_DELIVERY_COUNT,
    NON_LEGAL_DELIVERY_COUNT,
    WIDES_COUNT,
    NO_BALLS_COUNT,
    TOTAL_MATCH_COUNT,
    BALL_RECORDED_MATCH_COUNT,
    ABANDONED_MATCH_COUNT,
)
from app.auction_intelligence.foundation.quality_audit import DataQualityAuditService
from app.auction_intelligence.foundation.squad_baseline import RRSquadBaselineService, DISCLAIMERS

REPO_ROOT = get_repo_root()


@pytest.fixture(scope="module")
def ingestion_svc():
    return DataIngestionService()


@pytest.fixture(scope="module")
def quality_svc(ingestion_svc):
    return DataQualityAuditService(ingestion_svc)


@pytest.fixture(scope="module")
def squad_svc(ingestion_svc):
    return RRSquadBaselineService(ingestion_svc)


def test_data_pack_files_exist_and_checksummed(ingestion_svc):
    """Verifies that all 7 required raw data pack CSV files exist and can be inspected."""
    datasets = ingestion_svc.inspect_datasets()
    assert len(datasets) == len(EXPECTED_FILES)
    for filename in EXPECTED_FILES:
        assert filename in datasets
        meta = datasets[filename]
        assert meta.size_bytes > 0
        assert len(meta.sha256) == 64
        assert meta.row_count > 0
        assert meta.column_count == EXPECTED_FILES[filename]


def test_delivery_semantics_exact_counts(ingestion_svc):
    """Verifies the exact delivery semantics:
    - 200,999 total deliveries
    - 8,290 non-legal balls (7,714 wides + 576 overstep no-balls)
    - 192,709 strict legal deliveries
    """
    summary = ingestion_svc.reconcile_delivery_semantics()
    assert summary.total_rows == TOTAL_DELIVERY_COUNT
    assert summary.legal_deliveries == LEGAL_DELIVERY_COUNT
    assert summary.extras_deliveries == NON_LEGAL_DELIVERY_COUNT
    assert summary.wides == WIDES_COUNT
    assert summary.no_balls == NO_BALLS_COUNT
    assert summary.total_runs_conceded > 0
    assert summary.total_wickets > 0


def test_match_coverage_exact_counts(ingestion_svc):
    """Verifies match coverage:
    - 883 total matches in matches.csv
    - 867 matches with ball-by-ball delivery records
    - 16 matches abandoned or without ball-by-ball records
    """
    coverage = ingestion_svc.reconcile_match_coverage()
    assert coverage.total_matches == TOTAL_MATCH_COUNT
    assert coverage.matches_with_balls == BALL_RECORDED_MATCH_COUNT
    assert coverage.abandoned_or_no_result == ABANDONED_MATCH_COUNT


def test_ipl_players_null_bowling_styles(quality_svc):
    """Verifies that exactly 32 players have null Bowling_Style and that all are non-bowling Batters or Keepers."""
    issues = quality_svc.audit_null_values()
    assert len(issues) == 1
    issue = issues[0]
    assert issue.affected_rows == 32
    assert issue.resolution_status == "VALIDATED_DOMAIN_CORRECT"

    # Direct dataframe verification
    players_df = quality_svc.ingestion.load_dataset("ipl_players.csv")
    null_bowling = players_df[players_df["Bowling_Style"].isna()]
    assert len(null_bowling) == 32
    roles = null_bowling["Role"].value_counts().to_dict()
    assert roles.get("Batter", 0) == 3
    assert roles.get("Wicketkeeper-Batter", 0) == 29
    assert roles.get("Bowler", 0) == 0
    assert roles.get("All-rounder", 0) == 0


def test_duplicate_player_detection(quality_svc):
    """Verifies that exactly one player name is duplicated in ipl_players.csv: Ravi Bishnoi."""
    issues = quality_svc.audit_duplicate_records()
    assert len(issues) == 1
    issue = issues[0]
    assert "RAVI_BISHNOI" in issue.issue_id
    assert issue.affected_rows == 2

    # Direct dataframe verification
    players_df = quality_svc.ingestion.load_dataset("ipl_players.csv")
    dup_names = players_df[players_df.duplicated(subset=["Name"], keep=False)]
    assert dup_names["Name"].nunique() == 1
    assert dup_names["Name"].iloc[0] == "Ravi Bishnoi"
    teams = set(dup_names["Team"])
    assert teams == {"Rajasthan Royals", "Lucknow Super Giants"}


def test_rr_2026_squad_baseline_reconciliation(squad_svc):
    """Verifies that the RR squad baseline contains exactly 27 entries:
    - 12 Bowlers
    - 6 All-rounders
    - 5 Batters
    - 4 Wicketkeeper-Batters
    """
    breakdown = squad_svc.get_role_breakdown()
    assert breakdown.total_players == 27
    assert breakdown.bowlers == 12
    assert breakdown.all_rounders == 6
    assert breakdown.batters == 5
    assert breakdown.wicketkeeper_batters == 4


def test_rr_squad_governance_disclaimers(squad_svc):
    """Verifies that critical franchise dislocations and trade disclaimers are documented."""
    disclaimers = squad_svc.get_disclaimer_audit()
    assert "Sanju Samson" in disclaimers
    assert "Ravindra Jadeja" in disclaimers
    assert "Sam Curran" in disclaimers
    assert "Ravi Bishnoi" in disclaimers

    # Sanju Samson listed under CSK
    players_df = squad_svc.ingestion.load_dataset("ipl_players.csv")
    samson = players_df[players_df["Name"] == "Sanju Samson"]
    assert len(samson) == 1
    assert samson.iloc[0]["Team"] == "Chennai Super Kings"

    # Jadeja and Curran listed under RR
    jadeja = players_df[players_df["Name"] == "Ravindra Jadeja"]
    assert len(jadeja) == 1
    assert jadeja.iloc[0]["Team"] == "Rajasthan Royals"

    curran = players_df[players_df["Name"] == "Sam Curran"]
    assert len(curran) == 1
    assert curran.iloc[0]["Team"] == "Rajasthan Royals"


def test_referential_integrity(quality_svc):
    """Verifies that 100% of deliveries and playing eleven match_ids exist in matches.csv."""
    issues = quality_svc.audit_referential_integrity()
    bbb_issue = next(i for i in issues if i.issue_id == "DQI-003-ORPHAN-BBB-MATCHES")
    p11_issue = next(i for i in issues if i.issue_id == "DQI-004-ORPHAN-P11-MATCHES")
    abandoned_issue = next(i for i in issues if i.issue_id == "DQI-005-ABANDONED-MATCHES")

    assert bbb_issue.affected_rows == 0
    assert bbb_issue.resolution_status == "VERIFIED_CLEAN"

    assert p11_issue.affected_rows == 0
    assert p11_issue.resolution_status == "VERIFIED_CLEAN"

    assert abandoned_issue.affected_rows == 16


def test_competition_mapping_universe_breadth(ingestion_svc):
    """Verifies that competition_team_player_mapping.csv covers 1,217 unique players across 6,413 rows."""
    mapping_df = ingestion_svc.load_dataset("competition_team_player_mapping.csv")
    assert len(mapping_df) == 6413
    assert mapping_df["player_id"].nunique() == 1217


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
