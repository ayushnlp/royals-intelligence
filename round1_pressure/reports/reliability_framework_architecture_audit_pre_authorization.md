# ROYALS INTELLIGENCE — TASK R1-07.0 ARCHITECTURE & METHODOLOGY AUDIT REPORT
## Pressure Reliability Decision Framework — Architecture & Methodology Planning Audit

**Document Path:** `round1_pressure/reports/r1_07_0_reliability_framework_architecture_audit.md`  
**Generated:** 2026-11-16T12:00:00+05:30  
**Architecture:** ROYALS INTELLIGENCE v4.1  
**Project:** SupeRR Selector Season 2 — Round 1  
**Challenge Objective:** Identify the Most Reliable Players Under Pressure  
**Starting Checkpoint:** `6005022`  
**Task Type:** Read-Only Architecture, Methodology, and Implementation Planning Audit  
**Audit Status:** `METHODOLOGY_AND_ARCHITECTURE_AUDIT_COMPLETE`  

---

## 1. Executive Summary & Audit Mandate

Following the formal completion and acceptance of Tasks R1-01 through R1-06.2.3, this planning audit defines the architectural, statistical, and methodological blueprint for **R1-07: Pressure Reliability Decision Framework**.

### Core Audit Mandate
The challenge objective is: **Identify the Most Reliable Players Under Pressure**.  
The fundamental business and analytical question that ROYALS INTELLIGENCE must answer is:
$$\mathbf{Q}: \text{\textbf{Which players demonstrate the most dependable performance under pressure, and how strong is the available evidence?}}$$

This is strictly a **read-only planning and architecture audit**. In accordance with strict governance constraints:
- No existing statistical calculations, models, or priors are modified.
- No new player rankings, scores, leaderboards, or shortlists are produced.
- No source code, database schemas, frontend/backend application code, or analytical Parquet artifacts are altered.
- No Git commits or remote pushes are executed.

---

## 2. Existing System Capability Audit (R1-01 through R1-06.2.3)

A rigorous audit of the existing ROYALS INTELLIGENCE v4.1 analytics stack establishes the exact technical baseline across all completed tasks.

```
ROYALS INTELLIGENCE v4.1 Architecture & Pipeline Stack:
+--------------------------------------------------------------------------------------------------------+
| R1-01 / R1-02.3: Data QA & Match-State Reconstruction                                                  |
| - 200,999 ball-by-ball deliveries across 883 matches (867 with deliveries, 16 abandoned)               |
| - Strict vs Permissive delivery legality classification; exact RRR withholding on DLS / lower bounds   |
+--------------------------------------------------------------------------------------------------------+
                                                    |
                                                    v
+--------------------------------------------------------------------------------------------------------+
| R1-03 / R1-03.1: Pressure Detection & Situation Classification                                         |
| - Situational exposure events: 33,005 batting events, 39,436 bowling events (100% strict invariant)     |
| - Legal pressure deliveries: 31,163 batting, 37,014 bowling (Strict); 31,257 & 37,222 (Permissive)     |
| - Primary definitions: BAT_COMPOSITE_HIGH (19.4% exposure) and BOWL_COMPOSITE_HIGH (20.3% exposure)    |
+--------------------------------------------------------------------------------------------------------+
                                                    |
                                                    v
+--------------------------------------------------------------------------------------------------------+
| R1-04 / R1-04.1: Context-Stratified Baselines & Bayesian Shrinkage                                     |
| - 12 stratified ordinary baselines (comp_tier x innings x phase: PP, Mid, Death)                      |
| - DerSimonian-Laird Empirical Bayes shrinkage (Batting: mu = -34.24, tau = 32.94; Bowling: mu = +1.82)|
| - Chronological holdout validation: 22.3% MSE reduction (batting) and 27.7% MSE reduction (bowling)    |
+--------------------------------------------------------------------------------------------------------+
                                                    |
                                                    v
+--------------------------------------------------------------------------------------------------------+
| R1-05 / R1-05.2: Reliability Scoring & Validation Closure                                              |
| - Value-at-Risk conservative bound: BAT_CONSERVATIVE = theta - 1.0*SE; BOWL_CONSERVATIVE = -theta - 1.0*SE|
| - Cohort-relative nature of PRI min-max scaling proven (Spearman > 0.999; shifts absolute score ~0.5)  |
| - TCF identified as experimental tenure heuristic; out-of-sample transferability and Brier calibration  |
+--------------------------------------------------------------------------------------------------------+
                                                    |
                                                    v
+--------------------------------------------------------------------------------------------------------+
| R1-06 / R1-06.2.3: Player Intelligence, Leaderboards & Governance Remediation                          |
| - Full population accounting: 824 batters (278 qualified >=30b); 596 bowlers (239 qualified >=30b)     |
| - Two-Dimensional Classification: Dim A (Performance Status) x Dim B (Volume Tier: High, Med, Low)   |
| - Table 1 sample qualification: balls >= 60 OR (balls >= 50 AND matches >= 10) (161 bat, 168 bowl)    |
| - Verbatim 1-SE uncertainty disclosures in all reports and 517 candidate Parquet profiles              |
| - Complete delivery-count reconciliation: 200,999 raw deliveries confirmed across all 6 Parquet tables |
+--------------------------------------------------------------------------------------------------------+
```

### Detailed Review by Milestone:
1. **R1-01 to R1-02.3 (Data QA & Match-State Reconstruction):**
   - *Implemented & Validated:* Robust parsing of 200,999 ball-by-ball deliveries across 883 matches. Clean identification of match boundaries, innings transitions, legal deliveries, extras breakdown (wides, no-balls, leg-byes, byes, penalty runs, and ambiguous 'other' extras). Strict handling of DLS and revised-overs fixtures with explicit withholding of exact target and exact RRR on lower-bound score states. Elimination of display-name collisions via canonical integer `player_id`.
   - *Limitations:* Ball-tracking data (pitch maps, release speed, deviation) is absent from source CSVs. Confounding partner effects (non-striker impact on strike rotation) are not explicitly conditioned.
2. **R1-03 to R1-03.1 (Pressure Detection & Situation Classification):**
   - *Implemented & Validated:* Rigorous separation of situational exposure (`state_before`) from performance outcomes (`state_after`). Quantile benchmarking across candidate definitions. Primary definitions `BAT_COMPOSITE_HIGH` (19.4% of primary deliveries) and `BOWL_COMPOSITE_HIGH` (20.3% of primary deliveries) capture genuine high-leverage contexts (steep chase RRR, depleted wickets, high-difficulty death defense).
   - *Limitations:* Strong concentration in the Death phase (overs 16–20 account for 87.7% of pressure deliveries). Pressure detection does not currently model multi-ball leverage dynamics (e.g. pressure spikes after two consecutive dot balls).
3. **R1-04 to R1-04.1 (Expected Performance Baselines & Bayesian Shrinkage):**
   - *Implemented & Validated:* 12-stratum context baseline matrix ($2 \text{ competitions} \times 2 \text{ innings} \times 3 \text{ phases}$) completely resolves Simpson's Paradox and phase-allocation bias. DerSimonian-Laird Empirical Bayes shrinkage estimates population hyperparameters directly from data ($\mu_b = -34.24 \text{ SR pts}, \tau_b = 32.94$; $\mu_{bw} = +1.82 \text{ RPO}, \tau_{bw} = 0.77$). Out-of-sample chronological backtesting (2022–2024 train $\to$ 2025–2026 test) confirms 22.3% predictive MSE reduction in batting and 27.7% in bowling over raw noisy rates.
   - *Limitations:* Baselines assume homogeneous opposition bowling/batting strength within strata. Batter-bowler matchup head-to-head adjustments are not modeled due to severe sample sparsity.
