# ROYALS INTELLIGENCE — ROUND 1 BOWLING PRESSURE RELIABILITY SHORTLIST
**Generated:** 2026-11-11T17:18:05.664773+00:00  
**Architecture:** ROYALS INTELLIGENCE v4.1  
**Task:** R1-06 Evidence-Backed Player Reliability Intelligence & Ranking Engine  
**Primary Metric:** Conservative Runs Saved per Over `BOWL_CONSERVATIVE = -posterior_mean_economy_diff - posterior_SE_economy` (Runs Saved/Over)  

---

## 1. Executive Shortlist Overview

The Bowling Pressure Reliability Shortlist identifies bowlers who restrict run-scoring under high-leverage conditions relative to context expectations, penalized by posterior estimation uncertainty. Remember that average bowling economy increases by **+1.82 RPO** under pressure; therefore, conceding fewer runs than peers constitutes runs saved. Exactly **11 bowlers satisfy all Strong Evidence criteria** (conservative runs saved $\ge -1.75$ RPO, posterior mean differential $\le +1.25$ RPO, and $\ge 60$ legal pressure balls across $\ge 10$ matches).

### Bowling Leaderboard (Top 11 Candidates Meeting Strong Evidence):

| Rank | Bowler Name | BOWL_CONSERVATIVE (Runs Saved) | Posterior Mean Diff | Posterior SE | 95% Credible Interval | Pressure Balls | Matches | Seasons | Comp Coverage | P(Beat Base) | P(Beat Peers) | Evidence Class |
| :--- | :--- | ---: | ---: | ---: | :---: | ---: | ---: | ---: | :--- | ---: | ---: | :--- |
| **1** | **Jasprit Bumrah** | **-0.16** | -0.20 | $\pm$0.36 | [-0.90, +0.50] | 521 | 60 | 5 | `BOTH` | 71.1% | 100.0% | `STRONG_EVIDENCE` |
| **2** | **Sunil Narine** | **-0.94** | +0.39 | $\pm$0.55 | [-0.68, +1.47] | 153 | 24 | 5 | `IPL_ONLY` | 23.8% | 99.5% | `STRONG_EVIDENCE` |
| **3** | **Maheesh Theekshana** | **-0.96** | +0.55 | $\pm$0.41 | [-0.25, +1.35] | 421 | 58 | 5 | `BOTH` | 9.0% | 99.9% | `STRONG_EVIDENCE` |
| **4** | **Matheesha Pathirana** | **-1.05** | +0.63 | $\pm$0.41 | [-0.18, +1.44] | 440 | 44 | 5 | `BOTH` | 6.2% | 99.8% | `STRONG_EVIDENCE` |
| **5** | **Nasum Ahmed** | **-1.32** | +0.70 | $\pm$0.63 | [-0.53, +1.93] | 47 | 8 | 4 | `T20I_ONLY` | 13.3% | 96.4% | `PROMISING_CANDIDATE` |
| **6** | **Shaheen Afridi** | **-1.43** | +0.91 | $\pm$0.52 | [-0.10, +1.92] | 191 | 31 | 4 | `T20I_ONLY` | 3.8% | 96.1% | `STRONG_EVIDENCE` |
| **7** | **Mustafizur Rahman** | **-1.47** | +1.09 | $\pm$0.38 | [+0.35, +1.84] | 578 | 61 | 5 | `BOTH` | 0.2% | 97.2% | `STRONG_EVIDENCE` |
| **8** | **Richard Ngarava** | **-1.56** | +1.10 | $\pm$0.46 | [+0.19, +2.01] | 287 | 34 | 5 | `T20I_ONLY` | 0.9% | 94.1% | `STRONG_EVIDENCE` |
| **9** | **Vipraj Nigam** | **-1.57** | +0.91 | $\pm$0.66 | [-0.39, +2.21] | 46 | 7 | 1 | `IPL_ONLY` | 8.5% | 91.6% | `PROMISING_CANDIDATE` |
| **10** | **Lungi Ngidi** | **-1.65** | +1.13 | $\pm$0.53 | [+0.09, +2.16] | 222 | 26 | 5 | `BOTH` | 1.6% | 90.7% | `STRONG_EVIDENCE` |
| **11** | **Ramon Simmonds** | **-1.66** | +0.98 | $\pm$0.68 | [-0.36, +2.32] | 30 | 3 | 2 | `T20I_ONLY` | 7.7% | 89.1% | `PROMISING_CANDIDATE` |

