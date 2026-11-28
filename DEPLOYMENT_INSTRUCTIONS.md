# ROYALS INTELLIGENCE — Production Deployment Runbook

**Target Environments:** Render (FastAPI Backend) & Vercel (Next.js Frontend)  
**Branch:** `release/royals-intelligence-production`  
**Security Standard:** Strict Server-Side Authentication & Zero Data Leaks  

---

## 1. Architecture & Deployment Workflow Separation

Production deployment consists of four strictly isolated phases:
1. **Application Deployment (Render Backend):** Builds and runs the Docker image (`backend/Dockerfile`). Docker image contains only application code and dependencies—**no raw or protected datasets**.
2. **Runtime Dataset Provisioning (Render Persistent Disk):** Authoritative datasets are mounted externally to `/var/data` via Render Persistent Disk.
3. **Database Migration (PostgreSQL):** Applies schema migrations via Alembic.
4. **Frontend Deployment (Vercel):** Builds static Next.js pages and points API calls to Render.

---

## 2. Frontend Configuration (Vercel)

### Environment Variables
Configure in **Vercel Project Settings $\rightarrow$ Environment Variables**:

| Variable Name | Required? | Recommended Production Value | Notes |
| :--- | :--- | :--- | :--- |
| `NEXT_PUBLIC_API_URL` | **Mandatory** | `https://royals-intelligence-api.onrender.com/api/v1` | **Must include `/api/v1` prefix** and no trailing slash. |

> [!WARNING]
> `NEXT_PUBLIC_SCOUT_ADMIN_TOKEN` has been **completely removed**. Administrative credentials must NEVER be placed in any `NEXT_PUBLIC_` environment variable or browser bundle.

### Build & Output Settings
- **Framework Preset:** Next.js
- **Build Command:** `npm run build`
- **Output Directory:** `.next`
- **Node.js Version:** 20.x or 22.x

---

## 3. Backend Configuration (Render)

### Service Details
- **Environment:** Docker
- **Dockerfile Path:** `backend/Dockerfile`
- **Port:** Render dynamically assigns `$PORT` (typically 10000). The Dockerfile automatically binds to `0.0.0.0:${PORT:-8000}`.

### Environment Variables
Configure in **Render Dashboard $\rightarrow$ Environment**:

| Variable Name | Required? | Example / Value Specification | Purpose |
| :--- | :--- | :--- | :--- |
| `ENVIRONMENT` | **Mandatory** | `production` | Enables production security validators and turns off debug echo. |
| `SECRET_KEY` | **Mandatory** | *(Generate unique $\ge 32$ character secret)* | Used for cryptographic session signing. Fails closed if default or $<32$ characters. |
| `SCOUT_ADMIN_API_KEY` | **Mandatory in Production** | *(Generate unique high-entropy token)* | Required at startup when `ENVIRONMENT=production` (enforced by `validate_production_security`). Authorizes administrative scouting mutations. |
| `LEAD_ANALYST_API_KEY` | **Mandatory in Production** | *(Generate unique high-entropy token)* | Required at startup when `ENVIRONMENT=production`. Authorizes lead analyst mutations. |
| `BACKEND_CORS_ORIGINS` | **Mandatory** | `https://royals-intelligence.vercel.app` | Comma-separated list of allowed origins. (`https://*.vercel.app` is auto-allowed via regex). |
| `DATA_DIR` | **Mandatory** | `/var/data` | Root path where Render Persistent Disk is mounted. |
| `DATABASE_URL` | Optional / Recommended | `postgresql+asyncpg://user:pass@host:5432/db` | Render PostgreSQL URL. Automatically converted from `postgres://` to `postgresql+asyncpg://`. |
| `REDIS_URL` | **Optional** | `redis://localhost:6379/0` | **Standby only.** No active application features depend on Redis. |

> [!IMPORTANT]
> The previously hardcoded legacy token `"rr_scout_admin_secret_token_2026"` has been **permanently revoked** in `backend/app/core/security.py`. Render operators must generate and set a fresh, secret `SCOUT_ADMIN_API_KEY` in the Render environment settings.

---

## 4. Runtime Data Asset Hydration Matrix (12 Required Datasets)

The backend requires 12 runtime datasets resolved deterministically via `backend/app/core/config.py:resolve_asset_path()`.

### Persistent Disk Layout (`/var/data`):
```text
/var/data/
├── canonical_player_registry.parquet          (~67 KB)
├── senior_international_eligibility_ledger.parquet (~78 KB)
├── delivery_states_strict.parquet             (~25 MB)
├── competitions.csv                           (~2 KB)
├── matches.csv                                (~150 KB)
├── playing_eleven.csv                         (~400 KB)
├── competition_team_player_mapping.csv        (~1.3 MB)
├── teams.csv                                  (~2 KB)
└── pressure/
    ├── batting_leaderboard.parquet            (~121 KB)
    ├── bowling_leaderboard.parquet            (~107 KB)
    ├── batting_evidence_profiles.parquet      (~100 KB)
    └── bowling_evidence_profiles.parquet      (~80 KB)
```
*(Note: The resolver also seamlessly supports placing the four pressure Parquet files directly under `/var/data/`).*

### Complete Asset Inventory:

