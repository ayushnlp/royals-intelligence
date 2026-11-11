# ROYALS INTELLIGENCE — ROUND 1 BATTING PRESSURE RELIABILITY SHORTLIST
**Generated:** 2026-11-11T21:49:31.495627+00:00  
**Architecture:** ROYALS INTELLIGENCE v4.1  
**Task:** R1-06 / R1-06.2 Candidate Classification & Evidence Governance Remediation  
**Primary Metric:** Conservative Lower Credible Bound `BAT_CONSERVATIVE = posterior_mean_SR - posterior_SE_SR` (SR Points)  

---

## 1. Executive Shortlist Overview

The Batting Pressure Reliability Shortlist evaluates batters under high-leverage match conditions, penalized by posterior estimation uncertainty. Under the remediated **Two-Dimensional Classification System** (Task R1-06.2):
- **Dimension A (Performance Evidence Status):** Separates candidates whose conservative bound is strictly positive from those with positive estimated effect but unresolved uncertainty.
- **Dimension B (Evidence Volume Tier):** HIGH_VOLUME ($\ge 150$ balls), MEDIUM_VOLUME ($60-149$ balls), LOW_VOLUME ($30-59$ balls).

> [!IMPORTANT]
> **Conservative Lower Bound & Statistical Evidence:**
> - **Exactly 2 qualified batters** establish strictly positive conservative lower bounds (`POSITIVE_CONSERVATIVE_EVIDENCE`): **Nicholas Pooran (+2.2 SR pts)** and **Donovan Ferreira (+0.9 SR pts)**.
> - Candidates ranked #3 through #12 exhibit positive posterior means ($\hat{\theta} > 0.0$), but their 84% conservative lower bounds are non-positive ($L \le 0$). They are classified as `NEGATIVE_CONSERVATIVE_ESTIMATE` (positive estimated effect with unresolved uncertainty spanning zero), NOT negative performance.
> - Candidates ranked #3 through #12 have heavily overlapping 95% credible intervals (e.g. Tim David: [-14.1, +33.3], Dinesh Karthik: [-14.0, +32.5], Ashutosh Sharma: [-17.0, +37.6]). Small ranking differences among these players reflect empirical sample variance rather than proven qualitative superiority.

> [!NOTE]
> **Probability Interpretation Disclosure:**
> `P(Exceed League Avg Under Pressure)` evaluates exceedance over the league-wide pressure prior mean ($\mu_b = -34.24$ SR pts). Because league-wide batting strike rates collapse by ~34 points under pressure, achieving 90%+ probability of exceeding the league pressure average is a much lower hurdle than beating ordinary baseline expectation ($P(\text{Beat Base})$).

### Batting Leaderboard (Top 12 Candidates):

