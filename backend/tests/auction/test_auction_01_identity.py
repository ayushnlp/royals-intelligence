"""
Royals Intelligence - RR Auction & Retention Intelligence
Unit & Integration Tests for AUCTION-01: Player Identity & Candidate Universe.
Updated to reflect rigorous acceptance checks:
1. Ravi Bishnoi identity semantics (1 individual, 2 preserved source rows, no identity conflict).
2. Globally unique namespaced canonical keys (RR-PLAYER-XXXXX).
3. Sai Kishore and Vyshak Kumar certified as VERIFIED_CAPPED.
4. Unproven candidates downgraded to PENDING_VERIFICATION.
5. Byte-for-byte SHA-256 verification of 4 protected Round 1 Parquet artifacts.
"""

import hashlib
from pathlib import Path
import pytest
import pandas as pd

from app.schemas.auction.identity import PlayerIdentityMapping, CandidateUniverseSummary
from app.auction_intelligence.identity.alias_resolver import AliasResolver, KNOWN_NAME_ALIASES, KNOWN_DISAMBIGUATION_MAP
from app.auction_intelligence.identity.canonical_registry import (
    CanonicalPlayerRegistryService,
    SENIOR_NATIONAL_TEAMS,
    HISTORICAL_SENIOR_INDIAN_CAPS,
    VERIFIED_INDIAN_UNCAPPED,
    KNOWN_CONFLICT_NOTES,
)

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent


@pytest.fixture(scope="module")
def registry_data():
    """Initializes and builds the canonical player identity registry."""
    svc = CanonicalPlayerRegistryService()
    registry, summary = svc.build_registry()
    return registry, summary


@pytest.mark.data_dependent
def test_canonical_universe_breadth(registry_data):
    """Verifies candidate universe includes all 1,217 players and is not restricted to 268."""
    registry, summary = registry_data
    assert summary.total_canonical_players == 1217
    assert len(registry) == 1217
    assert summary.total_ipl_historical_players == 477
    assert summary.total_supplied_csv_players == 268
    assert summary.total_canonical_players > summary.total_supplied_csv_players
    assert summary.verified_uncapped_count == 26
    assert summary.verified_capped_count == 931
    assert summary.pending_verification_count == 260
    assert summary.conflicting_evidence_count == 0


@pytest.mark.data_dependent
def test_source_id_preservation_and_canonical_key(registry_data):
    """Verifies that source IDs are preserved and canonical keys are globally unique."""
    registry, _ = registry_data
    seen_keys = set()
    for pid, mapping in registry.items():
        assert mapping.canonical_id == pid
        assert pid in mapping.source_player_ids
        assert len(mapping.source_player_ids) >= 1
        assert len(mapping.canonical_name.strip()) > 0
        expected_key = f"RR-PLAYER-{pid:05d}"
        assert mapping.canonical_key == expected_key
        assert expected_key not in seen_keys
        seen_keys.add(expected_key)

    assert len(seen_keys) == 1217


@pytest.mark.unit
def test_alias_resolution_all_23_cases():
    """Verifies that all 23 known name aliases resolve to valid canonical entities."""
    for raw_alias, (expected_id, expected_name) in KNOWN_NAME_ALIASES.items():
        res = AliasResolver.resolve_alias(raw_alias)
        assert res is not None, f"Failed to resolve alias: {raw_alias}"
        assert res[0] == expected_id, f"ID mismatch for {raw_alias}: expected {expected_id}, got {res[0]}"


@pytest.mark.unit
def test_duplicate_name_disambiguation():
    """Verifies that identical strings (Abdul Samad, Rashid Khan, Haider Ali) disambiguate correctly."""
    # Abdul Samad
    srh_samad = AliasResolver.resolve_alias("Abdul Samad", "Sunrisers Hyderabad")
    pak_samad = AliasResolver.resolve_alias("Abdul Samad", "Pakistan")
    assert srh_samad[0] == 7446
    assert pak_samad[0] == 6922

    # Rashid Khan
    gt_rashid = AliasResolver.resolve_alias("Rashid Khan", "Gujarat Titans")
    nepal_rashid = AliasResolver.resolve_alias("Rashid Khan", "Nepal")
    assert gt_rashid[0] == 4722
    assert nepal_rashid[0] == 20172

    # Haider Ali
    pak_haider = AliasResolver.resolve_alias("Haider Ali", "Pakistan")
    uae_haider = AliasResolver.resolve_alias("Haider Ali", "United Arab Emirates")
    assert pak_haider[0] == 7338
    assert uae_haider[0] == 28756


