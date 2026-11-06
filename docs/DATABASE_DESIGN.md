# ROYALS INTELLIGENCE — DATABASE ARCHITECTURE & DESIGN
**Document Version:** 1.0.0 (Stage 0 Baseline)  
**Database Engine:** PostgreSQL 16  
**ORM / Data Layer:** SQLAlchemy 2.0 (Async) + AsyncPG  
**Schema Migration Engine:** Alembic  

---

## 1. Overview & Strategy

The database architecture for ROYALS INTELLIGENCE is designed to handle high-frequency ball-by-ball event streams, multi-dimensional player telemetry, venue environmental states, and confidential auction valuations.

In accordance with **Stage 0 execution rules**:
- Only the core connection engine, session management, declarative metadata base, and migration harness are instantiated.
- No dummy or fabricated cricket tables/records are populated in the database.
- The comprehensive target schema is formally documented below for implementation across Stages 1–13.

---

## 2. Target Entity-Relationship Model (Conceptual)

```
       +------------------+             +------------------+
       |      VENUES      |             |      TEAMS       |
       +--------+---------+             +--------+---------+
                | 1                              | 1
                |                                |
                | M                              | M
       +--------v---------+             +--------v---------+
       |     MATCHES      |<------------|   TEAM_SQUADS    |
       +--------+---------+ M         1 +--------+---------+
                | 1                              | M
                |                                |
                | M                              | 1
       +--------v---------+             +--------v---------+
       |     INNINGS      |             |     PLAYERS      |
       +--------+---------+             +---+----+----+----+
                | 1                         |    |    |
                |                           |    |    |
                | M                         |    |    |
       +--------v---------+                 |    |    |
       |    DELIVERIES    |-----------------+    |    |
       |  (Ball-by-Ball)  | (Bowler/Striker/     |    |
       +------------------+  Non-Striker)        |    |
                                                 |    |
                +--------------------------------+    |
                | M                                   | M
       +--------v---------+                  +--------v---------+
       | SCOUTING_DOSSIER |                  | AUCTION_PROFILE  |
       |  (Confidential)  |                  | (Valuations/WAR) |
       +------------------+                  +------------------+
```

---

## 3. Future Entity Definitions

### 3.1. Core Competition Entities
1. **`teams`**:
   - `id`: UUID (Primary Key)
   - `code`: VARCHAR(10) UNIQUE (e.g., 'RR', 'CSK', 'MI')
   - `name`: VARCHAR(100)
   - `is_rr`: BOOLEAN DEFAULT FALSE
   - `created_at`: TIMESTAMPTZ

2. **`venues`**:
   - `id`: UUID (Primary Key)
   - `name`: VARCHAR(150)
   - `city`: VARCHAR(100)
   - `country`: VARCHAR(100)
   - `altitude_m`: NUMERIC(6, 2)
   - `pitch_soil_type`: VARCHAR(50) (e.g., 'Black Soil', 'Red Soil', 'Composite')
   - `boundary_dim_straight_m`: NUMERIC(5, 2)
   - `boundary_dim_off_m`: NUMERIC(5, 2)
   - `boundary_dim_leg_m`: NUMERIC(5, 2)

3. **`matches`**:
   - `id`: UUID (Primary Key)
   - `external_match_id`: VARCHAR(100) UNIQUE (e.g., Cricsheet / Official ID)
   - `season`: VARCHAR(20) (e.g., 'IPL 2026')
   - `match_date`: DATE
   - `venue_id`: UUID (FK -> venues.id)
   - `team_home_id`: UUID (FK -> teams.id)
   - `team_away_id`: UUID (FK -> teams.id)
   - `toss_winner_id`: UUID (FK -> teams.id)
   - `toss_decision`: VARCHAR(10) ('bat' | 'field')
   - `result`: VARCHAR(50)
   - `winner_id`: UUID (FK -> teams.id, NULLABLE)
   - `margin_runs`: INTEGER (NULLABLE)
   - `margin_wickets`: INTEGER (NULLABLE)

