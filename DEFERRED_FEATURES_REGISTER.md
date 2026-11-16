# ROYALS INTELLIGENCE — DEFERRED FEATURES REGISTER
## Comprehensive Inventory of Out-of-Scope, Extra, and Preserved Components

**Document Classification:** Authoritative Scope Control & Preservation Register  
**Platform Version:** ROYALS INTELLIGENCE v4.2  
**Audit Timestamp:** 2026-11-17T01:54:00+05:30  
**Current Git Baseline:** Branch `main` | HEAD `0f24302c61e3d4c070d0e669fc152830c9b2c4e1`  
**Governance Policy:** STRICT PRESERVATION — ZERO CODE DELETION

---

## 1. Governance Principles & Status Definitions

This register documents every feature, module, API, and architectural track that is **not part of the mandatory SupeRR Selector Season 2 Round 1 Pressure Challenge submission**, but which exists or was planned in the repository.

### Governing Status Codes:
* **`PRESERVED / DEFERRED`**: Fully or partially implemented, tested, and operational in the codebase, but intentionally excluded from the primary Round 1 submission scope to prevent scope bloat and submission distraction. **All code, schemas, endpoints, and datasets remain 100% intact.**
* **`DEFERRED / PENDING`**: Conceptually planned or architected in historical roadmaps, but with zero implementation code written. Postponed to post-Round 1 development.
* **`DEFERRED / BLOCKED`**: Fully specified in architecture planning documents, but explicitly blocked from implementation until official user authorization (e.g., R1-07.1 through R1-07.4).

---

## 2. Track 1: Rajasthan Royals Auction & Retention Intelligence (IPL 2027)

This track was developed to evaluate mega-auction player valuation, squad retention governance, and international cap certification. It is completely independent of the Round 1 Pressure Analytics challenge.

| Feature ID | Feature Name | Implementation Status | Existing Files & Locations | Existing Tests | Reason Outside Round 1 | Recommended Future Phase |
| :--- | :--- | :---: | :--- | :--- | :--- | :--- |
| **AUCTION-00** | Data Ingestion & Discrepancies Audit | **PRESERVED / DEFERRED** | `AUCTION_00_*.md` (7 reports) | Data QA verification scripts | Data audit for auction registry; Round 1 uses raw CSVs directly. | Round 2 (Auction Engine) |
| **AUCTION-01** | Canonical Player Identity Registry | **PRESERVED / DEFERRED** | `backend/app/auction_intelligence/identity/`, `canonical_player_registry.parquet` (1,217 players) | `test_auction_01_identity.py` (11 tests passed) | Identity deduplication across 1,217 players; Round 1 uses qualified pool of 517. | Round 2 (Auction Engine) |
| **AUCTION-02** | Senior International Eligibility Ledger | **PRESERVED / DEFERRED** | `backend/app/auction_intelligence/eligibility/`, `senior_international_eligibility_ledger.parquet` | `test_auction_02_eligibility.py` (10 tests passed) | 3-format Test/ODI/T20I cap verification (26 uncapped); Round 1 evaluates performance regardless of cap. | Round 2 (Auction Engine) |
| **AUCTION-03** | RR Retention Governance & 2026 Squad Baseline | **PRESERVED / DEFERRED** | `AUCTION_03_*.md` (7 reports) | Squad audit verification | Franchise salary cap rules (₹157 Cr) & Samson CSK trade; outside pressure scope. | Round 2 (Auction Engine) |
| **AUCTION-04** | Historical Performance & Competition Normalization | **PRESERVED / DEFERRED** | `backend/app/auction_intelligence/normalization/`, `normalized_batting_performance.parquet`, `normalized_bowling_performance.parquet` | `test_auction_04_normalization.py` (11 tests passed) | Bayesian competition scoring environment normalization for auction pricing. | Round 2 (Auction Engine) |
| **AUCTION-05** | RR Retention Decision Engine (Top 3 Retentions) | **PRESERVED / DEFERRED** | `backend/app/auction_intelligence/retention/`, `rr_retention_recommendations.parquet`, `rr_retention_candidates.parquet` | `test_auction_05_retention.py` (10 tests passed) | Recommends 3 retentions (Jaiswal, Parag, Jurel); Round 1 requires Top 10 Batters/Bowlers under pressure. | Round 2 (Auction Engine) |
| **AUCTION-06** | Uncapped Batting Intelligence Engine | **DEFERRED / PENDING** | Planned in `docs/RR_AUCTION_...md` | None | Dedicated uncapped batting valuation for auction bidding. | Round 2 (Auction Engine) |
| **AUCTION-07** | Uncapped Bowling Intelligence Engine | **DEFERRED / PENDING** | Planned in `docs/RR_AUCTION_...md` | None | Dedicated uncapped bowling valuation for auction bidding. | Round 2 (Auction Engine) |
| **AUCTION-08** | Multi-Role Valuation & Auction Pricing | **DEFERRED / PENDING** | Planned in `docs/RR_AUCTION_...md` | None | Dynamic base price and fair auction valuation model. | Round 2 (Auction Engine) |
| **AUCTION-09** | Purse Allocation & Bidding War Simulator | **DEFERRED / PENDING** | Planned in `docs/RR_AUCTION_...md` | None | Simulation of opponent bidding behaviors and purse depletion. | Round 2 (Auction Engine) |
| **AUCTION-10** | Live Auction Day Recommendation System | **DEFERRED / PENDING** | Planned in `docs/RR_AUCTION_...md` | None | Real-time war room recommendation tool. | Round 2 (Auction Engine) |
| **AUCTION-11** | Full-Stack Auction UI Dashboard | **DEFERRED / PENDING** | Planned in `docs/RR_AUCTION_...md` | None | Dedicated auction war-room frontend interface. | Round 2 (Auction Engine) |
| **AUCTION-12** | End-to-End System Integration Audit | **DEFERRED / PENDING** | Planned in `docs/RR_AUCTION_...md` | None | Full pipeline audit across auction services. | Round 2 (Auction Engine) |
| **AUCTION-13** | Executive Dossier & Presentation | **DEFERRED / PENDING** | Planned in `docs/RR_AUCTION_...md` | None | Final executive deck for franchise management. | Round 2 (Auction Engine) |