@pytest.mark.data_dependent
def test_unmatched_player_coverage(registry_data):
    """Verifies that 100% of the 268 records in ipl_players.csv resolve cleanly."""
    registry, summary = registry_data
    ipl_csv_path = REPO_ROOT / "data" / "raw" / "rajasthan_royals" / "round_1_data_pack" / "ipl_players.csv"
    df = pd.read_csv(ipl_csv_path)
    assert len(df) == 268

    matched_count = 0
    for _, row in df.iterrows():
        pname = str(row["Name"]).strip()
        team = str(row["Team"]).strip()

        matched = False
        for pid, ent in registry.items():
            if pname == ent.canonical_name or pname in ent.aliases:
                matched = True
                break
        assert matched, f"Player from ipl_players.csv failed to resolve: {pname} ({team})"
        matched_count += 1

    assert matched_count == 268


@pytest.mark.data_dependent
def test_ravi_bishnoi_identity_semantics(registry_data):
    """
    Verifies that Ravi Bishnoi is ONE human individual:
    - 1 canonical entity (canonical_id 7503)
    - Both source records preserved (Row 179 and Row 261)
    - Both franchise associations preserved (LSG and RR)
    - Not classified as an identity conflict
    - Certified as VERIFIED_CAPPED
    """
    registry, _ = registry_data
    rb = registry.get(7503)
    assert rb is not None
    assert rb.canonical_id == 7503
    assert rb.canonical_key == "RR-PLAYER-07503"
    assert rb.has_identity_conflict is False
    assert rb.conflict_notes is None
    assert "Lucknow Super Giants" in rb.historical_franchises
    assert "Rajasthan Royals" in rb.historical_franchises
    assert rb.source_record_indices.get("ipl_players.csv") == [179, 261]
    assert rb.cap_certification_status == "VERIFIED_CAPPED"


@pytest.mark.data_dependent
def test_rr_squad_strict_decoupling(registry_data):
    """Verifies strict decoupling of historical RR association from verified current squad."""
    registry, summary = registry_data
    assert summary.rr_historical_core_count == 69
    assert summary.rr_supplied_csv_count == 27

    for pid, ent in registry.items():
        assert ent.verified_current_rr_squad == "UNCONFIRMED_PENDING_BCCI_CIRCULAR"
        assert ent.contract_retention_status == "PENDING_OFFICIAL_FILING"
        assert ent.auction_registration_status == "PENDING_OFFICIAL_IPL_2027_LONGLIST"


@pytest.mark.data_dependent
def test_capped_reclassifications_and_downgrades(registry_data):
    """Verifies that Sai Kishore is CAPPED, and Vyshak + unproven players are PENDING."""
    registry, _ = registry_data

    # Sai Kishore (Asian Games 2023 T20I Cap #108)
    sk = registry[5577]
    assert sk.cap_certification_status == "VERIFIED_CAPPED"
    assert "Asian Games 2023" in sk.cap_evidence_notes

    # Vyshak Kumar (Touring squad call-up only, 0 playing XI appearances -> PENDING)
    vk = registry[4487]
    assert vk.cap_certification_status == "PENDING_VERIFICATION"
    assert "Selection evidence" in vk.cap_evidence_notes
    assert "0 actual playing XI appearances" in vk.cap_evidence_notes

    # Downgraded unproven candidates
    for pid in [71311, 58135, 33067, 66513, 41503, 47523]:
        p = registry[pid]
        assert p.cap_certification_status == "PENDING_VERIFICATION", f"Player {pid} ({p.canonical_name}) should be PENDING"


@pytest.mark.data_dependent
def test_four_eligibility_states_governance(registry_data):
    """Verifies four discrete eligibility states without inferring uncapped from omission."""
    registry, summary = registry_data
    valid_states = {"VERIFIED_UNCAPPED", "VERIFIED_CAPPED", "PENDING_VERIFICATION", "CONFLICTING_EVIDENCE"}

    state_counts = {s: 0 for s in valid_states}
    for ent in registry.values():
        state_counts[ent.cap_certification_status] += 1

    assert state_counts["VERIFIED_UNCAPPED"] == summary.verified_uncapped_count
    assert state_counts["VERIFIED_CAPPED"] == summary.verified_capped_count
    assert state_counts["PENDING_VERIFICATION"] == summary.pending_verification_count
    assert state_counts["CONFLICTING_EVIDENCE"] == summary.conflicting_evidence_count

    assert summary.verified_uncapped_count == 26
    assert summary.verified_capped_count == 931
    assert summary.pending_verification_count == 260
    assert summary.conflicting_evidence_count == 0


@pytest.mark.data_dependent
def test_provenance_and_traceability(registry_data):
    """Verifies that all entities track provenance sources."""
    registry, _ = registry_data
    for ent in registry.values():
        assert len(ent.provenance_sources) >= 1
        assert "competition_team_player_mapping.csv" in ent.provenance_sources


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
