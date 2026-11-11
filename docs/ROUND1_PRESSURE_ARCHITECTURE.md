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

## 8. R1-02.2 & R1-02.3 Final Match-Level Classification Integrity Closure

Tasks R1-02.2 and R1-02.3 resolved the discrepancy between the 23 matches with source-recorded revised targets and the completed DLS chases, separating non-exclusive metadata flags from mutually exclusive match-level categories across all 883 matches:

1. **Separation of Non-Exclusive Metadata Flags (Can Overlap):**
   - **`flag_revised_target_recorded` (23 matches):** Source explicitly provides a positive `revised_target` in `matches.csv` (includes Match 17765).
   - **`flag_revised_overs_recorded` (34 matches):** Source provides revised scheduled-ball metadata (`first_inn_revised_overs` or `second_inn_revised_overs`). Unit verified as legal balls (integers divisible by 6, range 30 to 114).
   - **`flag_dls_method_in_result_text` (19 matches):** Matches whose `result` text contains `'D/L'` or `'DLS'`.
   - **`flag_dls_target_applicable` (22 matches):** Matches where positive revised target was applicable to a concluded chase (excludes Match 17765).
   - **`flag_dls_status_unresolved` (4 matches):** Matches 20182, 23674, 24822, 28334 (DLS stated in result, target/overs omitted from schema).
   - **`flag_match_abandoned` (40 matches):** Matches ending in 'No Result' or 'Match Abandoned' (including Match 17765 and 16 zero-delivery matches).

2. **8 Mutually Exclusive Match Reconciliation Categories (Sum = 883):**
   - `WICKET_WIN_NO_OFFICIAL_TOTAL_IN_SCHEMA`: 394 matches (44.6%)
   - `INCOMPLETE_EXTRAS_RUN_WIN`: 382 matches (43.3%)
   - `NO_RESULT_OR_ABANDONED`: 40 matches (4.5%) [Match 17765 assigned here]
   - `OTHER_RESULT`: 30 matches (3.4%) [Ties, Super Overs]
   - `DLS_TARGET_APPLICABLE`: 22 matches (2.5%) [Concluded chases with verified target]
   - `EXACT_BOTH_INNS_MARGIN_MISMATCH`: 6 matches (0.7%)
   - `EXACT_BOTH_INNS_MARGIN_MATCH`: 5 matches (0.6%)
   - `DLS_STATUS_UNRESOLVED`: 4 matches (0.5%) [Matches 20182, 23674, 24822, 28334]
   - **Total:** Exactly **883 matches** (100.0% coverage, 0 overlap).

3. **Classification Integrity for Edge Cases:**
   - **Match 17765 (IND vs SA 2022):** Single category `NO_RESULT_OR_ABANDONED`. Retains metadata flags `flag_revised_target_recorded = True` (130.0), `flag_revised_overs_recorded = True` (72 balls), `flag_match_abandoned = True`, `flag_dls_target_applicable = False`. Chase was incomplete (abandoned after 25 balls).
   - **Four Unresolved DLS Matches (20182, 23674, 24822, 28334):** Single category `DLS_STATUS_UNRESOLVED`. Exact metrics strictly withheld (`target_source = 'DLS_METHOD_UNRECORDED_TARGET'`, `target_exact = None`, `runs_required_exact = None`, `required_run_rate_exact = None`). Zero invented targets.

4. **Score Uncertainty Protection Rule (Downstream Contract for R1-03):**
   - Do NOT authorize any fallback pressure formula that relies on uncertain current score or current run rate.
   - Exact RRR requires both an exact score AND a valid target.
   - Lower-bound scores must never be represented as exact scores.
   - Any proposed score-independent pressure features (e.g. phase leverage, wickets in hand, balls remaining) must be separately justified and validated in R1-03.
   - Unresolved DLS matches must never receive invented or guessed targets.

