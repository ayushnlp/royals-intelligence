# ROYALS INTELLIGENCE — ROUND 1 BOWLING PRESSURE RELIABILITY SHORTLIST
**Generated:** 2026-11-11T21:49:31.495627+00:00  
**Architecture:** ROYALS INTELLIGENCE v4.1  
**Task:** R1-06 / R1-06.2 Candidate Classification & Evidence Governance Remediation  
**Primary Metric:** Conservative Runs Saved per Over `BOWL_CONSERVATIVE = -posterior_mean_economy_diff - posterior_SE_economy` (Runs Saved/Over)  

---

## 1. Executive Shortlist Overview

The Bowling Pressure Reliability Shortlist evaluates bowler run containment under high-leverage conditions relative to context expectations, penalized by posterior estimation uncertainty. Under the remediated **Two-Dimensional Classification System** (Task R1-06.2):
- **Dimension A (Performance Evidence Status):** Evaluates runs saved point estimate and uncertainty intervals relative to baseline expectation.
- **Dimension B (Evidence Volume Tier):** HIGH_VOLUME ($\ge 150$ balls), MEDIUM_VOLUME ($60-149$ balls), LOW_VOLUME ($30-59$ balls).

> [!IMPORTANT]
> **Jasprit Bumrah Benchmark & Absolute Baseline Findings:**
> - Across all 239 qualified bowlers, **exactly 0 bowlers establish positive conservative runs saved** (`POSITIVE_CONSERVATIVE_EVIDENCE`).
> - **Jasprit Bumrah (#1: -0.16 RPO)** is the **ONLY qualified bowler in the 883-match dataset** who concedes fewer runs under pressure (8.94 RPO) than ordinary baseline (9.70 RPO), with a positive runs saved point estimate ($S = +0.20$ RPO, posterior economy diff $-0.20 \pm 0.36$), classified as `NEGATIVE_CONSERVATIVE_ESTIMATE (HIGH_VOLUME)`.
> - **Sunil Narine (#2: -0.94 RPO)** is classified as `INCONCLUSIVE_EVIDENCE (HIGH_VOLUME)` because his posterior economy diff is $+0.39$ RPO ($S = -0.39$) with $\text{SE} = 0.55$, giving an upper runs saved bound of $+0.16 \ge 0$.
> - The remaining **237 qualified bowlers** are classified as `BELOW_BASELINE_EVIDENCE` because their 1-sigma uncertainty intervals fall strictly below ordinary baseline expectations.

> [!NOTE]
> **Resolution of the 87 vs 88 Bowling Promising Discrepancy:**
> The R1-06.1 audit identified a count divergence between 87 and 88 bowlers outperforming peer average (+1.82 RPO). Full-precision unrounded investigation reveals that Sakib Hussain (`shrunk_diff_economy = 1.817738...`) is strictly below 1.82, whereas Riley Meredith (`shrunk_diff_economy = 1.821739...`) is strictly above 1.82. When code pre-rounded values to 2 decimal places, both evaluated as `1.82 < 1.82 == False`, producing 87. Under full-precision evaluation, Sakib Hussain is included (88). Against the exact prior mean $\mu = 1.82275596$, both are below. The platform now enforces full-precision float comparisons across all pipelines.

> [!NOTE]
> **Probability Interpretation Disclosure:**
> `P(Exceed League Avg Under Pressure)` evaluates exceedance over the league-wide pressure prior mean ($\mu_{bw} = +1.82$ RPO). Conceding fewer than +1.82 RPO extra under pressure beats the average pressured bowler, but does NOT constitute beating ordinary baseline performance.

### Bowling Leaderboard (Top 11 Candidates):

| Rank | Bowler Name | BOWL_CONSERVATIVE (Runs Saved) | Posterior Mean Diff | Posterior SE | 95% Credible Interval | Pressure Balls | Matches | Comp Qual | P(Beat Base) | P(Exceed League Avg Under Pressure) | Dim A (Evidence Status) | Dim B (Volume) | Watchlist Cohort |
| :--- | :--- | ---: | ---: | ---: | :---: | ---: | ---: | :--- | ---: | ---: | :--- | :--- | :--- |
| **1** | **Jasprit Bumrah** | **-0.16** | -0.20 | $\pm$0.36 | [-0.90, +0.50] | 521 | 60 | `DUAL_TOURNAMENT_QUALIFIED` | 71.1% | 100.0% | `NEGATIVE_CONSERVATIVE_ESTIMATE` | `HIGH_VOLUME` | `OUTPERFORMING_BASELINE_ESTIMATE` |
| **2** | **Sunil Narine** | **-0.94** | +0.39 | $\pm$0.55 | [-0.68, +1.47] | 153 | 24 | `IPL_QUALIFIED` | 23.8% | 99.5% | `INCONCLUSIVE_EVIDENCE` | `HIGH_VOLUME` | `INCONCLUSIVE` |
| **3** | **Maheesh Theekshana** | **-0.96** | +0.55 | $\pm$0.41 | [-0.25, +1.35] | 421 | 58 | `DUAL_TOURNAMENT_QUALIFIED` | 9.0% | 99.9% | `BELOW_BASELINE_EVIDENCE` | `HIGH_VOLUME` | `PEER_BEATING_ESTABLISHED` |
| **4** | **Matheesha Pathirana** | **-1.05** | +0.63 | $\pm$0.41 | [-0.18, +1.44] | 440 | 44 | `DUAL_TOURNAMENT_QUALIFIED` | 6.2% | 99.8% | `BELOW_BASELINE_EVIDENCE` | `HIGH_VOLUME` | `PEER_BEATING_ESTABLISHED` |
| **5** | **Nasum Ahmed** | **-1.32** | +0.70 | $\pm$0.63 | [-0.53, +1.93] | 47 | 8 | `T20I_QUALIFIED` | 13.3% | 96.4% | `BELOW_BASELINE_EVIDENCE` | `LOW_VOLUME` | `PEER_BEATING_EMERGING` |
| **6** | **Shaheen Afridi** | **-1.43** | +0.91 | $\pm$0.52 | [-0.10, +1.92] | 191 | 31 | `T20I_QUALIFIED` | 3.8% | 96.1% | `BELOW_BASELINE_EVIDENCE` | `HIGH_VOLUME` | `PEER_BEATING_ESTABLISHED` |
| **7** | **Mustafizur Rahman** | **-1.47** | +1.09 | $\pm$0.38 | [+0.35, +1.84] | 578 | 61 | `DUAL_TOURNAMENT_QUALIFIED` | 0.2% | 97.2% | `BELOW_BASELINE_EVIDENCE` | `HIGH_VOLUME` | `PEER_BEATING_ESTABLISHED` |
| **8** | **Richard Ngarava** | **-1.56** | +1.10 | $\pm$0.46 | [+0.19, +2.01] | 287 | 34 | `T20I_QUALIFIED` | 0.9% | 94.1% | `BELOW_BASELINE_EVIDENCE` | `HIGH_VOLUME` | `PEER_BEATING_ESTABLISHED` |
| **9** | **Vipraj Nigam** | **-1.57** | +0.91 | $\pm$0.66 | [-0.39, +2.21] | 46 | 7 | `IPL_QUALIFIED` | 8.5% | 91.6% | `BELOW_BASELINE_EVIDENCE` | `LOW_VOLUME` | `PEER_BEATING_EMERGING` |
| **10** | **Lungi Ngidi** | **-1.65** | +1.13 | $\pm$0.53 | [+0.09, +2.16] | 222 | 26 | `DUAL_TOURNAMENT_QUALIFIED` | 1.6% | 90.7% | `BELOW_BASELINE_EVIDENCE` | `HIGH_VOLUME` | `PEER_BEATING_ESTABLISHED` |
| **11** | **Ramon Simmonds** | **-1.66** | +0.98 | $\pm$0.68 | [-0.36, +2.32] | 30 | 3 | `T20I_QUALIFIED` | 7.7% | 89.1% | `BELOW_BASELINE_EVIDENCE` | `LOW_VOLUME` | `PEER_BEATING_EMERGING` |

---

## 2. In-Depth Candidate Evidence Profiles

### #1 — Jasprit Bumrah (`NEGATIVE_CONSERVATIVE_ESTIMATE (HIGH_VOLUME)`)
- **Why Considered:** Ranked #1 in Bowling with a conservative diagnostic value of -0.16 RPO. Two-Dimensional Classification: 'NEGATIVE_CONSERVATIVE_ESTIMATE (HIGH_VOLUME)' (Evidence Status: `NEGATIVE_CONSERVATIVE_ESTIMATE`, Volume: `HIGH_VOLUME`, Cohort: `OUTPERFORMING_BASELINE_ESTIMATE`). Sample qualification: QUALIFIED (legacy: 'STRONG_EVIDENCE').
- **Evidence Volume:** 521 legal pressure deliveries bowled/faced, categorized in 'HIGH_VOLUME' (Volume Tier B).
- **Temporal Stability:** Demonstrated across 60 unique pressure matches and 5 active seasons (Distribution: 2022: 116b, 2023: 12b, 2024: 101b, 2025: 155b, 2026: 137b).
- **Observed vs Expected:** Observed Economy Rate: 7.37 (raw difference of -0.76 RPO versus context expectation). | Context-adjusted expectation: 8.13 Economy Rate, derived from stratified 12-cell baselines across phase, tournament tier, and innings.
- **Conservative Diagnostic Score:** BOWL_CONSERVATIVE = -0.16 RPO. Represents the 84% 1-sided credible lower bound (conservative runs saved per over), inherently penalizing estimation uncertainty.
- **Uncertainty & CI:** Posterior standard error: $\pm$0.36 RPO. Shrinkage weight $r = 0.783$. | 95% Credible Interval: [-0.90, 0.50] RPO (width: 1.41 RPO).
- **Competition Support:** Coverage: BOTH (388 balls in IPL, 133 balls in Senior T20I | Classification: `DUAL_TOURNAMENT_QUALIFIED`). Supported by substantial sample in both competitions. Note: Dual-tournament qualification indicates sample exposure availability in both competitions, NOT statistical proof of cross-competition skill transferability.
- **Key Limitations:** Robust sample volume and multi-season stability; residual uncertainty bounded by 95% CI.
- **Sensitivity Profile:** Under unpenalized posterior mean, performance is -0.20 RPO. Model credibility against baseline: 71.1%; against league-wide pressure mean (prior mean $\mu = +1.82 RPO$): 100.0%. Exceeding league average under pressure compares against degraded match conditions, NOT fellow shortlisted candidates. Exploratory PRI without TCF: 100.0; Experimental PRI with TCF: 100.0.

### #2 — Sunil Narine (`INCONCLUSIVE_EVIDENCE (HIGH_VOLUME)`)
- **Why Considered:** Ranked #2 in Bowling with a conservative diagnostic value of -0.94 RPO. Two-Dimensional Classification: 'INCONCLUSIVE_EVIDENCE (HIGH_VOLUME)' (Evidence Status: `INCONCLUSIVE_EVIDENCE`, Volume: `HIGH_VOLUME`, Cohort: `INCONCLUSIVE`). Sample qualification: QUALIFIED (legacy: 'STRONG_EVIDENCE').
- **Evidence Volume:** 153 legal pressure deliveries bowled/faced, categorized in 'HIGH_VOLUME' (Volume Tier B).
- **Temporal Stability:** Demonstrated across 24 unique pressure matches and 5 active seasons (Distribution: 2022: 48b, 2023: 37b, 2024: 18b, 2025: 12b, 2026: 38b).
- **Observed vs Expected:** Observed Economy Rate: 7.14 (raw difference of -1.08 RPO versus context expectation). | Context-adjusted expectation: 8.21 Economy Rate, derived from stratified 12-cell baselines across phase, tournament tier, and innings.
- **Conservative Diagnostic Score:** BOWL_CONSERVATIVE = -0.94 RPO. Represents the 84% 1-sided credible lower bound (conservative runs saved per over), inherently penalizing estimation uncertainty.
- **Uncertainty & CI:** Posterior standard error: $\pm$0.55 RPO. Shrinkage weight $r = 0.494$. | 95% Credible Interval: [-0.68, 1.47] RPO (width: 2.15 RPO).
- **Competition Support:** Coverage: IPL_ONLY (153 balls in IPL, 0 balls in Senior T20I | Classification: `IPL_QUALIFIED`). Limited cross-competition sample overlap. Note: Dual-tournament qualification indicates sample exposure availability in both competitions, NOT statistical proof of cross-competition skill transferability.
- **Key Limitations:** Heavily skewed towards IPL; cross-league transferability is not guaranteed.
- **Sensitivity Profile:** Under unpenalized posterior mean, performance is +0.39 RPO. Model credibility against baseline: 23.8%; against league-wide pressure mean (prior mean $\mu = +1.82 RPO$): 99.5%. Exceeding league average under pressure compares against degraded match conditions, NOT fellow shortlisted candidates. Exploratory PRI without TCF: 92.0; Experimental PRI with TCF: 95.7.

### #3 — Maheesh Theekshana (`BELOW_BASELINE_EVIDENCE (HIGH_VOLUME)`)
- **Why Considered:** Ranked #3 in Bowling with a conservative diagnostic value of -0.96 RPO. Two-Dimensional Classification: 'BELOW_BASELINE_EVIDENCE (HIGH_VOLUME)' (Evidence Status: `BELOW_BASELINE_EVIDENCE`, Volume: `HIGH_VOLUME`, Cohort: `PEER_BEATING_ESTABLISHED`). Sample qualification: QUALIFIED (legacy: 'STRONG_EVIDENCE').
- **Evidence Volume:** 421 legal pressure deliveries bowled/faced, categorized in 'HIGH_VOLUME' (Volume Tier B).
- **Temporal Stability:** Demonstrated across 58 unique pressure matches and 5 active seasons (Distribution: 2022: 100b, 2023: 60b, 2024: 82b, 2024/25: 18b, 2025: 120b, 2026: 41b).
- **Observed vs Expected:** Observed Economy Rate: 8.08 (raw difference of +0.05 RPO versus context expectation). | Context-adjusted expectation: 8.03 Economy Rate, derived from stratified 12-cell baselines across phase, tournament tier, and innings.
- **Conservative Diagnostic Score:** BOWL_CONSERVATIVE = -0.96 RPO. Represents the 84% 1-sided credible lower bound (conservative runs saved per over), inherently penalizing estimation uncertainty.
- **Uncertainty & CI:** Posterior standard error: $\pm$0.41 RPO. Shrinkage weight $r = 0.717$. | 95% Credible Interval: [-0.25, 1.35] RPO (width: 1.61 RPO).
- **Competition Support:** Coverage: BOTH (179 balls in IPL, 242 balls in Senior T20I | Classification: `DUAL_TOURNAMENT_QUALIFIED`). Supported by substantial sample in both competitions. Note: Dual-tournament qualification indicates sample exposure availability in both competitions, NOT statistical proof of cross-competition skill transferability.
- **Key Limitations:** Robust sample volume and multi-season stability; residual uncertainty bounded by 95% CI.
- **Sensitivity Profile:** Under unpenalized posterior mean, performance is +0.55 RPO. Model credibility against baseline: 9.0%; against league-wide pressure mean (prior mean $\mu = +1.82 RPO$): 99.9%. Exceeding league average under pressure compares against degraded match conditions, NOT fellow shortlisted candidates. Exploratory PRI without TCF: 80.1; Experimental PRI with TCF: 96.2.

### #4 — Matheesha Pathirana (`BELOW_BASELINE_EVIDENCE (HIGH_VOLUME)`)
- **Why Considered:** Ranked #4 in Bowling with a conservative diagnostic value of -1.05 RPO. Two-Dimensional Classification: 'BELOW_BASELINE_EVIDENCE (HIGH_VOLUME)' (Evidence Status: `BELOW_BASELINE_EVIDENCE`, Volume: `HIGH_VOLUME`, Cohort: `PEER_BEATING_ESTABLISHED`). Sample qualification: QUALIFIED (legacy: 'STRONG_EVIDENCE').
- **Evidence Volume:** 440 legal pressure deliveries bowled/faced, categorized in 'HIGH_VOLUME' (Volume Tier B).
- **Temporal Stability:** Demonstrated across 44 unique pressure matches and 5 active seasons (Distribution: 2022: 17b, 2023: 140b, 2024: 122b, 2024/25: 6b, 2025: 137b, 2026: 18b).
- **Observed vs Expected:** Observed Economy Rate: 8.29 (raw difference of +0.16 RPO versus context expectation). | Context-adjusted expectation: 8.14 Economy Rate, derived from stratified 12-cell baselines across phase, tournament tier, and innings.
- **Conservative Diagnostic Score:** BOWL_CONSERVATIVE = -1.05 RPO. Represents the 84% 1-sided credible lower bound (conservative runs saved per over), inherently penalizing estimation uncertainty.
- **Uncertainty & CI:** Posterior standard error: $\pm$0.41 RPO. Shrinkage weight $r = 0.713$. | 95% Credible Interval: [-0.18, 1.44] RPO (width: 1.62 RPO).
- **Competition Support:** Coverage: BOTH (336 balls in IPL, 104 balls in Senior T20I | Classification: `DUAL_TOURNAMENT_QUALIFIED`). Supported by substantial sample in both competitions. Note: Dual-tournament qualification indicates sample exposure availability in both competitions, NOT statistical proof of cross-competition skill transferability.
- **Key Limitations:** Robust sample volume and multi-season stability; residual uncertainty bounded by 95% CI.
- **Sensitivity Profile:** Under unpenalized posterior mean, performance is +0.63 RPO. Model credibility against baseline: 6.2%; against league-wide pressure mean (prior mean $\mu = +1.82 RPO$): 99.8%. Exceeding league average under pressure compares against degraded match conditions, NOT fellow shortlisted candidates. Exploratory PRI without TCF: 85.2; Experimental PRI with TCF: 97.2.

### #5 — Nasum Ahmed (`BELOW_BASELINE_EVIDENCE (LOW_VOLUME)`)
- **Why Considered:** Ranked #5 in Bowling with a conservative diagnostic value of -1.32 RPO. Two-Dimensional Classification: 'BELOW_BASELINE_EVIDENCE (LOW_VOLUME)' (Evidence Status: `BELOW_BASELINE_EVIDENCE`, Volume: `LOW_VOLUME`, Cohort: `PEER_BEATING_EMERGING`). Sample qualification: EXCEPTION_PENDING (legacy: 'PROMISING_CANDIDATE').
- **Evidence Volume:** 47 legal pressure deliveries bowled/faced, categorized in 'LOW_VOLUME' (Volume Tier B).
- **Temporal Stability:** Demonstrated across 8 unique pressure matches and 4 active seasons (Distribution: 2022: 6b, 2022/23: 6b, 2023: 6b, 2025: 18b, 2026: 11b).
- **Observed vs Expected:** Observed Economy Rate: 6.26 (raw difference of -1.51 RPO versus context expectation). | Context-adjusted expectation: 7.77 Economy Rate, derived from stratified 12-cell baselines across phase, tournament tier, and innings.
- **Conservative Diagnostic Score:** BOWL_CONSERVATIVE = -1.32 RPO. Represents the 84% 1-sided credible lower bound (conservative runs saved per over), inherently penalizing estimation uncertainty.
- **Uncertainty & CI:** Posterior standard error: $\pm$0.63 RPO. Shrinkage weight $r = 0.338$. | 95% Credible Interval: [-0.53, 1.93] RPO (width: 2.46 RPO).
- **Competition Support:** Coverage: T20I_ONLY (0 balls in IPL, 47 balls in Senior T20I | Classification: `T20I_QUALIFIED`). Limited cross-competition sample overlap. Note: Dual-tournament qualification indicates sample exposure availability in both competitions, NOT statistical proof of cross-competition skill transferability.
- **Key Limitations:** Moderate sample volume (47 balls; estimation CI width is 2.5 RPO); Heavily skewed towards T20I; cross-league transferability is not guaranteed.
- **Sensitivity Profile:** Under unpenalized posterior mean, performance is +0.70 RPO. Model credibility against baseline: 13.3%; against league-wide pressure mean (prior mean $\mu = +1.82 RPO$): 96.4%. Exceeding league average under pressure compares against degraded match conditions, NOT fellow shortlisted candidates. Exploratory PRI without TCF: 71.0; Experimental PRI with TCF: 71.5.

### #6 — Shaheen Afridi (`BELOW_BASELINE_EVIDENCE (HIGH_VOLUME)`)
- **Why Considered:** Ranked #6 in Bowling with a conservative diagnostic value of -1.43 RPO. Two-Dimensional Classification: 'BELOW_BASELINE_EVIDENCE (HIGH_VOLUME)' (Evidence Status: `BELOW_BASELINE_EVIDENCE`, Volume: `HIGH_VOLUME`, Cohort: `PEER_BEATING_ESTABLISHED`). Sample qualification: QUALIFIED (legacy: 'STRONG_EVIDENCE').
- **Evidence Volume:** 191 legal pressure deliveries bowled/faced, categorized in 'HIGH_VOLUME' (Volume Tier B).
- **Temporal Stability:** Demonstrated across 31 unique pressure matches and 4 active seasons (Distribution: 2023: 30b, 2024: 60b, 2025: 95b, 2026: 6b).
- **Observed vs Expected:** Observed Economy Rate: 8.04 (raw difference of +0.18 RPO versus context expectation). | Context-adjusted expectation: 7.87 Economy Rate, derived from stratified 12-cell baselines across phase, tournament tier, and innings.
- **Conservative Diagnostic Score:** BOWL_CONSERVATIVE = -1.43 RPO. Represents the 84% 1-sided credible lower bound (conservative runs saved per over), inherently penalizing estimation uncertainty.
- **Uncertainty & CI:** Posterior standard error: $\pm$0.52 RPO. Shrinkage weight $r = 0.552$. | 95% Credible Interval: [-0.10, 1.92] RPO (width: 2.02 RPO).
- **Competition Support:** Coverage: T20I_ONLY (0 balls in IPL, 191 balls in Senior T20I | Classification: `T20I_QUALIFIED`). Limited cross-competition sample overlap. Note: Dual-tournament qualification indicates sample exposure availability in both competitions, NOT statistical proof of cross-competition skill transferability.
- **Key Limitations:** Heavily skewed towards T20I; cross-league transferability is not guaranteed.
- **Sensitivity Profile:** Under unpenalized posterior mean, performance is +0.91 RPO. Model credibility against baseline: 3.8%; against league-wide pressure mean (prior mean $\mu = +1.82 RPO$): 96.1%. Exceeding league average under pressure compares against degraded match conditions, NOT fellow shortlisted candidates. Exploratory PRI without TCF: 76.2; Experimental PRI with TCF: 88.9.

### #7 — Mustafizur Rahman (`BELOW_BASELINE_EVIDENCE (HIGH_VOLUME)`)
- **Why Considered:** Ranked #7 in Bowling with a conservative diagnostic value of -1.47 RPO. Two-Dimensional Classification: 'BELOW_BASELINE_EVIDENCE (HIGH_VOLUME)' (Evidence Status: `BELOW_BASELINE_EVIDENCE`, Volume: `HIGH_VOLUME`, Cohort: `PEER_BEATING_ESTABLISHED`). Sample qualification: QUALIFIED (legacy: 'STRONG_EVIDENCE').
- **Evidence Volume:** 578 legal pressure deliveries bowled/faced, categorized in 'HIGH_VOLUME' (Volume Tier B).
- **Temporal Stability:** Demonstrated across 61 unique pressure matches and 5 active seasons (Distribution: 2022: 126b, 2022/23: 18b, 2023: 84b, 2024: 140b, 2025: 192b, 2026: 18b).
- **Observed vs Expected:** Observed Economy Rate: 8.93 (raw difference of +0.86 RPO versus context expectation). | Context-adjusted expectation: 8.07 Economy Rate, derived from stratified 12-cell baselines across phase, tournament tier, and innings.
- **Conservative Diagnostic Score:** BOWL_CONSERVATIVE = -1.47 RPO. Represents the 84% 1-sided credible lower bound (conservative runs saved per over), inherently penalizing estimation uncertainty.
- **Uncertainty & CI:** Posterior standard error: $\pm$0.38 RPO. Shrinkage weight $r = 0.756$. | 95% Credible Interval: [0.35, 1.84] RPO (width: 1.49 RPO).
- **Competition Support:** Coverage: BOTH (216 balls in IPL, 362 balls in Senior T20I | Classification: `DUAL_TOURNAMENT_QUALIFIED`). Supported by substantial sample in both competitions. Note: Dual-tournament qualification indicates sample exposure availability in both competitions, NOT statistical proof of cross-competition skill transferability.
- **Key Limitations:** Robust sample volume and multi-season stability; residual uncertainty bounded by 95% CI.
- **Sensitivity Profile:** Under unpenalized posterior mean, performance is +1.09 RPO. Model credibility against baseline: 0.2%; against league-wide pressure mean (prior mean $\mu = +1.82 RPO$): 97.2%. Exceeding league average under pressure compares against degraded match conditions, NOT fellow shortlisted candidates. Exploratory PRI without TCF: 69.2; Experimental PRI with TCF: 74.0.

### #8 — Richard Ngarava (`BELOW_BASELINE_EVIDENCE (HIGH_VOLUME)`)
- **Why Considered:** Ranked #8 in Bowling with a conservative diagnostic value of -1.56 RPO. Two-Dimensional Classification: 'BELOW_BASELINE_EVIDENCE (HIGH_VOLUME)' (Evidence Status: `BELOW_BASELINE_EVIDENCE`, Volume: `HIGH_VOLUME`, Cohort: `PEER_BEATING_ESTABLISHED`). Sample qualification: QUALIFIED (legacy: 'STRONG_EVIDENCE').
- **Evidence Volume:** 287 legal pressure deliveries bowled/faced, categorized in 'HIGH_VOLUME' (Volume Tier B).
- **Temporal Stability:** Demonstrated across 34 unique pressure matches and 5 active seasons (Distribution: 2022: 15b, 2023: 24b, 2023/24: 20b, 2024: 114b, 2025: 84b, 2026: 30b).
- **Observed vs Expected:** Observed Economy Rate: 8.51 (raw difference of +0.69 RPO versus context expectation). | Context-adjusted expectation: 7.82 Economy Rate, derived from stratified 12-cell baselines across phase, tournament tier, and innings.
- **Conservative Diagnostic Score:** BOWL_CONSERVATIVE = -1.56 RPO. Represents the 84% 1-sided credible lower bound (conservative runs saved per over), inherently penalizing estimation uncertainty.
- **Uncertainty & CI:** Posterior standard error: $\pm$0.46 RPO. Shrinkage weight $r = 0.638$. | 95% Credible Interval: [0.19, 2.01] RPO (width: 1.82 RPO).
- **Competition Support:** Coverage: T20I_ONLY (0 balls in IPL, 287 balls in Senior T20I | Classification: `T20I_QUALIFIED`). Limited cross-competition sample overlap. Note: Dual-tournament qualification indicates sample exposure availability in both competitions, NOT statistical proof of cross-competition skill transferability.
- **Key Limitations:** Heavily skewed towards T20I; cross-league transferability is not guaranteed.
- **Sensitivity Profile:** Under unpenalized posterior mean, performance is +1.10 RPO. Model credibility against baseline: 0.9%; against league-wide pressure mean (prior mean $\mu = +1.82 RPO$): 94.1%. Exceeding league average under pressure compares against degraded match conditions, NOT fellow shortlisted candidates. Exploratory PRI without TCF: 66.1; Experimental PRI with TCF: 70.1.

### #9 — Vipraj Nigam (`BELOW_BASELINE_EVIDENCE (LOW_VOLUME)`)
- **Why Considered:** Ranked #9 in Bowling with a conservative diagnostic value of -1.57 RPO. Two-Dimensional Classification: 'BELOW_BASELINE_EVIDENCE (LOW_VOLUME)' (Evidence Status: `BELOW_BASELINE_EVIDENCE`, Volume: `LOW_VOLUME`, Cohort: `PEER_BEATING_EMERGING`). Sample qualification: EXCEPTION_PENDING (legacy: 'PROMISING_CANDIDATE').
- **Evidence Volume:** 46 legal pressure deliveries bowled/faced, categorized in 'LOW_VOLUME' (Volume Tier B).
- **Temporal Stability:** Demonstrated across 7 unique pressure matches and 1 active seasons (Distribution: 2025: 46b).
- **Observed vs Expected:** Observed Economy Rate: 6.52 (raw difference of -1.70 RPO versus context expectation). | Context-adjusted expectation: 8.23 Economy Rate, derived from stratified 12-cell baselines across phase, tournament tier, and innings.
- **Conservative Diagnostic Score:** BOWL_CONSERVATIVE = -1.57 RPO. Represents the 84% 1-sided credible lower bound (conservative runs saved per over), inherently penalizing estimation uncertainty.
- **Uncertainty & CI:** Posterior standard error: $\pm$0.66 RPO. Shrinkage weight $r = 0.259$. | 95% Credible Interval: [-0.39, 2.21] RPO (width: 2.60 RPO).
- **Competition Support:** Coverage: IPL_ONLY (46 balls in IPL, 0 balls in Senior T20I | Classification: `IPL_QUALIFIED`). Limited cross-competition sample overlap. Note: Dual-tournament qualification indicates sample exposure availability in both competitions, NOT statistical proof of cross-competition skill transferability.
- **Key Limitations:** Moderate sample volume (46 balls; estimation CI width is 2.6 RPO); Heavily skewed towards IPL; cross-league transferability is not guaranteed; Short multi-season track record (1 seasons active).
- **Sensitivity Profile:** Under unpenalized posterior mean, performance is +0.91 RPO. Model credibility against baseline: 8.5%; against league-wide pressure mean (prior mean $\mu = +1.82 RPO$): 91.6%. Exceeding league average under pressure compares against degraded match conditions, NOT fellow shortlisted candidates. Exploratory PRI without TCF: 80.7; Experimental PRI with TCF: 52.8.

### #10 — Lungi Ngidi (`BELOW_BASELINE_EVIDENCE (HIGH_VOLUME)`)
- **Why Considered:** Ranked #10 in Bowling with a conservative diagnostic value of -1.65 RPO. Two-Dimensional Classification: 'BELOW_BASELINE_EVIDENCE (HIGH_VOLUME)' (Evidence Status: `BELOW_BASELINE_EVIDENCE`, Volume: `HIGH_VOLUME`, Cohort: `PEER_BEATING_ESTABLISHED`). Sample qualification: QUALIFIED (legacy: 'STRONG_EVIDENCE').
- **Evidence Volume:** 222 legal pressure deliveries bowled/faced, categorized in 'HIGH_VOLUME' (Volume Tier B).
- **Temporal Stability:** Demonstrated across 26 unique pressure matches and 5 active seasons (Distribution: 2022: 30b, 2022/23: 12b, 2023: 12b, 2024: 30b, 2025: 34b, 2026: 104b).
- **Observed vs Expected:** Observed Economy Rate: 8.57 (raw difference of +0.51 RPO versus context expectation). | Context-adjusted expectation: 8.06 Economy Rate, derived from stratified 12-cell baselines across phase, tournament tier, and innings.
- **Conservative Diagnostic Score:** BOWL_CONSERVATIVE = -1.65 RPO. Represents the 84% 1-sided credible lower bound (conservative runs saved per over), inherently penalizing estimation uncertainty.
- **Uncertainty & CI:** Posterior standard error: $\pm$0.53 RPO. Shrinkage weight $r = 0.532$. | 95% Credible Interval: [0.09, 2.16] RPO (width: 2.07 RPO).
- **Competition Support:** Coverage: BOTH (116 balls in IPL, 106 balls in Senior T20I | Classification: `DUAL_TOURNAMENT_QUALIFIED`). Supported by substantial sample in both competitions. Note: Dual-tournament qualification indicates sample exposure availability in both competitions, NOT statistical proof of cross-competition skill transferability.
- **Key Limitations:** Robust sample volume and multi-season stability; residual uncertainty bounded by 95% CI.
- **Sensitivity Profile:** Under unpenalized posterior mean, performance is +1.13 RPO. Model credibility against baseline: 1.6%; against league-wide pressure mean (prior mean $\mu = +1.82 RPO$): 90.7%. Exceeding league average under pressure compares against degraded match conditions, NOT fellow shortlisted candidates. Exploratory PRI without TCF: 74.7; Experimental PRI with TCF: 86.6.

---

## 3. Promising Candidates Watchlist (Peer-Beaters Under Pressure)

These bowlers outperform peer averages ($\hat{\theta} < +1.82$ RPO), saving runs relative to the degraded match environment. They are separated into Emerging ($<60$ balls) and Established ($\ge 60$ balls) tiers:

### A. Emerging Peer-Beating Bowlers (`PEER_BEATING_EMERGING` — $30 \le n < 60$ balls, beating peer mean):

| Bowler Name | Posterior Mean Diff | Posterior SE | Conservative Runs Saved | Pressure Balls | Matches | Volume Tier | Watchlist Cohort | Two-Dimensional Status |
| :--- | ---: | ---: | ---: | ---: | ---: | :--- | :--- | :--- |
| **Nasum Ahmed** | +0.70 RPO | $\pm$0.63 | -1.32 RPO | 47 | 8 | `LOW_VOLUME` | `PEER_BEATING_EMERGING` | `BELOW_BASELINE_EVIDENCE (LOW_VOLUME)` |
| **Vipraj Nigam** | +0.91 RPO | $\pm$0.66 | -1.57 RPO | 46 | 7 | `LOW_VOLUME` | `PEER_BEATING_EMERGING` | `BELOW_BASELINE_EVIDENCE (LOW_VOLUME)` |
| **Ramon Simmonds** | +0.98 RPO | $\pm$0.68 | -1.66 RPO | 30 | 3 | `LOW_VOLUME` | `PEER_BEATING_EMERGING` | `BELOW_BASELINE_EVIDENCE (LOW_VOLUME)` |
| **Roston Chase** | +1.16 RPO | $\pm$0.67 | -1.83 RPO | 54 | 9 | `LOW_VOLUME` | `PEER_BEATING_EMERGING` | `BELOW_BASELINE_EVIDENCE (LOW_VOLUME)` |
| **Piyush Chawla** | +1.20 RPO | $\pm$0.70 | -1.90 RPO | 43 | 7 | `LOW_VOLUME` | `PEER_BEATING_EMERGING` | `BELOW_BASELINE_EVIDENCE (LOW_VOLUME)` |
| **Mohammad Nawaz** | +1.37 RPO | $\pm$0.69 | -2.06 RPO | 35 | 7 | `LOW_VOLUME` | `PEER_BEATING_EMERGING` | `BELOW_BASELINE_EVIDENCE (LOW_VOLUME)` |
| **Sayed Monib** | +1.40 RPO | $\pm$0.70 | -2.10 RPO | 30 | 3 | `LOW_VOLUME` | `PEER_BEATING_EMERGING` | `BELOW_BASELINE_EVIDENCE (LOW_VOLUME)` |
| **Jeffrey Vandersay** | +1.46 RPO | $\pm$0.69 | -2.15 RPO | 30 | 4 | `LOW_VOLUME` | `PEER_BEATING_EMERGING` | `BELOW_BASELINE_EVIDENCE (LOW_VOLUME)` |
| **Zahoor Khan** | +1.53 RPO | $\pm$0.67 | -2.20 RPO | 48 | 5 | `LOW_VOLUME` | `PEER_BEATING_EMERGING` | `BELOW_BASELINE_EVIDENCE (LOW_VOLUME)` |
| **Liam Dawson** | +1.56 RPO | $\pm$0.68 | -2.25 RPO | 51 | 9 | `LOW_VOLUME` | `PEER_BEATING_EMERGING` | `BELOW_BASELINE_EVIDENCE (LOW_VOLUME)` |

### B. Established Peer-Beating Bowlers (`PEER_BEATING_ESTABLISHED` — $n \ge 60$ balls, beating peer mean):

| Bowler Name | Posterior Mean Diff | Posterior SE | Conservative Runs Saved | Pressure Balls | Matches | Volume Tier | Watchlist Cohort | Two-Dimensional Status |
| :--- | ---: | ---: | ---: | ---: | ---: | :--- | :--- | :--- |
| **Maheesh Theekshana** | +0.55 RPO | $\pm$0.41 | -0.96 RPO | 421 | 58 | `HIGH_VOLUME` | `PEER_BEATING_ESTABLISHED` | `BELOW_BASELINE_EVIDENCE (HIGH_VOLUME)` |
| **Matheesha Pathirana** | +0.63 RPO | $\pm$0.41 | -1.05 RPO | 440 | 44 | `HIGH_VOLUME` | `PEER_BEATING_ESTABLISHED` | `BELOW_BASELINE_EVIDENCE (HIGH_VOLUME)` |
| **Shaheen Afridi** | +0.91 RPO | $\pm$0.52 | -1.43 RPO | 191 | 31 | `HIGH_VOLUME` | `PEER_BEATING_ESTABLISHED` | `BELOW_BASELINE_EVIDENCE (HIGH_VOLUME)` |
| **Mustafizur Rahman** | +1.09 RPO | $\pm$0.38 | -1.47 RPO | 578 | 61 | `HIGH_VOLUME` | `PEER_BEATING_ESTABLISHED` | `BELOW_BASELINE_EVIDENCE (HIGH_VOLUME)` |
| **Richard Ngarava** | +1.10 RPO | $\pm$0.46 | -1.56 RPO | 287 | 34 | `HIGH_VOLUME` | `PEER_BEATING_ESTABLISHED` | `BELOW_BASELINE_EVIDENCE (HIGH_VOLUME)` |
| **Lungi Ngidi** | +1.13 RPO | $\pm$0.53 | -1.65 RPO | 222 | 26 | `HIGH_VOLUME` | `PEER_BEATING_ESTABLISHED` | `BELOW_BASELINE_EVIDENCE (HIGH_VOLUME)` |
| **Ravichandran Ashwin** | +1.11 RPO | $\pm$0.57 | -1.67 RPO | 147 | 21 | `MEDIUM_VOLUME` | `PEER_BEATING_ESTABLISHED` | `BELOW_BASELINE_EVIDENCE (MEDIUM_VOLUME)` |
| **Hasan Mahmud** | +1.08 RPO | $\pm$0.61 | -1.69 RPO | 90 | 11 | `MEDIUM_VOLUME` | `PEER_BEATING_ESTABLISHED` | `BELOW_BASELINE_EVIDENCE (MEDIUM_VOLUME)` |
| **Nathan Ellis** | +1.24 RPO | $\pm$0.46 | -1.71 RPO | 347 | 35 | `HIGH_VOLUME` | `PEER_BEATING_ESTABLISHED` | `BELOW_BASELINE_EVIDENCE (HIGH_VOLUME)` |
| **Haris Rauf** | +1.34 RPO | $\pm$0.46 | -1.80 RPO | 356 | 39 | `HIGH_VOLUME` | `PEER_BEATING_ESTABLISHED` | `BELOW_BASELINE_EVIDENCE (HIGH_VOLUME)` |