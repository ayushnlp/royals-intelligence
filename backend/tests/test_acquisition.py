"""
Royals Intelligence - Stage 1 Data Acquisition Engine Test Suite
Validates source registry, adapters, data contracts, validation rules,
idempotency, Parquet queries, and acquisition REST endpoints.
"""

import json
from pathlib import Path
import pytest
from app.acquisition.registry import source_registry
from app.acquisition.validation.validator import CricketDataValidator
from app.acquisition.normalization.normalizer import CricketDataNormalizer
from app.acquisition.storage.raw_storage import RawStorageManager
from app.acquisition.storage.parquet_store import ParquetStorageManager
from app.acquisition.orchestration.orchestrator import orchestrator
from app.schemas.contracts.cricket_contracts import (
    BallByBallDelivery,
    DeliveryExtras,
    SourceReference,
)
from datetime import datetime, timezone


# --- 1. Source Registry Tests ---

def test_source_registry_listing():
    sources = source_registry.list_sources()
    assert len(sources) >= 5
    source_ids = [s["source_id"] for s in sources]
    assert "cricsheet_open" in source_ids
    assert "iplt20_official" in source_ids
    assert "open_meteo_historical" in source_ids
    assert "espncricinfo_reference" in source_ids


def test_source_registry_tier_filtering():
    tier1_sources = source_registry.list_sources(tier="TIER_1")
    assert all(s["tier"] == "TIER_1" for s in tier1_sources)
    assert any(s["source_id"] == "cricsheet_open" for s in tier1_sources)

    tier4_sources = source_registry.list_sources(tier="TIER_4")
    assert all(s["tier"] == "TIER_4" for s in tier4_sources)
    assert any(s["source_id"] == "espncricinfo_reference" for s in tier4_sources)


def test_source_availability_check():
    diag_cricsheet = source_registry.check_source_availability("cricsheet_open")
    assert diag_cricsheet["is_accessible"] is True
    assert diag_cricsheet["status"] == "AVAILABLE"

    diag_espn = source_registry.check_source_availability("espncricinfo_reference")
    assert diag_espn["is_accessible"] is False
    assert diag_espn["status"] == "RESTRICTED_MANUAL_ONLY"


# --- 2. Cricket Data Contract & Anti-Fabrication Rules ---

def test_ball_by_ball_delivery_contract_valid():
    source_ref = SourceReference(
        source_id="cricsheet_open",
        source_url_or_file="sample.json",
        ingested_at=datetime.now(timezone.utc),
    )
    delivery = BallByBallDelivery(
        match_id="test_001",
        innings_number=1,
        over_number=0,
        ball_in_over=1,
        over_display=0.1,
        phase="Powerplay",
        batting_team="RR",
        bowling_team="CSK",
        striker="Yashasvi Jaiswal",
        non_striker="Jos Buttler",
        bowler="Deepak Chahar",
        batter_runs=4,
        extras=DeliveryExtras(),
        total_runs=4,
        is_legal=True,
        is_boundary_four=True,
        source_ref=source_ref,
        # Strictly None unless source provides it
        release_speed_kph=None,
        delivery_classification=None,
    )
    assert delivery.total_runs == 4
    assert delivery.delivery_classification is None


def test_ball_by_ball_arithmetic_mismatch_rejected():
    source_ref = SourceReference(
        source_id="cricsheet_open",
        source_url_or_file="sample.json",
        ingested_at=datetime.now(timezone.utc),
    )
    with pytest.raises(ValueError, match="total_runs.*must equal"):
        BallByBallDelivery(
            match_id="test_002",
            innings_number=1,
            over_number=0,
            ball_in_over=1,
            over_display=0.1,
            phase="Powerplay",
            batting_team="RR",
            bowling_team="CSK",
            striker="Sanju Samson",
            non_striker="Jos Buttler",
            bowler="Mustafizur Rahman",
            batter_runs=2,
            extras=DeliveryExtras(),
            total_runs=6,  # Fabricated arithmetic
            source_ref=source_ref,
        )


# --- 3. Cricket Data Validation Engine Tests ---

def test_validator_detects_arithmetic_mismatch():
    corrupted_match = {
        "info": {
            "teams": ["Rajasthan Royals", "Chennai Super Kings"],
            "dates": ["2024-04-22"],
            "match_type": "T20"
        },
        "innings": [
            {
                "team": "Rajasthan Royals",
                "overs": [
                    {
                        "over": 0,
                        "deliveries": [
                            {
                                "batter": "Sanju Samson",
                                "bowler": "Deepak Chahar",
                                "non_striker": "Jos Buttler",
                                "runs": {"batter": 2, "extras": 0, "total": 5}  # Corrupted
                            }
                        ]
                    }
                ]
            }
        ]
    }
    summary = CricketDataValidator.validate_cricsheet_match_dict(corrupted_match, "corrupt_001")
    assert summary.passed is False
    assert any(e.error_type == "ARITHMETIC_MISMATCH" for e in summary.errors)