| Rank | Batter Name | BAT_CONSERVATIVE (SR pts) | Posterior Mean $\hat{\theta}$ | Posterior SE | 95% Credible Interval | Pressure Balls | Matches | Comp Qual | P(Beat Base) | P(Exceed League Avg Under Pressure) | Dim A (Evidence Status) | Dim B (Volume) | Watchlist Cohort |
| :--- | :--- | ---: | ---: | ---: | :---: | ---: | ---: | :--- | ---: | ---: | :--- | :--- | :--- |
| **1** | **Nicholas Pooran** | **+2.2** | +16.2 | $\pm$14.0 | [-11.2, +43.6] | 212 | 26 | `DUAL_TOURNAMENT_QUALIFIED` | 87.7% | 100.0% | `POSITIVE_CONSERVATIVE_EVIDENCE` | `HIGH_VOLUME` | `CONFIRMED_POSITIVE_RELIABILITY` |
| **2** | **Donovan Ferreira** | **+0.9** | +20.7 | $\pm$19.8 | [-18.0, +59.4] | 84 | 13 | `IPL_QUALIFIED` | 85.2% | 99.7% | `POSITIVE_CONSERVATIVE_EVIDENCE` | `MEDIUM_VOLUME` | `CONFIRMED_POSITIVE_RELIABILITY` |
| **3** | **Tim David** | **-2.5** | +9.6 | $\pm$12.1 | [-14.1, +33.3] | 290 | 33 | `DUAL_TOURNAMENT_QUALIFIED` | 78.6% | 100.0% | `NEGATIVE_CONSERVATIVE_ESTIMATE` | `HIGH_VOLUME` | `ESTABLISHED_MARGINAL_PERFORMER` |
| **4** | **Dinesh Karthik** | **-2.7** | +9.2 | $\pm$11.9 | [-14.1, +32.6] | 260 | 30 | `DUAL_TOURNAMENT_QUALIFIED` | 78.1% | 100.0% | `NEGATIVE_CONSERVATIVE_ESTIMATE` | `HIGH_VOLUME` | `ESTABLISHED_MARGINAL_PERFORMER` |
| **5** | **Ashutosh Sharma** | **-3.6** | +10.3 | $\pm$13.9 | [-17.0, +37.6] | 191 | 20 | `IPL_QUALIFIED` | 77.0% | 99.9% | `NEGATIVE_CONSERVATIVE_ESTIMATE` | `HIGH_VOLUME` | `ESTABLISHED_MARGINAL_PERFORMER` |
| **6** | **Marcus Stoinis** | **-5.8** | +7.1 | $\pm$12.9 | [-18.1, +32.3] | 220 | 32 | `DUAL_TOURNAMENT_QUALIFIED` | 70.9% | 99.9% | `NEGATIVE_CONSERVATIVE_ESTIMATE` | `HIGH_VOLUME` | `ESTABLISHED_MARGINAL_PERFORMER` |
| **7** | **Naman Dhir** | **-6.9** | +7.9 | $\pm$14.9 | [-21.2, +37.1] | 145 | 18 | `IPL_QUALIFIED` | 70.4% | 99.8% | `NEGATIVE_CONSERVATIVE_ESTIMATE` | `MEDIUM_VOLUME` | `ESTABLISHED_MARGINAL_PERFORMER` |
| **8** | **Rinku Singh** | **-7.0** | +3.4 | $\pm$10.4 | [-17.0, +23.8] | 363 | 48 | `DUAL_TOURNAMENT_QUALIFIED` | 62.8% | 100.0% | `NEGATIVE_CONSERVATIVE_ESTIMATE` | `HIGH_VOLUME` | `ESTABLISHED_MARGINAL_PERFORMER` |
| **9** | **Tristan Stubbs** | **-8.2** | +2.4 | $\pm$10.5 | [-18.3, +23.0] | 266 | 33 | `DUAL_TOURNAMENT_QUALIFIED` | 58.9% | 100.0% | `NEGATIVE_CONSERVATIVE_ESTIMATE` | `HIGH_VOLUME` | `ESTABLISHED_MARGINAL_PERFORMER` |
| **10** | **Sherfane Rutherford** | **-8.2** | +6.9 | $\pm$15.1 | [-22.7, +36.6] | 151 | 21 | `DUAL_TOURNAMENT_QUALIFIED` | 67.7% | 99.7% | `NEGATIVE_CONSERVATIVE_ESTIMATE` | `HIGH_VOLUME` | `ESTABLISHED_MARGINAL_PERFORMER` |
| **11** | **Rovman Powell** | **-8.8** | +1.7 | $\pm$10.5 | [-18.8, +22.2] | 342 | 47 | `DUAL_TOURNAMENT_QUALIFIED` | 56.3% | 100.0% | `NEGATIVE_CONSERVATIVE_ESTIMATE` | `HIGH_VOLUME` | `ESTABLISHED_MARGINAL_PERFORMER` |
| **12** | **Aiden Markram** | **-9.0** | +5.7 | $\pm$14.7 | [-23.2, +34.6] | 133 | 13 | `DUAL_TOURNAMENT_QUALIFIED` | 65.0% | 99.7% | `NEGATIVE_CONSERVATIVE_ESTIMATE` | `MEDIUM_VOLUME` | `ESTABLISHED_MARGINAL_PERFORMER` |

---

## 2. In-Depth Candidate Evidence Profiles

### #1 — Nicholas Pooran (`POSITIVE_CONSERVATIVE_EVIDENCE (HIGH_VOLUME)`)
- **Why Considered:** Ranked #1 in Batting with a conservative diagnostic value of +2.25 SR pts. Two-Dimensional Classification: 'POSITIVE_CONSERVATIVE_EVIDENCE (HIGH_VOLUME)' (Evidence Status: `POSITIVE_CONSERVATIVE_EVIDENCE`, Volume: `HIGH_VOLUME`, Cohort: `CONFIRMED_POSITIVE_RELIABILITY`). Sample qualification: QUALIFIED (legacy: 'STRONG_EVIDENCE').
- **Evidence Volume:** 212 legal pressure deliveries bowled/faced, categorized in 'HIGH_VOLUME' (Volume Tier B).
- **Temporal Stability:** Demonstrated across 26 unique pressure matches and 5 active seasons (Distribution: 2022: 47b, 2023: 49b, 2024: 102b, 2025: 4b, 2026: 10b).
- **Observed vs Expected:** Observed Strike Rate: 190.57 (raw difference of +27.31 SR pts versus context expectation). | Context-adjusted expectation: 163.25 Strike Rate, derived from stratified 12-cell baselines across phase, tournament tier, and innings.
- **Conservative Diagnostic Score:** BAT_CONSERVATIVE = +2.25 SR pts. Represents the 84% 1-sided credible lower bound (posterior mean minus 1.0 SE), inherently penalizing estimation uncertainty.
- **Uncertainty & CI:** Posterior standard error: $\pm$13.98 SR pts. Shrinkage weight $r = 0.820$. | 95% Credible Interval: [-11.17, 43.63] SR pts (width: 54.80 SR pts).
- **Competition Support:** Coverage: BOTH (144 balls in IPL, 68 balls in Senior T20I | Classification: `DUAL_TOURNAMENT_QUALIFIED`). Supported by substantial sample in both competitions. Note: Dual-tournament qualification indicates sample exposure availability in both competitions, NOT statistical proof of cross-competition skill transferability.
- **Key Limitations:** Robust sample volume and multi-season stability; residual uncertainty bounded by 95% CI.
- **Sensitivity Profile:** Under unpenalized posterior mean, performance is +16.23 SR pts. Model credibility against baseline: 87.7%; against league-wide pressure mean (prior mean $\mu = -34.24 SR pts$): 100.0%. Exceeding league average under pressure compares against degraded match conditions, NOT fellow shortlisted candidates. Exploratory PRI without TCF: 95.2; Experimental PRI with TCF: 83.4.

