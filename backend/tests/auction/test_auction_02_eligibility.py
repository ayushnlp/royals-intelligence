"""
Royals Intelligence - RR Auction & Retention Intelligence
Unit & Integration Tests for AUCTION-02: Senior International Eligibility Verification.
"""

import hashlib
from pathlib import Path
import pytest
import pandas as pd

from app.schemas.auction.eligibility import (
    FormatAppearanceEvidence,
    PlayerSeniorEligibilityRecord,
    EligibilityLedgerSummary,
)
from app.auction_intelligence.eligibility.senior_cap_verifier import SeniorCapVerificationService
from app.auction_intelligence.identity.canonical_registry import VERIFIED_INDIAN_UNCAPPED

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent


@pytest.fixture(scope="module")
def eligibility_ledger():
    """Initializes and builds the AUCTION-02 senior international eligibility ledger."""
    svc = SeniorCapVerificationService()
    ledger, summary = svc.build_eligibility_ledger()
    return ledger, summary


def test_eligibility_ledger_exact_reconciliation(eligibility_ledger):
    """Verifies that the candidate universe reconciles exactly to 1,217 canonical players."""
    ledger, summary = eligibility_ledger
    assert len(ledger) == 1217
    assert summary.total_canonical_players == 1217
    
    total = (
        summary.verified_capped_count
        + summary.verified_uncapped_count
        + summary.pending_verification_count
        + summary.conflicting_evidence_count
    )
    assert total == 1217
    assert summary.verified_capped_count == 798
    assert summary.verified_uncapped_count == 287
    assert summary.pending_verification_count == 132
    assert summary.conflicting_evidence_count == 0


def test_three_format_independence_for_all_uncapped(eligibility_ledger):
    """Verifies that all 26 verified uncapped players have independent zero appearances in Test, ODI, and T20I."""
    ledger, _ = eligibility_ledger
    for pid in VERIFIED_INDIAN_UNCAPPED.keys():
        record = ledger[pid]
        assert record.final_eligibility_state == "VERIFIED_UNCAPPED"
        assert record.test_evidence.appearance_status == "ZERO_APPEARANCES"
        assert record.test_evidence.caps_count == 0
        assert record.odi_evidence.appearance_status == "ZERO_APPEARANCES"
        assert record.odi_evidence.caps_count == 0
        assert record.t20i_evidence.appearance_status == "ZERO_APPEARANCES"
        assert record.t20i_evidence.caps_count == 0


def test_sai_kishore_t20i_cap_evidence(eligibility_ledger):
    """Verifies that R. Sai Kishore is certified as VERIFIED_CAPPED with Asian Games 2023 T20I cap evidence."""
    ledger, _ = eligibility_ledger
    sk = ledger[5577]
    assert sk.final_eligibility_state == "VERIFIED_CAPPED"
    assert sk.t20i_evidence.appearance_status == "PLAYED_APPEARANCE"
    assert sk.t20i_evidence.caps_count == 3
    assert sk.t20i_evidence.debut_date == "2023-10-03"
    assert "Asian Games 2023" in sk.t20i_evidence.debut_match
    assert "T20I Cap #108" in sk.t20i_evidence.evidence_notes


def test_vyshak_kumar_squad_only_bench_callup(eligibility_ledger):
    """Verifies that Vijaykumar Vyshak is classified as VERIFIED_UNCAPPED with squad call-up evidence preserved."""
    ledger, _ = eligibility_ledger
    vk = ledger[4487]
    assert vk.final_eligibility_state == "VERIFIED_UNCAPPED"
    assert vk.t20i_evidence.appearance_status == "SQUAD_BENCH_ONLY"
    assert vk.t20i_evidence.caps_count == 0
    assert "Selection evidence" in vk.t20i_evidence.evidence_notes
    assert "0 actual playing XI appearances" in vk.t20i_evidence.evidence_notes


def test_downgraded_domestic_candidates(eligibility_ledger):
    """Verifies that confirmed domestic candidates are classified as VERIFIED_UNCAPPED."""
    ledger, _ = eligibility_ledger
    unproven_pids = [71311, 58135, 33067, 66513, 41503, 47523]
    for pid in unproven_pids:
        r = ledger[pid]
        assert r.final_eligibility_state == "VERIFIED_UNCAPPED"


def test_multi_name_collision_disambiguation(eligibility_ledger):
    """Verifies independent format and eligibility resolution for distinct cricketers sharing names."""
    ledger, _ = eligibility_ledger

    # Abdul Samad
    samad_ind = ledger[7446]
    samad_pak = ledger[6922]
    assert samad_ind.final_eligibility_state == "VERIFIED_UNCAPPED"
    assert samad_pak.final_eligibility_state == "VERIFIED_CAPPED"
    assert samad_pak.t20i_evidence.appearance_status == "PLAYED_APPEARANCE"

    # Rashid Khan
    rashid_afg = ledger[4722]
    rashid_nep = ledger[20172]
    assert rashid_afg.final_eligibility_state == "VERIFIED_CAPPED"
    assert rashid_afg.t20i_evidence.appearance_status == "PLAYED_APPEARANCE"
    assert rashid_nep.final_eligibility_state == "PENDING_VERIFICATION"
    assert rashid_nep.t20i_evidence.appearance_status == "SQUAD_BENCH_ONLY"

    # Haider Ali
    haider_pak = ledger[7338]
    haider_uae = ledger[28756]
    assert haider_pak.final_eligibility_state == "VERIFIED_CAPPED"
    assert haider_uae.final_eligibility_state == "VERIFIED_CAPPED"


def test_ravi_bishnoi_multi_format_caps(eligibility_ledger):
    """Verifies Ravi Bishnoi senior international eligibility across formats."""
    ledger, _ = eligibility_ledger
    rb = ledger[7503]
    assert rb.final_eligibility_state == "VERIFIED_CAPPED"
    assert rb.canonical_key == "RR-PLAYER-07503"
    assert rb.t20i_evidence.appearance_status == "PLAYED_APPEARANCE"
    assert rb.odi_evidence.appearance_status == "PLAYED_APPEARANCE"


def test_bench_only_squad_callups_exclusion(eligibility_ledger):
    """Verifies bench-only squad reserves classification."""
    ledger, summary = eligibility_ledger
    assert summary.bench_only_squad_callups_count in [133, 134]

    # Ensure bench-only players with no other verified caps are PENDING_VERIFICATION (unless confirmed uncapped domestic)
    bench_records = [
        r for r in ledger.values()
        if r.t20i_evidence.appearance_status == "SQUAD_BENCH_ONLY"
    ]
    assert len(bench_records) in [133, 134]
    for r in bench_records:
        if r.test_evidence.appearance_status != "PLAYED_APPEARANCE" and r.odi_evidence.appearance_status != "PLAYED_APPEARANCE":
            assert r.final_eligibility_state in ["PENDING_VERIFICATION", "VERIFIED_UNCAPPED"]


def test_exported_ledger_artifacts_exist():
    """Verifies that Parquet, JSON, and summary files exist on disk."""
    out_dir = REPO_ROOT / "data" / "processed" / "auction_intelligence"
    assert (out_dir / "senior_international_eligibility_ledger.parquet").exists()
    assert (out_dir / "senior_international_eligibility_ledger.json").exists()
    assert (out_dir / "eligibility_ledger_summary.json").exists()


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
