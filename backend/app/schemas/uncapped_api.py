"""
Royals Intelligence - Uncapped Players & Analytics API Schemas
Pydantic contracts for player search, eligibility verification, career analytics,
and proprietary data ingestion.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class IdentityItem(BaseModel):
    """External source identifier for a player."""
    source_name: str
    external_player_id: str
    confidence_score: float = 1.0


class UncappedPlayerSummary(BaseModel):
    """Player roster card for scouting and auction rosters."""
    id: str
    canonical_id: str
    full_name: str
    known_as: Optional[str] = None
    dob: Optional[str] = None
    calculated_age: Optional[float] = None
    home_state_association: Optional[str] = None
    primary_role: Optional[str] = None
    batting_hand: Optional[str] = None
    bowling_style: Optional[str] = None
    is_capped: bool = False
    eligibility_status: str = "PENDING_VERIFICATION"
    scouting_tier: str = "MONITOR"
    is_rr_trialist: bool = False


class UncappedPlayerDetail(UncappedPlayerSummary):
    """Full player detail with identities and eligibility verification history."""
    identities: List[IdentityItem] = Field(default_factory=list)
    dob_source: Optional[str] = None
    dob_verified: bool = False
    verification_notes: Optional[str] = None
    reference_date_used: Optional[str] = None
    eligibility_rule_source: Optional[str] = None
    rule_version: Optional[str] = None
    international_caps_detail: Optional[str] = None
    created_at: str


class EligibilityVerificationRequest(BaseModel):
    """Request to update or manually verify a player's uncapped eligibility."""
    new_status: str = Field(..., description="CONFIRMED_UNCAPPED, SUSPECTED_CAPPED, INELIGIBLE_OVERAGE, PENDING_VERIFICATION, FLAGGED_CONFLICT")
    verification_notes: str = Field(..., description="Audit justification and source proof")
    verified_by: str = Field(default="RR_LEAD_SCOUT")


class EligibilityVerificationResponse(BaseModel):
    """Result of an eligibility verification operation."""
    player_id: str
    full_name: str
    previous_status: str
    updated_status: str
    verified_at: str
    verification_notes: str


class EvaluationResponse(BaseModel):
    """Scout evaluation record with role-based data masking applied."""
    id: str
    uncapped_profile_id: str
    scout_identifier: str
    evaluation_date: str
    competition_or_trial: str
    technical_skill_rating: float
    temperament_rating: float
    athleticism_rating: float
    tactical_iq_rating: float
    ceiling_potential_rating: float
    strengths_summary: str
    development_areas: str
    scout_recommendation: str
    proprietary_notes: Optional[str] = None
    data_classification: str = "RR_PROPRIETARY_CONFIDENTIAL"
