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
   - 20 dedicated unit tests in `test_expected_performance.py` (96/96 in `round1_pressure`, 61/61 in `backend`, 157/157 total passing across workspace).

---

## 11. R1-04.1 Statistical Validation, Bayesian Methodology and Baseline Robustness Audit

Task R1-04.1 executes an exhaustive statistical and methodological audit of the R1-04 foundation:

1. **Chronological Out-of-Sample Predictive Verification (Audit A):**
   - Zero future-period information enters historical posteriors or parameter estimation.
   - Evaluated against three transparent baseline predictors (Zero differential $\hat{y}=0$, Historical population mean $\hat{y}=\mu_{\text{train}}$, and Raw historical differential $\hat{y}=y_{i,\text{train}}$).
   - Paired $t$-tests confirm statistically significant MSE reductions: Batting raw 1,240.03 $\to$ shrunk 994.00 (**+19.8%**, $p = 0.0151$); Bowling raw 4.57 $\to$ shrunk 2.77 (**+39.4%**, $p = 0.0052$).
   - 95% Confidence Intervals for MSE difference are strictly positive.
2. **Sampling Variance & Clustering Addressed (Audit B):**
   - Intra-match delivery clustering inflates standard errors by +8.6% in batting and +13.6% in bowling.
   - Incorporating match-level cluster-robust standard errors further reduces batting prediction MSE to 936.79 (**+24.5% reduction** over raw).
3. **Qualification Threshold Robustness (Audit C):**
   - Sensitivity testing across 10, 20, 30, 50, 75, 100 legal pressure balls confirms that 30 balls provides the optimal balance, capturing 96.4% of batting and 97.1% of bowling pressure volume while avoiding small-sample tailender distortions.
4. **Common Support & Stratification Bounds (Audit D):**
   - Proved mathematically that conditioning ordinary baselines on severe match states (e.g. $\le 4$ wickets remaining in Death) causes a **positivity / common support violation** (12 empty cells), confirming that the 12-cell context grid is the maximal empirical stratification satisfying common support.
5. **Simpson's Paradox Exact Reproduction (Audit E):**
   - Confirmed exact numbers: Ordinary 139.7 vs Pressure 140.9 overall; Death 176.5 vs 149.2; Middle 134.3 vs 104.3; Powerplay 137.2 vs 113.3.
6. **Shrinkage Weight Disambiguation (Audit F):**
   - Clarified that $r_i \in [0, 1]$ is a variance-ratio shrinkage weight, not a probability of reliability.
   - Verified that $n=1$ observations have wide 95% credible intervals (> 125 SR points), preventing artificial precision.
7. **Strict Scope Boundary Invariant:**
   - No player rankings, Top 10 lists, or composite index $\Psi$ created.

---

## 12. R1-05 Explainable Player Pressure Reliability Scoring Engine

Task R1-05 constructs an explainable, statistically grounded player pressure reliability scoring engine to answer the SupeRR Selector Season 2 — Round 1 objective: *Identify the Most Reliable Players Under Pressure*.

### 1. Architectural Scope & Methodological Principles:
- **Discipline Independence:** Batting and bowling reliability models operate completely independently and are never co-mingled in primary evaluation.
- **Population Evaluated:** All 691 batters (278 qualified $\ge 30$ legal pressure balls) and 479 bowlers (239 qualified $\ge 30$ legal pressure balls).
- **Two-Way All-Rounder Synthesis:** Exactly 139 players qualify in both disciplines; analyzed using dual combination methods (Harmonic and Arithmetic Means) while fully preserving separate discipline scores.
- **Anti-Simplification Mandate:** Reliability is not defined by naive raw strike rates or economy rates. True reliability integrates:
  1. Context-adjusted expected performance (controlling for phase, innings, tier).
  2. Hierarchical Empirical Bayes shrinkage (DerSimonian-Laird estimation).
  3. Posterior estimation uncertainty (penalizing small-sample volatility via credible lower bounds).
  4. Multi-season temporal consistency (rewarding sustained multi-year reliability and penalizing inter-season volatility).

### 2. Implemented Candidate Scoring Formulations:
To guarantee transparent explainability and verify sensitivity across model choices, five distinct formulations were evaluated:
1. **Conservative Credibility Bound (Value-at-Risk, 84.1% One-Sided Lower Bound):**
   - Batting: $\text{Score}_{\text{bat, cons}} = \hat{\theta}_{i, \text{SR}} - 1.0 \times \text{SE}_{\text{post}, i}$
   - Bowling: $\text{Score}_{\text{bowl, cons}} = -\hat{\theta}_{i, \text{Econ}} - 1.0 \times \text{SE}_{\text{post}, i}$
