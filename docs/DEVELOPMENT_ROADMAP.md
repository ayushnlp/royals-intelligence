# ROYALS INTELLIGENCE — COMPREHENSIVE DEVELOPMENT ROADMAP
**Platform Target:** Rajasthan Royals Cricket Intelligence & IPL 2027 Auction Decision Support  
**Roadmap Scope:** Stages 0 through 13  

---

## Roadmap Overview

```
+-----------------------------------------------------------------------------------------+
| Stage 0: Foundation & Architecture Setup (CURRENT)                                      |
+-----------------------------------------------------------------------------------------+
       |
       v
+------------------------------------+      +-------------------------------------------+
| Stage 1: Data Ingestion & Pipeline | ---> | Stage 2: Database Schema & Relational ETL |
+------------------------------------+      +-------------------------------------------+
       |
       v
+------------------------------------+      +-------------------------------------------+
| Stage 3: Core Batting Analytics    | ---> | Stage 4: Core Bowling & Phase Analytics   |
+------------------------------------+      +-------------------------------------------+
       |
       v
+------------------------------------+      +-------------------------------------------+
| Stage 5: Venue & Pitch Engine      | ---> | Stage 6: Player vs Player Matchups        |
+------------------------------------+      +-------------------------------------------+
       |
       v
+------------------------------------+      +-------------------------------------------+
| Stage 7: Playing XI & Impact Player| ---> | Stage 8: Opposition Intelligence & Scouting|
+------------------------------------+      +-------------------------------------------+
       |
       v
+------------------------------------+      +-------------------------------------------+
| Stage 9: In-Season IPL 2026 Engine | ---> | Stage 10: Hidden Talent Discovery Engine   |
+------------------------------------+      +-------------------------------------------+
       |
       v
+------------------------------------+      +-------------------------------------------+
| Stage 11: Match & Roster Simulator | ---> | Stage 12: IPL 2027 Auction Decision Hub   |
+------------------------------------+      +-------------------------------------------+
       |
       v
+-----------------------------------------------------------------------------------------+
| Stage 13: Enterprise Hardening, Security Audit & Operational Handover                   |
+-----------------------------------------------------------------------------------------+
```

---

## Detailed Stage Definitions

### Stage 0: Foundation, Repository Setup & Architecture Initialization (CURRENT STAGE)
* **Objective:** Establish the clean monorepo, Rajasthan Royals visual identity frontend shell, FastAPI async backend, database connection architecture, Docker orchestration, comprehensive documentation, and CI/CD foundations.
* **Deliverables:**
  * Clean monorepo structure with zero legacy dependencies.
  * Next.js App Router shell with Royals navy/pink branding and responsive navigation.
  * FastAPI backend with `/health` and `/api/v1/health` probes.
  * SQLAlchemy 2.0 Async + Alembic migration harness.
  * Documentation suite (`PROJECT_BLUEPRINT`, `ARCHITECTURE`, `DATABASE_DESIGN`, `DATA_STRATEGY`, `API_DESIGN`, `DEVELOPMENT_ROADMAP`, `DESIGN_SYSTEM`, `SECURITY`, `STAGE_STATUS`).
  * Docker Compose configuration for Postgres, Redis, Backend, Frontend.
  * Verified unit tests for backend health probes and frontend production build.

### Stage 1: Data Ingestion Infrastructure & Historical Data Pipelines
* **Objective:** Build robust automated ingestion pipelines for historical IPL and domestic T20 cricket data.
* **Deliverables:**
  * Cricsheet and raw JSON match data parsers with schema validation.
  * Data normalization and player identity deduplication engine.
  * Partitioned Apache Parquet analytical store in `data/processed/`.

### Stage 2: Database Schema Implementation & Relational Persistence
* **Objective:** Execute Alembic migrations to instantiate all core relational tables and indexes.
* **Deliverables:**
  * Tables: `teams`, `venues`, `matches`, `innings`, `deliveries`, `players`.
  * High-performance composite indexes on `(match_id, innings_id, over_number)` and `(bowler_id, striker_id)`.
  * Batch async loading pipeline from Parquet to PostgreSQL.

