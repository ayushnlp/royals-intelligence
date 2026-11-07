"""
Royals Intelligence - Performance Database Models
SQLAlchemy 2.0 models for Scorecards, Ball-by-Ball Deliveries, Fielding,
Partnerships, and Match-Level Player Summaries.
"""

import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import (
    String, Integer, SmallInteger, Float, Boolean, DateTime,
    ForeignKey, UniqueConstraint, Index, CheckConstraint
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, generate_uuid, utc_now


class BattingScorecardModel(Base):
    """Batting innings performance per player."""
    __tablename__ = "batting_scorecards"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    match_id: Mapped[str] = mapped_column(String(36), ForeignKey("matches.id", ondelete="CASCADE"), nullable=False, index=True)
    innings_number: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    player_id: Mapped[str] = mapped_column(String(36), ForeignKey("players.id", ondelete="CASCADE"), nullable=False, index=True)
    team_id: Mapped[str] = mapped_column(String(36), ForeignKey("teams.id"), nullable=False)
    
    batting_position: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    runs: Mapped[int] = mapped_column(SmallInteger, default=0)
    balls_faced: Mapped[int] = mapped_column(SmallInteger, default=0)
    fours: Mapped[int] = mapped_column(SmallInteger, default=0)
    sixes: Mapped[int] = mapped_column(SmallInteger, default=0)
    strike_rate: Mapped[float] = mapped_column(Float, default=0.0)
    is_out: Mapped[bool] = mapped_column(Boolean, default=True)
    dismissal_kind: Mapped[Optional[str]] = mapped_column(String(40), nullable=True)
    bowler_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("players.id"), nullable=True)
    fielder_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("players.id"), nullable=True)
    dot_balls: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)
    
    # Phase splits
    powerplay_runs: Mapped[Optional[int]] = mapped_column(SmallInteger, default=0)
    powerplay_balls: Mapped[Optional[int]] = mapped_column(SmallInteger, default=0)
    middle_runs: Mapped[Optional[int]] = mapped_column(SmallInteger, default=0)
    middle_balls: Mapped[Optional[int]] = mapped_column(SmallInteger, default=0)
    death_runs: Mapped[Optional[int]] = mapped_column(SmallInteger, default=0)
    death_balls: Mapped[Optional[int]] = mapped_column(SmallInteger, default=0)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)

    __table_args__ = (
        UniqueConstraint("match_id", "innings_number", "player_id", name="uq_batting_match_innings_player"),
        Index("ix_batting_player_perf", "player_id", "runs", "strike_rate"),
    )

    # Relationships
    player: Mapped["PlayerModel"] = relationship("PlayerModel", foreign_keys=[player_id])
    bowler: Mapped[Optional["PlayerModel"]] = relationship("PlayerModel", foreign_keys=[bowler_id])
    fielder: Mapped[Optional["PlayerModel"]] = relationship("PlayerModel", foreign_keys=[fielder_id])
    team: Mapped["TeamModel"] = relationship("TeamModel", foreign_keys=[team_id])


