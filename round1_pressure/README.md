# ROYALS INTELLIGENCE — ROUND 1 PRESSURE ANALYSIS PACKAGE

## 1. Objective & Scope

This package (`round1_pressure/`) is a standalone, isolated analysis module within `royals-intelligence` built specifically for the **SupeRR Selector Season 2 — Round 1** challenge:

> **"Identify the Most Reliable Players Under Pressure"**

The analytical pipeline will generate two independent rankings:
1. **Top 10 Batters Under Pressure**
2. **Top 10 Bowlers Under Pressure**

The analytical methodology will use mathematical modelling, probability theory, statistics, AI/ML, Bayesian reliability, explainability, and sensitivity analysis.

---

## 2. Package Architecture

```text
round1_pressure/
├── config/
│   └── dataset_config.yaml         # Dataset paths, expected schemas, cricket rules, extras code mapping
├── data/
│   ├── raw/                        # Raw competition CSV files (strictly ignored by .gitignore)
│   ├── processed/                  # Normalized match-state Parquet tables (.gitignored)
│   │   ├── delivery_states_strict.parquet
│   │   ├── delivery_states_permissive.parquet
│   │   ├── innings_state_summary.parquet
│   │   ├── match_state_summary.parquet
│   │   ├── match_result_reconciliation.parquet # R1-02.1: 883-match reconciliation audit
│   │   ├── dls_and_revised_overs_audit.parquet # R1-02.1: 34-match shortened/DLS audit
│   │   ├── excluded_innings.parquet
│   │   ├── reconstruction_audit.parquet
│   │   ├── batting_pressure_events_strict.parquet     # R1-03: Batting pressure classifications
│   │   ├── bowling_pressure_events_strict.parquet     # R1-03: Bowling pressure classifications
│   │   ├── batting_pressure_events_permissive.parquet # R1-03: Sensitivity analysis
│   │   ├── bowling_pressure_events_permissive.parquet # R1-03: Sensitivity analysis
│   │   ├── pressure_definition_comparison.parquet     # R1-03: 22 candidate definitions comparison
│   │   └── pressure_coverage_summary.parquet          # R1-03: Match & player coverage metrics
│   └── outputs/                    # QA summary JSON, validation logs, deterministic outputs
├── reports/
│   ├── data_quality_report.md      # Auto-generated comprehensive data audit and domain trap report
│   ├── match_state_reconstruction_report.md # Deterministic match-state reconstruction report (R1-02 & R1-02.1)
│   └── pressure_detection_report.md         # R1-03: Pressure detection & situation classification report
├── src/
│   ├── __init__.py
│   ├── load_qa.py                  # Core DatasetQAEngine profiling and validation class
│   ├── 01_load_qa.py               # Executable deterministic data quality runner script
│   ├── match_state.py              # Core MatchStateEngine delivery-level state reconstruction
│   ├── 02_reconstruct_match_state.py # Executable deterministic match-state reconstruction runner
│   ├── pressure_detection.py       # R1-03: Core PressureDetectionEngine class
│   └── 03_detect_pressure.py       # R1-03: Executable deterministic pressure classification runner
├── tests/
│   ├── test_data_qa.py             # 15 focused pytest test cases validating data integrity and delivery legality
│   ├── test_match_state.py         # 39 focused pytest test cases validating match-state reconstruction & audits
│   └── test_pressure_detection.py  # 22 focused pytest test cases validating pressure rules, audits & invariants
├── requirements.txt                # Lightweight dependencies (pandas, numpy, pyyaml, pytest, pyarrow)
└── README.md                       # Package documentation and usage guide
```

---

## 3. Critical Cricket Domain Findings (R1-01 & R1-01.1)

1. **Extras Code Trap (`extras1_runs`):**
   - In `ball_by_ball.csv`, `extras1_runs` is a **categorical ID code** (1: Overstep, 2: wide, 3: legbyes, 4: byes, 5: other, 6: NONE, 7: Penalty), NOT a numerical run amount.
   - `runs` is strictly runs scored off the bat. Never calculate total runs as `runs + extras1_runs`.
