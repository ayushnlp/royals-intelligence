# ROYALS INTELLIGENCE — REST API ARCHITECTURE SPECIFICATION
**API Version:** v1 (Stage 0 Baseline)  
**Standard:** OpenAPI 3.1 / RFC-7807 Problem Details  
**Base URL:** `http://localhost:8000/api/v1`  

---

## 1. Design Conventions & Standards

1. **Versioning:** All functional endpoints are namespaced under `/api/v1/`. Root health probes reside at `/health` and `/api/v1/health`.
2. **Naming Conventions:**
   - Resource paths use plural nouns in lowercase kebab-case (e.g., `/api/v1/scouting-reports`, `/api/v1/match-simulations`).
   - Query parameters use camelCase (e.g., `?seasonYear=2026&role=batter`).
   - JSON response bodies use snake_case for Python/Pydantic alignment.
3. **HTTP Status Codes:**
   - `200 OK`: Successful retrieval or execution.
   - `201 Created`: Resource successfully created.
   - `400 Bad Request`: Validation failure or invalid query parameters.
   - `404 Not Found`: Target entity does not exist.
   - `422 Unprocessable Entity`: Schema validation error.
   - `500 Internal Server Error`: Unhandled server or pipeline error.
   - `503 Service Unavailable`: Dependent service (e.g., Database, Redis) unreachable.

---

## 2. Implemented Stage 0 Endpoints

### 2.1. Root Health Check
* **Route:** `GET /health`
* **Purpose:** Lightweight container orchestrator / load balancer liveness probe.
* **Response Body:**
```json
{
  "status": "healthy",
  "project": "Royals Intelligence",
  "version": "0.1.0-stage0",
  "environment": "development",
  "timestamp": "2026-11-07T04:15:00.000Z"
}
```

### 2.2. API v1 Deep Health & Diagnostics Check
* **Route:** `GET /api/v1/health`
* **Purpose:** Deep readiness probe verifying service uptime and downstream dependencies (PostgreSQL database engine, Redis connection).
* **Response Body:**
```json
{
  "status": "healthy",
  "api_version": "v1",
  "environment": "development",
  "timestamp": "2026-11-07T04:15:00.000Z",
  "components": {
    "database": {
      "status": "connected",
      "engine": "postgresql+asyncpg",
      "pool_size": 10
    },
    "redis": {
      "status": "standby"
    }
  }
}
```

### 2.3. Data Acquisition Engine Endpoints (Stage 1)

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/v1/acquisition/sources` | Lists registered cricket data sources with reliability tiers and legal licensing |
| `GET` | `/api/v1/acquisition/sources/{source_id}` | Detailed source specifications, update frequency, and known gaps |
| `GET` | `/api/v1/acquisition/sources/{source_id}/health` | Operational availability probe and access constraints |
| `GET` | `/api/v1/acquisition/runs` | List recent ingestion runs with execution duration and validation completeness |
| `GET` | `/api/v1/acquisition/runs/{run_id}` | Detailed execution log, SHA-256 checksums, and validation error records |
| `POST`| `/api/v1/acquisition/runs` | Trigger an authorized ingestion run over a specified raw folder / source |
| `GET` | `/api/v1/acquisition/datasets` | List acquired dataset manifests with record counts and Parquet paths |
| `GET` | `/api/v1/acquisition/datasets/{dataset_id}` | Retrieve provenance manifest and SHA-256 hashes for an acquired dataset |
| `GET` | `/api/v1/acquisition/coverage` | Comprehensive tournament coverage audit across IPL 2026, SMAT, Ranji |
| `POST`| `/api/v1/acquisition/upload` | Safe manual upload for user-supplied JSON/CSV datasets with SHA-256 verification |

---

## 3. Centralized Error Response Format

All error responses adhere to RFC-7807 problem details:

```json
{
  "title": "Validation Error",
  "status": 422,
  "detail": "Field 'season' is required and must match pattern 'IPL [0-9]{4}'",
  "instance": "/api/v1/matches",
  "timestamp": "2026-11-07T04:15:00.000Z"
}
```

---

## 4. Future API Endpoint Standards (Stages 1–13)

### 4.1. Standard Pagination Schema
All list endpoints will support cursor or offset-based pagination:
```
GET /api/v1/players?limit=25&offset=0
```
Response:
```json
{
  "items": [],
  "total": 0,
  "limit": 25,
  "offset": 0,
  "has_more": false
}
```

### 4.2. Sample Size & Confidence Metadata
Every analytics endpoint will return confidence telemetry:
```json
{
  "player_id": "...",
  "metric_name": "strike_rate_vs_left_arm_pace",
  "value": 146.2,
  "sample_balls": 48,
  "confidence_interval": [132.0, 160.4],
  "confidence_rating": "MODERATE"
}
```


---

## 5. Implemented Stage 2 Endpoints (Uncapped Players & Analytics)

### 5.1. Uncapped Players Directory
* **Route:** `GET /api/v1/players`
* **Query Parameters:** `eligibility`, `tier`, `role`, `state`, `trialist_only`
* **Response:** Array of `UncappedPlayerSummary` objects with calculated age at cutoff (`2026-11-18`), verification badges, and primary discipline.

### 5.2. Granular Player Profile & Provenance
* **Route:** `GET /api/v1/players/{player_id}`
* **Response:** Detailed `UncappedPlayerDetail` including all multi-source external IDs, DOB source, and verification history notes.

### 5.3. Audit & Update Eligibility
* **Route:** `POST /api/v1/players/{player_id}/verify-eligibility`
* **Payload:** `{"new_status": "...", "verification_notes": "...", "verified_by": "..."}`
* **Response:** `EligibilityVerificationResponse` with timestamp and previous/new status.

### 5.4. Career Batting & Phase Breakdown
* **Route:** `GET /api/v1/analytics/players/{player_id}/batting`
* **Response:** Total runs, balls faced, strike rate, average, boundary %, dot ball %, and granular Powerplay, Middle, and Death overs phase splits.

### 5.5. Career Bowling & Phase Breakdown
* **Route:** `GET /api/v1/analytics/players/{player_id}/bowling`
* **Response:** Overs, legal balls, runs conceded, wickets, economy rate, bowling average, bowling strike rate, and Death overs economy.

### 5.6. Chronological Recent Form Window
* **Route:** `GET /api/v1/analytics/players/{player_id}/recent-form?last_n=5&discipline=batting`
* **Response:** Scorecards across the last N match innings with match dates, venues, oppositions, and strike rates.

### 5.7. RR Proprietary Schema Discovery
* **Route:** `POST /api/v1/proprietary/discover-schema`
* **Payload:** `{"sample_rows": [...]}`
* **Response:** Discovered column names, inferred data types, and recommended mapping.

### 5.8. RR Proprietary Pack Ingestion
* **Route:** `POST /api/v1/proprietary/ingest-pack`
* **Payload:** `{"records": [...], "column_mapping": {...}, "dataset_key": "..."}`
* **Response:** Ingestion summary with conflict reports and missing-field audits.

### 5.9. Role-Masked Scouting Evaluations
* **Route:** `GET /api/v1/proprietary/evaluations/{player_id}`
* **Header:** `x-user-role: public | rr_scout_admin`
* **Security:** Strips confidential scout notes and anonymizes scout identifiers unless user has `rr_scout_admin` privileges.
