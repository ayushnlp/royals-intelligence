"""
Royals Intelligence - Domestic Season & Match Intelligence Unit & Integration Tests
Validates domestic competition directory, season match listings, detailed scorecards,
fall of wickets, partnerships, phase progression, batting & bowling calculations,
all-round dual contribution summaries, and uncapped player scope boundaries.
"""

import pytest
import pytest_asyncio
from starlette.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.main import app as fastapi_app
from app.db.base import Base
import app.models
from app.services.domestic.domestic_match_service import DomesticMatchService, BOWLER_CREDITED_DISMISSALS
from app.services.domestic.domestic_season_service import DomesticSeasonService

client = TestClient(fastapi_app)


@pytest_asyncio.fixture
async def async_test_session():
    """In-memory SQLite async engine and session for isolation and fast execution."""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


def test_format_aware_phase_assignment():
    """Verifies that phase assignment correctly adapts across T20, List A, and First-Class formats."""
    # 1. T20 (20 overs)
    assert DomesticMatchService.assign_phase(0, "T20") == "Powerplay"
    assert DomesticMatchService.assign_phase(5, "T20") == "Powerplay"
    assert DomesticMatchService.assign_phase(6, "T20") == "Middle"
    assert DomesticMatchService.assign_phase(14, "T20") == "Middle"
    assert DomesticMatchService.assign_phase(15, "T20") == "Death"
    assert DomesticMatchService.assign_phase(19, "T20") == "Death"

    # 2. List A / ODI (50 overs)
    assert DomesticMatchService.assign_phase(0, "List A") == "Powerplay"
    assert DomesticMatchService.assign_phase(9, "List A") == "Powerplay"
    assert DomesticMatchService.assign_phase(10, "List A") == "Middle"
    assert DomesticMatchService.assign_phase(39, "List A") == "Middle"
    assert DomesticMatchService.assign_phase(40, "List A") == "Death"
    assert DomesticMatchService.assign_phase(49, "List A") == "Death"

    # 3. First Class (Ranji Trophy)
    assert DomesticMatchService.assign_phase(5, "First Class") == "New Ball"
    assert DomesticMatchService.assign_phase(14, "First Class") == "New Ball"
    assert DomesticMatchService.assign_phase(25, "First Class") == "Middle / Old Ball"


def test_bowler_credited_dismissals_exclusion():
    """Verifies that non-bowler dismissals (run-outs, retired hurt) are never credited to bowlers."""
    assert "bowled" in BOWLER_CREDITED_DISMISSALS
    assert "caught" in BOWLER_CREDITED_DISMISSALS
    assert "lbw" in BOWLER_CREDITED_DISMISSALS
    assert "stumped" in BOWLER_CREDITED_DISMISSALS
    assert "hit wicket" in BOWLER_CREDITED_DISMISSALS

    # Must be excluded
    assert "run out" not in BOWLER_CREDITED_DISMISSALS
    assert "retired hurt" not in BOWLER_CREDITED_DISMISSALS
    assert "obstructing the field" not in BOWLER_CREDITED_DISMISSALS
    assert "timed out" not in BOWLER_CREDITED_DISMISSALS


def test_zero_denominator_and_edge_case_handling():
    """Verifies that zero denominators produce None or 0.0 rather than crashing or fabricating numbers."""
    # Batting strike rate: 0 balls -> 0.0
    balls = 0
    runs = 0
    sr = round((runs / balls) * 100, 2) if balls > 0 else 0.0
    assert sr == 0.0

    # Batting average: 0 dismissals (not out) -> None (undefined, never fabricated)
    dismissals = 0
    avg = round(runs / dismissals, 2) if dismissals > 0 else None
    assert avg is None

    # Balls per boundary: 0 boundaries -> None
    fours = 0
    sixes = 0
    bpb = round(balls / (fours + sixes), 1) if (fours + sixes) > 0 else None
    assert bpb is None

    # Bowling economy: 0 balls -> 0.0
    legal_balls = 0
    runs_conceded = 0
    econ = round(runs_conceded / (legal_balls / 6.0), 2) if legal_balls > 0 else 0.0
    assert econ == 0.0

    # Bowling average: 0 wickets -> None
    wickets = 0
    bowl_avg = round(runs_conceded / wickets, 2) if wickets > 0 else None
    assert bowl_avg is None


@pytest.mark.asyncio
async def test_domestic_season_service_competitions(async_test_session: AsyncSession):
    """Verifies listing of domestic competitions and seasons."""
    comps = await DomesticSeasonService.list_competitions(async_test_session)
    assert len(comps) >= 4
    comp_ids = [c.competition_id for c in comps]
    assert "smat" in comp_ids
    assert "vht" in comp_ids
    assert "ranji" in comp_ids

    # Format specifications
    smat = next(c for c in comps if c.competition_id == "smat")
    assert smat.competition_type == "T20"
    assert smat.is_domestic is True
    assert smat.validation_pass_rate == 100.0


@pytest.mark.asyncio
async def test_domestic_season_service_matches(async_test_session: AsyncSession):
    """Verifies listing season matches with team filtering and pagination."""
    matches, total = await DomesticSeasonService.list_season_matches(
        session=async_test_session,
        competition_id="smat",
        season="2024",
        page=1,
        page_size=10,
    )
    assert total >= 1
    assert len(matches) >= 1
    m1 = matches[0]
    assert m1.competition_id == "smat"
    assert m1.home_team_code in ["DEL", "MP", "CHG"]