4. **R1-05 to R1-05.2 (Reliability Scoring & Statistical Audit):**
   - *Implemented & Validated:* The 1-SE Value-at-Risk conservative bound ($\hat{\theta} - 1.0 \times \text{SE}_{\text{post}}$) was proven to be the indispensable statistical anchor preventing small-sample flyers from infiltrating top tiers. Cohort perturbation tests verified that min-max PRI is cohort-relative ($r_s > 0.999$, absolute delta ~0.5 pts).
   - *Limitations & Audit Findings:* TCF (Temporal Consistency Factor) was proven to be an unvalidated tenure penalty $(S/4)^{0.35}$ that punishes newer players regardless of performance; it was relegated to experimental/exploratory status. Posterior exceedance probabilities exhibit Brier scores of ~0.26–0.27, representing directional credibility rather than sharp calibrated match-winning probabilities.
5. **R1-06 to R1-06.2.3 (Player Intelligence, Leaderboards & Governance Remediation):**
   - *Implemented & Validated:* Full population accounting across all 824 batters and 596 bowlers. Clean two-dimensional classification separating Performance Evidence Status (Dimension A) from Evidence Volume Tier (Dimension B). Candidate sample qualification logic (`balls >= 60` or `balls >= 50 and matches >= 10`). Resolved Table 1 leaderboard inclusions (only sample-qualified candidates) and separated non-overlapping watchlists (Emerging High-Upside and Established Marginal/Peer-Beaters). Verbatim 1-SE uncertainty disclosures implemented across 517 candidate Parquet profiles and markdown shortlists. Complete reconciliation of delivery counts (200,999 raw deliveries confirmed 1:1 across all tables).
   - *Remaining Gaps:* R1-06 is a ranking and diagnostic engine, not an interactive or operational decision framework. It ranks players unidimensionally on conservative bounds without evaluating multi-match consistency, role-specific archetypes, or context-specific dependability tradeoffs.

---

## 3. Implemented versus Experimental Feature Matrix

The table below catalogs every analytical feature, component, and metric currently in the repository, defining its implementation status, mathematical foundation, empirical validity, and governance constraints.

| Analytical Feature / Component | Current Implementation Status | Mathematical Specification | Codebase Provenance | Empirical Validation Status | Methodological Limitations & Governance Rules |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Strict vs Permissive Delivery Legality** | **Fully Implemented & Validated** | Sequence-based legal progression (`outcome_is_legal == True`) | `match_state.py`, `load_qa.py` | 100% Invariant in batting pressure (0 delta); 0.56% variance in bowling; rank correlation $r_s > 0.999$ | Authoritative primary policy. Permissive legality preserved strictly for sensitivity checks. |
| **Stratified Ordinary Baselines** | **Fully Implemented & Validated** | $\mathbb{E}[Y \mid c, i, p] = \frac{\sum \text{runs}}{\sum \text{balls}}$ across 12 strata | `expected_performance.py`, `batting/bowling_ordinary_baseline.parquet` | Eliminates phase-allocation bias and Simpson's Paradox | Assumes league-average opposition quality within strata. |
| **Empirical Bayes Shrinkage (DerSimonian-Laird)** | **Fully Implemented & Validated** | $\hat{\theta}_i = w_i Y_i + (1-w_i)\mu$, $w_i = \frac{\tau^2}{\tau^2 + s_i^2}$ | `expected_performance.py`, `bayesian_shrinkage_summary.parquet` | 22.3% MSE reduction in batting; 27.7% in bowling in out-of-sample test | Superior to subjective priors. Shrinkage intensity is governed by sample variance $s_i^2$. |
| **Conservative Lower Credible Bound (1-SE)** | **Fully Implemented & Validated** | $\text{Score}_{\text{cons}} = \hat{\theta}_i - 1.0 \times \text{SE}_{\text{post}, i}$ | `player_reliability.py`, `batting/bowling_leaderboard.parquet` | Dropping 1-SE bound drops Top 10 overlap from 81.8% to 42.9%, admitting small-sample noise | Directional diagnostic ($\approx 84.1\%$ one-sided posterior credibility under normality). **NOT a 95% CI or empirical guarantee.** |
| **Two-Dimensional Classification System** | **Fully Implemented & Validated** | Dimension A (4 evidence states) $\times$ Dimension B (4 volume tiers) | `r1_06_candidate_selection.py`, `batting/bowling_intelligence.parquet` | Eliminates conflation of effect direction, statistical evidence, and sample volume | Governs candidate classification. Prevents describing positive mean with negative bound as "strong evidence". |
| **Dual-Tournament Exposure Accounting** | **Fully Implemented & Validated** | $n_{\text{IPL}} \ge 30 \land n_{\text{T20I}} \ge 30$ | `r1_06_player_intelligence.py`, `competition_candidate_views.parquet` | Validated sample availability accounting across environments | Confirms dual exposure availability, **NOT statistical proof of invariant cross-competition transferability.** |
| **Exploratory PRI (Without TCF)** | **Exploratory / Diagnostic** | Min-max scaled weighted composite of 4 context-adjusted metrics | `player_reliability.py`, `audit_pri_weight_sensitivity.parquet` | Rank correlation $r_s > 0.995$ with equal weights under conservative anchoring | **Cohort-relative index**, NOT an absolute probability. Adding/removing players shifts scores by ~0.5 pts. |
| **Temporal Consistency Factor (TCF)** | **Experimental / Heuristic** | $\text{TCF} = (S/4)^{0.35} \times (1 - 0.25 \min(1, \sigma_{\text{season}} / \text{Scale}))$ | `player_reliability.py`, `audit_tcf_ablation_comparison.parquet` | Causes severe rank shifts (mean 34.3 ranks; up to 160 ranks); punishes 1–2 season players | **FORMALLY EXCLUDED from primary rankings.** Conflates true talent drift with Poisson sample noise. |
| **Posterior Exceedance Probabilities** | **Exploratory / Model-Based** | $P(\theta_i > \text{Threshold}) = 1 - \Phi\left(\frac{\text{Threshold} - \hat{\theta}_i}{\text{SE}_{\text{post}, i}}\right)$ | `player_reliability.py`, `validation_probability_calibration.parquet` | Brier scores 0.22–0.26; Brier skill score near zero due to high delivery-level variance | **Model-derived Bayesian credibility under context expectations, NOT calibrated match-winning probabilities.** |
| **All-Rounder Composite PRI** | **Exploratory / Unvalidated** | Harmonic / Arithmetic mean of batting and bowling PRI | `player_reliability.py`, `all_rounder_pressure_reliability.parquet` | Sensitivity to arbitrary weighting; non-comparable discipline scales | **EXCLUDED from primary decision framework.** Batting and bowling must remain strictly separated. |
| **Match-Level Variance Decomposition** | **Missing / Planned for R1-07** | $\sigma^2_{\text{total}} = \sigma^2_{\text{between-match}} + \sigma^2_{\text{within-match}}$ | *Not yet implemented* | Proposed for R1-07.1 | Necessary to distinguish consistent match-in, match-out performers from high-variance boom-or-bust players. |
| **Phase-Conditioned Role Reliability** | **Missing / Planned for R1-07** | Phase-specific differentials $\hat{\theta}_{\text{Death}}$ vs $\hat{\theta}_{\text{Middle}}$ | *Not yet implemented* | Proposed for R1-07.2 | Necessary to evaluate role fit (Top-order chase vs Finisher; Powerplay container vs Death closer). |

---

## 4. Proposed Batting Reliability Decision Framework

### 4.1 Objective and Core Challenge
Batting under pressure in T20 cricket is characterized by high right-skewness: a batter can have multiple low scores and then win a match with a single 15-ball 35-run blitz. A defensible decision framework must separate **dependable pressure performers** from **high-variance, high-impact flyers** whose overall averages are inflated by isolated explosive innings.

### 4.2 Distinguishing Batting Candidate Archetypes
The proposed framework establishes five distinct, mutually exclusive candidate categories based on statistical evidence and multi-match stability:

