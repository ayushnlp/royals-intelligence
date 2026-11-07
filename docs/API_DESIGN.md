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
* **Query Parameters:** `eligibility`, `tier`, `role`, `state`, `trialist_only`, `reference_date` (optional confirmed competition cutoff date)
* **Response:** Array of `UncappedPlayerSummary` objects with dynamically calculated age (or `null`/unresolved if reference date is unconfirmed), verification badges, and primary discipline.

### 5.2. Granular Player Profile & Provenance
* **Route:** `GET /api/v1/players/{player_id}`
* **Query Parameters:** `reference_date` (optional)
* **Response:** Detailed `UncappedPlayerDetail` including all multi-source external IDs, DOB source, eligibility rule source/version, and verification history notes.

### 5.3. Audit & Update Eligibility
* **Route:** `POST /api/v1/players/{player_id}/verify-eligibility`
* **Security:** Authenticated Principal (`Authorization: Bearer <token>` or `X-API-Key: <key>`), role: `rr_scout_admin`.
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
* **Security:** Strips confidential scout notes and anonymizes scout identifiers unless user provides verified server-side Bearer token / API key with `rr_scout_admin` privileges.

---

## 6. Implemented Stage 3 Endpoints (Domestic Season & Match Intelligence)

All Stage 3 endpoints are mounted under `/api/v1/domestic` and enforce the strict platform scope: **UNCAPPED PLAYERS ONLY**.

### 6.1. Domestic Competitions Directory
* **Route:** `GET /api/v1/domestic/competitions`
* **Purpose:** Directory of verified domestic competitions (SMAT, Vijay Hazare, Ranji, DPL, UP T20).
* **Response:** Array of `CompetitionSeasonSummary` with match counts, participating teams, ball-by-ball availability flags, and data completeness metrics.

### 6.2. Season Matches Explorer
* **Route:** `GET /api/v1/domestic/seasons/{competition_id}/{season}/matches`
* **Query Parameters:** `team` (optional filter), `page` (default 1), `page_size` (default 20)
* **Response:** Paginated list of `MatchSummaryItem` objects with match date, home/away teams, venue, outcome, and ball-by-ball verification flags.

### 6.3. Season Standings & Performance Summary
* **Route:** `GET /api/v1/domestic/seasons/{competition_id}/{season}/summary`
* **Response:** Aggregate season metrics including total matches, active teams, ball-by-ball pass rates, and provenance metadata.

### 6.4. Complete Match Scorecard & Context
* **Route:** `GET /api/v1/domestic/matches/{match_id}`
* **Purpose:** Comprehensive match intelligence dossier.
* **Response:** Complete `MatchScorecardResponse` including match metadata (venue, toss, player of match, winner) and detailed analysis for all innings.

### 6.5. Deep Innings Diagnostics
* **Route:** `GET /api/v1/domestic/matches/{match_id}/innings/{innings_number}`
* **Purpose:** Granular ball-by-ball analytics for a specific innings.
* **Response:** `InningsAnalysisResponse` containing:
  - Batting scorecards (with runs, balls, 4s, 6s, SR, and phase-split contributions).
  - Bowling scorecards (with overs, maidens, runs, bowler wickets excluding run-outs, economy, dot balls).
  - Fall of Wickets (FoW) progression.
  - Wicket partnerships with individual batter contributions and unbroken flags.
  - Format-aware phase leverage summaries (Powerplay, Middle, Death).
  - Over-by-over scoring progression (cumulative runs and wickets).

### 6.6. Uncapped Player Domestic Season Aggregates
* **Route:** `GET /api/v1/domestic/players/{player_id}/season-stats`
* **Query Parameters:** `competition_id` (optional filter)
* **Security/Scope:** Strictly guards against capped international players (`403 Forbidden`).
* **Response:** Array of `PlayerDomesticSeasonStats` with batting metrics (average, strike rate, boundaries, high score) and bowling metrics (average, economy, bowler wickets).