class BowlingScorecardModel(Base):
    """Bowling innings performance per player."""
    __tablename__ = "bowling_scorecards"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    match_id: Mapped[str] = mapped_column(String(36), ForeignKey("matches.id", ondelete="CASCADE"), nullable=False, index=True)
    innings_number: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    player_id: Mapped[str] = mapped_column(String(36), ForeignKey("players.id", ondelete="CASCADE"), nullable=False, index=True)
    team_id: Mapped[str] = mapped_column(String(36), ForeignKey("teams.id"), nullable=False)
    
    overs: Mapped[float] = mapped_column(Float, default=0.0)
    legal_balls: Mapped[int] = mapped_column(SmallInteger, default=0)
    maidens: Mapped[int] = mapped_column(SmallInteger, default=0)
    runs_conceded: Mapped[int] = mapped_column(SmallInteger, default=0)
    wickets: Mapped[int] = mapped_column(SmallInteger, default=0)
    economy_rate: Mapped[float] = mapped_column(Float, default=0.0)
    dot_balls: Mapped[Optional[int]] = mapped_column(SmallInteger, default=0)
    wides: Mapped[int] = mapped_column(SmallInteger, default=0)
    noballs: Mapped[int] = mapped_column(SmallInteger, default=0)
    fours_conceded: Mapped[Optional[int]] = mapped_column(SmallInteger, default=0)
    sixes_conceded: Mapped[Optional[int]] = mapped_column(SmallInteger, default=0)
    
    # Phase splits
    powerplay_overs: Mapped[Optional[float]] = mapped_column(Float, default=0.0)
    powerplay_wickets: Mapped[Optional[int]] = mapped_column(SmallInteger, default=0)
    powerplay_runs: Mapped[Optional[int]] = mapped_column(SmallInteger, default=0)
    death_overs: Mapped[Optional[float]] = mapped_column(Float, default=0.0)
    death_wickets: Mapped[Optional[int]] = mapped_column(SmallInteger, default=0)
    death_runs: Mapped[Optional[int]] = mapped_column(SmallInteger, default=0)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)

    __table_args__ = (
        UniqueConstraint("match_id", "innings_number", "player_id", name="uq_bowling_match_innings_player"),
        Index("ix_bowling_player_perf", "player_id", "wickets", "economy_rate"),
    )

    # Relationships
    player: Mapped["PlayerModel"] = relationship("PlayerModel", foreign_keys=[player_id])
    team: Mapped["TeamModel"] = relationship("TeamModel", foreign_keys=[team_id])


class BallByBallDeliveryModel(Base):
    """High-volume ball-by-ball delivery event stream."""
    __tablename__ = "ball_by_ball_deliveries"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    match_id: Mapped[str] = mapped_column(String(36), ForeignKey("matches.id", ondelete="CASCADE"), nullable=False, index=True)
    innings_id: Mapped[str] = mapped_column(String(36), ForeignKey("innings.id", ondelete="CASCADE"), nullable=False, index=True)
    
    over_number: Mapped[int] = mapped_column(SmallInteger, nullable=False)  # 0 to 19
    ball_in_over: Mapped[int] = mapped_column(SmallInteger, nullable=False)  # 1 to 6+
    over_display: Mapped[float] = mapped_column(Float, nullable=False)  # e.g., 0.1, 19.6
    phase: Mapped[str] = mapped_column(String(20), nullable=False, index=True)  # 'Powerplay', 'Middle', 'Death'
    
    batting_team_id: Mapped[str] = mapped_column(String(36), ForeignKey("teams.id"), nullable=False)
    bowling_team_id: Mapped[str] = mapped_column(String(36), ForeignKey("teams.id"), nullable=False)
    striker_id: Mapped[str] = mapped_column(String(36), ForeignKey("players.id"), nullable=False, index=True)
    non_striker_id: Mapped[str] = mapped_column(String(36), ForeignKey("players.id"), nullable=False)
    bowler_id: Mapped[str] = mapped_column(String(36), ForeignKey("players.id"), nullable=False, index=True)
    
    batter_runs: Mapped[int] = mapped_column(SmallInteger, default=0)
    extra_runs: Mapped[int] = mapped_column(SmallInteger, default=0)
    extra_type: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)  # 'wides', 'noballs', 'legbyes', 'byes'
    total_runs: Mapped[int] = mapped_column(SmallInteger, default=0)
    
    is_legal: Mapped[bool] = mapped_column(Boolean, default=True)
    is_boundary_four: Mapped[bool] = mapped_column(Boolean, default=False)
    is_boundary_six: Mapped[bool] = mapped_column(Boolean, default=False)
    is_dot_ball: Mapped[bool] = mapped_column(Boolean, default=False)
    is_wicket: Mapped[bool] = mapped_column(Boolean, default=False)
    dismissal_type: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    player_dismissed_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("players.id"), nullable=True)
    fielder_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("players.id"), nullable=True)
    
    # Sensor telemetry - strictly NULL unless sensor records exist (NEVER FABRICATED)
    release_speed_kph: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    delivery_classification: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)  # 'yorker', 'slower_ball' etc.
    shot_type: Mapped[Optional[str]] = mapped_column(String(40), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)

    __table_args__ = (
        CheckConstraint("total_runs = batter_runs + extra_runs", name="ck_runs_math_balance"),
        Index("ix_delivery_matchup", "bowler_id", "striker_id"),
        Index("ix_delivery_over_sequence", "match_id", "innings_id", "over_number", "ball_in_over"),
    )


