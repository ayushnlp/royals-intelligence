# ROYALS INTELLIGENCE — SECURITY & DATA PROTECTION POLICY
**Classification:** Confidential / Rajasthan Royals Technical Security Standard  
**Document Version:** 1.2.0 (Stage 4 Baseline)  

---

## 1. Core Principles

1. **Confidentiality of Competitive Intelligence:** Strategic scout notes, psychological ratings, and auction bid limits represent core sporting IP. A breach gives opposing franchises an asymmetric advantage.
2. **Zero Hardcoded Secrets:** Credentials, private keys, API secrets, and connection URIs must never exist in plaintext within the repository.
3. **Partitioned Data Domains:** Strict isolation between open-source cricket records and Rajasthan Royals proprietary intelligence.
4. **Data Provenance & Scientific Integrity:** Observational weather and boundary surveys must never be synthesized or fabricated; unknowns are represented as `None` / `UNAVAILABLE`.

---

## 2. Secrets Management & Git Policy

- **Ignored Artifacts:** The `.gitignore` at the repository root strictly excludes:
  - All `.env`, `.env.local`, `.env.*` configuration files.
  - SSH/TLS certificates (`*.pem`, `*.key`).
  - Cache databases and temporary test runs.
- **Environment Templates:** All required configuration variables must be documented in `.env.example` templates with non-functional dummy defaults.
- **Pre-Commit Auditing:** Before any commit or push, staged files must be inspected for accidental secret exposure.

---

## 3. Data Protection & Storage Boundaries

### 3.1. Public vs. Proprietary Data Boundary
```
[PUBLIC / UNRESTRICTED]
- Historical match scorecards
- Public ball-by-ball delivery feeds (Cricsheet)
- Player career basic aggregates
- Tournament schedules & venue locations
- Weather telemetry (Open-Meteo CC-BY 4.0)
- Official venue boundary survey specifications
      |
      | (Physical Directory & Access Barrier)
      v
[PROPRIETARY / RESTRICTED (Rajasthan Royals Internal Only)]
- Scout qualitative evaluation logs
- Medical and biomechanical screening dossiers
- Replacement simulator WAR calculations
- IPL 2027 Auction purse allocation models and max bid ceilings
- Tactical opposition weakness dossiers
```

### 3.2. Proprietary Data Handling Rules
1. Proprietary files reside exclusively in `data/proprietary/` which is ignored by Git.
2. Stored records must be encrypted at rest in production environments (AES-256).
3. Database backups containing proprietary tables must be encrypted using franchise-managed KMS keys.

---

## 4. API & Network Security

- **CORS Protection:** Backend API strictly allows configured origins (e.g., `http://localhost:3000` in local dev). Wildcard `*` origins are prohibited.
- **Health Probes:** `/health` and `/api/v1/health` endpoints expose only operational status, latency, and component health. Database connection strings, passwords, and host IP addresses are never leaked in response payloads.
- **Error Sanitization:** Centralized exception handlers catch database and server exceptions and return sanitized RFC-7807 problem details without internal stack traces in non-debug mode.

---

## 5. Stage 2 & 3 Access Boundary Enforcement

### 5.1. Dataset Classification Levels
1. **`PUBLIC`**: Standard scorecards and aggregated metrics. Freely exposed to all API callers.
2. **`INTERNAL_SCOUTING`**: Roster priority tiers, player archetypes, and calculated age metrics. Visible within platform interface.
3. **`RR_PROPRIETARY_CONFIDENTIAL`**: Qualitative scout evaluations, confidential notes, strategic bid ceilings, and trialist evaluations.

### 5.2. Automated Access Masking & Server-Side Authorization Engine
The system enforces automatic role-based data masking via `RRDataPackService.mask_confidential_data()` backed by trusted server-side authentication:
- **Server-Side Authentication Dependency:** Requests must supply valid Bearer tokens or API keys (`Authorization: Bearer <token>` or `X-API-Key: <key>`).
- **Rejection of Client-Asserted Roles:** Client-controlled headers such as `x-user-role` are untrusted and rejected with `401 Unauthorized` if supplied without matching server-verified credentials.
- **Deny-by-Default:** Anonymous and standard callers receive masked evaluation payloads:
  - `confidential_notes`: `"[RESTRICTED - RAJASTHAN ROYALS PROPRIETARY]"`
  - `proprietary_notes`: `"[RESTRICTED - RAJASTHAN ROYALS PROPRIETARY]"`
  - `scout_identifier`: `"[ANONYMIZED_RR_SCOUT]"`
  - `scouting_tier`: `"INTERNAL"`
- **Privileged Unmasked Access:** Full evaluation fidelity is unlocked exclusively for authenticated principals verified with the `rr_scout_admin` role. Privileged actions (such as data pack ingestion and schema discovery) require explicit scout admin credentials.

---

## 6. Stage 4 Venue & Weather Intelligence Security & Policy Controls

### 6.1. Open-Meteo CC-BY 4.0 Compliance & Rate Limiting
- **Licensing Requirement:** Attribution to Open-Meteo is strictly required under the Creative Commons Attribution 4.0 International license (CC-BY 4.0).
- **Public Attribution:** The platform UI and API (`/api/v1/weather/source-status`) explicitly advertise Open-Meteo attribution: `"Weather data by Open-Meteo.com under CC-BY 4.0"`.
- **Keyless Rate Guardrails:** Open-Meteo keyless access is limited to 10,000 calls/day and 600 calls/minute. The backend enforces in-memory and Redis-backed response caching (TTL: 1 hour for forecasts, permanent for historical match windows) and graceful fallback to offline climate normals (`reliability: "ESTIMATED"`) to avoid rate exhaustion.

### 6.2. Strict Uncapped Scope Enforcement on Venue Endpoints
- In compliance with the overarching project scope (**UNCAPPED PLAYERS ONLY**), the venue prospect performance endpoint (`GET /api/v1/venues/{venue_id}/player-performance`) strictly restricts queries to domestic uncapped prospects.
- Requests targeting senior international capped players (e.g., `virat_kohli`, `rohit_sharma`, `pat_cummins`) raise a `PermissionError` resulting in an immediate `403 Forbidden` response.

### 6.3. Weather Observation vs. Forecast Data Segregation
- Forecast data must never overwrite, contaminate, or be presented as observed ground truth.
- All forecast telemetry payloads explicitly set `is_forecast: true` and `reliability: "FORECAST_PROJECTION"`.
- Verified match weather conditions set `is_forecast: false` and `reliability: "VERIFIED_OBSERVATION"`.

### 6.4. Anti-Fabrication Boundary Survey Governance
- Venue boundary dimensions and geospatial coordinates are sourced exclusively from verified stadium blueprints and BCCI survey specifications.
- Where survey data is unavailable, values are strictly recorded as `None` with `dimensions_source: "NOT_SURVEYED"`. Fabricated or inferred boundary lengths are strictly prohibited by automated schema assertions.
