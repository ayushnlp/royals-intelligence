# ROYALS INTELLIGENCE — R1-SUBMISSION-02: BOWLING METRIC DIRECTION & RANKING INTEGRITY AUDIT

**Audit Type:** Targeted Read-Only Mathematical, Statistical & Ranking Integrity Verification  
**Project:** ROYALS INTELLIGENCE v4.1  
**Milestone:** Pre-Submission Verification (SupeRR Selector Season 2 — Round 1)  
**Target Subject:** Top 10 Bowling Under Pressure Leaderboard & Diagnostic Mechanics  
**Repository Working Directory:** `c:\Users\ayush\Documents\ROYALS INTELLIGENCE`  
**Current Git Checkpoint:** `6005022` (`feat(r1-06.2.3)`)  
**Audit Report Path:** `round1_pressure/reports/R1_SUBMISSION_02_BOWLING_RANKING_INTEGRITY_AUDIT.md`  
**Audit Execution Mode:** Strict Read-Only (Zero Code, Parquet, Formula, or Checkpoint Modifications)

---

## 1. TRACE OF THE BOWLING PRI & DIAGNOSTIC FORMULAS

The mathematical and algorithmic mechanics governing the Bowling Pressure Reliability Index (PRI) and candidate ranking were audited directly from source code across `round1_pressure/src/expected_performance.py`, `player_reliability.py`, `r1_06_player_intelligence.py`, `r1_06_candidate_selection.py`, and `r1_06_explainability.py`.

### 1.1 Raw Economy Differential Sign Convention
In `expected_performance.py` (lines 100–108), the raw delivery-level performance differential is defined as:
$$\text{diff\_economy}_i = \text{Observed\_Economy}_i - \text{Expected\_Economy}_i$$
- **Observed Economy:** Total runs conceded per 6 legal balls in high-pressure situations:
  $$\text{Observed\_Economy}_i = \frac{\text{Runs Conceded}_i}{\text{Legal Pressure Balls}_i} \times 6.0$$
- **Expected Economy:** Context-weighted baseline economy derived from stratified 12-cell baselines across phase (Powerplay, Middle, Death), tournament tier (IPL vs. Senior T20I), and innings (1st vs. 2nd):
  $$\text{Expected\_Economy}_i = \frac{\sum_{c} \text{Balls}_{i, c} \cdot \bar{E}_c}{\text{Legal Pressure Balls}_i}$$
- **Sign Convention:**
  - $\text{diff\_economy}_i < 0$ (**Negative**): The bowler conceded **fewer runs per over** than expected by match context. This indicates superior containment (outperforming baseline).
  - $\text{diff\_economy}_i > 0$ (**Positive**): The bowler conceded **more runs per over** than expected by match context. This indicates leakage relative to baseline.

### 1.2 Empirical Bayes Hierarchical Shrinkage
In `expected_performance.py` and `player_reliability.py` (lines 250–266), small-sample noise is controlled using empirical Bayes shrinkage towards the league-wide bowling prior mean $\mu_{\text{bw}}$:
$$\hat{\theta}_{\text{Econ}, i} = (1 - r_i) \cdot \mu_{\text{bw}} + r_i \cdot \text{diff\_economy}_i$$
where:
- $\mu_{\text{bw}} = +1.822756$ RPO: Empirical league-wide prior mean across all qualified bowlers under pressure. In high pressure (overwhelmingly death overs), the average bowler concedes **+1.82 runs per over more** than ordinary baselines.
- $\tau_{\text{bw}} = 0.770593$ RPO: Between-bowler standard deviation (prior spread).
- $\sigma_i^2 = \text{se\_economy}_i^2$: Individual sampling variance, inversely proportional to legal balls bowled.
- $r_i = \frac{\tau_{\text{bw}}^2}{\tau_{\text{bw}}^2 + \sigma_i^2}$: Shrinkage reliability weight ($0 \le r_i \le 1$). High-exposure veterans have $r_i \to 1$ (minimal shrinkage); small-sample bowlers have $r_i \to 0$ (pulled towards $+1.82$ RPO).
- $\text{SE}_{\text{post}, i} = \sqrt{\frac{1}{\frac{1}{\tau_{\text{bw}}^2} + \frac{1}{\sigma_i^2}}}$: Posterior standard error.