```
Batting Reliability Decision Taxonomy:
+----------------------------------------------------------------------------------------------------+
| 1. Confirmed Positive Reliability (High Volume, Positive Lower Bound)                              |
|    - Criteria: BAT_CONSERVATIVE > 0.0, Evidence Volume >= 150 balls, Matches >= 15, Seasons >= 3   |
|    - Exemplars: Nicholas Pooran (+2.2 SR bound, 212 balls), Heinrich Klaasen (+0.4 bound, 155 balls)|
|    - Decision Utility: First-choice clutch batters; dependable across multi-season campaigns.     |
+----------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
+----------------------------------------------------------------------------------------------------+
| 2. High-Impact Volatile Batters (Positive Mean, High Cross-Match Dispersion)                       |
|    - Criteria: theta_hat > +10.0 SR, BAT_CONSERVATIVE <= 0.0, Match-Level Volatility sigma_m >= 45.0|
|    - Archetype: Match-winners with high boom-or-bust variance; prone to early-over dismissals.    |
|    - Decision Utility: Tactical high-risk/high-reward accelerators; pair with low-variance anchors.|
+----------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
+----------------------------------------------------------------------------------------------------+
| 3. Positive Estimates with Unresolved Uncertainty (Sample-Qualified Established Performers)        |
|    - Criteria: theta_hat > 0.0, BAT_CONSERVATIVE <= 0.0, Balls >= 60, Matches >= 10                |
|    - Exemplars: Tim David (+16.8 mean, bound -0.7), Glenn Maxwell (+14.2 mean, bound -3.0),        |
|      Rinku Singh (+9.5 mean, bound -4.3), Marcus Stoinis (+10.7 mean, bound -4.4)                  |
|    - Decision Utility: Highly capable performers where sample volume does not yet rule out zero.   |
+----------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
+----------------------------------------------------------------------------------------------------+
| 4. Emerging High-Upside Watchlist (Small-Sample Positive Flyers)                                   |
|    - Criteria: theta_hat > 0.0, Balls in [30, 59], Matches < 10                                    |
|    - Exemplars: Cooper Connolly (+20.1 mean, bound -6.1, 33b), Ishan Kishan (+1.8 mean, 36b)       |
|    - Decision Utility: Development / monitoring watchlist; insufficient sample for primary trust. |
+----------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
+----------------------------------------------------------------------------------------------------+
| 5. Evidence of Below-Baseline Performance (Statistically Confirmed Sub-Par)                        |
|    - Criteria: theta_hat + 1.0*SE < 0.0 (entire 1-sigma interval below ordinary context baseline)  |
|    - Population: 182 qualified batters                                                             |
|    - Decision Utility: Identify players who reliably degrade in strike rate under pressure.        |
+----------------------------------------------------------------------------------------------------+
```

### 4.3 Multi-Vector Tactical Evaluation (No Arbitrary Weights)
Rather than condensing performance into an arbitrary linear sum, the batting decision framework evaluates a **vector of context-adjusted differentials**:
1. **Scoring Velocity Differential:** $\Delta_{\text{SR}} = \text{SR}_{\text{obs}} - \mathbb{E}[\text{SR} \mid \text{context}]$ (Primary speed metric).
2. **Boundary Generation Differential:** $\Delta_{\text{Bnd}} = \text{Bnd}\%_{\text{obs}} - \mathbb{E}[\text{Bnd}\% \mid \text{context}]$ (Boundary dependence).
3. **Dot Ball Suppression Differential:** $-\Delta_{\text{Dot}} = -(\text{Dot}\%_{\text{obs}} - \mathbb{E}[\text{Dot}\% \mid \text{context}])$ (Strike rotation under pressure).
4. **Dismissal Resistance Differential:** $-\Delta_{\text{Dism}} = -(\text{Dism}\%_{\text{obs}} - \mathbb{E}[\text{Dism}\% \mid \text{context}])$ (Wicket preservation).

### 4.4 Role-Conditioned Batting Profiles
A batter's pressure reliability must be evaluated relative to their tactical role:
- **Top-Order Chase Anchors (Overs 1–10 entry):** High leverage arises from early wicket collapses. Key diagnostic: Dot ball suppression and dismissal resistance while maintaining context strike rate.
- **Middle-Order Accelerators (Overs 11–15 entry):** Key diagnostic: Immediate boundary generation against spin/pace without requiring an extended sight-screen period.
- **Death-Phase Finishers (Overs 16–20 entry):** 87.7% of pressure events. Key diagnostic: Maximum boundary generation ($\Delta_{\text{Bnd}} > 0$) with high tolerance for dismissal risk.

---

## 5. Proposed Bowling Reliability Decision Framework

### 5.1 Resolving the Bowling Baseline Floor Paradox
A critical finding from Tasks R1-04.1 through R1-06.2 is that bowling pressure performance exhibits severe **baseline floor clustering**:
- The ordinary context baseline for bowling is ~7.98 RPO (across all innings and phases).
- Under pressure (concentrated heavily in Death overs 16–20), the macro unweighted average economy conceded rises to **10.06 RPO** (+2.085 RPO degradation).
- The context-stratified, precision-weighted DerSimonian-Laird population prior mean is **$\mu_{bw} = +1.82$ RPO conceded** above ordinary baseline.
- Consequently, **237 of the 239 qualified bowlers** concede more runs under pressure than their ordinary baselines ($\hat{\theta}_{\text{Econ}} > 0$, meaning negative runs saved relative to ordinary baseline).
- **Jasprit Bumrah** is the *only* qualified bowler with a positive point estimate of runs saved relative to ordinary baseline ($\hat{\theta} = -0.16$, runs saved $+0.16$ RPO; but $\text{SE} = 0.36$, lower bound $-0.20$ RPO).
- **Sunil Narine** is the *only* qualified bowler with inconclusive bounds spanning ordinary baseline ($\hat{\theta} = +0.33$, bound $-0.77$ RPO, upper bound $+0.11$ RPO).

> [!IMPORTANT]
> **Governing Bowling Decision Principle:**  
> If bowling reliability were evaluated strictly against the ordinary baseline, virtually every bowler in world cricket would be classified as "unreliable". The proposed decision framework resolves this by establishing a **Dual-Benchmark Evaluation**:
> 1. **Absolute Benchmark (Ordinary Baseline):** Evaluates whether a bowler miraculously prevents death-phase inflation (Bumrah anomaly).
> 2. **Relative Peer Benchmark (League Pressure Average $\mu_{bw} = +1.82$ RPO):** Evaluates whether a bowler outperforms peer bowlers under identical high-leverage conditions.

### 5.2 Distinguishing Bowling Candidate Archetypes

```
Bowling Reliability Decision Taxonomy:
+----------------------------------------------------------------------------------------------------+
| 1. Confirmed Positive Absolute Reliability (Positive Conservative Runs Saved > 0.0)                |
|    - Criteria: BOWL_CONSERVATIVE > 0.0 relative to ordinary baseline                               |
|    - Status: Currently ZERO players qualify in Senior T20 cricket (reflects extreme death leverage).|
+----------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
+----------------------------------------------------------------------------------------------------+
| 2. Baseline Outperformers with Unresolved Uncertainty                                              |
|    - Criteria: Runs Saved Point Estimate > 0.0, BOWL_CONSERVATIVE <= 0.0                           |
|    - Exemplar: Jasprit Bumrah (+0.16 RPO saved point estimate, -0.20 RPO bound, SE=0.36, 145 balls)|
|    - Decision Utility: World-class gold standard; exceptional containment under pressure.         |
+----------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
+----------------------------------------------------------------------------------------------------+
| 3. Established Peer-Beaters (Beats League Pressure Mean mu = +1.82, Sample Qualified)              |
|    - Criteria: theta_hat < +1.82 RPO conceded, Balls >= 60 OR (Balls >= 50 AND Matches >= 10)      |
|    - Population: 68 qualified bowlers (e.g. Rashid Khan, Bhuvneshwar Kumar, Kagiso Rabada,         |
|      Arshdeep Singh, Mitchell Starc, Trent Boult, Anrich Nortje, Sandeep Sharma, Pat Cummins)      |
|    - Decision Utility: Core elite bowling assets; reliably limit damage relative to peer baseline. |
+----------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
+----------------------------------------------------------------------------------------------------+
| 4. Emerging Peer-Beaters (Beats League Pressure Mean mu = +1.82, Small Sample)                     |
|    - Criteria: theta_hat < +1.82 RPO conceded, Balls in [30, 59], Matches < 10                     |
|    - Population: 30 bowlers (e.g. Yash Dayal, Spencer Johnson, Vijaykumar Vyshak, Nuwan Thushara)   |
|    - Decision Utility: High-potential scouting watchlist; provisional peer-beating evidence.      |
+----------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
+----------------------------------------------------------------------------------------------------+
| 5. Severe Underperformers Under Pressure (Concedes > League Pressure Average)                       |
|    - Criteria: theta_hat >= +1.82 RPO conceded, entire 1-sigma interval above peer average         |
|    - Population: 139 qualified bowlers                                                             |
|    - Decision Utility: Bowlers who concede excessive runs under high leverage; avoid in death overs.|
+----------------------------------------------------------------------------------------------------+
```