2. **Evidence-Based Delivery Legality & Sequence Verification (R1-01.1):**
   - **Total Deliveries:** 200,999.
   - **Confirmed Legal Extras:** `legbyes` (2,748), `byes` (529), `Penalty` (1) + Standard (189,167) = **192,445**.
   - **Penalty Investigation:** Match 16753, Inn 2, Over 6, Ball 4. Exactly 6 deliveries bowled in over (`over_ball_num` 1–6). Consumed 1 legal ball without re-bowl. Confirmed Legal.
   - **Confirmed Illegal Extras:** `wide` (7,714), `Overstep` (576) = **8,290** (always re-bowled).
   - **Ambiguous Extras (`other` - 264 records):**
     - Delivery styles: 116 beamers (above waist), 72 high full tosses, 16 bouncers, 60 other.
     - Dismissals: 0 bowled, 0 caught, 0 LBW (261 NaN, 3 run outs) — proving batters cannot be caught/bowled on these deliveries under no-ball laws.
     - Sequence behavior: In 253 of 264 overs, the over reached 6 legal balls excluding `other` (re-bowled). In remaining 11 instances, the innings ended early (10 target chased mid-over, 1 Super Over).
     - Status: Retained as explicitly ambiguous rather than forcing an artificial classification.
     - Dual Metrics: **Strict Legal Total: 192,445** vs **Permissive Legal Total: 192,709** (`unresolved_deliveries_count: 264`).
3. **Bowling Attribution & Spelling Normalization:**
   - RunOuts (600), Retire Outs (6), and Obstructing the field (3) must strictly be excluded from bowler wickets and bowling averages.
   - Dataset contains typo `'Obstracting the field'` (2 records) alongside `'Obstructing the field'` (1 record); normalized to 3 total.
   - Unknown dismissal guard rejects any unlisted dismissal type from bowler wicket credit.
   - Total bowler-credited wickets: **10,272** (Bowled: 1,775, Caught: 7,557, LBW: 709, Stump: 214, Hit Wicket: 17).
4. **Super Overs:**
   - Innings 3 (25 deliveries) and Innings 4 (13 deliveries) across 6 matches are Super Overs and must be segregated from standard innings datasets.
5. **Bowling Speed Sensor Anomalies:**
   - 38.7% of deliveries have `bowl_speed == 0.0`. Implausible speeds (`-1.0` kph and up to `1456.1` kph) exist and require sensor filtering before use.
6. **Canonical `player_id` Key:**
   - Exactly 7 player names belong to multiple distinct individuals (e.g. Abdul Samad [SRH Indian batter vs Pakistani international]; Rashid Khan [Afghanistan superstar vs UAE cricketer]).
   - Never merge players on `player_name`. `player_id` is the sole canonical key.

---

## 4. Match-State Reconstruction Governance (R1-02)

1. **Dual Scenarios (Strict vs Permissive):**
   - **Scenario A (Strict):** Treats ambiguous `other` deliveries as illegal/re-bowled. Confirmed legal balls: **192,445**.
   - **Scenario B (Permissive):** Treats ambiguous `other` deliveries as legal for sensitivity analysis. Permissive legal balls: **192,709**.
   - Both scenarios are fully generated as independent Parquet tables with explicit `state_before` and `state_after` for all variables.
2. **Scope Segregation:**
   - **Primary Analysis Scope:** 193,988 deliveries across IPL (2022–2026) and Senior T20I (2022–2026) ordinary innings.
   - **Excluded Tournaments:** 30 matches (6,985 deliveries) from Emerging Teams Asia Cup 2024 and Rising Stars 2025.
   - **Excluded Super Overs:** 38 deliveries across 6 matches.
   - **Abandoned Matches:** 16 matches with 0 deliveries.
   - All exclusions are cataloged in `excluded_innings.parquet`.
