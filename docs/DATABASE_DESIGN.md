# ROYALS INTELLIGENCE — DATABASE ARCHITECTURE & DESIGN
**Document Version:** 3.0.0 (Stage 4 Implemented & Verified)  
**Database Engine:** PostgreSQL 16 (Production) / SQLite Async (In-Memory Testing Harness)  
**ORM / Data Layer:** SQLAlchemy 2.0 (Async) + AsyncPG / aiosqlite  
**Schema Migration Engine:** Alembic (Revisions: `001_uncapped_player_foundation`, `002_venue_pitch_weather`)  
**Target Scope:** UNCAPPED PLAYERS ONLY  

---

## 1. Overview & Architecture

The database architecture for ROYALS INTELLIGENCE provides an enterprise foundation for high-volume cricket delivery streams, multi-source player identity deduplication, data provenance tracking, stadium geometry, pitch diagnostics, Open-Meteo CC-BY 4.0 meteorological telemetry, and confidential Rajasthan Royals uncapped scouting evaluations.

All 31 relational models are defined using modern SQLAlchemy 2.0 type-annotated Declarative syntax (`Mapped[...]`, `mapped_column(...)`), with strict foreign keys, cascade rules, composite indexes, and check constraints.

```
       +------------------+             +------------------+
       |   COMPETITIONS   |             |      VENUES      |<----+
       +--------+---------+             +--------+---------+     |
                | 1                              | 1             |
                |                                |               |
                | M                              | M             |
       +--------v---------+             +--------v---------+     |
       |     SEASONS      |             |     MATCHES      |<----+
       +--------+---------+             +---+----+----+----+     |
                | 1                         |    |    |          |
                | M                         |    |    |          |
                +---------------------------+    |    |          |
                                                 |    |          |
       +------------------+             +--------v----+----+     |
       |      TEAMS       |             |     INNINGS      |     |
       +--------+---------+             +--------+---------+     |
                | 1                              | 1             |
                | M                              | M             |
                |                       +--------v---------+     |
                |                       |    DELIVERIES    |     |
                |                       |  (Ball-by-Ball)  |     |
                |                       +--------+---------+     |
                |                                |               |
                +--------------------+-----------+               |
                                     |                           |
                            +--------v---------+                 |
                            |     PLAYERS      |                 |
                            +---+----+----+----+                 |
                                |    |    |                      |
             +------------------+    |    +----------------------+
             | 1                     | 1                         | 1
             | M                     | 1                         | M
    +--------v---------+    +--------v------------------+  +-----v------------------------+
    | PLAYER_IDENTITY  |    |  UNCAPPED_PLAYER_PROFILE  |  | MATCH_WEATHER_OBSERVATIONS   |
    | (Multi-Source IDs|    | (Eligibility Verification |  | (Open-Meteo CC-BY 4.0        |
    |  & Name Aliases) |    |  Age Cutoff & RR Tier)    |  |  Hourly Telemetry & Dew Risk)|
    +------------------+    +--------+------------------+  +------------------------------+
                                     | 1                         | 1
                                     | M                         | M
                            +--------v------------------+  +-----v------------------------+
                            |   SCOUTING_EVALUATIONS    |  |   VENUE_PITCH_REPORTS        |
                            | (Confidential RR Insights |  | (Soil classification, turn,  |
                            |  Access Boundary Masked)  |  |  pace & bounce observations) |
                            +---------------------------+  +------------------------------+
```

---

## 2. Implemented Schema Inventory (29 Tables)

### 2.1. Core Competition & Demographics (10 Tables)
1. **`competitions`**: Multi-tournament registry (`IPL`, `SMAT`, `VHT`, `Ranji`).
2. **`seasons`**: Tournament seasons linked to competitions with composite uniqueness `(competition_id, season_id)`.
3. **`teams`**: State domestic teams and franchises with `is_rr`, `is_domestic`, and state association mapping.
4. **`venues`**: Cricket grounds with pitch soil types, boundary dimensions (straight/off/leg in meters), and coordinates.
5. **`players`**: Canonical demographic registry (`canonical_id`, `full_name`, `dob`, `dob_source`, `dob_verified`, `is_capped`).
6. **`player_identities`**: Multi-source external IDs (Cricsheet, BCCI, ESPNcricinfo, RR Data Pack) and name spelling variations with confidence scores and conflict notes. Unique constraint: `(source_name, external_player_id)`.
7. **`player_roles`**: Tactical archetype categorization (e.g. `Top Order Batter`, `Express Pace`, `Finisher`).
8. **`matches`**: Fixtures with toss decision, winner, win margins, super over flags, and composite date/venue indexes.
9. **`innings`**: Match innings aggregate records with batting/bowling team foreign keys.
10. **`player_participations`**: Match-level participation tracking (Playing XI, Impact Player In/Out, Captain, Wicketkeeper).

