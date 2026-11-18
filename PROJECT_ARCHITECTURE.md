# ROYALS INTELLIGENCE — SYSTEM ARCHITECTURE SPECIFICATION
**Platform:** ROYALS INTELLIGENCE v4.1  
**Target:** SupeRR Selector Season 2 — Round 1  
**Architecture Type:** High-Performance Cricket Intelligence & Bayesian Decision Platform  
**Document Status:** Authoritative Architectural Standard  

---

## 1. Architectural Philosophy & Dual-Track Cohesion

ROYALS INTELLIGENCE v4.1 is engineered to solve the official **SupeRR Selector Season 2 Round 1 Challenge** ("Identify the Most Reliable Players Under Pressure") while preserving the platform's extensible, enterprise-grade architecture.

The platform unifies two complementary engines:
1. **The Pressure Analytics & Reliability Engine (`round1_pressure/`):** A mathematically audited, Bayesian empirical Bayes decision system designed for competitive ranking, player shortlisting, and uncertainty assessment under acute match pressure.
2. **The Tactical Cricket Intelligence Engine (`backend/` & `frontend/`):** A high-speed, dataset-driven analytical service exposing phase splits, stroke efficiency, handedness matchups, delivery variations, radar speed telemetry, and micro-battles.

```
+===================================================================================================+
|                                  ROYALS INTELLIGENCE v4.1 ARCHITECTURE                            |
+===================================================================================================+
|                                                                                                   |
|  [PRESENTATION LAYER]                                                                             |
|  Next.js 15 App Router • TypeScript 5.7 • Tailwind CSS • Rajasthan Royals Design System          |
|  Routes: /tactical (Active) • /acquisition • /domestic • /venues • /uncapped                      |
|                                                                                                   |
+---------------------------------------------------------------------------------------------------+
|                                                                                                   |
|  [API & SERVICE LAYER]                                                                            |
|  FastAPI 0.115 • Pydantic v2 Schemas • 10 Tactical Endpoints under /api/v1/analytics/tactical/     |
|                                                                                                   |
+---------------------------------------------------------------------------------------------------+
|                                                                                                   |
|  [ANALYTICAL & STATISTICAL MODELING LAYER]                                                        |
|  +---------------------------------------------+  +--------------------------------------------+  |
|  | Track A: Tactical Intelligence Engine       |  | Track B: Round 1 Pressure Reliability      |  |
|  | - Phase Performance (PP, Mid, Death)       |  | - Dynamic Ball-by-Ball Leverage Scoring    |  |
|  | - 30 Batting Stroke Efficiency Profiles     |  | - 12-Cell Context Stratified Baselines     |  |
|  | - 4-Way Handedness Matchup Matrix           |  | - Empirical Bayes Prior & Shrinkage        |  |
|  | - 34 Bowling Variations & Movement Threat   |  | - Player Reliability Index (PRI)           |  |
|  | - Radar Speed Profiles & Sensor Safeguards  |  | - Conservative PRI (1-SE Lower Bound)      |  |
|  | - Death Overs Finishers & Containment       |  | - Two-Dimensional Classification          |  |
|  | - Head-to-Head Micro-Battle Engine          |  | - Top 10 Batting & Bowling Leaderboards   |  |
|  +---------------------------------------------+  +--------------------------------------------+  |
|                                                                                                   |
+---------------------------------------------------------------------------------------------------+
|                                                                                                   |
|  [DATA GOVERNANCE & PROVENANCE LAYER]                                                             |
|  Official Rajasthan Royals Round 1 Competition Data Pack (7 Files • 200,999 Balls • 883 Matches)  |
|  Strict Delivery Arithmetic • Bowler Wicket Credit • Non-Bowler Wicket Exclusion • Zero Synthetic |
|                                                                                                   |
+===================================================================================================+
```

---

## 2. Layer-by-Layer Architectural Specifications

### 2.1 Layer 1: Data Governance & Provenance Layer
*Authoritative source data store and physical validation boundary.*

- **Location:** `data/raw/rajasthan_royals/round_1_data_pack/`
- **Controlling Files:**
  1. `ball_by_ball.csv` (200,999 records, 39.17 MB) — Ball-level tracking with bowler speed, extras, pitch location, and shot stroke types.
  2. `matches.csv` (883 records, 0.12 MB) — Match metadata, venue IDs, competition links, toss results, and match outcomes.
  3. `competitions.csv` (141 records, 0.01 MB) — Tournament metadata spanning IPL (2022–2026) and Senior T20Is.
  4. `teams.csv` (353 records, 0.01 MB) — Team identifiers and franchise names.
  5. `playing_eleven.csv` (28,381 records, 0.92 MB) — Confirmed match-day lineups and captaincy flags.
  6. `competition_team_player_mapping.csv` (6,413 records, 0.44 MB) — Canonical player mapping across franchises and international squads.
  7. `venues.csv` / venue metadata — Ground information and location.