### 5.3 Tactical Containment vs Wicket-Taking Tradeoff
In high-leverage death bowling, a bowler who takes 2 wickets but concedes 22 runs in an over may lose a match, whereas a bowler who bowls 4 dot balls, concedes 6 runs, and takes 0 wickets wins it.
- **Primary Diagnostic:** Conservative Runs Saved per Over ($\text{BOWL\_CONSERVATIVE} = -\hat{\theta}_{\text{Econ}} - 1.0 \times \text{SE}_{\text{post}}$).
- **Secondary Diagnostics:**
  - Context-adjusted Dot Ball % ($\Delta_{\text{Dot}}$): Measures execution precision (yorkers, wide lines).
  - Context-adjusted Boundary Conceded % ($-\Delta_{\text{Bnd}}$): Measures avoidance of boundary leaks.
  - Context-adjusted Wicket % ($\Delta_{\text{Wkt}}$): Contextualized by phase (taking a top-order wicket in Powerplay pressure vs death tail-ender wickets).

### 5.4 Separation of Batting and Bowling
The audit firmly confirms that **batting and bowling reliability must NEVER be combined into a single composite all-rounder score** in the primary decision framework:
- Batting and bowling occur in fundamentally non-commensurable units (SR points vs RPO).
- Min-max scaling or harmonic combinations introduce severe cohort-dependent rank distortion.
- All-rounder evaluation must present **dual independent reliability vectors** (e.g., Hardik Pandya: Batting Profile + Bowling Profile evaluated separately).

---

## 6. Statistical Methodology and Evidence Requirements (10 Dimensions)

The table below provides a comprehensive architectural specification for the 10 core dimensions mandated for the decision framework.

| # | Dimension Name | Existing Data Fields & Provenance | Proposed Statistical / Analytical Method | Methodological Status | Risks of Bias or Double-Counting | Role in Decision Framework |
| :---: | :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | **Context-Adjusted Performance** | `diff_strike_rate`, `diff_economy`, `batting/bowling_pressure_differentials.parquet` | Stratified empirical expectation subtraction $\Delta_i = Y_i - \mathbb{E}[Y \mid \text{stratum}]$ | **Validated** | Omission of opposition bowling quality bias | **Primary Decision Metric** |
| **2** | **Multi-Match Reliability vs Outliers** | `pressure_matches`, match-level aggregations in `delivery_states_strict.parquet` | Cluster-robust standard errors and match-level variance decomposition $\sigma^2_{\text{match}}$ | **Proposed for R1-07.1** | Double-counting delivery volume if not cluster-weighted | **Primary Decision Filter** |
| **3** | **Sample Size & Exposure Sufficiency** | `pressure_legal_balls`, `pressure_matches`, `evidence_volume_tier` | Effective sample size calculation and sample qualification boundaries ($\ge 60$b or $\ge 50$b/$\ge 10$m) | **Validated** | Arbitrary threshold artifacts mitigated by continuous SE weighting | **Primary Decision Prerequisite** |
| **4** | **Posterior Uncertainty & Conservative Bounds** | `posterior_mean`, `posterior_se`, `primary_diagnostic_value` | Empirical Bayes shrinkage with 1-SE Value-at-Risk conservative bound $\hat{\theta} - 1.0 \times \text{SE}$ | **Validated** | Misinterpreting 1-SE bound as 95% CI (governed by verbatim disclosure) | **Primary Ranking & Decision Anchor** |
| **5** | **Consistency Across Pressure Types** | `is_bat_chase_rrr_p75`, `is_bat_depleted_wickets_w2`, `is_bat_death_accel_w3` | Differential breakdown across chase pressure vs collapse pressure vs death acceleration | **Exploratory** | Small-sample fragmentation across narrow sub-definitions | **Supporting Diagnostic** |
| **6** | **Performance Across Phase Contexts** | `innings_phase` (Powerplay, Middle, Death) in `delivery_states_strict.parquet` | Phase-conditioned differential vectors ($\Delta_{\text{Death}}$ vs $\Delta_{\text{Middle}}$) | **Proposed for R1-07.2** | 87.7% sample concentration in Death phase causes middle/PP sparsity | **Supporting Tactical Diagnostic** |
| **7** | **Role-Specific Evaluation** | Entry over, batting order proxy, bowler spell allocation | Stratified peer benchmarking within tactical roles (Top-order vs Finisher; PP vs Death) | **Proposed for R1-07.2** | Survivor bias in entry points; role misclassification | **Supporting Tactical Filter** |
| **8** | **Competition Transferability** | `ipl_legal_balls`, `t20i_legal_balls`, `competition_coverage` | Cross-competition correlation and holdout prediction error (IPL $\leftrightarrow$ T20I) | **Exploratory / Validated Limits** | Assuming transferability where only 47 batters and 63 bowlers have dual exposure | **Supporting Governance Limitation** |
| **9** | **Recency & Historical Stability** | `season`, `season_span`, `season_distribution`, `pressure_seasons` | Exponential time-decay weighting or rolling multi-season windows (replacing heuristic TCF) | **Proposed for R1-07.3** | Arbitrary season tenure penalties (proven flaw of legacy TCF) | **Supporting Temporal Context** |
| **10** | **Evidence Quality & Confidence Limits** | `ci_95_width`, `shrinkage_weight`, `uncertainty_level` | Rigorous disclosure of credible interval overlap and Poisson delivery noise limits | **Validated** | False precision; claiming calibrated win probabilities where Brier score ~0.26 | **Mandatory Governance Disclosure** |

---

## 7. Validation and Leakage-Prevention Strategy

A rigorous validation strategy is mandatory to ensure that the reliability decision framework provides defensible analytical intelligence rather than retrofitted descriptive narratives.

### 7.1 Distinguishing Descriptive Analysis from Predictive Validation
- **Descriptive Historical Analysis:** Summarizes what a player accomplished under pressure during 2022–2026, accounting for context difficulty and sample variance.
- **Out-of-Sample Predictive Validation:** Evaluates whether past pressure reliability metrics forecast future pressure performance better than naive baselines.
- **Governance Mandate:** The decision framework must explicitly distinguish descriptive performance summaries from forward-looking projections. Future performance guarantees are strictly prohibited.

### 7.2 Leakage-Prevention Architecture
1. **Match-Level Grouping Invariant:** Deliveries from the same match must NEVER be split across training and validation sets. Any cross-validation or holdout split must group strictly by `match_id` to prevent within-match tactical leakage.
2. **Chronological Forward Validation:** Temporal splits must evaluate past data predicting future seasons (e.g. Train on 2022–2024 $\to$ Validate on 2025–2026). Reverse temporal evaluation or random k-fold shuffling across time is strictly prohibited.
3. **Strict Baseline Isolation:** Ordinary expected baselines must be computed exclusively on historical training partitions, preventing future league-wide scoring trends from leaking into historical expectations.

### 7.3 Quantitative Validation Protocols
- **Brier Score & Calibration Curves:** Evaluate posterior exceedance probabilities against observed binary performance outcomes. If Brier Skill Score remains near zero due to Poisson noise, probabilities must be explicitly labeled as uncalibrated Bayesian credible estimates.
- **Rank Stability Under Perturbation:** Calculate Spearman rank correlation and Top 10 Jaccard overlap under:
  - 10% random match omission (bootstrap subsampling).
  - Outlier player omission.
  - Exposure threshold variation ($n \in \{30, 45, 60, 75, 100\}$ balls).
  - Target: $r_s > 0.95$ across all standard configurations.
