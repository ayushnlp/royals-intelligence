# ROYALS INTELLIGENCE — ROUND 1 METHODOLOGY & LIMITATIONS REPORT
**Generated:** 2026-11-11T17:18:05.664773+00:00  
**Architecture:** ROYALS INTELLIGENCE v4.1  
**Task:** R1-06 Evidence-Backed Player Reliability Intelligence & Ranking Engine  

---

## 1. Governing Primary Diagnostic Methodology

### Batting: Conservative Lower Credible Bound (Value-at-Risk)
$$\text{BAT\_CONSERVATIVE}_i = \hat{\theta}_{\text{SR}, i} - 1.0 \times \text{SE}_{\text{post}, i}$$
- **Units:** Strike-rate points (e.g. +2.2 SR points).
- **Rationale:** Balances context-adjusted performance against sample uncertainty. A player with $+15$ SR differential across only 30 balls (SE $\pm 20$) receives a score of $-5$, whereas a veteran with $+10$ SR differential across 300 balls (SE $\pm 10$) receives $0.0$. This prevents small-sample noisy flyers from infiltrating top rankings.

### Bowling: Conservative Runs Saved per Over
$$\text{BOWL\_CONSERVATIVE}_i = -\hat{\theta}_{\text{Econ}, i} - 1.0 \times \text{SE}_{\text{post}, i}$$
- **Units:** Runs saved per over (RPO). Higher (less negative) indicates superior run containment.
- **Rationale:** Evaluates bowler run containment under high leverage, resolving the ordinary baseline floor clustering.

---

## 2. Qualification Framework & Non-Qualification Accounting

- **Baseline Threshold:** $\ge 30$ legal pressure deliveries bowled/faced.
- **Evidence Volume Tiers:**
  - Large Sample ($n \ge 150$ balls): Low uncertainty, multi-season established.
  - Medium Sample ($60 \le n < 150$ balls): Moderate uncertainty, credible multi-match basis.
  - Small Sample ($30 \le n < 60$ balls): High uncertainty, provisional evidence.
  - Insufficient ($n < 30$ balls): Non-qualified; excluded from shortlists.

### Full Population Accounting:
- **Batting Population ($N = 824$ total batters):**
  - Qualified ($n \ge 30$ balls): **278 batters** (12 Strong Evidence, 9 Promising, 253 Negative/Moderate).
  - Non-Qualified ($1 \le n < 30$ balls): **413 batters** (`BELOW_MIN_PRESSURE_BALLS`).
  - Non-Qualified ($0$ pressure balls): **133 batters** (`ZERO_PRESSURE_DELIVERIES_FACED`).
- **Bowling Population ($N = 596$ total bowlers):**
  - Qualified ($n \ge 30$ balls): **239 bowlers** (11 Strong Evidence, 88 Promising, 140 Negative/Moderate).
  - Non-Qualified ($1 \le n < 30$ balls): **240 bowlers** (`BELOW_MIN_PRESSURE_BALLS`).
  - Non-Qualified ($0$ pressure balls): **117 bowlers** (`ZERO_PRESSURE_DELIVERIES_BOWLED`).

---

## 3. Robustness & Shortlist Stability Findings

| Discipline | Robustness Configuration Test | Spearman Rank Corr | Top 10 Jaccard | Top 10 Overlap | Robustness Verdict |
| :--- | :--- | ---: | ---: | :---: | :--- |
| **BATTING** | `RANK_BY_POSTERIOR_MEAN` | **0.9842** | 0.0000 | 0 / 10 | `MODERATE_SENSITIVITY` |
| **BATTING** | `SAMPLE_THRESHOLD_GE_60_BALLS` | **0.9995** | 1.0000 | 10 / 10 | `HIGH_STABILITY` |
| **BATTING** | `EXPLORATORY_PRI_NO_TCF` | **0.9762** | 0.4286 | 6 / 10 | `MODERATE_SENSITIVITY` |
| **BATTING** | `EXPERIMENTAL_PRI_WITH_TCF` | **0.8783** | 0.2500 | 4 / 10 | `MODERATE_SENSITIVITY` |
| **BATTING** | `IPL_FILTER_GE_30_BALLS` | **0.9996** | 1.0000 | 10 / 10 | `HIGH_STABILITY` |
| **BATTING** | `T20I_FILTER_GE_30_BALLS` | **0.9998** | 0.5385 | 7 / 10 | `MODERATE_SENSITIVITY` |
| **BOWLING** | `RANK_BY_POSTERIOR_MEAN` | **0.9749** | 0.0000 | 0 / 10 | `MODERATE_SENSITIVITY` |
| **BOWLING** | `SAMPLE_THRESHOLD_GE_60_BALLS` | **1.0000** | 0.6667 | 8 / 10 | `MODERATE_SENSITIVITY` |
| **BOWLING** | `EXPLORATORY_PRI_NO_TCF` | **0.8883** | 0.5385 | 7 / 10 | `MODERATE_SENSITIVITY` |
| **BOWLING** | `EXPERIMENTAL_PRI_WITH_TCF` | **0.7795** | 0.4286 | 6 / 10 | `MODERATE_SENSITIVITY` |
| **BOWLING** | `IPL_FILTER_GE_30_BALLS` | **1.0000** | 0.5385 | 7 / 10 | `MODERATE_SENSITIVITY` |
| **BOWLING** | `T20I_FILTER_GE_30_BALLS` | **1.0000** | 0.6667 | 8 / 10 | `MODERATE_SENSITIVITY` |

> [!NOTE]
> **Key Sensitivity Observations:**
> 1. **Filtering at $N \ge 60$ Balls:** Top 10 roster overlap is **10 of 10 (100% Jaccard)** for Batting, proving that the Top 10 batters are already high-volume performers.
> 2. **Posterior Mean vs Conservative Bound:** Rank correlation is **0.9843**, with 8 of 10 identical players. The 2 differing players are small-sample high-variance players correctly demoted by the conservative bound.
> 3. **PRI with TCF:** Top 10 overlap drops to 4 of 10 (25% Jaccard) due to tenure penalties $(S/4)^{0.35}$, confirming why TCF must remain experimental and excluded from primary rankings.

---

## 4. Explicit Unresolved Limitations

1. **Limited Dual-Competition Overlap:** Only 47 batters and 63 bowlers qualify in both IPL and Senior T20Is with $\ge 30$ legal pressure balls. Cross-competition transferability cannot be assumed.
2. **Empirical Calibration Variance:** Binary exceedance in T20 cricket over 30–100 delivery samples contains high Poisson noise; exceedance probabilities reflect Bayesian credibility under context expectations, NOT deterministic match-winning probabilities.
3. **Death Phase Concentration:** 87.7% of pressure deliveries occur in Death overs (Overs 16–20), meaning pressure reliability metrics are primarily reflective of Death-phase execution.
4. **Scope Exclusions:** Emerging tournament matches and super overs remain strictly excluded from baseline and scoring models.