"""
Royals Intelligence - Uncapped API Integration Tests
Tests /api/v1/players, /api/v1/analytics, and /api/v1/proprietary endpoints,
including server-side authentication, deny-by-default RBAC, forged header rejection,
and configurable reference date age calculation.
"""

import pytest
from starlette.testclient import TestClient
from app.main import app
from app.core.config import settings

client = TestClient(app)

ADMIN_HEADERS = {"Authorization": f"Bearer {settings.SCOUT_ADMIN_API_KEY}"}
ANALYST_HEADERS = {"Authorization": f"Bearer {settings.LEAD_ANALYST_API_KEY}"}


@pytest.mark.unit
def test_list_uncapped_players():
    """Tests GET /api/v1/players with and without filters, and with dynamic reference date."""
    # 1. Base query without confirmed reference date -> Age is unresolved (None)
    response = client.get("/api/v1/players")
    assert response.status_code == 200
    players = response.json()
    assert isinstance(players, list)
    assert len(players) > 0
    # Confirm default is unresolved (None) when official rule reference date is unconfirmed
    assert players[0]["calculated_age"] is None

    # 2. Query with explicit confirmed reference date -> Dynamically calculates fractional age
    res_with_ref = client.get("/api/v1/players?reference_date=2026-11-18")
    assert res_with_ref.status_code == 200
    players_ref = res_with_ref.json()
    shashank = next((p for p in players_ref if p["full_name"] == "Shashank Singh"), None)
    assert shashank is not None
    assert shashank["calculated_age"] is not None
    assert 34.8 <= shashank["calculated_age"] <= 35.2

    # 3. Missing DOB player with reference date -> Age remains None (never fabricates DOB)
    vipraj = next((p for p in players_ref if p["full_name"] == "Vipraj Nigam"), None)
    assert vipraj is not None
    assert vipraj["dob"] is None
    assert vipraj["calculated_age"] is None

    # 4. Filter by eligibility
    res_elig = client.get("/api/v1/players?eligibility=CONFIRMED_UNCAPPED")
    assert res_elig.status_code == 200
    for p in res_elig.json():
        assert p["eligibility_status"] == "CONFIRMED_UNCAPPED"

    # 5. Filter by trialist
    res_trial = client.get("/api/v1/players?trialist_only=true")
    assert res_trial.status_code == 200
    for p in res_trial.json():
        assert p["is_rr_trialist"] is True


@pytest.mark.unit
def test_get_uncapped_player_detail():
    """Tests GET /api/v1/players/{id} with and without reference date."""
    # Without reference date
    response = client.get("/api/v1/players/uncapped_rr_01")
    assert response.status_code == 200
    detail = response.json()
    assert detail["full_name"] == "Shashank Singh"
    assert detail["is_capped"] is False
    assert len(detail["identities"]) >= 1
    assert detail["calculated_age"] is None

    # With reference date
    res_dated = client.get("/api/v1/players/uncapped_rr_01?reference_date=2026-12-01")
    assert res_dated.status_code == 200
    detail_dated = res_dated.json()
    assert detail_dated["calculated_age"] is not None
    assert detail_dated["reference_date_used"] == "2026-12-01"

    # Nonexistent
    res_404 = client.get("/api/v1/players/nonexistent_player_id")
    assert res_404.status_code == 404


@pytest.mark.unit
def test_verify_player_eligibility_authorization():
    """Verifies that eligibility modification requires server-side admin credentials."""
    payload = {
        "new_status": "CONFIRMED_UNCAPPED",
        "verification_notes": "Audited domestic scorecards. 0 senior caps confirmed.",
        "verified_by": "RR_SCOUT_LEAD",
    }

    # 1. Anonymous request -> 401 Unauthorized
    res_anon = client.post("/api/v1/players/uncapped_rr_01/verify-eligibility", json=payload)
    assert res_anon.status_code == 401

    # 2. Forged client header without credentials -> 401 Unauthorized
    res_forged = client.post(
        "/api/v1/players/uncapped_rr_01/verify-eligibility",
        json=payload,
        headers={"x-user-role": "rr_scout_admin"}
    )
    assert res_forged.status_code == 401

    # 3. Valid Scout Admin credentials -> 200 OK
    res_admin = client.post(
        "/api/v1/players/uncapped_rr_01/verify-eligibility",
        json=payload,
        headers=ADMIN_HEADERS
    )
    assert res_admin.status_code == 200
    data = res_admin.json()
    assert data["updated_status"] == "CONFIRMED_UNCAPPED"
    assert "Audited domestic" in data["verification_notes"]