### #2 — Donovan Ferreira (`POSITIVE_CONSERVATIVE_EVIDENCE (MEDIUM_VOLUME)`)
- **Why Considered:** Ranked #2 in Batting with a conservative diagnostic value of +0.93 SR pts. Two-Dimensional Classification: 'POSITIVE_CONSERVATIVE_EVIDENCE (MEDIUM_VOLUME)' (Evidence Status: `POSITIVE_CONSERVATIVE_EVIDENCE`, Volume: `MEDIUM_VOLUME`, Cohort: `CONFIRMED_POSITIVE_RELIABILITY`). Sample qualification: QUALIFIED (legacy: 'STRONG_EVIDENCE').
- **Evidence Volume:** 84 legal pressure deliveries bowled/faced, categorized in 'MEDIUM_VOLUME' (Volume Tier B).
- **Temporal Stability:** Demonstrated across 13 unique pressure matches and 4 active seasons (Distribution: 2023: 14b, 2024: 8b, 2025: 18b, 2026: 44b).
- **Observed vs Expected:** Observed Strike Rate: 220.24 (raw difference of +51.60 SR pts versus context expectation). | Context-adjusted expectation: 168.64 Strike Rate, derived from stratified 12-cell baselines across phase, tournament tier, and innings.
- **Conservative Diagnostic Score:** BAT_CONSERVATIVE = +0.93 SR pts. Represents the 84% 1-sided credible lower bound (posterior mean minus 1.0 SE), inherently penalizing estimation uncertainty.
- **Uncertainty & CI:** Posterior standard error: $\pm$19.76 SR pts. Shrinkage weight $r = 0.640$. | 95% Credible Interval: [-18.05, 59.43] SR pts (width: 77.47 SR pts).
- **Competition Support:** Coverage: BOTH (55 balls in IPL, 29 balls in Senior T20I | Classification: `IPL_QUALIFIED`). Limited cross-competition sample overlap. Note: Dual-tournament qualification indicates sample exposure availability in both competitions, NOT statistical proof of cross-competition skill transferability.
- **Key Limitations:** Moderate sample volume (84 balls; estimation CI width is 77.5 SR pts); Heavily skewed towards IPL; cross-league transferability is not guaranteed.
- **Sensitivity Profile:** Under unpenalized posterior mean, performance is +20.69 SR pts. Model credibility against baseline: 85.2%; against league-wide pressure mean (prior mean $\mu = -34.24 SR pts$): 99.7%. Exceeding league average under pressure compares against degraded match conditions, NOT fellow shortlisted candidates. Exploratory PRI without TCF: 98.1; Experimental PRI with TCF: 94.7.

### #3 — Tim David (`NEGATIVE_CONSERVATIVE_ESTIMATE (HIGH_VOLUME)`)
- **Why Considered:** Ranked #3 in Batting with a conservative diagnostic value of -2.53 SR pts. Two-Dimensional Classification: 'NEGATIVE_CONSERVATIVE_ESTIMATE (HIGH_VOLUME)' (Evidence Status: `NEGATIVE_CONSERVATIVE_ESTIMATE`, Volume: `HIGH_VOLUME`, Cohort: `ESTABLISHED_MARGINAL_PERFORMER`). Sample qualification: QUALIFIED (legacy: 'STRONG_EVIDENCE').
- **Evidence Volume:** 290 legal pressure deliveries bowled/faced, categorized in 'HIGH_VOLUME' (Volume Tier B).
- **Temporal Stability:** Demonstrated across 33 unique pressure matches and 5 active seasons (Distribution: 2022: 50b, 2023: 24b, 2024: 89b, 2025: 109b, 2026: 18b).
- **Observed vs Expected:** Observed Strike Rate: 190.34 (raw difference of +16.42 SR pts versus context expectation). | Context-adjusted expectation: 173.93 Strike Rate, derived from stratified 12-cell baselines across phase, tournament tier, and innings.
- **Conservative Diagnostic Score:** BAT_CONSERVATIVE = -2.53 SR pts. Represents the 84% 1-sided credible lower bound (posterior mean minus 1.0 SE), inherently penalizing estimation uncertainty.
- **Uncertainty & CI:** Posterior standard error: $\pm$12.10 SR pts. Shrinkage weight $r = 0.865$. | 95% Credible Interval: [-14.14, 33.30] SR pts (width: 47.44 SR pts).
- **Competition Support:** Coverage: BOTH (198 balls in IPL, 92 balls in Senior T20I | Classification: `DUAL_TOURNAMENT_QUALIFIED`). Supported by substantial sample in both competitions. Note: Dual-tournament qualification indicates sample exposure availability in both competitions, NOT statistical proof of cross-competition skill transferability.
- **Key Limitations:** Robust sample volume and multi-season stability; residual uncertainty bounded by 95% CI.
- **Sensitivity Profile:** Under unpenalized posterior mean, performance is +9.58 SR pts. Model credibility against baseline: 78.6%; against league-wide pressure mean (prior mean $\mu = -34.24 SR pts$): 100.0%. Exceeding league average under pressure compares against degraded match conditions, NOT fellow shortlisted candidates. Exploratory PRI without TCF: 89.6; Experimental PRI with TCF: 95.5.

