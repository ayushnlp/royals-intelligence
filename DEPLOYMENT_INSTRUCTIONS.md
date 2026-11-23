# ROYALS INTELLIGENCE — Production Deployment Runbook

**Target Environments:** Render (FastAPI Backend) & Vercel (Next.js Frontend)  
**Branch:** `release/royals-intelligence-production`  
**Security Standard:** Strict Server-Side Authentication & Zero Data Leaks  

---

## 1. Frontend Configuration (Vercel)

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

## 2. Backend Configuration (Render)

### Service Details
- **Environment:** Docker or Python 3.12
- **Dockerfile Path:** `backend/Dockerfile`
- **Port:** Render dynamically assigns `$PORT` (typically 10000). The Dockerfile automatically binds to `0.0.0.0:${PORT:-8000}`.

### Environment Variables
Configure in **Render Dashboard $\rightarrow$ Environment**:

| Variable Name | Required? | Example / Value Specification | Purpose |
| :--- | :--- | :--- | :--- |
| `ENVIRONMENT` | **Mandatory** | `production` | Enables production security validators and turns off debug echo. |
| `SECRET_KEY` | **Mandatory** | *(Generate unique $\ge 32$ character secret)* | Used for cryptographic session signing. Fails closed if default. |
| `SCOUT_ADMIN_API_KEY` | **Mandatory for Admin** | *(Generate unique high-entropy token)* | Required for administrative scouting mutations and audit logging. |
| `LEAD_ANALYST_API_KEY` | **Mandatory for Analyst** | *(Generate unique high-entropy token)* | Required for analyst-tier mutations. |
| `BACKEND_CORS_ORIGINS` | **Mandatory** | `https://royals-intelligence.vercel.app` | Comma-separated list of allowed origins. (`https://*.vercel.app` is auto-allowed via regex). |
| `DATA_DIR` | **Mandatory** | `/var/data` (Render Disk) or `/etc/secrets` | Root path where runtime authorized data assets are mounted. |
| `DATABASE_URL` | Optional / Recommended | `postgresql+asyncpg://user:pass@host:5432/db` | Render PostgreSQL URL. Automatically converted from `postgres://` to `postgresql+asyncpg://`. |
| `REDIS_URL` | **Optional** | `redis://localhost:6379/0` | **Standby only.** No active application features depend on Redis. |

> [!IMPORTANT]
> The previously hardcoded legacy token `"rr_scout_admin_secret_token_2026"` has been **permanently revoked** in `backend/app/core/security.py`. Render operators must generate and set a fresh, secret `SCOUT_ADMIN_API_KEY` in the Render environment settings.

---

## 3. Runtime Data Asset Hydration Matrix

The backend requires 8 runtime datasets resolved deterministically via `backend/app/core/config.py:resolve_asset_path()`.

| Asset Filename | Expected Mount Location | Storage Type | Size | Required? | Sensitivity |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `canonical_player_registry.parquet` | `$DATA_DIR/canonical_player_registry.parquet` | Git / Secret File / Disk | ~67 KB | **Yes** | Standard Registry |
| `senior_international_eligibility_ledger.parquet` | `$DATA_DIR/senior_international_eligibility_ledger.parquet` | Git / Secret File / Disk | ~78 KB | **Yes** | Standard Ledger |
| `delivery_states_strict.parquet` | `$DATA_DIR/delivery_states_strict.parquet` | **Render Persistent Disk** (`/var/data`) | ~25 MB | **Yes** | **Confidential Match Telemetry** |
| `competitions.csv` | `$DATA_DIR/competitions.csv` | Secret File / Disk | ~2 KB | **Yes** | Tournament Catalog |
| `matches.csv` | `$DATA_DIR/matches.csv` | Secret File / Disk | ~150 KB | **Yes** | Match Fixtures |
| `playing_eleven.csv` | `$DATA_DIR/playing_eleven.csv` | Secret File / Disk | ~400 KB | **Yes** | Lineup Registry |
| `competition_team_player_mapping.csv` | `$DATA_DIR/competition_team_player_mapping.csv` | Git / Secret File / Disk | ~1.3 MB | **Yes** | Player-Team Mapping |
| `teams.csv` | `$DATA_DIR/teams.csv` | Secret File / Disk | ~2 KB | Optional | Team Details |

### Storage Mounting Guidelines on Render:
1. **Render Secret Files (`/etc/secrets`):** Suitable for small CSVs and lookup files ($\le 512$ KB).
2. **Render Persistent Disk (`/var/data`):** Attach a 1 GB persistent disk mounted at `/var/data` for heavy Parquet assets (`delivery_states_strict.parquet`).

---

## 4. Health & Verification Endpoints

- **Root Liveness Probe:** `GET /health`  
  Returns HTTP 200 with `{"status": "healthy", "project": "Royals Intelligence"}`. Used by cloud load balancers and Render health checks.
- **Deep Diagnostics & Readiness Probe:** `GET /api/v1/health`  
  Returns HTTP 200 with component statuses (`api`, `database`, `redis`). If PostgreSQL is offline, returns HTTP 200 with `database: offline_or_unreachable` (analytics endpoints remain operational).

---

## 5. Database Migrations (PostgreSQL)

If PostgreSQL is enabled for administrative audit trails, run migrations prior to service traffic:
```bash
cd backend
alembic upgrade head
```
Revisions:
- `001_uncapped_player_foundation.py`
- `002_venue_pitch_weather.py`