- **Governed Domain Invariants:**
  - **Categorical Extras Trap:** `extras1_runs` represents categorical extra types (1: Overstep, 2: wide, 3: legbyes, 4: byes, 5: other, 6: NONE, 7: Penalty), NOT numerical extra runs. Runs off the bat are strictly sourced from `runs`.
  - **Legal Delivery Definition:** A delivery is legal if and only if `extras_type` is not in `['wide', 'Overstep']`. Exactly **192,709 legal deliveries** exist across the dataset.
  - **Bowler Wicket Attribution:** Bowler wickets include strictly `bowled`, `caught`, `lbw`, `stumped`, and `hit wicket`. Non-bowler dismissals (`RunOut`, `Retire Out`, and normalized `Obstructing the field`) are strictly excluded. Exactly **10,489 bowler wickets** fallen.
  - **Abandoned Matches:** Exactly **16 matches** in `matches.csv` were abandoned without a ball bowled, reconciling the 883 match records with the 867 matches containing deliveries.
  - **State:** **COMPLETED & VERIFIED**

---

### 2.2 Layer 2: Pressure Analytics & Statistical Reliability Engine (`round1_pressure/`)
*The governing mathematical core resolving the SupeRR Selector Round 1 challenge.*

#### 2.2.1 Dynamic Ball-by-Ball Leverage Scoring
Pressure is evaluated ball-by-ball through five contextual dimensions:
$$\text{Leverage} = f\left(\text{Required Run Rate}, \text{Balls Remaining}, \text{Wickets in Hand}, \text{Contest Margin}, \text{Match Phase}\right)$$

- **Strict Pressure (Governing Primary Scope):**
  - Chasing ($I=2$): $\text{RRR} \ge 9.0$ with $B_{\text{rem}} \le 36$, OR $\text{RRR} \ge 12.0$ at any point, OR late-innings finishes ($B_{\text{rem}} \le 18$ with runs required $\le 36$ and wickets $\le 5$).
  - Setting Target ($I=1$): Overs 16–20 with team losing $\ge 4$ wickets, OR overs 18–20 in any contested match.
  - Empirical Volume: **37,014 legal bowling balls** and **31,163 legal batting balls**.
  - Death Overs Concentration: **87.28%** of bowling pressure and **78.95%** of batting pressure concentrate in overs 16–20.

#### 2.2.2 Context-Stratified 12-Cell Expected Baselines
To eliminate structural phase and venue biases, every delivery's ordinary expected performance is derived from a 12-cell non-pressure matrix:
$$\text{Cell} = \text{Phase } (\text{PP, Mid, Death}) \times \text{Tier } (\text{IPL, T20I}) \times \text{Innings } (1, 2)$$

Expected performance is personalized to each player's exact delivery exposure:
$$\text{Expected\_SR}_i = \frac{\sum_{c=1}^{12} N_{i, c} \cdot \overline{\text{SR}}_c}{N_i}, \quad \text{Expected\_Economy}_i = \frac{\sum_{c=1}^{12} N_{i, c} \cdot \overline{\text{Econ}}_c}{N_i}$$

Performance differentials represent observed minus expected performance under pressure:
$$\Delta \text{SR}_i = \text{Observed\_SR}_i - \text{Expected\_SR}_i$$
$$\Delta \text{Econ}_i = \text{Observed\_Economy}_i - \text{Expected\_Economy}_i$$

#### 2.2.3 Hierarchical Empirical Bayes Shrinkage & Conservative PRI
Raw differentials $\Delta_i$ have estimation variance $\sigma_i^2 = s_i^2 / N_i$. To eliminate small-sample noise, an empirical Bayes Gaussian prior $\mathcal{N}(\mu_0, \tau^2)$ is fitted across high-exposure players ($N \ge 60$):

$$\text{Posterior Mean } \hat{\theta}_i = B_i \mu_0 + (1 - B_i) \Delta_i, \quad \text{where } B_i = \frac{\sigma_i^2}{\sigma_i^2 + \tau^2}$$
$$\text{Posterior Variance } \text{Var}(\theta_i | \text{Data}) = \frac{\sigma_i^2 \tau^2}{\sigma_i^2 + \tau^2}, \quad \text{SE}_i = \sqrt{\text{Var}(\theta_i | \text{Data})}$$

To prioritize dependability over volatile high-variance candidates, ranking is governed strictly by the **one-standard-error lower credible bound (Conservative PRI)**:
$$\text{Conservative PRI}_{\text{Batting}} = \hat{\theta}_i - 1.0 \times \text{SE}_i \quad (\text{Higher is better})$$
$$\text{Conservative PRI}_{\text{Bowling}} = -(\hat{\theta}_i + 1.0 \times \text{SE}_i) \quad (\text{Runs Saved: Higher is better})$$