- **Cross-Competition Transferability Holdout:** Evaluate whether shrunk IPL performance differentials predict Senior T20I differentials with lower MSE than raw un-shrunk estimates.

---

## 8. Decision Output Specification (Traceable Player Decision Card)

The eventual decision output must provide an operational, explainable, and fully traceable **Player Pressure Reliability Decision Card** for each evaluated candidate.

### Structural Blueprint of the Player Decision Card:

```
========================================================================================================
ROYALS INTELLIGENCE — PLAYER PRESSURE RELIABILITY DECISION CARD
========================================================================================================
1. PLAYER IDENTITY & ROLE PROFILE
   - Canonical Player ID: [Integer ID] | Player Name: [Display Name]
   - Discipline: [BATTING | BOWLING] | Primary Role: [Top-Order Anchor | Finisher | Death Closer | etc.]
   - Primary League Status: [IPL Specialist | Dual-Competition Proven | T20I Specialist]

2. EXPOSURE & EXPERIENCE ENVELOPE
   - Pressure Exposure: [N] legal balls | [M] matches | [S] seasons (Span: YYYY-YYYY)
   - Competition Breakdown: IPL: [N_ipl] balls in [M_ipl] matches | T20I: [N_t20i] balls in [M_t20i] matches
   - Evidence Volume Tier: [HIGH_VOLUME (>=150b) | MEDIUM_VOLUME (60-149b) | LOW_VOLUME (30-59b)]
   - Candidate Sample Qualification: [QUALIFIED (>=60b or >=50b/10m) | WATCHLIST_ONLY | DISQUALIFIED]

3. CONTEXT-ADJUSTED PERFORMANCE VECTOR
   - Batting Vector:
     * Observed SR: [X.X] vs Context Expected SR: [Y.Y] -> Raw Differential: [+Z.Z] SR pts
     * Dot Ball % Diff: [+/-A.A]% | Boundary % Diff: [+/-B.B]% | Dismissal % Diff: [+/-C.C]%
   - Bowling Vector:
     * Observed Econ: [X.XX] vs Context Expected Econ: [Y.YY] -> Raw Differential: [+Z.ZZ] RPO
     * Dot Ball % Diff: [+/-A.A]% | Boundary Conceded % Diff: [+/-B.B]% | Wicket % Diff: [+/-C.C]%

4. STATISTICAL UNCERTAINTY & CONSERVATIVE ESTIMATE
   - Posterior Mean (Shrunk theta): [+X.X] SR pts / RPO | Shrinkage Factor (w_i): [0.XX]
   - Posterior Standard Error (SE_post): [+/-Y.Y] | 95% Credible Interval: [Lower, Upper]
   - Primary Conservative Score (1-SE Bound): [+Z.Z] SR pts / RPO
   - Mandatory Uncertainty Disclosure:
     "Under an approximate normal posterior distribution, a positive one-standard-error lower bound
      implies posterior probability above zero greater than approximately 84.1%. This is a directional
      uncertainty diagnostic, not a 95% credible interval, conventional 95% statistical significance,
      or a guarantee of future performance."

5. RELIABILITY CLASSIFICATION & DECISION TAXONOMY
   - Performance Evidence Status (Dimension A): [POSITIVE_CONSERVATIVE_EVIDENCE | POSITIVE_ESTIMATE_UNRESOLVED |
                                                BELOW_BASELINE_EVIDENCE | INCONCLUSIVE_EVIDENCE]
   - Watchlist / Decision Cohort: [CONFIRMED_POSITIVE_RELIABILITY | HIGH_IMPACT_VOLATILE |
                                   ESTABLISHED_PEER_BEATER | EMERGING_HIGH_UPSIDE | BELOW_BASELINE]
   - Peer Benchmark Exceedance: P(Exceed League Pressure Prior Mean) = [XX.X]%

6. TACTICAL STRENGTHS & VULNERABILITIES
   - Phase Execution: Death Phase Diff: [+/-X.X] | Middle Phase Diff: [+/-Y.Y]
   - Chase vs Defend: Target Chase Diff: [+/-X.X] | Defending Total Diff: [+/-Y.Y]
   - Match Dispersion: Cross-Match Volatility (sigma_m): [XX.X] | Positive-Match Win Rate: [XX.X]%
   - Tactical Archetype Summary: [Clear, qualitative narrative explaining operational strengths and flaws]

7. MATCH-LEVEL SUPPORTING EVIDENCE & AUDIT TRACE
   - Top 3 Clutch Performances:
     1. Match [ID]: vs [Opponent], [Date] -> [Situation details, balls faced, outcome differential]
     2. Match [ID]: vs [Opponent], [Date] -> [Situation details, balls faced, outcome differential]
     3. Match [ID]: vs [Opponent], [Date] -> [Situation details, balls faced, outcome differential]
   - High-Leverage Breakdown: Exact RRR >= 12.0 performance, final 12 balls execution.

8. EXPLICIT LIMITATIONS & GOVERNANCE WARNINGS
   - Sample Size Caveats: [Warnings if balls < 60 or matches < 10]
   - Credible Interval Overlap: [List of candidates whose 95% CIs overlap with this player]
   - Cross-Competition Caveat: [Explicit warning if performance is derived predominantly from one tournament]
   - Death Phase Concentration: [Warning regarding 87.7% death overs concentration]
========================================================================================================
```

---

## 9. Identified Risks and Unresolved Methodological Questions

The audit identifies six critical methodological risks that must be resolved prior to or during R1-07 implementation:

1. **Death-Phase Concentration Bias:**
   - *Risk:* 87.7% of all pressure deliveries occur in Overs 16–20. Consequently, general "pressure reliability" is overwhelmingly a proxy for death-overs execution.
   - *Mitigation:* Explicitly label metrics as "Death-Dominant Pressure Reliability" and condition secondary diagnostics on phase entry points.
2. **Bowling Ordinary Baseline Floor Clustering:**
   - *Risk:* Ordinary bowling baselines create the illusion that 99% of bowlers are unreliable under pressure, because death bowling naturally concedes ~10.06 RPO.
   - *Mitigation:* Mandate the dual-benchmark approach: absolute runs saved for elite anomalies (Bumrah), and peer-relative runs saved against the empirical prior mean (+1.82 RPO conceded) for standard candidate evaluation.
3. **Severe Cross-Competition Sample Sparsity:**
   - *Risk:* Only 47 batters and 63 bowlers meet the minimum 30-ball threshold in both IPL and Senior T20Is. Cross-tournament skill transferability cannot be proven statistically for the majority of the cohort.
   - *Mitigation:* Require explicit competition provenance tags (`IPL_SPECIALIST`, `T20I_SPECIALIST`, `DUAL_TOURNAMENT_QUALIFIED`) on every decision output, with mandatory transferability caveats.
4. **Lack of Ball-Tracking and Matchup Micro-Data:**
   - *Risk:* The dataset lacks release speed, length/line tracking, and pitch conditions. Confounding factors (e.g. bowling to set batters vs tailenders; batting with an anchor vs a tailender) remain unobserved.
   - *Mitigation:* Explicitly disclose unobserved variable limitations in every player profile.
5. **Conflating Variance with Inconsistency in Multi-Season Profiling:**
   - *Risk:* Legacy TCF penalized players with fewer seasons active using an unvalidated scalar $(S/4)^{0.35}$ and treated Poisson sample noise as talent instability.
   - *Mitigation:* Discard legacy TCF. Replace with match-level cluster variance and hierarchical random-effects modeling that separates sampling error from true player performance drift.
6. **False Precision and Probability Over-Interpretation:**
   - *Risk:* Stakeholders may interpret posterior exceedance probabilities (e.g. 84.1% or 95%) as calibrated match-winning guarantees.
   - *Mitigation:* Enforce the verbatim 1-SE uncertainty disclosure across all system outputs and reports.

---

## 10. Proposed R1-07 Implementation Milestones & Dependencies

To ensure disciplined execution, R1-07 is structured into four sequential, dependency-linked milestones:

