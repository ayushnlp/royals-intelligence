# ROYALS INTELLIGENCE — DATA STRATEGY & GOVERNANCE
**Classification:** Confidential / Rajasthan Royals Technical Operations  
**Document Version:** 1.0.0 (Stage 0 Baseline)  

---

## 1. Data Classification Model

Royals Intelligence enforces a strict **Dual-Domain Data Partitioning Model**:

| Classification Tier | Domain Description | Storage Location | Access Policy |
| :--- | :--- | :--- | :--- |
| **Tier 1: Public Domain Data** | Public ball-by-ball cricket data (e.g., Cricsheet, official IPL scorecards, international bilateral fixtures, domestic SMAT, Ranji, VHT). | `data/raw/public/`, `data/processed/public/` | Accessible to automated analytics, pipelines, and general model training. |
| **Tier 2: Tracking & Telemetry** | Hawk-Eye/radar ball-tracking data, release speed, trajectory curves, and stadium boundary spatial geometry. | `data/raw/telemetry/`, `data/processed/telemetry/` | Restricted access; anonymized during model benchmarking. |
| **Tier 3: Proprietary RR Intelligence** | Scout observation dossiers, psychological assessments, medical/fitness screening logs, and internal auction bid ceilings for IPL 2027. | `data/proprietary/` (Excluded from Git) | Strictly isolated; role-based access; zero exposure to public APIs. |

---

## 2. Directory Structure & Ingestion Lifecycle

```
data/
├── raw/                # Immutable source records
│   ├── public/         # Raw JSON/CSV match files
│   ├── telemetry/      # Release metrics and trajectory feeds
│   └── .gitkeep
├── processed/          # High-performance Parquet format
│   ├── ball_by_ball/   # Partitioned by season and match
│   ├── player_aggregates/
│   └── .gitkeep
├── external/           # Reference datasets
│   ├── venues/         # Ground coordinates and dimensions
│   ├── weather/        # Meteorological historical dew logs
│   └── .gitkeep
└── metadata/           # Data dictionary, schema definitions, player ID maps
    └── .gitkeep
```

---

## 3. Storage Formats & Data Processing Flow

1. **Raw Ingestion:** Ingestion scripts download or parse source JSON/CSV feeds directly into `data/raw/`. Files in raw are treated as immutable source logs.
2. **Transformation & Validation:** Using Pandas and Pydantic schema validators:
   - Match IDs and Player names are reconciled against `data/metadata/player_id_mapping.json`.
   - Data anomalies (e.g., impossible speeds, missing extra runs, duplicate deliveries) are quarantined into error logs.
3. **Optimized Storage:** Cleaned event data is exported to columnar Apache Parquet files in `data/processed/` and ingested asynchronously into PostgreSQL 16 for relational indexing.
4. **Fast Caching:** Frequently accessed player splits (e.g., Powerplay Strike Rate vs Left-arm pace) are cached in Redis 7 with a 12-hour TTL.

---

## 4. Quality Assurance & Explainability Guards

- **Sample Size Thresholds:** Any analytical metric derived from fewer than 30 deliveries or 5 innings is flagged with a `SAMPLE_WARNING` badge in the UI.
- **Data Lineage:** Every calculated KPI carries a deterministic pipeline hash tracing back to the raw source match records.
- **Audit Trails:** Proprietary scouting assessments are timestamped and tagged with scout IDs for accountability.
