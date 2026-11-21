"""
Royals Intelligence - Match-Specific Scorecard Data Integrity Tests
Comprehensive regression tests ensuring authentic match-identity binding, dynamic scorecards,
accurate phase calculations, and prevention of repeated mock scorecards.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.domestic.domestic_match_service import DomesticMatchService


@pytest.fixture
def client():
    return TestClient(app)


@pytest.mark.data_integrity
def test_two_different_match_ids_return_different_metadata(client):
    """Verifies that two different match IDs return different match-specific metadata."""
    # Match 14094: CSK vs KKR (IPL 2022)
    # Match 14098: SRH vs RR (IPL 2022)
    res_1 = client.get("/api/v1/domestic/matches/14094")
    res_2 = client.get("/api/v1/domestic/matches/14098")

    assert res_1.status_code == 200
    assert res_2.status_code == 200

    data_1 = res_1.json()
    data_2 = res_2.json()

    # Different match IDs
    assert data_1["match_id"] == "14094"
    assert data_2["match_id"] == "14098"

    # Different teams
    assert data_1["home_team"]["name"] == "Chennai Super Kings"
    assert data_1["away_team"]["name"] == "Kolkata Knight Riders"

    assert data_2["home_team"]["name"] == "Sunrisers Hyderabad"
    assert data_2["away_team"]["name"] == "Rajasthan Royals"

    # Different dates
    assert data_1["match_date"] != data_2["match_date"]


@pytest.mark.data_integrity
def test_each_response_contains_requested_match_id(client):
    """Verifies that each response contains exactly the requested match ID."""
    test_ids = ["13511", "13522", "14095", "19556", "28960"]
    for mid in test_ids:
        res = client.get(f"/api/v1/domestic/matches/{mid}")
        assert res.status_code == 200
        assert res.json()["match_id"] == mid


@pytest.mark.data_integrity
def test_batting_and_bowling_teams_match_selected_match(client):
    """Verifies that batting and bowling teams match the selected match."""
    # Match 14095: Mumbai Indians 174/5 vs Delhi Capitals 168/6
    res = client.get("/api/v1/domestic/matches/14095")
    assert res.status_code == 200
    data = res.json()

    assert data["home_team"]["name"] == "Delhi Capitals"
    assert data["away_team"]["name"] == "Mumbai Indians"

    inn1 = data["innings"][0]
    assert inn1["batting_team_name"] == "Mumbai Indians"
    assert inn1["bowling_team_name"] == "Delhi Capitals"

    inn2 = data["innings"][1]
    assert inn2["batting_team_name"] == "Delhi Capitals"
    assert inn2["bowling_team_name"] == "Mumbai Indians"


@pytest.mark.data_integrity
def test_innings_totals_reconcile_with_actual_source_records(client):
    """Verifies that innings totals reconcile with raw deliveries and matches.csv."""
    # Match 14094: CSK vs KKR
    res = client.get("/api/v1/domestic/matches/14094")
    assert res.status_code == 200
    data = res.json()

    inn1 = data["innings"][0]
    inn2 = data["innings"][1]

    # CSK scored 125/5 in 20.0 overs
    assert inn1["total_runs"] == 125
    assert inn1["wickets"] == 5
    assert inn1["overs_completed"] == 20.0

    # KKR scored 129/4 in 18.3 overs
    assert inn2["total_runs"] == 129
    assert inn2["wickets"] == 4
    assert inn2["overs_completed"] == 18.3


@pytest.mark.data_integrity
def test_phase_totals_calculated_from_correct_match_deliveries(client):
    """Verifies that phase totals are derived strictly from the match's actual deliveries."""
    # Match 14098: RR 196/6 vs SRH 139/7
    res = client.get("/api/v1/domestic/matches/14098")
    assert res.status_code == 200
    data = res.json()

    inn1_phases = {p["phase_name"]: p for p in data["innings"][0]["phase_summaries"]}
    # RR Innings 1: Powerplay 53/0, Middle 85/3, Death 58/3 -> total runs = 196, total wkts = 6
    assert inn1_phases["Powerplay"]["runs"] == 53
    assert inn1_phases["Powerplay"]["wickets"] == 0
    assert inn1_phases["Middle"]["runs"] == 85
    assert inn1_phases["Middle"]["wickets"] == 3
    assert inn1_phases["Death"]["runs"] == 58
    assert inn1_phases["Death"]["wickets"] == 3

    assert (
        inn1_phases["Powerplay"]["runs"]
        + inn1_phases["Middle"]["runs"]
        + inn1_phases["Death"]["runs"]
    ) == data["innings"][0]["total_runs"]