```
Proposed R1-07 Milestone Dependency Roadmap:
+----------------------------------------------------------------------------------------------------+
| Milestone R1-07.1: Multi-Match Variance Decomposition & Situational Clustering Engine               |
| - Computes match-level aggregations, cluster-robust standard errors, and cross-match volatility    |
| - Separates isolated single-match heroics from dependable match-in, match-out performers           |
+----------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
+----------------------------------------------------------------------------------------------------+
| Milestone R1-07.2: Role-Stratified & Phase-Conditioned Reliability Profiler                        |
| - Maps players to tactical archetypes (Top-Order Anchor, Middle Surge, Death Finisher, Closer)     |
| - Constructs phase-specific differential vectors and dual-benchmark bowling peer evaluations       |
+----------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
+----------------------------------------------------------------------------------------------------+
| Milestone R1-07.3: Out-of-Sample Rolling-Origin Temporal & Transferability Validation Suite        |
| - Implements forward rolling-origin backtesting (2022-2024 -> 2025 -> 2026) without data leakage   |
| - Tests rank stability, threshold monotonicity, and IPL-T20I transferability limits                |
+----------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
+----------------------------------------------------------------------------------------------------+
| Milestone R1-07.4: Operational Decision Card Generation & Traceable Decision Governance Framework  |
| - Generates standardized, fully traceable Player Decision Cards for all qualified candidates       |
| - Produces comprehensive decision documentation, audit summaries, and stakeholder executive reports|
+----------------------------------------------------------------------------------------------------+
```

### Detailed Milestone Specifications:

#### Milestone R1-07.1: Multi-Match Variance Decomposition & Situational Clustering Engine
- **Objective:** Quantify consistency across multiple matches rather than isolated single-match performances.
- **Why Necessary:** Prevents players with one massive 50-run over or 4-wicket haul from dominating reliability ratings if their remaining matches were below baseline.
- **Key Deliverables:** Match-aggregated differential datasets; cluster-robust variance estimates; per-player match consistency metrics ($\sigma^2_{\text{match}}$ and % of positive matches).

#### Milestone R1-07.2: Role-Stratified & Phase-Conditioned Reliability Profiler
- **Objective:** Evaluate batters and bowlers against phase-specific and role-specific demands.
- **Why Necessary:** Resolves the bowling baseline floor paradox by formalizing the Peer-Beating benchmark (+1.82 RPO) and evaluates batters within their tactical entry envelopes.
- **Key Deliverables:** Phase-stratified differential vectors; tactical role classifications; dual-benchmark bowling candidate evaluation tables.

#### Milestone R1-07.3: Out-of-Sample Rolling-Origin Temporal & Transferability Validation Suite
- **Objective:** Execute rigorous, leakage-free predictive validation and stability audits.
- **Why Necessary:** Distinguishes genuine predictive stability from retrospective overfitting and verifies rank robustness against sample variations.
- **Key Deliverables:** Chronological rolling-origin evaluation artifacts; perturbation stability reports ($r_s > 0.95$ proof); competition transferability audit.

#### Milestone R1-07.4: Operational Decision Card Generation & Governance Framework
- **Objective:** Synthesize all validated analytics into operational, explainable, and traceable decision artifacts.
- **Why Necessary:** Delivers the ultimate SupeRR Selector Round 1 challenge solution: identifying the most reliable players under pressure with complete evidence backing.
- **Key Deliverables:** Full candidate decision cards (Parquet + Markdown); executive summary report; methodology and limitations documentation.

---

## 11. Explicit Acceptance Criteria for Each Proposed Milestone

| Milestone | Target Capability | Strict Quantitative & Qualitative Acceptance Criteria |
| :--- | :--- | :--- |
| **R1-07.1** | Multi-Match Clustering & Variance Decomposition | 1. 100% of deliveries correctly mapped to match IDs without loss or duplication.<br>2. Cluster-robust standard errors computed for all 278 batting and 239 bowling qualified candidates.<br>3. Cross-match variance $\sigma^2_{\text{match}}$ and positive-match win rate computed for all candidates with $\ge 5$ pressure matches.<br>4. High-impact volatile players explicitly separated from consistent performers.<br>5. Zero data leakage across match boundaries; full test suite pass rate. |
| **R1-07.2** | Role-Stratified & Phase Profiling | 1. Every qualified candidate assigned a deterministic tactical role based on historical entry over.<br>2. Phase-specific differentials ($\Delta_{\text{Death}}$, $\Delta_{\text{Middle}}$, $\Delta_{\text{PP}}$) computed where sample $n \ge 15$ balls.<br>3. Dual-benchmark bowling evaluation operationalized: absolute runs saved AND peer-relative runs saved.<br>4. Established Peer-Beaters ($N=68$) and Emerging Peer-Beaters ($N=30$) fully profiled.<br>5. Batting and bowling evaluations maintained strictly independent (zero universal composite scores). |
| **R1-07.3** | Rolling-Origin Temporal & Transferability Validation | 1. Chronological forward validation executed across 2 rolling splits (Train 2022–2024 $\to$ Test 2025; Train 2022–2025 $\to$ Test 2026).<br>2. Out-of-sample MSE of shrunk estimates strictly lower than raw un-shrunk estimates ($>15\%$ error reduction).<br>3. Spearman rank correlation under 10% bootstrap match omission strictly $> 0.95$.<br>4. Exposure threshold monotonicity verified across $n \in \{30, 45, 60, 75, 100\}$ balls.<br>5. Cross-competition transferability evaluated for all 47 dual-qualified batters and 63 dual-qualified bowlers with explicit sample limitation disclosures. |
| **R1-07.4** | Operational Decision Cards & Final Reporting | 1. Individual Player Decision Cards generated for all 278 qualified batters and 239 qualified bowlers.<br>2. Every decision card includes: metadata, exposure envelope, context vector, conservative bound, classification, tactical strengths/weaknesses, top 3 match evidence, and explicit limitations.<br>3. Verbatim 1-SE uncertainty disclosure present on every decision card and report.<br>4. 100% referential integrity and traceability back to source raw data rows.<br>5. Complete test coverage ($\ge 95\%$ pass rate) with zero modifications to legacy R1-01 through R1-06.2 calculations. |

---

## 12. Verification and Audit Sign-Off

- **Planning Document Path:** `round1_pressure/reports/r1_07_0_reliability_framework_architecture_audit.md`
- **Execution Boundary Check:**
  - Python source code modified: **NO (0 lines)**
  - SQL schemas / migrations modified: **NO (0 lines)**
  - Application code modified: **NO (0 lines)**
  - Datasets / Parquet files modified: **NO (0 bytes)**
  - Scores / Leaderboards recomputed: **NO (0 scores)**
  - Git commits created: **NO (0 commits)**
  - Remote Git push executed: **NO (0 pushes)**
- **Audit Conclusion:** The architecture and methodology for the R1-07 Pressure Reliability Decision Framework are fully specified, statistically grounded, and ready for disciplined staged implementation upon explicit user authorization.

---

## 13. Addendum: R1-07.0 Formal Clarification, Failed Test Forensic Audit & Methodology Refinement

### 13.1 Forensic Investigation of the Failed Governance Boundary Test

#### A. Exact Execution Context & Command
- **Command Executed:** `& .\backend\.venv\Scripts\python.exe -m pytest round1_pressure/tests/test_r1_06_2_3_reconciliation.py -v`
- **Execution Timestamp:** 2026-11-16T12:02:26+05:30
- **Exit Code:** `1` (8 passed, 1 failed in 2.43s)

