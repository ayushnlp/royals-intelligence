"""
Royals Intelligence - Uncapped Player Scouting Database Models
SQLAlchemy 2.0 models for Uncapped Player Profiles, Eligibility Auditing,
Performance Snapshots, Role Assessments, Scouting Evaluations, and Evidence.
Strict Scope: UNCAPPED PLAYERS ONLY.
"""

import uuid
from datetime import date, datetime
from typing import Optional, List
from sqlalchemy import (
    String, Integer, SmallInteger, Float, Boolean, Date, DateTime, Text,
    ForeignKey, UniqueConstraint, Index
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, generate_uuid, utc_now


class UncappedPlayerProfileModel(Base):
    """
    Core Uncapped Player Profile & Eligibility State.
    Enforces strict verification states:
      - CONFIRMED_UNCAPPED: Verified zero senior international caps.
      - SUSPECTED_CAPPED: Flagged for international representation.
      - INELIGIBLE_OVERAGE: Exceeds competition age cutoff if tournament-specific.
      - PENDING_VERIFICATION: Missing DOB or incomplete match lineage.
      - FLAGGED_CONFLICT: Conflicting source records detected.
    """
    __tablename__ = "uncapped_player_profiles"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    player_id: Mapped[str] = mapped_column(String(36), ForeignKey("players.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    
    # Eligibility & Verification
    eligibility_status: Mapped[str] = mapped_column(
        String(30),
        default="PENDING_VERIFICATION",
        index=True
    )  # 'CONFIRMED_UNCAPPED', 'SUSPECTED_CAPPED', 'INELIGIBLE_OVERAGE', 'PENDING_VERIFICATION', 'FLAGGED_CONFLICT'
    
    eligibility_verified_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    verification_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Age calculation provenance
    calculated_age_at_cutoff: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    reference_date_used: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    
    # Eligibility rule provenance and cap separation
    international_caps_detail: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    last_international_appearance_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    eligibility_rule_source: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    rule_version: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    rule_evidence: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # State and domestic allegiance
    state_association: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, index=True)
    current_domestic_team: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    # Primary scouting discipline
    primary_discipline: Mapped[str] = mapped_column(String(60), default="All-Rounder")
    
    # Rajasthan Royals Internal Scouting Status
    scouting_tier: Mapped[str] = mapped_column(String(30), default="MONITOR")  # 'TARGET_A_LIST', 'WATCHLIST_HIGH', 'MONITOR', 'BACKUP'
    is_rr_trialist: Mapped[bool] = mapped_column(Boolean, default=False)
    has_video_evidence: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Proprietary access segregation
    data_classification: Mapped[str] = mapped_column(String(40), default="INTERNAL_SCOUTING")
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, onupdate=utc_now)

    # Relationships
    player: Mapped["PlayerModel"] = relationship("PlayerModel", back_populates="uncapped_profile", lazy="selectin")
    snapshots: Mapped[List["PlayerPerformanceSnapshotModel"]] = relationship("PlayerPerformanceSnapshotModel", back_populates="profile", cascade="all, delete-orphan", lazy="selectin")
    role_assessments: Mapped[List["PlayerRoleAssessmentModel"]] = relationship("PlayerRoleAssessmentModel", back_populates="profile", cascade="all, delete-orphan", lazy="selectin")
    evaluations: Mapped[List["ScoutingEvaluationModel"]] = relationship("ScoutingEvaluationModel", back_populates="profile", cascade="all, delete-orphan", lazy="selectin")


class PlayerPerformanceSnapshotModel(Base):
    """Aggregated performance snapshot across a competition / season for an uncapped player."""
    __tablename__ = "player_performance_snapshots"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    uncapped_profile_id: Mapped[str] = mapped_column(String(36), ForeignKey("uncapped_player_profiles.id", ondelete="CASCADE"), nullable=False, index=True)
    competition_id: Mapped[str] = mapped_column(String(50), nullable=False)  # 'smat', 'vht', 'ck_nayudu'
    season: Mapped[str] = mapped_column(String(20), nullable=False)  # '2024', '2025'
    
    matches: Mapped[int] = mapped_column(SmallInteger, default=0)
    innings_batted: Mapped[int] = mapped_column(SmallInteger, default=0)
    runs: Mapped[int] = mapped_column(Integer, default=0)
    balls_faced: Mapped[int] = mapped_column(Integer, default=0)
    batting_strike_rate: Mapped[float] = mapped_column(Float, default=0.0)
    batting_average: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    boundary_percentage: Mapped[float] = mapped_column(Float, default=0.0)
    dot_ball_percentage_batting: Mapped[float] = mapped_column(Float, default=0.0)
    
    # Phase splits for batting
    powerplay_strike_rate: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    death_strike_rate: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    
    # Bowling metrics
    overs_bowled: Mapped[float] = mapped_column(Float, default=0.0)
    wickets: Mapped[int] = mapped_column(SmallInteger, default=0)
    bowling_economy: Mapped[float] = mapped_column(Float, default=0.0)
    bowling_strike_rate: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    bowling_average: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    death_economy: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    dot_ball_percentage_bowling: Mapped[float] = mapped_column(Float, default=0.0)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)

    __table_args__ = (
        UniqueConstraint("uncapped_profile_id", "competition_id", "season", name="uq_snapshot_profile_comp_season"),
    )

    # Relationships
    profile: Mapped["UncappedPlayerProfileModel"] = relationship("UncappedPlayerProfileModel", back_populates="snapshots")