### 2.2. Performance Entities (6 Tables)
11. **`batting_scorecards`**: Batting performance per match with strike rate, dot balls, and phase splits (Powerplay, Middle, Death). Composite unique constraint: `(match_id, innings_number, player_id)`.
12. **`bowling_scorecards`**: Bowling spells with legal balls, overs, economy rate, maidens, wickets, dot balls, and phase splits.
13. **`ball_by_ball_deliveries`**: High-frequency delivery event stream.
    - Check Constraint: `CHECK (total_runs = batter_runs + extra_runs)`.
    - Composite Matchup Index: `ix_delivery_matchup (bowler_id, striker_id)`.
    - Composite Sequence Index: `ix_delivery_over_sequence (match_id, innings_id, over_number, ball_in_over)`.
    - Sensor Telemetry: Radar speeds and delivery classifications strictly optional (`None` unless sensor verified).
14. **`fielding_contributions`**: Catches, direct-hit run-outs, assisted run-outs, stumpings, and runs saved.
15. **`partnerships`**: Batting partnerships with wicket sequence, run splits, and unbroken status.
16. **`player_match_performances`**: Composite match-level all-round performance summary.

### 2.3. Data Governance & Provenance (7 Tables)
17. **`data_sources`**: Registered providers with tier classification (`TIER_1` to `TIER_4`), licenses, and rate limits.
18. **`datasets`**: Registered analytical datasets categorized by security classification (`PUBLIC`, `INTERNAL_SCOUTING`, `RR_PROPRIETARY_CONFIDENTIAL`).
19. **`ingestion_runs`**: Ingestion execution telemetry (start time, duration, record counts, idempotent skips, completeness %).
20. **`dataset_manifests`**: SHA-256 cryptographic provenance manifests and raw artifact inventory.
21. **`validation_results`**: Granular validation check audit log entries with severity (`CRITICAL`, `WARNING`).
22. **`source_references`**: Row-level lineage linking any entity row back to its exact raw source artifact and file SHA-256.
23. **`data_quality_records`**: Completeness scores, conflict descriptions, and missing field tracking per player and match.

### 2.4. Uncapped Scouting & Proprietary Evaluation (6 Tables)
24. **`uncapped_player_profiles`**: Core uncapped profile enforcing the 5 verification states:
    - `CONFIRMED_UNCAPPED`: Zero senior international caps verified.
    - `SUSPECTED_CAPPED`: International representation detected.
    - `INELIGIBLE_OVERAGE`: Exceeds tournament age limit.
    - `PENDING_VERIFICATION`: Missing date of birth or debut history.
    - `FLAGGED_CONFLICT`: Discrepancies between sources.
    - Age at cutoff calculated dynamically using verified competition reference date (or None / unresolved when unconfirmed). International cap facts decoupled from competition-specific uncapped eligibility (e.g. IPL 5-year inactive international clause).
25. **`player_performance_snapshots`**: Domestic T20 season aggregates (SMAT, CK Nayudu) with phase strike rates and death economy.
26. **`player_role_assessments`**: Readiness ratings (Powerplay, Middle, Death, Pace vs Spin comfort) on 1.0–10.0 scale.
27. **`scouting_evaluations`**: Rajasthan Royals proprietary scout evaluations. Data classification: `RR_PROPRIETARY_CONFIDENTIAL`. Protected by automated security masking.
28. **`scouting_evidence`**: Empirical benchmarks, video clips, and trial session telemetry backing scout assessments.
29. **`player_comparisons`**: Peer benchmarking and statistical similarity scores between uncapped prospects.

### 2.5. Venue, Pitch & Weather Intelligence (2 Tables, Stage 4)
30. **`match_weather_observations`**: In-match hourly meteorological telemetry (temperature, relative humidity, dew point, dew severity risk index, wind speed/direction, cloud cover) from Open-Meteo CC-BY 4.0 API. Includes `is_forecast: bool` to strictly separate observations from forecast models.
31. **`venue_pitch_reports`**: Expert groundstaff and RR talent scout pitch evaluations, recording soil types (black soil, red soil, loam blend), grass coverage, expected pace/bounce, expected turn, reporter reference, and confidence score.

---

## 3. Alembic Migrations

- Migration `001_uncapped_player_foundation.py`:
  - Upgrades: 29 core, performance, governance, and uncapped scouting tables.
  - Downgrades: Reverse topological drop.
- Migration `002_venue_pitch_weather.py`:
  - Upgrades: Adds `boundary_dimensions_source` and `coordinates_source` columns to `venues`; creates `match_weather_observations` and `venue_pitch_reports` tables with indexes on `(match_id)` and `(venue_id)`.
  - Downgrades: Drops tables and removes added columns cleanly.
- Dialect Agnostic: Seamless execution on PostgreSQL 16 and in-memory SQLite (`sqlite+aiosqlite:///:memory:`).
