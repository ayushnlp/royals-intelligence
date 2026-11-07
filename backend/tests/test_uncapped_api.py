"""
Royals Intelligence - Uncapped API Integration Tests
Tests /api/v1/players, /api/v1/analytics, and /api/v1/proprietary endpoints.
"""

import pytest
from starlette.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_list_uncapped_players():
    """Tests GET /api/v1/players with and without filters."""
    response = client.get("/api/v1/players")
    assert response.status_code == 200
    players = response.json()
    assert isinstance(players, list)
    assert len(players) > 0

    # Filter by eligibility
    res_elig = client.get("/api/v1/players?eligibility=CONFIRMED_UNCAPPED")
    assert res_elig.status_code == 200
    for p in res_elig.json():
        assert p["eligibility_status"] == "CONFIRMED_UNCAPPED"

    # Filter by trialist
    res_trial = client.get("/api/v1/players?trialist_only=true")
    assert res_trial.status_code == 200
    for p in res_trial.json():
        assert p["is_rr_trialist"] is True


def test_get_uncapped_player_detail():
    """Tests GET /api/v1/players/{id}."""
    response = client.get("/api/v1/players/uncapped_rr_01")
    assert response.status_code == 200
    detail = response.json()
    assert detail["full_name"] == "Shashank Singh"
    assert detail["is_capped"] is False
    assert len(detail["identities"]) >= 1

    # Nonexistent
    res_404 = client.get("/api/v1/players/nonexistent_player_id")
    assert res_404.status_code == 404


def test_verify_player_eligibility():
    """Tests POST /api/v1/players/{id}/verify-eligibility."""
    payload = {
        "new_status": "CONFIRMED_UNCAPPED",
        "verification_notes": "Audited domestic scorecards. 0 senior caps confirmed.",
        "verified_by": "LEAD_ANALYST",
    }
    response = client.post("/api/v1/players/uncapped_rr_01/verify-eligibility", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["updated_status"] == "CONFIRMED_UNCAPPED"
    assert "Audited domestic" in data["verification_notes"]


def test_analytics_batting_and_bowling_endpoints():
    """Tests GET /api/v1/analytics/players/{id}/batting and bowling."""
    # Batting
    res_bat = client.get("/api/v1/analytics/players/uncapped_rr_01/batting")
    assert res_bat.status_code == 200
    bat = res_bat.json()
    assert bat["player_id"] == "uncapped_rr_01"
    assert "Powerplay" in bat["phase_splits"]
    assert "Death" in bat["phase_splits"]

    # Bowling
    res_bowl = client.get("/api/v1/analytics/players/uncapped_rr_03/bowling")
    assert res_bowl.status_code == 200
    bowl = res_bowl.json()
    assert bowl["player_id"] == "uncapped_rr_03"
    assert bowl["wickets"] > 0

    # Recent form
    res_form = client.get("/api/v1/analytics/players/uncapped_rr_01/recent-form?last_n=5&discipline=batting")
    assert res_form.status_code == 200


def test_proprietary_schema_discovery_and_evaluations():
    """Tests POST /api/v1/proprietary/discover-schema and GET /evaluations with security masking."""
    # Discover schema
    sample_payload = {
        "sample_rows": [
            {
                "player": "Test Batter",
                "birth_date": "2002-05-10",
                "state": "Rajasthan",
                "skill_rating": 8.0,
                "notes": "Good front foot drive."
            }
        ]
    }
    res_disc = client.post("/api/v1/proprietary/discover-schema", json=sample_payload)
    assert res_disc.status_code == 200
    disc = res_disc.json()
    assert "player" in disc["detected_columns"]

    # Evaluations masking test
    # 1. Public user
    res_pub = client.get("/api/v1/proprietary/evaluations/uncapped_rr_01", headers={"x-user-role": "public"})
    assert res_pub.status_code == 200
    evals_pub = res_pub.json()
    assert len(evals_pub) > 0
    assert "[RESTRICTED" in evals_pub[0]["proprietary_notes"]
    assert "[ANONYMIZED" in evals_pub[0]["scout_identifier"]

    # 2. RR Scout Admin
    res_admin = client.get("/api/v1/proprietary/evaluations/uncapped_rr_01", headers={"x-user-role": "rr_scout_admin"})
    assert res_admin.status_code == 200
    evals_admin = res_admin.json()
    assert "Immediate target" in evals_admin[0]["proprietary_notes"]
    assert evals_admin[0]["scout_identifier"] == "RR_SCOUT_DOMESTIC_NORTH"
