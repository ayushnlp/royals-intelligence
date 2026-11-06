# ROYALS INTELLIGENCE

> **A Rajasthan Royals-focused Cricket Intelligence, Performance Analytics, Talent Scouting and IPL 2027 Auction Decision Support Platform.**

[![Current Stage](https://img.shields.io/badge/Stage-0%20(Foundation)-E91E8F?style=for-the-badge)](./docs/STAGE_STATUS.md)
[![Python](https://img.shields.io/badge/Python-3.12-101C37?style=for-the-badge&logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-15+-000000?style=for-the-badge&logo=next.js)](https://nextjs.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?style=for-the-badge&logo=postgresql)](https://postgresql.org)
[![Redis](https://img.shields.io/badge/Redis-7-DC382D?style=for-the-badge&logo=redis)](https://redis.io)

---

## 1. Project Purpose & Strategic Objective

ROYALS INTELLIGENCE is an elite, evidence-driven sports intelligence platform engineered exclusively for the **Rajasthan Royals (RR)** franchise. 

- **Primary Analytical Season:** IPL 2026.
- **Strategic Objective:** Develop an evidence-driven recruitment, roster optimization, and auction strategy for **Rajasthan Royals IPL 2027 Auction**.

The platform bridges cutting-edge cricket analytics, machine learning simulation models, real-time match condition forecasting, and confidential scouting workflows to give Rajasthan Royals decision-makers an asymmetric competitive advantage.

---

## 2. Planned Functional Scope

### Core Analytical Modules (1 to 20)
1. **IPL 2026 Season Intelligence:** Macro campaign tracking, NRR sensitivity, and playoff path simulations.
2. **Match-by-Match Intelligence:** Tactical pre-game briefing packets, phase leverage, and WPA analysis.
3. **Stadium and Venue Intelligence:** Boundary geometries, air density, altitude, and chasing bias.
4. **Pitch and Weather Intelligence:** Soil composition tracking, pitch wear curves, and dew factor modeling.
5. **Batting Intelligence:** Entry point acceleration, false shot rates, dot ball mitigation, pace-vs-spin splits.
6. **Bowling Intelligence:** Release height consistency, length cluster heatmaps, variation efficacy.
7. **All-Rounder Intelligence:** Dual-skill impact scoring, 3D balance index, phase bridging utility.
8. **Uncapped Player Scouting:** SMAT, Ranji Trophy, VHT talent discovery with competition normalization.
9. **Capped Player Scouting:** Global franchise surveillance, aging curves, and workload management.
10. **Opposition Intelligence:** Rival franchise decision trees, captaincy triggers, and bench depth vulnerabilities.
11. **Player vs Player Matchups:** Head-to-head empirical matchups and archetype clustering.
12. **Batting Position and Bowling Role Intelligence:** Anchor/Enforcer/Finisher role optimization.
13. **Playing XI and Impact Player Optimisation:** Dynamic integer linear programming XI optimizer.
14. **Predictive Match Condition Engine:** Real-time win probability and par score decay.
15. **IPL 2027 Auction Intelligence:** Dynamic price estimation, WAR per crore, and purse optimization.
16. **Fielding and Wicketkeeping Intelligence:** Runs saved, catch conversion probability, stumping metrics.
17. **Partnership Analysis:** Strike rotation fluidity, right-left synergy, bowling hunting pairs.
18. **Player Form and Development Tracking:** Exponential moving average form tracking, technical flaw alerts.
19. **Tactical Decision Review:** DRS accuracy analysis and opportunity cost audits.
20. **Data Reliability and Model Explainability:** Sample size confidence intervals, SHAP value explainers.

### Advanced Strategic Features (21 to 26)
21. **Hidden Talent Discovery Engine:** Algorithmic anomaly detection for undervalued domestic cricketers.
22. **Replacement and Upgrade Simulator:** Monte Carlo roster delta simulation for injury/availability scenarios.
23. **What-If Match Simulator:** Counterfactual ball-by-ball scenario sandbox.
24. **Form and Development Tracker:** Longitudinal biomechanical and skill trajectory modeling.
25. **Evidence and Confidence Engine:** Transparent confidence ratings and Bayesian credibility bounds.
26. **AI Scouting Report Generator:** Automated executive briefings anchored to verified statistical pipelines.

*Full details available in [docs/PROJECT_BLUEPRINT.md](./docs/PROJECT_BLUEPRINT.md).*

---

## 3. Technology Stack

| Layer | Technologies |
| :--- | :--- |
| **Frontend** | Next.js 15+, React 19, TypeScript, Tailwind CSS, Lucide Icons, Plotly / ECharts compatible |
| **Backend** | Python 3.12, FastAPI, Pydantic v2, Pydantic-Settings, SQLAlchemy 2.0 Async, AsyncPG, Alembic |
| **Database** | PostgreSQL 16 (TimescaleDB ready), connection pooling with AsyncPG |
| **Cache & Tasks** | Redis 7, Celery task queue integration |
| **Analytics Engine**| Pandas, NumPy, SciPy, Scikit-learn, Matplotlib |
| **Infrastructure** | Docker, Docker Compose, Pytest, GitHub Actions CI/CD |

---

## 4. Repository Structure

```
royals-intelligence/
├── frontend/                     # Next.js App Router frontend application
│   ├── src/
│   │   ├── app/                  # Application routes and layouts
│   │   ├── components/           # UI and Layout components
│   │   ├── features/             # Domain-specific feature modules
│   │   ├── hooks/                # React custom hooks
│   │   ├── lib/                  # Utilities and API clients
│   │   ├── services/             # Frontend HTTP services
│   │   ├── types/                # TypeScript type definitions
│   │   └── styles/               # Global styling and Tailwind directives
│   ├── public/                   # Static public assets
│   ├── package.json              # Frontend dependencies and scripts
│   └── tsconfig.json             # TypeScript configuration
├── backend/                      # FastAPI asynchronous backend application
│   ├── app/
│   │   ├── api/v1/               # Versioned API routes (/health, etc.)
│   │   ├── core/                 # Settings, configuration, logging
│   │   ├── db/                   # Async database engine, session, Base
│   │   ├── models/               # SQLAlchemy ORM models (Stage 2+)
│   │   ├── schemas/              # Pydantic request/response schemas
│   │   ├── services/             # Core business logic services
│   │   ├── repositories/         # Database access repository pattern
│   │   ├── analytics/            # Mathematical & ML analytics modules
│   │   ├── pipelines/            # Ingestion & transformation pipelines
│   │   └── main.py               # FastAPI application entrypoint
│   ├── alembic/                  # Alembic database migration environment
│   ├── tests/                    # Pytest test suite
│   └── requirements.txt          # Backend Python dependencies
├── data/                         # Data storage partition
│   ├── raw/                      # Immutable raw data feeds (gitignored)
│   ├── processed/                # Parquet analytics tables (gitignored)
│   ├── external/                 # Venues and meteorological reference data
│   └── metadata/                 # Schemas and player identity mappings
├── reports/                      # Tactical reports and exports
│   ├── generated/                # Automated PDF/Markdown reports
│   └── templates/                # Report styling templates
├── docs/                         # Platform Architecture & Strategy Documentation
│   ├── PROJECT_BLUEPRINT.md      # Comprehensive 26-module specification
│   ├── ARCHITECTURE.md           # Monorepo and system architecture
│   ├── DATABASE_DESIGN.md        # Relational schema roadmap
│   ├── DATA_STRATEGY.md          # Public vs proprietary data partition
│   ├── API_DESIGN.md             # REST API standard & OpenAPI specs
│   ├── DEVELOPMENT_ROADMAP.md    # Stages 0 through 13 milestones
│   ├── DESIGN_SYSTEM.md          # Rajasthan Royals visual identity tokens
│   ├── SECURITY.md               # Secret hygiene & confidentiality policy
│   └── STAGE_STATUS.md           # Real-time implementation ledger
├── scripts/                      # Operational automation & validation scripts
├── infrastructure/               # Docker & deployment manifests
│   └── docker/
├── .github/workflows/            # CI/CD pipelines
├── .gitignore                    # Comprehensive multi-language ignore rules
├── .env.example                  # Root environment template
├── docker-compose.yml            # Local multi-service orchestration
├── README.md                     # This file
└── LICENSE                       # Proprietary Rajasthan Royals license
```

---

## 5. Getting Started & Installation

### Prerequisites
- **Node.js:** v20+ (v24 LTS recommended)
- **Python:** v3.12+
- **Docker & Docker Compose:** optional for full containerized stack
- **Git**

### 1. Clone & Setup Environment Files
```bash
# Clone the repository
git clone <repository-url> royals-intelligence
cd royals-intelligence

# Initialize local environment files from templates
cp .env.example .env
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env.local
```

### 2. Backend Setup
```bash
cd backend

# Create and activate Python virtual environment
python -m venv .venv
# On Windows PowerShell:
.venv\Scripts\Activate.ps1
# On Linux/macOS:
# source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run backend test suite
pytest

# Launch FastAPI development server (starts on http://localhost:8000)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Frontend Setup
```bash
cd ../frontend

# Install dependencies
npm install

# Run type check and linting
npm run type-check
npm run lint

# Launch Next.js development server (starts on http://localhost:3000)
npm run dev
```

### 4. Running via Docker Compose
```bash
# From the repository root
docker compose up -d --build

# View container logs
docker compose logs -f
```

---

## 6. Health & Diagnostic Endpoints

The backend exposes verified health endpoints:
- `GET http://localhost:8000/health`: Quick liveness check.
- `GET http://localhost:8000/api/v1/health`: Deep diagnostics probe (reports DB engine, Redis, uptime).

---

## 7. Security & Confidentiality

- **Zero Secret Commits:** Secrets, credentials, and private keys must never be committed to Git.
- **Proprietary Data Vault:** All scouting assessments, internal valuations, and medical records reside in encrypted, gitignored directories (`data/proprietary/`).
- Refer to [docs/SECURITY.md](./docs/SECURITY.md) for full compliance protocols.

---

## 8. Current Stage & Next Steps

- **Current Status:** **Stage 0 Complete & Verified**.
- **Next Stage:** **Stage 1 — Data Ingestion Infrastructure & Historical Data Pipelines** (Awaiting user authorization).