5. **Comprehensive Verification:**
   - 39 dedicated unit tests in `test_match_state.py` (54 tests in `round1_pressure`, 61 in `backend`, 115 total across workspace, 100% passing).

---

## 9. R1-03 Pressure Detection and Situation Classification Engine

Task R1-03 implements a reproducible, evidence-driven Pressure Detection Engine that establishes objective, domain-grounded pressure events independently for batters and bowlers before any player ranking or Bayesian scoring is computed:

1. **Discipline Independence & Tactical Asymmetry:**
   - Batting and bowling pressure situations are modeled independently.
   - Tactical asymmetry is rigorously respected:
     - *Death overs with $\ge 6$ wickets in hand:* **HIGH pressure for bowler** (boundary assault hazard), but **LOW pressure for batter** (freedom to attack with abundant wickets).
     - *Powerplay with 3 wickets lost:* **HIGH pressure for batter** (collapse salvage required), but **LOW pressure for bowler** (attacking dominance with huge margin for error).
   - In primary scope: 33,005 batting pressure deliveries (17.01%, 692 batters) vs 39,436 bowling pressure deliveries (20.33%, 480 bowlers).

2. **Empirical Distribution Quantiles & Threshold Selection:**
   - Exact chase RRR distribution on verified subset ($N = 6,748$):
     - Median ($p_{50}$): 9.64
     - 75th percentile ($p_{75}$): 11.48 ($\approx 11.5$)
     - 85th percentile ($p_{85}$): 12.99 ($\approx 13.0$)
     - 90th percentile ($p_{90}$): 14.35 ($\approx 14.5$)
   - Structural leverage points:
     - `BAT_COLLAPSE_EARLY_W3`: $\ge 3$ wickets lost in Powerplay (top 6.2% severe collapses, 3,797 balls, 336 matches).
     - `BAT_DEPLETED_WICKETS_W3`: $\le 3$ wickets in hand in Middle/Death (top 9.7% depleted states, 12,921 balls, 619 matches).
     - `BAT_DEATH_ACCEL_W5`: Overs 16–20 with $\le 5$ wickets in hand (26,130 balls, 774 matches).
     - `BOWL_ASSAULT_HIGH_WICKETS_DEATH`: Overs 16–20 with $\ge 6$ batting wickets in hand (17,373 balls, 667 matches).
     - `BOWL_DEATH_FINAL18`: Overs 18–20 final 18 balls high leverage (24,729 balls, 811 matches).
     - `BOWL_PP_DAMAGE_CONTROL_W0`: Overs 5–6 with 0 wickets taken (4,860 balls, 443 matches).

3. **Zero Outcome Leakage Guarantee:**
   - Pressure classifications depend exclusively on pre-delivery match context (`state_before`).
   - Outcome variables (`runs`, `is_wicket`, `delivery_bowler_conceded_runs`, `dismissals`, `extras`) are strictly forbidden from pressure classification rules.

4. **Score Uncertainty Contract Enforcement & Provenance:**
   - In accordance with R1-02.3, exact chase RRR is strictly withheld (`null`) on `LOWER_BOUND_ONLY` score states and unresolved DLS matches.
   - Vectorized dimension tracking records `dimensions_available` and `dimensions_withheld` for every delivery.
   - Score-independent structural dimensions (`PHASE`, `BALLS_REM`, `WKTS_REM`, `LEGAL_BALLS`) provide complete, uncorrupted match-state pressure detection across all 193,988 primary deliveries.

