# ROYALS INTELLIGENCE — FRONTEND INTEGRATION & SYNCHRONIZATION AUDIT
**Document Version:** 1.0 (Comprehensive Architectural Audit)  
**Platform Target:** Rajasthan Royals Cricket Operations & IPL Decision Support System  
**Audit Timestamp:** 2026-11-16T16:15:00+05:30  
**Audit Mode:** READ-ONLY Verification (Zero Code / Zero Checkpoint Modifications)  
**Authoritative Data Source:** Official Rajasthan Royals Round 1 Data Pack (200,999 Deliveries, 883 Matches)  

---

## 1. GIT GOVERNANCE & REPOSITORY PREFLIGHT AUDIT

An exhaustive Git repository and commit tree audit was performed prior to analyzing the frontend and backend codebase:

### 1.1. Working Tree & Branch Telemetry
- **Active Branch:** `main`
- **Active HEAD Commit:** `6005022` (`feat(r1-06.2.3): final data-count reconciliation and statistical wording correction`)
- **Remote Configuration:** Local repository operating in offline, read-only audit mode (zero remote pushes).
- **Working Tree State:** All existing analytical models, Parquet outputs, Stage 4 venue/weather implementations, Stage 5 tactical engines, and Round 1 submission documents are preserved intact.

### 1.2. Git Branch Divergence & Historical Discovery
The audit uncovered an unmerged feature branch in the repository:
- **Branch Name:** `feat/frontend-ux-redesign`
- **Base Commit:** `321a381` (branched from `5614a4a`, which dates to 2026-11-11 following milestone R1-05).
- **Branch Contents:** Contains initial exploratory work on `pressure.py` endpoint, `reliability/page.tsx`, `reports/page.tsx`, and `round1Data.ts`.
- **Root Cause of Divergence:** Development on `main` advanced significantly past `5614a4a`, completing milestones R1-06 (Player Intelligence), R1-06.1 (Classification Audit), R1-06.2 (Candidate Classification Remediation), R1-06.2.1 (Consistency Audit), R1-06.2.2 (Governance Remediation), R1-06.2.3 (Final Data-Count Reconciliation), the Official Submission document (`ROYALS_INTELLIGENCE_ROUND_1_SUBMISSION.md`), and the Stage 5 Deep Tactical Analytics engine.
- **Consequence:** The frontend on `main` was never updated or merged with the feature branch. Consequently, the user-facing application on `main` remains frozen in early Stage 3 state.

---

## 2. BRANDING, DESIGN SYSTEM & COMPLETED ARCHITECTURE

The repository possesses a well-established, premium design system anchored in the official Rajasthan Royals visual identity. Any future frontend synchronization must strictly preserve these tokens:

### 2.1. Brand Palette & Design Tokens
- **RR Deep Navy (`#101C37`):** Primary background, sidebar container, card base, and high-contrast text.
- **RR Royal Pink (`#E91E8F`):** Primary brand accent, active selection states, key action buttons, and highlight badges.
- **RR Royal Gold (`#D6B56D`):** Secondary luxury accent, verification badges, high-reliability indicators, and card borders.
- **Slate Neutrals (`#0F172A`, `#1E293B`, `#334155`, `#94A3B8`, `#F8FAFC`):** Borders, muted labels, metric units, and surface backgrounds.

### 2.2. Component Architecture
- **StatCard (`frontend/src/components/ui/StatCard.tsx`):** Standard metric display with title, value, subtitle, status badge, and icon.
- **StatusBadge (`frontend/src/components/ui/StatusBadge.tsx`):** Standard status indicator supporting verified, pending, active, and degraded states.
- **ModuleCard (`frontend/src/components/ui/ModuleCard.tsx`):** Stage module representation with stage number, title, category, and status.
- **Header (`frontend/src/components/layout/Header.tsx`):** Sticky top bar with service health status and breadcrumb navigation.
- **Sidebar (`frontend/src/components/layout/Sidebar.tsx`):** Collapsible vertical navigation bar with brand logo and module links.

---

## 3. IDENTIFICATION OF OUTDATED & HARDCODED FRONTEND ELEMENTS

A systematic, line-by-line inspection of all frontend files on `main` revealed substantial discrepancies between the displayed UI text and actual repository capabilities:

### 3.1. Main Overview Dashboard (`frontend/src/app/page.tsx`)
1. **Outdated Hero Stage Badge (Line 149):**
   - Displays: `<span className="... bg-[#E91E8F] ...">STAGE 3 ACTIVE</span>`
   - Reality: Stage 3, Stage 4, Round 1 Pressure Analytics, and Stage 5 Tactical Analytics are fully completed and verified.