### 1.3 Definition of Runs Saved per Over
Because bowling quality is an inverse metric (lower economy = better defense), `player_reliability.py` (lines 251–254) maps the posterior economy differential $\hat{\theta}_{\text{Econ}, i}$ to positive utility (**Runs Saved per Over** relative to ordinary expectation):
$$\text{Runs\_Saved}_i = -\hat{\theta}_{\text{Econ}, i}$$
- If $\hat{\theta}_{\text{Econ}} = -0.20$ RPO (Bumrah), Runs Saved $= -(-0.20) = +0.20$ RPO (saving runs).
- If $\hat{\theta}_{\text{Econ}} = +0.55$ RPO (Theekshana), Runs Saved $= -(+0.55) = -0.55$ RPO (conceding 0.55 runs/over relative to ordinary baseline, but saving $+1.27$ runs/over relative to the league prior $+1.82$).

### 1.4 The Governing Primary Ranking Metric: Conservative Runs Saved per Over
To balance estimated containment against estimation uncertainty, `r1_06_player_intelligence.py` and `r1_06_candidate_selection.py` establish **$\text{BOWL\_CONSERVATIVE}$** as the primary diagnostic:
$$\text{BOWL\_CONSERVATIVE}_i = -\hat{\theta}_{\text{Econ}, i} - 1.0 \times \text{SE}_{\text{post}, i}$$
- **Units:** Runs saved per over (RPO).
- **Statistical Interpretation:** Represents the **lower bound of the 1-sigma (84.1%) posterior credible interval** for runs saved. We are approximately 84.1% confident that the bowler's true run containment under pressure saves at least $\text{BOWL\_CONSERVATIVE}$ runs per over.
- **Direction:** **Higher (less negative / more positive) is algebraically and competitively superior.**
  - A bowler with $\text{BOWL\_CONSERVATIVE} = -0.16$ RPO is vastly superior to a bowler with $\text{BOWL\_CONSERVATIVE} = -0.96$ RPO, who in turn is superior to a bowler with $-1.71$ RPO.
- **Sorting Rule:** `bowl_qual.sort_values("primary_diagnostic_value", ascending=False)` (lines 244–247 of `r1_06_candidate_selection.py`). Sorting descending on this metric correctly places the highest-performing, lowest-risk run-containment bowlers at the top.

---

## 2. VERIFICATION OF ALL TEN BOWLING CANDIDATES

All data was extracted directly from the production Parquet artifact `round1_pressure/data/processed/bowling_leaderboard.parquet` and verified against `r1_06_bowling_shortlist.md`.

### 2.1 Complete Diagnostic Audit Table (Top 10 + Alternate)

