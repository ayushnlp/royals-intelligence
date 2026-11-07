# ROYALS INTELLIGENCE — DATA STRATEGY & ACQUISITION GOVERNANCE
**Classification:** Confidential / Rajasthan Royals Technical Operations  
**Document Version:** 1.1.0 (Stage 1 Data Acquisition Engine)  

---

## 1. Reliability Classification Tiers

Royals Intelligence enforces a four-tier reliability model for all cricket datasets to eliminate arbitrary scoring:

| Tier | Classification Name | Definition & Legal Criteria | Permitted Ingestion Modality |
| :--- | :--- | :--- | :--- |
| **TIER 1** | **Authoritative Open Data (Explicit Open License)** | Verified schema stability with explicit open licenses (Open Data Commons ODbL, CC-BY 4.0). Completely unencumbered for automated analytics, bulk downloads, and programmatic ingestion (e.g. Cricsheet, Open-Meteo). | Automated batch downloads, streaming parsers, public APIs. |
| **TIER 2** | **Official Governing Body / Franchise Public Web Feeds** | Official tournament and franchise portals (BCCI, IPLT20, Rajasthan Royals). Authoritative for official squads, tournament schedules, and results. Free public view; requires conservative rate-limiting and cache policies. | Cached read-only web clients, official public feeds. |
| **TIER 3** | **Curated Structured Datasets & Manual Import** | Internal franchise scouting dossiers, verified state-association scorecards, and trial evaluations with cryptographic SHA-256 provenance tracking. | Manual secure upload, vetted structured JSON/CSV imports. |
| **TIER 4** | **Restricted Commercial Platforms (ToS Prohibited / Gated)** | Commercial cricket media (ESPNcricinfo, Cricbuzz) with strict Terms of Service anti-scraping clauses or bot-detection barriers. **Direct scraping is strictly prohibited.** | Compliant manual-import export route only. |

---

## 2. Evaluated Sources Matrix

| Source ID | Provider / Platform | Tier | Coverage Scope | Permitted Method | Rate Limit Policy |
| :--- | :--- | :---: | :--- | :--- | :--- |
| `cricsheet_open` | Cricsheet | TIER 1 | IPL (2008–2026), SMAT, International T20s | Batch download / JSON archive | No programmatic restriction |
| `iplt20_official` | IPL Official Portal | TIER 2 | Official IPL 2026 squads, fixtures, results | Read-only public web endpoints | Max 30 req/min; cached |
| `rajasthan_royals_official`| Rajasthan Royals Official | TIER 2 | RR official roster, retentions, SupeRR Selector | Public web feeds / announcements | Conservative polling (1/hour) |
| `bcci_domestic` | BCCI Domestic Operations | TIER 2 | SMAT, Ranji Trophy, Vijay Hazare, U23 | Public tournament portal | Max 20 req/min |
| `open_meteo_historical` | Open-Meteo Weather API | TIER 1 | Venue hourly temp, humidity, dew point, wind | REST JSON API | 10,000 req/day (free tier) |
| `espncricinfo_reference`| ESPNcricinfo | TIER 4 | Player career bios, international history | **Scraping prohibited**; Manual CSV/JSON import | Anti-bot / Cloudflare blocked |
| `curated_rr_scouting` | RR Talent Scouting Network | TIER 3 | Domestic uncapped trial notes, IPL 2027 watchlist| Secure upload / SHA-256 verified | Internal filesystem only |

---

## 3. Raw Data Storage & Partitioning Layout

```
data/
├── raw/                      # Immutable raw source artifacts (excluded from Git)
│   ├── ipl/                  # Official IPL schedule & squad snapshots
│   ├── matches/              # Cricsheet raw JSON match files partitioned by competition/season
│   ├── players/              # Player biographical and career raw feeds
│   ├── scorecards/           # Historical official match scorecards
│   ├── ball_by_ball/         # Raw delivery streams
│   ├── domestic/             # SMAT, Ranji Trophy, and VHT domestic feeds
│   ├── venues/               # Venue specifications and GPS coordinates
│   ├── weather/              # Meteorological hourly dew point and wind logs
│   └── fixtures/             # Verified test fixtures (synthetic data strictly labeled)
├── metadata/                 # Provenance, schemas, and catalogs (version-controlled)
│   ├── sources/              # source_registry.json
│   ├── runs/                 # Ingestion run audit logs (run_*.json)
│   ├── manifests/            # Dataset manifests with SHA-256 hashes
│   ├── coverage/             # Tournament coverage report (coverage_report.json)
│   └── validation/           # Quality logs and rejected records
└── processed/                # Columnar Apache Parquet partition store (excluded from Git)
    ├── ball_by_ball/         # season={season}/deliveries.parquet
    ├── matches/              # matches.parquet
    └── player_aggregates/    # Fast player splits (Stage 3+)
```