2. **Conflicting Scope Subtitle (Lines 155, 160–166):**
   - Displays: `"Target: IPL 2026 & IPL 2027 Auction (Uncapped Scope)"` and `"Royals Intelligence Domestic Season & Match Command Center"`.
   - Reality: The platform's active mission is the **SupeRR Selector Season 2 Round 1 Challenge** and the **Official Dataset Tactical Intelligence Engine**.
3. **Outdated Roadmap Progress StatCard (Lines 217–220):**
   - Displays: `title="Project Roadmap", value="Stage 3 / 13", subtitle="Domestic Season & Match Intelligence operational. Scope: Uncapped Only."`
   - Reality: Stages 0 through 4 and Round 1 Pressure Analytics are completed and verified; Stage 5 Tactical Engine is active.
4. **Phantom Modules List (Lines 18–139):**
   - Lists 12 theoretical modules (e.g., ILP Optimizer, Shadow Auction Simulator, WAR per Crore) all marked with `status: "Data integration pending"`.
   - Zero mention of the verified Round 1 Pressure Reliability engine, Top 10 Batters, Top 10 Bowlers, or Stage 5 Tactical Analytics.

### 3.2. Sidebar Navigation (`frontend/src/components/layout/Sidebar.tsx`)
1. **Simultaneous Hardcoded Active States (Lines 41, 48, 55, 62):**
   - Four items are hardcoded as `active: true` (`/acquisition`, `/uncapped`, `/domestic`, `/venues`), regardless of the user's current URL.
2. **Dead Anchor Links (`href="#"`):**
   - Batting Diagnostics (`#`) — Stage 3
   - Bowling Mechanics (`#`) — Stage 4
   - Talent Scouting (`#`) — Stage 8
   - IPL 2027 Auction (`#`) — Stage 12
   - Health & Schema (`#health`)
   - Clicking these produces zero action or jumps to page top.
3. **Missing Core Navigation Links:**
   - No link to **Round 1 Pressure Analytics** (`/pressure`).
   - No link to **Top 10 Batting & Bowling Shortlists** (`/leaderboards`).
   - No link to **Tactical Analytics Command Center** (`/tactical`).
   - No link to **Methodology & Submission Reports** (`/reports`).
4. **Outdated Footer Badge (Lines 226–232):**
   - Displays: `Architecture: STAGE 0` and `Stage 1 of 13 Ingestion Active`.

### 3.3. Application Header (`frontend/src/components/layout/Header.tsx`)
1. **Hardcoded Breadcrumb (Lines 36–38):**
   - Always displays: `"Platform Overview & Architecture Initialization"` across every route.
2. **Hardcoded Stage Badge (Lines 40–42):**
   - Always displays: `STAGE 0`.
3. **Placeholder Documentation Link (Line 77):**
   - Hardcoded to external placeholder `https://github.com/rajasthanroyals/royals-intelligence`.

### 3.4. Data Acquisition Hub (`frontend/src/app/acquisition/page.tsx`)
1. **Hardcoded Fallback Traps:**
   - Displays 31 deliveries and 2 matches when backend is offline, contradicting the official 200,999 delivery dataset.
2. **Hardcoded Localhost URL (Line 81):**
   - `fetch("http://localhost:8000/api/v1/acquisition/upload", ...)` hardcodes `localhost:8000` rather than using `API_BASE_URL` from `@/lib/api`.

### 3.5. Legacy Pages (`/uncapped` and `/domestic`)
1. **Synthetic Data Violation in `/uncapped` (Lines 54–62):**
   - Hardcodes mock player "Ashutosh Sharma" with synthetic DOB `"1998-09-15"`, violating our Anti-Fabrication rule for the official data pack.
2. **Hardcoded Trialists in `/domestic` (Line 60):**
   - Uses hardcoded `uncapped_rr_01` trialist list rather than real player mapping from `competition_team_player_mapping.csv`.

---

## 4. BACKEND API VS. FRONTEND CONNECTIVITY AUDIT

The backend provides 33 production endpoints across 9 routers. A comprehensive audit was conducted to verify which endpoints are actively consumed by the frontend:

