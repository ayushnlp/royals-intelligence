"""
Royals Intelligence - Core Cricket Database Models
SQLAlchemy 2.0 models for Competitions, Seasons, Teams, Venues, Matches, Innings,
and Player Identity & Demographics.
"""

import uuid
from datetime import date, datetime
from typing import List, Optional
from sqlalchemy import (
    String, Integer, SmallInteger, Float, Boolean, Date, DateTime, Text,
    ForeignKey, UniqueConstraint, Index
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, generate_uuid, utc_now


class CompetitionModel(Base):
    """Competition / Tournament (e.g., IPL, SMAT, VHT, Ranji)."""
    __tablename__ = "competitions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    competition_id: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    competition_type: Mapped[str] = mapped_column(String(30), nullable=False)  # T20, List A, First Class
    governing_body: Mapped[str] = mapped_column(String(50), default="BCCI")
    is_domestic: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)

    # Relationships
    seasons: Mapped[List["SeasonModel"]] = relationship("SeasonModel", back_populates="competition", cascade="all, delete-orphan")
    matches: Mapped[List["MatchModel"]] = relationship("MatchModel", back_populates="competition")


class SeasonModel(Base):
    """Season within a competition (e.g., 2024, 2025, 2026)."""
    __tablename__ = "seasons"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    season_id: Mapped[str] = mapped_column(String(20), index=True)  # '2026', '2025'
    competition_id: Mapped[str] = mapped_column(String(36), ForeignKey("competitions.id", ondelete="CASCADE"), nullable=False)
    year_start: Mapped[int] = mapped_column(Integer, nullable=False)
    year_end: Mapped[int] = mapped_column(Integer, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)

    # Unique constraint per competition + season
    __table_args__ = (
        UniqueConstraint("competition_id", "season_id", name="uq_season_competition"),
    )

    # Relationships
    competition: Mapped["CompetitionModel"] = relationship("CompetitionModel", back_populates="seasons")
    matches: Mapped[List["MatchModel"]] = relationship("MatchModel", back_populates="season_rel")


class TeamModel(Base):
    """Domestic state team or franchise (e.g., Rajasthan Royals, Mumbai, Tamil Nadu)."""
    __tablename__ = "teams"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    team_code: Mapped[str] = mapped_column(String(20), unique=True, index=True)  # 'RR', 'MUM', 'TN', 'RAJ'
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    short_name: Mapped[str] = mapped_column(String(50), nullable=False)
    is_rr: Mapped[bool] = mapped_column(Boolean, default=False)
    is_domestic: Mapped[bool] = mapped_column(Boolean, default=True)
    state_association: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    primary_color: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    accent_color: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)

    # Relationships
    home_matches: Mapped[List["MatchModel"]] = relationship("MatchModel", foreign_keys="MatchModel.team_home_id", back_populates="team_home")
    away_matches: Mapped[List["MatchModel"]] = relationship("MatchModel", foreign_keys="MatchModel.team_away_id", back_populates="team_away")


class VenueModel(Base):
    """Cricket ground / stadium with geographic and pitch attributes."""
    __tablename__ = "venues"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    venue_code: Mapped[str] = mapped_column(String(50), unique=True, index=True)  # 'SMS_JAIPUR'
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    city: Mapped[str] = mapped_column(String(80), nullable=False)
    country: Mapped[str] = mapped_column(String(80), default="India")
    is_rr_home: Mapped[bool] = mapped_column(Boolean, default=False)
    altitude_m: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    pitch_soil_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # 'Black Soil', 'Red Soil'
    straight_boundary_m: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    off_boundary_m: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    leg_boundary_m: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    latitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    longitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)

    # Relationships
    matches: Mapped[List["MatchModel"]] = relationship("MatchModel", back_populates="venue")


