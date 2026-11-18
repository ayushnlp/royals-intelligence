# ROYALS INTELLIGENCE — FRONTEND IMPLEMENTATION & SYNCHRONIZATION ROADMAP
**Document Version:** 1.0 (Implementation Blueprint)  
**Platform Target:** Rajasthan Royals Cricket Intelligence Platform  
**Target Milestone:** Full Frontend Synchronization with Round 1 Pressure Analytics & Stage 5 Tactical Engine  
**Governance Mode:** Read-Only Plan (Awaiting User Review before Implementation)  
**Authoritative Foundation:** Official Rajasthan Royals Round 1 Data Pack (`data/raw/rajasthan_royals/round_1_data_pack/`) & Verified Parquet Outputs  

---

## 1. STRATEGIC ARCHITECTURE & INTEGRATION OBJECTIVES

This document defines the exact step-by-step roadmap to synchronize the Next.js 15 frontend with the verified analytical capabilities of the platform, resolving the divergence identified in [`FRONTEND_INTEGRATION_AUDIT.md`](file:///c:/Users/ayush/Documents/ROYALS%20INTELLIGENCE/FRONTEND_INTEGRATION_AUDIT.md).

### Core Architectural Objectives:
1. **Preserve Rajasthan Royals Visual Identity:** Anchor all interfaces in Deep Navy (`#101C37`), Royal Pink (`#E91E8F`), and Royal Gold (`#D6B56D`), utilizing the existing Tailwind CSS design tokens and component library.
2. **First-Class Round 1 Pressure Representation:** Build dedicated, interactive views for the completed SupeRR Selector Round 1 challenge: Top 10 Batters, Top 10 Bowlers, Stratified Ordinary Baselines, and Individual Player Evidence Profiles.
3. **First-Class Stage 5 Tactical Engine Representation:** Expose the 9 newly implemented REST endpoints under `/api/v1/analytics/tactical` for phase mastery, 30 stroke efficiencies, 34 bowling delivery variations, speed telemetry with sensor safeguards, and head-to-head micro-battles.
4. **Dynamic & Truthful Navigation:** Eliminate hardcoded stage badges ("STAGE 0", "STAGE 3 ACTIVE"), dead `#` links, and phantom modules, replacing them with a live, telemetry-driven status registry.
5. **Strict Anti-Fabrication Compliance:** Render only empirical data from the official data pack. Bar synthetic player salaries, unverified dates of birth, or speculative auction bidding.

---

## 2. INFORMATION ARCHITECTURE & TARGET ROUTE TAXONOMY

The frontend navigation and layout will be restructured into **five coherent analytical pillars**:

```text
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                          ROYALS INTELLIGENCE PLATFORM v4.2                             │
│       Official Rajasthan Royals Cricket Operations & IPL Decision Support System       │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │
   ┌───────────────────┬────────────────────┼───────────────────┬────────────────────┐
   ▼                   ▼                    ▼                   ▼                    ▼
[PILLAR 1]          [PILLAR 2]           [PILLAR 3]          [PILLAR 4]           [PILLAR 5]
Command Center      Round 1 Pressure     Tactical Engine     Venue & Matches      Methodology &
& Overview          Analytics Hub        (Stage 5 Active)    (Stages 3 & 4)       Submission
Route: `/`          Route: `/pressure`   Route: `/tactical`  Routes: `/domestic`, Route: `/reports`
                                                             `/venues`
- Platform Goals    - Challenge Overview - Phase Mastery     - 98 Venues Catalog  - Official Submission
- Milestone Status  - Top 10 Batters     - 30 Shot Strokes   - BCCI Boundary Par  - Bayesian PRI Theory
- Telemetry Probes  - Top 10 Bowlers     - 34 Variations     - Pitch Diagnostics  - Baseline Strata
- Dataset Summary   - Evidence Dossiers  - Speed Telemetry   - Weather Telemetry  - Reconciliation
- Next Action Cards - 12 Stratified Cells- Head-to-Head      - Match Progression  - Parquet Manifests
```

---

## 3. BACKEND-TO-FRONTEND API MAPPING MATRIX

To power the unified interface, the frontend will connect to existing backend endpoints, complemented by a dedicated, lightweight `/api/v1/pressure` router that directly reads the verified Parquet artifacts:

| # | Target UI Page / Section | Frontend Component | Required Data Element | Backend Endpoint Path | HTTP Method | Response Schema | Fallback Strategy |
| :---: | :--- | :--- | :--- | :--- | :---: | :--- | :--- |
| **01** | Global Header & Health | `Header.tsx` | Service liveness & database state | `/api/v1/health` | GET | `SystemHealth` | Standby offline banner |
| **02** | Overview Hero & Metrics | `app/page.tsx` | Dataset volume & match counts | `/api/v1/analytics/tactical/summary` | GET | `TacticalDatasetSummaryResponse` | Deterministic data pack totals |
| **03** | Overview Milestones | `app/page.tsx` | Live milestone audit status | `/api/v1/pressure/status` | GET | `PressureStatusResponse` | Static verified status registry |
| **04** | R1 Batting Leaderboard | `app/pressure/page.tsx` | Top 10 Batters Under Pressure | `/api/v1/pressure/batting` | GET | `List[BatterReliabilityRecord]` | `r1_06_batting_shortlist` snapshot |
| **05** | R1 Bowling Leaderboard | `app/pressure/page.tsx` | Top 10 Bowlers Under Pressure | `/api/v1/pressure/bowling` | GET | `List[BowlerReliabilityRecord]` | `r1_06_bowling_shortlist` snapshot |
| **06** | R1 Baseline Strata | `app/pressure/page.tsx` | 12 Ordinary Stratified Cells | `/api/v1/pressure/baselines` | GET | `List[BaselineCell]` | Precomputed 12-cell baseline table |
| **07** | R1 Player Evidence Modal | `components/pressure/PlayerModal.tsx` | Bayesian posterior & tenure text | `/api/v1/pressure/evidence/{player_id}` | GET | `PlayerEvidenceResponse` | Parquet evidence profile lookup |
| **08** | Tactical Phase Breakdown| `app/tactical/page.tsx` | PP / Middle / Death splits | `/api/v1/analytics/tactical/phases` | GET | `TacticalPhaseResponse` | Full tournament phase summary |
| **09** | Tactical Stroke Radar | `app/tactical/page.tsx` | 30 stroke efficiency & risks | `/api/v1/analytics/tactical/strokes` | GET | `TacticalStrokesResponse` | Precomputed stroke rankings |
| **10** | Tactical Handedness | `app/tactical/page.tsx` | RHB/LHB vs Pace/Spin | `/api/v1/analytics/tactical/handedness` | GET | `HandednessMatrixResponse` | 4-way cross-split matrix |
| **11** | Tactical Speed Profile | `app/tactical/page.tsx` | Radar release velocity & brackets | `/api/v1/analytics/tactical/speed-profiles` | GET | `SpeedProfileResponse` | Governed speed distribution |
| **12** | Tactical Head-to-Head | `app/tactical/page.tsx` | Batter vs Bowler micro-battles | `/api/v1/analytics/tactical/matchups` | GET | `HeadToHeadMatchupResponse` | Empirical head-to-head records |
| **13** | Venue Command Center | `app/venues/page.tsx` | Stadium catalog & par trends | `/api/v1/venues` | GET | `List[VenueSummaryItem]` | Verified 10 major venues |
| **14** | Weather Telemetry | `app/venues/page.tsx` | In-situ weather & dew risk | `/api/v1/weather/match/{id}` | GET | `MatchWeatherContextResponse` | Open-Meteo CC-BY 4.0 fallback |
| **15** | Official Submission | `app/reports/page.tsx` | Submission document & audit | `/api/v1/pressure/submission` | GET | `SubmissionDocumentResponse` | Reads `ROYALS_INTELLIGENCE_ROUND_1_SUBMISSION.md` |

---

## 4. COMPONENT & ROUTE MODIFICATION PLAN

### Phase 1: Shared Shell & Navigation Hardening
1. **`frontend/src/components/layout/Header.tsx`:**
   - Replace hardcoded `"Platform Overview & Architecture Initialization"` with dynamic page title derived from Next.js `usePathname()`.
   - Replace hardcoded `STAGE 0` with dynamic active status pill (e.g. `SUPE-RR SELECTOR R1 VERIFIED` / `STAGE 5 ACTIVE`).
   - Wire API liveness button directly to `/api/v1/health`.
2. **`frontend/src/components/layout/Sidebar.tsx`:**
   - Replace static `active: true` flags with pathname-matching logic: `currentPath === item.href`.
   - Eliminate all dead `href="#"` links.
   - Reorganize menu into 5 logical categories:
     - **Overview:** System Overview (`/`).
     - **Round 1 Pressure Analytics:** Pressure Hub & Top 10 Leaderboards (`/pressure`).
     - **Tactical Engine (Stage 5):** Phase Mastery, Strokes, Speed & Matchups (`/tactical`).
     - **Match & Venue Intelligence:** Domestic Matches (`/domestic`), Stadiums & Pitch (`/venues`).
     - **Governance & Methodology:** Official Submission & Reports (`/reports`).
   - Update footer badge to display `ROYALS INTELLIGENCE v4.2` and `Round 1 Verified • Stage 5 Active`.

### Phase 2: Root Overview Dashboard Rebaseline (`frontend/src/app/page.tsx`)
1. **Hero Section:**
   - Update title to `"Royals Intelligence Platform — SupeRR Selector & Tactical Command Center"`.
   - Update badge to `"ROUND 1 SEALED (293/293 TESTS) • STAGE 5 ACTIVE"`.
   - Display official data pack coverage metrics: 200,999 Deliveries, 883 Matches, 141 Tournaments, 1,217 Players.
2. **Active Milestones Progress Card Grid:**
   - **Track B (SupeRR Selector Round 1):** R1-01 to R1-06.2.3 Sealed & Verified (Top 10 Batters & Bowlers complete).
   - **Track A Platform Foundations:** Stages 0–4 Sealed & Verified (FastAPI, AsyncPG, Domestic scorecards, Venues & Dew).
   - **Stage 5 Deep Tactical Engine:** Active (200,999 delivery attributes, 9 REST endpoints live).
3. **Guided Next Action Cards:**
   - *Explore Round 1 Shortlists:* One-click link to `/pressure` to review Top 10 Batters & Bowlers.
   - *Analyze Tactical Stroke & Speed Radars:* One-click link to `/tactical` to inspect shot efficiency.
   - *Inspect Official Submission Document:* One-click link to `/reports` to read the complete publication draft.

### Phase 3: Round 1 Pressure Analytics Hub (`frontend/src/app/pressure/page.tsx`)
Create a dedicated, interactive dashboard for SupeRR Selector Round 1:
1. **Challenge Objective Header:** Formal definition of situational pressure ($PI \ge 60$) and Bayesian Player Reliability Index ($PRI$).
2. **Top 10 Batters Under Pressure Leaderboard:**
   - Interactive table with ranking, player name, team, pressure balls faced, observed strike rate, baseline expected strike rate, strike rate differential, Bayesian conservative lower bound, and $P(\text{Maintain Ordinary})$.
   - Filter by tournament (All, IPL Only, Senior T20I Only).
   - One-click trigger to open player's detailed evidence profile modal.
3. **Top 10 Bowlers Under Pressure Leaderboard:**
   - Interactive table with ranking, player name, bowling discipline, pressure legal balls, observed economy, baseline expected economy, economy differential ($Economy_{\text{base}} - Economy_{\text{obs}}$ where positive is superior), conservative lower bound, and $P(\text{Exceed Peers})$.
   - One-click trigger to open bowler's evidence profile modal.
4. **12 Stratified Ordinary Baselines Table:**
   - View of the 12 mutually exclusive baseline cells (Competition Tier $\times$ Innings $\times$ Phase), explaining the empirical resolution of Simpson's Paradox.
5. **Interactive Evidence Profile Drawer / Modal:**
   - Full mathematical narrative, 95% Bayesian credible interval visualizer, tenure breakdown across seasons (2022–2026), and qualitative pressure performance record.

### Phase 4: Stage 5 Tactical Analytics Command Center (`frontend/src/app/tactical/page.tsx`)
Create a dedicated UI for the newly implemented Stage 5 REST API:
1. **Phase Mastery Explorer:** Powerplay vs Middle vs Death side-by-side comparative cards with run rates, dot %, boundary %, and balls-per-wicket.
2. **30 Shot Strokes Efficiency Radar:** Searchable table & visualization showing runs per shot, boundary conversion rate, and dismissal risk % (Cover Drive, Pull shot, Worked, Scoop, etc.).
3. **Handedness Matrix:** 4-way cross-split interactive cards (RHB vs Pace, RHB vs Spin, LHB vs Pace, LHB vs Spin).
4. **Radar Release Velocity Telemetry:** Speed brackets distribution, express pace ($\ge 140\text{ km/h}$) counts, and fastest bowlers ranking with sensor calibration safeguards.
5. **Head-to-Head Micro-Battle Sandbox:** Select any striker and bowler to view historical delivery count, runs, dismissals, and strike rate.

### Phase 5: Methodology & Reports Hub (`frontend/src/app/reports/page.tsx`)
1. **Submission Document Reader:** Clean markdown renderer for `ROYALS_INTELLIGENCE_ROUND_1_SUBMISSION.md`.
2. **Validation & Audit Trail:** Interactive cards for R1-01 (Data QA), R1-02 (Match State), R1-03 (Pressure Detection), R1-04 (Bayesian Shrinkage), R1-05 (Statistical Validation), and R1-06 (Candidate Shortlists).
3. **Exportable Artifacts Manifest:** Direct access to processed Parquet schemas and validation closure reports.

### Phase 6: Lightweight Backend Pressure Router (`backend/app/api/v1/endpoints/pressure.py`)
To feed the frontend with verified Round 1 analytics without touching or modifying existing Parquet artifacts:
- Create `backend/app/api/v1/endpoints/pressure.py` mounting routes:
  - `GET /api/v1/pressure/status`: Returns milestone completion records and test coverage.
  - `GET /api/v1/pressure/batting`: Reads `r1_06_player_intelligence_batting.parquet` / `batting_leaderboard.parquet` and returns Top 10 Batters with conservative bounds.
  - `GET /api/v1/pressure/bowling`: Reads `r1_06_player_intelligence_bowling.parquet` / `bowling_leaderboard.parquet` and returns Top 10 Bowlers.
  - `GET /api/v1/pressure/baselines`: Reads `batting_ordinary_baseline.parquet` and returns the 12 stratification cells.
  - `GET /api/v1/pressure/evidence/{player_id}`: Returns player evidence record.
  - `GET /api/v1/pressure/submission`: Reads `ROYALS_INTELLIGENCE_ROUND_1_SUBMISSION.md` and returns structured submission text.
- Register `pressure.router` in `backend/app/api/v1/router.py`.

---

## 5. TESTING, VALIDATION & ACCEPTANCE CRITERIA

Prior to marking the frontend synchronization complete, the implementation must satisfy all of the following verification gates:

### Gate 1: Frontend Strict Compilation & Type-Checking
- `npm run type-check` (`tsc --noEmit`) passes with **0 errors**.
- `npm run lint` (`next lint`) passes with **0 warnings and 0 errors**.
- `npm run build` (`next build`) produces production static and dynamic pages with **0 build failures**.

### Gate 2: Backend API & Regression Suite
- All 97 existing backend tests in `backend/tests/` pass with **0 failures and 0 warnings**.
- All 196 Round 1 pressure tests in `round1_pressure/tests/` pass with **0 failures and 0 warnings**.
- New unit tests for `backend/tests/test_pressure_api.py` pass with **100% test coverage**.

### Gate 3: Data Governance & Integrity Verification
- Zero commercial attributes (salaries, prices, bids) exposed in any UI component or API response.
- Zero fabricated player ages or synthetic match scores rendered.
- All numbers on Round 1 leaderboards match `ROYALS_INTELLIGENCE_ROUND_1_SUBMISSION.md` with 100% precision:
  - Batting #1: Nicholas Pooran (Conservative Bound: +2.2, P(Exceed Baseline): 87.7%).
  - Bowling #1: Varun Chakravarthy (Conservative Bound: +0.47, P(Exceed Peers): 87.3%).

### Gate 4: Responsive & Visual UX Verification
- Layout renders flawlessly across mobile (375px), tablet (768px), and desktop (1280px+) viewport breakpoints.
- Brand colors match `#101C37`, `#E91E8F`, and `#D6B56D`.
- Navigation active state dynamically reflects current URL with zero dead links.