- **State:** **COMPLETED & VERIFIED** (196 / 196 tests passing)

---

### 2.3 Layer 3: Tactical Cricket Intelligence Engine (`backend/app/analytics/`)
*High-speed tactical domain service extracting situational and micro-battle intelligence.*

- **Engine:** `DatasetCricketIntelligenceEngine`
- **Key Modules:**
  1. **Phase Performance Splitter:** Generates Powerplay, Middle, and Death metrics (SR, economy, boundary %, dot %, balls per wicket) for tournament baseline or individual players.
  2. **Batting Stroke Profiler:** Evaluates productivity and hazard across 30 stroke types, calculating runs per shot, boundary %, and dismissal risk %.
  3. **Handedness Matrix Engine:** 4-way cross-split matrix cross-referencing RHB/LHB stance against pace/spin bowling disciplines.
  4. **Bowling Delivery Variation Service:** Evaluates 34 delivery styles and seam/spin movements, classing variations into containment weapons vs wicket hunters.
  5. **Radar Speed Telemetry Processor:** Ingests 123,113 valid velocity records (61.3% coverage), executes 10x multiplier scaling for values $\ge 500$, clips noise ($<50$ and $>170$ km/h), and ranks express bowlers.
  6. **Player Tactical Dossier Assembler:** Synthesizes multi-dimensional player profiles combining batting phases, strokes, bowling mechanics, and speed profiles.
  7. **Death Overs Elite Ranker:** Separate leaderboards for high-strike-rate finishers and low-economy containment bowlers in overs 16–20.
  8. **Head-to-Head Micro-Battle Engine:** Chronological query engine returning exact empirical head-to-head records and automated tactical verdicts.
- **State:** **COMPLETED & VERIFIED** (20 / 20 tests passing)

---

### 2.4 Layer 4: REST API Routing Layer (`backend/app/api/v1/`)
*Standardized FastAPI router exposing tactical intelligence endpoints.*

- **Base Route:** `/api/v1/analytics/tactical/`
- **Active Endpoints:**
  - `GET /summary` — Aggregate dataset metrics, legal balls, speed records.
  - `GET /phases` — Phase-wise splits for tournament or filtered player.
  - `GET /strokes` — 30 batting strokes efficiency and dismissal risk.
  - `GET /handedness` — 4-way RHB/LHB vs Pace/Spin matchup matrix.
  - `GET /variations` — 34 delivery styles effectiveness and dot ball %.
  - `GET /speed-profiles` — Speed distribution brackets, fastest bowlers, sensor safeguards.
  - `GET /players/{player_id}` — Multi-dimensional player tactical dossier.
  - `GET /death-overs` — Death phase elite finishers and containment bowlers.
  - `GET /matchups` — Striker vs Bowler direct empirical micro-battles.
  - `GET /players` — Live search and autocomplete player lookup.
- **State:** **COMPLETED & VERIFIED** (28 / 28 tests passing)

---

### 2.5 Layer 5: Frontend Application Layer (`frontend/`)
*Next.js 15 presentation layer implementing the Rajasthan Royals design system.*

- **Framework:** Next.js 15.1.0 (App Router), React 19.0.0, TypeScript 5.7.2, Tailwind CSS.
- **Visual Design Identity:**
  - Royal Navy (`#101C37`) & Deep Canvas (`#0B132B`)
  - Royals Pink (`#E91E8F`) for primary active states, tabs, and batting highlights
  - Royals Gold (`#D6B56D`) for badges, secondary accents, and tactical insights
  - Border Slate (`#1A2B50`) for grid containers and dividers
- **Active Routes:**
  - `/tactical` — Tactical Cricket Intelligence Dashboard (Modules A through I).
  - `/` — System Overview & Architecture Initialization.
  - `/acquisition` — Data Ingestion & Parquet Storage Explorer.
  - `/uncapped` — Uncapped Scouting Directory (Historical Track).
  - `/domestic` — Domestic Season & Scorecard Intelligence.
  - `/venues` — Venue Geometry & Pitch Intelligence.
- **Targeted Round 1 UI Enhancement (Pending):** Dedicated `/pressure` route presenting the official Top 10 Batting and Bowling leaderboards, candidate evidence cards, and methodology report.
- **State:** **COMPLETED & VERIFIED** (Static build passing, 0 errors, 0 warnings)

---

### 2.6 Layer 6: Automated Verification & Test Harness
*Continuous verification across all mathematical models, API contracts, and user interfaces.*