| # | Router Module | Backend Endpoint Path | HTTP Method | Frontend Function in `api.ts` | Consumed in UI Page? | Status & Integration Gap |
| :---: | :--- | :--- | :---: | :--- | :---: | :--- |
| **01** | Health | `/api/v1/health` | GET | `fetchSystemHealth()` | YES (`Header.tsx`) | **CONNECTED** |
| **02** | Acquisition | `/api/v1/acquisition/sources` | GET | `fetchSources()` | YES (`acquisition/page.tsx`) | **CONNECTED** |
| **03** | Acquisition | `/api/v1/acquisition/coverage` | GET | `fetchCoverage()` | YES (`acquisition/page.tsx`) | **CONNECTED** |
| **04** | Acquisition | `/api/v1/acquisition/runs` | GET | `fetchIngestionRuns()` | YES (`acquisition/page.tsx`) | **CONNECTED** |
| **05** | Acquisition | `/api/v1/acquisition/datasets` | GET | `fetchDatasets()` | YES (`acquisition/page.tsx`) | **CONNECTED** |
| **06** | Players | `/api/v1/players` | GET | `fetchUncappedPlayers()` | YES (`uncapped/page.tsx`) | **CONNECTED (Legacy)** |
| **07** | Players | `/api/v1/players/{id}` | GET | `fetchUncappedPlayerDetail()` | YES (`uncapped/page.tsx`) | **CONNECTED (Legacy)** |
| **08** | Players | `/api/v1/players/{id}/eligibility` | POST | `verifyPlayerEligibility()` | YES (`uncapped/page.tsx`) | **CONNECTED (Legacy)** |
| **09** | Analytics | `/api/v1/analytics/players/{id}/batting` | GET | `fetchPlayerBatting()` | YES (`uncapped/page.tsx`) | **CONNECTED (Legacy)** |
| **10** | Analytics | `/api/v1/analytics/players/{id}/bowling` | GET | `fetchPlayerBowling()` | YES (`uncapped/page.tsx`) | **CONNECTED (Legacy)** |
| **11** | Analytics | `/api/v1/analytics/players/{id}/recent-form`| GET | `fetchPlayerRecentForm()` | YES (`uncapped/page.tsx`) | **CONNECTED (Legacy)** |
| **12** | **Tactical** | `/api/v1/analytics/tactical/summary` | GET | *None* | **NO** | **DISCONNECTED (Stage 5)** |
| **13** | **Tactical** | `/api/v1/analytics/tactical/phases` | GET | *None* | **NO** | **DISCONNECTED (Stage 5)** |
| **14** | **Tactical** | `/api/v1/analytics/tactical/strokes` | GET | *None* | **NO** | **DISCONNECTED (Stage 5)** |
| **15** | **Tactical** | `/api/v1/analytics/tactical/handedness` | GET | *None* | **NO** | **DISCONNECTED (Stage 5)** |
| **16** | **Tactical** | `/api/v1/analytics/tactical/variations` | GET | *None* | **NO** | **DISCONNECTED (Stage 5)** |
| **17** | **Tactical** | `/api/v1/analytics/tactical/speed-profiles` | GET | *None* | **NO** | **DISCONNECTED (Stage 5)** |
| **18** | **Tactical** | `/api/v1/analytics/tactical/players/{id}` | GET | *None* | **NO** | **DISCONNECTED (Stage 5)** |
| **19** | **Tactical** | `/api/v1/analytics/tactical/death-overs` | GET | *None* | **NO** | **DISCONNECTED (Stage 5)** |
| **20** | **Tactical** | `/api/v1/analytics/tactical/matchups` | GET | *None* | **NO** | **DISCONNECTED (Stage 5)** |
| **21** | Proprietary | `/api/v1/proprietary/discover-schema` | POST | `discoverProprietarySchema()`| YES (`uncapped/page.tsx`) | **CONNECTED (Legacy)** |
| **22** | Proprietary | `/api/v1/proprietary/ingest` | POST | `ingestProprietaryPack()` | YES (`uncapped/page.tsx`) | **CONNECTED (Legacy)** |
| **23** | Proprietary | `/api/v1/proprietary/evaluations/{id}` | GET | `fetchPlayerEvaluations()` | YES (`uncapped/page.tsx`) | **CONNECTED (Legacy)** |
| **24** | Domestic | `/api/v1/domestic/competitions` | GET | `fetchDomesticCompetitions()` | YES (`domestic/page.tsx`) | **CONNECTED** |
| **25** | Domestic | `/api/v1/domestic/seasons/{c}/{s}/matches` | GET | `fetchSeasonMatches()` | YES (`domestic/page.tsx`) | **CONNECTED** |
| **26** | Domestic | `/api/v1/domestic/matches/{id}/scorecard` | GET | `fetchMatchScorecard()` | YES (`domestic/page.tsx`) | **CONNECTED** |
| **27** | Venues | `/api/v1/venues` | GET | `fetchVenues()` | YES (`venues/page.tsx`) | **CONNECTED** |
| **28** | Venues | `/api/v1/venues/{id}` | GET | `fetchVenueDetail()` | YES (`venues/page.tsx`) | **CONNECTED** |
| **29** | Venues | `/api/v1/venues/{id}/scoring-trends` | GET | `fetchVenueScoringTrends()` | YES (`venues/page.tsx`) | **CONNECTED** |
| **30** | Venues | `/api/v1/venues/{id}/pitch-analysis` | GET | `fetchVenuePitchAnalysis()` | YES (`venues/page.tsx`) | **CONNECTED** |
| **31** | Weather | `/api/v1/weather/match/{id}` | GET | `fetchMatchWeatherContext()` | YES (`venues/page.tsx`) | **CONNECTED** |
| **32** | Weather | `/api/v1/weather/source-status` | GET | `fetchWeatherSourceStatus()` | YES (`venues/page.tsx`) | **CONNECTED** |
| **33** | **Pressure** | `/api/v1/pressure/*` | N/A | *None* | **NO** | **MISSING BACKEND ROUTER** |