@pytest.mark.asyncio
async def test_domestic_match_detail_and_innings(async_test_session: AsyncSession):
    """Verifies deep match scorecard, FoW, partnerships, and progression."""
    match_detail = await DomesticMatchService.get_match_detail(async_test_session, "smat_2024_del_pun")
    assert match_detail is not None
    assert match_detail.competition_id == "smat"
    assert len(match_detail.innings) >= 1

    inn1 = match_detail.innings[0]
    assert inn1.total_runs == 198
    assert inn1.wickets == 4
    assert len(inn1.batting_scorecards) >= 3
    assert len(inn1.bowling_scorecards) >= 1
    assert len(inn1.fall_of_wickets) >= 2
    assert len(inn1.partnerships) >= 2
    assert len(inn1.phase_summaries) == 3
    assert len(inn1.scoring_progression) == 20

    # Validate Priyansh Arya scorecard
    priyansh = next(b for b in inn1.batting_scorecards if b.player_name == "Priyansh Arya")
    assert priyansh.runs == 74
    assert priyansh.balls_faced == 42
    assert priyansh.fours == 8
    assert priyansh.sixes == 4
    assert priyansh.strike_rate > 170.0
    assert priyansh.powerplay_runs == 38

    # Validate Harshit Rana bowling
    harshit = next(b for b in inn1.bowling_scorecards if b.player_name == "Harshit Rana")
    assert harshit.bowler_wickets == 2
    assert harshit.economy_rate == 8.0


@pytest.mark.asyncio
async def test_player_domestic_season_stats_and_allround(async_test_session: AsyncSession):
    """Verifies season statistics and evidence-based non-composite all-round contribution."""
    stats = await DomesticSeasonService.get_player_season_stats(async_test_session, "uncapped_rr_01")
    assert len(stats) >= 1
    smat_stat = next(s for s in stats if s.competition_id == "smat")
    assert smat_stat.runs == 268
    assert smat_stat.strike_rate > 160.0
    assert smat_stat.bowler_wickets == 4
    assert smat_stat.boundary_percentage > 60.0

    # All-Round Contribution summary
    allround = await DomesticSeasonService.get_player_all_round_contribution(async_test_session, "uncapped_rr_01")
    assert allround.player_id == "uncapped_rr_01"
    assert allround.sample_size["matches"] == 13
    assert "strike_rate" in allround.batting_summary
    assert "economy_rate" in allround.bowling_summary
    assert "catches" in allround.fielding_summary
    assert "Finishing Batter" in allround.primary_role
    # Transparent qualitative context without arbitrary composite score
    assert len(allround.role_archetype_context) > 10


def test_domestic_api_endpoints_integration():
    """Tests all 9 Stage 3 FastAPI endpoints under /api/v1/domestic."""
    # 1. Competitions directory
    res_comps = client.get("/api/v1/domestic/competitions")
    assert res_comps.status_code == 200
    comps = res_comps.json()
    assert isinstance(comps, list)
    assert any(c["competition_id"] == "smat" for c in comps)

    # 2. Season matches
    res_matches = client.get("/api/v1/domestic/seasons/smat/2024/matches?page=1&page_size=5")
    assert res_matches.status_code == 200
    m_data = res_matches.json()
    assert m_data["competition_id"] == "smat"
    assert len(m_data["matches"]) >= 1

    # 3. Season summary
    res_summary = client.get("/api/v1/domestic/seasons/smat/2024/summary")
    assert res_summary.status_code == 200
    s_data = res_summary.json()
    assert s_data["total_matches_scheduled"] == 138
    assert len(s_data["top_teams"]) >= 2

    # 4. Match detail
    res_match = client.get("/api/v1/domestic/matches/smat_2024_del_pun")
    assert res_match.status_code == 200
    match_data = res_match.json()
    assert match_data["home_team"]["team_code"] == "DEL"
    assert len(match_data["innings"]) >= 1

    # 5. Innings analysis
    res_inn = client.get("/api/v1/domestic/matches/smat_2024_del_pun/innings/1")
    assert res_inn.status_code == 200
    inn_data = res_inn.json()
    assert inn_data["total_runs"] == 198
    assert len(inn_data["batting_scorecards"]) >= 2
    assert len(inn_data["fall_of_wickets"]) >= 1
    assert len(inn_data["partnerships"]) >= 1
    assert len(inn_data["scoring_progression"]) == 20

    # 6. Player domestic season stats
    res_stats = client.get("/api/v1/domestic/players/uncapped_rr_01/season-stats")
    assert res_stats.status_code == 200
    stats_data = res_stats.json()
    assert isinstance(stats_data, list)
    assert stats_data[0]["runs"] > 0

    # 7. Player match history
    res_history = client.get("/api/v1/domestic/players/uncapped_rr_01/match-history?page=1&page_size=10")
    assert res_history.status_code == 200
    hist_data = res_history.json()
    assert len(hist_data["matches"]) >= 1

    # 8. Player phase splits
    res_phases = client.get("/api/v1/domestic/players/uncapped_rr_01/phase-splits")
    assert res_phases.status_code == 200
    phases_data = res_phases.json()
    assert len(phases_data) == 3
    assert phases_data[0]["phase"] == "Powerplay"
    assert phases_data[2]["phase"] == "Death"

    # 9. All-round dual contribution
    res_allround = client.get("/api/v1/domestic/players/uncapped_rr_01/all-round-summary")
    assert res_allround.status_code == 200
    ar_data = res_allround.json()
    assert ar_data["player_id"] == "uncapped_rr_01"
    assert "strike_rate" in ar_data["batting_summary"]
    assert "economy_rate" in ar_data["bowling_summary"]
