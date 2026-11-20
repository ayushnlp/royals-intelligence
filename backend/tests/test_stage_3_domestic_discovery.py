"""
Royals Intelligence - Stage 3 Domestic Intelligence Dynamic Player Discovery Tests
Verifies the complete implementation of:
1. Dynamic player discovery across canonical registry and eligibility ledger.
2. Filter by eligibility: VERIFIED_UNCAPPED (26 players), PENDING_VERIFICATION.
3. Search by player name, key, and aliases.
4. Overseas player exclusion from domestic uncapped discovery.
5. Canonical integer IDs exclusively enforced.
6. HTTP 404 on nonexistent player ID.
7. HTTP 403 on Senior Capped International player.
8. Real domestic statistics aggregation from delivery_states_strict.parquet.
9. NO_STATISTICAL_COVERAGE handling with zero fabrication for players with 0 deliveries.
10. Phase splits aggregation across Powerplay, Middle, Death overs.
11. Evidence-based all-round dual contribution without composite score fabrication.
12. Competition directory discovery with complete exclusion of UP T20 League.
13. Season parameter normalization (2024-25 vs 2024).
14. Backward compatibility preservation for legacy test fixtures.
"""

import pytest
from starlette.testclient import TestClient
from app.main import app
from app.services.domestic.domestic_season_service import DomesticSeasonService

client = TestClient(app)


@pytest.mark.data_dependent
def test_dynamic_player_discovery_endpoint():
    """Verifies that GET /api/v1/domestic/players returns paginated candidate records."""
    res = client.get("/api/v1/domestic/players?page=1&page_size=20")
    assert res.status_code == 200
    data = res.json()
    assert "items" in data
    assert "total" in data
    assert "page" in data
    assert "page_size" in data
    assert "total_pages" in data
    assert data["total"] >= 280
    assert len(data["items"]) == 20

    first = data["items"][0]
    assert isinstance(first["canonical_id"], int)
    assert first["player_id"] == str(first["canonical_id"])
    assert len(first["player_name"]) > 0
    assert first["eligibility_status"] in ["VERIFIED_UNCAPPED", "PENDING_VERIFICATION"]
    assert first["statistical_coverage_status"] in ["AVAILABLE", "NO_STATISTICAL_COVERAGE"]


@pytest.mark.data_dependent
def test_verified_uncapped_player_filter():
    """Verifies that filtering by VERIFIED_UNCAPPED returns all verified uncapped Indian domestic players."""
    res = client.get("/api/v1/domestic/players?eligibility_status=VERIFIED_UNCAPPED&page_size=100")
    assert res.status_code == 200
    data = res.json()
    assert data["total"] == 287
    for item in data["items"]:
        assert item["eligibility_status"] == "VERIFIED_UNCAPPED"
        assert item["is_uncapped"] is True

    # Confirm key uncapped prospects exist in the list
    names = [p["player_name"] for p in data["items"]]
    assert "Ashutosh Sharma" in names
    assert "Priyansh Arya" in names
    assert "Vaibhav Arora" in names
    assert "Sameer Rizvi" in names
    assert "Nehal Wadhera" in names


@pytest.mark.data_dependent
def test_pending_verification_domestic_filter():
    """Verifies that filtering by PENDING_VERIFICATION returns 0 candidates following complete domestic verification."""
    res = client.get("/api/v1/domestic/players?eligibility_status=PENDING_VERIFICATION&page_size=20")
    assert res.status_code == 200
    data = res.json()
    assert data["total"] == 0
    for item in data["items"]:
        assert item["eligibility_status"] == "PENDING_VERIFICATION"


@pytest.mark.data_dependent
def test_overseas_exclusion_from_domestic_discovery():
    """Verifies that overseas players (e.g. Australian, English, West Indian) are excluded from domestic discovery."""
    res = client.get("/api/v1/domestic/players?eligibility_status=ALL&page_size=500")
    assert res.status_code == 200
    data = res.json()
    names = [p["player_name"] for p in data["items"]]
    # Confirm known senior overseas players are NOT in the domestic discovery pool
    assert "Pat Cummins" not in names
    assert "Travis Head" not in names
    assert "Mitchell Starc" not in names
    assert "Nicholas Pooran" not in names
    assert "Heinrich Klaasen" not in names


@pytest.mark.data_dependent
def test_player_search_by_name():
    """Verifies that search finds players by full or partial name."""
    res = client.get("/api/v1/domestic/players?search=Ashutosh")
    assert res.status_code == 200
    data = res.json()
    assert data["total"] >= 1
    p = data["items"][0]
    assert p["canonical_id"] == 8101
    assert "Ashutosh" in p["player_name"]


@pytest.mark.data_dependent
def test_nonexistent_player_returns_404():
    """Verifies that nonexistent player IDs return HTTP 404 Not Found (no silent fallback)."""
    # 1. Nonexistent integer ID
    res1 = client.get("/api/v1/domestic/players/999999/all-round-summary")
    assert res1.status_code == 404

    res2 = client.get("/api/v1/domestic/players/999999/season-stats")
    assert res2.status_code == 404

    # 2. Nonexistent synthetic string ID
    res3 = client.get("/api/v1/domestic/players/uncapped_rr_99/all-round-summary")
    assert res3.status_code == 404