---

## 4. Provenance & Cryptographic Lineage Policy

1. **SHA-256 Checksums:** Every acquired raw artifact is hashed at ingestion. The checksum is written to the dataset manifest.
2. **Idempotent Ingestion:** If an incoming file has a matching SHA-256 checksum, redundant storage is skipped and recorded as an `idempotent_skip`.
3. **Immutability:** Existing raw files are never silently overwritten. Collisions generate timestamped snapshots (`{stem}_{timestamp}_{suffix}`).
4. **Anti-Fabrication Guarantee:** Delivery-level classifications (such as yorkers, bouncers, slower balls, cutters) are **strictly recorded as `None`** unless explicit sensor/telemetry source records exist. Statistical indicators are never invented.

---

## 5. Cricket Data Validation & Quality Metrics

Every match artifact undergoes a three-layer validation check before being accepted into the processed store:

### 5.1. Structural Validation
- JSON/CSV syntax compliance.
- Required top-level sections: `info`, `innings`.
- Schema compatibility against `CricketDataContracts`.

### 5.2. Cricket-Specific Rules
- Over sequence monotonicity (over index must strictly increase).
- Run balance arithmetic:
  $$\text{runs.batter} + \text{runs.extras} = \text{runs.total}$$
- Extras balance:
  $$\text{wides} + \text{noballs} + \text{legbyes} + \text{byes} + \text{penalty} = \text{runs.extras}$$
- Dismissal logic: `player_out` must be verified; caught dismissals require a credited fielder.
- Duplicate delivery prevention: unique key on `(match_id, innings_number, over_number, ball_in_over)`.

### 5.3. Validation Pass Rate vs. Data Completeness Metrics
In Royals Intelligence telemetry, validation check success is rigorously distinguished from data attribute completeness:

1. **Validation Pass Rate (%):**
   $$\text{Validation Pass Rate} = \left( \frac{\text{Valid Checks}}{\text{Total Checks}} \right) \times 100$$
   Measures structural and logical rule conformity. Any file with a critical error is flagged as `REJECTED`, preserving raw evidence without polluting analytical stores.

2. **Dataset Field Completeness (%):**
   $$\text{Completeness Percentage} = \left( \frac{\text{Present Required Attributes}}{\text{Total Expected Attributes}} \right) \times 100$$
   Measures demographic and match-level coverage (e.g., presence of verified DOB, tracking of batting hands, bowling styles, and venue coordinates). Missing attributes trigger `data_quality_records` diagnostic entries.


---

## 6. Uncapped Player Identity, Eligibility & RR 8 Nov Data Pack

### 6.1. Player Identity Deduplication & Alias Resolution
1. **Canonical Player ID:** Immutable internal UUID assigned to each distinct physical player.
2. **Multi-Source Identity Mapping:** `player_identities` table maps external provider IDs (Cricsheet, BCCI, ESPNcricinfo, RR Scouting).
3. **Name Normalization:** Dot-stripped title casing (e.g., `R. Parag` -> `R Parag`, `A.B. de Villiers` -> `Ab De Villiers`).
4. **DOB Provenance:** Every date of birth carries its verified source and timestamp. **Dates of birth are never invented.** Missing DOBs trigger `PENDING_VERIFICATION` and age is set to `None`.
5. **Age Calculation & Cutoff Integrity:** Evaluated dynamically against an explicitly verified competition cutoff date:
   $$\text{Age (yrs)} = \frac{\text{Confirmed Reference Date} - \text{DOB}}{365.25}$$
   *Rule Policy:* No reference date is silently assumed. If the tournament's official age-reference date is unconfirmed by tournament organizers, age is marked as `None` ("Age Unresolved"). Missing DOB never produces a fabricated age.