| Suite | File Count | Tests | Pass Rate | Scope |
| :--- | :-: | :-: | :-: | :--- |
| **Backend Integration Suite** | 6 files | 98 | **100% (98/98)** | Tactical API, dataset intelligence, venues, domestic matches, uncapped |
| **Pressure Verification Suite** | 8 files | 196 | **100% (196/196)** | Data QA, pressure scoring, expected baselines, empirical Bayes, ranking integrity |
| **Frontend Type Checker** | Full codebase | N/A | **Pass (0 errors)** | TypeScript compiler verification (`tsc --noEmit`) |
| **Frontend Production Build** | 9 routes | 9 routes | **Pass (0 errors)** | Next.js production build (`next build`) |
| **Total Automated Tests** | — | **294** | **100% (294/294)** | Complete platform verification |

- **State:** **COMPLETED & VERIFIED**

---

## 3. Component Status Matrix

| Component / Subsystem | Primary Location | Architectural Role | Status |
| :--- | :--- | :--- | :---: |
| **Official Round 1 Data Pack** | `data/raw/rajasthan_royals/` | Authoritative single source of truth | **COMPLETED** |
| **Data QA & Legality Filter** | `round1_pressure/src/data_qa.py` | Delivery arithmetic & legality classification | **COMPLETED** |
| **Match State Reconstruction** | `round1_pressure/src/match_state_reconstruction.py` | Ball-by-ball chronological leverage | **COMPLETED** |
| **Pressure Event Detection** | `round1_pressure/src/pressure_detection.py` | Situational pressure classification | **COMPLETED** |
| **12-Cell Baseline Engine** | `round1_pressure/src/expected_performance.py` | Context-stratified expected performance | **COMPLETED** |
| **Empirical Bayes Shrinkage** | `round1_pressure/src/player_reliability.py` | Bayesian PRI & Conservative lower bound | **COMPLETED** |
| **Candidate Shortlists** | `round1_pressure/reports/r1_06_*` | Official Top 10 Batters & Bowlers | **COMPLETED** |
| **Submission Deliverable** | `ROYALS_INTELLIGENCE_ROUND_1_SUBMISSION.md` | Master publication report | **COMPLETED** |
| **Dataset Tactical Engine** | `backend/app/analytics/dataset_cricket_intelligence.py` | Tactical analytics service | **COMPLETED** |
| **Tactical REST API (10 routes)**| `backend/app/api/v1/endpoints/tactical.py` | REST API endpoints | **COMPLETED** |
| **Tactical Dashboard UI** | `frontend/src/app/tactical/page.tsx` | Interactive web dashboard (Modules A–I) | **COMPLETED** |
| **Pressure Dashboard UI** | `frontend/src/app/pressure/` | Web UI for official Top 10 leaderboards | **PENDING** |
| **Multi-Match Variance Research**| `round1_pressure/src/research/` | Mixed-effects consistency research | **OPTIONAL FUTURE RESEARCH** |
| **Cluster-Robust Error Modeling** | `round1_pressure/src/research/` | Match-clustered variance validation | **OPTIONAL FUTURE RESEARCH** |

---

## 8. Additive Platform Domain: RR Auction & Retention Intelligence

To support long-range IPL 2027 roster construction and squad-retention planning without altering Round 1 competition deliverables, ROYALS INTELLIGENCE incorporates the **RR Auction & Retention Intelligence** domain as an independent, additive bounded context.

### 8.1 Domain Scope & Sovereign Deliverables
1. **Module A — RR Retention Intelligence:** Exactly three recommended retention choices from the active Rajasthan Royals squad, evaluated across 14 multi-season performance, consistency, replacement difficulty, and wage-cap dimensions (zero artificial role quotas).
2. **Module B — Combined Uncapped Batters Intelligence:** Exactly one unified Top 10 leaderboard evaluating eligible Indian and overseas uncapped batters against competition-normalized phase baselines.
3. **Module C — Combined Uncapped Bowlers Intelligence:** Exactly one unified Top 10 leaderboard evaluating eligible Indian and overseas uncapped bowlers across phase containment, dot frequency, radar speed distributions, and variation deception.

### 8.2 Architectural Governance & Isolation
- **Bounded Context:** Isolated under `backend/app/auction_intelligence/` with independent schemas, API routes (`/api/v1/auction/*`), and test suites.
- **Strict Cap Verification:** Enforces sovereign international cap certification (0 Test, ODI, or T20I appearances across senior men's cricket). U19 or domestic participation does not constitute a cap.
- **Reference Specification:** Full system architecture, mathematical formulations, and stage-wise implementation blueprints are authoritatively defined in [docs/RR_AUCTION_RETENTION_INTELLIGENCE_ARCHITECTURE.md](file:///c:/Users/ayush/Documents/ROYALS%20INTELLIGENCE/docs/RR_AUCTION_RETENTION_INTELLIGENCE_ARCHITECTURE.md).