5. **Operational Candidate Definitions & Coverage:**
   - **Primary Batting Definition (`BAT_COMPOSITE_HIGH`):** 33,005 deliveries (17.01%) across 692 unique batters and 794 matches. Formulated as $\text{CHASE\_P85} \lor \text{COLLAPSE\_W3} \lor \text{DEPLETED\_W3} \lor \text{DEATH\_ACCEL\_W5}$ with exact inclusion-exclusion union verified.
   - **Primary Bowling Definition (`BOWL_COMPOSITE_HIGH`):** 39,436 deliveries (20.33%) across 480 unique bowlers and 822 matches. Formulated as $\text{ASSAULT\_DEATH} \lor \text{FINAL18} \lor \text{PP\_W0} \lor \text{DEF\_P85}$ with exact inclusion-exclusion union verified.
   - Sensitivity analysis across Strict vs Permissive scenarios demonstrates zero variance in batting (0.000%) and 80 deliveries variance in bowling (0.041%), physically isolated to cumulative legal ball boundary shifts in Over 17 (72 balls) and Over 4 (8 balls).
   - Reconciled population metrics: 200,999 raw total = 193,988 primary bowled deliveries + 7,011 excluded (6,985 Emerging + 26 Senior Super Overs). Strict legal is 185,692; Permissive legal is 185,951. Score completeness: 86,905 EXACT + 107,083 LOWER_BOUND_ONLY = 193,988; exact chase demand available on 6,748 deliveries, withheld on 187,240 deliveries.

6. **Generated Datasets & Reports:**
   - `batting_pressure_events_strict.parquet`
   - `bowling_pressure_events_strict.parquet`
   - `batting_pressure_events_permissive.parquet`
   - `bowling_pressure_events_permissive.parquet`
   - `pressure_definition_comparison.parquet`
   - `pressure_coverage_summary.parquet`
   - `pressure_detection_report.md`

7. **Test Verification:**
   - 22 dedicated unit tests in `test_pressure_detection.py` (76/76 in `round1_pressure`, 61/61 in `backend`, 137/137 total passing across workspace).

---

## 10. R1-04 Expected Performance Baselines & Bayesian Reliability Foundation

Task R1-04 establishes statistically defensible player performance baselines under ordinary conditions, calculates player-level pressure-versus-ordinary differentials, and implements hierarchical Empirical Bayes shrinkage:

1. **Stratified Ordinary Baselines (12 Context Cells):**
   - Ordinary (non-pressure) deliveries are partitioned into 12 mutually exclusive strata:
     $$\text{Cell} = \text{comp\_tier (IPL, T20I)} \times \text{innings (1, 2)} \times \text{innings\_phase (Powerplay, Middle, Death)}$$
   - Batting baseline population: **154,529** legal ordinary deliveries (83.2% of primary scope).
   - Bowling baseline population: **148,678** legal ordinary deliveries (80.1% of primary scope).
   - Baselines are evaluated independently for batters and bowlers, preventing cross-discipline contamination.

2. **Simpson's Paradox Discovery in Pressure Batting:**
   - Raw overall ordinary strike rate is **139.7**, while raw pressured strike rate is **140.9** (+1.2 SR points).
   - **The Confounding:** 79.3% of pressure deliveries occur in the Death phase, where the ordinary baseline strike rate is **176.5**.
   - **True Within-Phase Degradation Under Pressure:**
     - Death: Strike rate drops from **176.5 to 149.2** (-27.3 points; 15.5% drop).
     - Middle: Strike rate drops from **134.3 to 104.3** (-30.0 points; 22.3% drop).
     - Powerplay: Strike rate drops from **137.2 to 113.3** (-23.9 points; 17.4% drop).
   - **Context-Weighted Expectations:** Every player's expectation under pressure is computed as:
     $$E[M_i] = \sum_{c} w_{i,c} \cdot B_{c,M}$$
     where $w_{i,c}$ is player $i$'s empirical proportion of pressure deliveries in cell $c$. This eliminates phase-distribution confounding.

3. **Bowling Degradation Under Pressure:**
   - Ordinary overall economy is **7.98 RPO**, jumping to **10.07 RPO** under pressure (+2.08 RPO increase in runs conceded).
   - Powerplay Overs 5–6 with 0 wickets lost: Economy surges from **7.95 to 10.33 RPO** (+2.38 RPO).
   - Death overs: Economy surges from **7.98 to 10.03 RPO** (+2.05 RPO).

