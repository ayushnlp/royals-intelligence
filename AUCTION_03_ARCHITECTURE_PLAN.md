# ROYALS INTELLIGENCE — AUCTION-03 ARCHITECTURE PLAN
## System Design, Data Schemas, API Contracts & Frontend Integration Architecture

**Document Version:** 3.0.0 (Reconciled with 2026 Baseline & Official Trade Data)  
**Phase:** RR Auction & Retention Intelligence Expansion  
**Stage:** `AUCTION-03` — Final Current-Squad Reconciliation and Retention Candidate Audit  
**Git Baseline Branch:** `main` | **HEAD:** `0f24302c61e3d4c070d0e669fc152830c9b2c4e1`  
**Execution Timestamp:** 2026-11-17T00:07:00+05:30  
**Status:** REVISED ARCHITECTURE FORMALIZED — IMPLEMENTATION LOCKED

---

## 1. System Topology & Architectural Guardrails

The **Retention Intelligence & Salary Cap Engine** consumes canonical player identities (AUCTION-01), format-by-format eligibility states (AUCTION-02), and pressure performance baselines (Round 1) to model decision-support retention recommendations and salary-cap allocations.

### 1.1 Strict Boundary Rules:
- **Candidate Pool Restriction:** Only players with status **`VERIFIED_CURRENT_CONTRACT`** (currently 11 players) are fed into the retention recommendation scoring pipeline.
- **Financial Metric Integrity:** The engine maintains absolute separation between **Total Salary Cap (₹157 Cr)**, **Auction Purse**, **Match-Fee Reserves**, and **Committed Salaries**. It never subtracts player contracts directly from ₹157.00 Crore.
- **Three-Player Directive:** Handled as a platform product requirement, not a statutory BCCI ceiling.

---

## 2. Revised Data Schemas (Pydantic Models)

### 2.1 Current Squad Verification Schema (`CurrentSquadVerificationRecord`)
```python
from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum

class PreAuction2027ContractStatus(str, Enum):
    VERIFIED_CURRENT_CONTRACT = "VERIFIED_CURRENT_CONTRACT"
    VERIFIED_RELEASED = "VERIFIED_RELEASED"
    VERIFIED_TRADED = "VERIFIED_TRADED"
    PENDING_VERIFICATION = "PENDING_VERIFICATION"
    CONFLICTING_EVIDENCE = "CONFLICTING_EVIDENCE"

class CurrentSquadVerificationRecord(BaseModel):
    """Authoritative contracted squad record for Rajasthan Royals (2026 baseline & 2027 contract)."""
    canonical_id: int = Field(..., description="Stable internal player ID from AUCTION-01")
    canonical_key: str = Field(..., description="Formatted canonical key (e.g. RR-PLAYER-06819)")
    player_name: str = Field(..., description="Canonical player name")
    tactical_role: str = Field(..., description="Batter, Bowler, All-rounder, Wicketkeeper")
    senior_cap_status: str = Field(..., description="AUCTION-02 status: VERIFIED_CAPPED or VERIFIED_UNCAPPED")
    is_overseas: bool = Field(..., description="Whether player occupies an overseas player slot")
    
    # Tripartite status fields separating 2026 squad, 2027 contract, and retention decisions
    ipl_2026_squad_status: str = Field(..., description="ACTIVE_SQUAD, WITHDRAWN, TRADED_OUT, RELEASED, or NOT_IN_SQUAD")
    pre_auction_2027_contract_status: PreAuction2027ContractStatus = Field(..., description="Mandated 2027 contract eligibility state")
    ipl_2027_retention_decision: str = Field(default="PENDING_DECISION", description="RETAINED, RELEASED, TRADED, or PENDING_DECISION")
    
    contract_entry_type: str = Field(..., description="PRE_AUCTION_RETAINED, AUCTION_PURCHASED, TRADED, or UNCONFIRMED")
    contract_salary_inr_cr: Optional[float] = Field(None, description="Annual contract value in Crores INR")
    verification_source: str = Field(..., description="Official BCCI / IPL registry reference")
    verification_url: str = Field(..., description="Authoritative announcement URL")
    verification_date: str = Field(..., description="ISO 8601 date of contract verification")
    governance_notes: Optional[str] = Field(None, description="Contextual notes or trade caveats")
```

### 2.2 Retention Evaluation & Recommendation Schema (`RetentionCandidateEvaluation`)
```python
class RetentionCandidateEvaluation(BaseModel):
    """Multi-criteria evaluation record for an eligible RR retention candidate."""
    canonical_id: int
    canonical_name: str
    tactical_role: str
    senior_cap_status: str
    contract_salary_inr_cr: float
    
    # Quantitative evaluation metrics (strictly PROVISIONAL until calibrated)
    pressure_index: float = Field(..., description="Composite pressure reliability score (0-100)")
    tactical_scarcity_score: float = Field(..., description="Market scarcity index (0-100)")
    estimated_valuation_inr_cr: float = Field(..., description="Algorithmic open-market valuation")
    surplus_value_inr_cr: float = Field(..., description="Estimated Valuation minus Contract Salary")
    age_trajectory_score: float = Field(..., description="Age and peak projection score (0-100)")
    
    # Composite score and recommendation
    composite_retention_score: float = Field(..., description="Weighted multi-criteria score (0-100)")
    recommendation_rank: Optional[int] = Field(None, description="Rank within eligible candidate pool")
    is_recommended_retention: bool = Field(False, description="True for exactly the top 3 selections")
    recommendation_rationale: str = Field(..., description="Evidence-backed strategic justification")
    methodology_caveats: str = Field(default="Weights and scores are provisional pending sensitivity analysis.")
```

