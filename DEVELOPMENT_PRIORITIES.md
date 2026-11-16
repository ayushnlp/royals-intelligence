# ROYALS INTELLIGENCE — DEVELOPMENT PRIORITIES & IMPLEMENTATION BACKLOG
**Platform:** ROYALS INTELLIGENCE v4.1  
**Target:** SupeRR Selector Season 2 — Round 1  
**Status:** Realigned & Authoritative  

---

## 1. Prioritization Framework & Governance Directives

All development priorities are strictly aligned with the **SupeRR Selector Season 2 Round 1 Challenge**:
1. Top 10 Batters Under Pressure
2. Top 10 Bowlers Under Pressure
3. Comprehensive Methodology & Empirical Evidence

### State Classifications Enforced:
- **COMPLETED:** Fully implemented, verified against official data, backed by automated tests, and sealed.
- **IMPLEMENTED BUT AWAITING VALIDATION:** Functional in code/API, undergoing final user acceptance or schema validation.
- **PENDING:** Prioritized for execution in the current or upcoming sprint to fulfill core challenge requirements.
- **OPTIONAL FUTURE RESEARCH:** Advanced statistical proposals (Phase 7) strictly segregated from locked competition rankings.

---

## 2. Priority Tiers & Implementation Backlog

### TIER 1: IMMEDIATE PRIORITY — Sprint 1
*Goal: Bridge the final presentation gap by bringing the sealed Round 1 Pressure Leaderboards and Candidate Evidence Profiles directly into the ROYALS INTELLIGENCE frontend.*

| Task ID | Task Title & Scope | Architectural Layer | Primary Deliverables | Status |
| :---: | :--- | :--- | :--- | :---: |
| **PRI-01** | **Round 1 Pressure REST API Router**<br>Expose locked Top 10 Batters, Top 10 Bowlers, and 20 candidate evidence profiles via `/api/v1/analytics/pressure/leaderboards` and `/api/v1/analytics/pressure/candidates/{player_id}`. | Backend API (`backend/app/api/v1/endpoints/pressure.py`) | FastAPI router, Pydantic schemas, unit tests | **COMPLETED** |
| **PRI-02** | **Pressure Intelligence Frontend Dashboard (`/pressure`)**<br>Implement dedicated interactive page displaying the official Top 10 Batters and Top 10 Bowlers Under Pressure with Conservative PRI, Credible Intervals, and qualification badges. | Frontend UI (`frontend/src/app/pressure/page.tsx`) | Leaderboard table, dual-discipline toggles, filter controls | **COMPLETED** |
| **PRI-03** | **Candidate Evidence Dossier Cards**<br>Interactive deep-dive modal showcasing candidate match leverage distribution, 11-question evidence fields, and baseline comparison. | Frontend Components (`frontend/src/app/pressure/page.tsx`) | Candidate evidence view, Q1–Q11 dossiers | **COMPLETED** |
| **PRI-04** | **Methodology & Limitations Report Viewer**<br>In-app interactive reader for methodology and limitations with baseline strata, shrinkage formulas, and qualification gates. | Frontend UI (`frontend/src/app/pressure/page.tsx`) | Methodology tab, 12-cell baseline breakdown | **COMPLETED** |

---

### TIER 2: HIGH PRIORITY — Sprint 2
*Goal: Realign the Platform Overview (`/`) and Sidebar Navigation to reflect the Round 1 challenge and Stage 5 Tactical achievements.*

| Task ID | Task Title & Scope | Architectural Layer | Primary Deliverables | Status |
| :---: | :--- | :--- | :--- | :---: |
| **PRI-05** | **System Overview Dashboard Realignment (`/`)**<br>Update the root landing page from generic Stage 0–3 placeholders to showcase the Round 1 Pressure Challenge status, Top 10 podium previews, and Stage 5 Tactical telemetry. | Frontend UI (`frontend/src/app/page.tsx`) | Hero banner realignment, Round 1 telemetry cards, podium widgets | **COMPLETED** |
| **PRI-06** | **Global Navigation Hierarchy Reordering**<br>Update `Sidebar.tsx` to elevate **"Pressure Intelligence (Round 1)"** and **"Tactical Intelligence (Stage 5)"** to the primary navigation group. | Frontend Layout (`frontend/src/components/layout/Sidebar.tsx`) | Reordered nav items, updated badges, active route matching | **COMPLETED** |
| **PRI-07** | **Tactical & Pressure Deep Linking**<br>Add direct cross-navigation links between `/tactical` and `/pressure` header bars and player dossiers. | Frontend Routing | One-click cross-navigation pills | **COMPLETED** |

---

### TIER 3: MEDIUM PRIORITY — Sprint 3
*Goal: Platform performance optimization, automated audit reports, and export capabilities.*

| Task ID | Task Title & Scope | Architectural Layer | Primary Deliverables | Status |
| :--- | :--- | :--- | :--- | :---: |
| **PRI-08** | **PDF Export for Official Submission Document**<br>Add automated markdown-to-PDF rendering script for `ROYALS_INTELLIGENCE_ROUND_1_SUBMISSION.md` for offline competition submission. | Reporting Scripts (`scripts/export_submission_pdf.py`) | Formatted PDF document with styled tables and charts | **PENDING** |
| **PRI-09** | **Sub-Second Caching for Tactical Endpoints**<br>Implement in-memory LRU caching on `DatasetCricketIntelligenceEngine` queries for instant UI filtering. | Backend Analytics (`backend/app/analytics/`) | Cached query responses, sub-50ms latency | **PENDING** |
| **PRI-10** | **End-to-End Cypress / Playwright Smoke Tests**<br>Automated browser test suite verifying `/tactical` and `/pressure` tabs, sliders, and selectors. | Frontend Testing (`frontend/tests/e2e/`) | E2E browser test suite | **PENDING** |

