# ROYALS INTELLIGENCE — SYSTEM ARCHITECTURE
**Architecture Version:** 1.0.0 (Stage 0 Baseline)  
**System Type:** Monorepo Distributed High-Performance Sports Analytics System  

---

## 1. Architectural Principles

1. **Modularity & Loose Coupling:** Frontend, backend, database migrations, and analytics pipelines reside in clean, independent domains within the monorepo.
2. **Evidence-Driven Integrity:** Zero mock data in production surfaces. If data is absent, explicit "Pending Data Integration" or "Sample Too Small" states are displayed.
3. **Async-First Backend:** Fully asynchronous I/O with FastAPI, SQLAlchemy 2.0 Async, and AsyncPG for high concurrency during live match operations.
4. **Data Isolation & Confidentiality:** Strict boundary separating public ball-by-ball datasets from proprietary Rajasthan Royals scouting dossiers, medical reports, and auction valuations.
5. **Explainability by Design:** Every predictive model output is architected to surface confidence bands, sample counts, and feature attributions.

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
|  | - Endpoints: /health, /api/v1/health (System status, DB health check)       |  |
|  | - CORS Security & Rate Limiting Guardrails                                  |  |
|  +---------------------------------------+-------------------------------------+  |
+------------------------------------------|----------------------------------------+
                                           | Async SQLAlchemy 2.0 / AsyncPG
                                           v
+-----------------------------------------------------------------------------------+
|                               PERSISTENCE & CACHE                                 |
|                                                                                   |
|  +---------------------------------------+  +----------------------------------+  |
|  | PostgreSQL 16 (Timescale Ready)       |  | Redis 7 (Cache & Task Broker)    |  |
|  | - Ball-by-ball relational schema      |  | - Live score & state cache       |  |
|  | - Venue & Weather telemetry           |  | - Celery async task queue broker |  |
|  | - Scouting & Auction entity models    |  | - Rate limiting state            |  |
|  +---------------------------------------+  +----------------------------------+  |
+-----------------------------------------------------------------------------------+
                                           ^
                                           | Ingestion / Transformation / Scoring
+------------------------------------------+----------------------------------------+
|                                DATA & ANALYTICS LAYER                             |
|                                                                                   |
|  +-----------------------+  +------------------------+  +----------------------+  |
|  | Ingestion Pipelines   |  | Analytics Engine       |  | Machine Learning     |  |
|  | - Ball-by-ball feeds  |  | - Pandas / NumPy       |  | - Scikit-learn       |  |
|  | - Tracking telemetry  |  | - SciPy statistics     |  | - Monte Carlo sims   |  |
|  | - Scouting logs (RR)  |  | - Matchup matrices     |  | - Bayesian models    |  |
|  +-----------------------+  +------------------------+  +----------------------+  |
+-----------------------------------------------------------------------------------+
```

---

## 3. Frontend Architecture

* **Framework:** Next.js (App Router) with React, TypeScript.
* **Styling & Theming:** Tailwind CSS utilizing Rajasthan Royals brand tokens:
  * Primary / Royal Navy: `#101C37`
  * Accent / Royals Pink: `#E91E8F`
  * Auxiliary Gold: `#D6B56D`
  * Surface Light Grey: `#F4F6FA`
  * Base White: `#FFFFFF`
* **Component Architecture:**
  * `components/layout`: Application Shell, Sidebar navigation, Header, Breadcrumbs.
  * `components/ui`: Accessible primitives (cards, badges, buttons, tables, empty states).
  * `features`: Domain-specific view controllers (Matchup viewer, Auction matrix, Scouting dossiers).
  * `lib`: Utility functions, API client wrappers, design system helpers.
  * `types`: TypeScript interfaces shared with API schemas.

---

## 4. Backend Architecture

* **Framework:** FastAPI with Python 3.12.
* **Core Subsystems:**
  * `app/core/config.py`: Centralized environment management using Pydantic Settings (`pydantic-settings`).
  * `app/core/logging.py`: Structured JSON logging with request correlation IDs and latency profiling.
  * `app/api/v1/router.py`: Centralized API versioning router grouping domain sub-routers.
  * `app/api/v1/endpoints/health.py`: Dual health check routes (`/health` and `/api/v1/health`) performing deep dependency validation (database, redis, disk space).
  * `app/db/session.py`: Asynchronous SQLAlchemy session management with connection pool configuration.
  * `app/db/base.py`: Declarative base metadata class for entity definitions.
* **Error Handling:** Central exception handlers intercepting validation errors, database timeouts, and unhandled exceptions to return consistent RFC-7807 problem details.

---

## 5. Database Architecture

* **RDBMS:** PostgreSQL 16.
* **Driver & ORM:** `asyncpg` with SQLAlchemy 2.0 Async IO.
* **Migrations:** Alembic configured in asynchronous mode (`alembic/env.py`) for reproducible, version-controlled schema evolution.
* **Connection Pooling:**
  * Standard pool size: 10 connections.
  * Max overflow: 20 connections.
  * Pool pre-ping: enabled to discard stale sockets.

---

## 6. Data Pipeline Architecture

```
data/
├── raw/         # Immutable raw source feeds (ball-by-ball JSON/CSV, tracking logs)
├── processed/   # Normalized, cleaned, parquet-indexed analytics tables
├── external/    # Public tournament metadata, weather historical records
└── metadata/    # Schema definitions, team mappings, venue coordinates
```
* **Separation Policy:**
  * Public cricket data is ingested and processed through automated batch scripts.
  * Proprietary scouting logs and auction valuations are partitioned with cryptographic encryption and strict role-based access control.

---

## 7. Security Architecture

1. **Zero Secret Leakage:** No plaintext credentials in Git. `.env` files are ignored in root and all subdirectories.
2. **CORS Hardening:** Backend strictly restricts origins to authorized frontend domains.
3. **Data Protection:** Database passwords, JWT secret keys, and data storage paths are configurable via environment variables only.
4. **Isolated Network:** In Docker environments, database and redis are exposed only to the backend internal network, not mapped directly to public host interfaces in production.


---

## 6. Stage 2 Database & Analytics Foundation Architecture

```
+-----------------------------------------------------------------------------------+
|                        STAGE 2 SERVICES & FOUNDATION LAYER                        |
|                                                                                   |
|  +---------------------------+  +----------------------------------------------+  |
|  | PlayerIdentityService     |  | RRDataPackService                            |  |
|  | - Canonical player dedupe |  | - Dynamic schema discovery                   |  |
|  | - External source IDs     |  | - Configurable column mapping                |  |
|  | - Age at 2026-11-18 cutoff|  | - Confidential data masking                  |  |
|  | - 5 eligibility states    |  | - Conflict & missing DOB audit               |  |
|  +-------------+-------------+  +----------------------+-----------------------+  |
|                |                                       |                          |
|                +-------------------+-------------------+                          |
|                                    |                                              |
|                                    v                                              |
|  +---------------------------------+-------------------------------------------+  |
|  | UncappedAnalyticsService        | RelationalLoader                          |  |
|  | - Career batting/bowling aggs   | - Parquet to relational DB sync           |  |
|  | - Phase splits (PP/Middle/Death)| - Foreign key integrity & idempotency     |  |
|  | - Recent form window (last N)   | - Check constraint balance                |  |
|  +---------------------------------+-------------------------------------------+  |
+------------------------------------+----------------------------------------------+
```
