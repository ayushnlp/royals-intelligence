"""
Royals Intelligence - RR Auction & Retention Intelligence
Pydantic v2 Schemas for Canonical Player Identity and Candidate Universe.
Stage: AUCTION-01
"""

from typing import Optional, List, Dict, Any, Set
from pydantic import BaseModel, Field


class PlayerIdentityMapping(BaseModel):
    """Canonical mapping entry for an individual player identity."""
    canonical_id: int = Field(..., description="Stable internal canonical player ID (source integer)")
    canonical_key: str = Field(..., description="Globally unique namespaced canonical key, e.g. RR-PLAYER-07503")
    canonical_name: str = Field(..., description="Standardized canonical display name")
    source_player_ids: List[int] = Field(default_factory=list, description="Original source IDs from match datasets")
    source_record_indices: Dict[str, List[int]] = Field(default_factory=dict, description="Row indices across source datasets")
    aliases: List[str] = Field(default_factory=list, description="Spelling variants and name permutations")
    
    # Supplied Reference CSV Attributes (ipl_players.csv)
    supplied_csv_team: Optional[str] = None
    supplied_csv_age: Optional[int] = None
    supplied_csv_role: Optional[str] = None
    batting_style: Optional[str] = None
    bowling_style: Optional[str] = None
    spin_type: Optional[str] = None
    
    # Franchise & Tournament Participation (2022-2026 data pack)
    historical_ipl_matches: int = 0
    historical_t20i_matches: int = 0
    historical_franchises: List[str] = Field(default_factory=list)
    is_rr_historical_player: bool = False
    is_rr_supplied_csv_roster: bool = False
    
    # Contract & Retention State (Strictly Decoupled)
    verified_current_rr_squad: str = "UNCONFIRMED_PENDING_BCCI_CIRCULAR"
    contract_retention_status: str = "PENDING_OFFICIAL_FILING"
    auction_registration_status: str = "PENDING_OFFICIAL_IPL_2027_LONGLIST"
    
    # Senior International Eligibility Certification
    senior_test_caps: Optional[int] = None
    senior_odi_caps: Optional[int] = None
    senior_t20i_caps: Optional[int] = None
    cap_certification_status: str = Field(
        ...,
        description="One of: VERIFIED_UNCAPPED, VERIFIED_CAPPED, PENDING_VERIFICATION, CONFLICTING_EVIDENCE"
    )
    cap_evidence_notes: str = ""
    
    # Identity & Roster Conflicts
    has_identity_conflict: bool = False
    conflict_notes: Optional[str] = None
    
    # Provenance
    provenance_sources: List[str] = Field(default_factory=list)


class CandidateUniverseSummary(BaseModel):
    """High-level metrics for the candidate universe."""
    total_canonical_players: int
    total_ipl_historical_players: int
    total_supplied_csv_players: int
    verified_uncapped_count: int
    verified_capped_count: int
    pending_verification_count: int
    conflicting_evidence_count: int
    rr_historical_core_count: int
    rr_supplied_csv_count: int
    audit_stage: str = "AUCTION-01"
    governing_dataset: str = "Official Rajasthan Royals Round 1 Competition Data Pack + ipl_players.csv"