@pytest.mark.unit
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


@pytest.mark.unit
def test_proprietary_endpoints_security_and_masking():
    """Tests authentication enforcement and confidential data masking across proprietary endpoints."""
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

    # 1. Discover Schema: Anonymous rejected (401)
    res_disc_anon = client.post("/api/v1/proprietary/discover-schema", json=sample_payload)
    assert res_disc_anon.status_code == 401

    # 2. Discover Schema: Forged header rejected (401)
    res_disc_forged = client.post(
        "/api/v1/proprietary/discover-schema",
        json=sample_payload,
        headers={"x-user-role": "rr_scout_admin"}
    )
    assert res_disc_forged.status_code == 401

    # 3. Discover Schema: Authenticated scout admin succeeded (200)
    res_disc_auth = client.post(
        "/api/v1/proprietary/discover-schema",
        json=sample_payload,
        headers=ADMIN_HEADERS
    )
    assert res_disc_auth.status_code == 200
    disc = res_disc_auth.json()
    assert "player" in disc["detected_columns"]

    # 4. Ingest Pack: Anonymous rejected (401)
    ingest_payload = {
        "records": [
            {
                "player_name": "New Uncapped Prospect",
                "dob": "2003-04-12",
                "state_association": "Rajasthan",
            }
        ]
    }
    res_ingest_anon = client.post("/api/v1/proprietary/ingest-pack", json=ingest_payload)
    assert res_ingest_anon.status_code == 401

    # 5. Ingest Pack: Forged header rejected (401)
    res_ingest_forged = client.post(
        "/api/v1/proprietary/ingest-pack",
        json=ingest_payload,
        headers={"x-user-role": "rr_scout_admin"}
    )
    assert res_ingest_forged.status_code == 401

    # 6. Ingest Pack: Authenticated scout admin succeeded (200)
    res_ingest_auth = client.post(
        "/api/v1/proprietary/ingest-pack",
        json=ingest_payload,
        headers=ADMIN_HEADERS
    )
    assert res_ingest_auth.status_code == 200

    # 7. Evaluations Masking: Anonymous user receives strictly masked confidential data
    res_pub = client.get("/api/v1/proprietary/evaluations/uncapped_rr_01")
    assert res_pub.status_code == 200
    evals_pub = res_pub.json()
    assert len(evals_pub) > 0
    assert "[RESTRICTED" in evals_pub[0]["proprietary_notes"]
    assert "[ANONYMIZED" in evals_pub[0]["scout_identifier"]

    # 8. Evaluations Masking: Forged role header without token is rejected or masked
    res_forged_eval = client.get(
        "/api/v1/proprietary/evaluations/uncapped_rr_01",
        headers={"x-user-role": "rr_scout_admin"}
    )
    assert res_forged_eval.status_code == 401  # Forged privileged header rejected

    # 9. Evaluations Masking: Authenticated RR Scout Admin receives full unmasked view
    res_admin = client.get(
        "/api/v1/proprietary/evaluations/uncapped_rr_01",
        headers=ADMIN_HEADERS
    )
    assert res_admin.status_code == 200
    evals_admin = res_admin.json()
    assert "Immediate target" in evals_admin[0]["proprietary_notes"]
    assert evals_admin[0]["scout_identifier"] == "RR_SCOUT_DOMESTIC_NORTH"