2. **Conservative 95% One-Sided Lower Bound:**
   - Evaluates lower tail under 95% credibility: $\hat{\theta} - 1.645 \times \text{SE}_{\text{post}}$.
3. **Posterior Exceedance Probability vs Ordinary Baseline:**
   - Batting: $P(\theta_i > 0 \mid y) = \Phi\left(\frac{\hat{\theta}_{i, \text{SR}}}{\text{SE}_{\text{post}, i}}\right)$
   - Bowling: $P(\theta_i < 0 \mid y) = \Phi\left(\frac{-\hat{\theta}_{i, \text{Econ}}}{\text{SE}_{\text{post}, i}}\right)$
4. **Posterior Exceedance Probability vs Pressured Peers:**
   - Batting: $P(\theta_i > \mu_{\text{bat}} \mid y) = \Phi\left(\frac{\hat{\theta}_{i, \text{SR}} - \mu_{\text{bat}}}{\text{SE}_{\text{post}, i}}\right)$ where $\mu_{\text{bat}} = -34.24$ SR pts.
   - Bowling: $P(\theta_i < \mu_{\text{bowl}} \mid y) = \Phi\left(\frac{\mu_{\text{bowl}} - \hat{\theta}_{i, \text{Econ}}}{\text{SE}_{\text{post}, i}}\right)$ where $\mu_{\text{bowl}} = +1.82$ RPO.
5. **Multi-Dimensional Composite Pressure Reliability Index ($\text{PRI} \in [0, 100]$):**
   - Integrates primary scoring/containment ($45\%$), boundary hazard control ($20\%$), dot-ball control ($20\%$), and dismissal/wicket threat ($15\%$), scaled by a **Temporal Consistency Factor (TCF)**:
     $$\text{TCF}_i = \left(\frac{\min(S_i, 4)}{4}\right)^{0.35} \times \left(1 - 0.25 \times \min\left(1.0, \frac{\sigma_{\text{season}, i}}{\text{Scale}_\sigma}\right)\right)$$

### 3. Pairwise Methodological Agreement:
Pairwise Spearman rank correlations across all candidate scoring formulations confirm methodological consistency:
- Batting: Pairwise correlations between Conservative Lower Bound, 95% Bound, Exceedance Probabilities, and Composite PRI range from **0.884 to 0.995**.
- Bowling: Correlations between Conservative Runs Saved and Composite PRI range from **0.781 to 0.990**.
- **Floor Effect in Bowling Baseline Exceedance:** In bowling, ordinary economy is 7.98 RPO while pressure economy is 10.07 RPO. Only Jasprit Bumrah maintains a shrunk differential below ordinary baseline ($\hat{\theta} = -0.20$ RPO, $P(\theta < 0) = 71.1\%$), causing floor compression for $P(\theta < 0)$ across all other bowlers. In contrast, evaluating against pressured peers ($P(\theta < \mu)$) and using Conservative Runs Saved per Over provides smooth, continuous differentiation across the entire population.

### 4. Key Empirical Benchmarks:
- **Top Batters Under Pressure (Diagnostic Conservative Bound):**
  - **Nicholas Pooran:** 212 balls, 26 matches, 5 seasons (135 death balls). Shrunk diff **+16.2 $\pm$ 14.0** (95% CI: [-11.2, +43.6]). Cons. 84% Bound: **+2.2 SR pts**, $P(\text{Beat Baseline}) = 87.7\%$, Composite PRI = **83.4**.
  - **Donovan Ferreira:** 84 balls, 13 matches, 4 seasons. Shrunk diff **+20.7 $\pm$ 19.8**. Cons. Bound: **+0.9 SR pts**, $P(\text{Beat Baseline}) = 85.2\%$, PRI = **94.7**.
  - **Tim David:** 290 balls, 33 matches, 5 seasons (261 death balls). Shrunk diff **+9.6 $\pm$ 12.1**. Cons. Bound: **-2.5 SR pts**, $P(\text{Beat Baseline}) = 78.6\%$, PRI = **95.5**.
  - **Dinesh Karthik:** 260 balls, 30 matches, 3 seasons (253 death balls). Shrunk diff **+9.2 $\pm$ 11.9**. Cons. Bound: **-2.7 SR pts**, PRI = **86.9**.
  - **Ashutosh Sharma:** 191 balls, 20 matches, 3 seasons (179 death balls). Shrunk diff **+10.3 $\pm$ 13.9**. Cons. Bound: **-3.6 SR pts**, PRI = **87.5**.
  - **Marcus Stoinis:** 220 balls, 32 matches, 5 seasons. Shrunk diff **+7.1 $\pm$ 12.9**, Cons. Bound: **-5.8 SR pts**, PRI = **78.8**.
  - **Rinku Singh:** 363 balls, 48 matches, 5 seasons. Shrunk diff **+3.4 $\pm$ 10.4**, Cons. Bound: **-7.0 SR pts**, PRI = **93.4**.
  - **Tristan Stubbs:** 266 balls, 33 matches, 5 seasons. Shrunk diff **+2.4 $\pm$ 10.5**, Cons. Bound: **-8.2 SR pts**, PRI = **86.5**.