---

## 3. Track 2: Advanced Tactical Cricket Intelligence (Stage 5–13)

Features originating from the historical 14-stage platform roadmap that provide deep tactical analytics, lineup optimization, or match simulation:

| Feature Name | Implementation Status | Existing Files & Locations | Existing Tests | Reason Outside Round 1 | Recommended Future Phase |
| :--- | :---: | :--- | :--- | :--- | :--- |
| **Radar Speed & Telemetry Analytics** | **PRESERVED / DEFERRED** | `backend/app/analytics/dataset_cricket_intelligence.py`, `backend/app/schemas/tactical.py` | `test_dataset_cricket_intelligence.py` (9 tests passed) | Analyzes `bowl_speed` radar telemetry and variations; Round 1 focuses on pressure impact. | Stage 5 Tactical Expansion |
| **10 Tactical REST Endpoints** | **PRESERVED / DEFERRED** | `backend/app/api/v1/endpoints/tactical.py` | `test_tactical_api.py` (28 tests passed) | Provides radar speed, phase splits, stroke types, bowling styles. | Stage 5 Tactical Expansion |
| **Tactical Dashboard UI (`/tactical`)** | **PRESERVED / DEFERRED** | `frontend/src/app/tactical/page.tsx` | Next.js compilation | Interactive tactical dashboard; beyond Round 1 submission scope. | Stage 5 Tactical Expansion |
| **Uncapped Player Intelligence API & UI** | **PRESERVED / DEFERRED** | `backend/app/analytics/uncapped_pressure_intelligence.py`, `backend/app/api/v1/endpoints/uncapped.py`, `frontend/src/app/uncapped/page.tsx` | `test_uncapped_api.py` (5 tests), `test_uncapped_pressure_api.py` (4 tests) | Dedicated uncapped filtering; Round 1 evaluates all qualified players uniformly. | Future Commercial Track |
| **Domestic Season & Match Intelligence** | **PRESERVED / DEFERRED** | `backend/app/api/v1/endpoints/domestic.py`, `frontend/src/app/domestic/page.tsx` | `test_domestic_intelligence.py` (8 tests passed) | Domestic tournament profiling; Round 1 is IPL + T20I focused. | Platform Expansion |
| **Venue, Pitch & Weather Intelligence** | **PRESERVED / DEFERRED** | `backend/app/api/v1/endpoints/venues.py`, `weather.py` | `test_venue_pitch_weather.py` (9 tests passed) | Venue condition modeling; supplementary to core pressure index. | Platform Expansion |
| **Data Acquisition Service** | **PRESERVED / DEFERRED** | `backend/app/api/v1/endpoints/acquisition.py`, `backend/app/services/acquisition/` | `test_acquisition.py` (18 tests passed) | External feed ingestion; Round 1 is anchored to provided static data pack. | Platform Expansion |
| **Granular H2H Matchup Engine (Stage 6)** | **DEFERRED / PENDING** | Planned in `docs/REVISED_14_STAGE_ROADMAP.md` | None | Ball-by-ball batter vs bowler matchup matrix. | Post-Round 1 Stage 6 |
| **Playing XI & Impact Player Optimizer (Stage 7)** | **DEFERRED / PENDING** | Planned in `docs/REVISED_14_STAGE_ROADMAP.md` | None | Tactical substitution & lineup optimizer. | Post-Round 1 Stage 7 |
| **Opposition Scouting Engine (Stage 8)** | **DEFERRED / PENDING** | Planned in `docs/REVISED_14_STAGE_ROADMAP.md` | None | Automated opponent pre-match briefing generator. | Post-Round 1 Stage 8 |
| **In-Season Match Simulation / WPA (Stage 9)** | **DEFERRED / PENDING** | Planned in `docs/REVISED_14_STAGE_ROADMAP.md` | None | Monte Carlo win probability added simulator. | Post-Round 1 Stage 9 |
| **Emerging Talent Discovery Engine (Stage 10)** | **DEFERRED / PENDING** | Planned in `docs/REVISED_14_STAGE_ROADMAP.md` | None | Algorithmic talent discovery without synthetic DOBs. | Post-Round 1 Stage 10 |
| **Tactical Counterfactual Sandbox (Stage 11)** | **DEFERRED / PENDING** | Planned in `docs/REVISED_14_STAGE_ROADMAP.md` | None | "What-if" scenario evaluation tool. | Post-Round 1 Stage 11 |
| **Squad Construction & Roster Balance (Stage 12)**| **DEFERRED / PENDING** | Planned in `docs/REVISED_14_STAGE_ROADMAP.md` | None | Multi-constraint integer programming squad builder. | Post-Round 1 Stage 12 |
| **Enterprise Hardening & Caching (Stage 13)** | **DEFERRED / PENDING** | Planned in `docs/REVISED_14_STAGE_ROADMAP.md` | None | Redis sub-second caching & cluster deployment. | Post-Round 1 Stage 13 |

