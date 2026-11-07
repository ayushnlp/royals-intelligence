# ROYALS INTELLIGENCE — DATA SOURCE REGISTRY & EVALUATION
**Document Version:** 1.0.0 (Stage 1 Data Acquisition Engine)  
**Standard:** Legal Compliance, Source Transparency & Provenance  

---

## 1. Reliability Classification Tiers

To eliminate arbitrary scoring, Royals Intelligence classifies all cricket data sources into four deterministic **Reliability Tiers**:

| Tier | Classification Name | Definition & Legal Criteria | Permitted Ingestion Modality |
| :--- | :--- | :--- | :--- |
| **TIER 1** | **Authoritative Open Data (Explicit Open License)** | Verified schema stability with explicit open licenses (e.g., Open Data Commons ODbL, Creative Commons CC-BY 4.0). Completely unencumbered for automated analytics, bulk downloads, and programmatic ingestion. | Automated batch downloads, streaming parsers, public APIs. |
| **TIER 2** | **Official Governing Body / Franchise Public Web Feeds** | Official tournament and franchise portals (BCCI, IPLT20, Rajasthan Royals). Authoritative for official squads, tournament schedules, and results. Free public view; requires conservative rate-limiting and cache policies. | Cached read-only web clients, official public feeds. |
| **TIER 3** | **Curated Structured Datasets & Manual Import** | Internal franchise scouting dossiers, verified state-association scorecards, and trial evaluations with cryptographic SHA-256 provenance tracking. | Manual secure upload, vetted structured JSON/CSV imports. |
| **TIER 4** | **Restricted Commercial Platforms (ToS Prohibited / Gated)** | Commercial cricket media (ESPNcricinfo, Cricbuzz) with strict Terms of Service anti-scraping clauses or bot-detection barriers. **Direct scraping is strictly prohibited.** | Compliant manual-import export route only. |

---

## 2. Source-by-Source Evaluation

### 2.1. Cricsheet (`cricsheet_open`) — TIER 1
* **URL:** `https://cricsheet.org`
* **Categories:** Ball-by-ball deliveries, match info, player registries, toss decisions, venue, outcome.
* **Competitions & Seasons:** IPL (2008–2025/2026), SMAT, International T20s, Ranji Trophy (selected), BBL, PSL, CPL.
* **Licensing:** Open Data Commons Open Database License (ODbL). Commercial and analytical usage permitted with attribution.
* **Access Method:** Downloadable zip bundles of structured JSON match files.
* **Rate Limits:** No programmatic API restrictions; bulk archive download utilized to avoid per-file requests.
* **Reliability:** High. Standardized against official scorecards with ball-by-ball delivery validation.
* **Known Gaps:** Does not capture Hawkeye ball-tracking trajectories (release speed, release angle) or wagon wheel coordinates.

### 2.2. IPL Official Platform (`iplt20_official`) — TIER 2
* **URL:** `https://www.iplt20.com`
* **Categories:** Official IPL schedules, franchise squads, match scorecards, points table, auction player pools.
* **Competitions & Seasons:** Indian Premier League (2008–2026).
* **Licensing:** BCCI / IPL Proprietary. Public display permitted; commercial redistribution restricted.
* **Access Method:** Public web endpoints and official tournament schedules.
* **Rate Limits:** Max 30 requests/min; mandatory local caching (1-hour TTL for static, 10-second for live).
* **Reliability:** High. Authoritative for player auction registrations and official match designations.
* **Known Gaps:** No bulk historical database export provided.

### 2.3. Rajasthan Royals Official Portal (`rajasthan_royals_official`) — TIER 2
* **URL:** `https://www.rajasthanroyals.com`
* **Categories:** Verified franchise rosters, player biographies, jersey numbers, retention decisions, and SupeRR Selector campaign metadata.
* **Competitions & Seasons:** Rajasthan Royals IPL campaigns (2008–2026).
* **Licensing:** Royal Multisport Private Limited Proprietary.
* **Access Method:** Public web feed & official announcements.
* **Rate Limits:** Conservative polling (1 request/hour).
* **Reliability:** Authoritative for RR franchise operational facts and official player announcements.

### 2.4. BCCI Domestic Cricket Operations (`bcci_domestic`) — TIER 2
* **URL:** `https://www.bcci.tv`
* **Categories:** Syed Mushtaq Ali Trophy (SMAT), Ranji Trophy, Vijay Hazare Trophy (VHT), Duleep Trophy, CK Nayudu Trophy.
* **Competitions & Seasons:** Indian domestic cricket (2018–2026).
* **Licensing:** BCCI Domestic Regulations.
* **Access Method:** Public tournament portals and match centers.
* **Rate Limits:** Max 20 requests/min.
* **Reliability:** Authoritative for Indian domestic uncapped player scouting identification.
* **Known Gaps:** Ball-by-ball depth is occasionally incomplete for early-round non-broadcast matches.

### 2.5. Open-Meteo Historical & Forecast API (`open_meteo_historical`) — TIER 1
* **URL:** `https://open-meteo.com`
* **Categories:** Hourly temperature, relative humidity, dew point, wind speed/direction, surface air pressure, precipitation.
* **Coverage:** Exact GPS coordinates for all IPL venues (Sawai Mansingh Stadium, Barsapara, Wankhede, Chepauk, Eden Gardens, etc.).
* **Licensing:** Creative Commons Attribution 4.0 International (CC-BY 4.0). Open data.
* **Access Method:** REST JSON API (`https://archive-api.open-meteo.com/v1/archive`).
* **Rate Limits:** 10,000 requests/day free tier without authentication.
* **Reliability:** High (based on ECMWF ERA5 reanalysis and high-resolution meteorological models).

### 2.6. ESPNcricinfo (`espncricinfo_reference`) — TIER 4
* **URL:** `https://www.espncricinfo.com`
* **Categories:** Player career records, match articles, historical scorecards.
* **Licensing:** ESPN Sports Media Ltd. Strictly all rights reserved.
* **Access Policy:** Web scraping is prohibited by Terms of Service. Anti-bot Cloudflare gates in place.
* **Ingestion Modality:** **Manual export / user-supplied CSV/JSON only.** The system will never run automated scraping against ESPNcricinfo.

### 2.7. Rajasthan Royals Curated Scouting Dossiers (`curated_rr_scouting`) — TIER 3
* **Reference:** `internal://data/raw/domestic/rr_scouting_manifest.json`
* **Categories:** Scout notes, mechanical observations, trial reports, domestic uncapped target lists for IPL 2027.
* **Licensing:** Strictly Confidential & Proprietary (Rajasthan Royals Internal Only).
* **Access Method:** Encrypted local JSON / manual secure upload interface with SHA-256 verification.
* **Reliability:** High. Primary observations direct from RR talent scouting network.