### Stage 3: Core Batting Intelligence & Advanced Metrics
* **Objective:** Implement advanced batting diagnostics beyond conventional average and strike rate.
* **Deliverables:**
  * Phase-specific metrics (Powerplay, Middle, Death).
  * Control percentage, false shot rate, dot ball mitigation index, and boundary frequency.
  * Pace-vs-spin splits and entry-point acceleration profiles.

### Stage 4: Core Bowling & Phase Intelligence
* **Objective:** Implement bowling diagnostics, length distributions, and release consistency analysis.
* **Deliverables:**
  * Length cluster efficiency (yorker, full, good, back-of-length, short).
  * Pressure-over metrics (defending <8 runs in 19th/20th overs).
  * Slower ball variation detection and wicket-taking threat indices.

### Stage 5: Venue, Pitch & Environmental Intelligence
* **Objective:** Quantify the influence of ground geometry, soil, dew, and weather conditions.
* **Deliverables:**
  * Venue boundary length database and asymmetry scoring.
  * Black soil vs Red soil turn/bounce decay modeling.
  * Dew impact regression engine for night matches.

### Stage 6: Player vs Player Matchups & Archetype Engine
* **Objective:** Build granular micro-battle analytics and archetype generalization for low-sample pairings.
* **Deliverables:**
  * Direct batter-vs-bowler head-to-head empirical dossiers.
  * Unsupervised clustering of bowlers and batters into archetypes (e.g., Express Pace vs LHB Anchor).
  * Probabilistic matchup outcome matrices with Bayesian smoothing.

### Stage 7: Playing XI & Impact Player Dynamic Optimizer
* **Objective:** Deliver algorithmic team selection and tactical substitution guidance.
* **Deliverables:**
  * Integer Linear Programming (ILP) optimizer for optimal XI based on venue and opposition.
  * Impact Player decision trees: dynamic batting-first vs bowling-first substitution matrices.
  * Emergency contingency substitution models.

### Stage 8: Opposition Intelligence & Scouting Engine
* **Objective:** Provide automated reconnaissance on rival IPL franchises and player pools.
* **Deliverables:**
  * Rival team tactical tendencies and captaincy decision trees.
  * Domestic uncapped player scouting database (SMAT, Ranji, VHT).
  * Confidential scout observation ingestion and qualitative scoring UI.

### Stage 9: In-Season IPL 2026 Real-Time Intelligence
* **Objective:** Provide live match-day intelligence and in-game tactical advisory.
* **Deliverables:**
  * Pre-match executive briefing packets generated 24h before matchday.
  * Live Win Probability Added (WPA) and Expected Runs Added (ERA) calculators.
  * Post-match tactical decision review engine (DRS accuracy, bowling rotation audit).

### Stage 10: Hidden Talent Discovery Engine
* **Objective:** Discover undervalued, high-ceiling domestic and global cricketers.
* **Deliverables:**
  * Algorithmic anomaly detector across state and lower-tier tournaments.
  * Biomechanical ceiling indicators (bat speed, release velocity).
  * Age-adjusted performance projection curves for players under 23.

### Stage 11: Counterfactual Match & Roster What-If Simulator
* **Objective:** Enable coaching staff to simulate tactical scenarios and roster substitutions.
* **Deliverables:**
  * Ball-by-ball Markov chain match simulator.
  * Injury and replacement simulation: quantifying marginal net win percentage change.
  * What-if tactical sandbox for strategic timeouts.

### Stage 12: IPL 2027 Auction Decision Support Hub
* **Objective:** Deliver the mission-critical war-room command center for the IPL 2027 Auction.
* **Deliverables:**
  * Player market valuation models and Wins Above Replacement (WAR) per INR crore.
  * Rival franchise purse exhaustion trackers and paddle-bidding threshold calculators.
  * Dynamic auction roster builder with purse optimization.

### Stage 13: Enterprise Hardening, Security Audit & Operational Handover
* **Objective:** Finalize production infrastructure, perform penetration testing, and train RR staff.
* **Deliverables:**
  * End-to-end security audit and proprietary data vault penetration testing.
  * High-availability failover configuration and sub-second caching latency validation.
  * Operational runbooks, user manuals, and coaching staff handover documentation.
