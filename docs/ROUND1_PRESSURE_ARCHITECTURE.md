# ROYALS INTELLIGENCE — ROUND 1 PRESSURE ARCHITECTURE & IMPLEMENTATION NOTE
**Document Version:** 1.0.0 (Round 1 Baseline)  
**Target:** SupeRR Selector Season 2 — Round 1  
**Core Objective:** *Identify the Most Reliable Players Under Pressure*  
**Final Deliverables:** Top 10 Batters Under Pressure & Top 10 Bowlers Under Pressure  

---

## 1. Shift in Round 1 Implementation Objective

The previous developmental roadmap targeted:
> *"Top 10 Youngest Uncapped Players Rajasthan Royals Should Back at the IPL 2027 Auction."*

That roadmap is **archived for Round 1** (preserved in Git history and existing codebase documentation, but not executed for this milestone).

The official SupeRR Selector Season 2 Round 1 challenge is:
> **"Build a data-driven system that measures how batters and bowlers perform in high-pressure match situations compared with their usual performance levels. Use your system to identify and rank the players who deliver most consistently when it matters."**

The platform will output:
1. **Top 10 Batters Under Pressure** (Rank 1 through Rank 10)
2. **Top 10 Bowlers Under Pressure** (Rank 1 through Rank 10)
3. **Comprehensive Methodology Report** explaining pressure definitions, baselines, rating logic, fair comparisons (sample sizes, IPL vs T20I), evidence, and reliability/limitations.

---

## 2. Standalone Analysis Package Boundary (`round1_pressure/`)

To protect existing production foundations (Stages 0 through 4), all Round 1 analytics, models, pipelines, and tests reside in a self-contained, isolated package:

```text
round1_pressure/
├── config/             # YAML configurations (dataset schemas, cricket rules, extras mappings)
├── data/               # Raw, processed, and output data partitions (.gitignored)
├── reports/            # Markdown data audit reports and methodology documents
├── src/                # Deterministic analysis scripts and reusable engines
└── tests/              # Dedicated Pytest verification suites
```

### Strict Non-Pollution Guarantees:
- **Zero API/UI Pollution:** No new Next.js pages or FastAPI endpoints are created for Round 1 unless explicitly requested.
- **Zero Schema Pollution:** No PostgreSQL migrations or database schema changes are introduced.
- **Zero Git Leakage:** All competition datasets (41+ MB CSV files) and generated intermediate Parquet files are excluded by `.gitignore`.
- **Local-Only Processing:** In full compliance with competition confidentiality, all data processing runs strictly on local compute; zero raw records are transmitted to external services.

---

## 3. Reusable Components vs. Deferred Components

| Existing Component | Current Implementation | Reusable for Round 1? | Adaptation / Integration Plan |
| :--- | :--- | :---: | :--- |
| **Stage 0 Core Config & Logging** | `app.core.config`, `app.core.logging` | **YES** | Used for environment settings and structured JSON logging. |
| **Stage 1 Parquet Storage** | `app.acquisition.storage.parquet_store` | **YES** | Reusable for high-speed columnar partitioning of processed match-state tables. |
| **Stage 1 Delivery Arithmetic Validator** | `app.acquisition.validation.validator` | **WITH ADAPTATION** | Existing validator assumed Cricsheet column names; must not be run directly against supplied CSV schema (`runs` = batter runs, `extras1_runs` = categorical code). |
| **Stage 2 Canonical Identity Deduplication** | `app.services.identity.player_identity_service` | **PARTIALLY** | `player_id` must be the sole canonical key (never merge on name). Uncapped age cutoffs and 5-year inactive clauses are deferred (Round 1 evaluates all players). |
| **Stage 3 Format-Aware Phase Engine** | `DomesticMatchService.assign_phase()` | **YES** | Identifies Powerplay (0–5), Middle (6–14), and Death (15–19) phases for match-context and pressure weighting. |
| **Stage 3 Dismissal Wicket Attribution** | `BOWLER_CREDITED_DISMISSALS` | **YES** | Strictly credits bowler wickets only for `bowled`, `caught`, `lbw`, `stumped`, and `hit wicket`. Run-outs, retire-outs, and obstructing the field are excluded. |
| **Stage 4 Venue & Weather Telemetry** | `VenueIntelligenceService`, `WeatherIntelligenceService` | **DEFERRED** | Secondary contextual features (dew, boundary dimensions) are deferred until core ball-by-ball pressure ratings are established. |
| **Old Stage 5–13 Roadmap** | Youngest talent, auction valuation, purse allocation | **ARCHIVED** | Preserved in repository documentation for future auction strategy, but inactive for Round 1. |

---

## 4. Data-Quality Dependencies & Findings (R1-01 & R1-01.1)