3. **Score Completeness Governance:**
   - Innings with zero unconfirmed extras (or exact mathematical match) are flagged `EXACT` (329 innings).
   - Innings with unconfirmed extras (byes, legbyes, penalty) are flagged `LOWER_BOUND_ONLY` (1,395 innings).
   - Valid partial metrics (batter runs, bowler wickets, balls bowled, balls remaining) are fully preserved without fabricating synthetic runs.
4. **Chase & DLS Rules:**
   - 23 matches with official revised DLS targets use the verified `revised_target` from `matches.csv`.
   - Ordinary 2nd innings use `target = first_innings_total + 1`.
   - 34 shortened matches use verified scheduled balls (e.g. 30, 48, 66, 90 balls).

---

## 5. Match-State Integrity Audit & Targeted Remediation (R1-02.1)

1. **Score Disentanglement & Strict Withholding:**
   - Cumulative team scores are segregated into `cumulative_team_runs_lower_bound` (always populated) and `cumulative_team_runs_exact` (strictly `null` on `LOWER_BOUND_ONLY` innings).
   - Lower-bound scores are NEVER exposed as exact scores to downstream models.
   - On `LOWER_BOUND_ONLY` innings, `runs_required_exact` and `required_run_rate_exact` are strictly withheld (`null`) to eliminate false precision.
   - Robust bounding metrics (`runs_required_upper_bound` and `required_run_rate_upper_bound`) remain available for all innings.
2. **Empirical Inference Status of `extras_2_runs`:**
   - Non-zero on exactly 36 of 200,999 deliveries (0.018%). In all 36 deliveries, `runs == 0` and values are 1 (19 times) or 4 (17 times) on no-balls/beamers.
   - Explicitly categorized as an **empirical inference**, rather than an official schema standard, preserving documented uncertainty for downstream models.
3. **Match-Result Reconciliation Across All 883 Matches:**
   - Documented critical schema limitation: `matches.csv` contains NO independent official innings score fields (`inn1_runs`, `inn2_runs`). Only text `result` (margins in runs or wickets).
   - Categorized all 883 matches cleanly into 7 mutually exclusive groups in `match_result_reconciliation.parquet`:
     - `WICKET_WIN_NO_OFFICIAL_TOTAL_IN_SCHEMA`: 394 matches
     - `INCOMPLETE_EXTRAS_RUN_WIN`: 382 matches
     - `NO_RESULT_OR_ABANDONED`: 40 matches
     - `OTHER_RESULT` (Ties/Super Overs): 30 matches
     - `DLS_REVISED_TARGET`: 26 matches
     - `EXACT_BOTH_INNS_MARGIN_MISMATCH`: 6 matches (1–4 run discrepancies from unrecorded multi-run extras)
     - `EXACT_BOTH_INNS_MARGIN_MATCH`: 5 matches (exact margin match)
4. **Revised Overs & DLS Audit Across All 34 Shortened Matches:**
   - Verified that `first_inn_revised_overs` and `second_inn_revised_overs` store **legal balls** (integers divisible by 6, range 30 to 114 balls).
   - All 23 `revised_target` matches apply exclusively to **Innings 2** (the chase).
   - Cataloged in `dls_and_revised_overs_audit.parquet`.
5. **Strict vs. Permissive Reconciliation (The 5 Out-of-Scope Records):**
   - Exactly 264 deliveries with `extras_type == 'other'` across entire dataset; 259 are in primary scope.
   - The remaining 5 are accounted for: 3 in Emerging Teams Asia Cup 2024 (Matches 37088, 37090, 37093), 1 in Asia Cup Rising Stars 2025 (Match 48015), and 1 in IPL 2025 Super Over (Match 40725, Innings 3).
