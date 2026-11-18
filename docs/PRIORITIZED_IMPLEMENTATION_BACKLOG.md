# ROYALS INTELLIGENCE — PRIORITIZED IMPLEMENTATION BACKLOG
**Platform:** Rajasthan Royals Cricket Intelligence Platform  
**Document Version:** 1.0 (Post-Rebaseline)  
**Authoritative Foundation:** Official Rajasthan Royals Round 1 Data Pack (`data/raw/rajasthan_royals/round_1_data_pack/`)  
**Alignment:** Revised 14-Stage Development Roadmap (`docs/REVISED_14_STAGE_ROADMAP.md`)  

---

## 1. BACKLOG PRIORITIZATION FRAMEWORK

Items in this backlog are ranked using the **MoSCoW (Must, Should, Could, Won't) & RICE (Reach, Impact, Confidence, Effort)** prioritization frameworks, calibrated specifically for Rajasthan Royals match-day decision support and long-term roster strategy:

```
+--------------------------------------------------------------------------------------------------+
| PRIORITY TIERS:                                                                                  |
| - TIER P0 (CRITICAL / IMMEDIATE): Stage 5 Core Tactical Analytics & Data Pack Preprocessing    |
| - TIER P1 (HIGH / NEXT SPRINTS): Stage 6 Matchups & Stage 7 Impact Player Optimization          |
| - TIER P2 (MEDIUM / STRATEGIC): Stage 8 Opposition Scouting & Stage 10 Emerging Talent Discovery|
| - TIER P3 (SYSTEM / SCALE): Stage 13 Caching, Hardening, and Production Deployment             |
+--------------------------------------------------------------------------------------------------+
```

---

## 2. DETAILED BACKLOG WORK PACKAGES

### Epic 1: Stage 5 — Official Dataset Deep Tactical Analytics Engine (TIER P0 — IMMEDIATE)

| Task ID | Item Title | Priority | Target Module | Technical Description & Acceptance Criteria | Status |
| :---: | :--- | :---: | :--- | :--- | :---: |
| **ST5-01** | **Data Pack Tactical Ingestion & Preprocessing** | P0 | `backend/app/analytics/dataset_cricket_intelligence.py` | Load all 200,999 deliveries, clean radar release speed sensor anomalies, filter legal balls, calculate accurate bowler runs conceded. | **IN PROGRESS** |
| **ST5-02** | **Phase Mastery Diagnostics Engine** | P0 | `backend/app/analytics/dataset_cricket_intelligence.py` | Aggregate Powerplay (overs 1–6), Middle (7–15), and Death (16–20) strike rates, economy, dot %, boundary %, and balls-per-wicket. | **IN PROGRESS** |
| **ST5-03** | **Handedness & Bowling Sub-Discipline Matrix** | P0 | `backend/app/analytics/dataset_cricket_intelligence.py` | 4-way stance/pace-spin split + 12-way bowling type matrix with empirical averages and boundary suppression. | **IN PROGRESS** |
| **ST5-04** | **Tactical Stroke & Dismissal Risk Engine** | P0 | `backend/app/analytics/dataset_cricket_intelligence.py` | 30 stroke types profiling: runs per shot, boundary conversion rate, and dismissal risk %. | **IN PROGRESS** |
| **ST5-05** | **Delivery Variation & Movement Diagnostics** | P0 | `backend/app/analytics/dataset_cricket_intelligence.py` | 34 delivery styles profiling: cutters, seam, inswing, outswing, googly, leg break economy and dot %. | **IN PROGRESS** |
| **ST5-06** | **Tactical Analytics REST API Router** | P0 | `backend/app/api/v1/endpoints/tactical.py` | Expose FastAPI endpoints for player phase profiles, stroke breakdown, and handedness splits. | **BACKLOG** |

---

### Epic 2: Stage 6 — Head-to-Head Matchup & Tactical Archetype Engine (TIER P1)

| Task ID | Item Title | Priority | Target Module | Technical Description & Acceptance Criteria | Status |
| :---: | :--- | :---: | :--- | :--- | :---: |
| **ST6-01** | **Batter vs Bowler Micro-Battle Engine** | P1 | `backend/app/analytics/matchup_engine.py` | Query head-to-head records across 200,999 deliveries with Empirical Bayes shrinkage for low-sample pairs. | **READY** |
| **ST6-02** | **Dismissal Quadrant & Sector Attribution** | P1 | `backend/app/analytics/matchup_engine.py` | Map dismissals to `stroke` and `on_or_off` ground sector to pinpoint dismissal vulnerability zones. | **READY** |
| **ST6-03** | **Bowling Angle Optimization (`over_or_around`)** | P1 | `backend/app/analytics/matchup_engine.py` | Quantify bowler effectiveness around vs over the wicket against RHB and LHB opponents. | **READY** |
| **ST6-04** | **Unsupervised Player Archetype Clustering** | P1 | `backend/app/analytics/archetypes.py` | Cluster batters into Enforcers, Anchors, Finishers; cluster bowlers into Swing, Enforcers, Death Specialists. | **READY** |

---

### Epic 3: Stage 7 — Playing XI & Impact Player Dynamic Optimizer (TIER P1)

| Task ID | Item Title | Priority | Target Module | Technical Description & Acceptance Criteria | Status |
| :---: | :--- | :---: | :--- | :--- | :---: |
| **ST7-01** | **Empirical Impact Player Decision Trees** | P1 | `backend/app/analytics/impact_optimizer.py` | Trained on 558 sub-ins/outs in `playing_eleven.csv`. Models batting-first vs bowling-first substitution strategies. | **READY** |
| **ST7-02** | **Algorithmic Lineup Optimizer (ILP)** | P1 | `backend/app/analytics/lineup_optimizer.py` | Integer linear program selecting optimal XI subject to overseas limits, wicketkeeper rules, and bowling quotas. | **READY** |
| **ST7-03** | **Match Condition Adaptation Matrix** | P1 | `backend/app/analytics/lineup_optimizer.py` | Dynamically alters lineup composition based on venue historical par and dew severity risk. | **READY** |

---

### Epic 4: Stage 8 & 10 — Opposition Scouting & Emerging Talent Discovery (TIER P2)

| Task ID | Item Title | Priority | Target Module | Technical Description & Acceptance Criteria | Status |
| :---: | :--- | :---: | :--- | :--- | :---: |
| **ST8-01** | **IPL Franchise Scouting Dossiers** | P2 | `backend/app/analytics/opposition_scout.py` | Automated tactical dossiers for all 10 IPL franchises based on 2022–2026 match progressions. | **READY** |
| **ST8-02** | **Big-Match Temperament Index** | P2 | `backend/app/analytics/opposition_scout.py` | Performance differential across 56 Knockout/Playoff matches vs 827 League matches. | **READY** |
| **ST10-01** | **Developmental Tournament Anomaly Detector** | P2 | `backend/app/analytics/talent_discovery.py` | Mines Emerging Teams Asia Cup and Rising Stars for high-efficiency, low-exposure prospects. | **READY** |
| **ST10-02** | **Radar Velocity & Biomechanical Filter** | P2 | `backend/app/analytics/talent_discovery.py` | Identifies bowlers consistently exceeding 140 km/h release speed. | **READY** |

---

### Epic 5: Platform Hardening & Frontend Experience (TIER P3)

| Task ID | Item Title | Priority | Target Module | Technical Description & Acceptance Criteria | Status |
| :---: | :--- | :---: | :--- | :--- | :---: |
| **ST13-01** | **Redis Sub-Second Analytics Caching** | P3 | `backend/app/core/caching.py` | Cache precomputed phase and matchup matrices to guarantee sub-100ms API response times. | **BACKLOG** |
| **ST13-02** | **Interactive Tactical UI Command Center** | P3 | `frontend/app/tactics/page.tsx` | Next.js 15 command center displaying stroke efficiency radars, matchup heads-up, and death-over rankings. | **BACKLOG** |
