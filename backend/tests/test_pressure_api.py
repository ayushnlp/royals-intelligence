"""
Royals Intelligence - Pressure Analytics API Test Suite
Verifies the locked Round 1 Pressure Analytics REST endpoints against the official dataset.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as test_client:
        yield test_client


# ---------------------------------------------------------------------------
# 1. Overview Endpoint Tests
# ---------------------------------------------------------------------------

def test_get_pressure_overview(client):
    """Verifies Round 1 overview metadata and volume counts."""
    response = client.get("/api/v1/analytics/pressure/overview")
    assert response.status_code == 200
    data = response.json()
    assert data["total_deliveries"] == 200999
    assert data["legal_deliveries"] == 192709
    assert data["matches_with_deliveries"] == 867
    assert data["reconciled_abandoned_matches"] == 16
    assert data["strict_pressure_bowling_balls"] == 37014
    assert data["strict_pressure_batting_balls"] == 31163
    assert data["death_overs_bowling_pressure_share_pct"] > 87.0
    assert data["death_overs_batting_pressure_share_pct"] > 78.0


# ---------------------------------------------------------------------------
# 2. Leaderboards Endpoint Tests
# ---------------------------------------------------------------------------

def test_get_pressure_leaderboards_all(client):
    """Verifies combined leaderboards response returns both batting and bowling."""
    response = client.get("/api/v1/analytics/pressure/leaderboards?discipline=all&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert data["discipline_filter"] == "all"
    assert data["batting_count"] == 10
    assert data["bowling_count"] == 10
    assert len(data["batting_leaderboard"]) == 10
    assert len(data["bowling_leaderboard"]) == 10


def test_get_pressure_leaderboard_batting_ranks(client):
    """Verifies Top 10 Batters Under Pressure match the sealed competition rankings."""
    response = client.get("/api/v1/analytics/pressure/leaderboards?discipline=batting&limit=10")
    assert response.status_code == 200
    data = response.json()
    batting = data["batting_leaderboard"]
    assert len(batting) == 10

    # Rank 1: Nicholas Pooran (3125)
    assert batting[0]["rank"] == 1
    assert batting[0]["player_id"] == 3125
    assert batting[0]["player_name"] == "Nicholas Pooran"
    assert batting[0]["conservative_pri"] > 2.0  # +2.25 SR pts

    # Rank 2: Donovan Ferreira (8182)
    assert batting[1]["rank"] == 2
    assert batting[1]["player_id"] == 8182
    assert batting[1]["player_name"] == "Donovan Ferreira"
    assert batting[1]["conservative_pri"] > 0.5  # +0.94 SR pts

    # Rank 3: Tim David (6396)
    assert batting[2]["rank"] == 3
    assert batting[2]["player_id"] == 6396
    assert batting[2]["player_name"] == "Tim David"

    # Rank 4: Dinesh Karthik (143)
    assert batting[3]["rank"] == 4
    assert batting[3]["player_id"] == 143
    assert batting[3]["player_name"] == "Dinesh Karthik"


def test_get_pressure_leaderboard_bowling_ranks(client):
    """Verifies Top 10 Bowlers Under Pressure match the sealed competition rankings."""
    response = client.get("/api/v1/analytics/pressure/leaderboards?discipline=bowling&limit=10")
    assert response.status_code == 200
    data = response.json()
    bowling = data["bowling_leaderboard"]
    assert len(bowling) == 10

    # Rank 1: Jasprit Bumrah (2933)
    assert bowling[0]["rank"] == 1
    assert bowling[0]["player_id"] == 2933
    assert bowling[0]["player_name"] == "Jasprit Bumrah"
    assert bowling[0]["conservative_runs_saved"] == -0.16

    # Rank 2: Sunil Narine (781)
    assert bowling[1]["rank"] == 2
    assert bowling[1]["player_id"] == 781
    assert bowling[1]["player_name"] == "Sunil Narine"

    # Rank 3: Maheesh Theekshana (19316)
    assert bowling[2]["rank"] == 3
    assert bowling[2]["player_id"] == 19316
    assert bowling[2]["player_name"] == "Maheesh Theekshana"

    # Rank 4: Matheesha Pathirana (8661)
    assert bowling[3]["rank"] == 4
    assert bowling[3]["player_id"] == 8661
    assert bowling[3]["player_name"] == "Matheesha Pathirana"


def test_get_pressure_leaderboard_invalid_discipline(client):
    """Verifies 400 Bad Request for unrecognized discipline."""
    response = client.get("/api/v1/analytics/pressure/leaderboards?discipline=fielding")
    assert response.status_code == 400


# ---------------------------------------------------------------------------
# 3. Candidate Profile Tests
# ---------------------------------------------------------------------------

def test_get_candidate_profile_pooran(client):
    """Verifies complete candidate evidence profile for Nicholas Pooran (3125)."""
    response = client.get("/api/v1/analytics/pressure/candidates/3125?discipline=batting")
    assert response.status_code == 200
    data = response.json()
    assert data["player_id"] == 3125
    assert data["player_name"] == "Nicholas Pooran"
    assert data["rank"] == 1
    assert data["discipline"] == "batting"
    assert data["governing_metric_value"] > 2.0
    assert "evidence_questions" in data
    assert "Ranked #1 in Batting" in data["evidence_questions"]["q1_why_considered"]
    assert data["evidence_questions"]["q6_conservative_diagnostic"] != ""


def test_get_candidate_profile_bumrah(client):
    """Verifies complete candidate evidence profile for Jasprit Bumrah (2933)."""
    response = client.get("/api/v1/analytics/pressure/candidates/2933?discipline=bowling")
    assert response.status_code == 200
    data = response.json()
    assert data["player_id"] == 2933
    assert data["player_name"] == "Jasprit Bumrah"
    assert data["rank"] == 1
    assert data["discipline"] == "bowling"
    assert data["governing_metric_value"] == -0.16
    assert "evidence_questions" in data
    assert "q1_why_considered" in data["evidence_questions"]


def test_get_candidate_profile_unknown_player(client):
    """Verifies 404 response for unknown candidate ID."""
    response = client.get("/api/v1/analytics/pressure/candidates/9999999")
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# 4. Methodology Endpoint Tests
# ---------------------------------------------------------------------------

def test_get_pressure_methodology(client):
    """Verifies methodology endpoint returns 12-cell matrix and formulas."""
    response = client.get("/api/v1/analytics/pressure/methodology")
    assert response.status_code == 200
    data = response.json()
    assert len(data["baseline_strata_12_cell"]) == 12
    assert "bayesian_shrinkage_formulation" in data
    assert "conservative_pri_formula" in data
    assert len(data["limitations"]) >= 4