6. **Downstream Feature-Eligibility Contract (R1-03 Transition):**
   - **Tier 1 (Safe for All Deliveries):** Striker runs, legal balls bowled/faced, wickets, bowler attribution, balls remaining, match metadata, phase.
   - **Tier 2 (Score-Dependent):** `runs_required_exact`, `required_run_rate_exact`, `cumulative_team_runs_exact` (restricted strictly to `EXACT` score subsets; models on partial matches must use bounded intervals).
   - **Tier 3 (Uncertain / Sensitivity Required):** Multi-run byes/legbyes, penalty amounts, ambiguous `other` deliveries (must evaluate Strict vs Permissive scenarios).

---

## 6. Match Metadata Flags vs. Mutually Exclusive Categories (R1-02.2 & R1-02.3)

1. **Separation of Non-Exclusive Metadata Flags from Match Categories:**
   - **`flag_revised_target_recorded` (23 matches):** Matches with explicit `revised_target > 0` in `matches.csv` (includes Match 17765).
   - **`flag_revised_overs_recorded` (34 matches):** Matches with explicit revised overs metadata.
   - **`flag_dls_method_in_result_text` (19 matches):** Matches whose `result` text contains `'D/L'` or `'DLS'`.
   - **`flag_dls_target_applicable` (22 matches):** Matches where positive revised target was applicable to a concluded chase (excludes Match 17765).
   - **`flag_dls_status_unresolved` (4 matches):** Matches 20182, 23674, 24822, 28334 (DLS stated in result, target/overs omitted).
   - **`flag_match_abandoned` (40 matches):** Matches ending in 'No Result' or 'Match Abandoned' (including Match 17765 and 16 zero-delivery matches).
2. **Exactly One Mutually Exclusive Category per Match (Sums to Exactly 883):**
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

---

## 7. Pressure Detection & Situation Classification Engine (R1-03)

Task R1-03 delivers a reproducible, evidence-driven Pressure Detection Engine that identifies high-pressure match situations independently for batters and bowlers without introducing subjective weights or performance outcome leakage.

### 1. Architectural Principles:
1. **Discipline Independence & Tactical Asymmetry:**
   - Batting and bowling pressure situations are modeled independently.
   - Tactical asymmetry is rigorously respected:
     - *Death overs with $\ge 6$ wickets in hand:* **HIGH pressure for bowler** (boundary assault hazard), but **LOW pressure for batter** (freedom to attack with abundant wickets).
     - *Powerplay with 3 wickets lost:* **HIGH pressure for batter** (collapse salvage required), but **LOW pressure for bowler** (attacking dominance with huge margin for error).
2. **Zero Outcome Leakage:**
   - Pressure classification strictly evaluates match context *before* the delivery occurs (`state_before`).
   - Outcome variables (`runs`, `is_wicket`, `delivery_bowler_conceded_runs`, `dismissals`, `extras`) are strictly forbidden from pressure rules.
3. **Score Uncertainty Contract Enforcement:**
   - Where cumulative score is `LOWER_BOUND_ONLY` or DLS target is unrecorded, exact RRR is strictly withheld (`null`).
   - Deliveries retain transparent metadata flags: `dimensions_available` and `dimensions_withheld`.
   - Score-independent structural dimensions (`PHASE`, `BALLS_REM`, `WKTS_REM`, `LEGAL_BALLS`) provide complete, uncorrupted match-state pressure detection across all 193,988 primary deliveries.
4. **Primary Analysis Scope Segregation:**
   - Evaluates Senior Men's T20 cricket (IPL & Senior T20I, comps 2673, 2674, 2675; innings 1 & 2; 193,988 primary deliveries).
   - Super Overs (38 deliveries) and Emerging Tournaments (6,985 deliveries) are classified with explicit reasons and excluded from primary pressure rankings.

### 2. Empirical Quantile Benchmarks:
- **Chase RRR Distribution (Exact Subset, N = 6,748):**
  - 50th percentile (Median): 9.64
  - 75th percentile: 11.48 ($\approx 11.5$)
  - 85th percentile: 12.99 ($\approx 13.0$)
  - 90th percentile: 14.35 ($\approx 14.5$)
