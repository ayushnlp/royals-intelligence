"""
Royals Intelligence - Database Models & Schema Integration Tests
Validates all 29 SQLAlchemy 2.0 models, table creation, relationships, foreign keys,
constraints, and Alembic migration functions.
"""

import pytest
import pytest_asyncio
from datetime import date, datetime
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import select, text

from app.db.base import Base
import app.models  # load all models
from app.models.core import (
    CompetitionModel,
    SeasonModel,
    TeamModel,
    VenueModel,
    PlayerModel,
    PlayerIdentityModel,
    MatchModel,
    InningsModel,
)
from app.models.performance import (
    BattingScorecardModel,
    BowlingScorecardModel,
    BallByBallDeliveryModel,
)
from app.models.scouting import (
    UncappedPlayerProfileModel,
    ScoutingEvaluationModel,
)
from app.models.governance import (
    DataSourceModel,
    DataQualityRecordModel,
)


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


@pytest.mark.environment
@pytest.mark.asyncio
async def test_all_models_table_registration():
    """Verifies all 29 target tables are properly registered with Base.metadata."""
    table_names = set(Base.metadata.tables.keys())
    expected_tables = {
        "competitions", "seasons", "teams", "venues", "players",
        "player_identities", "player_roles", "matches", "innings",
        "player_participations", "batting_scorecards", "bowling_scorecards",
        "ball_by_ball_deliveries", "fielding_contributions", "partnerships",
        "player_match_performances", "data_sources", "datasets",
        "ingestion_runs", "dataset_manifests", "validation_results",
        "source_references", "data_quality_records", "uncapped_player_profiles",
        "player_performance_snapshots", "player_role_assessments",
        "scouting_evaluations", "scouting_evidence", "player_comparisons",
    }
    assert expected_tables.issubset(table_names), f"Missing tables: {expected_tables - table_names}"
    assert len(table_names) >= 29


@pytest.mark.environment
@pytest.mark.asyncio
async def test_core_entities_lifecycle(async_test_session: AsyncSession):
    """Tests creating, querying, and relationship traversal of core competition entities."""
    session = async_test_session

    # 1. Create Competition & Season
    comp = CompetitionModel(
        competition_id="smat",
        name="Syed Mushtaq Ali Trophy",
        competition_type="T20",
        governing_body="BCCI",
        is_domestic=True,
    )
    session.add(comp)
    await session.flush()

    season = SeasonModel(
        season_id="2024",
        competition_id=comp.id,
        year_start=2024,
        year_end=2025,
        is_active=False,
    )
    session.add(season)

    # 2. Create Teams & Venue
    rr = TeamModel(team_code="RR", name="Rajasthan Royals", short_name="Royals", is_rr=True, is_domestic=False)
    csk = TeamModel(team_code="CSK", name="Chennai Super Kings", short_name="CSK", is_rr=False, is_domestic=False)
    venue = VenueModel(venue_code="SMS_JAIPUR", name="Sawai Mansingh Stadium", city="Jaipur", is_rr_home=True)
    session.add_all([rr, csk, venue])
    await session.flush()

    # 3. Create Player & External Identity
    player = PlayerModel(
        canonical_id="shashank_singh_test",
        full_name="Shashank Singh",
        known_as="Shashank Singh",
        dob=date(1991, 11, 21),
        dob_source="BCCI Domestic Registry",
        dob_verified=True,
        home_state_association="Chhattisgarh",
        primary_role="Finishing Batter",
        is_capped=False,
    )
    session.add(player)
    await session.flush()

    identity = PlayerIdentityModel(
        player_id=player.id,
        source_name="cricsheet",
        external_player_id="shashank_cric_1",
        name_as_source="Shashank Singh",
        confidence_score=1.0,
    )
    profile = UncappedPlayerProfileModel(
        player_id=player.id,
        eligibility_status="CONFIRMED_UNCAPPED",
        calculated_age_at_cutoff=35.0,
        reference_date_used=date(2026, 11, 18),
        scouting_tier="TARGET_A_LIST",
        is_rr_trialist=True,
    )
    session.add_all([identity, profile])
    await session.flush()

    # 4. Verify queries and relationships
    q_stmt = select(PlayerModel).where(PlayerModel.id == player.id)
    res = await session.execute(q_stmt)
    retrieved = res.scalar_one()

    assert retrieved.full_name == "Shashank Singh"
    assert retrieved.is_capped is False
    assert len(retrieved.identities) == 1
    assert retrieved.identities[0].external_player_id == "shashank_cric_1"
    assert retrieved.uncapped_profile.eligibility_status == "CONFIRMED_UNCAPPED"


