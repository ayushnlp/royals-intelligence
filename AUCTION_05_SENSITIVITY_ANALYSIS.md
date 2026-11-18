# ROYALS INTELLIGENCE — AUCTION-05 SENSITIVITY ANALYSIS
## Model Robustness, Weight Perturbations and Invariance Testing

**Document Version:** 1.0.0  
**Phase:** RR Auction & Retention Intelligence Expansion  
**Stage:** `AUCTION-05` — Retention Ranking Engine  
**Execution Timestamp:** 2026-11-17T01:43:00+05:30  
**Status:** VALIDATED & STABLE

---

## 1. Overview and Purpose

Because retention model weights are provisional pending out-of-sample statistical calibration across multi-year IPL auctions, it is mandatory to test the stability and responsiveness of the ranking engine under severe parameter perturbations.

The goal of this analysis is to determine whether the recommended retention core (**Yashasvi Jaiswal, Riyan Parag, Dhruv Jurel**) remains invariant under competing strategic philosophies, and to identify the exact thresholds where the recommendation boundaries shift.

---

## 2. Weight Perturbation Scenarios

Five distinct strategic scenarios were executed against the verified eligible candidate pool ($N=11$):

$$\begin{array}{|l|r|r|r|r|r|}
\hline
\textbf{Retention Dimension} & \textbf{Baseline} & \textbf{Perf Heavy} & \textbf{Scarcity Heavy} & \textbf{Age Heavy} & \textbf{Equal Weights} \\
\hline
\text{Player Performance } (w_{\text{perf}}) & 0.25 & \mathbf{0.40} & 0.15 & 0.20 & 0.1429 \\
\text{Role Scarcity } (w_{\text{scarcity}}) & 0.20 & 0.15 & \mathbf{0.30} & 0.15 & 0.1429 \\
\text{Replacement Difficulty } (w_{\text{replace}}) & 0.20 & 0.15 & \mathbf{0.30} & 0.15 & 0.1429 \\
\text{Squad Balance } (w_{\text{balance}}) & 0.15 & 0.10 & 0.10 & 0.10 & 0.1429 \\
\text{Age \& Career Stage } (w_{\text{age}}) & 0.05 & 0.05 & 0.05 & \mathbf{0.25} & 0.1429 \\
\text{Reliability } (w_{\text{reliability}}) & 0.05 & 0.05 & 0.05 & 0.05 & 0.1429 \\
\text{Sample Confidence } (w_{\text{confidence}}) & 0.10 & 0.10 & 0.05 & 0.10 & 0.1429 \\
\hline
\textbf{Total Weight Sum} & \mathbf{1.00} & \mathbf{1.00} & \mathbf{1.00} & \mathbf{1.00} & \mathbf{1.00} \\
\hline
\end{array}$$

---

## 3. Empirical Results Across Scenarios

$$\begin{array}{|l|l|c|l|}
\hline
\textbf{Scenario Name} & \textbf{Top 3 Recommended Retentions} & \textbf{Invariant?} & \textbf{Key Rank Shifts \& Strategic Implications} \\
\hline
\textbf{Baseline (Audited Balanced)} & \text{Jaiswal, Parag, Jurel} & \mathbf{\text{TRUE}} & \text{Core domestic spine established.} \\
\textbf{Performance Heavy (40\%)} & \text{Jaiswal, Parag, Sooryavanshi} & \mathbf{\text{FALSE}} & \text{Sooryavanshi rises to \#3 (+1) due to raw 226.49 U19 SR.} \\
\textbf{Scarcity \& Auction Heavy} & \text{Jaiswal, Parag, Jurel} & \mathbf{\text{TRUE}} & \text{Jaiswal (98.0) and Parag (94.0) widen lead over field.} \\
\textbf{Age \& Horizon Heavy (25\%)} & \text{Jaiswal, Parag, Jurel} & \mathbf{\text{TRUE}} & \text{Jaiswal (age 24) and Parag/Jurel (age 25) dominate veterans.} \\
\textbf{Equal Weights (14.28\% Each)} & \text{Jaiswal, Parag, Jurel} & \mathbf{\text{TRUE}} & \text{Top 3 identical; robust against arbitrary weight tuning.} \\
\hline
\end{array}$$

---

## 4. Key Sensitivity Findings

1. **Top-3 Invariance Rate:** The recommended core of **Yashasvi Jaiswal, Riyan Parag, and Dhruv Jurel** is invariant across **4 out of 5 scenarios (80.0%)**.
2. **The Performance-Heavy Boundary:**
   - Under the extreme *Performance Heavy* scenario ($w_{\text{perf}} = 0.40$), 15-year-old **Vaibhav Sooryavanshi** overtakes Dhruv Jurel for the #3 spot by a margin of $+0.84$ points.
   - *Forensic Root Cause:* Sooryavanshi accumulated a shrunk strike rate of $226.49$ with a $38.1\%$ boundary rate across 674 balls in emerging/U19 competitions. When raw performance is weighted at $40\%$ without sufficient dampening for competition tier discount or developmental age incubation, his score spikes to $98.0/100$.
   - *Strategic Resolution:* In professional IPL governance, committing a primary retention slot to a 15-year-old with zero senior IPL matches exposes the franchise to extreme tactical risk. The baseline balanced weighting ($w_{\text{perf}} = 0.25$, $w_{\text{scarcity}} = 0.20$, $w_{\text{replace}} = 0.20$) correctly gates this risk and confirms Dhruv Jurel as the legitimate senior retention.
3. **Overseas Penalty Sensitivity:**
   - Even when performance is prioritized, overseas candidates (Shimron Hetmyer and Jofra Archer) fail to breach the Top 3 due to the structural penalty of consuming scarce overseas roster slots ($S_{\text{balance}} = 75.0$) and high auction substitutability ($S_{\text{scarcity}} \le 80.0$).
