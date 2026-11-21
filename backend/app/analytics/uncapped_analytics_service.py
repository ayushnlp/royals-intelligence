"""
Royals Intelligence - Analytics Foundation Service
High-performance asynchronous querying and aggregation for Uncapped Players:
Career aggregates, phase splits (Powerplay, Middle, Death), recent form windows,
venue splits, and role-based benchmarking.
"""

from typing import Optional, List, Dict
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

from app.models.core import MatchModel, VenueModel
from app.models.performance import (
    BattingScorecardModel,
    BowlingScorecardModel,
)


class PhaseMetrics(BaseModel):
    """Batting or bowling phase split metrics."""
    phase: str
    runs: int = 0
    balls: int = 0
    wickets: int = 0
    strike_rate: float = 0.0
    economy_rate: float = 0.0
    boundary_percentage: float = 0.0
    dot_ball_percentage: float = 0.0


class BattingAggregates(BaseModel):
    """Batting aggregate performance summary."""
    player_id: str
    innings_count: int = 0
    runs: int = 0
    balls_faced: int = 0
    fours: int = 0
    sixes: int = 0
    strike_rate: float = 0.0
    batting_average: Optional[float] = None
    dismissals: int = 0
    dot_balls: int = 0
    dot_ball_percentage: float = 0.0
    boundary_percentage: float = 0.0
    high_score: int = 0
    phase_splits: Dict[str, PhaseMetrics] = Field(default_factory=dict)
    is_degraded_reference: bool = Field(default=False, description="Flag indicating degraded offline reference data")
    data_source: str = Field(default="live_database", description="Data provenance: live_database or reference_seed_not_live")


class BowlingAggregates(BaseModel):
    """Bowling aggregate performance summary."""
    player_id: str
    innings_count: int = 0
    overs: float = 0.0
    legal_balls: int = 0
    runs_conceded: int = 0
    wickets: int = 0
    economy_rate: float = 0.0
    bowling_average: Optional[float] = None
    bowling_strike_rate: Optional[float] = None
    dot_balls: int = 0
    dot_ball_percentage: float = 0.0
    phase_splits: Dict[str, PhaseMetrics] = Field(default_factory=dict)
    is_degraded_reference: bool = Field(default=False, description="Flag indicating degraded offline reference data")
    data_source: str = Field(default="live_database", description="Data provenance: live_database or reference_seed_not_live")


class MatchScorecardItem(BaseModel):
    """Single match batting or bowling entry in a form window."""
    match_id: str
    match_date: str
    opposition_team: str
    venue_name: str
    runs_or_wickets_display: str
    strike_rate_or_economy: float


class RecentFormWindow(BaseModel):
    """Recent performance window (e.g., last 5 or 10 innings)."""
    player_id: str
    window_size: int
    innings_evaluated: int
    aggregate_metric_summary: str
    recent_matches: List[MatchScorecardItem] = Field(default_factory=list)