### #4 — Dinesh Karthik (`NEGATIVE_CONSERVATIVE_ESTIMATE (HIGH_VOLUME)`)
- **Why Considered:** Ranked #4 in Batting with a conservative diagnostic value of -2.67 SR pts. Two-Dimensional Classification: 'NEGATIVE_CONSERVATIVE_ESTIMATE (HIGH_VOLUME)' (Evidence Status: `NEGATIVE_CONSERVATIVE_ESTIMATE`, Volume: `HIGH_VOLUME`, Cohort: `ESTABLISHED_MARGINAL_PERFORMER`). Sample qualification: QUALIFIED (legacy: 'STRONG_EVIDENCE').
- **Evidence Volume:** 260 legal pressure deliveries bowled/faced, categorized in 'HIGH_VOLUME' (Volume Tier B).
- **Temporal Stability:** Demonstrated across 30 unique pressure matches and 3 active seasons (Distribution: 2022: 122b, 2022/23: 6b, 2023: 35b, 2024: 97b).
- **Observed vs Expected:** Observed Strike Rate: 194.62 (raw difference of +15.79 SR pts versus context expectation). | Context-adjusted expectation: 178.83 Strike Rate, derived from stratified 12-cell baselines across phase, tournament tier, and innings.
- **Conservative Diagnostic Score:** BAT_CONSERVATIVE = -2.67 SR pts. Represents the 84% 1-sided credible lower bound (posterior mean minus 1.0 SE), inherently penalizing estimation uncertainty.
- **Uncertainty & CI:** Posterior standard error: $\pm$11.91 SR pts. Shrinkage weight $r = 0.869$. | 95% Credible Interval: [-14.10, 32.59] SR pts (width: 46.69 SR pts).
- **Competition Support:** Coverage: BOTH (194 balls in IPL, 66 balls in Senior T20I | Classification: `DUAL_TOURNAMENT_QUALIFIED`). Supported by substantial sample in both competitions. Note: Dual-tournament qualification indicates sample exposure availability in both competitions, NOT statistical proof of cross-competition skill transferability.
- **Key Limitations:** Robust sample volume and multi-season stability; residual uncertainty bounded by 95% CI.
- **Sensitivity Profile:** Under unpenalized posterior mean, performance is +9.24 SR pts. Model credibility against baseline: 78.1%; against league-wide pressure mean (prior mean $\mu = -34.24 SR pts$): 100.0%. Exceeding league average under pressure compares against degraded match conditions, NOT fellow shortlisted candidates. Exploratory PRI without TCF: 92.6; Experimental PRI with TCF: 86.9.

### #5 — Ashutosh Sharma (`NEGATIVE_CONSERVATIVE_ESTIMATE (HIGH_VOLUME)`)
- **Why Considered:** Ranked #5 in Batting with a conservative diagnostic value of -3.63 SR pts. Two-Dimensional Classification: 'NEGATIVE_CONSERVATIVE_ESTIMATE (HIGH_VOLUME)' (Evidence Status: `NEGATIVE_CONSERVATIVE_ESTIMATE`, Volume: `HIGH_VOLUME`, Cohort: `ESTABLISHED_MARGINAL_PERFORMER`). Sample qualification: QUALIFIED (legacy: 'STRONG_EVIDENCE').
- **Evidence Volume:** 191 legal pressure deliveries bowled/faced, categorized in 'HIGH_VOLUME' (Volume Tier B).
- **Temporal Stability:** Demonstrated across 20 unique pressure matches and 3 active seasons (Distribution: 2024: 73b, 2025: 69b, 2026: 49b).
- **Observed vs Expected:** Observed Strike Rate: 197.38 (raw difference of +19.99 SR pts versus context expectation). | Context-adjusted expectation: 177.39 Strike Rate, derived from stratified 12-cell baselines across phase, tournament tier, and innings.
- **Conservative Diagnostic Score:** BAT_CONSERVATIVE = -3.63 SR pts. Represents the 84% 1-sided credible lower bound (posterior mean minus 1.0 SE), inherently penalizing estimation uncertainty.
- **Uncertainty & CI:** Posterior standard error: $\pm$13.93 SR pts. Shrinkage weight $r = 0.821$. | 95% Credible Interval: [-16.99, 37.59] SR pts (width: 54.59 SR pts).
- **Competition Support:** Coverage: IPL_ONLY (191 balls in IPL, 0 balls in Senior T20I | Classification: `IPL_QUALIFIED`). Limited cross-competition sample overlap. Note: Dual-tournament qualification indicates sample exposure availability in both competitions, NOT statistical proof of cross-competition skill transferability.
- **Key Limitations:** Heavily skewed towards IPL; cross-league transferability is not guaranteed.
- **Sensitivity Profile:** Under unpenalized posterior mean, performance is +10.30 SR pts. Model credibility against baseline: 77.0%; against league-wide pressure mean (prior mean $\mu = -34.24 SR pts$): 99.9%. Exceeding league average under pressure compares against degraded match conditions, NOT fellow shortlisted candidates. Exploratory PRI without TCF: 91.3; Experimental PRI with TCF: 87.5.