| Official Rank | Player ID | Player Name | Pressure Balls | Matches | Obs Econ | Exp Econ | Raw Diff ($\text{diff}$) | Posterior Mean ($\hat{\theta}$) | Posterior SE ($\text{SE}$) | Calculated Bound ($-\hat{\theta} - \text{SE}$) | Stored Diag ($\text{BOWL\_CONS}$) | Absolute Discrepancy ($\Delta$) | 95% Credible Interval | P(Beat Baseline) | P(Exceed League Avg) | Evidence Status | Volume Tier |
| :---: | :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **1** | 2933 | **Jasprit Bumrah** | 521 | 60 | 7.37 | 8.13 | -0.76 | -0.20 | 0.36 | **-0.16** | **-0.16** | `0.000000` | [-0.90, +0.50] | 71.1% | 100.0% | `POSITIVE_ESTIMATE_UNRESOLVED` | `HIGH_VOLUME` |
| **2** | 781 | **Sunil Narine** | 153 | 24 | 7.14 | 8.21 | -1.08 | +0.39 | 0.55 | **-0.94** | **-0.94** | `0.000000` | [-0.68, +1.47] | 23.8% | 99.5% | `INCONCLUSIVE_EVIDENCE` | `HIGH_VOLUME` |
| **3** | 19316 | **Maheesh Theekshana**| 421 | 58 | 8.08 | 8.03 | +0.05 | +0.55 | 0.41 | **-0.96** | **-0.96** | `0.000000` | [-0.25, +1.35] | 9.0% | 99.9% | `BELOW_BASELINE_EVIDENCE` | `HIGH_VOLUME` |
| **4** | 8661 | **Matheesha Pathirana**| 440 | 44 | 8.29 | 8.14 | +0.16 | +0.63 | 0.41 | **-1.05** | **-1.05** | `0.000000` | [-0.18, +1.44] | 6.2% | 99.8% | `BELOW_BASELINE_EVIDENCE` | `HIGH_VOLUME` |
| **5** | 6355 | **Shaheen Afridi** | 191 | 31 | 8.04 | 7.87 | +0.18 | +0.91 | 0.52 | **-1.43** | **-1.43** | `0.000000` | [-0.10, +1.92] | 3.8% | 96.1% | `BELOW_BASELINE_EVIDENCE` | `HIGH_VOLUME` |
| **6** | 4373 | **Mustafizur Rahman** | 578 | 61 | 8.93 | 8.07 | +0.86 | +1.09 | 0.38 | **-1.47** | **-1.47** | `0.000000` | [+0.35, +1.84] | 0.2% | 97.2% | `BELOW_BASELINE_EVIDENCE` | `HIGH_VOLUME` |
| **7** | 4874 | **Richard Ngarava** | 287 | 34 | 8.51 | 7.82 | +0.69 | +1.10 | 0.46 | **-1.56** | **-1.56** | `0.000000` | [+0.19, +2.01] | 0.9% | 94.1% | `BELOW_BASELINE_EVIDENCE` | `HIGH_VOLUME` |
| **8** | 4641 | **Lungi Ngidi** | 222 | 26 | 8.57 | 8.06 | +0.51 | +1.13 | 0.53 | **-1.65** | **-1.65** | `0.000000` | [+0.09, +2.16] | 1.6% | 90.7% | `BELOW_BASELINE_EVIDENCE` | `HIGH_VOLUME` |
| **9** | 305 | **Ravichandran Ashwin**| 147 | 21 | 8.45 | 8.18 | +0.27 | +1.11 | 0.57 | **-1.67** | **-1.67** | `0.000000` | [-0.00, +2.22] | 2.5% | 89.6% | `BELOW_BASELINE_EVIDENCE` | `MEDIUM_VOLUME` |
| **10** | 6643 | **Hasan Mahmud** | 90 | 11 | 7.67 | 7.81 | -0.14 | +1.08 | 0.61 | **-1.69** | **-1.69** | `0.000000` | [-0.11, +2.28] | 3.7% | 88.7% | `BELOW_BASELINE_EVIDENCE` | `MEDIUM_VOLUME` |
| *Alt #11*| 7920 | **Nathan Ellis** | 347 | 35 | 8.96 | 8.04 | +0.92 | +1.24 | 0.46 | **-1.71** | **-1.71** | `0.000000` | [+0.34, +2.15] | 0.4% | 89.5% | `BELOW_BASELINE_EVIDENCE` | `HIGH_VOLUME` |

### 2.2 Numerical Recalculation Audit Findings
1. **Mathematical Accuracy:** Independent recalculation of $\text{BOWL\_CONSERVATIVE} = -\hat{\theta}_{\text{Econ}} - \text{SE}_{\text{post}}$ matches the stored `primary_diagnostic_value` column to **six decimal places ($\Delta = 0.000000$)** for all candidates.
2. **Strict Algebraic Monotonicity:**
   $$-0.1597 \ge -0.9398 \ge -0.9583 \ge -1.0455 \ge -1.4289 \ge -1.4748 \ge -1.5604 \ge -1.6531 \ge -1.6749 \ge -1.6939 \ge -1.7063$$
   Every successive player down the leaderboard has an equal or more negative conservative score. The ranking order is 100% strictly decreasing.

---

## 3. VERIFICATION OF RANKING DIRECTION & SORTING LOGIC

### 3.1 Why Jasprit Bumrah Ranks #1 Above Sunil Narine and Theekshana
A critical audit question was whether Jasprit Bumrah (-0.16 RPO) belongs above bowlers with values like -0.94 RPO and -0.96 RPO.

**Findings & Mathematical Proof:**
1. **The Algebraic Direction:** In the real number system $\mathbb{R}$:
   $$-0.16 > -0.94 > -0.96 > -1.05 > -1.43 > \dots > -1.71$$
   $-0.16$ is algebraically **larger** than $-0.94$ (it is closer to zero and further to the right on the number line).
