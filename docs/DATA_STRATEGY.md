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

### 5.3. Completeness Calculation
$$\text{Completeness Percentage} = \left( \frac{\text{Valid Checks}}{\text{Total Checks}} \right) \times 100$$
Any file with a critical error is flagged as `REJECTED`, preserving the raw evidence for operator inspection without polluting the analytical Parquet store.