4. **Hierarchical Empirical Bayes Shrinkage (DerSimonian-Laird):**
   - Observed sample differentials $y_i = \text{Observed}_i - E[M_i]$ are separated into true talent differentials and sampling noise:
     $$\theta_i = r_i y_i + (1 - r_i) \mu, \quad r_i = \frac{\tau^2}{\tau^2 + \sigma_i^2}$$
   - **Batting Strike Rate Differential:**
     - Prior Population Mean $\mu = -34.24$ SR points.
     - Between-Player Variance $\tau^2 = 1,084.89$ ($\tau = 32.94$ SR points).
     - Minimum qualification threshold: $\ge 30$ legal balls under pressure (278 qualified batters of 691).
     - Median reliability $r_i = 0.747$ (range: 0.436 to 0.955).
   - **Bowling Economy Differential:**
     - Prior Population Mean $\mu = +1.82$ RPO.
     - Between-Player Variance $\tau^2 = 0.59$ ($\tau = 0.77$ RPO).
     - Minimum qualification threshold: $\ge 30$ legal balls under pressure (239 qualified bowlers of 479).
     - Median reliability $r_i = 0.296$ (range: 0.088 to 0.841). Bowling economy exhibits much higher per-ball variance, appropriately requiring stronger shrinkage toward the population mean.

5. **Chronological Out-of-Sample Validation:**
   - Train on past seasons **2022–2024** (111,323 legal balls); test on future seasons **2025–2026** (74,369 legal balls).
   - **Batting ($N = 108$ overlapping players):**
     - Raw Sample MSE: 1,240.03 $\to$ Shrunk Posterior MSE: 994.00 (**19.8% MSE reduction**).
     - Cross-era correlation: Raw $r = 0.549 \to$ Shrunk $r = 0.570$.
   - **Bowling ($N = 115$ overlapping players):**
     - Raw Sample MSE: 4.57 $\to$ Shrunk Posterior MSE: 2.77 (**39.4% MSE reduction**).
     - Cross-era correlation: Raw $r = 0.136 \to$ Shrunk $r = 0.185$.
   - Shrunk differentials demonstrably improve predictive accuracy and stability over raw observed statistics.

6. **Strict Scope Boundary Invariant:**
   - In accordance with task constraints, NO composite rankings, Top 10 lists, or final Pressure Index $\Psi$ are constructed in R1-04.

7. **Generated Datasets & Reports:**
   - `batting_ordinary_baseline.parquet`
   - `bowling_ordinary_baseline.parquet`
   - `batting_pressure_differentials.parquet`
   - `bowling_pressure_differentials.parquet`
   - `bayesian_shrinkage_summary.parquet`
   - `chronological_validation_results.parquet`
   - `expected_performance_report.md`

8. **Test Verification:**
   - 14 dedicated unit tests in `test_expected_performance.py` (90/90 in `round1_pressure`, 61/61 in `backend`, 151/151 total passing across workspace).

---

## 11. Downstream Roadmap for R1-05 (Player Reliability Scoring & Final Rankings)

With statistical baselines established, differentials contextualized, and Empirical Bayes shrinkage validated out-of-sample, the final analytical stage (R1-05) will construct:
1. **Multi-Metric Composite Reliability:** Synthesizing shrunk differentials (Strike Rate, Dot %, Boundary %, Dismissal % for batters; Economy, Wicket %, Dot %, Boundary Conceded % for bowlers).
2. **Context Leverage Weighting:** Combining frequency-based sample reliability with leverage-weighted pressure exposure.
3. **Credibility Bounds:** Incorporating 95% Credible Intervals to guard against sample size fragility.
4. **Final Top 10 Rankings:** Publishing reproducible, fully audited Top 10 Most Reliable Batters and Top 10 Most Reliable Bowlers Under Pressure.
