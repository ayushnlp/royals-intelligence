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

## 6. R1-02 Match-State Reconstruction Baseline

Task R1-02 delivers a deterministic, independently tested delivery-level match-state reconstruction engine:
- **Dual Scenarios Implemented:**
  - **Scenario A (Strict):** 192,445 legal deliveries (`other` treated as illegal/re-bowled per sequence evidence).
  - **Scenario B (Permissive):** 192,709 legal deliveries (`other` treated as legal for sensitivity analysis).
- **Explicit `state_before` and `state_after`:** Tracked across cumulative runs, wickets, legal balls, balls remaining, CRR, RRR, and completion status.
- **Scope Segregation:**
  - 193,988 primary deliveries across IPL & Senior T20I matches.
  - 30 Emerging tournament matches (6,985 deliveries) and 6 Super Over matches (38 deliveries) segregated into `excluded_innings.parquet`.
  - 16 abandoned matches documented.
- **Score Completeness Governance:**
  - 329 innings verified as `EXACT` (zero unconfirmed extras).
  - 1,395 innings flagged as `LOWER_BOUND_ONLY` due to unconfirmed bye/legbye/penalty run amounts.
  - No synthetic runs fabricated.
- **Parquet Datasets Saved:**
  - `delivery_states_strict.parquet`
  - `delivery_states_permissive.parquet`
  - `innings_state_summary.parquet`
  - `match_state_summary.parquet`
  - `match_result_reconciliation.parquet`
  - `dls_and_revised_overs_audit.parquet`
  - `excluded_innings.parquet`
  - `reconstruction_audit.parquet`

---

## 7. R1-02.1 Match-State Integrity Audit & Remediation

Task R1-02.1 performed a focused integrity audit and targeted remediation to ensure zero false mathematical precision:
1. **Score Disentanglement & Strict Withholding:**
   - Cumulative team scores are segregated into lower bounds (`cumulative_team_runs_lower_bound`) and exact scores (`cumulative_team_runs_exact`).
   - Exact chase metrics (`runs_required_exact`, `required_run_rate_exact`) are strictly set to `null` on `LOWER_BOUND_ONLY` innings to prevent downstream mathematical corruption.
   - Robust bounding metrics (`runs_required_upper_bound`, `required_run_rate_upper_bound`) remain populated for all innings.
2. **Empirical Inference Status of `extras_2_runs`:**
   - Present on 36 deliveries (0.018%) with values `1` or `4` on no-balls.
   - Classified as an empirical inference rather than an official schema specification, preserving documented uncertainty.
3. **Match-Result Reconciliation Across All 883 Matches:**
   - Established that `matches.csv` contains NO independent official innings score fields (`inn1_runs`, `inn2_runs`). Only text `result`.
   - Reconciled all 883 matches across 7 mutually exclusive categories in `match_result_reconciliation.parquet`.
4. **Revised Overs & DLS Audit Across All 34 Curtailed Matches:**
   - Proved that revised overs fields store legal balls (integers divisible by 6, range 30 to 114 balls).
   - Confirmed all 23 DLS targets apply exclusively to Innings 2. Cataloged in `dls_and_revised_overs_audit.parquet`.
5. **Strict vs. Permissive Reconciliation (The 5 Out-of-Scope Ambiguous Deliveries):**
   - Accounted for all 264 ambiguous `other` deliveries: 259 in primary scope, 3 in Emerging Teams Asia Cup 2024 (Matches 37088, 37090, 37093), 1 in Asia Cup Rising Stars 2025 (Match 48015), and 1 in IPL 2025 Super Over (Match 40725, Innings 3).
6. **Downstream Feature-Eligibility Contract (R1-03 Transition):**
   - **Tier 1 (Safe for All Deliveries):** Striker runs, legal balls bowled/faced, wickets, bowler attribution, balls remaining, match metadata, phase.
   - **Tier 2 (Score-Dependent):** `runs_required_exact`, `required_run_rate_exact`, `cumulative_team_runs_exact` (restricted strictly to `EXACT` score subsets; models on partial matches must use bounded intervals).
   - **Tier 3 (Uncertain / Sensitivity Required):** Multi-run byes/legbyes, penalty amounts, ambiguous `other` deliveries (must evaluate Strict vs Permissive scenarios).
7. **Comprehensive Test Suite:**
   - Expanded from 16 to 30 tests in `test_match_state.py` covering miniature fixtures and dataset-wide invariants.
   - 45/45 tests passing in `round1_pressure`; 61/61 backend tests passing (106/106 total passing across repository).

---