@pytest.mark.data_dependent
def test_senior_capped_player_returns_403_forbidden():
    """Verifies that senior international capped players are rejected with HTTP 403 Forbidden under uncapped scope."""
    # Jasprit Bumrah (canonical_id 2933) is senior capped
    res1 = client.get("/api/v1/domestic/players/2933/all-round-summary")
    assert res1.status_code == 403
    assert "Senior Capped" in res1.json()["detail"]

    # Virat Kohli (canonical_id 47) is senior capped
    res2 = client.get("/api/v1/domestic/players/47/season-stats")
    assert res2.status_code == 403


@pytest.mark.data_dependent
def test_real_statistical_aggregation_ashutosh_sharma():
    """Verifies dynamic aggregation of real statistics from delivery_states_strict.parquet for Ashutosh Sharma (8101)."""
    # 1. Season stats
    res_stats = client.get("/api/v1/domestic/players/8101/season-stats")
    assert res_stats.status_code == 200
    stats = res_stats.json()
    assert len(stats) >= 1

    total_runs = sum(s["runs"] for s in stats)
    assert total_runs > 500  # Ashutosh has 577 recorded runs across seasons

    ipl_2024 = next((s for s in stats if s["season"] == "2024"), None)
    assert ipl_2024 is not None
    assert ipl_2024["runs"] == 189
    assert ipl_2024["strike_rate"] > 165.0
    assert ipl_2024["sixes"] == 15

    # 2. Phase splits
    res_phases = client.get("/api/v1/domestic/players/8101/phase-splits")
    assert res_phases.status_code == 200
    phases = res_phases.json()
    assert len(phases) == 3
    death = next(p for p in phases if p["phase"] == "Death")
    assert death["batting_runs"] > 350
    assert death["batting_strike_rate"] > 180.0

    # 3. All-Round Summary
    res_ar = client.get("/api/v1/domestic/players/8101/all-round-summary")
    assert res_ar.status_code == 200
    ar = res_ar.json()
    assert ar["canonical_id"] == "8101"
    assert ar["statistical_coverage_status"] == "AVAILABLE"
    assert ar["sample_size"]["matches"] > 20
    assert ar["batting_summary"]["runs"] == total_runs


@pytest.mark.data_dependent
def test_real_bowling_aggregation_vaibhav_arora():
    """Verifies real bowling aggregation for Vaibhav Arora (8746)."""
    res_ar = client.get("/api/v1/domestic/players/8746/all-round-summary")
    assert res_ar.status_code == 200
    ar = res_ar.json()
    assert ar["canonical_id"] == "8746"
    assert ar["statistical_coverage_status"] == "AVAILABLE"
    assert ar["bowling_summary"]["bowler_wickets"] >= 40
    assert ar["bowling_summary"]["overs"] > 100.0


@pytest.mark.data_dependent
def test_no_statistical_coverage_yarra_prithviraj():
    """Verifies that an uncapped player with 0 deliveries returns NO_STATISTICAL_COVERAGE and zero stats."""
    # Yarra Prithviraj (6351) is a verified uncapped bowler with 0 match deliveries in current pack
    res_ar = client.get("/api/v1/domestic/players/6351/all-round-summary")
    assert res_ar.status_code == 200
    ar = res_ar.json()
    assert ar["canonical_id"] == "6351"
    assert ar["statistical_coverage_status"] == "NO_STATISTICAL_COVERAGE"
    assert ar["has_sufficient_sample"] is False
    assert "No domestic match telemetry recorded" in ar["data_note"]
    assert ar["sample_size"]["innings_batted"] == 0
    assert ar["sample_size"]["overs_bowled"] == 0.0

    res_stats = client.get("/api/v1/domestic/players/6351/season-stats")
    assert res_stats.status_code == 200
    assert res_stats.json() == []


@pytest.mark.data_dependent
def test_competitions_catalog_excludes_up_t20():
    """Verifies that GET /api/v1/domestic/competitions completely excludes non-existent UP T20 League."""
    res = client.get("/api/v1/domestic/competitions")
    assert res.status_code == 200
    comps = res.json()
    comp_ids = [c["competition_id"].lower() for c in comps]
    comp_names = [c["competition_name"].lower() for c in comps]

    assert "up_t20" not in comp_ids
    assert "up t20" not in comp_names
    assert not any("up t20" in name for name in comp_names)

    # Valid competitions are present
    assert "ipl" in comp_ids
    assert "smat" in comp_ids
    assert "vht" in comp_ids
    assert "ranji" in comp_ids
    assert "dpl" in comp_ids


@pytest.mark.data_dependent
def test_season_identifier_normalization():
    """Verifies that season parameter formats ('2024-25' and '2024') resolve consistently."""
    res1 = client.get("/api/v1/domestic/seasons/ipl/2024/matches?page=1&page_size=10")
    assert res1.status_code == 200
    assert res1.json()["total_matches"] == 74

    res2 = client.get("/api/v1/domestic/seasons/ipl/2024-25/matches?page=1&page_size=10")
    assert res2.status_code == 200
    assert res2.json()["total_matches"] == 74


@pytest.mark.unit
def test_legacy_test_alias_preservation():
    """Verifies that legacy test ID 'uncapped_rr_01' continues to function for backward test compatibility."""
    res_stats = client.get("/api/v1/domestic/players/uncapped_rr_01/season-stats")
    assert res_stats.status_code == 200
    stats = res_stats.json()
    assert len(stats) >= 1
    assert stats[0]["runs"] == 268

    res_ar = client.get("/api/v1/domestic/players/uncapped_rr_01/all-round-summary")
    assert res_ar.status_code == 200
    assert res_ar.json()["player_id"] == "uncapped_rr_01"
