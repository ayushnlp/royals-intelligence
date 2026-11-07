# ROYALS INTELLIGENCE — SYSTEM ARCHITECTURE
**Architecture Version:** 1.2.0 (Stage 4 Baseline)  
**System Type:** Monorepo Distributed High-Performance Sports Analytics System  

---

## 1. Architectural Principles

1. **Modularity & Loose Coupling:** Frontend, backend, database migrations, and analytics pipelines reside in clean, independent domains within the monorepo.
2. **Evidence-Driven Integrity:** Zero mock data in production surfaces. If data is absent, explicit "Pending Data Integration" or "Sample Too Small" states are displayed.
3. **Async-First Backend:** Fully asynchronous I/O with FastAPI, SQLAlchemy 2.0 Async, and AsyncPG for high concurrency during live match operations.
4. **Data Isolation & Confidentiality:** Strict boundary separating public ball-by-ball datasets from proprietary Rajasthan Royals scouting dossiers, medical reports, and auction valuations.
5. **Explainability by Design:** Every predictive model output is architected to surface confidence bands, sample counts, and feature attributions.
6. **Data Provenance & Scientific Integrity:** Observational weather, boundary surveys, and pitch characteristics must never be synthesized or fabricated; unknowns are represented as `None` / `UNAVAILABLE`.

---

## 2. High-Level Architecture Diagram

```
+-----------------------------------------------------------------------------------+
|                                 PRESENTATION LAYER                                |
|                                                                                   |
|  +-----------------------------------------------------------------------------+  |
|  | Next.js App Router (React 19 / TypeScript / Tailwind CSS / Design System)   |  |
|  | - Royals Navy & Pink Visual Identity                                        |  |
|  | - Responsive Analytics Shell (Sidebar, Header, Dynamic Viewports)          |  |
|  | - Command Centers: Domestic (/domestic), Uncapped (/uncapped), Venues (/venues) |
|  | - Pluggable Visualization Engine (Plotly / Apache ECharts Ready)             |  |
|  +-----------------------------------------------------------------------------+  |
+------------------------------------------+----------------------------------------+
                                           | HTTPS / JSON REST API
                                           v
+-----------------------------------------------------------------------------------+
|                               APPLICATION API LAYER                               |
|                                                                                   |
|  +-----------------------------------------------------------------------------+  |
|  | FastAPI Core (Python 3.12 / Pydantic v2 / Structlog / Central Error Handler) |  |
|  | - Versioned API: /api/v1/*                                                  |  |
|  | - Routers: /health, /acquisition, /domestic, /uncapped, /venues, /weather    |  |
|  | - CORS Security, Bearer/API-Key Authorization & Rate Limiting Guardrails    |  |
|  +---------------------------------------+-------------------------------------+  |
+------------------------------------------|----------------------------------------+
                                           | Async SQLAlchemy 2.0 / AsyncPG
                                           v
+-----------------------------------------------------------------------------------+
|                               PERSISTENCE & CACHE                                 |
|                                                                                   |
|  +---------------------------------------+  +----------------------------------+  |
|  | PostgreSQL 16 (Timescale Ready)       |  | Redis 7 (Cache & Task Broker)    |  |
|  | - 31 Relational schema tables         |  | - Live score & state cache       |  |
|  | - Venues, Weather & Pitch reports     |  | - Celery async task queue broker |  |
|  | - Scouting & Auction entity models    |  | - Weather API rate limit state   |  |
|  +---------------------------------------+  +----------------------------------+  |
+-----------------------------------------------------------------------------------+
                                           ^
                                           | Ingestion / Transformation / Scoring
+------------------------------------------+----------------------------------------+
|                                DATA & ANALYTICS LAYER                             |
|                                                                                   |
|  +-----------------------+  +------------------------+  +----------------------+  |
|  | Ingestion Pipelines   |  | Analytics Engines      |  | Environmental Intel  |  |
|  | - Ball-by-ball feeds  |  | - Domestic Season & MoM|  | - Open-Meteo CC-BY   |  |
|  | - Parquet partitioner |  | - Format-aware phases  |  | - Dew Severity Model |  |
|  | - Scouting logs (RR)  |  | - Pitch pace vs spin   |  | - Venue Boundary DB  |  |
|  +-----------------------+  +------------------------+  +----------------------+  |
+-----------------------------------------------------------------------------------+
```

---

## 3. Frontend Architecture

* **Framework:** Next.js (App Router) with React 19, TypeScript.
* **Styling & Theming:** Tailwind CSS utilizing Rajasthan Royals brand tokens:
  * Primary / Royal Navy: `#101C37`
  * Accent / Royals Pink: `#E91E8F`
  * Auxiliary Gold: `#D6B56D`
  * Surface Light Grey: `#F4F6FA`
  * Base White: `#FFFFFF`
