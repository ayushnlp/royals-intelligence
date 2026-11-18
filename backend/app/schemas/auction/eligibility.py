"""
Royals Intelligence - RR Auction & Retention Intelligence
Pydantic v2 Schemas for Senior International Eligibility Verification.
Stage: AUCTION-02
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class FormatAppearanceEvidence(BaseModel):
    """Detailed appearance evidence for a specific international cricket format."""
    format_name: str = Field(..., description="Format: 'Test', 'ODI', or 'T20I'")
    appearance_status: str = Field(
        ...,
        description="One of: 'PLAYED_APPEARANCE', 'SQUAD_BENCH_ONLY', 'ZERO_APPEARANCES', 'UNCONFIRMED'"
    )
    caps_count: Optional[int] = Field(default=None, description="Official career cap number or match appearances")
    debut_date: Optional[str] = Field(default=None, description="Date of international debut if appeared")
    debut_match: Optional[str] = Field(default=None, description="Opponent or series of debut")
    source_authority: str = Field(..., description="Governing authority (e.g. BCCI, ICC, ESPNcricinfo, Cricsheet)")
    source_url: Optional[str] = Field(default=None, description="Authoritative reference URL or dataset path")
    evidence_notes: str = Field(default="", description="Detailed factual record of evidence or absence")


class PlayerSeniorEligibilityRecord(BaseModel):
    """Comprehensive player-level senior international eligibility record."""
    canonical_id: int = Field(..., description="Stable internal canonical player ID")
    canonical_key: str = Field(..., description="Globally unique namespaced canonical key, e.g. RR-PLAYER-07503")
    canonical_name: str = Field(..., description="Standardized canonical display name")
    aliases: List[str] = Field(default_factory=list, description="Known spelling variants and name permutations")
    
    # Independent Format Evidence
    test_evidence: FormatAppearanceEvidence
    odi_evidence: FormatAppearanceEvidence
    t20i_evidence: FormatAppearanceEvidence
    
    # Senior International Eligibility Classification
    final_eligibility_state: str = Field(
        ...,
        description="One of: 'VERIFIED_UNCAPPED', 'VERIFIED_CAPPED', 'PENDING_VERIFICATION', 'CONFLICTING_EVIDENCE'"
    )
    
    # Audit Traceability
    primary_authority: str = Field(..., description="Primary certifying authority")
    source_url: Optional[str] = Field(default=None, description="Authoritative source reference")
    verification_timestamp: str = Field(default="2026-11-16T23:20:00+05:30")
    reviewer_notes: str = Field(default="", description="Reviewer justification and selection vs appearance audit")
    unresolved_limitations: Optional[str] = Field(default=None, description="Known gaps or pending external verifications")


class EligibilityLedgerSummary(BaseModel):
    """Aggregate statistics for AUCTION-02 Senior International Eligibility Ledger."""
    total_canonical_players: int
    verified_capped_count: int
    verified_uncapped_count: int
    pending_verification_count: int
    conflicting_evidence_count: int
    test_capped_count: int
    odi_capped_count: int
    t20i_capped_count: int
    bench_only_squad_callups_count: int
    audit_stage: str = "AUCTION-02"
    governing_rules: str = "BCCI & ICC Official Senior International Cap Standards (Test, ODI, T20I)"