---

## 4. Track 3: Advanced Reliability Research (R1-07.1–R1-07.4)

These sub-stages were architected in `reliability_framework_architecture_audit_pre_authorization.md` as advanced post-Round 1 extensions of the statistical reliability framework. **They remain strictly blocked from implementation until explicit user authorization.**

| Sub-Stage ID | Module Name | Implementation Status | Existing Planning Artifacts | Reason Blocked / Deferred |
| :--- | :--- | :---: | :--- | :--- |
| **R1-07.0** | Reliability Decision Framework Architecture Audit | **COMPLETE (PLANNING)** | `round1_pressure/reports/reliability_framework_architecture_audit_pre_authorization.md` | Planning document only; code implementation explicitly gated. |
| **R1-07.1** | Multi-Match Variance Decomposition & Situational Clustering | **DEFERRED / BLOCKED** | Specified in Section 13.2 of planning doc | Blocked by Safety Rule #12; requires explicit user sign-off. |
| **R1-07.2** | Two-Dimensional Reliability Classification Engine | **DEFERRED / BLOCKED** | Specified in Section 13.3 of planning doc | Blocked by Safety Rule #12; 2D matrix already reported in R1-06. |
| **R1-07.3** | Rolling-Origin Temporal & Transferability Validation | **DEFERRED / BLOCKED** | Specified in Section 13.4 of planning doc | Blocked by Safety Rule #12; historical validation already closed in R1-05. |
| **R1-07.4** | Operational Decision Cards & Final Reporting | **DEFERRED / BLOCKED** | Specified in Section 13.5 of planning doc | Blocked by Safety Rule #12; evidence profiles already generated in R1-06. |

---

## 5. Preservation Guarantee

* **Zero Deletions:** No existing code file, test file, schema, or documentation file has been removed or deprecated.
* **Full Reproducibility:** All preserved features remain fully importable and testable via their respective test suites (`pytest backend/tests/auction/`, `pytest backend/tests/test_tactical_api.py`, etc.).
* **Test Isolation:** The core Round 1 regression suite (`round1_pressure/tests/`, 196 tests) runs completely independently of all preserved and deferred modules.