- **Structural Collapses & Leverage Points:**
  - `BAT_COLLAPSE_EARLY_W3`: $\ge 3$ wickets lost in Powerplay represents top 6.2% most severe top-order collapses (3,797 deliveries, 336 matches).
  - `BAT_DEPLETED_WICKETS_W3`: $\le 3$ wickets in hand in Middle/Death represents top 9.7% most depleted states (12,921 deliveries, 619 matches).
  - `BAT_DEATH_ACCEL_W5`: Death overs with $\le 5$ wickets in hand (26,130 deliveries, 774 matches).
  - `BOWL_ASSAULT_HIGH_WICKETS_DEATH`: Death overs with $\ge 6$ batting wickets in hand (17,373 deliveries, 667 matches).
  - `BOWL_DEATH_FINAL18`: Overs 18–20 final 18 balls high leverage (24,729 deliveries, 811 matches).
  - `BOWL_PP_DAMAGE_CONTROL_W0`: Overs 5–6 with 0 wickets lost (4,860 deliveries, 443 matches).

### 3. Primary Candidate Definitions & Inclusion-Exclusion Union:
- **Batting Primary Definition (`BAT_COMPOSITE_HIGH`):**
  - Captures **33,005** deliveries (17.01% of primary scope) across **692** unique batters and **794** matches.
  - Formulated as the 4-component union:
    $$\text{BAT\_COMPOSITE\_HIGH} = \text{CHASE\_P85} \lor \text{COLLAPSE\_W3} \lor \text{DEPLETED\_W3} \lor \text{DEATH\_ACCEL\_W5}$$
  - Exact Inclusion-Exclusion: $\sum S_1 (43,859) - \sum S_2 (10,982) + \sum S_3 (128) - S_4 (0) = 33,005$.
  - Phase breakdown: Death = 26,185, Powerplay = 3,924, Middle = 2,896.
- **Bowling Primary Definition (`BOWL_COMPOSITE_HIGH`):**
  - Captures **39,436** deliveries (20.33% of primary scope) across **480** unique bowlers and **822** matches.
  - Formulated as the 4-component union:
    $$\text{BOWL\_COMPOSITE\_HIGH} = \text{ASSAULT\_DEATH} \lor \text{FINAL18} \lor \text{PP\_W0} \lor \text{DEF\_P85}$$
  - Exact Inclusion-Exclusion: $\sum S_1 (47,110) - \sum S_2 (7,718) + \sum S_3 (44) - S_4 (0) = 39,436$.
  - Phase breakdown: Death = 34,576, Powerplay = 4,860, Middle = 0.
- **Strict vs Permissive Sensitivity (Event-Level Investigation):**
  - Batting: 0 deliveries difference (**0.000% variance**; 100% invariant).
  - Bowling: 80 deliveries difference (**0.041% variance**; < 0.1% threshold) occurring strictly on cumulative legal ball boundary transitions: (1) 72 balls in Over 17 crossing `balls_remaining_before <= 18` (`BOWL_DEATH_FINAL18`) one delivery earlier in Permissive mode; and (2) 8 balls in Over 4 crossing `legal_balls_bowled_before >= 24` (`BOWL_PP_DAMAGE_CONTROL_W0`) one delivery earlier in Permissive mode.

### 4. Population & Score Completeness Reconciliation (R1-03.1):
- **Population Reconciled:** 200,999 total raw deliveries = 193,988 primary scope deliveries + 7,011 excluded deliveries (6,985 Emerging + 26 Senior Super Overs).
- **Legal Deliveries Reconciled:** Within primary scope (193,988 bowled), Strict legal is 185,692 (with 8,296 illegal balls); Permissive legal is 185,951 (with 8,037 illegal balls). The 259 difference represents ambiguous `other` deliveries.
- **Score Completeness Reconciled:** 193,988 primary deliveries = 86,905 EXACT score + 107,083 LOWER_BOUND_ONLY score.
- **Exact Chase Reconciled:** Exact RRR is available on exactly 6,748 chase deliveries (both target exact and score exact). In all other 187,240 deliveries, exact chase metrics are strictly withheld (`null`).