### 6.7. Player Chronological Domestic Match History
* **Route:** `GET /api/v1/domestic/players/{player_id}/match-history`
* **Query Parameters:** `competition_id`, `season`, `page`, `page_size`
* **Response:** Paginated list of `PlayerMatchHistoryItem` records showing individual match performances in chronological order.

### 6.8. Granular Player Phase Splits
* **Route:** `GET /api/v1/domestic/players/{player_id}/phase-splits`
* **Query Parameters:** `competition_id` (optional)
* **Response:** Detailed `PlayerPhaseSplitDetail` array with format-aware phase cuts (Powerplay, Middle, Death) for both batting and bowling disciplines.

### 6.9. All-Round Dual-Contribution Profile
* **Route:** `GET /api/v1/domestic/players/{player_id}/all-round-summary`
* **Integrity Rule:** Strictly avoids arbitrary composite formulas or synthetic ratings. Preserves independent batting, bowling, and fielding profiles with transparent sample sizes.
* **Response:** `AllRoundContributionResponse` featuring evidence-based qualitative role archetype classification and sample sizes (matches, innings batted, overs bowled).

---

## 7. Implemented Stage 4 Endpoints (Venue, Pitch & Weather Intelligence)

Endpoints are mounted under `/api/v1/venues` and `/api/v1/weather`.

### 7.1. Venue Directory & Overview
* **Route:** `GET /api/v1/venues`
* **Query Parameters:** `rr_only: bool = false`
* **Response:** List of `VenueSummaryItem` objects with city, state, coordinates, altitude, soil type, and match count.

### 7.2. Venue Detail & Boundary Geometry
* **Route:** `GET /api/v1/venues/{venue_id}`
* **Response:** `VenueDetailResponse` containing measured straight, off, and leg boundary lengths (in meters) with source attribution, soil details, floodlights certification, and capacity.

### 7.3. Venue Historical Scoring Trends
* **Route:** `GET /api/v1/venues/{venue_id}/scoring-trends`
* **Response:** `VenueScoringTrendsResponse` featuring 1st/2nd innings averages, highest/lowest scores, toss win & match win rates, average wickets, phase run rates, and sample size confidence score.

### 7.4. Evidence-Backed Pitch Diagnostics
* **Route:** `GET /api/v1/venues/{venue_id}/pitch-analysis`
* **Integrity Rule:** Strictly separates observed statistical patterns from subjective reports. Disclaims deterministic predictions.
* **Response:** `PitchEvidenceAnalysisResponse` with pace vs spin wicket shares, economy comparison, boundary runs %, dot ball %, empirical conditions classification, and limitations caveat.

### 7.5. Uncapped Prospect Venue Performance
* **Route:** `GET /api/v1/venues/{venue_id}/player-performance?player_id={player_id}`
* **Security/Scope:** Strictly restricted to uncapped domestic players (`403 Forbidden` if capped player requested).
* **Response:** `UncappedPlayerVenuePerformanceResponse` containing batting & bowling records at the venue with sample size warnings.

### 7.6. Match Weather & Environmental Context
* **Route:** `GET /api/v1/weather/match/{match_id}`
* **Response:** `MatchWeatherContextResponse` with in-match hourly observations, temperature/humidity swings, dew severity risk assessment, and scoring variance against venue historical par.

### 7.7. Historical Weather Telemetry
* **Route:** `GET /api/v1/weather/historical?venue_code={code}&match_date={date}`
* **Response:** Array of `WeatherObservationItem` from Open-Meteo CC-BY 4.0 (`is_forecast: false`).

### 7.8. Meteorological Fixture Forecast
* **Route:** `GET /api/v1/weather/forecast?venue_code={code}&days_ahead={days}`
* **Response:** Array of `WeatherObservationItem` tagged with `is_forecast: true` and `reliability: "FORECAST_PROJECTION"`.

### 7.9. Weather Source Status & Attribution
* **Route:** `GET /api/v1/weather/source-status`
* **Response:** `WeatherSourceStatusResponse` auditing Open-Meteo CC-BY 4.0 status, legal licensing, and rate limits.
