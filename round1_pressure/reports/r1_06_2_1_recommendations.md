# ROYALS INTELLIGENCE — TASK R1-06.2.1 AUDIT REPORT
# Prioritized Recommendations & Governance Action Plan

**Audit Phase:** Task R1-06.2.1  
**Target Subject:** Governance, Classification, and Presentation Remediation  
**Repository:** `royals-intelligence`  
**Branch:** `main`  
**Starting Checkpoint:** `bed7329`  
**Architecture:** ROYALS INTELLIGENCE v4.1  
**Competition:** SupeRR Selector Season 2 — Round 1  

---

## 1. Prioritized Recommendations Register

| ID | Priority | Category | Finding / Issue | Proposed Remediation | Target File(s) |
| :--- | :---: | :--- | :--- | :--- | :--- |
| **REC-R1-06.2.1-01** | **HIGH** | Presentation Defect | Table 1 of Bowling Shortlist includes 3 non-sample-qualified bowlers due to un-filtered `head(11)` selection, duplicating with Section 3 Watchlist and omitting Ashwin, Mahmud, and Ellis. | Filter `self.bowl_leaderboard` by `is_candidate_qualified == True` prior to calling `.head(11)`. | [`round1_pressure/src/r1_06_explainability.py`](file:///c:/Users/ayush/Documents/ROYALS%20INTELLIGENCE/round1_pressure/src/r1_06_explainability.py#L340), [`round1_pressure/reports/r1_06_bowling_shortlist.md`](file:///c:/Users/ayush/Documents/ROYALS%20INTELLIGENCE/round1_pressure/reports/r1_06_bowling_shortlist.md) |
| **REC-R1-06.2.1-02** | **MEDIUM** | Cognitive Governance | Label `NEGATIVE_CONSERVATIVE_ESTIMATE` causes non-technical readers to mistake positive estimated performance for below-baseline performance. | Rename label to `POSITIVE_ESTIMATE_UNRESOLVED_BOUND` (or `POSITIVE_ESTIMATE_CONSERVATIVE_NONPOSITIVE`). | [`round1_pressure/src/r1_06_candidate_selection.py`](file:///c:/Users/ayush/Documents/ROYALS%20INTELLIGENCE/round1_pressure/src/r1_06_candidate_selection.py#L120), [`round1_pressure/src/r1_06_explainability.py`](file:///c:/Users/ayush/Documents/ROYALS%20INTELLIGENCE/round1_pressure/src/r1_06_explainability.py) |
| **REC-R1-06.2.1-03** | **MEDIUM** | Statistical Transparency | Readers may assume conservative lower bounds represent 95% classical confidence intervals rather than 1-SE (84.1%) posterior credibility. | Add explicit methodology callout to Table 1 headers stating that primary ranking reflects 84.1% one-sided posterior credibility. | [`round1_pressure/reports/r1_06_batting_shortlist.md`](file:///c:/Users/ayush/Documents/ROYALS%20INTELLIGENCE/round1_pressure/reports/r1_06_batting_shortlist.md), [`round1_pressure/reports/r1_06_bowling_shortlist.md`](file:///c:/Users/ayush/Documents/ROYALS%20INTELLIGENCE/round1_pressure/reports/r1_06_bowling_shortlist.md) |
| **REC-R1-06.2.1-04** | **LOW** | Code Cleanliness | Legacy display rounding (`round(mean, 2) < 1.82`) remains in compatibility branches of candidate selection. | Purge display rounding from all mathematical decision branches; enforce unrounded IEEE 754 64-bit float comparisons globally. | [`round1_pressure/src/r1_06_candidate_selection.py`](file:///c:/Users/ayush/Documents/ROYALS%20INTELLIGENCE/round1_pressure/src/r1_06_candidate_selection.py#L182) |

---

## 2. Detailed Remediation Specifications

### REC-R1-06.2.1-01: Correct Bowling Shortlist Table 1 Generation
- **Root Cause:** In [`round1_pressure/src/r1_06_explainability.py`](file:///c:/Users/ayush/Documents/ROYALS%20INTELLIGENCE/round1_pressure/src/r1_06_explainability.py#L340):
  ```python
  # CURRENT DEFECTIVE CODE
  top_bowl = self.bowl_leaderboard.head(11)
  ```
  `self.bowl_leaderboard` is sorted across all 239 bowlers with $\ge 30$ pressure balls. Taking `.head(11)` directly selects bowlers regardless of `is_candidate_qualified`.
- **Impact:**
  - Three players with $< 60$ balls (**Nasum Ahmed**: 47b, **Vipraj Nigam**: 46b, **Ramon Simmonds**: 30b) are inserted into Table 1 and duplicated in Section 3.A Watchlist.
  - Three fully sample-qualified bowlers (**Ravichandran Ashwin**: 147b, **Hasan Mahmud**: 90b, **Nathan Ellis**: 347b) are pushed out.
- **Recommended Remediation:**
  ```python
  # REMEDIATED CODE
  top_bowl = self.bowl_leaderboard[self.bowl_leaderboard["is_candidate_qualified"]].head(11)
  ```
- **Resulting Table 1 Roster (Top 11 Sample-Qualified Bowlers):**
  1. **Jasprit Bumrah** (521 balls, 60 matches, BOWL_CONSERVATIVE: -0.16 RPO)
  2. **Sunil Narine** (153 balls, 24 matches, BOWL_CONSERVATIVE: -0.94 RPO)
  3. **Maheesh Theekshana** (421 balls, 58 matches, BOWL_CONSERVATIVE: -1.02 RPO)
  4. **Matheesha Pathirana** (440 balls, 44 matches, BOWL_CONSERVATIVE: -1.06 RPO)
  5. **Shaheen Afridi** (191 balls, 31 matches, BOWL_CONSERVATIVE: -1.14 RPO)
  6. **Mustafizur Rahman** (578 balls, 61 matches, BOWL_CONSERVATIVE: -1.15 RPO)
  7. **Richard Ngarava** (287 balls, 34 matches, BOWL_CONSERVATIVE: -1.16 RPO)
  8. **Lungi Ngidi** (222 balls, 26 matches, BOWL_CONSERVATIVE: -1.17 RPO)
  9. **Ravichandran Ashwin** (147 balls, 21 matches, BOWL_CONSERVATIVE: -1.18 RPO)
  10. **Hasan Mahmud** (90 balls, 11 matches, BOWL_CONSERVATIVE: -1.19 RPO)
  11. **Nathan Ellis** (347 balls, 35 matches, BOWL_CONSERVATIVE: -1.20 RPO)

---

### REC-R1-06.2.1-02: Terminological Governance for Positive Point Estimates
- **Context:** Batters like Tim David, Dinesh Karthik, Ashutosh Sharma, and bowler Jasprit Bumrah have positive estimated overperformance ($\hat{\theta} > 0$), but their 1-SE lower bound is non-positive ($L \le 0$).
- **Defect:** Labeling this state `NEGATIVE_CONSERVATIVE_ESTIMATE` places "NEGATIVE" as the leading token. In stakeholder briefings, this leads decision-makers to conclude the player performs worse than baseline under pressure.
- **Remediation:** Refactor the category name to:
  $$\text{POSITIVE\_ESTIMATE\_UNRESOLVED\_BOUND}$$
  *(or `POSITIVE_ESTIMATE_CONSERVATIVE_NONPOSITIVE`)*
- This makes clear that:
  1. The point estimate indicates positive value.
  2. The statistical bound remains unconfirmed at the 84% threshold due to sample variance.

---

### REC-R1-06.2.1-03: Statistical Credibility Disclosure
- **Context:** 36.8% of Below-Baseline batters and 4.6% of Below-Baseline bowlers have 95% credible intervals that cross zero. Both Positive Conservative batters (Pooran and Ferreira) have 95% CIs crossing zero.
- **Remediation:** Add a standard methodological alert box to the head of Section 1 in both shortlist reports:
  > **Statistical Credibility Specification:**
  > Primary rankings use 1-SE conservative bounds ($\approx 84.1\%$ one-sided posterior credibility). In T20 cricket where sample sizes are constrained, requiring 95% confidence intervals would yield zero qualifying positive batters. Full 95% credible intervals are provided alongside each score to quantify remaining uncertainty without imposing artificial conservatism.

---

## 3. Downstream Execution Roadmap

1. **Audit Phase Sign-Off (R1-06.2.1):** Complete current independent verification audit and commit audit reports and test suite.
2. **Remediation Sprint (R1-06.3):**
   - Apply REC-R1-06.2.1-01 to `r1_06_explainability.py` and regenerate `r1_06_bowling_shortlist.md`.
   - Apply REC-R1-06.2.1-02 and REC-R1-06.2.1-04 to `r1_06_candidate_selection.py`.
   - Run full regression suite across Round 1 tests.
3. **Transition to R1-07:** Once R1-06.3 clean sign-off is achieved, proceed with R1-07 candidate delivery profile and match-up analysis.
