"""
Royals Intelligence - Analytics Foundation Unit Tests
Validates calculation of batting aggregates, bowling metrics, phase splits,
and recent form windows.
"""

import pytest
import pytest_asyncio
from datetime import date
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.db.base import Base
import app.models
from app.models.core import CompetitionModel, SeasonModel, TeamModel, VenueModel, MatchModel, PlayerModel
from app.models.performance import BattingScorecardModel, BowlingScorecardModel
from app.analytics.uncapped_analytics_service import UncappedAnalyticsService


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


@pytest.mark.asyncio
async def test_batting_aggregates_and_phase_splits(async_test_session: AsyncSession):
    """Verifies batting calculation totals, boundary %, dot %, and phase breakdown."""
    session = async_test_session

    # Setup parent entities
    comp = CompetitionModel(competition_id="smat", name="SMAT", competition_type="T20")
    session.add(comp)
    await session.flush()

    season = SeasonModel(season_id="2024", competition_id=comp.id, year_start=2024, year_end=2024)
    team = TeamModel(team_code="DEL", name="Delhi", short_name="DEL")
    venue = VenueModel(venue_code="SMS_JAIPUR", name="SMS", city="Jaipur")
    player = PlayerModel(canonical_id="priyansh_arya", full_name="Priyansh Arya")
    session.add_all([season, team, venue, player])
    await session.flush()

    match = MatchModel(
        external_match_id="m1",
        competition_id=comp.id,
        season_id=season.id,
        venue_id=venue.id,
        team_home_id=team.id,
        team_away_id=team.id,
        match_date=date(2024, 10, 15),
    )
    match2 = MatchModel(
        external_match_id="m1_b",
        competition_id=comp.id,
        season_id=season.id,
        venue_id=venue.id,
        team_home_id=team.id,
        team_away_id=team.id,
        match_date=date(2024, 10, 18),
    )
    session.add_all([match, match2])
    await session.flush()

    # Add 2 batting scorecards
    sc1 = BattingScorecardModel(
        match_id=match.id,
        innings_number=1,
        player_id=player.id,
        team_id=team.id,
        batting_position=1,
        runs=60,
        balls_faced=30,
        fours=6,
        sixes=4,
        strike_rate=200.0,
        is_out=True,
        dot_balls=8,
        powerplay_runs=40,
        powerplay_balls=18,
        middle_runs=20,
        middle_balls=12,
        death_runs=0,
        death_balls=0,
    )
    sc2 = BattingScorecardModel(
        match_id=match2.id,
        innings_number=1,
        player_id=player.id,
        team_id=team.id,
        batting_position=1,
        runs=40,
        balls_faced=20,
        fours=4,
        sixes=2,
        strike_rate=200.0,
        is_out=False,
        dot_balls=4,
        powerplay_runs=30,
        powerplay_balls=14,
        middle_runs=10,
        middle_balls=6,
        death_runs=0,
        death_balls=0,
    )
    session.add_all([sc1, sc2])
    await session.commit()

    aggs = await UncappedAnalyticsService.get_player_batting_aggregates(session, player.id)

    assert aggs.innings_count == 2
    assert aggs.runs == 100
    assert aggs.balls_faced == 50
    assert aggs.strike_rate == 200.0
    assert aggs.batting_average == 100.0  # 1 dismissal
    assert aggs.fours == 10
    assert aggs.sixes == 6
    assert aggs.dot_balls == 12
    assert aggs.dot_ball_percentage == 24.0
    # Phase splits
    assert aggs.phase_splits["Powerplay"].runs == 70
    assert aggs.phase_splits["Powerplay"].balls == 32
    assert round(aggs.phase_splits["Powerplay"].strike_rate, 1) == 218.8


@pytest.mark.asyncio
async def test_bowling_aggregates_and_recent_form(async_test_session: AsyncSession):
    """Verifies bowling metrics (economy, wickets, average) and recent form window."""
    session = async_test_session

    comp = CompetitionModel(competition_id="smat", name="SMAT", competition_type="T20")
    session.add(comp)
    await session.flush()

    season = SeasonModel(season_id="2024", competition_id=comp.id, year_start=2024, year_end=2024)
    team = TeamModel(team_code="DEL", name="Delhi", short_name="DEL")
    venue = VenueModel(venue_code="SMS_JAIPUR", name="SMS", city="Jaipur")
    player = PlayerModel(canonical_id="harshit_rana", full_name="Harshit Rana")
    session.add_all([season, team, venue, player])
    await session.flush()

    match = MatchModel(
        external_match_id="m2",
        competition_id=comp.id,
        season_id=season.id,
        venue_id=venue.id,
        team_home_id=team.id,
        team_away_id=team.id,
        match_date=date(2024, 10, 20),
    )
    session.add(match)
    await session.flush()

    sc = BowlingScorecardModel(
        match_id=match.id,
        innings_number=1,
        player_id=player.id,
        team_id=team.id,
        overs=4.0,
        legal_balls=24,
        maidens=0,
        runs_conceded=32,
        wickets=3,
        economy_rate=8.0,
        dot_balls=10,
        death_overs=2.0,
        death_wickets=2,
        death_runs=16,
    )
    session.add(sc)
    await session.commit()

    aggs = await UncappedAnalyticsService.get_player_bowling_aggregates(session, player.id)
    assert aggs.innings_count == 1
    assert aggs.wickets == 3
    assert aggs.economy_rate == 8.0
    assert aggs.bowling_average == round(32 / 3, 2)
    assert aggs.bowling_strike_rate == 8.0  # 24 balls / 3 wickets
    assert aggs.phase_splits["Death"].wickets == 2

    # Test recent form
    form = await UncappedAnalyticsService.get_recent_form(session, player.id, last_n=5, discipline="bowling")
    assert form.innings_evaluated == 1
    assert len(form.recent_matches) == 1
    assert "3/32" in form.recent_matches[0].runs_or_wickets_display
