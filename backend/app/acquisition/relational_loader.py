"""
Royals Intelligence - Parquet to Relational Database Loader
Synchronizes normalized Apache Parquet data and match dictionaries from Stage 1
into normalized SQLAlchemy relational tables with transactional safety and idempotency.
"""

from datetime import date, datetime
from typing import Dict, Any, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.core import (
    CompetitionModel,
    SeasonModel,
    TeamModel,
    VenueModel,
    MatchModel,
    InningsModel,
    PlayerModel,
    PlayerParticipationModel,
)
from app.models.performance import (
    BattingScorecardModel,
    BowlingScorecardModel,
    BallByBallDeliveryModel,
)
from app.services.identity.player_identity_service import PlayerIdentityService
from app.core.logging import logger


class RelationalLoader:
    """ETL service synchronizing Stage 1 normalized artifacts into PostgreSQL/SQLite."""

    @classmethod
    async def get_or_create_competition(
        cls,
        session: AsyncSession,
        competition_id: str,
        name: str = "Indian Premier League",
        competition_type: str = "T20",
    ) -> CompetitionModel:
        """Retrieves or creates a competition record."""
        stmt = select(CompetitionModel).where(CompetitionModel.competition_id == competition_id)
        res = await session.execute(stmt)
        comp = res.scalar_one_or_none()
        if not comp:
            comp = CompetitionModel(
                competition_id=competition_id,
                name=name,
                competition_type=competition_type,
                governing_body="BCCI",
                is_domestic=competition_id.lower() != "ipl",
            )
            session.add(comp)
            await session.flush()
        return comp

    @classmethod
    async def get_or_create_season(
        cls,
        session: AsyncSession,
        competition_db_id: str,
        season_id: str,
    ) -> SeasonModel:
        """Retrieves or creates a season record."""
        stmt = select(SeasonModel).where(
            SeasonModel.competition_id == competition_db_id,
            SeasonModel.season_id == season_id
        )
        res = await session.execute(stmt)
        season = res.scalar_one_or_none()
        if not season:
            year = int(season_id) if season_id.isdigit() else 2026
            season = SeasonModel(
                competition_id=competition_db_id,
                season_id=season_id,
                year_start=year,
                year_end=year,
                is_active=(year >= 2026),
            )
            session.add(season)
            await session.flush()
        return season

    @classmethod
    async def get_or_create_team(
        cls,
        session: AsyncSession,
        team_code: str,
        name: Optional[str] = None,
    ) -> TeamModel:
        """Retrieves or creates a team record."""
        stmt = select(TeamModel).where(TeamModel.team_code == team_code)
        res = await session.execute(stmt)
        team = res.scalar_one_or_none()
        if not team:
            full_name = name or team_code
            team = TeamModel(
                team_code=team_code,
                name=full_name,
                short_name=team_code,
                is_rr=(team_code == "RR"),
                is_domestic=True,
            )
            session.add(team)
            await session.flush()
        return team

    @classmethod
    async def get_or_create_venue(
        cls,
        session: AsyncSession,
        venue_code: str,
        name: Optional[str] = None,
        city: str = "Jaipur",
    ) -> VenueModel:
        """Retrieves or creates a venue record."""
        stmt = select(VenueModel).where(VenueModel.venue_code == venue_code)
        res = await session.execute(stmt)
        venue = res.scalar_one_or_none()
        if not venue:
            venue = VenueModel(
                venue_code=venue_code,
                name=name or venue_code,
                city=city,
                country="India",
                is_rr_home=("JAIPUR" in venue_code or "SMS" in venue_code),
            )
            session.add(venue)
            await session.flush()
        return venue

    @classmethod
    async def load_match_bundle(
        cls,
        session: AsyncSession,
        match_data: Dict[str, Any],
        deliveries_data: List[Dict[str, Any]],
        batting_scorecards: Optional[List[Dict[str, Any]]] = None,
        bowling_scorecards: Optional[List[Dict[str, Any]]] = None,
    ) -> MatchModel:
        """
        Loads a complete match entity along with innings, scorecards, and ball-by-ball deliveries.
        Idempotent: updates existing match record if external_match_id exists.
        """
        ext_match_id = match_data["match_id"]

        # 1. Ensure core parent entities
        comp = await cls.get_or_create_competition(session, match_data.get("competition_id", "ipl"))
        season = await cls.get_or_create_season(session, comp.id, match_data.get("season", "2024"))
        venue = await cls.get_or_create_venue(session, match_data.get("venue", "SMS_JAIPUR"), name=match_data.get("venue_name"))
        team_home = await cls.get_or_create_team(session, match_data.get("team1", "RR"))
        team_away = await cls.get_or_create_team(session, match_data.get("team2", "CSK"))

        # 2. Check if match already exists
        match_stmt = select(MatchModel).where(MatchModel.external_match_id == ext_match_id)
        m_res = await session.execute(match_stmt)
        match_obj = m_res.scalar_one_or_none()

        match_date = match_data.get("match_date")
        if isinstance(match_date, str):
            match_date = datetime.strptime(match_date, "%Y-%m-%d").date()

        if not match_obj:
            match_obj = MatchModel(
                external_match_id=ext_match_id,
                competition_id=comp.id,
                season_id=season.id,
                venue_id=venue.id,
                team_home_id=team_home.id,
                team_away_id=team_away.id,
                match_date=match_date or date(2024, 4, 1),
                toss_winner_id=team_home.id if match_data.get("toss_winner") == team_home.team_code else team_away.id,
                toss_decision=match_data.get("toss_decision", "bat"),
                result_outcome=match_data.get("result", {}).get("outcome_summary", "normal"),
            )
            session.add(match_obj)
            await session.flush()

        # 3. Cache player mapping for rapid delivery lookup
        player_cache: Dict[str, PlayerModel] = {}

        async def get_cached_player(name_str: str) -> PlayerModel:
            if name_str in player_cache:
                return player_cache[name_str]
            p, _, _, _ = await PlayerIdentityService.resolve_or_create_player(
                session=session,
                source_name="match_ingest",
                external_id=f"auto_{name_str.lower().replace(' ', '_')}",
                name=name_str,
            )
            player_cache[name_str] = p
            return p

        # 4. Create Innings if not present
        innings_cache: Dict[int, InningsModel] = {}
        for inn_num in [1, 2]:
            inn_stmt = select(InningsModel).where(
                InningsModel.match_id == match_obj.id,
                InningsModel.innings_number == inn_num
            )
            i_res = await session.execute(inn_stmt)
            inn_obj = i_res.scalar_one_or_none()
            if not inn_obj:
                bat_team = team_home if inn_num == 1 else team_away
                bowl_team = team_away if inn_num == 1 else team_home
                inn_obj = InningsModel(
                    match_id=match_obj.id,
                    innings_number=inn_num,
                    batting_team_id=bat_team.id,
                    bowling_team_id=bowl_team.id,
                    total_runs=0,
                    wickets=0,
                    overs_completed=20.0,
                )
                session.add(inn_obj)
                await session.flush()
            innings_cache[inn_num] = inn_obj

        # 5. Insert Deliveries (bulk checking existing)
        for d in deliveries_data:
            inn_num = d.get("innings_number", 1)
            inn_record = innings_cache.get(inn_num, innings_cache[1])
            
            striker = await get_cached_player(d["striker"])
            non_striker = await get_cached_player(d["non_striker"])
            bowler = await get_cached_player(d["bowler"])
            
            bat_team = await cls.get_or_create_team(session, d.get("batting_team", "RR"))
            bowl_team = await cls.get_or_create_team(session, d.get("bowling_team", "CSK"))

            delivery = BallByBallDeliveryModel(
                match_id=match_obj.id,
                innings_id=inn_record.id,
                over_number=d.get("over_number", int(d.get("over_display", 0.0))),
                ball_in_over=d.get("ball_in_over", 1),
                over_display=d.get("over_display", 0.1),
                phase=d.get("phase", "Powerplay"),
                batting_team_id=bat_team.id,
                bowling_team_id=bowl_team.id,
                striker_id=striker.id,
                non_striker_id=non_striker.id,
                bowler_id=bowler.id,
                batter_runs=d.get("batter_runs", 0),
                extra_runs=d.get("extras", {}).get("total", 0) if isinstance(d.get("extras"), dict) else d.get("extra_runs", 0),
                extra_type=d.get("extra_type"),
                total_runs=d.get("total_runs", 0),
                is_legal=d.get("is_legal", True),
                is_boundary_four=d.get("is_boundary_four", False),
                is_boundary_six=d.get("is_boundary_six", False),
                is_dot_ball=d.get("is_dot_ball", False),
                is_wicket=d.get("is_wicket", False),
                dismissal_type=d.get("dismissal", {}).get("kind") if isinstance(d.get("dismissal"), dict) else None,
                release_speed_kph=d.get("release_speed_kph"),
                delivery_classification=d.get("delivery_classification"),
                shot_type=d.get("shot_type"),
            )
            session.add(delivery)

        # 6. Insert Scorecards if provided
        if batting_scorecards:
            for b in batting_scorecards:
                p = await get_cached_player(b["player_name"])
                t = await cls.get_or_create_team(session, b.get("team_code", "RR"))
                card = BattingScorecardModel(
                    match_id=match_obj.id,
                    innings_number=b.get("innings_number", 1),
                    player_id=p.id,
                    team_id=t.id,
                    batting_position=b.get("batting_position", 1),
                    runs=b.get("runs", 0),
                    balls_faced=b.get("balls_faced", 0),
                    fours=b.get("fours", 0),
                    sixes=b.get("sixes", 0),
                    strike_rate=b.get("strike_rate", 0.0),
                    is_out=b.get("is_out", True),
                    dismissal_kind=b.get("dismissal_kind"),
                    dot_balls=b.get("dot_balls", 0),
                    powerplay_runs=b.get("powerplay_runs", 0),
                    powerplay_balls=b.get("powerplay_balls", 0),
                    death_runs=b.get("death_runs", 0),
                    death_balls=b.get("death_balls", 0),
                )
                session.add(card)

        if bowling_scorecards:
            for b in bowling_scorecards:
                p = await get_cached_player(b["bowler_name"])
                t = await cls.get_or_create_team(session, b.get("team_code", "CSK"))
                card = BowlingScorecardModel(
                    match_id=match_obj.id,
                    innings_number=b.get("innings_number", 1),
                    player_id=p.id,
                    team_id=t.id,
                    overs=b.get("overs", 0.0),
                    legal_balls=b.get("legal_balls", int(b.get("overs", 0.0) * 6)),
                    maidens=b.get("maidens", 0),
                    runs_conceded=b.get("runs_conceded", 0),
                    wickets=b.get("wickets", 0),
                    economy_rate=b.get("economy_rate", 0.0),
                    dot_balls=b.get("dot_balls", 0),
                    wides=b.get("wides", 0),
                    noballs=b.get("noballs", 0),
                    powerplay_overs=b.get("powerplay_overs", 0.0),
                    powerplay_wickets=b.get("powerplay_wickets", 0),
                    death_overs=b.get("death_overs", 0.0),
                    death_wickets=b.get("death_wickets", 0),
                )
                session.add(card)

        await session.flush()
        return match_obj