class FieldingContributionModel(Base):
    """Fielding contributions in a match."""
    __tablename__ = "fielding_contributions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    match_id: Mapped[str] = mapped_column(String(36), ForeignKey("matches.id", ondelete="CASCADE"), nullable=False, index=True)
    player_id: Mapped[str] = mapped_column(String(36), ForeignKey("players.id", ondelete="CASCADE"), nullable=False, index=True)
    catches: Mapped[int] = mapped_column(SmallInteger, default=0)
    run_outs_direct: Mapped[int] = mapped_column(SmallInteger, default=0)
    run_outs_assisted: Mapped[int] = mapped_column(SmallInteger, default=0)
    stumpings: Mapped[int] = mapped_column(SmallInteger, default=0)
    dropped_catches: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)
    runs_saved: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)

    __table_args__ = (
        UniqueConstraint("match_id", "player_id", name="uq_fielding_match_player"),
    )

    player: Mapped["PlayerModel"] = relationship("PlayerModel")


class PartnershipModel(Base):
    """Wicket batting partnerships."""
    __tablename__ = "partnerships"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    match_id: Mapped[str] = mapped_column(String(36), ForeignKey("matches.id", ondelete="CASCADE"), nullable=False, index=True)
    innings_number: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    wicket_number: Mapped[int] = mapped_column(SmallInteger, nullable=False)  # 1st wicket, 2nd wicket, etc.
    batter_1_id: Mapped[str] = mapped_column(String(36), ForeignKey("players.id"), nullable=False)
    batter_2_id: Mapped[str] = mapped_column(String(36), ForeignKey("players.id"), nullable=False)
    runs: Mapped[int] = mapped_column(SmallInteger, default=0)
    balls: Mapped[int] = mapped_column(SmallInteger, default=0)
    batter_1_runs: Mapped[int] = mapped_column(SmallInteger, default=0)
    batter_1_balls: Mapped[int] = mapped_column(SmallInteger, default=0)
    batter_2_runs: Mapped[int] = mapped_column(SmallInteger, default=0)
    batter_2_balls: Mapped[int] = mapped_column(SmallInteger, default=0)
    is_unbroken: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)

    __table_args__ = (
        UniqueConstraint("match_id", "innings_number", "wicket_number", name="uq_partnership_wicket"),
    )


class PlayerMatchPerformanceModel(Base):
    """All-round composite match performance record."""
    __tablename__ = "player_match_performances"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    match_id: Mapped[str] = mapped_column(String(36), ForeignKey("matches.id", ondelete="CASCADE"), nullable=False, index=True)
    player_id: Mapped[str] = mapped_column(String(36), ForeignKey("players.id", ondelete="CASCADE"), nullable=False, index=True)
    team_id: Mapped[str] = mapped_column(String(36), ForeignKey("teams.id"), nullable=False)
    
    batting_runs: Mapped[int] = mapped_column(SmallInteger, default=0)
    batting_balls: Mapped[int] = mapped_column(SmallInteger, default=0)
    batting_strike_rate: Mapped[float] = mapped_column(Float, default=0.0)
    
    bowling_wickets: Mapped[int] = mapped_column(SmallInteger, default=0)
    bowling_runs_conceded: Mapped[int] = mapped_column(SmallInteger, default=0)
    bowling_overs: Mapped[float] = mapped_column(Float, default=0.0)
    bowling_economy: Mapped[float] = mapped_column(Float, default=0.0)
    
    catches: Mapped[int] = mapped_column(SmallInteger, default=0)
    stumpings: Mapped[int] = mapped_column(SmallInteger, default=0)
    is_player_of_match: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)

    __table_args__ = (
        UniqueConstraint("match_id", "player_id", name="uq_player_match_perf"),
        Index("ix_player_allround_perf", "player_id", "batting_runs", "bowling_wickets"),
    )

    player: Mapped["PlayerModel"] = relationship("PlayerModel")