2. **The Cricket Context (Runs Saved):**
   - Bumrah's conservative lower bound is $-0.16$ RPO. This means that at the 84.1% credibility bound, Bumrah's run rate increases by at most $0.16$ runs per over under pressure.
   - Sunil Narine's conservative lower bound is $-0.94$ RPO. At the 84.1% credibility bound, Narine's run rate may increase by up to $0.94$ runs per over.
   - Maheesh Theekshana's conservative lower bound is $-0.96$ RPO (increasing by up to $0.96$ runs per over).
   - Nathan Ellis's conservative lower bound is $-1.71$ RPO (increasing by up to $1.71$ runs per over).
3. **Conclusion:** Bumrah's containment under pressure degrades substantially less than any other bowler in the dataset. He concedes fewer runs per over under high leverage. Ranking Bumrah at #1 is mathematically, statistically, and competitively **correct**.

### 3.2 Verification of Sample Qualification Filtering
In `bowling_leaderboard.parquet`, before filtering by `is_candidate_qualified`, three bowlers had values algebraically between Bumrah and Narine/Shaheen:
- **Nasum Ahmed:** $\text{BOWL\_CONSERVATIVE} = -0.70$ RPO (47 legal balls, 8 matches).
- **Vipraj Nigam:** $\text{BOWL\_CONSERVATIVE} = -0.91$ RPO (46 legal balls, 7 matches).
- **Ramon Simmonds:** $\text{BOWL\_CONSERVATIVE} = -0.98$ RPO (30 legal balls, 3 matches).

**Governance Audit:**
- The sample qualification rule validated in R1-06.2.2 and R1-06.2.3 requires:
  $$\text{Qualified} \iff (\text{Balls} \ge 60) \lor (\text{Balls} \ge 50 \land \text{Matches} \ge 10)$$
- None of these three bowlers satisfy this threshold:
  - Nasum Ahmed: 47 balls ($< 60$ and $< 50$).
  - Vipraj Nigam: 46 balls ($< 60$ and $< 50$).
  - Ramon Simmonds: 30 balls ($< 60$ and $< 50$).
- In `r1_06_explainability.py` (line 364), Table 1 takes `self.bowl_leaderboard[self.bowl_leaderboard["is_candidate_qualified"]].head(11)`.
- All three unexposed bowlers were correctly filtered out of Table 1 and placed into the **Emerging Peer-Beating Watchlist**.
- Qualified bowlers (Mustafizur, Ngarava, Ngidi, Ashwin, Hasan Mahmud) were properly elevated into the primary Top 10.

---

## 4. EVIDENCE & INTERPRETATION GUIDE

### 4.1 Why Are Most Bowling PRI Scores Negative?
In batting, a batter's ordinary baseline strike rate is around 125–130. Under pressure, the average batter drops by $-34.24$ SR points. Elite finishers (Pooran, Ferreira, David) maintain positive differentials relative to their ordinary baseline ($\hat{\theta}_{\text{SR}} > 0$).

In bowling, high-pressure match situations concentrate heavily in the death overs (**87.28% of legal pressure balls occur in overs 16–20**). In modern T20 cricket, death overs are structurally hostile to bowlers:
- The league-wide empirical bowling prior mean is:
  $$\mu_{\text{bw}} = +1.822756 \text{ RPO}$$
  Across all competitions from 2022 to 2026, the typical bowler concedes **1.82 runs per over more** in pressure situations than their ordinary baseline.
- Therefore, expecting a bowler to concede fewer runs in death-over pressure than in middle-over ordinary situations ($\text{diff\_economy} < 0$) is an exceptionally high bar.
- Only **Jasprit Bumrah** achieved a negative posterior economy differential ($\hat{\theta}_{\text{Econ}} = -0.20$ RPO).
- All other elite bowlers (Narine, Theekshana, Pathirana, Shaheen, Mustafizur) concede slightly more runs per over in pressure death overs than their ordinary baseline (+0.39 to +1.13 RPO).
- When $\text{Runs Saved} = -\hat{\theta}_{\text{Econ}}$ is calculated, their point estimates range from $-0.39$ to $-1.13$ RPO.
- When penalized by $1.0 \times \text{SE}$ ($\pm 0.38$ to $\pm 0.61$), their conservative lower bounds become $-0.94$ to $-1.69$ RPO.