---

## 8. Expected Performance Baselines & Bayesian Reliability Foundation (R1-04)

### 1. Stratified Ordinary Baselines (12 Cells):
To establish true player skill differentials under pressure, expected performance is measured against ordinary (non-pressure) deliveries partitioned into 12 mutually exclusive context cells:
$$\text{Cell} = \text{comp\_tier (IPL, T20I)} \times \text{innings (1, 2)} \times \text{innings\_phase (Powerplay, Middle, Death)}$$
- **Batting Baseline Population:** 154,529 legal ordinary deliveries (83.2% of primary scope).
- **Bowling Baseline Population:** 148,678 legal ordinary deliveries (80.1% of primary scope).
- **Independence:** Batting and bowling baselines are independently computed and never co-mingled.

### 2. Simpson's Paradox Discovery in Pressure Batting:
- Raw ordinary strike rate is **139.7**, while raw pressured strike rate is **140.9** (+1.2 SR points).
- **The Paradox:** Naive unstratified analysis suggests batters hit faster under pressure.
- **The Reality:** 79.3% of pressure deliveries occur in the Death phase, where the ordinary baseline strike rate is **176.5**.
- **Within-Phase Degradation Under Pressure:**
  - Death Phase: Strike rate plunges from **176.5 to 149.2** (-27.3 points; 15.5% drop).
  - Middle Phase: Strike rate plunges from **134.3 to 104.3** (-30.0 points; 22.3% drop).
  - Powerplay Phase: Strike rate plunges from **137.2 to 113.3** (-23.9 points; 17.4% drop).
- **Context-Weighted Expectation:** Each player's expected performance under pressure is weighted by their exact delivery allocation across the 12 cells:
  $$E[M_i] = \sum_{c \in \text{Cells}} w_{i,c} \cdot B_{c,M}$$
  This completely removes phase-distribution bias and guarantees unbiased differential measurement.

### 3. Bowling Degradation Under Pressure:
- Ordinary overall economy is **7.98 RPO**, jumping to **10.07 RPO** under pressure (+2.08 RPO increase in runs conceded).
- Powerplay Overs 5–6 with 0 wickets lost: Economy jumps from **7.95 to 10.33 RPO** (+2.38 RPO).
- Death overs: Economy jumps from **7.98 to 10.03 RPO** (+2.05 RPO).

### 4. Hierarchical Empirical Bayes Shrinkage (DerSimonian-Laird):
Observed sample differentials $y_i = \text{Observed}_i - E[M_i]$ are separated into true talent differentials and sampling noise using empirical Bayes shrinkage:
$$\theta_i = r_i y_i + (1 - r_i) \mu, \quad r_i = \frac{\tau^2}{\tau^2 + \sigma_i^2}$$
- **Batting Strike Rate Differential:**
  - Prior Population Mean $\mu = -34.24$ SR points.
  - Between-Player Variance $\tau^2 = 1,084.89$ ($\tau = 32.94$ SR points).
  - Minimum sample qualification: $\ge 30$ legal balls under pressure (278 qualified batters of 691).
  - Median reliability $r_i = 0.747$ (range: 0.436 to 0.955).
- **Bowling Economy Differential:**
  - Prior Population Mean $\mu = +1.82$ RPO.
  - Between-Player Variance $\tau^2 = 0.59$ ($\tau = 0.77$ RPO).
  - Minimum sample qualification: $\ge 30$ legal balls under pressure (239 qualified bowlers of 479).
  - Median reliability $r_i = 0.296$ (range: 0.088 to 0.841). Bowling economy has substantially higher noise per ball, requiring greater shrinkage toward the population mean.