### 2.3 Salary Cap Simulation Schema (`SalaryCapSimulationResponse`)
```python
class SalaryCapSimulationResponse(BaseModel):
    """Output contract for salary cap and purse allocation simulations."""
    total_salary_cap_inr_cr: float = Field(157.0, description="Gross authorized 2027 BCCI Total Salary Cap")
    base_auction_purse_inr_cr: float = Field(..., description="Provisional or ratified auction purse pool")
    match_fee_expenditure_inr_cr: float = Field(12.60, description="Mandated match-fee reserve (14 matches x 12 players)")
    performance_pay_allowance_inr_cr: float = Field(..., description="Reserved performance incentive allowance")
    
    # Retention outlays and net purse
    retention_mode: str = Field(..., description="CONTRACT_PASS_THROUGH_ASSUMPTION or SIMULATED_SLABS_SCENARIO")
    retained_player_count: int = Field(3, description="Platform recommendation count")
    retained_players: List[RetentionCandidateEvaluation]
    committed_retention_salaries_inr_cr: float = Field(..., description="Sum of retained base salaries")
    remaining_available_auction_purse_inr_cr: float = Field(..., description="Net capital available for auction: Purse minus Retentions")
    
    # Squad construction limits
    roster_slots_remaining: int = Field(..., description="Target squad size (25) minus retentions")
    overseas_slots_remaining: int = Field(..., description="Overseas limit (8) minus retained overseas")
    budget_per_remaining_slot_inr_cr: float = Field(..., description="Average purchasing power per remaining slot")
    disclaimer: str = Field(
        default="Total Salary Cap (₹157 Cr) includes match fees and performance pay. "
                "Net auction purse is derived strictly from auction purse allocations."
    )
```

---

## 3. Revised Backend API Endpoints (FastAPI)

1. `GET /api/v1/auction/retention/squad`
   - Returns the complete RR tracking roster (20 players) with their discrete `verification_state` (`VERIFIED_CURRENT_CONTRACT`, `CONFLICTING_EVIDENCE`, `PENDING_VERIFICATION`).
   - Query filters: `state` (e.g. `?state=VERIFIED_CURRENT_CONTRACT`).
2. `GET /api/v1/auction/retention/recommendations`
   - Returns the **11 eligible contracted players** ranked by retention value, highlighting the **top 3 recommended retentions** under the platform mandate.
   - Includes full provisional weight disclosures and sensitivity notes.
3. `POST /api/v1/auction/retention/simulate`
   - Real-time purse simulation endpoint allowing management to test any combination of retentions against purse parameters.

---

## 4. Frontend Integration & Layout (`/retention`)

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│ ROYALS INTELLIGENCE — RR RETENTION INTELLIGENCE & SALARY CAP (IPL 2027)         │
├──────────────────────────────────────────────────────────────────────────────────┤
│ [Top 3 Recommended Retentions (Platform Recommendation)]                         │
│  ┌──────────────────────┐  ┌──────────────────────┐  ┌──────────────────────┐   │
│  │ #1 Yashasvi Jaiswal  │  │ #2 Riyan Parag       │  │ #3 Dhruv Jurel       │   │
│  │ Top-Order Batter     │  │ All-Rounder          │  │ Wkt-Batter           │   │
│  │ Contract: ₹18.00 Cr  │  │ Contract: ₹14.00 Cr  │  │ Contract: ₹14.00 Cr  │   │
│  │ Status: VERIFIED     │  │ Status: VERIFIED     │  │ Status: VERIFIED     │   │
│  └──────────────────────┘  └──────────────────────┘  └──────────────────────┘   │
├──────────────────────────────────────────────────────────────────────────────────┤
│ [Financial Framework Overview Bar]                                               │
│  Total Salary Cap: ₹157.00 Cr (Gross)                                            │
│  ├─ Match Fee Reserve: ₹12.60 Cr (14 Matches x 12 Players @ ₹7.5L)               │
│  ├─ Performance Pay Allowance: Reserved                                          │
│  └─ Auction Purse Allocation: Dedicated Pool                                     │
│     ├─ Committed Retentions: ₹46.00 Cr                                           │
│     └─ Net Available Auction Purse: Net Capital for Open Bidding                 │
├──────────────────────────────────────────────────────────────────────────────────┤
│ [Tabs: (1) Verified Squad Matrix  (2) Quarantined / Pending  (3) Purse Sim]     │
│  - Tab 1: 11 VERIFIED_CURRENT_CONTRACT players eligible for retention            │
│  - Tab 2: Sanju Samson (CONFLICTING_EVIDENCE) & 8 PENDING_VERIFICATION entries   │
│  - Tab 3: Interactive purse simulator with dynamic slot budgeting               │
└──────────────────────────────────────────────────────────────────────────────────┘
```

> [!IMPORTANT]
> **Implementation Lock:**  
> All architecture components remain locked until formal approval of the planning phase is granted.