@pytest.mark.data_integrity
def test_missing_scorecard_data_produces_clear_unavailable_state(client):
    """Verifies that an abandoned match without deliveries returns 0 innings with clear status."""
    # Match 32610: England vs Pakistan (Abandoned)
    res = client.get("/api/v1/domestic/matches/32610")
    assert res.status_code == 200
    data = res.json()

    assert data["match_id"] == "32610"
    assert len(data["innings"]) == 0
    assert data["data_provenance"]["ball_by_ball_available"] is False
    assert "Abandoned" in data["win_margin"]


@pytest.mark.data_integrity
def test_invalid_match_ids_never_return_another_match_scorecard(client):
    """Verifies that invalid or nonexistent match IDs return 404 rather than an unrelated scorecard."""
    invalid_ids = ["invalid_match_9999", "non_existent_fixture", "fake_id_12345"]
    for inv in invalid_ids:
        res = client.get(f"/api/v1/domestic/matches/{inv}")
        assert res.status_code == 404, f"Expected 404 for {inv}, got {res.status_code}"
        err = res.json()["detail"]
        assert "not found" in err.lower()


@pytest.mark.data_integrity
def test_regression_against_repeated_delhi_punjab_scorecard(client):
    """
    CRITICAL REGRESSION TEST:
    Ensures that non-Delhi/Punjab matches never receive the Delhi vs Punjab 198/4 scorecard.
    """
    # Test across multiple distinct matches from different competitions and seasons
    sample_matches = ["13511", "13512", "13612", "14094", "14096", "14097", "14098", "19556", "28960", "41849"]

    for mid in sample_matches:
        res = client.get(f"/api/v1/domestic/matches/{mid}")
        assert res.status_code == 200
        data = res.json()

        # None of these matches should have home_team="Delhi" AND away_team="Punjab" AND inn1=198/4
        is_del_pun = (
            data["home_team"]["name"] == "Delhi"
            and data["away_team"]["name"] == "Punjab"
            and len(data["innings"]) > 0
            and data["innings"][0]["total_runs"] == 198
        )
        assert not is_del_pun, f"Match {mid} incorrectly received the repeated Delhi vs Punjab 198/4 scorecard!"


@pytest.mark.data_integrity
def test_multiple_competitions_and_seasons_work_independently(client):
    """Verifies that scorecards across multiple competitions and seasons work independently."""
    # 2022 T20I (West Indies vs England)
    res_2022 = client.get("/api/v1/domestic/matches/13511")
    # 2023 T20I (India vs Sri Lanka)
    res_2023 = client.get("/api/v1/domestic/matches/19556")
    # 2024 T20I (India vs Afghanistan)
    res_2024 = client.get("/api/v1/domestic/matches/28960")
    # 2026 T20I (South Africa vs West Indies)
    res_2026 = client.get("/api/v1/domestic/matches/41849")

    assert res_2022.status_code == 200
    assert res_2023.status_code == 200
    assert res_2024.status_code == 200
    assert res_2026.status_code == 200

    d_2022 = res_2022.json()
    d_2023 = res_2023.json()
    d_2024 = res_2024.json()
    d_2026 = res_2026.json()

    assert d_2022["season"] == "2022"
    assert d_2023["season"] == "2023"
    assert d_2024["season"] == "2024"
    assert d_2026["season"] == "2026"

    # All should have distinct teams and scorecards
    assert d_2022["home_team"]["name"] != d_2023["home_team"]["name"]
    assert d_2023["home_team"]["name"] != d_2026["home_team"]["name"]