class PlayerModel(Base):
    """Canonical Player entity (demographics, cap status, role)."""
    __tablename__ = "players"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    canonical_id: Mapped[str] = mapped_column(String(60), unique=True, index=True)  # Canonical slug / ID
    full_name: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    known_as: Mapped[Optional[str]] = mapped_column(String(80), nullable=True)
    dob: Mapped[Optional[date]] = mapped_column(Date, nullable=True, index=True)
    dob_source: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    dob_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    nationality: Mapped[str] = mapped_column(String(60), default="India")
    home_state_association: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    batting_hand: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)  # 'Right', 'Left'
    bowling_style: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # 'Right-arm offbreak', etc.
    primary_role: Mapped[Optional[str]] = mapped_column(String(40), nullable=True)  # 'Batter', 'Bowler', 'All-Rounder', 'Wicketkeeper'
    
    # Cap Status: True if player has represented Senior National team in any format
    is_capped: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    last_international_match_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    international_caps_detail: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    ipl_debut_season: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, onupdate=utc_now)

    # Relationships
    identities: Mapped[List["PlayerIdentityModel"]] = relationship("PlayerIdentityModel", back_populates="player", cascade="all, delete-orphan", lazy="selectin")
    roles: Mapped[List["PlayerRoleModel"]] = relationship("PlayerRoleModel", back_populates="player", cascade="all, delete-orphan", lazy="selectin")
    participations: Mapped[List["PlayerParticipationModel"]] = relationship("PlayerParticipationModel", back_populates="player", lazy="selectin")
    uncapped_profile: Mapped[Optional["UncappedPlayerProfileModel"]] = relationship("UncappedPlayerProfileModel", back_populates="player", uselist=False, lazy="selectin")


class PlayerIdentityModel(Base):
    """Source-specific external identifiers and name spelling variations."""
    __tablename__ = "player_identities"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    player_id: Mapped[str] = mapped_column(String(36), ForeignKey("players.id", ondelete="CASCADE"), nullable=False, index=True)
    source_name: Mapped[str] = mapped_column(String(50), nullable=False)  # 'cricsheet', 'bcci', 'espncricinfo', 'rr_scouting'
    external_player_id: Mapped[str] = mapped_column(String(100), nullable=False)
    name_as_source: Mapped[str] = mapped_column(String(120), nullable=False)
    alias_names: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # Comma-separated or JSON string of aliases
    confidence_score: Mapped[float] = mapped_column(Float, default=1.0)
    conflict_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)

    __table_args__ = (
        UniqueConstraint("source_name", "external_player_id", name="uq_source_external_player"),
        Index("ix_player_identity_lookup", "source_name", "name_as_source"),
    )

    # Relationships
    player: Mapped["PlayerModel"] = relationship("PlayerModel", back_populates="identities")


class PlayerRoleModel(Base):
    """Detailed role assessment (e.g. 'Opening Batter', 'Death Specialist', 'Pinch Hitter')."""
    __tablename__ = "player_roles"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    player_id: Mapped[str] = mapped_column(String(36), ForeignKey("players.id", ondelete="CASCADE"), nullable=False, index=True)
    role_category: Mapped[str] = mapped_column(String(50), nullable=False)  # 'Top Order Batter', 'Finisher', 'Express Pace'
    batting_phase_preference: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)  # 'Powerplay', 'Middle', 'Death'
    bowling_phase_preference: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    tactical_niche: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)  # 'Hard length enforcer', 'Pace-hitter'
    is_primary: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)

    # Relationships
    player: Mapped["PlayerModel"] = relationship("PlayerModel", back_populates="roles")