### #6 — Marcus Stoinis (`NEGATIVE_CONSERVATIVE_ESTIMATE (HIGH_VOLUME)`)
- **Why Considered:** Ranked #6 in Batting with a conservative diagnostic value of -5.77 SR pts. Two-Dimensional Classification: 'NEGATIVE_CONSERVATIVE_ESTIMATE (HIGH_VOLUME)' (Evidence Status: `NEGATIVE_CONSERVATIVE_ESTIMATE`, Volume: `HIGH_VOLUME`, Cohort: `ESTABLISHED_MARGINAL_PERFORMER`). Sample qualification: QUALIFIED (legacy: 'STRONG_EVIDENCE').
- **Evidence Volume:** 220 legal pressure deliveries bowled/faced, categorized in 'HIGH_VOLUME' (Volume Tier B).
- **Temporal Stability:** Demonstrated across 32 unique pressure matches and 5 active seasons (Distribution: 2022: 61b, 2023: 28b, 2024: 12b, 2025: 71b, 2026: 48b).
- **Observed vs Expected:** Observed Strike Rate: 181.36 (raw difference of +14.54 SR pts versus context expectation). | Context-adjusted expectation: 166.83 Strike Rate, derived from stratified 12-cell baselines across phase, tournament tier, and innings.
- **Conservative Diagnostic Score:** BAT_CONSERVATIVE = -5.77 SR pts. Represents the 84% 1-sided credible lower bound (posterior mean minus 1.0 SE), inherently penalizing estimation uncertainty.
- **Uncertainty & CI:** Posterior standard error: $\pm$12.87 SR pts. Shrinkage weight $r = 0.847$. | 95% Credible Interval: [-18.13, 32.31] SR pts (width: 50.44 SR pts).
- **Competition Support:** Coverage: BOTH (156 balls in IPL, 64 balls in Senior T20I | Classification: `DUAL_TOURNAMENT_QUALIFIED`). Supported by substantial sample in both competitions. Note: Dual-tournament qualification indicates sample exposure availability in both competitions, NOT statistical proof of cross-competition skill transferability.
- **Key Limitations:** Robust sample volume and multi-season stability; residual uncertainty bounded by 95% CI.
- **Sensitivity Profile:** Under unpenalized posterior mean, performance is +7.09 SR pts. Model credibility against baseline: 70.9%; against league-wide pressure mean (prior mean $\mu = -34.24 SR pts$): 99.9%. Exceeding league average under pressure compares against degraded match conditions, NOT fellow shortlisted candidates. Exploratory PRI without TCF: 90.0; Experimental PRI with TCF: 78.8.

### #7 — Naman Dhir (`NEGATIVE_CONSERVATIVE_ESTIMATE (MEDIUM_VOLUME)`)
- **Why Considered:** Ranked #7 in Batting with a conservative diagnostic value of -6.91 SR pts. Two-Dimensional Classification: 'NEGATIVE_CONSERVATIVE_ESTIMATE (MEDIUM_VOLUME)' (Evidence Status: `NEGATIVE_CONSERVATIVE_ESTIMATE`, Volume: `MEDIUM_VOLUME`, Cohort: `ESTABLISHED_MARGINAL_PERFORMER`). Sample qualification: QUALIFIED (legacy: 'STRONG_EVIDENCE').
- **Evidence Volume:** 145 legal pressure deliveries bowled/faced, categorized in 'MEDIUM_VOLUME' (Volume Tier B).
- **Temporal Stability:** Demonstrated across 18 unique pressure matches and 3 active seasons (Distribution: 2024: 28b, 2025: 68b, 2026: 49b).
- **Observed vs Expected:** Observed Strike Rate: 193.79 (raw difference of +18.72 SR pts versus context expectation). | Context-adjusted expectation: 175.07 Strike Rate, derived from stratified 12-cell baselines across phase, tournament tier, and innings.
- **Conservative Diagnostic Score:** BAT_CONSERVATIVE = -6.91 SR pts. Represents the 84% 1-sided credible lower bound (posterior mean minus 1.0 SE), inherently penalizing estimation uncertainty.
- **Uncertainty & CI:** Posterior standard error: $\pm$14.86 SR pts. Shrinkage weight $r = 0.797$. | 95% Credible Interval: [-21.17, 37.07] SR pts (width: 58.23 SR pts).
- **Competition Support:** Coverage: BOTH (118 balls in IPL, 27 balls in Senior T20I | Classification: `IPL_QUALIFIED`). Limited cross-competition sample overlap. Note: Dual-tournament qualification indicates sample exposure availability in both competitions, NOT statistical proof of cross-competition skill transferability.
- **Key Limitations:** Heavily skewed towards IPL; cross-league transferability is not guaranteed.
- **Sensitivity Profile:** Under unpenalized posterior mean, performance is +7.95 SR pts. Model credibility against baseline: 70.4%; against league-wide pressure mean (prior mean $\mu = -34.24 SR pts$): 99.8%. Exceeding league average under pressure compares against degraded match conditions, NOT fellow shortlisted candidates. Exploratory PRI without TCF: 92.6; Experimental PRI with TCF: 91.9.

