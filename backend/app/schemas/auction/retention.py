"""
Royals Intelligence - AUCTION-05: Retention Engine Pydantic Schemas.

Defines data contracts for retention candidate eligibility, multi-dimensional
scoring components, explainability records, sensitivity analysis, and final recommendations.
"""

from enum import Enum
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field


class RetentionEligibilityStatus(str, Enum):
    """Audited pre-auction 2027 contract status."""
    VERIFIED_CURRENT_CONTRACT = "VERIFIED_CURRENT_CONTRACT"
    PENDING_VERIFICATION = "PENDING_VERIFICATION"
    VERIFIED_TRADED = "VERIFIED_TRADED"
    VERIFIED_RELEASED = "VERIFIED_RELEASED"
    WITHDRAWN = "WITHDRAWN"


class SampleConfidenceTier(str, Enum):
    """Confidence tier based on legal deliveries faced/bowled."""
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    NO_DATA = "NO_DATA"


class DimensionScore(BaseModel):
    """Individual score for one of the 7 retention dimensions."""
    dimension_name: str = Field(..., description="Name of the retention evaluation dimension")
    raw_metric_summary: str = Field(..., description="Descriptive summary of the raw empirical metric")
    normalized_score: float = Field(..., ge=0.0, le=100.0, description="Normalized score on [0, 100] scale")
    provisional_weight: float = Field(..., ge=0.0, le=1.0, description="Provisional model weight")
    weighted_score: float = Field(..., ge=0.0, le=100.0, description="Normalized score multiplied by weight")
    definition: str = Field(..., description="Mathematical or domain definition of the dimension")
    evidence_provenance: str = Field(..., description="Source table or artifact provenance")


class RetentionCandidateProfile(BaseModel):
    """Comprehensive retention evaluation profile for a candidate."""
    canonical_id: int = Field(..., description="Unique canonical player identifier")
    canonical_key: str = Field(..., description="Stable canonical key (e.g. RR-PLAYER-06819)")
    canonical_name: str = Field(..., description="Canonical player name")
    squad_role: str = Field(..., description="Primary squad role from verified registry")
    batting_style: Optional[str] = Field(None, description="Batting handedness/style")
    bowling_style: Optional[str] = Field(None, description="Bowling style if applicable")
    verified_age: Optional[float] = Field(None, description="Verified chronological age (None if unverified)")
    international_cap_status: str = Field(..., description="Senior international cap status from AUCTION-02")
    eligibility_status: RetentionEligibilityStatus = Field(..., description="Audited 2027 contract eligibility")
    is_eligible_for_retention: bool = Field(..., description="Whether player is in the active retention candidate pool")
    
    # 7 Dimension scores
    performance_score: DimensionScore = Field(..., description="Player Performance & Impact score")
    scarcity_score: DimensionScore = Field(..., description="Squad Role Scarcity score")
    replacement_difficulty_score: DimensionScore = Field(..., description="Replacement Difficulty score")
    squad_balance_score: DimensionScore = Field(..., description="Squad Balance Contribution score")
    age_career_stage_score: DimensionScore = Field(..., description="Age and Career Stage score")
    reliability_score: DimensionScore = Field(..., description="Performance Consistency & Reliability score")
    sample_confidence_score: DimensionScore = Field(..., description="Evidence Confidence & Sample Adequacy score")

    # Composite & Ranking
    composite_retention_score: float = Field(..., ge=0.0, le=100.0, description="Final weighted composite retention score")
    retention_rank: int = Field(..., ge=1, description="Rank within the eligible candidate pool")
    is_recommended_retention: bool = Field(..., description="True if within the exactly 3 recommended retentions")

    # Explainability fields
    sample_confidence_tier: SampleConfidenceTier = Field(..., description="Sample confidence level")
    legal_deliveries_evaluated: int = Field(..., description="Total legal balls faced and/or bowled")
    replacement_difficulty_level: str = Field(..., description="HIGH, VERY_HIGH, EXTREME, MODERATE, or LOW")
    key_strengths: List[str] = Field(default_factory=list, description="Primary empirical strengths")
    key_weaknesses_or_risks: List[str] = Field(default_factory=list, description="Primary empirical risks or limitations")
    retention_rationale: str = Field(..., description="Detailed explanation of rank relative to peers")
    sensitivity_and_uncertainty_notes: str = Field(..., description="Sensitivity to weight adjustments and uncertainties")
    evidence_provenance: str = Field(..., description="Provenance citations for all data points")


class SensitivityScenarioResult(BaseModel):
    """Result of perturbing model weights to evaluate top-3 retention stability."""
    scenario_name: str = Field(..., description="Scenario identifier (e.g. 'Performance Heavy', 'Age Heavy')")
    weights: Dict[str, float] = Field(..., description="Perturbed weight configuration")
    recommended_player_ids: List[int] = Field(..., description="Canonical IDs of top 3 players under this scenario")
    recommended_player_names: List[str] = Field(..., description="Names of top 3 players under this scenario")
    is_top_3_invariant: bool = Field(..., description="True if identical set of 3 players as baseline")
    rank_order_changes: Dict[str, int] = Field(default_factory=dict, description="Rank changes for top candidates")


class RetentionRecommendationDossier(BaseModel):
    """Master output dossier containing the 3 recommendations and full squad audit."""
    execution_timestamp: str = Field(..., description="ISO 8601 execution timestamp")
    active_2026_squad_count: int = Field(25, description="Active squad baseline count")
    verified_eligible_pool_count: int = Field(..., description="Count of players with VERIFIED_CURRENT_CONTRACT")
    quarantined_pending_count: int = Field(..., description="Count of players pending 2027 contract verification")
    excluded_traded_count: int = Field(..., description="Count of traded-out players")
    excluded_released_count: int = Field(..., description="Count of pre-auction released players")
    
    baseline_weights: Dict[str, float] = Field(..., description="Provisional baseline weights")
    recommended_retentions: List[RetentionCandidateProfile] = Field(..., description="Exactly 3 recommended retentions")
    eligible_candidate_pool: List[RetentionCandidateProfile] = Field(..., description="All ranked eligible candidates")
    quarantined_candidates: List[Dict[str, Any]] = Field(default_factory=list, description="Quarantined candidate records")
    sensitivity_scenarios: List[SensitivityScenarioResult] = Field(default_factory=list, description="Sensitivity analysis scenarios")
    governance_notes: List[str] = Field(default_factory=list, description="Regulatory and governance boundary notes")