- **Top Bowlers Under Pressure (Diagnostic Conservative Runs Saved):**
  - **Jasprit Bumrah:** 521 balls, 60 matches, 5 seasons (454 death balls). Raw Econ 8.94 vs Exp 9.70 (-0.76 RPO). Shrunk diff **-0.20 $\pm$ 0.36 RPO** (95% CI: [-0.90, +0.50]). Conservative Runs Saved: **-0.16 RPO** (the ONLY qualified bowler conceding fewer runs than ordinary baseline under pressure). $P(\text{Beat Baseline}) = 71.1\%$, $P(\text{Beat Peers}) = 100.0\%$, Composite PRI = **79.7**.
  - **Sunil Narine:** 153 balls, 24 matches, 5 seasons (120 death balls). Shrunk diff **+0.39 $\pm$ 0.55 RPO**. Cons. Runs Saved: **-0.94 RPO**, $P(\text{Beat Peers}) = 99.5\%$, PRI = **67.3**.
  - **Maheesh Theekshana:** 421 balls, 58 matches, 5 seasons. Shrunk diff **+0.55 $\pm$ 0.41 RPO**. Cons. Runs Saved: **-0.96 RPO**, PRI = **63.5**.
  - **Matheesha Pathirana:** 440 balls, 44 matches, 5 seasons (440 death balls). Shrunk diff **+0.63 $\pm$ 0.41 RPO**. Cons. Runs Saved: **-1.05 RPO**, PRI = **66.1**.
  - **Mustafizur Rahman:** 578 balls, 61 matches, 5 seasons (521 death balls). Shrunk diff **+1.09 $\pm$ 0.38 RPO**. Cons. Runs Saved: **-1.47 RPO**, PRI = **56.8**.
- **Two-Way All-Rounder Evaluation ($N = 139$):**
  - Top performers by Harmonic PRI (penalizes single-discipline skew): Sunil Narine (Harmonic PRI: 77.2; Bat PRI 90.5, Bowl PRI 67.3), Ravindra Jadeja, Rashid Khan, Romario Shepherd, Andre Russell, Axar Patel, Sam Curran.

### 5. Strict Governance & Boundaries:
- **Zero Raw Data Commits:** All raw CSVs and generated Parquet files remain untracked in `.gitignore`.
- **No Auction or Squad Optimization:** No player prices, auction values, purse optimization, team optimizers, or API alterations.
- **No Unstratified Definitive Top 10:** Results are presented as diagnostic reliability profiles with full estimation uncertainty (credible intervals) and explainability records.

---

## 13. Task R1-05.1: Independent Statistical Audit & Metric Governance

An independent statistical audit of the R1-05 Player Pressure Reliability Scoring Engine was conducted to evaluate normalization stability, weight sensitivity, temporal scaling, legality robustness, Bayesian prior choices, and bowling baseline reconciliation.

### 1. PRI Normalization Architecture & Cohort Perturbation Test:
- **Normalization Transform:** Raw components are min-max scaled to $[0, 100]$ across qualified cohorts ($N = 278$ batting, $N = 239$ bowling), weighted, multiplied by TCF, and min-max scaled a second time.
- **Controlled Perturbation Tests:** Dropping a 10% random sample shifts existing players' PRI scores by an average of 0.401 pts (batting) and 0.584 pts (bowling), while Spearman rank correlation remains $> 0.999$.
- **Governance Finding:** PRI is strictly a **cohort-relative index**, NOT an absolute probability or invariant score. Adding or removing players modifies other players' absolute scores.

### 2. Weight Sensitivity & Essential Anchoring:
- **Equal Weights Concordance:** Spearman rank correlation between equal weights (25/25/25/25) and baseline (45/20/20/15) is **0.9952** (batting) and **0.9925** (bowling); Top 10 roster overlap is 9 of 10 players (81.8% Jaccard).
- **Essential Anchor:** Removing the Conservative Credible Bound drops Top 10 Jaccard overlap to **42.9%**, allowing small-sample noisy outliers to enter the top tier. The Conservative Bound is verified as the essential statistical stabilizer.

