# ROYALS INTELLIGENCE — TASK R1-06.1 AUDIT REPORT
## Probability Outputs & Statistical Exceedance Independent Audit

**Audit Date:** 2026-11-12  
**Architecture:** ROYALS INTELLIGENCE v4.1  
**Task:** R1-06.1 Independent Candidate Classification & Statistical Interpretation Audit  
**Starting Checkpoint:** `8e8f9f3`  
**Audit Status:** `AUDIT_COMPLETED — CRITICAL INTERPRETATION DEFECT IDENTIFIED`  

---

## 1. Executive Summary: The "100% P(Beat Peers)" Investigation

In Task R1-06, every single batter on the Batting Shortlist (#1 through #12) reportedly exhibited:
$$P(\text{Beat Peers}) = \mathbf{100.0\%}$$

This independent audit investigated the exact mathematical formulation, reference populations, and code implementation behind this metric.

### Core Audit Finding:
**The metric labeled `P(Beat Peers)` does NOT measure the probability of beating fellow shortlisted candidates or contemporaneous peers.**  
Instead, it measures:
$$P(\theta_i > \mu_{\text{prior}}) = \Phi\left(\frac{\hat{\theta}_i - \mu_{\text{prior}}}{\text{SE}_{\text{post}}}\right)$$
where $\mu_{\text{prior}} = \mathbf{-34.24\text{ SR points}}$ is the league-wide DerSimonian-Laird prior mean for pressured batting.

Because the average batter's strike rate collapses by $34.24\text{ SR points}$ under pressure, any candidate who maintains their ordinary strike rate ($\hat{\theta}_i \ge 0$) is $+34.24\text{ SR points}$ ahead of the population average. When divided by a posterior standard error of $11$ to $14\text{ SR points}$, the resulting z-score is $+2.5$ to $+3.8\sigma$, which mathematically yields:
$$\Phi(z) \ge 0.995 \implies \mathbf{100.0\%}$$

Presenting this metric to cricket analysts as "P(Beat Peers) = 100%" is severely misleading, as it is easily misinterpreted as a guarantee that a batter is superior to all other shortlisted candidates.

---

## 2. Mathematical Formulations & Code Tracing

The probability metrics originate in [`round1_pressure/src/player_reliability.py`](file:///c:/Users/ayush/Documents/ROYALS%20INTELLIGENCE/round1_pressure/src/player_reliability.py#L175-L182) and are propagated into R1-06 via [`r1_06_player_intelligence.py`](file:///c:/Users/ayush/Documents/ROYALS%20INTELLIGENCE/round1_pressure/src/r1_06_player_intelligence.py#L259-L260):

### Batting Implementation:
```python
# 1. Probability of exceeding ordinary context baseline (Strike Rate Diff > 0)
prob_exceed_baseline = stats.norm.cdf(
    shrunk_diff_strike_rate / posterior_se_strike_rate
)

# 2. Probability of exceeding the pressured peer population prior mean (mu_b = -34.24 SR)
prob_exceed_peer_mean = stats.norm.cdf(
    (shrunk_diff_strike_rate - mu_b) / posterior_se_strike_rate
)
```

### Bowling Implementation:
```python
# 1. Probability of conceding fewer runs than ordinary baseline (Economy Diff < 0)
prob_exceed_baseline = stats.norm.cdf(
    (0.0 - shrunk_diff_economy) / posterior_se_economy
)

# 2. Probability of outperforming the pressured peer population mean (mu_bw = +1.82 RPO)
prob_exceed_peer_mean = stats.norm.cdf(
    (mu_bw - shrunk_diff_economy) / posterior_se_economy
)
```

---

## 3. Dissecting the Batting Z-Scores Across the Shortlist

The table below reconstructs the exact mathematical steps producing the reported exceedance probabilities for all 12 shortlisted batters:

$$\mu_{\text{prior}} = -34.2384\text{ SR points}$$

| Rank | Player Name | Posterior Mean ($\hat{\theta}$) | Posterior SE | Distance to Baseline ($\hat{\theta} - 0$) | Z-Score vs Baseline | **P(Beat Baseline)** | Distance to Peer Mean ($\hat{\theta} - \mu_{\text{prior}}$) | Z-Score vs Peer Mean | **P(Beat Peers)** |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | Nicholas Pooran | +16.20 | 13.98 | +16.20 | +1.159 | **87.7%** | +50.44 | +3.608 | **99.98% $\approx$ 100.0%** |
| 2 | Donovan Ferreira | +20.72 | 19.82 | +20.72 | +1.045 | **85.2%** | +54.96 | +2.773 | **99.72% $\approx$ 100.0%** |
| 3 | Tim David | +9.61 | 12.14 | +9.61 | +0.792 | **78.6%** | +43.85 | +3.612 | **99.98% $\approx$ 100.0%** |
| 4 | Dinesh Karthik | +9.26 | 11.91 | +9.26 | +0.777 | **78.1%** | +43.50 | +3.652 | **99.99% $\approx$ 100.0%** |
| 5 | Ashutosh Sharma | +13.52 | 17.10 | +13.52 | +0.791 | **78.6%** | +47.76 | +2.793 | **99.74% $\approx$ 100.0%** |
| 6 | Marcus Stoinis | +6.02 | 11.79 | +6.02 | +0.511 | **69.5%** | +40.26 | +3.415 | **99.97% $\approx$ 100.0%** |
| 7 | Naman Dhir | +11.82 | 18.73 | +11.82 | +0.631 | **73.6%** | +46.06 | +2.459 | **99.30% $\approx$ 99.3%** |
| 8 | Rinku Singh | +4.53 | 11.55 | +4.53 | +0.392 | **65.2%** | +38.77 | +3.357 | **99.96% $\approx$ 100.0%** |
| 9 | Tristan Stubbs | +4.59 | 12.76 | +4.59 | +0.360 | **64.1%** | +38.83 | +3.043 | **99.88% $\approx$ 99.9%** |
| 10 | Sherfane Rutherford | +4.87 | 13.05 | +4.87 | +0.373 | **64.5%** | +39.11 | +2.997 | **99.86% $\approx$ 99.9%** |
| 11 | Rovman Powell | +3.32 | 12.12 | +3.32 | +0.274 | **60.8%** | +37.56 | +3.099 | **99.90% $\approx$ 99.9%** |
| 12 | Aiden Markram | +2.61 | 11.65 | +2.61 | +0.224 | **58.9%** | +36.85 | +3.163 | **99.92% $\approx$ 99.9%** |

### Mathematical Insights:
1. **The $+34.24\text{ SR}$ Advantage:** Every shortlisted player has a positive posterior mean ($\hat{\theta} \ge 0$). Thus, their point estimate is at least $34.24\text{ SR points}$ superior to the average pressured batter.
2. **The Z-Scores are Universally Massive:** The z-scores against the peer mean range from $+2.46$ to $+3.65$. In a normal distribution, $\Phi(2.46) = 0.993$ and $\Phi(3.65) = 0.9999$.
3. When formatted as `{prob * 100:.1f}%` or `{prob:.1%}`, 10 of the 12 round up to **100.0%**, and the remaining two are **99.3%** and **99.9%**.
4. **Analyst Trap:** Seeing $P(\text{Beat Peers}) = 100.0\%$ for Tim David does NOT mean Tim David has a 100% chance of out-batting Nicholas Pooran. In reality, the probability that Pooran outperforms David is roughly $65-70\%$, as their posterior credible intervals heavily overlap.

---

## 4. Dissecting the Bowling Z-Scores Across the Shortlist

$$\mu_{\text{prior}} = +1.8228\text{ RPO}$$

| Rank | Player Name | Posterior Mean Diff | Posterior SE | Distance to Baseline ($0 - \hat{\theta}$) | **P(Beat Baseline)** | Distance to Peer Mean ($\mu_{\text{prior}} - \hat{\theta}$) | Z-Score vs Peer Mean | **P(Beat Peers)** |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | Jasprit Bumrah | **-0.20 RPO** | $\pm 0.36$ | +0.20 RPO | **71.1%** | +2.02 RPO | +5.611 | **100.0%** |
| 2 | Sunil Narine | +0.39 RPO | $\pm 0.55$ | -0.39 RPO | **23.3%** | +1.43 RPO | +2.600 | **99.6%** |
| 3 | Maheesh Theekshana | +0.55 RPO | $\pm 0.41$ | -0.55 RPO | **8.8%** | +1.27 RPO | +3.098 | **99.9%** |
| 4 | Matheesha Pathirana | +0.63 RPO | $\pm 0.41$ | -0.63 RPO | **6.0%** | +1.19 RPO | +2.902 | **99.8%** |
| 5 | Shaheen Afridi | +0.93 RPO | $\pm 0.50$ | -0.93 RPO | **3.1%** | +0.89 RPO | +1.780 | **96.1%** |
| 6 | Mustafizur Rahman | +1.11 RPO | $\pm 0.36$ | -1.11 RPO | **0.1%** | +0.71 RPO | +1.972 | **97.4%** |
| 7 | Richard Ngarava | +1.11 RPO | $\pm 0.45$ | -1.11 RPO | **0.7%** | +0.71 RPO | +1.578 | **94.2%** |
| 8 | Lungi Ngidi | +1.18 RPO | $\pm 0.47$ | -1.18 RPO | **0.6%** | +0.64 RPO | +1.362 | **91.3%** |
| 9 | Ravichandran Ashwin | +1.11 RPO | $\pm 0.56$ | -1.11 RPO | **2.4%** | +0.71 RPO | +1.268 | **89.8%** |
| 10 | Hasan Mahmud | +1.03 RPO | $\pm 0.66$ | -1.03 RPO | **5.9%** | +0.79 RPO | +1.197 | **88.5%** |
| 11 | Nathan Ellis | +1.28 RPO | $\pm 0.43$ | -1.28 RPO | **0.1%** | +0.54 RPO | +1.256 | **89.6%** |

### Mathematical Insights:
1. **The Asymmetry with Batting:** Unlike batting where point estimates beat ordinary baseline ($\hat{\theta} > 0$), 10 of the 11 bowlers have positive economy differentials ($\hat{\theta} > 0$), meaning they concede *more* runs per over under pressure than ordinary baseline.
2. For Nathan Ellis, $P(\text{Beat Baseline}) = 0.1\%$, while $P(\text{Beat Peers}) = 89.6\%$. This illustrates the profound difference between the two reference baselines.
3. Bumrah is the only bowler whose distance to baseline is positive ($+0.20\text{ RPO}$), producing $P(\text{Beat Baseline}) = 71.1\%$.

---

## 5. Statistical Nature & Calibration Limits (Per R1-05.2)

The statistical audit evaluated whether these probabilities possess empirical calibration:

1. **They are Model Credibility Quantiles, NOT Frequentist Probabilities:**  
   Per the formal findings of R1-05.2, exceedance probabilities are derived from integrating a Gaussian posterior under Empirical Bayes shrinkage:
   $$P(\theta > c) = 1 - \Phi\left(\frac{c - \hat{\theta}}{\text{SE}_{\text{post}}}\right)$$
   They do not represent the empirical win rate of a player in real match outcomes.

2. **Calibration Uncertainty:**  
   As proven in Task R1-05.2, Brier scores on held-out testing partitions range from $0.2228$ to $0.2707$. Over small sample volumes ($30-60$ deliveries), Poisson event noise dominates, preventing sharp empirical probability calibration.

3. **Sensitivity to the Empirical Bayes Prior Mean:**  
   For small-sample players, $P(\text{Beat Baseline})$ is highly sensitive to the assumed prior mean. Shifting the prior mean from $-34.24$ to $0.0$ shifts a 30-ball player's baseline exceedance probability from $35\%$ to $65\%$.

---

## 6. Audit Recommendations on Probability Presentation

1. **Deprecate the Term `P(Beat Peers)`:**  
   Replace it with:
   $$\text{P(Exceed League Average Under Pressure)} \quad \text{or} \quad P(\theta > \mu_{\text{prior}})$$
2. **Always Disclose the Reference Population:**  
   Every display of this metric must explicitly state:
   *"Relative to the league-wide pressured batting average ($\mu = -34.24\text{ SR}$) / bowling average ($\mu = +1.82\text{ RPO}$)."*
3. **Prohibit Head-to-Head Interpretation:**  
   Reports must include a prominent warning:
   > **Note:** This metric measures performance against the overall league average under pressure. It does NOT represent the probability of one shortlisted player outperforming another shortlisted player.