class MatchModel(Base):
    """Match fixture record."""
    __tablename__ = "matches"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    external_match_id: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    competition_id: Mapped[str] = mapped_column(String(36), ForeignKey("competitions.id"), nullable=False, index=True)
    season_id: Mapped[str] = mapped_column(String(36), ForeignKey("seasons.id"), nullable=False, index=True)
    venue_id: Mapped[str] = mapped_column(String(36), ForeignKey("venues.id"), nullable=False, index=True)
    team_home_id: Mapped[str] = mapped_column(String(36), ForeignKey("teams.id"), nullable=False, index=True)
    team_away_id: Mapped[str] = mapped_column(String(36), ForeignKey("teams.id"), nullable=False, index=True)
    
    match_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    match_number: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    toss_winner_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("teams.id"), nullable=True)
    toss_decision: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)  # 'bat', 'field'
    winner_team_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("teams.id"), nullable=True)
    win_margin_runs: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    win_margin_wickets: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    is_tie: Mapped[bool] = mapped_column(Boolean, default=False)
    is_super_over: Mapped[bool] = mapped_column(Boolean, default=False)
    result_outcome: Mapped[str] = mapped_column(String(100), default="normal")
    player_of_match_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("players.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)

    # Relationships
    competition: Mapped["CompetitionModel"] = relationship("CompetitionModel", back_populates="matches")
    season_rel: Mapped["SeasonModel"] = relationship("SeasonModel", back_populates="matches")
    venue: Mapped["VenueModel"] = relationship("VenueModel", back_populates="matches")
    team_home: Mapped["TeamModel"] = relationship("TeamModel", foreign_keys=[team_home_id], back_populates="home_matches")
    team_away: Mapped["TeamModel"] = relationship("TeamModel", foreign_keys=[team_away_id], back_populates="away_matches")
    innings: Mapped[List["InningsModel"]] = relationship("InningsModel", back_populates="match", cascade="all, delete-orphan")
    participations: Mapped[List["PlayerParticipationModel"]] = relationship("PlayerParticipationModel", back_populates="match")


class InningsModel(Base):
    """Innings aggregate within a match."""
    __tablename__ = "innings"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    match_id: Mapped[str] = mapped_column(String(36), ForeignKey("matches.id", ondelete="CASCADE"), nullable=False, index=True)
    innings_number: Mapped[int] = mapped_column(SmallInteger, nullable=False)  # 1, 2, 3 (Super Over)
    batting_team_id: Mapped[str] = mapped_column(String(36), ForeignKey("teams.id"), nullable=False)
    bowling_team_id: Mapped[str] = mapped_column(String(36), ForeignKey("teams.id"), nullable=False)
    total_runs: Mapped[int] = mapped_column(Integer, default=0)
    wickets: Mapped[int] = mapped_column(SmallInteger, default=0)
    overs_completed: Mapped[float] = mapped_column(Float, default=0.0)
    is_declared_or_all_out: Mapped[bool] = mapped_column(Boolean, default=False)
    extras_total: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)

    __table_args__ = (
        UniqueConstraint("match_id", "innings_number", name="uq_match_innings_number"),
    )

    # Relationships
    match: Mapped["MatchModel"] = relationship("MatchModel", back_populates="innings")
    batting_team: Mapped["TeamModel"] = relationship("TeamModel", foreign_keys=[batting_team_id])
    bowling_team: Mapped["TeamModel"] = relationship("TeamModel", foreign_keys=[bowling_team_id])


class PlayerParticipationModel(Base):
    """Player participation in a match (Playing XI, Impact Sub, Captain)."""
    __tablename__ = "player_participations"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    match_id: Mapped[str] = mapped_column(String(36), ForeignKey("matches.id", ondelete="CASCADE"), nullable=False, index=True)
    player_id: Mapped[str] = mapped_column(String(36), ForeignKey("players.id", ondelete="CASCADE"), nullable=False, index=True)
    team_id: Mapped[str] = mapped_column(String(36), ForeignKey("teams.id"), nullable=False, index=True)
    role_in_match: Mapped[str] = mapped_column(String(40), nullable=False)  # 'Playing XI', 'Impact Player Used', 'Substitute'
    is_impact_in: Mapped[bool] = mapped_column(Boolean, default=False)
    is_impact_out: Mapped[bool] = mapped_column(Boolean, default=False)
    is_captain: Mapped[bool] = mapped_column(Boolean, default=False)
    is_wicketkeeper: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)

    __table_args__ = (
        UniqueConstraint("match_id", "player_id", name="uq_match_player_participation"),
    )

    # Relationships
    match: Mapped["MatchModel"] = relationship("MatchModel", back_populates="participations")
    player: Mapped["PlayerModel"] = relationship("PlayerModel", back_populates="participations")
    team: Mapped["TeamModel"] = relationship("TeamModel")
