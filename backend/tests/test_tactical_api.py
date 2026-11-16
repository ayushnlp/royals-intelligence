"""
Royals Intelligence - Tactical Analytics REST API Test Suite
Stage 5 Verification: End-to-end tests for /api/v1/analytics/tactical endpoints.
"""

import pytest


# ---------------------------------------------------------------------------
# 1. Dataset Tactical Summary
# ---------------------------------------------------------------------------

def test_get_tactical_summary(client):
    """Verifies GET /api/v1/analytics/tactical/summary returns official data counts."""
    response = client.get("/api/v1/analytics/tactical/summary")
    assert response.status_code == 200
    data = response.json()
    assert data["total_deliveries"] == 200999
    assert data["legal_deliveries"] == 192709
    assert data["total_matches_with_deliveries"] == 867
    assert data["total_unique_strikers"] == 888
    assert data["total_unique_bowlers"] == 647
    assert data["total_runs_off_bat"] == 269550
    assert data["total_wickets_fallen"] == 10881
    assert data["total_bowler_wickets"] == 10272
    assert "data_provenance" in data
    assert "generated_at" in data


# ---------------------------------------------------------------------------
# 2. Phase-wise Performance
# ---------------------------------------------------------------------------

def test_get_phase_performance_overall(client):
    """Verifies tournament-wide phase splits."""
    response = client.get("/api/v1/analytics/tactical/phases")
    assert response.status_code == 200
    data = response.json()
    assert "phases" in data
    assert "Powerplay" in data["phases"]
    assert "Middle" in data["phases"]
    assert "Death" in data["phases"]
    pp = data["phases"]["Powerplay"]
    assert pp["total_balls"] > 50000
    assert pp["dot_ball_percentage"] > 45.0


def test_get_phase_performance_batter(client):
    """Verifies phase splits for Jos Buttler (striker_id 813)."""
    response = client.get("/api/v1/analytics/tactical/phases?striker_id=813")
    assert response.status_code == 200
    data = response.json()
    assert data["striker_id"] == 813
    assert data["striker_name"] == "Jos Buttler"
    assert "phases" in data
    assert data["phases"]["Powerplay"]["runs"] > 800


def test_get_phase_performance_bowler(client):
    """Verifies phase splits for Yuzvendra Chahal (bowler_id 1612)."""
    response = client.get("/api/v1/analytics/tactical/phases?bowler_id=1612")
    assert response.status_code == 200
    data = response.json()
    assert data["bowler_id"] == 1612
    assert data["bowler_name"] == "Yuzvendra Chahal"
    assert "phases" in data
    assert data["phases"]["Middle"]["wickets"] > 70


def test_get_phase_performance_single_phase_filter(client):
    """Verifies filtering by single phase."""
    response = client.get("/api/v1/analytics/tactical/phases?phase=Powerplay")
    assert response.status_code == 200
    data = response.json()
    assert len(data["phases"]) == 1
    assert "Powerplay" in data["phases"]


def test_get_phase_performance_invalid_phase(client):
    """Verifies error handling for invalid phase parameter."""
    response = client.get("/api/v1/analytics/tactical/phases?phase=SuperOver")
    assert response.status_code == 400
    data = response.json()
    assert "Invalid phase" in data["detail"]


def test_get_phase_performance_conflicting_filters(client):
    """Verifies error handling when both striker_id and bowler_id are provided."""
    response = client.get("/api/v1/analytics/tactical/phases?striker_id=813&bowler_id=1612")
    assert response.status_code == 400
    data = response.json()
    assert "Cannot filter by both" in data["detail"]


def test_get_phase_performance_unknown_player(client):
    """Verifies 404 response for unknown player ID."""
    response = client.get("/api/v1/analytics/tactical/phases?striker_id=9999999")
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"].lower()


# ---------------------------------------------------------------------------
# 3. Stroke-wise Batting Efficiency
# ---------------------------------------------------------------------------

def test_get_stroke_efficiency_overall(client):
    """Verifies overall stroke efficiency ranking."""
    response = client.get("/api/v1/analytics/tactical/strokes?min_balls=100")
    assert response.status_code == 200
    data = response.json()
    assert data["total_strokes_analyzed"] >= 15
    strokes = [s["stroke"] for s in data["strokes"]]
    assert "Pull shot" in strokes
    assert "Cover Drive" in strokes