| # | Asset Filename | Expected Mount Location | Storage Type | Size | Required? | Sensitivity |
| :-: | :--- | :--- | :--- | :-: | :-: | :--- |
| 1 | `canonical_player_registry.parquet` | `$DATA_DIR/canonical_player_registry.parquet` | Render Disk / Secret File | ~67 KB | **Yes** | Standard Registry |
| 2 | `senior_international_eligibility_ledger.parquet` | `$DATA_DIR/senior_international_eligibility_ledger.parquet` | Render Disk / Secret File | ~78 KB | **Yes** | Senior Cap Ledger |
| 3 | `delivery_states_strict.parquet` | `$DATA_DIR/delivery_states_strict.parquet` | **Render Persistent Disk** | ~25 MB | **Yes** | **Confidential Match Telemetry** |
| 4 | `competitions.csv` | `$DATA_DIR/competitions.csv` | Render Disk / Secret File | ~2 KB | **Yes** | Tournament Catalog |
| 5 | `matches.csv` | `$DATA_DIR/matches.csv` | Render Disk / Secret File | ~150 KB | **Yes** | Match Fixtures |
| 6 | `playing_eleven.csv` | `$DATA_DIR/playing_eleven.csv` | Render Disk / Secret File | ~400 KB | **Yes** | Lineup Registry |
| 7 | `competition_team_player_mapping.csv` | `$DATA_DIR/competition_team_player_mapping.csv` | Render Disk / Secret File | ~1.3 MB | **Yes** | Player-Team Mapping |
| 8 | `teams.csv` | `$DATA_DIR/teams.csv` | Render Disk / Secret File | ~2 KB | Optional | Team Details |
| 9 | `batting_leaderboard.parquet` | `$DATA_DIR/pressure/batting_leaderboard.parquet` | **Render Persistent Disk** | ~121 KB | **Yes** | **Sealed Pressure Ranking** |
| 10 | `bowling_leaderboard.parquet` | `$DATA_DIR/pressure/bowling_leaderboard.parquet` | **Render Persistent Disk** | ~107 KB | **Yes** | **Sealed Pressure Ranking** |
| 11 | `batting_evidence_profiles.parquet` | `$DATA_DIR/pressure/batting_evidence_profiles.parquet` | **Render Persistent Disk** | ~100 KB | **Yes** | **Candidate Evidence Dossier** |
| 12 | `bowling_evidence_profiles.parquet` | `$DATA_DIR/pressure/bowling_evidence_profiles.parquet` | **Render Persistent Disk** | ~80 KB | **Yes** | **Candidate Evidence Dossier** |

### Step-by-Step Dataset Provisioning Procedure:
1. Attach a **1 GB Render Persistent Disk** mounted at `/var/data` to the backend web service.
2. In the Render service dashboard, open the Shell tab (or use SCP/SSH) and upload the 12 assets into `/var/data` matching the layout above.
3. Validate presence and readability of all 12 assets before routing production traffic:
   ```bash
   python -c "from app.core.config import resolve_asset_path; import pandas as pd; assets = ['canonical_player_registry.parquet', 'senior_international_eligibility_ledger.parquet', 'delivery_states_strict.parquet', 'competitions.csv', 'matches.csv', 'playing_eleven.csv', 'competition_team_player_mapping.csv', 'teams.csv', 'batting_leaderboard.parquet', 'bowling_leaderboard.parquet', 'batting_evidence_profiles.parquet', 'bowling_evidence_profiles.parquet']; [print(f'OK: {a:<45} | Rows: {len(pd.read_parquet(resolve_asset_path(a)) if a.endswith(\".parquet\") else pd.read_csv(resolve_asset_path(a))):>6}') for a in assets]; print('ALL 12 ASSETS EXIST AND ARE 100% READABLE!')"
   ```
4. **Missing Asset Diagnosis:**
   If any Pressure Intelligence dataset is missing from disk, endpoints `/api/v1/analytics/pressure/*` return HTTP 503 (`Service Unavailable`) with a descriptive message naming the missing asset. The base application (`/health`, `/api/v1/health`) remains fully operational.
5. **Asset Updates:**
   To update rankings or data packs, upload new Parquet artifacts to `/var/data` and restart the service via the Render dashboard.

---

## 5. Health & Verification Endpoints

- **Root Liveness Probe:** `GET /health`  
  Returns HTTP 200 with `{"status": "healthy", "project": "Royals Intelligence"}`. Used by cloud load balancers and Render health checks.
- **Deep Diagnostics & Readiness Probe:** `GET /api/v1/health`  
  Returns HTTP 200 with component statuses (`api`, `database`, `redis`). If PostgreSQL is offline, returns HTTP 200 with `database: offline_or_unreachable` (analytics endpoints remain operational).
- **Pressure Intelligence Probe:** `GET /api/v1/analytics/pressure/overview`  
  Returns HTTP 200 with official delivery counts (`strict_pressure_bowling_balls: 37014`, `strict_pressure_batting_balls: 31163`).

---

## 6. Database Migrations (PostgreSQL)

If PostgreSQL is enabled for administrative audit trails, run migrations prior to service traffic:
```bash
cd backend
alembic upgrade head
```
Revisions:
- `001_uncapped_player_foundation.py`
- `002_venue_pitch_weather.py`
