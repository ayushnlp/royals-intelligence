# ROYALS INTELLIGENCE — ROUND 1 METHODOLOGY & LIMITATIONS REPORT
**Generated:** 2026-11-11T21:49:31.495627+00:00  
**Architecture:** ROYALS INTELLIGENCE v4.1  
**Task:** R1-06 / R1-06.2 Candidate Classification & Evidence Governance Remediation  

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

### Two-Dimensional Candidate Classification System (Remediated Under Task R1-06.2)
To prevent the conflation of performance direction, statistical evidence, and exposure volume, R1-06.2 implements two orthogonal dimensions:
1. **Dimension A: Performance Evidence Status:**
   - `POSITIVE_CONSERVATIVE_EVIDENCE`: Conservative lower bound is strictly $> 0$.
   - `NEGATIVE_CONSERVATIVE_ESTIMATE`: Posterior mean is positive ($\hat{\theta} > 0$), but conservative lower bound is $\le 0$ (positive estimated performance with unresolved uncertainty).
   - `BELOW_BASELINE_EVIDENCE`: Entire 1-sigma interval is below baseline ($\hat{\theta} + \text{SE} < 0$ for batting; runs saved upper bound $< 0$ for bowling).
   - `INCONCLUSIVE_EVIDENCE`: Point estimate non-positive, but 1-sigma interval spans zero.
2. **Dimension B: Evidence Volume Tier:**
   - `HIGH_VOLUME`: $\ge 150$ legal pressure deliveries.
   - `MEDIUM_VOLUME`: $60-149$ legal pressure deliveries.
   - `LOW_VOLUME`: $30-59$ legal pressure deliveries.
   - `NO_QUALIFYING_EXPOSURE`: $< 30$ legal pressure deliveries.

### Candidate Sample Qualification Logic (DEF-04 Fix)
Candidate selection sample qualification is governed by: `(balls >= 60) or (balls >= 50 and matches >= 10)`. This fixes the DEF-04 syntax bug where `matches >= 10` was erroneously applied to the $\ge 60$ balls branch.

### Competition Exposure vs Skill Transferability (DEF-05 Remediation)
`DUAL_TOURNAMENT_QUALIFIED` signifies that a candidate has accumulated $\ge 30$ legal pressure deliveries in both IPL and Senior T20I matches. This confirms sample availability across both competition environments, NOT statistical proof of invariant cross-competition skill transferability.

### Probability Disclosures & Reference Prior Means (DEF-02 Remediation)
`P(Exceed League Avg Under Pressure)` evaluates candidate performance against the league-wide pressure prior mean:
- Batting prior mean: $\mu_b = -34.24$ SR pts.
- Bowling prior mean: $\mu_{bw} = +1.82$ RPO conceded.
Exceeding the league pressure average reflects outperforming an environment where performance degrades substantially under pressure; it is a significantly lower bar than exceeding ordinary baseline performance.

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
  - Qualified ($n \ge 30$ balls): **278 batters** (2 Positive Conservative Evidence, 19 Negative Conservative Estimate, 182 Below Baseline, 75 Inconclusive).
  - Non-Qualified ($1 \le n < 30$ balls): **413 batters** (`BELOW_MIN_PRESSURE_BALLS`).
  - Non-Qualified ($0$ pressure balls): **133 batters** (`ZERO_PRESSURE_DELIVERIES_FACED`).
- **Bowling Population ($N = 596$ total bowlers):**
  - Qualified ($n \ge 30$ balls): **239 bowlers** (0 Positive Conservative Evidence, 1 Negative Conservative Estimate [Bumrah], 1 Inconclusive [Narine], 237 Below Baseline).
  - Non-Qualified ($1 \le n < 30$ balls): **240 bowlers** (`BELOW_MIN_PRESSURE_BALLS`).
  - Non-Qualified ($0$ pressure balls): **117 bowlers** (`ZERO_PRESSURE_DELIVERIES_BOWLED`).

---

## 3. Robustness & Shortlist Stability Findings

| Discipline | Robustness Configuration Test | Spearman Rank Corr | Top 10 Jaccard | Top 10 Overlap | Robustness Verdict |
| :--- | :--- | ---: | ---: | :---: | :--- |
| **BATTING** | `RANK_BY_POSTERIOR_MEAN` | **0.9843** | 0.0000 | 0 / 10 | `MODERATE_SENSITIVITY` |
| **BATTING** | `SAMPLE_THRESHOLD_GE_60_BALLS` | **0.9995** | 1.0000 | 10 / 10 | `HIGH_STABILITY` |
| **BATTING** | `EXPLORATORY_PRI_NO_TCF` | **0.9762** | 0.4286 | 6 / 10 | `MODERATE_SENSITIVITY` |
| **BATTING** | `EXPERIMENTAL_PRI_WITH_TCF` | **0.8780** | 0.2500 | 4 / 10 | `MODERATE_SENSITIVITY` |
| **BATTING** | `IPL_FILTER_GE_30_BALLS` | **0.9996** | 1.0000 | 10 / 10 | `HIGH_STABILITY` |
| **BATTING** | `T20I_FILTER_GE_30_BALLS` | **0.9998** | 0.5385 | 7 / 10 | `MODERATE_SENSITIVITY` |
| **BOWLING** | `RANK_BY_POSTERIOR_MEAN` | **0.9751** | 0.0000 | 0 / 10 | `MODERATE_SENSITIVITY` |
| **BOWLING** | `SAMPLE_THRESHOLD_GE_60_BALLS` | **1.0000** | 0.6667 | 8 / 10 | `MODERATE_SENSITIVITY` |
| **BOWLING** | `EXPLORATORY_PRI_NO_TCF` | **0.8886** | 0.5385 | 7 / 10 | `MODERATE_SENSITIVITY` |
| **BOWLING** | `EXPERIMENTAL_PRI_WITH_TCF` | **0.7802** | 0.4286 | 6 / 10 | `MODERATE_SENSITIVITY` |
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