* **Command Centers & Pages:**
  * `/`: Mission dashboard, system health and quick action hubs.
  * `/acquisition`: Data ingestion registry, pipeline runner, and dataset audit metrics.
  * `/domestic`: Domestic cricket command center (SMAT, VHT, Ranji), scorecard viewer, phase leverage, FoW, and progression worms.
  * `/uncapped`: Uncapped player talent scouting radar, archetype discovery, and proprietary data pack viewer.
  * `/venues`: Venue, pitch and weather intelligence center, stadium dimensions, scoring par, pace vs spin splits, and dew severity.
* **Component Architecture:**
  * `components/layout`: Application Shell, Sidebar navigation, Header, Breadcrumbs.
  * `components/ui`: Accessible primitives (cards, badges, buttons, tables, empty states).
  * `lib`: Utility functions, API client wrappers, design system helpers.
  * `types`: TypeScript interfaces shared with API schemas.

---

## 4. Backend Architecture

* **Framework:** FastAPI with Python 3.12.
* **Core Subsystems:**
  * `app/core/config.py`: Centralized environment management using Pydantic Settings (`pydantic-settings`).
  * `app/core/logging.py`: Structured JSON logging with request correlation IDs and latency profiling.
  * `app/api/v1/router.py`: Centralized API versioning router grouping domain sub-routers (`health`, `acquisition`, `domestic`, `uncapped`, `venues`, `weather`).
  * `app/db/session.py`: Asynchronous SQLAlchemy session management with connection pool configuration.
  * `app/db/base.py`: Declarative base metadata class for entity definitions.
* **Error Handling:** Central exception handlers intercepting validation errors, database timeouts, and unhandled exceptions to return consistent RFC-7807 problem details.

---

## 5. Database Architecture

* **RDBMS:** PostgreSQL 16.
* **Driver & ORM:** `asyncpg` with SQLAlchemy 2.0 Async IO.
* **Migrations:** Alembic configured in asynchronous mode (`alembic/env.py`) with 2 active version migrations:
  * `001_uncapped_player_foundation.py`: Core competitions, seasons, teams, players, matches, deliveries, and scouting tables.
  * `002_venue_pitch_weather.py`: Venue coordinate/boundary provenance columns, `match_weather_observations`, and `venue_pitch_reports`.
* **Connection Pooling:** Standard pool size of 10 connections with max overflow of 20 and active pre-pinging.

---

## 6. Stage 4 Venue, Pitch and Weather Intelligence Subsystem

```
+-----------------------------------------------------------------------------------+
|                        VENUE & WEATHER INTELLIGENCE SUBSYSTEM                     |
|                                                                                   |
|  +---------------------------+  +----------------------------------------------+  |
|  | VenueIntelligenceService  |  | WeatherIntelligenceService                   |  |
|  | - Verified Venue Catalog  |  | - Open-Meteo CC-BY 4.0 API integration       |  |
|  | - Boundary dimension docs |  | - Empirical Dew Severity risk calculator     |  |
|  | - Scoring par & phase RRs |  | - Forecast vs historical segregation         |  |
|  | - Pitch pace/spin split   |  | - Climate normal offline fallback            |  |
|  | - Uncapped player venue   |  | - Attribution & keyless rate limit audits    |  |
|  +-------------+-------------+  +----------------------+-----------------------+  |
|                |                                       |                          |
|                +-------------------+-------------------+                          |
|                                    |                                              |
|                                    v                                              |
|  +---------------------------------+-------------------------------------------+  |
|  | VenueMatchContextEngine                                                     |  |
|  | - Correlates match scoring variance vs venue historical par                 |  |
|  | - In-match weather progression (temperature drop, humidity rise, dew risk)   |  |
|  | - Strict fallback/synthetic fixture tagging (is_fallback_data: true)       |  |
|  +-----------------------------------------------------------------------------+  |
+-----------------------------------------------------------------------------------+
```

### 6.1. Analytical Governance Rules
1. **No Dimension Guessing:** Physical boundary dimensions must be attributed to an authoritative survey (`BCCI_STADIUM_SPECIFICATIONS_2024`). Missing values are stored as `None` with status `"UNAVAILABLE"`.
2. **Pitch Behavioral Caveats:** Pace vs spin splits and phase economy distributions represent historical empirical statistics under past pitch preparations. They are accompanied by a strict limitations disclaimer stating they do not represent predictive guarantees.
3. **Dew Severity Risk Modeling:** Night match second-innings bowling grip and boundary defense difficulty are modeled based on relative humidity ($\ge 75\%$) and ambient temperature ($\le 26^\circ\text{C}$).
4. **Uncapped Scope Guarding:** Venue prospect performance queries strictly enforce uncapped domestic player status; senior capped international queries are rejected with `403 Forbidden`.