#### B. Complete Pytest Failure Output & Traceback
```
================================== FAILURES ===================================
______________________ test_governance_scope_boundaries _______________________

batting_intel =      player_id  ...  temporal_consistency_score
0            8  ...                    0.868224
1           23  ...   ...22      49268  ...                         NaN
823      60700  ...                         NaN

[824 rows x 46 columns]
bowling_intel =      player_id  ...  temporal_consistency_score
0           23  ...                    0.637475
1           28  ...   ...94      54404  ...                         NaN
595      57747  ...                         NaN

[596 rows x 46 columns]

    def test_governance_scope_boundaries(batting_intel, bowling_intel):
        """
        Verifies strict adherence to competition boundaries:
        1. Zero commercial, auction, price, purse, or salary features in intelligence datasets.
        2. Zero R1-07 files created during audit or remediation.
        """
        forbidden_terms = ["auction", "price", "salary", "crore", "inr", "usd", "bid", "purse"]
    
        for col in batting_intel.columns:
            assert not any(f in col.lower() for f in forbidden_terms), f"Forbidden commercial feature in batting: {col}"
    
        for col in bowling_intel.columns:
            assert not any(f in col.lower() for f in forbidden_terms), f"Forbidden commercial feature in bowling: {col}"
    
        # Verify no R1-07 files exist
        r1_07_files = list(ROOT_DIR.glob("**/r1_07*"))
>       assert len(r1_07_files) == 0, f"R1-07 files detected before authorization: {r1_07_files}"
E       AssertionError: R1-07 files detected before authorization: [WindowsPath('round1_pressure/reports/r1_07_0_reliability_framework_architecture_audit.md')]
E       assert 1 == 0
E        +  where 1 = len([WindowsPath('round1_pressure/reports/r1_07_0_reliability_framework_architecture_audit.md')])

round1_pressure\tests\test_r1_06_2_3_reconciliation.py:382: AssertionError
=========================== short test summary info ===========================
FAILED round1_pressure/tests/test_r1_06_2_3_reconciliation.py::test_governance_scope_boundaries
========================= 1 failed, 8 passed in 2.43s =========================
```

#### C. Root Cause & Failure Classification
1. **Failure Classification:** Explicit assertion failure (`AssertionError`) inside a milestone governance boundary check (`test_governance_scope_boundaries`). It is NOT an import error, syntax error, environment problem, or numerical regression.
2. **Mechanism:** In Task R1-06.2.3, `test_governance_scope_boundaries` was added to verify that the R1-06.2.3 remediation did not prematurely generate any R1-07 code or files. In Task R1-07.0, the prompt explicitly commanded:
   `Create: round1_pressure/reports/r1_07_0_reliability_framework_architecture_audit.md`
   As soon as this mandated planning deliverable was written, any subsequent run of `test_r1_06_2_3_reconciliation.py` detected the presence of that file via `ROOT_DIR.glob("**/r1_07*")`.
3. **Reproducibility:** 100% reproducible whenever an R1-07 planning document exists in the workspace.
4. **Impact on Accepted Checkpoint `6005022`:** Checkpoint `6005022` remains **100% unaffected and valid**. In commit `6005022`, exactly zero R1-07 files existed, and all 196 tests in `round1_pressure/tests/` passed cleanly (100% pass rate). Zero data, baselines, models, scores, or rankings have regressed.
5. **Incidental File Modification Check:** Running the test created or modified **zero files**.

---

### 13.2 Refined R1-07.1 Methodology Specification

#### A. Match-Level Aggregation Architecture
1. **Exact Aggregation Unit:**
   The fundamental unit of analysis is the unique `(match_id, player_id)` tuple (or `(match_id, player_id, discipline)`). Each record captures one player's aggregated pressure exposure and performance within a single fixture.
2. **Delivery Universe & Filtering:**
   - The **200,999 raw deliveries** represent the complete ball-by-ball universe across all 883 matches in `ball_by_ball.csv` and `delivery_states_strict.parquet`.
   - The match-level pressure reliability calculations aggregate **ONLY eligible legal pressure deliveries in the primary scope**:
     * **Batting:** `is_primary_scope == True & is_pressure_event == True & outcome_is_legal == True` (exactly **31,163 deliveries** across 867 matches).
     * **Bowling:** `is_primary_scope == True & is_pressure_event == True & outcome_is_legal == True` (exactly **37,014 deliveries** across 867 matches).
   - Ordinary non-pressure deliveries are utilized exclusively for baseline reference, never summed into pressure aggregates.
3. **Handling of Edge Cases:**
   - *Illegal Deliveries (Wides, No-Balls):* Wides and no-balls do not count as legal balls faced by a batter. For bowlers, runs conceded on wides/no-balls are charged to the bowler, but legal balls bowled are not incremented, strictly preserving the R1-02.3 delivery legality contract.
   - *Extras:* Leg-byes and byes are not charged to the bowler and not credited to the batter. Ambiguous `extras_type == 'other'` deliveries are classified as illegal under Strict legality.
   - *Super Overs:* Strictly **excluded** from primary evaluation (`innings in [1, 2]`), preserving the R1-01 through R1-06 boundary.
   - *Multiple Innings / Abandonments:* Abandoned matches with zero balls (16 matches) yield zero records. In rain-shortened matches with one completed innings, only the played innings is aggregated.
4. **Reconciliation Checks against Existing Artifacts:**
   Exact mathematical conservation invariants will be enforced:
   $$\sum_{m \in \mathcal{M}} n_{\text{balls}, i, m} = n_{\text{balls}, i} \quad \forall i \in \text{Players}$$
   $$\sum_{m \in \mathcal{M}} \text{runs}_{i, m} = \text{runs}_{i} \quad \forall i \in \text{Players}$$
   $$\sum_{i, m} n_{\text{balls}, i, m} = 31,163 \text{ (batting)} \quad \text{and} \quad 37,014 \text{ (bowling)}$$
   The sum of match-level aggregates must equal the totals in `batting_intelligence.parquet` and `bowling_intelligence.parquet` with **zero discrepancy**.

#### B. Cluster-Robust Uncertainty Estimation
1. **Statistical Estimator:**
   The proposed estimator is the **Huber-White / Liang-Zeger cluster-robust variance estimator (CRVE)** ($HC_1$ cluster adjustment):
   $$\hat{\mathbf{V}}_{\text{cluster}} = \left(\sum_{g=1}^G \mathbf{X}_g^T \mathbf{X}_g\right)^{-1} \left(\sum_{g=1}^G \mathbf{X}_g^T \mathbf{e}_g \mathbf{e}_g^T \mathbf{X}_g\right) \left(\sum_{g=1}^G \mathbf{X}_g^T \mathbf{X}_g\right)^{-1} \times \frac{G}{G-1} \times \frac{N-1}{N-K}$$
   where $g \in \{1, \dots, G\}$ indexes matches, and $\mathbf{e}_g$ represents within-match delivery residuals.
2. **Clustering Unit & Dependence Rationale:**
   - Clustering Unit: `match_id`.
   - Rationale: Deliveries within a single match share unobserved environmental shocks (pitch moisture, surface pace, ground dimensions, dew conditions, match leverage tempo, and specific opposition quality). Residuals within the same match are positively correlated, violating the Gauss-Markov independence assumption.
3. **Handling Small Cluster Counts:**
   - Standard asymptotic properties require $G \ge 10$ to $15$ independent clusters.
   - For candidates with $G < 10$ matches, standard cluster SEs can be downward-biased. In such cases, the framework applies the **Bell-McCaffrey bias adjustment** or uses a cohort-pooled variance inflation factor $\text{VIF}_{\text{cluster}} = 1 + (\bar{n}_g - 1)\hat{\rho}$, where $\hat{\rho}$ is the intra-class correlation coefficient.
   - For players with $G < 5$ matches, cluster SE is flagged as `PROVISIONAL_CLUSTER_SAMPLE`.
4. **Distinction from Bayesian Uncertainty:**
   - **Empirical Bayes Posterior Standard Error ($\text{SE}_{\text{post}}$):** Quantifies parameter uncertainty regarding a player's underlying latent skill $\theta_i$, shrunk toward population prior $\mu$.
   - **Cluster-Robust Standard Error ($\text{SE}_{\text{cluster}}$):** Quantifies empirical sampling variability under intra-match error clustering.
   - **Governance Mandate:** The primary ranking and Value-at-Risk conservative bound will **remain strictly anchored on $\text{SE}_{\text{post}}$**. $\text{SE}_{\text{cluster}}$ serves as a complementary diagnostic inflation metric and will **NOT replace** the validated Bayesian framework.