class PlayerRoleAssessmentModel(Base):
    """Granular role capability scorecards (archetypes, phase readiness)."""
    __tablename__ = "player_role_assessments"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    uncapped_profile_id: Mapped[str] = mapped_column(String(36), ForeignKey("uncapped_player_profiles.id", ondelete="CASCADE"), nullable=False, index=True)
    
    archetype_tag: Mapped[str] = mapped_column(String(60), nullable=False)  # 'Powerplay Enforcer', 'Death Hitter', 'Wrist-Spin Weapon'
    powerplay_rating: Mapped[float] = mapped_column(Float, default=5.0)  # Scale 1.0 to 10.0
    middle_overs_rating: Mapped[float] = mapped_column(Float, default=5.0)
    death_overs_rating: Mapped[float] = mapped_column(Float, default=5.0)
    
    pace_comfort_score: Mapped[float] = mapped_column(Float, default=5.0)
    spin_comfort_score: Mapped[float] = mapped_column(Float, default=5.0)
    
    role_readiness: Mapped[str] = mapped_column(String(40), default="DEVELOPMENTAL")  # 'IPL_READY', 'IMPACT_SUB_READY', 'DEVELOPMENTAL'
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)

    # Relationships
    profile: Mapped["UncappedPlayerProfileModel"] = relationship("UncappedPlayerProfileModel", back_populates="role_assessments")


class ScoutingEvaluationModel(Base):
    """
    Confidential Scout Report (Rajasthan Royals proprietary scouting).
    Strict data classification: RR_PROPRIETARY_CONFIDENTIAL.
    Protected by data masking in public views.
    """
    __tablename__ = "scouting_evaluations"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    uncapped_profile_id: Mapped[str] = mapped_column(String(36), ForeignKey("uncapped_player_profiles.id", ondelete="CASCADE"), nullable=False, index=True)
    scout_identifier: Mapped[str] = mapped_column(String(60), nullable=False)  # e.g. 'RR_SCOUT_DOMESTIC_NORTH'
    evaluation_date: Mapped[date] = mapped_column(Date, nullable=False)
    competition_or_trial: Mapped[str] = mapped_column(String(100), nullable=False)
    
    # 1.0 to 10.0 Ratings
    technical_skill_rating: Mapped[float] = mapped_column(Float, nullable=False)
    temperament_rating: Mapped[float] = mapped_column(Float, nullable=False)
    athleticism_rating: Mapped[float] = mapped_column(Float, nullable=False)
    tactical_iq_rating: Mapped[float] = mapped_column(Float, nullable=False)
    ceiling_potential_rating: Mapped[float] = mapped_column(Float, nullable=False)
    
    # Confidential Scouting Insights
    strengths_summary: Mapped[str] = mapped_column(Text, nullable=False)
    development_areas: Mapped[str] = mapped_column(Text, nullable=False)
    scout_recommendation: Mapped[str] = mapped_column(String(40), default="SHORTLIST")  # 'SIGN_URGENT', 'SHORTLIST', 'MONITOR', 'PASS'
    proprietary_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    data_classification: Mapped[str] = mapped_column(String(40), default="RR_PROPRIETARY_CONFIDENTIAL")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)

    # Relationships
    profile: Mapped["UncappedPlayerProfileModel"] = relationship("UncappedPlayerProfileModel", back_populates="evaluations")
    evidence_items: Mapped[List["ScoutingEvidenceModel"]] = relationship("ScoutingEvidenceModel", back_populates="evaluation", cascade="all, delete-orphan")


class ScoutingEvidenceModel(Base):
    """Measurable empirical evidence or video log backing a scout evaluation."""
    __tablename__ = "scouting_evidence"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    evaluation_id: Mapped[str] = mapped_column(String(36), ForeignKey("scouting_evaluations.id", ondelete="CASCADE"), nullable=False, index=True)
    evidence_type: Mapped[str] = mapped_column(String(40), nullable=False)  # 'MATCH_METRIC', 'VIDEO_CLIP', 'TRIAL_SESSION', 'PHYSICAL_TEST'
    metric_name: Mapped[str] = mapped_column(String(60), nullable=False)  # e.g., '140+ KPH Bowled In Death', 'Yo-Yo Test Score'
    metric_value: Mapped[str] = mapped_column(String(100), nullable=False)
    source_reference: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)

    # Relationships
    evaluation: Mapped["ScoutingEvaluationModel"] = relationship("ScoutingEvaluationModel", back_populates="evidence_items")


class PlayerComparisonModel(Base):
    """Comparative benchmarking model between an uncapped prospect and an archetype/peer."""
    __tablename__ = "player_comparisons"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    subject_player_id: Mapped[str] = mapped_column(String(36), ForeignKey("players.id", ondelete="CASCADE"), nullable=False, index=True)
    benchmark_player_id: Mapped[str] = mapped_column(String(36), ForeignKey("players.id", ondelete="CASCADE"), nullable=False, index=True)
    comparison_context: Mapped[str] = mapped_column(String(80), nullable=False)  # e.g., 'SMAT_2024_DEATH_HITTING'
    similarity_score: Mapped[float] = mapped_column(Float, default=0.0)  # Cosine / normalized similarity (0.0 - 1.0)
    comparison_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)

    __table_args__ = (
        UniqueConstraint("subject_player_id", "benchmark_player_id", "comparison_context", name="uq_player_benchmark_context"),
    )

    subject_player: Mapped["PlayerModel"] = relationship("PlayerModel", foreign_keys=[subject_player_id])
    benchmark_player: Mapped["PlayerModel"] = relationship("PlayerModel", foreign_keys=[benchmark_player_id])