def test_get_stroke_efficiency_single_player(client):
    """Verifies stroke efficiency for Yashasvi Jaiswal (6819)."""
    response = client.get("/api/v1/analytics/tactical/strokes?striker_id=6819")
    assert response.status_code == 200
    data = response.json()
    assert data["striker_id"] == 6819
    assert data["striker_name"] == "Yashasvi Jaiswal"
    assert len(data["strokes"]) > 0


def test_get_stroke_efficiency_empty_result(client):
    """Verifies empty list returned when non-existent stroke is requested."""
    response = client.get("/api/v1/analytics/tactical/strokes?stroke=HelicopterBicycleKick")
    assert response.status_code == 200
    data = response.json()
    assert data["total_strokes_analyzed"] == 0
    assert data["strokes"] == []


def test_get_stroke_efficiency_invalid_param(client):
    """Verifies 422 for invalid negative min_balls."""
    response = client.get("/api/v1/analytics/tactical/strokes?min_balls=-10")
    assert response.status_code == 422


# ---------------------------------------------------------------------------
# 4. Handedness Matchup Matrix
# ---------------------------------------------------------------------------

def test_get_handedness_matrix_overall(client):
    """Verifies 4-way handedness matrix."""
    response = client.get("/api/v1/analytics/tactical/handedness")
    assert response.status_code == 200
    data = response.json()
    assert len(data["matrix"]) == 4
    combos = {(m["batting_type"], m["pace_or_spin"]) for m in data["matrix"]}
    assert ("RHB", "Pace") in combos
    assert ("RHB", "Spin") in combos
    assert ("LHB", "Pace") in combos
    assert ("LHB", "Spin") in combos


def test_get_handedness_matrix_filtered(client):
    """Verifies filtering by batting_type=LHB and pace_or_spin=Pace."""
    response = client.get("/api/v1/analytics/tactical/handedness?batting_type=LHB&pace_or_spin=Pace")
    assert response.status_code == 200
    data = response.json()
    assert len(data["matrix"]) == 1
    assert data["matrix"][0]["batting_type"] == "LHB"
    assert data["matrix"][0]["pace_or_spin"] == "Pace"


def test_get_handedness_matrix_invalid_params(client):
    """Verifies 400 response for invalid batting_type or pace_or_spin."""
    response = client.get("/api/v1/analytics/tactical/handedness?batting_type=AMBIDEXTROUS")
    assert response.status_code == 400

    response2 = client.get("/api/v1/analytics/tactical/handedness?pace_or_spin=KNUCKLE")
    assert response2.status_code == 400


# ---------------------------------------------------------------------------
# 5. Delivery Variations
# ---------------------------------------------------------------------------

def test_get_delivery_variations_overall(client):
    """Verifies bowling delivery variation rankings."""
    response = client.get("/api/v1/analytics/tactical/variations?min_balls=100")
    assert response.status_code == 200
    data = response.json()
    assert data["total_styles_analyzed"] >= 15
    styles = [s["delivery_style"] for s in data["styles"]]
    assert "Seamed In" in styles
    assert "Leg Break" in styles


def test_get_delivery_variations_bowler(client):
    """Verifies delivery variation breakdown for Trent Boult (2320)."""
    response = client.get("/api/v1/analytics/tactical/variations?bowler_id=2320")
    assert response.status_code == 200
    data = response.json()
    assert data["bowler_id"] == 2320
    assert data["bowler_name"] == "Trent Boult"
    assert len(data["styles"]) > 0


# ---------------------------------------------------------------------------
# 6. Speed Profiles & Sensor Safeguards
# ---------------------------------------------------------------------------

def test_get_speed_profiles_overall(client):
    """Verifies tournament-wide speed telemetry profile."""
    response = client.get("/api/v1/analytics/tactical/speed-profiles")
    assert response.status_code == 200
    data = response.json()
    assert data["overall_valid_speed_deliveries"] > 120000
    assert data["speed_coverage_pct"] > 60.0
    assert data["mean_speed_kmh"] > 110.0
    assert data["sensor_safeguards_applied"] is True
    assert "top_fastest_bowlers" in data
    assert len(data["top_fastest_bowlers"]) > 0