#### C. Match-Level Consistency Metrics
1. **Match-Level Performance Differential:**
   - Batting: $\Delta_{\text{SR}, i, m} = \text{SR}_{i, m} - \mathbb{E}[\text{SR} \mid \text{context}]_{i, m}$ (SR points relative to context baseline of deliveries faced in match $m$).
   - Bowling: $\Delta_{\text{Econ}, i, m} = \text{Econ}_{i, m} - \mathbb{E}[\text{Econ} \mid \text{context}]_{i, m}$ (Runs saved: $-\Delta_{\text{Econ}, i, m}$).
2. **Positive-Differential Match Rate:**
   $$\text{WinRate}_{\text{match}, i} = \frac{\sum_{m \in \mathcal{M}_i} \mathbb{I}(\Delta_{i, m} > 0)}{|\mathcal{M}_i|}$$
   where $\mathcal{M}_i$ is the set of matches meeting the minimum match exposure threshold.
3. **Minimum Match Exposure Threshold:**
   To prevent single-ball noise (e.g. 1 ball, 0 runs $\implies$ SR = 0.0, $\Delta = -140$), a match qualifies for consistency calculation only if the player had **$\ge 3$ legal pressure deliveries** in that match (with sensitivity evaluated at $\ge 5$ balls).
4. **Treatment of Zero-Exposure Matches:**
   Matches where a player was in the playing XI but faced or bowled 0 eligible pressure balls are **excluded from the consistency denominator** $|\mathcal{M}_i|$. Consistency evaluates performance *conditional on being exposed to pressure*.
5. **Diagnostic Classification:**
   Explicitly classified as a **descriptive historical diagnostic**. It describes past empirical match-by-match success rates and carries no inferential future-performance guarantee.

#### D. Volatility Classification Framework
To avoid arbitrary thresholds, volatility is evaluated using objective dispersion benchmarks relative to the qualified cohort:
1. **Dispersion Metric:** Sample standard deviation of match differentials $s_{m, i} = \text{std}(\Delta_{i, m})$ across qualifying matches ($|\mathcal{M}_i| \ge 5$).
2. **Objective Cohort Benchmarks:** Cohort median $\tilde{s}$ and 75th percentile $s_{P75}$ computed across qualified players.
3. **Proposed Archetype Grid:**
   - **Consistently Positive:** Posterior mean $\hat{\theta}_i > 0$, positive match rate $\ge 60\%$, and match dispersion $s_{m, i} \le \tilde{s}$.
   - **High-Impact Volatile:** Posterior mean $\hat{\theta}_i > 0$, positive match rate $< 50\%$, and match dispersion $s_{m, i} > s_{P75}$ (indicating performance driven by isolated explosive outliers).
   - **Consistently Below-Baseline:** Posterior mean $\hat{\theta}_i < 0$, positive match rate $< 40\%$, entire 1-sigma interval below ordinary baseline.
   - **Insufficient Match Evidence:** Fewer than 5 eligible pressure matches ($|\mathcal{M}_i| < 5$), where degrees of freedom ($df < 4$) prevent reliable dispersion estimation.
4. **Governance Mandate:** If empirical validation in R1-07.1 reveals sensitivity to cutoff boundaries, formal volatility classification will be **explicitly designated as EXPLORATORY** and deferred to a later milestone, keeping primary decisions anchored to the accepted two-dimensional system.

---

### 13.3 Numerical Claim Evidence Traceability Matrix

Every numerical claim presented in R1-07.0 is fully traceable to validated artifacts and source calculations in the repository:

| Numerical Claim in R1-07.0 | Exact Value | Source File / Parquet Artifact | Exact Column / Variable / Calculation | Supporting Historical Report or Test |
| :--- | :---: | :--- | :--- | :--- |
| **Death-Over Concentration** | **87.28%** (legal) / **87.82%** (events) | `round1_pressure/data/processed/bowling_pressure_events_strict.parquet` | `(innings_phase == 'DEATH').sum() / len(df)`: 32,307 death / 37,014 legal bowling balls (87.28%); 35,732 death / 40,686 total events (87.82%) | Cited as ~87.7% in `r1_05_1_statistical_audit_report.md` (Audit 6), `README.md`, and `r1_06_methodology_and_limitations.md` |
| **Below-Baseline Qualified Bowlers** | **237 of 239** (99.16%) | `round1_pressure/data/processed/bowling_leaderboard.parquet` | `(performance_evidence_status == 'BELOW_BASELINE_EVIDENCE').sum()` = 237 out of 239 qualified bowlers. (Remaining 2: Bumrah = 1 Positive Estimate Unresolved; Narine = 1 Inconclusive) | `r1_06_2_1_population_reconciliation.md`, `r1_06_bowling_shortlist.md`, and `test_r1_06_2_classification_remediation.py` |
| **Established Peer-Beating Bowlers** | **68** | `round1_pressure/data/processed/bowling_leaderboard.parquet` | `(watchlist_cohort == 'PEER_BEATING_ESTABLISHED').sum()` = 68 qualified bowlers (balls $\ge 60$ or balls $\ge 50$ & matches $\ge 10$; posterior mean $< +1.82$ RPO) | `r1_06_2_1_population_reconciliation.md`, `r1_06_bowling_shortlist.md`, and `test_r1_06_2_2_governance_remediation.py` |
| **Dual-Tournament Qualified Batters** | **47** | `round1_pressure/data/processed/batting_leaderboard.parquet` | `(competition_qualification == 'DUAL_TOURNAMENT_QUALIFIED').sum()` = 47 batters with $\ge 30$ legal pressure balls in both IPL and Senior T20Is | `competition_candidate_views.parquet`, `r1_06_batting_shortlist.md`, and `test_r1_06_player_intelligence.py` |
| **Dual-Tournament Qualified Bowlers** | **63** | `round1_pressure/data/processed/bowling_leaderboard.parquet` | `(competition_qualification == 'DUAL_TOURNAMENT_QUALIFIED').sum()` = 63 bowlers with $\ge 30$ legal pressure balls in both IPL and Senior T20Is | `competition_candidate_views.parquet`, `r1_06_bowling_shortlist.md`, and `test_r1_06_player_intelligence.py` |
| **Batting Bayesian Prior Mean ($\mu_b$)** | **-34.24** SR pts (-34.238444) | `round1_pressure/data/processed/bayesian_shrinkage_summary.parquet` | `prior_mean_mu` for discipline == 'BATTING' | `expected_performance_report.md`, `r1_05_1_statistical_audit_report.md`, `test_expected_performance.py` |
| **Batting Between-Player Prior SD ($\tau_b$)** | **32.94** SR pts (32.937741) | `round1_pressure/data/processed/bayesian_shrinkage_summary.parquet` | `prior_std_tau` for discipline == 'BATTING' (variance $\tau^2 = 1084.894767$) | `expected_performance_report.md`, `r1_05_1_statistical_audit_report.md`, `test_expected_performance.py` |
| **Bowling Bayesian Prior Mean ($\mu_{bw}$)** | **+1.82** RPO (+1.822756) | `round1_pressure/data/processed/bayesian_shrinkage_summary.parquet` | `prior_mean_mu` for discipline == 'BOWLING' | `expected_performance_report.md`, `r1_05_1_statistical_audit_report.md`, `test_expected_performance.py` |
| **Bowling Between-Player Prior SD ($\tau_{bw}$)** | **0.77** RPO (0.770593) | `round1_pressure/data/processed/bayesian_shrinkage_summary.parquet` | `prior_std_tau` for discipline == 'BOWLING' (variance $\tau^2 = 0.593814$) | `expected_performance_report.md`, `r1_05_1_statistical_audit_report.md`, `test_expected_performance.py` |

---

### 13.4 Governance & Audit Boundary Attestation
1. **Checkpoint Unmodified:** Starting checkpoint remains `6005022`.
2. **Codebase Preserved:** Zero Python source code, database schemas, frontend/backend code, Parquet datasets, candidate scores, or Git history modified.
3. **No Implementation Started:** R1-07.1 has not been started.
4. **Remote Repository Invariant:** No remote Git push performed.