### #8 — Rinku Singh (`NEGATIVE_CONSERVATIVE_ESTIMATE (HIGH_VOLUME)`)
- **Why Considered:** Ranked #8 in Batting with a conservative diagnostic value of -7.02 SR pts. Two-Dimensional Classification: 'NEGATIVE_CONSERVATIVE_ESTIMATE (HIGH_VOLUME)' (Evidence Status: `NEGATIVE_CONSERVATIVE_ESTIMATE`, Volume: `HIGH_VOLUME`, Cohort: `ESTABLISHED_MARGINAL_PERFORMER`). Sample qualification: QUALIFIED (legacy: 'STRONG_EVIDENCE').
- **Evidence Volume:** 363 legal pressure deliveries bowled/faced, categorized in 'HIGH_VOLUME' (Volume Tier B).
- **Temporal Stability:** Demonstrated across 48 unique pressure matches and 5 active seasons (Distribution: 2022: 50b, 2023: 140b, 2024: 57b, 2025: 51b, 2026: 65b).
- **Observed vs Expected:** Observed Strike Rate: 181.27 (raw difference of +7.57 SR pts versus context expectation). | Context-adjusted expectation: 173.70 Strike Rate, derived from stratified 12-cell baselines across phase, tournament tier, and innings.
- **Conservative Diagnostic Score:** BAT_CONSERVATIVE = -7.02 SR pts. Represents the 84% 1-sided credible lower bound (posterior mean minus 1.0 SE), inherently penalizing estimation uncertainty.
- **Uncertainty & CI:** Posterior standard error: $\pm$10.41 SR pts. Shrinkage weight $r = 0.900$. | 95% Credible Interval: [-17.01, 23.79] SR pts (width: 40.80 SR pts).
- **Competition Support:** Coverage: BOTH (280 balls in IPL, 83 balls in Senior T20I | Classification: `DUAL_TOURNAMENT_QUALIFIED`). Supported by substantial sample in both competitions. Note: Dual-tournament qualification indicates sample exposure availability in both competitions, NOT statistical proof of cross-competition skill transferability.
- **Key Limitations:** Robust sample volume and multi-season stability; residual uncertainty bounded by 95% CI.
- **Sensitivity Profile:** Under unpenalized posterior mean, performance is +3.39 SR pts. Model credibility against baseline: 62.8%; against league-wide pressure mean (prior mean $\mu = -34.24 SR pts$): 100.0%. Exceeding league average under pressure compares against degraded match conditions, NOT fellow shortlisted candidates. Exploratory PRI without TCF: 87.9; Experimental PRI with TCF: 93.4.

### #9 — Tristan Stubbs (`NEGATIVE_CONSERVATIVE_ESTIMATE (HIGH_VOLUME)`)
- **Why Considered:** Ranked #9 in Batting with a conservative diagnostic value of -8.17 SR pts. Two-Dimensional Classification: 'NEGATIVE_CONSERVATIVE_ESTIMATE (HIGH_VOLUME)' (Evidence Status: `NEGATIVE_CONSERVATIVE_ESTIMATE`, Volume: `HIGH_VOLUME`, Cohort: `ESTABLISHED_MARGINAL_PERFORMER`). Sample qualification: QUALIFIED (legacy: 'STRONG_EVIDENCE').
- **Evidence Volume:** 266 legal pressure deliveries bowled/faced, categorized in 'HIGH_VOLUME' (Volume Tier B).
- **Temporal Stability:** Demonstrated across 33 unique pressure matches and 5 active seasons (Distribution: 2022: 11b, 2022/23: 1b, 2023: 13b, 2024: 94b, 2025: 71b, 2026: 76b).
- **Observed vs Expected:** Observed Strike Rate: 167.29 (raw difference of +6.55 SR pts versus context expectation). | Context-adjusted expectation: 160.74 Strike Rate, derived from stratified 12-cell baselines across phase, tournament tier, and innings.
- **Conservative Diagnostic Score:** BAT_CONSERVATIVE = -8.17 SR pts. Represents the 84% 1-sided credible lower bound (posterior mean minus 1.0 SE), inherently penalizing estimation uncertainty.
- **Uncertainty & CI:** Posterior standard error: $\pm$10.54 SR pts. Shrinkage weight $r = 0.898$. | 95% Credible Interval: [-18.29, 23.03] SR pts (width: 41.32 SR pts).
- **Competition Support:** Coverage: BOTH (169 balls in IPL, 97 balls in Senior T20I | Classification: `DUAL_TOURNAMENT_QUALIFIED`). Supported by substantial sample in both competitions. Note: Dual-tournament qualification indicates sample exposure availability in both competitions, NOT statistical proof of cross-competition skill transferability.
- **Key Limitations:** Robust sample volume and multi-season stability; residual uncertainty bounded by 95% CI.
- **Sensitivity Profile:** Under unpenalized posterior mean, performance is +2.37 SR pts. Model credibility against baseline: 58.9%; against league-wide pressure mean (prior mean $\mu = -34.24 SR pts$): 100.0%. Exceeding league average under pressure compares against degraded match conditions, NOT fellow shortlisted candidates. Exploratory PRI without TCF: 89.4; Experimental PRI with TCF: 86.5.