### 5. Chronological Out-of-Sample Validation & Statistical Audit (R1-04.1):
- Model trained strictly on past seasons **2022–2024** (111,323 legal balls); tested on future seasons **2025–2026** (74,369 legal balls). Zero future leakage into historical posteriors.
- **Transparent Baseline Comparison:**
  - Zero baseline MSE: Batting 1,926.65; Bowling 7.56.
  - Population mean MSE: Batting 1,496.11; Bowling 2.85.
  - Raw historical MSE: Batting 1,240.03; Bowling 4.57.
  - Shrunk posterior MSE: Batting 994.00 (**+19.8% reduction**, $p = 0.0151$); Bowling 2.77 (**+39.4% reduction**, $p = 0.0052$).
  - Cluster-robust MSE: Batting 936.79 (**+24.5% reduction** over raw).
- **Audit Findings:** Match-level clustering causes mild standard error inflation (+8.6% batting, +13.6% bowling). Conditioning on severe wickets in ordinary baselines causes a common-support violation (12 empty cells). 30-ball qualification threshold isolates 96.4%+ pressure volume with stable hyperparameters.
- Detailed audit report: `round1_pressure/reports/expected_performance_audit_report.md`.

### 6. Strict Scope Boundary Invariant:
No player rankings, Top 10 lists, or composite pressure index $\Psi$ are constructed in R1-04 or R1-04.1.

---

## 9. Explainable Player Pressure Reliability Scoring Engine (R1-05)

### 1. Objective & Methodological Governance:
Task R1-05 implements an explainable, statistically grounded player pressure reliability scoring engine to answer the SupeRR Selector Season 2 — Round 1 challenge: *Identify the Most Reliable Players Under Pressure*.
- **Populations Evaluated:** 691 batters (278 qualified $\ge 30$ pressure balls) and 479 bowlers (239 qualified $\ge 30$ pressure balls).
- **Two-Way All-Rounder Overlap:** Exactly 139 players qualify in both disciplines.
- **Core Principle:** Players are evaluated without naive unstratified rankings. True reliability combines **context-adjusted execution**, **hierarchical Empirical Bayes shrinkage**, **posterior estimation uncertainty (credible intervals)**, and **cross-season temporal stability**.

### 2. Candidate Scoring Formulations:
To guarantee transparent explainability and evaluate sensitivity to model choice, five distinct statistical scoring formulations were implemented:
1. **Conservative Credibility Bound (Value-at-Risk, 84.1% One-Sided Lower Bound):**
   - Batting: $\text{Score}_{\text{bat, cons}} = \hat{\theta}_{i, \text{SR}} - 1.0 \times \text{SE}_{\text{post}, i}$ (SR points above ordinary baseline).
   - Bowling: $\text{Score}_{\text{bowl, cons}} = -\hat{\theta}_{i, \text{Econ}} - 1.0 \times \text{SE}_{\text{post}, i}$ (Runs saved per over relative to ordinary baseline).
2. **Conservative 95% One-Sided Lower Bound:**
   - Evaluates worst-case performance under 95% credibility: $\hat{\theta} - 1.645 \times \text{SE}_{\text{post}}$.
3. **Posterior Exceedance Probability vs Ordinary Baseline:**
   - Batting: $P(\theta_i > 0 \mid y) = \Phi\left(\frac{\hat{\theta}_{i, \text{SR}}}{\text{SE}_{\text{post}, i}}\right)$ (Probability of maintaining ordinary strike rate under pressure).
   - Bowling: $P(\theta_i < 0 \mid y) = \Phi\left(\frac{-\hat{\theta}_{i, \text{Econ}}}{\text{SE}_{\text{post}, i}}\right)$ (Probability of outperforming ordinary economy under pressure).