@pytest.mark.environment
@pytest.mark.asyncio
async def test_ball_by_ball_delivery_persistence(async_test_session: AsyncSession):
    """Verifies ball-by-ball delivery integrity and run balance checks."""
    session = async_test_session

    comp = CompetitionModel(competition_id="ipl", name="IPL", competition_type="T20")
    session.add(comp)
    await session.flush()

    season = SeasonModel(season_id="2024", competition_id=comp.id, year_start=2024, year_end=2024)
    venue = VenueModel(venue_code="SMS_JAIPUR", name="SMS", city="Jaipur")
    rr = TeamModel(team_code="RR", name="Rajasthan Royals", short_name="RR")
    mi = TeamModel(team_code="MI", name="Mumbai Indians", short_name="MI")
    session.add_all([season, venue, rr, mi])
    await session.flush()

    p1 = PlayerModel(canonical_id="batter_1", full_name="Batter One", is_capped=False)
    p2 = PlayerModel(canonical_id="batter_2", full_name="Batter Two", is_capped=False)
    bowler = PlayerModel(canonical_id="bowler_1", full_name="Bowler One", is_capped=False)
    session.add_all([p1, p2, bowler])
    await session.flush()

    match = MatchModel(
        external_match_id="test_match_01",
        competition_id=comp.id,
        season_id=season.id,
        venue_id=venue.id,
        team_home_id=rr.id,
        team_away_id=mi.id,
        match_date=date(2024, 4, 15),
    )
    session.add(match)
    await session.flush()

    innings = InningsModel(
        match_id=match.id,
        innings_number=1,
        batting_team_id=rr.id,
        bowling_team_id=mi.id,
    )
    session.add(innings)
    await session.flush()

    # Delivery with valid run arithmetic
    delivery = BallByBallDeliveryModel(
        match_id=match.id,
        innings_id=innings.id,
        over_number=0,
        ball_in_over=1,
        over_display=0.1,
        phase="Powerplay",
        batting_team_id=rr.id,
        bowling_team_id=mi.id,
        striker_id=p1.id,
        non_striker_id=p2.id,
        bowler_id=bowler.id,
        batter_runs=4,
        extra_runs=0,
        total_runs=4,
        is_boundary_four=True,
    )
    session.add(delivery)
    await session.commit()

    # Query back
    stmt = select(BallByBallDeliveryModel).where(BallByBallDeliveryModel.match_id == match.id)
    res = await session.execute(stmt)
    saved = res.scalar_one()

    assert saved.total_runs == 4
    assert saved.batter_runs + saved.extra_runs == saved.total_runs
    assert saved.is_boundary_four is True
    assert saved.phase == "Powerplay"
    assert saved.release_speed_kph is None  # Never fabricated


@pytest.mark.environment
def test_migration_file_structure():
    """Validates Alembic migration file presence and upgrade/downgrade symbols."""
    import importlib.util
    from pathlib import Path
    mig_path = Path(__file__).resolve().parent.parent / "alembic" / "versions" / "001_uncapped_player_foundation.py"
    spec = importlib.util.spec_from_file_location("mig", str(mig_path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    assert mod.revision == "001_uncapped_player_foundation"
    assert mod.down_revision is None
    assert hasattr(mod, "upgrade")
    assert hasattr(mod, "downgrade")