### 6.2. Formal Eligibility Verification States & Cap Decoupling
Lifetime international cap history (`is_capped`, `last_international_match_date`) is strictly decoupled from competition-specific uncapped eligibility:
- `CONFIRMED_UNCAPPED`: Verified uncapped under competition rules. Includes domestic players with 0 senior international caps, or players eligible under competition exemptions such as the **IPL 5-Year Retired Player Clause (Rule 4.3)** (players inactive in international cricket for 5+ calendar years).
- `INELIGIBLE_CAPPED`: Active senior international player ineligible under competition rules.
- `INELIGIBLE_OVERAGE`: Exceeds tournament-specific age ceilings.
- `PENDING_VERIFICATION`: Demographic or debut evidence incomplete (e.g. missing DOB, unverified DOB provenance, or unconfirmed tournament reference dates).
- `FLAGGED_CONFLICT`: Discrepancies between sources (differing birth dates, batting styles, or cap status).

### 6.3. Rajasthan Royals 8 November Proprietary Data Pack Readiness
1. **Dynamic Schema Discovery:** Analyzes incoming files without preconceptions, infers column types, and recommends an optimal column mapping.
2. **Field-Level Validation & Type Casting:** Standardizes arbitrary column names to canonical player models.
3. **Conflict & Missing-Field Reporting:** Records discrepancies in `data_quality_records` without overwriting prior evidence.
4. **Data Classification & Access Boundaries:**
   - `PUBLIC`: Standard scorecard and aggregated stats.
   - `INTERNAL_SCOUTING`: Roster tiers and player archetype profiles.
   - `RR_PROPRIETARY_CONFIDENTIAL`: Scout ratings, qualitative notes, and auction strategic ceilings. Automatically masked for non-admin roles.

---

## 7. Venue, Pitch & Meteorological Data Governance (Stage 4)

### 7.1. Ground Measurement Sourcing & Anti-Fabrication Guarantee
1. **Measured Boundaries Only:** Boundary lengths (straight, off, leg in meters) are recorded exclusively from official BCCI stadium measurement surveys or verified engineering architectural plans.
2. **Explicit Missingness:** Where physical boundary dimensions or soil classifications are unknown or unverified, they are represented explicitly as `None` (`null`) with status `UNAVAILABLE`.
3. **Coordinates Provenance:** Venue GPS coordinates are derived from official stadium geocoding and Survey of India registries, attributed to `Open-Meteo Geocoding / Survey of India`.

### 7.2. Pitch Evidence vs Deterministic Prediction Rule
1. **Observational vs Reported Distinction:** Observed statistical distributions (e.g. pace vs spin wicket shares, boundary percentages) are strictly distinguished from qualitative pitch reports.
2. **Sample Size & Confidence Transparency:** Every pitch evaluation carries its sample size ($N$ matches), date range, and confidence classification (`HIGH` for $N \ge 10$, `MODERATE` for $5 \le N \le 9$, `LOW_SAMPLE` for $N < 5$ with advisory caveats).
3. **Anti-Deterministic Clause:** The platform enforces an explicit disclaimer: historical statistical tendencies reflect past conditions across evaluated samples and must never be interpreted as deterministic forecasts of pitch behaviour.

### 7.3. Open-Meteo CC-BY 4.0 Meteorological Governance
1. **Licensing Compliance:** Meteorological data is acquired under the Creative Commons Attribution 4.0 International (CC-BY 4.0) open license. Mandatory attribution text (`Weather data by Open-Meteo.com under CC-BY 4.0`) is embedded in all API responses and UI components.
2. **Rate Limit & Caching Architecture:** Free-tier access (up to 10,000 requests/day) is protected by persistent local caching. Redundant external calls for historical matches are strictly avoided.

### 7.4. Strict Segregation of Observations and Forecasts
1. **Historical Immutability:** Historical match observations are marked with `is_forecast: false` and `reliability: "HIGH"`.
2. **Forecast Projections:** Future match forecasts are marked with `is_forecast: true` and `reliability: "FORECAST_PROJECTION"`.
3. **No Overwrite Policy:** A forecast projection must never overwrite or masquerade as a verified historical weather observation.