### 3. Temporal Consistency Factor (TCF) Deep Dive:
- **Rank Shift Impact:** TCF causes an average rank shift of **34.3 positions** (and up to 160 positions) against raw execution scores ($r_s = 0.8366$).
- **Tenure Penalty:** Players with only 2 seasons receive a mandatory base scalar penalty $(2/4)^{0.35} = 0.785$, severely capping their scores regardless of per-ball performance.
- **Noise vs Volatility:** Empirical seasonal variance conflates Poisson sampling noise with true talent volatility.
- **Governance Classification:** TCF is formally designated as **EXPERIMENTAL / HEURISTIC**.

### 4. Strict vs Permissive Legality Robustness:
- **Batting Events:** 0 balls difference (100% invariant, $r_s = 1.000$).
- **Bowling Events:** 208 balls difference (0.56% volume variance) restricted to Over 17 and Over 4 boundary transitions. Spearman rank correlation between Strict and Permissive bowler metrics is $> 0.9998$.
- **Policy Invariant:** Strict delivery legality is preserved as the authoritative primary policy.

### 5. Bayesian Prior Sensitivity:
- Ranks remain highly stable across alternative priors (Zero $\mu=0$, Diffuse $2\tau$, Skeptical $0.5\tau$, Shifted $\mu \pm 10$ SR): $r_s > 0.982$.
- Small-sample players ($n \approx 30$) shift by up to 21 SR points across priors, whereas veterans ($n \ge 250$) shift by $< 6$ SR points, validating appropriate Empirical Bayes shrinkage.

### 6. Bowling Baseline Reconciliation (+2.085 RPO vs +1.823 RPO):
- **+2.085 RPO:** Unweighted macro delivery rate difference across all 148,678 ordinary balls (7.980 RPO) vs 37,014 pressure balls (10.065 RPO). Distorted by phase-allocation bias (87.7% of pressure balls are in Death overs).
- **+1.823 RPO:** DerSimonian-Laird random-effects population prior mean $\mu_{\text{DL}}$. Stratified against exact 12-cell context expectation $E[M_i]$ and weighted by inverse total variance $w_i = 1 / (\tau^2 + \sigma_i^2)$.
- **Resolution:** Both metrics are mathematically sound and measure distinct analytical levels. Neither baseline was altered.

### 7. Final Metric Governance:
- **Primary Batting Diagnostic Metric:** Conservative Lower Credible Bound ($\hat{\theta}_{\text{SR}} - 1.0 \times \text{SE}_{\text{post}}$).
- **Primary Bowling Diagnostic Metric:** Conservative Runs Saved per Over ($-\hat{\theta}_{\text{Econ}} - 1.0 \times \text{SE}_{\text{post}}$).
- **Composite PRI:** Retained as an exploratory cohort-relative index, always presented alongside credible intervals and sample sizes.
- **Harmonic All-Rounder PRI:** Authoritative synthesis method to prevent one-discipline masking.

---

## 14. Task R1-05.2: Statistical Validation Closure & Methodology Reconciliation

This milestone closes all validation gaps identified during R1-05.1 through targeted mathematical reconciliations, controlled cohort additions, sample-stratified Bayesian prior analyses, out-of-sample transferability evaluations, and probability calibration bounds.

### 1. Strict vs Permissive Batting Count Reconciliation:
- **Situational Pressure Exposure (R1-03.1):** Exactly 33,005 deliveries under Strict and 33,005 under Permissive (**0 delta; 100% invariant**). Pressure situations are determined strictly *before* the delivery is bowled.
- **Legal Pressure Deliveries Bowled (R1-05.1):** 31,163 balls under Strict vs 31,257 balls under Permissive (**94 delta; 0.30% variance**).
- **Exact Cause Traced:** Every single one of the 94 differing balls has `extras_type == 'other'`. Under Strict legality (sequence evidence), these are illegal re-bowled deliveries; under Permissive legality, they are treated as legal. Exactly 94 of the 259 primary `other` extras occurred during pressure situations.

### 2. Complete Cohort Addition Perturbation Results (Isolated Fixture):
- **Within-Range Additions:** Adding synthetic players at median, 10th percentile, or 90th percentile causes **0.0000 PRI score delta** on all existing players (1.000 rank correlation).
- **Boundary Outliers:** Adding extreme synthetic outliers beyond current minimum/maximum values causes a minor compression shift (mean delta ~0.5 to 1.8 pts) while rank correlation remains $> 0.998$.
- **Season Expansion:** Simulating a 25-player cohort expansion (~10% growth) across new seasons preserves 100% of Top 10 roster membership for batting ($r_s = 0.9999$) and 81.8% for bowling ($r_s = 0.9960$).