### #10 — Sherfane Rutherford (`NEGATIVE_CONSERVATIVE_ESTIMATE (HIGH_VOLUME)`)
- **Why Considered:** Ranked #10 in Batting with a conservative diagnostic value of -8.18 SR pts. Two-Dimensional Classification: 'NEGATIVE_CONSERVATIVE_ESTIMATE (HIGH_VOLUME)' (Evidence Status: `NEGATIVE_CONSERVATIVE_ESTIMATE`, Volume: `HIGH_VOLUME`, Cohort: `ESTABLISHED_MARGINAL_PERFORMER`). Sample qualification: QUALIFIED (legacy: 'STRONG_EVIDENCE').
- **Evidence Volume:** 151 legal pressure deliveries bowled/faced, categorized in 'HIGH_VOLUME' (Volume Tier B).
- **Temporal Stability:** Demonstrated across 21 unique pressure matches and 5 active seasons (Distribution: 2022: 16b, 2023: 8b, 2024: 43b, 2025: 25b, 2026: 59b).
- **Observed vs Expected:** Observed Strike Rate: 178.15 (raw difference of +17.93 SR pts versus context expectation). | Context-adjusted expectation: 160.21 Strike Rate, derived from stratified 12-cell baselines across phase, tournament tier, and innings.
- **Conservative Diagnostic Score:** BAT_CONSERVATIVE = -8.18 SR pts. Represents the 84% 1-sided credible lower bound (posterior mean minus 1.0 SE), inherently penalizing estimation uncertainty.
- **Uncertainty & CI:** Posterior standard error: $\pm$15.12 SR pts. Shrinkage weight $r = 0.789$. | 95% Credible Interval: [-22.69, 36.57] SR pts (width: 59.26 SR pts).
- **Competition Support:** Coverage: BOTH (40 balls in IPL, 111 balls in Senior T20I | Classification: `DUAL_TOURNAMENT_QUALIFIED`). Supported by substantial sample in both competitions. Note: Dual-tournament qualification indicates sample exposure availability in both competitions, NOT statistical proof of cross-competition skill transferability.
- **Key Limitations:** Robust sample volume and multi-season stability; residual uncertainty bounded by 95% CI.
- **Sensitivity Profile:** Under unpenalized posterior mean, performance is +6.94 SR pts. Model credibility against baseline: 67.7%; against league-wide pressure mean (prior mean $\mu = -34.24 SR pts$): 99.7%. Exceeding league average under pressure compares against degraded match conditions, NOT fellow shortlisted candidates. Exploratory PRI without TCF: 89.2; Experimental PRI with TCF: 78.1.

---

## 3. Promising Candidates Watchlist (Emerging vs Established Cohorts)

Audit finding DEF-03 remediation: The promising cohort is explicitly separated into genuine emerging talents and established veterans with marginal effects:

### A. Emerging High-Upside Candidates (`EMERGING_HIGH_UPSIDE` — $30 \le n < 60$ balls, positive posterior mean):
These emerging players have high estimated overperformance under pressure but limited exposure volume ($< 60$ balls), retaining higher estimation variance:

| Batter Name | Posterior Mean $\hat{\theta}$ | Posterior SE | Conservative Bound | Pressure Balls | Matches | Volume Tier | Watchlist Cohort | Two-Dimensional Status |
| :--- | ---: | ---: | ---: | ---: | ---: | :--- | :--- | :--- |
| **Cooper Connolly** | +11.9 SR | $\pm$22.6 | -10.7 SR | 50 | 4 | `LOW_VOLUME` | `EMERGING_HIGH_UPSIDE` | `NEGATIVE_CONSERVATIVE_ESTIMATE (LOW_VOLUME)` |
| **Ishan Kishan** | +2.0 SR | $\pm$21.6 | -19.5 SR | 52 | 9 | `LOW_VOLUME` | `EMERGING_HIGH_UPSIDE` | `NEGATIVE_CONSERVATIVE_ESTIMATE (LOW_VOLUME)` |

### B. Established Marginal Performers (`ESTABLISHED_MARGINAL_PERFORMER` — $n \ge 60$ balls, positive posterior mean, conservative bound $\le 0$):
Established multi-season veterans who maintain positive posterior strike rates but whose 1-sigma uncertainty bound crosses zero:

| Batter Name | Posterior Mean $\hat{\theta}$ | Posterior SE | Conservative Bound | Pressure Balls | Matches | Volume Tier | Watchlist Cohort | Two-Dimensional Status |
| :--- | ---: | ---: | ---: | ---: | ---: | :--- | :--- | :--- |
| **Tim David** | +9.6 SR | $\pm$12.1 | -2.5 SR | 290 | 33 | `HIGH_VOLUME` | `ESTABLISHED_MARGINAL_PERFORMER` | `NEGATIVE_CONSERVATIVE_ESTIMATE (HIGH_VOLUME)` |
| **Dinesh Karthik** | +9.2 SR | $\pm$11.9 | -2.7 SR | 260 | 30 | `HIGH_VOLUME` | `ESTABLISHED_MARGINAL_PERFORMER` | `NEGATIVE_CONSERVATIVE_ESTIMATE (HIGH_VOLUME)` |
| **Ashutosh Sharma** | +10.3 SR | $\pm$13.9 | -3.6 SR | 191 | 20 | `HIGH_VOLUME` | `ESTABLISHED_MARGINAL_PERFORMER` | `NEGATIVE_CONSERVATIVE_ESTIMATE (HIGH_VOLUME)` |
| **Marcus Stoinis** | +7.1 SR | $\pm$12.9 | -5.8 SR | 220 | 32 | `HIGH_VOLUME` | `ESTABLISHED_MARGINAL_PERFORMER` | `NEGATIVE_CONSERVATIVE_ESTIMATE (HIGH_VOLUME)` |
| **Naman Dhir** | +7.9 SR | $\pm$14.9 | -6.9 SR | 145 | 18 | `MEDIUM_VOLUME` | `ESTABLISHED_MARGINAL_PERFORMER` | `NEGATIVE_CONSERVATIVE_ESTIMATE (MEDIUM_VOLUME)` |
| **Rinku Singh** | +3.4 SR | $\pm$10.4 | -7.0 SR | 363 | 48 | `HIGH_VOLUME` | `ESTABLISHED_MARGINAL_PERFORMER` | `NEGATIVE_CONSERVATIVE_ESTIMATE (HIGH_VOLUME)` |
| **Tristan Stubbs** | +2.4 SR | $\pm$10.5 | -8.2 SR | 266 | 33 | `HIGH_VOLUME` | `ESTABLISHED_MARGINAL_PERFORMER` | `NEGATIVE_CONSERVATIVE_ESTIMATE (HIGH_VOLUME)` |
| **Sherfane Rutherford** | +6.9 SR | $\pm$15.1 | -8.2 SR | 151 | 21 | `HIGH_VOLUME` | `ESTABLISHED_MARGINAL_PERFORMER` | `NEGATIVE_CONSERVATIVE_ESTIMATE (HIGH_VOLUME)` |
| **Rovman Powell** | +1.7 SR | $\pm$10.5 | -8.8 SR | 342 | 47 | `HIGH_VOLUME` | `ESTABLISHED_MARGINAL_PERFORMER` | `NEGATIVE_CONSERVATIVE_ESTIMATE (HIGH_VOLUME)` |
| **Aiden Markram** | +5.7 SR | $\pm$14.7 | -9.0 SR | 133 | 13 | `MEDIUM_VOLUME` | `ESTABLISHED_MARGINAL_PERFORMER` | `NEGATIVE_CONSERVATIVE_ESTIMATE (MEDIUM_VOLUME)` |
| **Andre Russell** | +1.2 SR | $\pm$12.1 | -10.9 SR | 294 | 29 | `HIGH_VOLUME` | `ESTABLISHED_MARGINAL_PERFORMER` | `NEGATIVE_CONSERVATIVE_ESTIMATE (HIGH_VOLUME)` |
| **Shashank Singh** | +1.3 SR | $\pm$12.4 | -11.1 SR | 199 | 21 | `HIGH_VOLUME` | `ESTABLISHED_MARGINAL_PERFORMER` | `NEGATIVE_CONSERVATIVE_ESTIMATE (HIGH_VOLUME)` |
| **Rahul Tewatia** | +1.7 SR | $\pm$13.1 | -11.4 SR | 195 | 27 | `HIGH_VOLUME` | `ESTABLISHED_MARGINAL_PERFORMER` | `NEGATIVE_CONSERVATIVE_ESTIMATE (HIGH_VOLUME)` |
| **Suryakumar Yadav** | +1.4 SR | $\pm$13.6 | -12.2 SR | 199 | 23 | `HIGH_VOLUME` | `ESTABLISHED_MARGINAL_PERFORMER` | `NEGATIVE_CONSERVATIVE_ESTIMATE (HIGH_VOLUME)` |
| **Mohammad Nabi** | +1.6 SR | $\pm$13.8 | -12.3 SR | 172 | 21 | `HIGH_VOLUME` | `ESTABLISHED_MARGINAL_PERFORMER` | `NEGATIVE_CONSERVATIVE_ESTIMATE (HIGH_VOLUME)` |
| **Shreyas Iyer** | +1.0 SR | $\pm$15.9 | -14.9 SR | 116 | 19 | `MEDIUM_VOLUME` | `ESTABLISHED_MARGINAL_PERFORMER` | `NEGATIVE_CONSERVATIVE_ESTIMATE (MEDIUM_VOLUME)` |
| **Ramandeep Singh** | +0.9 SR | $\pm$18.0 | -17.1 SR | 93 | 17 | `MEDIUM_VOLUME` | `ESTABLISHED_MARGINAL_PERFORMER` | `NEGATIVE_CONSERVATIVE_ESTIMATE (MEDIUM_VOLUME)` |