### 4.2 Distinguishing Absolute vs. Model-Relative Performance
A critical distinction must be communicated to reviewers:

1. **Relative to Ordinary Baseline ($0.0$ RPO):**
   - 237 of the 239 evaluated bowlers have negative runs saved relative to their own ordinary baseline.
   - This reflects the macro reality of death-overs batting dominance, NOT individual bowling incompetence.
2. **Relative to Peer Pressure Environment ($+1.82$ RPO Prior Mean):**
   - All 10 shortlisted bowlers concede far fewer runs than the $+1.82$ RPO league-wide degradation.
   - For example, Maheesh Theekshana concedes $+0.55$ RPO above baseline, which is **1.27 RPO better than the peer average**.
   - His probability of outperforming the league pressure prior is **99.9%** ($P(\text{Exceed League Avg}) = 0.999$).
   - Every single bowler in the Top 10 has $P(\text{Exceed League Avg}) \ge 88.7\%$.

### 4.3 Why Conservative PRI Differs from Raw Economy Differential
- **Sunil Narine:** Raw differential is $-1.08$ RPO (better than Bumrah's raw $-0.76$ RPO). However, Narine bowled only 153 balls (vs. Bumrah's 521 balls).
  - Narine's shrinkage weight is $r = 0.494$ (shrunk 50.6% towards $+1.82$), yielding posterior mean $+0.39$ RPO.
  - Narine's posterior SE is $\pm 0.55$ RPO (vs. Bumrah's $\pm 0.36$ RPO).
  - Conservative bound: $-0.39 - 0.55 = -0.94$ RPO.
  - Bumrah's conservative bound: $+0.20 - 0.36 = -0.16$ RPO.
- **Verdict:** The conservative diagnostic successfully prevents Narine's smaller sample from leaping over Bumrah's multi-season, 521-ball mastery.

---

## 5. AUDIT CONCLUSION & VERDICT

Based on complete mathematical tracing, code inspection, and independent data recalculation:

### Final Audit Classification:
# **VERIFIED WITH LIMITATIONS — EXPLAIN THE LIMITATIONS**

### Detailed Assessment:

1. **What is Fully Verified (100% Pass):**
   - The mathematical formulas in `player_reliability.py` and `r1_06_candidate_selection.py` are executed with zero arithmetic defects.
   - The sign conventions ($\text{diff\_economy} = \text{Obs} - \text{Exp}$; $\text{Runs\_Saved} = -\text{diff\_economy}$) are mathematically rigorous.
   - Sorting by `primary_diagnostic_value` descending (`ascending=False`) correctly orders bowlers from highest to lowest conservative run containment.
   - Jasprit Bumrah (-0.16 RPO) is algebraically and competitively superior to all peers and rightfully occupies Rank 1.
   - Sample-size qualification (`is_candidate_qualified`) correctly filters out small-sample bowlers (Nasum Ahmed, Vipraj Nigam, Ramon Simmonds) before establishing Table 1.
   - The Top 10 roster is composed of exactly 10 unique, sample-qualified, verified bowlers.

2. **The Single Known Limitation (Presentation/Formatting Only):**
   - In `round1_pressure/reports/r1_06_bowling_shortlist.md`, Table 1 numbers the qualified candidates sequentially 1 through 11.
   - However, in Section 2 of that report, the individual Markdown profile headings retained their original unfiltered Parquet indices (`### #1 — Bumrah`, `### #2 — Narine`, `### #3 — Theekshana`, `### #4 — Pathirana`, `### #6 — Shaheen`, `### #7 — Mustafizur`, `### #8 — Ngarava`, `### #10 — Ngidi`, `### #12 — Ashwin`, `### #13 — Hasan Mahmud`).
   - **Recommended Action:** When compiling the final official submission document (`ROYALS_INTELLIGENCE_ROUND_1_SUBMISSION.md`), these profile headers must be sequentially renumbered Rank 1 through Rank 10 to exactly match Table 1 and the Unstop dropdown selections.

---
*Audit completed by Antigravity AI Assistant. Stopping per instructions.*
