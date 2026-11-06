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