def test_validator_passes_valid_sample_match():
    root_dir = Path(__file__).resolve().parent.parent.parent
    sample_file = root_dir / "data" / "raw" / "public" / "samples" / "sample_match_rr_csk.json"
    with open(sample_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    summary = CricketDataValidator.validate_cricsheet_match_dict(data, "sample_rr_csk")
    assert summary.passed is True
    assert summary.rejected_records == 0
    assert summary.completeness_percentage == 100.0


# --- 4. Normalization Layer Tests ---

def test_team_and_venue_normalization():
    assert CricketDataNormalizer.normalize_team("Kings XI Punjab") == "PBKS"
    assert CricketDataNormalizer.normalize_team("Royal Challengers Bangalore") == "RCB"
    assert CricketDataNormalizer.normalize_team("Delhi Daredevils") == "DC"
    assert CricketDataNormalizer.normalize_team("Rajasthan Royals") == "RR"

    assert CricketDataNormalizer.normalize_venue("Sawai Mansingh Stadium, Jaipur") == "SMS_JAIPUR"
    assert CricketDataNormalizer.normalize_venue("Wankhede Stadium, Mumbai") == "WANKHEDE_MUMBAI"


def test_phase_assignment():
    assert CricketDataNormalizer.get_phase(0) == "Powerplay"
    assert CricketDataNormalizer.get_phase(5) == "Powerplay"
    assert CricketDataNormalizer.get_phase(6) == "Middle"
    assert CricketDataNormalizer.get_phase(14) == "Middle"
    assert CricketDataNormalizer.get_phase(15) == "Death"
    assert CricketDataNormalizer.get_phase(19) == "Death"


# --- 5. Storage & Idempotent Ingestion Tests ---

def test_raw_storage_checksum_and_idempotency(tmp_path):
    storage = RawStorageManager(base_raw_dir=tmp_path)
    test_file = tmp_path / "test_match.json"
    test_file.write_text('{"test": "match_content"}', encoding="utf-8")

    meta1, is_new1 = storage.store_raw_file(test_file, subfolder="test_sub")
    assert is_new1 is True
    assert meta1.checksum_sha256 is not None

    # Storing identical file again should result in idempotent skip
    meta2, is_new2 = storage.store_raw_file(test_file, subfolder="test_sub")
    assert is_new2 is False
    assert meta1.checksum_sha256 == meta2.checksum_sha256


def test_parquet_deliveries_query():
    storage = ParquetStorageManager()
    stats = storage.get_storage_stats()
    assert stats["total_matches_indexed"] >= 1
    assert stats["total_deliveries_indexed"] >= 1

    df_jaiswal = storage.query_deliveries(batter="Yashasvi Jaiswal")
    assert len(df_jaiswal) >= 1
    assert "striker" in df_jaiswal.columns
    assert "phase" in df_jaiswal.columns


# --- 6. API Endpoint Tests ---

def test_api_list_sources(client):
    res = client.get("/api/v1/acquisition/sources")
    assert res.status_code == 200
    sources = res.json()
    assert len(sources) >= 5
    assert any(s["source_id"] == "cricsheet_open" for s in sources)


def test_api_get_source_detail(client):
    res = client.get("/api/v1/acquisition/sources/cricsheet_open")
    assert res.status_code == 200
    data = res.json()
    assert data["source_id"] == "cricsheet_open"
    assert "licensing" in data
    assert data["tier"] == "TIER_1"


def test_api_get_source_health(client):
    res = client.get("/api/v1/acquisition/sources/cricsheet_open/health")
    assert res.status_code == 200
    data = res.json()
    assert data["source_id"] == "cricsheet_open"
    assert data["is_accessible"] is True


def test_api_get_coverage_report(client):
    res = client.get("/api/v1/acquisition/coverage")
    assert res.status_code == 200
    data = res.json()
    assert "primary_season" in data
    assert data["primary_season"] == "IPL 2026"
    assert "competitions" in data


def test_api_list_runs_and_datasets(client):
    runs_res = client.get("/api/v1/acquisition/runs")
    assert runs_res.status_code == 200
    assert isinstance(runs_res.json(), list)

    datasets_res = client.get("/api/v1/acquisition/datasets")
    assert datasets_res.status_code == 200
    assert isinstance(datasets_res.json(), list)


def test_api_manual_upload_unsupported_format_rejected(client):
    files = {"file": ("unsupported.exe", b"malicious binary", "application/octet-stream")}
    res = client.post("/api/v1/acquisition/upload", files=files)
    assert res.status_code == 400
    assert "Unsupported file type" in res.json()["detail"]


def test_api_manual_upload_valid_json(client):
    valid_json = json.dumps({"note": "vetted domestic trial observation", "player": "Sanju Samson"})
    files = {"file": ("trial_notes.json", valid_json.encode("utf-8"), "application/json")}
    res = client.post(
        "/api/v1/acquisition/upload",
        files=files,
        data={"competition_id": "domestic", "season": "2026"}
    )
    assert res.status_code == 200
    data = res.json()
    assert data["checksum_sha256"] is not None
    assert data["file_format"] == "json"

