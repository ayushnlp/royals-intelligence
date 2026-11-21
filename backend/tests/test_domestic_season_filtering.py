import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.mark.data_dependent
def test_available_seasons_endpoint():
    """Verifies that GET /api/v1/domestic/seasons returns dynamic verified seasons descending."""
    res = client.get("/api/v1/domestic/seasons")
    assert res.status_code == 200
    seasons = res.json()
    assert len(seasons) >= 4
    season_keys = [s["season"] for s in seasons]
    assert season_keys[:4] == ["2026", "2025", "2024", "2023"]
    for s in seasons:
        assert s["has_data"] is True
        assert s["total_matches"] >= 100
        assert s["competition_count"] >= 20

@pytest.mark.data_dependent
def test_competitions_filtering_by_season_2026():
    """Verifies that selecting 2026 returns all 2026 verified competition records."""
    res = client.get("/api/v1/domestic/competitions?season=2026")
    assert res.status_code == 200
    comps = res.json()
    assert len(comps) == 23
    # First card is IPL
    c = comps[0]
    assert c["competition_id"] == "ipl"
    assert c["season"] == "2026"
    assert c["match_count"] == 74
    assert c["has_ball_by_ball"] is True
    # All cards strictly belong to 2026
    for comp in comps:
        assert comp["season"] == "2026"
        assert comp["match_count"] > 0

@pytest.mark.data_dependent
def test_competitions_filtering_by_season_2024():
    """Verifies that selecting 2024 returns all verified competitions for 2024 including feeder circuits."""
    res = client.get("/api/v1/domestic/competitions?season=2024")
    assert res.status_code == 200
    comps = res.json()
    assert len(comps) == 37
    for c in comps:
        assert c["season"] == "2024"
    comp_ids = {c["competition_id"] for c in comps}
    assert {"ipl", "smat", "vht", "ranji", "dpl", "2670"}.issubset(comp_ids)

@pytest.mark.data_dependent
def test_competitions_filtering_by_season_2025():
    """Verifies that selecting 2025 returns all 2025 verified competition records."""
    res = client.get("/api/v1/domestic/competitions?season=2025")
    assert res.status_code == 200
    comps = res.json()
    assert len(comps) == 32
    assert comps[0]["competition_id"] == "ipl"
    assert comps[0]["season"] == "2025"
    assert comps[0]["match_count"] == 75
    for c in comps:
        assert c["season"] == "2025"
    comp_ids = {c["competition_id"] for c in comps}
    assert "3289" in comp_ids  # Asia Cup Rising Stars

@pytest.mark.data_dependent
def test_competitions_filtering_by_season_2023():
    """Verifies that selecting 2023 returns all 2023 verified competition records."""
    res = client.get("/api/v1/domestic/competitions?season=2023")
    assert res.status_code == 200
    comps = res.json()
    assert len(comps) == 20
    assert comps[0]["competition_id"] == "ipl"
    assert comps[0]["season"] == "2023"
    assert comps[0]["match_count"] == 74
    for c in comps:
        assert c["season"] == "2023"

@pytest.mark.data_dependent
def test_competitions_filtering_unsupported_season():
    """Verifies that an unsupported season returns empty list."""
    res = client.get("/api/v1/domestic/competitions?season=2030")
    assert res.status_code == 200
    assert res.json() == []

@pytest.mark.data_dependent
def test_no_leak_of_2024_matches_into_2026_smat():
    """Verifies that SMAT matches are not leaked into 2026."""
    res = client.get("/api/v1/domestic/seasons/smat/2026/matches")
    assert res.status_code == 200
    data = res.json()
    assert data["total_matches"] == 0
    assert data["matches"] == []

@pytest.mark.data_dependent
def test_ipl_2026_matches_accessible():
    """Verifies that IPL matches are correctly retrieved for season 2026."""
    res = client.get("/api/v1/domestic/seasons/ipl/2026/matches?page=1&page_size=10")
    assert res.status_code == 200
    data = res.json()
    assert data["total_matches"] == 74
    assert len(data["matches"]) == 10
    for m in data["matches"]:
        assert m["season"] == "2026"
        assert m["competition_id"] == "ipl"

@pytest.mark.data_dependent
def test_non_ipl_competition_matches_accessible():
    """Verifies that non-IPL competitions in matches.csv are retrievable by comp_id."""
    res = client.get("/api/v1/domestic/seasons/3126/2026/matches")
    assert res.status_code == 200
    data = res.json()
    assert data["total_matches"] == 5
    assert len(data["matches"]) == 5
    for m in data["matches"]:
        assert m["season"] == "2026"

    res_emerging = client.get("/api/v1/domestic/seasons/2670/2024/matches")
    assert res_emerging.status_code == 200
    data_e = res_emerging.json()
    assert data_e["total_matches"] == 15