def test_get_speed_profiles_bowler(client):
    """Verifies speed profile for Arshdeep Singh (bowler_id 5328 or name check)."""
    # Prasidh Krishna (player_id 4489)
    response = client.get("/api/v1/analytics/tactical/speed-profiles?bowler_id=4489")
    assert response.status_code == 200
    data = response.json()
    assert data["bowler_id"] == 4489
    assert data["bowler_name"] == "Prasidh Krishna"
    assert data["sensor_safeguards_applied"] is True
    assert data["mean_speed_kmh"] > 130.0
    assert data["speed_brackets"]["express_over_140"] > 0


def test_get_speed_profiles_unknown_bowler(client):
    """Verifies 404 response for unknown bowler."""
    response = client.get("/api/v1/analytics/tactical/speed-profiles?bowler_id=9999999")
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# 7. Player Comprehensive Tactical Profile
# ---------------------------------------------------------------------------

def test_get_player_tactical_profile_batter(client):
    """Verifies complete tactical profile for Sanju Samson (2258)."""
    response = client.get("/api/v1/analytics/tactical/players/2258")
    assert response.status_code == 200
    data = response.json()
    assert data["player_id"] == 2258
    assert data["player_name"] == "Sanju Samson"
    assert data["is_batter"] is True
    assert data["batting_profile"] is not None
    assert "phase_splits" in data["batting_profile"]
    assert "top_strokes" in data["batting_profile"]


def test_get_player_tactical_profile_unknown(client):
    """Verifies 404 response for unknown player ID."""
    response = client.get("/api/v1/analytics/tactical/players/9999999")
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# 8. Death Overs (16–20) Rankings
# ---------------------------------------------------------------------------

def test_get_death_overs_rankings_all(client):
    """Verifies death overs rankings for both batting and bowling."""
    response = client.get("/api/v1/analytics/tactical/death-overs?discipline=all&limit=5")
    assert response.status_code == 200
    data = response.json()
    assert data["discipline"] == "all"
    assert len(data["batting_finishers"]) == 5
    assert len(data["bowling_containment"]) == 5

    # Check top finisher is Suryakumar Yadav
    assert data["batting_finishers"][0]["striker_name"] == "Suryakumar Yadav"
    assert data["batting_finishers"][0]["strike_rate"] > 200.0


def test_get_death_overs_rankings_invalid_discipline(client):
    """Verifies 400 for invalid discipline."""
    response = client.get("/api/v1/analytics/tactical/death-overs?discipline=fielding")
    assert response.status_code == 400


# ---------------------------------------------------------------------------
# 9. Head-to-Head Micro-Battles
# ---------------------------------------------------------------------------

def test_get_head_to_head_matchup(client):
    """Verifies Kohli (47) vs Rashid Khan (4722) head-to-head matchup."""
    response = client.get("/api/v1/analytics/tactical/matchups?striker_id=47&bowler_id=4722")
    assert response.status_code == 200
    data = response.json()
    assert data["striker_name"] == "Virat Kohli"
    assert data["bowler_name"] == "Rashid Khan"
    assert data["balls_faced"] == 76
    assert data["runs_scored"] >= 100
    assert data["strike_rate"] >= 140.0


def test_get_head_to_head_no_deliveries(client):
    """Verifies empty micro-battle profile when two players never faced each other."""
    # Yuzvendra Chahal (1612) as striker vs Trent Boult (2320) as bowler
    response = client.get("/api/v1/analytics/tactical/matchups?striker_id=1612&bowler_id=2320")
    assert response.status_code == 200
    data = response.json()
    assert data["balls_faced"] == 0
    assert data["runs_scored"] == 0
    assert data["dismissals"] == 0


def test_get_head_to_head_unknown_player(client):
    """Verifies 404 when either striker or bowler is unknown."""
    response = client.get("/api/v1/analytics/tactical/matchups?striker_id=9999999&bowler_id=4722")
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# 10. Player Search & Autocomplete
# ---------------------------------------------------------------------------

def test_search_players(client):
    """Verifies player search returns list of matching players."""
    response = client.get("/api/v1/analytics/tactical/players?query=samson")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    found = any(p["player_id"] == 2258 and "Samson" in p["player_name"] for p in data)
    assert found is True