### 3.2. Ball-by-Ball Telemetry
4. **`innings`**:
   - `id`: UUID (Primary Key)
   - `match_id`: UUID (FK -> matches.id)
   - `innings_number`: SMALLINT (1 or 2, plus Super Overs)
   - `batting_team_id`: UUID (FK -> teams.id)
   - `bowling_team_id`: UUID (FK -> teams.id)
   - `total_runs`: INTEGER
   - `total_wickets`: INTEGER
   - `is_declared`: BOOLEAN DEFAULT FALSE

5. **`deliveries`** (High-volume event table):
   - `id`: UUID (Primary Key)
   - `innings_id`: UUID (FK -> innings.id)
   - `over_number`: SMALLINT (1 to 20)
   - `ball_number`: SMALLINT (1 to 6+)
   - `striker_id`: UUID (FK -> players.id)
   - `non_striker_id`: UUID (FK -> players.id)
   - `bowler_id`: UUID (FK -> players.id)
   - `runs_batter`: SMALLINT
   - `runs_extras`: SMALLINT
   - `extra_type`: VARCHAR(20) (NULL, 'wide', 'no-ball', 'leg-bye', 'bye', 'penalty')
   - `is_wicket`: BOOLEAN DEFAULT FALSE
   - `dismissal_type`: VARCHAR(30)
   - `player_dismissed_id`: UUID (FK -> players.id, NULLABLE)
   - `fielder_involved_id`: UUID (FK -> players.id, NULLABLE)
   - `shot_type`: VARCHAR(50) (Optional telemetry)
   - `ball_line`: VARCHAR(30) (Telemetry: 'outside_off', 'stumps', 'down_leg')
   - `ball_length`: VARCHAR(30) (Telemetry: 'yorker', 'full', 'good', 'back_of_length', 'short')
   - `speed_kph`: NUMERIC(5, 2) (Telemetry)

### 3.3. Player & Scouting Entities
6. **`players`**:
   - `id`: UUID (Primary Key)
   - `full_name`: VARCHAR(150)
   - `dob`: DATE
   - `nationality`: VARCHAR(100)
   - `batting_hand`: VARCHAR(10) ('Right', 'Left')
   - `bowling_style`: VARCHAR(50)
   - `primary_role`: VARCHAR(50) ('Batter', 'Bowler', 'All-Rounder', 'Wicketkeeper')
   - `is_capped`: BOOLEAN DEFAULT FALSE

7. **`scouting_reports`** (Confidential RR Domain):
   - `id`: UUID (Primary Key)
   - `player_id`: UUID (FK -> players.id)
   - `scout_id`: VARCHAR(100)
   - `assessment_date`: DATE
   - `competition_observed`: VARCHAR(100)
   - `technical_rating`: NUMERIC(3, 1) (1.0 to 10.0)
   - `psychological_resilience_rating`: NUMERIC(3, 1)
   - `power_hitting_tier`: VARCHAR(20)
   - `qualitative_notes`: TEXT (Encrypted / Restricted)
   - `created_at`: TIMESTAMPTZ

8. **`auction_profiles`** (IPL 2027 Valuation Engine):
   - `id`: UUID (Primary Key)
   - `player_id`: UUID (FK -> players.id)
   - `auction_year`: INTEGER (2027)
   - `estimated_market_value_inr`: NUMERIC(12, 2)
   - `rr_strategic_ceiling_inr`: NUMERIC(12, 2)
   - `projected_war`: NUMERIC(5, 2)
   - `priority_tier`: VARCHAR(10) ('T1', 'T2', 'T3', 'Backup')
   - `updated_at`: TIMESTAMPTZ

---

## 4. Connection Engine & Lifecycle

* **Session Provider:** `app.db.session.get_db` provides an async session via `async_sessionmaker(engine, expire_on_commit=False)`.
* **Async Engine:** Initialized with `create_async_engine(settings.DATABASE_URL, echo=settings.DEBUG, pool_pre_ping=True)`.
* **Graceful Fallback:** If the database service is offline during initial startup, health checks report connection status non-destructively rather than crashing the API server.