## 8. R1-02.2 DLS Classification & Match-Reconciliation Consistency Audit

Task R1-02.2 resolved the discrepancy between the 23 matches with `revised_target > 0` and the 26 matches classified under `DLS_REVISED_TARGET` in R1-02.1, and established unambiguous classification definitions:

1. **Resolution of the 23-vs-26 Discrepancy:**
   - **Root Cause:** In R1-02.1, regex classification matched `"D/L"` or `"DLS"` in result strings before checking match outcome status:
     - 22 completed chases with `revised_target > 0` were included.
     - 4 matches (Matches 20182, 23674, 24822, 28334) had DLS in their result text, but both `revised_target` and revised overs were completely absent (NaN) from the schema.
     - 1 match (Match 17765: SA in IND 2022) had `revised_target = 130.0`, but was abandoned as `"No Result"` after 25 balls in Innings 2, routing to `NO_RESULT_OR_ABANDONED` (-1).
   - **Formula:** `23 recorded target - 1 abandoned (17765) + 4 unrecorded target matches = 26 matches` (net: `+3`).
2. **The 5 Authoritative Audit Concepts & Exact Counts:**
   - **`REVISED_TARGET_RECORDED` (23 matches):** Explicitly recorded `revised_target > 0` in `matches.csv`.
   - **`REVISED_OVERS_RECORDED` (34 matches):** Explicitly recorded `first_inn_revised_overs` or `second_inn_revised_overs`.
   - **`DLS_TARGET_APPLICABLE` (22 matches):** Positive revised target applicable to a concluded second-innings chase.
   - **`CURTAILED_WITHOUT_REVISED_TARGET` (11 matches):** Shortened matches without a recorded revised target: 2 completed 11-over standard chases (Matches 16753, 19959) where both innings were equally curtailed before play, plus 9 matches abandoned during Innings 1.
   - **`DLS_STATUS_UNRESOLVED` (4 matches):** Matches 20182, 23674, 24822, 28334. Result mentions D/L or DLS method, but target and overs are absent from schema.
3. **8 Mutually Exclusive Match Reconciliation Categories (Sum = 883):**
   - `WICKET_WIN_NO_OFFICIAL_TOTAL_IN_SCHEMA`: 394 matches
   - `INCOMPLETE_EXTRAS_RUN_WIN`: 382 matches
   - `NO_RESULT_OR_ABANDONED`: 39 matches (includes Match 17765)
   - `OTHER_RESULT`: 30 matches (Ties, Super Overs, bowl-outs)
   - `REVISED_TARGET_RECORDED`: 23 matches (official revised targets)
   - `EXACT_BOTH_INNS_MARGIN_MISMATCH`: 6 matches (exact deliveries, boundary multi-run extras discrepancy)
   - `EXACT_BOTH_INNS_MARGIN_MATCH`: 5 matches (exact mathematical match)
   - `DLS_STATUS_UNRESOLVED`: 4 matches (Matches 20182, 23674, 24822, 28334)
   - **Total:** Exactly **883 matches** (100% coverage, 0 overlap).
4. **Target Assignment & Invariants:**
   - First-innings target is ALWAYS `null` (`target_exact = None`, `runs_required_exact = None`, `required_run_rate_exact = None`).
   - Ordinary second-innings chase target is `cumulative_team_runs_exact(Innings 1) + 1`. If Innings 1 is `LOWER_BOUND_ONLY`, exact chase metrics are strictly withheld.
   - For `DLS_STATUS_UNRESOLVED` matches, `target_source = 'DLS_METHOD_UNRECORDED_TARGET'` and exact chase metrics are strictly withheld. Never fabricate or guess unrecorded DLS par targets.
5. **Comprehensive Verification:**
   - 34 dedicated unit tests in `test_match_state.py` (49 tests in `round1_pressure`, 61 in `backend`, 110 total across workspace, 100% passing).

---

## 9. Pending Decisions for R1-03 (Pressure Index & Quantification Engine)

With match state reconstructed and audited immediately before and after every delivery, the system is ready for Task R1-03:
1. **Multidimensional Pressure Index $\Psi(t)$:**
   - Innings phase leverage (Death overs vs Middle vs Powerplay).
   - Chase leverage (RRR vs CRR delta, runs required, balls remaining).
   - Wicket leverage (wickets in hand impact).
   - Target setting leverage (1st innings score acceleration pressure).
2. **Competition Weighting Matrix:** Calibration between IPL (Tier-1 Franchise) and Senior T20I.
3. **Qualification Thresholds:** Minimum legal balls faced / bowled under pressure for ranking inclusion.
