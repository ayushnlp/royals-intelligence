"""
Royals Intelligence - Uncapped Player Pressure Intelligence API Tests
Verifies uncapped leaderboards, eligibility audits, and separation from official Round 1.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture(scope="module")
def client():
    return TestClient(app)


def test_get_uncapped_overview(client):
    """Verifies uncapped overview counts and metadata."""
    response = client.get("/api/v1/analytics/uncapped/overview")
    assert response.status_code == 200
    data = response.json()
    assert data["total_verified_uncapped_batters"] >= 10
    assert data["total_verified_uncapped_bowlers"] >= 10
    assert data["top_uncapped_batter"] == "Ashutosh Sharma"
    assert data["top_uncapped_bowler"] == "Vaibhav Arora"


def test_get_uncapped_leaderboards_all(client):
    """Verifies combined uncapped leaderboards return verified domestic talents."""
    response = client.get("/api/v1/analytics/uncapped/leaderboards?discipline=all&limit=5")
    assert response.status_code == 200
    data = response.json()
    assert data["discipline_filter"] == "all"
    assert len(data["batting_leaderboard"]) == 5
    assert len(data["bowling_leaderboard"]) == 5

    # Check batting leader
    bat_leader = data["batting_leaderboard"][0]
    assert bat_leader["uncapped_rank"] == 1
    assert bat_leader["player_name"] == "Ashutosh Sharma"
    assert bat_leader["eligibility_status"] == "VERIFIED"

    # Check bowling leader
    bowl_leader = data["bowling_leaderboard"][0]
    assert bowl_leader["uncapped_rank"] == 1
    assert bowl_leader["player_name"] == "Vaibhav Arora"
    assert bowl_leader["eligibility_status"] == "VERIFIED"


def test_uncapped_eligibility_exclusion_legends(client):
    """Verifies that retired stars and senior capped players are excluded from uncapped status."""
    # MS Dhoni (ID 8)
    resp_dhoni = client.get("/api/v1/analytics/uncapped/eligibility/8")
    assert resp_dhoni.status_code == 200
    assert resp_dhoni.json()["eligibility_status"] == "NOT_ELIGIBLE"
    assert not resp_dhoni.json()["is_uncapped"]

    # Virat Kohli (ID 47)
    resp_kohli = client.get("/api/v1/analytics/uncapped/eligibility/47")
    assert resp_kohli.status_code == 200
    assert resp_kohli.json()["eligibility_status"] == "NOT_ELIGIBLE"

    # Jasprit Bumrah (ID 2933)
    resp_bumrah = client.get("/api/v1/analytics/uncapped/eligibility/2933")
    assert resp_bumrah.status_code == 200
    assert resp_bumrah.json()["eligibility_status"] == "NOT_ELIGIBLE"


def test_uncapped_eligibility_verified_talent(client):
    """Verifies that Ashutosh Sharma (ID 8101) is verified uncapped."""
    resp = client.get("/api/v1/analytics/uncapped/eligibility/8101")
    assert resp.status_code == 200
    assert resp.json()["eligibility_status"] == "VERIFIED"
    assert resp.json()["is_uncapped"] is True


def test_configurable_pressure_deliveries_threshold(client):
    """Verifies configurable pressure delivery thresholds (20, 30, 40, 50, 60)."""
    # 60 balls default
    res60 = client.get("/api/v1/analytics/uncapped/leaderboards?discipline=batting&limit=50&min_balls=60")
    assert res60.status_code == 200
    d60 = res60.json()
    assert d60["batting_count"] == 14
    assert not d60["is_exploratory_filter"]

    # 40 balls exploratory threshold
    res40 = client.get("/api/v1/analytics/uncapped/leaderboards?discipline=batting&limit=50&min_balls=40")
    assert res40.status_code == 200
    d40 = res40.json()
    assert d40["batting_count"] == 24
    assert d40["is_exploratory_filter"] is True
    # All players must have >= 40 pressure balls
    for player in d40["batting_leaderboard"]:
        assert player["pressure_legal_balls"] >= 40

    # 20 balls wide exploratory threshold
    res20 = client.get("/api/v1/analytics/uncapped/leaderboards?discipline=batting&limit=50&min_balls=20")
    assert res20.status_code == 200
    d20 = res20.json()
    assert d20["batting_count"] == 30
    assert d20["excluded_count"] == 0


def test_configurable_matches_threshold(client):
    """Verifies configurable matches played threshold (0, 20, 25, 50)."""
    # All matches (min_matches=0)
    res_all = client.get("/api/v1/analytics/uncapped/leaderboards?discipline=batting&limit=50&min_balls=20&min_matches=0")
    assert res_all.status_code == 200
    assert res_all.json()["batting_count"] == 30

    # 20 matches
    res_20m = client.get("/api/v1/analytics/uncapped/leaderboards?discipline=batting&limit=50&min_balls=20&min_matches=20")
    assert res_20m.status_code == 200
    d20m = res_20m.json()
    assert d20m["batting_count"] == 6
    assert d20m["is_exploratory_filter"] is True
    for p in d20m["batting_leaderboard"]:
        assert p["pressure_matches"] >= 20

    # 25 matches
    res_25m = client.get("/api/v1/analytics/uncapped/leaderboards?discipline=batting&limit=50&min_balls=20&min_matches=25")
    assert res_25m.status_code == 200
    assert res_25m.json()["batting_count"] == 2

    # 50 matches (strict, expected 0 for uncapped domestic talent)
    res_50m = client.get("/api/v1/analytics/uncapped/leaderboards?discipline=batting&limit=50&min_balls=20&min_matches=50")
    assert res_50m.status_code == 200
    assert res_50m.json()["batting_count"] == 0
    assert res_50m.json()["excluded_count"] == 30


def test_combined_sample_gate_and_overview(client):
    """Verifies combined independent filters and dynamic overview calculations."""
    res_ov = client.get("/api/v1/analytics/uncapped/overview?min_balls=40&min_matches=20")
    assert res_ov.status_code == 200
    data = res_ov.json()
    assert data["min_balls_applied"] == 40
    assert data["min_matches_applied"] == 20
    assert data["is_exploratory_filter"] is True
    assert data["total_verified_uncapped_batters"] == 6
    assert data["total_verified_uncapped_bowlers"] == 2
    assert data["excluded_batters_count"] == 24
    assert data["excluded_bowlers_count"] == 20
    assert "Exploratory Scouting Filter" in data["sample_gate_applied"]
    # Check top candidates remain valid
    assert data["top_uncapped_batter"] is not None
    assert data["top_uncapped_bowler"] is not None