The R1-01 and R1-01.1 audits established critical domain truths:
1. **Extras Code Trap:** `extras1_runs` is a categorical code (1: Overstep, 2: wide, 3: legbyes, 4: byes, 5: other, 6: NONE, 7: Penalty), NOT numerical runs. `runs` is strictly runs off the bat.
2. **Evidence-Based Delivery Legality & Sequence Verification (R1-01.1):**
   - **Confirmed Legal Deliveries (192,445):** Standard deliveries (189,167), `legbyes` (2,748), `byes` (529), and `Penalty` (1).
   - **Penalty Investigation:** Match 16753, Inn 2, Over 6, Ball 4. Exactly 6 deliveries bowled in over (`over_ball_num` 1–6). Consumed 1 legal ball without re-bowl. Confirmed Legal.
   - **Confirmed Illegal Extras (8,290):** `wide` (7,714) and `Overstep` (576). Always re-bowled.
   - **Ambiguous Extras (`other` - 264 records):**
     - Delivery styles: 116 beamers (above waist), 72 high full tosses, 16 bouncers, 60 other.
     - Dismissals: 0 bowled, 0 caught, 0 LBW (261 NaN, 3 run outs) — proving batters cannot be caught/bowled on these deliveries under no-ball laws.
     - Sequence behavior: In 253 of 264 overs, the over reached 6 legal balls excluding `other` (re-bowled). In remaining 11 instances, the innings ended early (10 target chased mid-over, 1 Super Over).
     - Retained as ambiguous rather than forcing an artificial single classification.
     - Dual Metrics: Strict Legal Total: 192,445 vs Permissive Legal Total: 192,709 (`unresolved_deliveries_count: 264`).
3. **Bowling Credit & Dismissal Spelling Normalization:**
   - 10,272 bowler wickets vs 609 non-bowler dismissals (RunOut: 600, Retire Out: 6, Obstructing: 3).
   - Typo `'Obstracting the field'` (2) normalized with `'Obstructing the field'` (1) to 3 total.
   - Unknown dismissals guard rejects any unlisted dismissal type from bowler credit.
4. **Super Overs:** 38 deliveries across 6 matches segregated from ordinary innings play.
5. **Bowling Speed Cleaning:** 38.7% zeroes and sensor corruptions (-1.0, 1456.1 kph) require rigorous cleaning.
6. **Canonical `player_id`:** Exactly 7 player names belong to multiple distinct cricketers (e.g. Abdul Samad, Rashid Khan). `player_id` must be the sole canonical key.

---

## 5. R1-01 & R1-01.1 Acceptance Verification

- [x] Full repository audit conducted without modifying existing Stage 0–4 code or Git history.
- [x] Standalone package `round1_pressure/` established with `.gitignore` data protection.
- [x] Profiling completed for all 6 CSV files (200,999 deliveries, 883 matches, 141 competitions, 353 teams, 28,381 playing XI rows, 6,413 player mappings).
- [x] Evidence-based delivery legality classification implemented with full sequence investigation.
- [x] `Penalty` delivery investigated in full over context: confirmed legal (6 balls in over, no re-bowl).
- [x] `other` deliveries (264 records) investigated: 253 re-bowled in completed overs, 0 bowled/caught dismissals; retained as explicitly ambiguous with dual reporting.
- [x] Dismissal spelling normalization (`Obstracting` $\to$ `Obstructing`) and unknown dismissal guard implemented.
- [x] 15 focused test cases implemented in `test_data_qa.py` (100% passing).
- [x] Full backend regression verified (61/61 backend tests passing; 76/76 total tests passing).
- [x] Machine-readable `qa_summary.json` and human-readable `data_quality_report.md` generated deterministically.

---

## 6. Pending Decisions for R1-02 (Match-State & Pressure Foundation)

Before implementing the Match-State Engine in task R1-02, the following methodological decisions must be finalized:
1. **Pressure Metric Definition:** Formulate the multidimensional pressure index $\Psi(t)$ combining:
   - Innings phase (Death overs vs Middle vs Powerplay).
   - Required Run Rate (RRR) leverage vs Current Run Rate (CRR).
   - Wickets in hand (Win Probability impact of next dismissal).
   - Chase leverage in 2nd innings vs target setting in 1st innings.
2. **Competition Weighting Matrix:** Calibration of weights between IPL (Tier-1 franchise) and Senior T20I matches (or whether to report them jointly and separately).
3. **Emerging Asia Cup Segregation:** Formalize exclusion of the 30 Emerging Teams Asia Cup matches from the primary IPL/T20I ranking dataset.
4. **Sample Size Qualification Thresholds:** Minimum legal balls faced under pressure (batters) and minimum legal balls bowled under pressure (bowlers) for Top 10 ranking eligibility.