---

## 5. ROOT-CAUSE ANALYSIS: WHY ROUND 1 PRESSURE ANALYTICS IS ABSENT

The total absence of the completed Round 1 Pressure Analytics engine from the frontend is explained by four distinct technical and structural factors:

1. **Dual-Track Architectural Bifurcation:**  
   The project was built in two distinct tracks:
   - **Track A (Full-Stack Platform):** Developed Stages 0–4 (FastAPI, PostgreSQL, Next.js UI) with a focus on domestic fixtures, uncapped scoping, and venue weather.
   - **Track B (SupeRR Selector Round 1):** Developed in `round1_pressure/` as an isolated analytical and statistical research pipeline to solve the competition challenge.
2. **Git Branch Isolation:**  
   An early attempt to connect Round 1 to the frontend was started on branch `feat/frontend-ux-redesign` (commit `321a381`), but this branch was never merged into `main`. The extensive subsequent work on `main` (R1-06 candidate selection, R1-06.1/R1-06.2 audits, final submission) occurred purely in Python scripts, Parquet tables, and Markdown reports.
3. **Absence of a `/api/v1/pressure` Backend Router on `main`:**  
   The verified Parquet files in `round1_pressure/data/processed/` (`batting_leaderboard.parquet`, `bowling_leaderboard.parquet`, `batting_evidence_profiles.parquet`, etc.) have no FastAPI endpoints on `main` to expose them to client applications.
4. **Static Frontend Navigation & Types:**  
   The frontend `Sidebar.tsx`, `Header.tsx`, `page.tsx`, and `types/index.ts` contain zero routes, interfaces, or fetch functions pointing to Round 1 metrics (PRI, conservative lower bounds, baseline differentials).

---

## 6. COMPLETE ROUTE & COMPONENT INVENTORY

```text
frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx             [Global Shell Layout with Sidebar & Header]
│   │   ├── page.tsx               [Root Overview Dashboard — Needs Stage/R1 Rebaseline]
│   │   ├── acquisition/page.tsx   [Data Acquisition Hub — Needs URL & State Fix]
│   │   ├── uncapped/page.tsx      [Uncapped Scouting — Needs Anti-Fabrication Safeguards]
│   │   ├── domestic/page.tsx      [Domestic Scorecards — Working]
│   │   └── venues/page.tsx        [Venue & Weather Command Center — Working]
│   ├── components/
│   │   ├── layout/
│   │   │   ├── Header.tsx         [Needs Dynamic Breadcrumbs & Accurate Stage Badge]
│   │   │   └── Sidebar.tsx        [Needs Dynamic Route Detection & R1/Tactical Links]
│   │   └── ui/
│   │       ├── ModuleCard.tsx     [Working UI Component]
│   │       ├── StatCard.tsx       [Working UI Component]
│   │       └── StatusBadge.tsx    [Working UI Component]
│   ├── lib/
│   │   ├── api.ts                 [API Client — Needs Tactical & Pressure Functions]
│   │   └── utils.ts               [Tailwind Merge Utility — Working]
│   └── types/
│       └── index.ts               [TypeScript Interfaces — Needs R1 & Tactical Contracts]
```