### 3. Extended Bayesian Prior Sensitivity across Sample-Size Strata:
- **Strata Evaluated:** Small Sample (30–59 balls), Medium Sample (60–149 balls), and Large Sample ($\ge 150$ balls).
- **Invariance:** Rank orders across all sample strata remain $> 0.98$ correlated with baseline Empirical Bayes.
- **Uncertainty Bounds:** Small-sample batters have mean posterior SE of $\pm 19.57$ SR points (95% CI width: 76.8 SR points), compared to $\pm 12.00$ SR points for large-sample veterans (95% CI width: 47.0 SR points).
- **Exceedance Sensitivity:** Exceedance against Ordinary Baseline for small-sample batters shifts from 12.0% under $\mu=-34.24$ to 24.2% under $\mu=0.0$, demonstrating that exceedance reflects model credibility under prior assumptions, NOT an absolute match probability.

### 4. Historical & Competition Transferability:
- **Historical Transfer (2022–2024 to 2025–2026):**
  - Evaluated on 82 qualified batters and 98 qualified bowlers.
  - Empirical Bayes shrinkage achieves positive predictive correlation ($r = 0.498$ batting, $r = 0.179$ bowling) and reduces out-of-sample MSE by **22.3% in batting** and **27.7% in bowling** over raw historical rates.
- **Competition Transfer (IPL to T20I and T20I to IPL):**
  - Confirms out-of-sample MSE reductions of 14.5% to 43.1%.
  - Sample-size limitation explicitly reported: only 47 batters and 63 bowlers qualify in both competitions with $\ge 30$ legal pressure balls.

### 5. Probability Calibration & Uncertainty Assessment:
- Brier scores across held-out testing partitions range from 0.2228 to 0.2707 against climatological baselines of 0.2165 to 0.2496.
- Reliability curves confirm appropriate directional ordering across terciles (e.g. peer exceedance observed rates rise from 25% in Low Prob to 70% in High Prob for batting).
- **Formal Ruling:** Exceedance probabilities are **model-derived Bayesian credibility estimates**, NOT empirical match-winning probabilities. High Poisson variance over 30–100 delivery samples precludes sharp empirical calibration.

### 6. Metric Governance Hierarchy:
- **Tier 1 (Authoritative Primary Diagnostic):** Conservative Credible Lower Bound ($\hat{\theta}_{\text{SR}} - 1.0 \times \text{SE}_{\text{post}}$ for batting; $-\hat{\theta}_{\text{Econ}} - 1.0 \times \text{SE}_{\text{post}}$ for bowling runs saved).
- **Tier 2 (Analytical Exploratory):** Composite PRI without TCF.
- **Tier 3 (Heuristic Experimental):** Composite PRI with TCF (tenure filter).
- **Tier 4 (Context Credibility):** Posterior Exceedance Probabilities ($P(\theta > 0)$ and $P(\theta > \mu)$).

---

## 15. Test Verification & Verification Summary

| Test Suite | Files | Test Count | Status | Execution Time |
| :--- | :--- | :---: | :---: | :---: |
| Data QA (R1-01.1) | `test_data_qa.py` | 15 | PASSED | ~4s |
| Match-State Reconstruction (R1-02 to R1-02.3) | `test_match_state.py` | 42 | PASSED | ~18s |
| Pressure Detection (R1-03 to R1-03.1) | `test_pressure_detection.py` | 19 | PASSED | ~12s |
| Expected Performance & Bayesian (R1-04 to R1-04.1) | `test_expected_performance.py` | 20 | PASSED | ~16s |
| Player Pressure Reliability Engine (R1-05) | `test_player_reliability.py` | 15 | PASSED | ~17s |
| Statistical Reliability Audit (R1-05.1) | `test_r1_05_1_statistical_audit.py` | 9 | PASSED | ~7s |
| Statistical Validation Closure (R1-05.2) | `test_r1_05_2_validation_closure.py` | 8 | PASSED | ~6s |
| **Total Round 1 Pressure Tests** | **7 suites** | **128** | **ALL PASSED** | **~55s** |
| Existing Backend Regression Suite | `backend/tests/` | 61 | **ALL PASSED** | **~40s** |
| **Workspace Combined Total** | | **189** | **ALL PASSED** | |