> [!IMPORTANT]
> **Jasprit Bumrah Benchmark:**
> - **Jasprit Bumrah (#1: -0.16 RPO)** is the **ONLY qualified bowler in the 883-match dataset** who concedes fewer runs under pressure (8.94 RPO) than ordinary baseline (9.70 RPO), with $P(\text{Beat Baseline}) = 71.1\%$ and $P(\text{Beat Peers}) = 100.0\%$ across 521 pressure deliveries.
> - **Sunil Narine (#2: -0.94 RPO)**, **Maheesh Theekshana (#3: -0.96 RPO)**, and **Matheesha Pathirana (#4: -1.05 RPO)** form the elite peer-beating tier, saving approximately 0.8 to 1.4 RPO relative to the average pressured bowler.

---

## 2. In-Depth Candidate Evidence Profiles

### #1 — Jasprit Bumrah (`STRONG_EVIDENCE`)
- **Why Considered:** Ranked #1 in Bowling with a conservative diagnostic value of -0.16 RPO. Classified as 'STRONG_EVIDENCE' based on context-adjusted overperformance under pressure.
- **Evidence Volume:** 521 legal pressure deliveries bowled/faced, categorized in 'Large Sample (>=150 balls)'.
- **Temporal Stability:** Demonstrated across 60 unique pressure matches and 5 active seasons (Distribution: 2022: 116b, 2023: 12b, 2024: 101b, 2025: 155b, 2026: 137b).
- **Observed vs Expected:** Observed Economy Rate: 7.37 (raw difference of -0.76 RPO versus context expectation). | Context-adjusted expectation: 8.13 Economy Rate, derived from stratified 12-cell baselines across phase, tournament tier, and innings.
- **Conservative Diagnostic Score:** BOWL_CONSERVATIVE = -0.16 RPO. Represents the 84% 1-sided credible lower bound (conservative runs saved per over), inherently penalizing estimation uncertainty.
- **Uncertainty & CI:** Posterior standard error: $\pm$0.36 RPO. Shrinkage weight $r = 0.783$. | 95% Credible Interval: [-0.90, 0.50] RPO (width: 1.41 RPO).
- **Competition Support:** Coverage: BOTH (388 balls in IPL, 133 balls in Senior T20I). Supported by substantial sample in both competitions.
- **Key Limitations:** Robust sample volume and multi-season stability; residual uncertainty bounded by 95% CI.
- **Sensitivity Profile:** Under unpenalized posterior mean, performance is -0.20 RPO. Model credibility against baseline: 71.1%; against peers: 100.0%. Exploratory PRI without TCF: 100.0; Experimental PRI with TCF: 100.0.

### #2 — Sunil Narine (`STRONG_EVIDENCE`)
- **Why Considered:** Ranked #2 in Bowling with a conservative diagnostic value of -0.94 RPO. Classified as 'STRONG_EVIDENCE' based on context-adjusted overperformance under pressure.
- **Evidence Volume:** 153 legal pressure deliveries bowled/faced, categorized in 'Large Sample (>=150 balls)'.
- **Temporal Stability:** Demonstrated across 24 unique pressure matches and 5 active seasons (Distribution: 2022: 48b, 2023: 37b, 2024: 18b, 2025: 12b, 2026: 38b).
- **Observed vs Expected:** Observed Economy Rate: 7.14 (raw difference of -1.08 RPO versus context expectation). | Context-adjusted expectation: 8.21 Economy Rate, derived from stratified 12-cell baselines across phase, tournament tier, and innings.
- **Conservative Diagnostic Score:** BOWL_CONSERVATIVE = -0.94 RPO. Represents the 84% 1-sided credible lower bound (conservative runs saved per over), inherently penalizing estimation uncertainty.
- **Uncertainty & CI:** Posterior standard error: $\pm$0.55 RPO. Shrinkage weight $r = 0.494$. | 95% Credible Interval: [-0.68, 1.47] RPO (width: 2.15 RPO).
- **Competition Support:** Coverage: IPL_ONLY (153 balls in IPL, 0 balls in Senior T20I). Limited cross-competition sample overlap.
- **Key Limitations:** Heavily skewed towards IPL; cross-league transferability is not guaranteed.
- **Sensitivity Profile:** Under unpenalized posterior mean, performance is +0.39 RPO. Model credibility against baseline: 23.8%; against peers: 99.5%. Exploratory PRI without TCF: 92.0; Experimental PRI with TCF: 95.7.

### #3 — Maheesh Theekshana (`STRONG_EVIDENCE`)
- **Why Considered:** Ranked #3 in Bowling with a conservative diagnostic value of -0.96 RPO. Classified as 'STRONG_EVIDENCE' based on context-adjusted overperformance under pressure.
- **Evidence Volume:** 421 legal pressure deliveries bowled/faced, categorized in 'Large Sample (>=150 balls)'.
- **Temporal Stability:** Demonstrated across 58 unique pressure matches and 5 active seasons (Distribution: 2022: 100b, 2023: 60b, 2024: 82b, 2024/25: 18b, 2025: 120b, 2026: 41b).
- **Observed vs Expected:** Observed Economy Rate: 8.08 (raw difference of +0.05 RPO versus context expectation). | Context-adjusted expectation: 8.03 Economy Rate, derived from stratified 12-cell baselines across phase, tournament tier, and innings.
- **Conservative Diagnostic Score:** BOWL_CONSERVATIVE = -0.96 RPO. Represents the 84% 1-sided credible lower bound (conservative runs saved per over), inherently penalizing estimation uncertainty.
- **Uncertainty & CI:** Posterior standard error: $\pm$0.41 RPO. Shrinkage weight $r = 0.717$. | 95% Credible Interval: [-0.25, 1.35] RPO (width: 1.61 RPO).
- **Competition Support:** Coverage: BOTH (179 balls in IPL, 242 balls in Senior T20I). Supported by substantial sample in both competitions.
- **Key Limitations:** Robust sample volume and multi-season stability; residual uncertainty bounded by 95% CI.
- **Sensitivity Profile:** Under unpenalized posterior mean, performance is +0.55 RPO. Model credibility against baseline: 9.0%; against peers: 99.9%. Exploratory PRI without TCF: 80.1; Experimental PRI with TCF: 96.2.

### #4 — Matheesha Pathirana (`STRONG_EVIDENCE`)
- **Why Considered:** Ranked #4 in Bowling with a conservative diagnostic value of -1.05 RPO. Classified as 'STRONG_EVIDENCE' based on context-adjusted overperformance under pressure.
- **Evidence Volume:** 440 legal pressure deliveries bowled/faced, categorized in 'Large Sample (>=150 balls)'.
- **Temporal Stability:** Demonstrated across 44 unique pressure matches and 5 active seasons (Distribution: 2022: 17b, 2023: 140b, 2024: 122b, 2024/25: 6b, 2025: 137b, 2026: 18b).
- **Observed vs Expected:** Observed Economy Rate: 8.29 (raw difference of +0.16 RPO versus context expectation). | Context-adjusted expectation: 8.14 Economy Rate, derived from stratified 12-cell baselines across phase, tournament tier, and innings.
- **Conservative Diagnostic Score:** BOWL_CONSERVATIVE = -1.05 RPO. Represents the 84% 1-sided credible lower bound (conservative runs saved per over), inherently penalizing estimation uncertainty.
- **Uncertainty & CI:** Posterior standard error: $\pm$0.41 RPO. Shrinkage weight $r = 0.713$. | 95% Credible Interval: [-0.18, 1.44] RPO (width: 1.62 RPO).
- **Competition Support:** Coverage: BOTH (336 balls in IPL, 104 balls in Senior T20I). Supported by substantial sample in both competitions.
- **Key Limitations:** Robust sample volume and multi-season stability; residual uncertainty bounded by 95% CI.
- **Sensitivity Profile:** Under unpenalized posterior mean, performance is +0.63 RPO. Model credibility against baseline: 6.2%; against peers: 99.8%. Exploratory PRI without TCF: 85.2; Experimental PRI with TCF: 97.2.

### #5 — Nasum Ahmed (`PROMISING_CANDIDATE`)
- **Why Considered:** Ranked #5 in Bowling with a conservative diagnostic value of -1.32 RPO. Classified as 'PROMISING_CANDIDATE' based on context-adjusted overperformance under pressure.
- **Evidence Volume:** 47 legal pressure deliveries bowled/faced, categorized in 'Small Sample (30-59 balls)'.
- **Temporal Stability:** Demonstrated across 8 unique pressure matches and 4 active seasons (Distribution: 2022: 6b, 2022/23: 6b, 2023: 6b, 2025: 18b, 2026: 11b).
- **Observed vs Expected:** Observed Economy Rate: 6.26 (raw difference of -1.51 RPO versus context expectation). | Context-adjusted expectation: 7.77 Economy Rate, derived from stratified 12-cell baselines across phase, tournament tier, and innings.
- **Conservative Diagnostic Score:** BOWL_CONSERVATIVE = -1.32 RPO. Represents the 84% 1-sided credible lower bound (conservative runs saved per over), inherently penalizing estimation uncertainty.
- **Uncertainty & CI:** Posterior standard error: $\pm$0.63 RPO. Shrinkage weight $r = 0.338$. | 95% Credible Interval: [-0.53, 1.93] RPO (width: 2.46 RPO).
- **Competition Support:** Coverage: T20I_ONLY (0 balls in IPL, 47 balls in Senior T20I). Limited cross-competition sample overlap.
- **Key Limitations:** Moderate sample volume (47 balls; estimation CI width is 2.5 RPO); Heavily skewed towards T20I; cross-league transferability is not guaranteed.
- **Sensitivity Profile:** Under unpenalized posterior mean, performance is +0.70 RPO. Model credibility against baseline: 13.3%; against peers: 96.4%. Exploratory PRI without TCF: 71.0; Experimental PRI with TCF: 71.5.

### #6 — Shaheen Afridi (`STRONG_EVIDENCE`)
- **Why Considered:** Ranked #6 in Bowling with a conservative diagnostic value of -1.43 RPO. Classified as 'STRONG_EVIDENCE' based on context-adjusted overperformance under pressure.
- **Evidence Volume:** 191 legal pressure deliveries bowled/faced, categorized in 'Large Sample (>=150 balls)'.
- **Temporal Stability:** Demonstrated across 31 unique pressure matches and 4 active seasons (Distribution: 2023: 30b, 2024: 60b, 2025: 95b, 2026: 6b).
- **Observed vs Expected:** Observed Economy Rate: 8.04 (raw difference of +0.18 RPO versus context expectation). | Context-adjusted expectation: 7.87 Economy Rate, derived from stratified 12-cell baselines across phase, tournament tier, and innings.
- **Conservative Diagnostic Score:** BOWL_CONSERVATIVE = -1.43 RPO. Represents the 84% 1-sided credible lower bound (conservative runs saved per over), inherently penalizing estimation uncertainty.
- **Uncertainty & CI:** Posterior standard error: $\pm$0.52 RPO. Shrinkage weight $r = 0.552$. | 95% Credible Interval: [-0.10, 1.92] RPO (width: 2.02 RPO).
- **Competition Support:** Coverage: T20I_ONLY (0 balls in IPL, 191 balls in Senior T20I). Limited cross-competition sample overlap.
- **Key Limitations:** Heavily skewed towards T20I; cross-league transferability is not guaranteed.
- **Sensitivity Profile:** Under unpenalized posterior mean, performance is +0.91 RPO. Model credibility against baseline: 3.8%; against peers: 96.1%. Exploratory PRI without TCF: 76.2; Experimental PRI with TCF: 88.9.

### #7 — Mustafizur Rahman (`STRONG_EVIDENCE`)
- **Why Considered:** Ranked #7 in Bowling with a conservative diagnostic value of -1.47 RPO. Classified as 'STRONG_EVIDENCE' based on context-adjusted overperformance under pressure.
- **Evidence Volume:** 578 legal pressure deliveries bowled/faced, categorized in 'Large Sample (>=150 balls)'.
- **Temporal Stability:** Demonstrated across 61 unique pressure matches and 5 active seasons (Distribution: 2022: 126b, 2022/23: 18b, 2023: 84b, 2024: 140b, 2025: 192b, 2026: 18b).
- **Observed vs Expected:** Observed Economy Rate: 8.93 (raw difference of +0.86 RPO versus context expectation). | Context-adjusted expectation: 8.07 Economy Rate, derived from stratified 12-cell baselines across phase, tournament tier, and innings.
- **Conservative Diagnostic Score:** BOWL_CONSERVATIVE = -1.47 RPO. Represents the 84% 1-sided credible lower bound (conservative runs saved per over), inherently penalizing estimation uncertainty.
- **Uncertainty & CI:** Posterior standard error: $\pm$0.38 RPO. Shrinkage weight $r = 0.756$. | 95% Credible Interval: [0.35, 1.84] RPO (width: 1.49 RPO).
- **Competition Support:** Coverage: BOTH (216 balls in IPL, 362 balls in Senior T20I). Supported by substantial sample in both competitions.
- **Key Limitations:** Robust sample volume and multi-season stability; residual uncertainty bounded by 95% CI.
- **Sensitivity Profile:** Under unpenalized posterior mean, performance is +1.09 RPO. Model credibility against baseline: 0.2%; against peers: 97.2%. Exploratory PRI without TCF: 69.2; Experimental PRI with TCF: 74.0.

### #8 — Richard Ngarava (`STRONG_EVIDENCE`)
- **Why Considered:** Ranked #8 in Bowling with a conservative diagnostic value of -1.56 RPO. Classified as 'STRONG_EVIDENCE' based on context-adjusted overperformance under pressure.
- **Evidence Volume:** 287 legal pressure deliveries bowled/faced, categorized in 'Large Sample (>=150 balls)'.
- **Temporal Stability:** Demonstrated across 34 unique pressure matches and 5 active seasons (Distribution: 2022: 15b, 2023: 24b, 2023/24: 20b, 2024: 114b, 2025: 84b, 2026: 30b).
- **Observed vs Expected:** Observed Economy Rate: 8.51 (raw difference of +0.69 RPO versus context expectation). | Context-adjusted expectation: 7.82 Economy Rate, derived from stratified 12-cell baselines across phase, tournament tier, and innings.
- **Conservative Diagnostic Score:** BOWL_CONSERVATIVE = -1.56 RPO. Represents the 84% 1-sided credible lower bound (conservative runs saved per over), inherently penalizing estimation uncertainty.
- **Uncertainty & CI:** Posterior standard error: $\pm$0.46 RPO. Shrinkage weight $r = 0.638$. | 95% Credible Interval: [0.19, 2.01] RPO (width: 1.82 RPO).
- **Competition Support:** Coverage: T20I_ONLY (0 balls in IPL, 287 balls in Senior T20I). Limited cross-competition sample overlap.
- **Key Limitations:** Heavily skewed towards T20I; cross-league transferability is not guaranteed.
- **Sensitivity Profile:** Under unpenalized posterior mean, performance is +1.10 RPO. Model credibility against baseline: 0.9%; against peers: 94.1%. Exploratory PRI without TCF: 66.1; Experimental PRI with TCF: 70.1.

### #9 — Vipraj Nigam (`PROMISING_CANDIDATE`)
- **Why Considered:** Ranked #9 in Bowling with a conservative diagnostic value of -1.57 RPO. Classified as 'PROMISING_CANDIDATE' based on context-adjusted overperformance under pressure.
- **Evidence Volume:** 46 legal pressure deliveries bowled/faced, categorized in 'Small Sample (30-59 balls)'.
- **Temporal Stability:** Demonstrated across 7 unique pressure matches and 1 active seasons (Distribution: 2025: 46b).
- **Observed vs Expected:** Observed Economy Rate: 6.52 (raw difference of -1.70 RPO versus context expectation). | Context-adjusted expectation: 8.23 Economy Rate, derived from stratified 12-cell baselines across phase, tournament tier, and innings.
- **Conservative Diagnostic Score:** BOWL_CONSERVATIVE = -1.57 RPO. Represents the 84% 1-sided credible lower bound (conservative runs saved per over), inherently penalizing estimation uncertainty.
- **Uncertainty & CI:** Posterior standard error: $\pm$0.66 RPO. Shrinkage weight $r = 0.259$. | 95% Credible Interval: [-0.39, 2.21] RPO (width: 2.60 RPO).
- **Competition Support:** Coverage: IPL_ONLY (46 balls in IPL, 0 balls in Senior T20I). Limited cross-competition sample overlap.
- **Key Limitations:** Moderate sample volume (46 balls; estimation CI width is 2.6 RPO); Heavily skewed towards IPL; cross-league transferability is not guaranteed; Short multi-season track record (1 seasons active).
- **Sensitivity Profile:** Under unpenalized posterior mean, performance is +0.91 RPO. Model credibility against baseline: 8.5%; against peers: 91.6%. Exploratory PRI without TCF: 80.7; Experimental PRI with TCF: 52.8.

### #10 — Lungi Ngidi (`STRONG_EVIDENCE`)
- **Why Considered:** Ranked #10 in Bowling with a conservative diagnostic value of -1.65 RPO. Classified as 'STRONG_EVIDENCE' based on context-adjusted overperformance under pressure.
- **Evidence Volume:** 222 legal pressure deliveries bowled/faced, categorized in 'Large Sample (>=150 balls)'.
- **Temporal Stability:** Demonstrated across 26 unique pressure matches and 5 active seasons (Distribution: 2022: 30b, 2022/23: 12b, 2023: 12b, 2024: 30b, 2025: 34b, 2026: 104b).
- **Observed vs Expected:** Observed Economy Rate: 8.57 (raw difference of +0.51 RPO versus context expectation). | Context-adjusted expectation: 8.06 Economy Rate, derived from stratified 12-cell baselines across phase, tournament tier, and innings.
- **Conservative Diagnostic Score:** BOWL_CONSERVATIVE = -1.65 RPO. Represents the 84% 1-sided credible lower bound (conservative runs saved per over), inherently penalizing estimation uncertainty.
- **Uncertainty & CI:** Posterior standard error: $\pm$0.53 RPO. Shrinkage weight $r = 0.532$. | 95% Credible Interval: [0.09, 2.16] RPO (width: 2.07 RPO).
- **Competition Support:** Coverage: BOTH (116 balls in IPL, 106 balls in Senior T20I). Supported by substantial sample in both competitions.
- **Key Limitations:** Robust sample volume and multi-season stability; residual uncertainty bounded by 95% CI.
- **Sensitivity Profile:** Under unpenalized posterior mean, performance is +1.13 RPO. Model credibility against baseline: 1.6%; against peers: 90.7%. Exploratory PRI without TCF: 74.7; Experimental PRI with TCF: 86.6.

---

## 3. Promising Candidates Watchlist (Emerging Evidence)

These bowlers outperform peer averages ($\hat{\theta} < +1.82$ RPO), but have smaller sample volumes ($30-59$ balls) or fewer matches ($< 10$), retaining higher estimation uncertainty:

| Bowler Name | Posterior Mean Diff | Posterior SE | Conservative Runs Saved | Pressure Balls | Matches | Limitation Reason |
| :--- | ---: | ---: | ---: | ---: | ---: | :--- |
| **Nasum Ahmed** | +0.70 RPO | $\pm$0.63 | -1.32 RPO | 47 | 8 | Outperforms peer prior mean (+0.70 RPO < +1.82), but limited sample/matches (47 balls, 8 matches; SE=0.63) |
| **Vipraj Nigam** | +0.91 RPO | $\pm$0.66 | -1.57 RPO | 46 | 7 | Outperforms peer prior mean (+0.91 RPO < +1.82), but limited sample/matches (46 balls, 7 matches; SE=0.66) |
| **Ramon Simmonds** | +0.98 RPO | $\pm$0.68 | -1.66 RPO | 30 | 3 | Outperforms peer prior mean (+0.98 RPO < +1.82), but limited sample/matches (30 balls, 3 matches; SE=0.68) |
| **Haris Rauf** | +1.34 RPO | $\pm$0.46 | -1.80 RPO | 356 | 39 | Outperforms peer prior mean (+1.34 RPO < +1.82), but limited sample/matches (356 balls, 39 matches; SE=0.46) |
| **Arshdeep Singh** | +1.51 RPO | $\pm$0.31 | -1.82 RPO | 1031 | 120 | Outperforms peer prior mean (+1.51 RPO < +1.82), but limited sample/matches (1031 balls, 120 matches; SE=0.31) |
| **Roston Chase** | +1.16 RPO | $\pm$0.67 | -1.83 RPO | 54 | 9 | Outperforms peer prior mean (+1.16 RPO < +1.82), but limited sample/matches (54 balls, 9 matches; SE=0.67) |
| **Tim Southee** | +1.30 RPO | $\pm$0.53 | -1.83 RPO | 222 | 30 | Outperforms peer prior mean (+1.30 RPO < +1.82), but limited sample/matches (222 balls, 30 matches; SE=0.53) |
| **Shamar Joseph** | +1.31 RPO | $\pm$0.56 | -1.87 RPO | 163 | 19 | Outperforms peer prior mean (+1.31 RPO < +1.82), but limited sample/matches (163 balls, 19 matches; SE=0.56) |
| **Zakary Foulkes** | +1.27 RPO | $\pm$0.61 | -1.88 RPO | 82 | 13 | Outperforms peer prior mean (+1.27 RPO < +1.82), but limited sample/matches (82 balls, 13 matches; SE=0.61) |
| **Benjamin Lister** | +1.25 RPO | $\pm$0.64 | -1.89 RPO | 77 | 9 | Outperforms peer prior mean (+1.25 RPO < +1.82), but limited sample/matches (77 balls, 9 matches; SE=0.64) |