4. **Posterior Exceedance Probability vs Pressured Peers:**
   - Batting: $P(\theta_i > \mu_{\text{bat}} \mid y) = \Phi\left(\frac{\hat{\theta}_{i, \text{SR}} - \mu_{\text{bat}}}{\text{SE}_{\text{post}, i}}\right)$ where $\mu_{\text{bat}} = -34.24$ SR pts.
   - Bowling: $P(\theta_i < \mu_{\text{bowl}} \mid y) = \Phi\left(\frac{\mu_{\text{bowl}} - \hat{\theta}_{i, \text{Econ}}}{\text{SE}_{\text{post}, i}}\right)$ where $\mu_{\text{bowl}} = +1.82$ RPO.
5. **Multi-Dimensional Composite Pressure Reliability Index ($\text{PRI} \in [0, 100]$):**
   - Integrates primary scoring/containment ($45\%$), boundary hazard control ($20\%$), dot-ball control ($20\%$), and dismissal/wicket threat ($15\%$), scaled by a **Temporal Consistency Factor (TCF)**:
     $$\text{TCF}_i = \left(\frac{\min(S_i, 4)}{4}\right)^{0.35} \times \left(1 - 0.25 \times \min\left(1.0, \frac{\sigma_{\text{season}, i}}{\text{Scale}_\sigma}\right)\right)$$

### 3. Pairwise Methodological Agreement:
Pairwise Spearman rank correlations demonstrate outstanding consistency across candidate scoring formulations:
- Batting: Correlations between Conservative Lower Bound, 95% Bound, Exceedance Probabilities, and Composite PRI range from **0.884 to 0.995**.
- Bowling: Correlations between Conservative Runs Saved and Composite PRI range from **0.781 to 0.990**.
- Bowling Floor Effect: Evaluating bowlers against ordinary baseline ($P(\theta < 0)$) suffers from floor clustering (only Jasprit Bumrah has $\hat{\theta} < 0$), whereas evaluating against pressured peers ($P(\theta < \mu)$) or using Conservative Runs Saved provides smooth, robust differentiation.

### 4. Key Diagnostic Profiles:
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
- **Two-Way All-Rounders ($N = 139$):**
  - Discloses both Harmonic Mean (penalizes imbalance) and Arithmetic Mean:
  - Top performers: Sunil Narine (Harmonic PRI: 77.2; Bat PRI 90.5, Bowl PRI 67.3), Ravindra Jadeja, Rashid Khan, Romario Shepherd, Andre Russell, Axar Patel, Sam Curran.

### 5. Strict Governance & Exclusions:
- **No Auction or Squad Optimization:** No player prices, auction values, purse optimization, team optimizers, or API alterations.
- **No Unstratified Definitive Top 10:** Results are presented as diagnostic reliability profiles with full estimation uncertainty (credible intervals) and explainability records.

---

## 10. Execution & Verification Commands

### Run Data QA (R1-01.1):
```bash
python round1_pressure/src/01_load_qa.py
pytest round1_pressure/tests/test_data_qa.py -v
```

### Run Match-State Reconstruction & Integrity Audits (R1-02, R1-02.1, R1-02.2 & R1-02.3):
```bash
python round1_pressure/src/02_reconstruct_match_state.py
pytest round1_pressure/tests/test_match_state.py -v
```

### Run Pressure Detection & Classification Engine (R1-03 & R1-03.1):
```bash
python round1_pressure/src/03_detect_pressure.py
pytest round1_pressure/tests/test_pressure_detection.py -v
```

### Run Expected Performance & Bayesian Shrinkage Engine (R1-04 & R1-04.1):
```bash
python round1_pressure/src/04_expected_performance.py
pytest round1_pressure/tests/test_expected_performance.py -v
```

### Run Explainable Player Pressure Reliability Engine (R1-05):
```bash
python round1_pressure/src/05_player_reliability.py
pytest round1_pressure/tests/test_player_reliability.py -v
```

### Run Full Round 1 Test Suite (All 111 Pressure Tests):
```bash
pytest round1_pressure/tests -v
```