---

### TIER 4: LOW PRIORITY — Phase 7 Research (Optional Proposal)
*Goal: Theoretical advancements in multi-match variance decomposition. Strictly segregated from locked Round 1 rankings.*

| Task ID | Task Title & Scope | Architectural Layer | Primary Deliverables | Status |
| :--- | :--- | :--- | :--- | :---: |
| **PRI-11** | **Linear Mixed-Effects Multi-Match Variance Decomposition**<br>Fitting crossed random-effects models ($u_{\text{player}} + v_{\text{match}}$) to separate within-match leverage from between-match consistency. | Research Scripts (`round1_pressure/src/research/`) | Research report and variance decomposition plots | **OPTIONAL FUTURE RESEARCH** |
| **PRI-12** | **Cluster-Robust Variance Estimation**<br>Comparing Huber-White match-clustered standard errors with binomial ball-level variance. | Research Scripts (`round1_pressure/src/research/`) | Comparative sensitivity whitepaper | **OPTIONAL FUTURE RESEARCH** |
| **PRI-13** | **Situational Volatility Index (SVI)**<br>Formulating a secondary consistency index based on match-to-match coefficient of variation under pressure. | Analytical Formulation | Methodological proposal | **OPTIONAL FUTURE RESEARCH** |

---

## 3. Scope Boundary Audit: Retained vs Out-of-Scope Features

To maintain platform stability while keeping Round 1 deliverables front and center, existing legacy components are categorized as follows:

| Existing Platform Feature | Primary Location | Scope Classification | Retention Strategy |
| :--- | :--- | :---: | :--- |
| **Round 1 Pressure Engine** | `round1_pressure/` | **CORE ROUND 1** | Primary governing engine. Sealed and verified. |
| **Tactical Intelligence Dashboard** | `frontend/src/app/tactical/` | **DIRECT SUPPORT** | Fully operational. Exposes phase splits, strokes, variations, radar speed, and micro-battles. |
| **Tactical REST APIs (10 routes)** | `backend/app/api/v1/endpoints/tactical.py` | **DIRECT SUPPORT** | Fully operational (28 / 28 tests passing). |
| **Data Ingestion Explorer** | `frontend/src/app/acquisition/` | **INDIRECT SUPPORT** | Preserved. Demonstrates robust data ingestion infrastructure. |
| **Domestic Scorecard Viewer** | `frontend/src/app/domestic/` | **INDIRECT SUPPORT** | Preserved. Demonstrates multi-format phase and match tracking capability. |
| **Venue & Pitch Intelligence** | `frontend/src/app/venues/` | **INDIRECT SUPPORT** | Preserved. Provides venue geometry context. |
| **Uncapped Scouting Directory** | `frontend/src/app/uncapped/` | **OUT OF SCOPE** | Preserved in codebase but demoted from primary navigation. Inactive for Round 1. |
| **IPL 2027 Auction Valuation** | Legacy Roadmap | **OUT OF SCOPE** | Archived. Zero code dependencies in Round 1 pipelines. |
| **Youngest-Talent Age Filters** | Legacy Specs | **OUT OF SCOPE** | Archived. Round 1 evaluates all players meeting sample criteria. |

---

## 4. Gap Analysis: Path to 100% Platform Integration

| Gap Area | Current State | Required Target State | Implementation Action |
| :--- | :--- | :--- | :--- |
| **Pressure Leaderboards in UI** | Available in Markdown reports and Parquet tables | Interactive web dashboard at `/pressure` with table sorting and candidate filters | Execute **PRI-01** and **PRI-02** |
| **Candidate Evidence Dossiers in UI** | Documented in `r1_06_*_shortlist.md` | Interactive candidate drawer/modal with pressure split charts | Execute **PRI-03** |
| **Overview Landing Page Focus** | Mentions Stage 0–3 infrastructure | Showcases Round 1 challenge readiness, Top 10 leaderboards, and Stage 5 telemetry | Execute **PRI-05** and **PRI-06** |
| **Methodology Report Accessibility** | Stored as `ROYALS_INTELLIGENCE_ROUND_1_SUBMISSION.md` | In-app methodology viewer at `/methodology` | Execute **PRI-04** |

---

## 5. Recommended Next Task

**Recommended Next Sprint Task:**  
**`ST5-08: Round 1 Pressure Analytics Frontend Integration (/pressure)`**  
- Expose the locked Top 10 Batters, Top 10 Bowlers, and 20 Candidate Evidence Profiles through a dedicated FastAPI router (`/api/v1/analytics/pressure`).
- Build the `/pressure` dashboard in Next.js 15, allowing competition judges to interactively inspect Conservative PRI, posterior shrinkage, credible regions, and candidate evidence profiles.
- Update `/` (System Overview) and `Sidebar.tsx` to elevate Pressure Intelligence as the flagship entry point of the platform.