class UncappedAnalyticsService:
    """Core analytics querying foundation for uncapped player evaluation."""

    @classmethod
    async def get_player_batting_aggregates(
        cls,
        session: AsyncSession,
        player_id: str,
        competition_id: Optional[str] = None,
        season_id: Optional[str] = None,
    ) -> BattingAggregates:
        """Computes comprehensive batting aggregates including phase splits."""
        query = select(BattingScorecardModel).where(BattingScorecardModel.player_id == player_id)

        if competition_id or season_id:
            query = query.join(MatchModel, BattingScorecardModel.match_id == MatchModel.id)
            if competition_id:
                query = query.where(MatchModel.competition_id == competition_id)
            if season_id:
                query = query.where(MatchModel.season_id == season_id)

        res = await session.execute(query)
        scorecards = res.scalars().all()

        if not scorecards:
            return BattingAggregates(player_id=player_id)

        total_runs = sum(sc.runs for sc in scorecards)
        total_balls = sum(sc.balls_faced for sc in scorecards)
        total_fours = sum(sc.fours for sc in scorecards)
        total_sixes = sum(sc.sixes for sc in scorecards)
        dismissals = sum(1 for sc in scorecards if sc.is_out)
        total_dots = sum(sc.dot_balls or 0 for sc in scorecards)
        high_score = max((sc.runs for sc in scorecards), default=0)

        sr = round((total_runs / total_balls * 100), 2) if total_balls > 0 else 0.0
        avg = round(total_runs / dismissals, 2) if dismissals > 0 else None
        dot_pct = round((total_dots / total_balls * 100), 2) if total_balls > 0 else 0.0
        boundary_pct = round(((total_fours * 4 + total_sixes * 6) / total_runs * 100), 2) if total_runs > 0 else 0.0

        # Phase splits
        pp_runs = sum(sc.powerplay_runs or 0 for sc in scorecards)
        pp_balls = sum(sc.powerplay_balls or 0 for sc in scorecards)
        mid_runs = sum(sc.middle_runs or 0 for sc in scorecards)
        mid_balls = sum(sc.middle_balls or 0 for sc in scorecards)
        death_runs = sum(sc.death_runs or 0 for sc in scorecards)
        death_balls = sum(sc.death_balls or 0 for sc in scorecards)

        phase_splits = {
            "Powerplay": PhaseMetrics(
                phase="Powerplay",
                runs=pp_runs,
                balls=pp_balls,
                strike_rate=round(pp_runs / pp_balls * 100, 2) if pp_balls > 0 else 0.0,
            ),
            "Middle": PhaseMetrics(
                phase="Middle",
                runs=mid_runs,
                balls=mid_balls,
                strike_rate=round(mid_runs / mid_balls * 100, 2) if mid_balls > 0 else 0.0,
            ),
            "Death": PhaseMetrics(
                phase="Death",
                runs=death_runs,
                balls=death_balls,
                strike_rate=round(death_runs / death_balls * 100, 2) if death_balls > 0 else 0.0,
            ),
        }

        return BattingAggregates(
            player_id=player_id,
            innings_count=len(scorecards),
            runs=total_runs,
            balls_faced=total_balls,
            fours=total_fours,
            sixes=total_sixes,
            strike_rate=sr,
            batting_average=avg,
            dismissals=dismissals,
            dot_balls=total_dots,
            dot_ball_percentage=dot_pct,
            boundary_percentage=boundary_pct,
            high_score=high_score,
            phase_splits=phase_splits,
        )

    @classmethod
    async def get_player_bowling_aggregates(
        cls,
        session: AsyncSession,
        player_id: str,
        competition_id: Optional[str] = None,
        season_id: Optional[str] = None,
    ) -> BowlingAggregates:
        """Computes comprehensive bowling aggregates including phase splits."""
        query = select(BowlingScorecardModel).where(BowlingScorecardModel.player_id == player_id)

        if competition_id or season_id:
            query = query.join(MatchModel, BowlingScorecardModel.match_id == MatchModel.id)
            if competition_id:
                query = query.where(MatchModel.competition_id == competition_id)
            if season_id:
                query = query.where(MatchModel.season_id == season_id)

        res = await session.execute(query)
        scorecards = res.scalars().all()

        if not scorecards:
            return BowlingAggregates(player_id=player_id)

        total_balls = sum(sc.legal_balls for sc in scorecards)
        total_runs = sum(sc.runs_conceded for sc in scorecards)
        total_wickets = sum(sc.wickets for sc in scorecards)
        total_dots = sum(sc.dot_balls or 0 for sc in scorecards)

        econ = round((total_runs / total_balls * 6), 2) if total_balls > 0 else 0.0
        avg = round(total_runs / total_wickets, 2) if total_wickets > 0 else None
        sr = round(total_balls / total_wickets, 2) if total_wickets > 0 else None
        dot_pct = round((total_dots / total_balls * 100), 2) if total_balls > 0 else 0.0

        # Phase breakdown
        pp_overs = sum(sc.powerplay_overs or 0.0 for sc in scorecards)
        pp_wkts = sum(sc.powerplay_wickets or 0 for sc in scorecards)
        pp_runs = sum(sc.powerplay_runs or 0 for sc in scorecards)
        death_overs = sum(sc.death_overs or 0.0 for sc in scorecards)
        death_wkts = sum(sc.death_wickets or 0 for sc in scorecards)
        death_runs = sum(sc.death_runs or 0 for sc in scorecards)

        phase_splits = {
            "Powerplay": PhaseMetrics(
                phase="Powerplay",
                runs=pp_runs,
                balls=int(pp_overs * 6),
                wickets=pp_wkts,
                economy_rate=round(pp_runs / pp_overs, 2) if pp_overs > 0 else 0.0,
            ),
            "Death": PhaseMetrics(
                phase="Death",
                runs=death_runs,
                balls=int(death_overs * 6),
                wickets=death_wkts,
                economy_rate=round(death_runs / death_overs, 2) if death_overs > 0 else 0.0,
            ),
        }

        return BowlingAggregates(
            player_id=player_id,
            innings_count=len(scorecards),
            overs=round(total_balls / 6, 1),
            legal_balls=total_balls,
            runs_conceded=total_runs,
            wickets=total_wickets,
            economy_rate=econ,
            bowling_average=avg,
            bowling_strike_rate=sr,
            dot_balls=total_dots,
            dot_ball_percentage=dot_pct,
            phase_splits=phase_splits,
        )

    @classmethod
    async def get_recent_form(
        cls,
        session: AsyncSession,
        player_id: str,
        last_n: int = 5,
        discipline: str = "batting",
    ) -> RecentFormWindow:
        """Retrieves chronological recent-form window (last N matches)."""
        if discipline == "batting":
            query = (
                select(BattingScorecardModel, MatchModel, VenueModel)
                .join(MatchModel, BattingScorecardModel.match_id == MatchModel.id)
                .join(VenueModel, MatchModel.venue_id == VenueModel.id)
                .where(BattingScorecardModel.player_id == player_id)
                .order_by(desc(MatchModel.match_date))
                .limit(last_n)
            )
            res = await session.execute(query)
            rows = res.all()

            items = []
            total_runs = 0
            for sc, m, v in rows:
                total_runs += sc.runs
                items.append(MatchScorecardItem(
                    match_id=m.id,
                    match_date=str(m.match_date),
                    opposition_team="Opposition",
                    venue_name=v.name,
                    runs_or_wickets_display=f"{sc.runs} ({sc.balls_faced})",
                    strike_rate_or_economy=sc.strike_rate,
                ))

            summary = f"{total_runs} runs across last {len(rows)} innings" if rows else "No recent innings on record"
            return RecentFormWindow(
                player_id=player_id,
                window_size=last_n,
                innings_evaluated=len(rows),
                aggregate_metric_summary=summary,
                recent_matches=items,
            )
        else:
            query = (
                select(BowlingScorecardModel, MatchModel, VenueModel)
                .join(MatchModel, BowlingScorecardModel.match_id == MatchModel.id)
                .join(VenueModel, MatchModel.venue_id == VenueModel.id)
                .where(BowlingScorecardModel.player_id == player_id)
                .order_by(desc(MatchModel.match_date))
                .limit(last_n)
            )
            res = await session.execute(query)
            rows = res.all()

            items = []
            total_wkts = 0
            for sc, m, v in rows:
                total_wkts += sc.wickets
                items.append(MatchScorecardItem(
                    match_id=m.id,
                    match_date=str(m.match_date),
                    opposition_team="Opposition",
                    venue_name=v.name,
                    runs_or_wickets_display=f"{sc.wickets}/{sc.runs_conceded} ({sc.overs} ov)",
                    strike_rate_or_economy=sc.economy_rate,
                ))

            summary = f"{total_wkts} wickets across last {len(rows)} spells" if rows else "No recent bowling spells on record"
            return RecentFormWindow(
                player_id=player_id,
                window_size=last_n,
                innings_evaluated=len(rows),
                aggregate_metric_summary=summary,
                recent_matches=items,
            )
