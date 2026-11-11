# ROYALS INTELLIGENCE — TASK R1-06.2.1 AUDIT REPORT
# Population Reconciliation & Multi-Level Cohort Census

**Audit Phase:** Task R1-06.2.1  
**Target Subject:** Task R1-06.2 Population Hierarchy, Invariance, and Cohort Partitioning  
**Repository:** `royals-intelligence`  
**Branch:** `main`  
**Starting Checkpoint:** `bed7329`  
**Architecture:** ROYALS INTELLIGENCE v4.1  
**Competition:** SupeRR Selector Season 2 — Round 1  

---

## 1. Executive Population Census

To prevent ambiguity between disparate subsets of the dataset, ROYALS INTELLIGENCE defines a strict **5-Level Population Hierarchy**. Each level has deterministic mathematical criteria and precise inclusion counts.

### Table 1.1: 5-Level Population Hierarchy & Cohort Sizes

| Level | Cohort Name | Qualification Criterion | Batters Count | Bowlers Count | Purpose & Analytical Role |
| :---: | :--- | :--- | :---: | :---: | :--- |
| **Level 1** | **Evaluated Population** | Any delivery faced or bowled in primary dataset matches (2021–2024) | **824** | **596** | Total player universe evaluated by ingestion and match-state pipelines. |
| **Level 2** | **Minimum-Exposure Population** | $\text{balls}_{\text{pressure}} \ge 30$ legal deliveries under pressure | **278** | **239** | Qualified for Empirical Bayes shrinkage reliability scoring; forms posterior distributions. |
| **Level 3** | **Sample-Qualified Candidates** | $\text{balls} \ge 60 \;\lor\; (\text{balls} \ge 50 \;\land\; \text{matches} \ge 10)$ | **161** | **168** | Candidates possessing sufficient exposure to qualify for primary selection shortlists. |
| **Level 4** | **Exploratory Watchlist Cohort** | $\text{balls} \ge 30$, positive or peer-beating effect, sub-sample or marginal | **19** | **98** | High-upside emerging talents ($< 60$b) and established marginal performers monitored for future selection. |
| **Level 5** | **Primary Shortlist Table** | Top-ranked candidates presented in Executive Shortlist Table 1 | **12** | **11** | Official decision-ready candidates evaluated in executive markdown reports. |

---

## 2. Exhaustive Cross-Tabulation: Two-Dimensional Classification Matrix

Task R1-06.2 implemented the Two-Dimensional Classification System separating **Performance Evidence Status (Dimension A)** from **Evidence Volume Tier (Dimension B)**.

### Table 2.1: Batting Population Cross-Tabulation ($N = 824$)

| Dimension A (Performance Evidence Status) | HIGH_VOLUME ($\ge 150$b) | MEDIUM_VOLUME ($60-149$b) | LOW_VOLUME ($30-59$b) | NO_QUALIFYING_EXPOSURE ($< 30$b) | Total |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `POSITIVE_CONSERVATIVE_EVIDENCE` | 1 | 1 | 0 | 0 | **2** |
| `NEGATIVE_CONSERVATIVE_ESTIMATE` | 13 | 4 | 2 | 0 | **19** |
| `BELOW_BASELINE_EVIDENCE` | 22 | 75 | 85 | 0 | **182** |
| `INCONCLUSIVE_EVIDENCE` | 18 | 18 | 39 | 0 | **75** |
| `NO_QUALIFYING_EXPOSURE` | 0 | 0 | 0 | 546 | **546** |
| **Total Batters** | **54** | **98** | **126** | **546** | **824** |

#### Batting Margin Checks:
- Total Qualified ($N \ge 30$): $54 + 98 + 126 = \mathbf{278}$.
- Total Non-Qualified ($N < 30$): $\mathbf{546}$.
- Total Evaluated Universe: $278 + 546 = \mathbf{824}$.
- Discrepancy: **0** (Exact margin match).

---

### Table 2.2: Bowling Population Cross-Tabulation ($N = 596$)

| Dimension A (Performance Evidence Status) | HIGH_VOLUME ($\ge 150$b) | MEDIUM_VOLUME ($60-149$b) | LOW_VOLUME ($30-59$b) | NO_QUALIFYING_EXPOSURE ($< 30$b) | Total |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `POSITIVE_CONSERVATIVE_EVIDENCE` | 0 | 0 | 0 | 0 | **0** |
| `NEGATIVE_CONSERVATIVE_ESTIMATE` | 1 | 0 | 0 | 0 | **1** |
| `BELOW_BASELINE_EVIDENCE` | 73 | 86 | 78 | 0 | **237** |
| `INCONCLUSIVE_EVIDENCE` | 1 | 0 | 0 | 0 | **1** |
| `NO_QUALIFYING_EXPOSURE` | 0 | 0 | 0 | 357 | **357** |
| **Total Bowlers** | **75** | **86** | **78** | **357** | **596** |

#### Bowling Margin Checks:
- Total Qualified ($N \ge 30$): $75 + 86 + 78 = \mathbf{239}$.
- Total Non-Qualified ($N < 30$): $\mathbf{357}$.
- Total Evaluated Universe: $239 + 357 = \mathbf{596}$.
- Discrepancy: **0** (Exact margin match).

---

## 3. Reconciliation of Sample-Qualified Expansion (DEF-04)

In Task R1-06.1, auditors noted that candidate qualification was improperly gated by an operator precedence defect:
$$\text{has\_sample}_{\text{buggy}} = (\text{balls} \ge 60 \;\lor\; (\text{balls} \ge 50 \;\land\; \text{matches} \ge 10)) \;\land\; \mathbf{matches \ge 10}$$
Because $\land\; \text{matches} \ge 10$ was appended to the entire expression, the logical condition collapsed to:
$$\text{has\_sample}_{\text{buggy}} = \text{balls} \ge 50 \;\land\; \text{matches} \ge 10$$
Any player who faced or bowled $\ge 60$ deliveries under pressure across fewer than 10 matches was disqualified.

In Task R1-06.2, DEF-04 corrected this to:
$$\text{has\_sample}_{\text{fixed}} = (\text{balls} \ge 60) \;\lor\; (\text{balls} \ge 50 \;\land\; \text{matches} \ge 10)$$

### Table 3.1: Complete Census of Newly Admitted Candidates ($N = 28$)

| Discipline | Player Name | Pressure Legal Balls | Pressure Matches | Volume Tier | Previous Status | Remediated Status |
| :--- | :--- | :---: | :---: | :--- | :--- | :--- |
| **Batting** | Ibrahim Zadran | 112 | 8 | MEDIUM_VOLUME | Disqualified | `is_candidate_qualified = True` |
| **Batting** | Abishek Porel | 88 | 8 | MEDIUM_VOLUME | Disqualified | `is_candidate_qualified = True` |
| **Batting** | George Linde | 80 | 9 | MEDIUM_VOLUME | Disqualified | `is_candidate_qualified = True` |
| **Batting** | Joshua Clarkson | 74 | 7 | MEDIUM_VOLUME | Disqualified | `is_candidate_qualified = True` |
| **Batting** | Kieron Pollard | 72 | 8 | MEDIUM_VOLUME | Disqualified | `is_candidate_qualified = True` |
| **Batting** | Aniket Verma | 71 | 9 | MEDIUM_VOLUME | Disqualified | `is_candidate_qualified = True` |
| **Batting** | Angelo Mathews | 68 | 6 | MEDIUM_VOLUME | Disqualified | `is_candidate_qualified = True` |
| **Batting** | Shamar Springer | 68 | 7 | MEDIUM_VOLUME | Disqualified | `is_candidate_qualified = True` |
| **Batting** | Imad Wasim | 68 | 6 | MEDIUM_VOLUME | Disqualified | `is_candidate_qualified = True` |
| **Batting** | Anuj Rawat | 67 | 6 | MEDIUM_VOLUME | Disqualified | `is_candidate_qualified = True` |
| **Batting** | Lalit Yadav | 67 | 9 | MEDIUM_VOLUME | Disqualified | `is_candidate_qualified = True` |
| **Batting** | Rajat Patidar | 62 | 7 | MEDIUM_VOLUME | Disqualified | `is_candidate_qualified = True` |
| **Batting** | David Willey | 61 | 8 | MEDIUM_VOLUME | Disqualified | `is_candidate_qualified = True` |
| **Bowling** | Dwayne Bravo | 92 | 9 | MEDIUM_VOLUME | Disqualified | `is_candidate_qualified = True` |
| **Bowling** | Lizaad Williams | 79 | 9 | MEDIUM_VOLUME | Disqualified | `is_candidate_qualified = True` |
| **Bowling** | Muhammad Jawadullah | 78 | 8 | MEDIUM_VOLUME | Disqualified | `is_candidate_qualified = True` |
| **Bowling** | Luke Wood | 78 | 9 | MEDIUM_VOLUME | Disqualified | `is_candidate_qualified = True` |
| **Bowling** | Benjamin Lister | 77 | 9 | MEDIUM_VOLUME | Disqualified | `is_candidate_qualified = True` |
| **Bowling** | Graham Hume | 74 | 9 | MEDIUM_VOLUME | Disqualified | `is_candidate_qualified = True` |
| **Bowling** | Tendai Chatara | 73 | 8 | MEDIUM_VOLUME | Disqualified | `is_candidate_qualified = True` |
| **Bowling** | Sakib Hussain | 72 | 9 | MEDIUM_VOLUME | Disqualified | `is_candidate_qualified = True` |
| **Bowling** | Mark Wood | 69 | 7 | MEDIUM_VOLUME | Disqualified | `is_candidate_qualified = True` |
| **Bowling** | Ehsan Khan | 68 | 8 | MEDIUM_VOLUME | Disqualified | `is_candidate_qualified = True` |
| **Bowling** | David Willey | 68 | 9 | MEDIUM_VOLUME | Disqualified | `is_candidate_qualified = True` |
| **Bowling** | Shamar Springer | 64 | 8 | MEDIUM_VOLUME | Disqualified | `is_candidate_qualified = True` |
| **Bowling** | Kane Richardson | 63 | 7 | MEDIUM_VOLUME | Disqualified | `is_candidate_qualified = True` |
| **Bowling** | Richard Gleeson | 61 | 9 | MEDIUM_VOLUME | Disqualified | `is_candidate_qualified = True` |
| **Bowling** | Praful Hinge | 60 | 7 | MEDIUM_VOLUME | Disqualified | `is_candidate_qualified = True` |

### Proof of Population Invariance:
1. **Minimum-Exposure Set Invariance:** Because every single player in Table 3.1 faced or bowled between 60 and 112 pressure balls, they were **already members of the Level 2 Minimum-Exposure Population** ($N \ge 30$).
2. **Prior & Shrinkage Invariance:** The Empirical Bayes prior distributions ($\mu, \tau^2, \sigma^2$) are fit across Level 2 ($N = 278$ and $N = 239$). Because the Level 2 population did not change by a single player, **zero posterior means, standard errors, or conservative diagnostic scores were altered** by the DEF-04 fix.
3. **Candidate Pool Shift:**
   - Batting Sample-Qualified Candidates: $148 \to \mathbf{161}$ (+13).
   - Bowling Sample-Qualified Candidates: $153 \to \mathbf{168}$ (+15).

---

## 4. Decomposition of the 100 Bowlers Outperforming Prior Mean

The Empirical Bayes league-wide bowling prior mean under pressure is:
$$\mu = 1.822755960207317 \text{ RPO extra conceded}$$
Across all 239 qualified bowlers, exactly **100 bowlers** achieve a posterior mean economy diff strictly less than this prior mean ($\hat{\theta} < \mu$).

### Table 4.1: Mathematical Census of 100 Bowlers Outperforming Prior Mean

| Category / Cohort | Count | Dimension A Status | Criteria | Representative Bowlers |
| :--- | :---: | :--- | :--- | :--- |
| **Baseline Outperformer** | **1** | `NEGATIVE_CONSERVATIVE_ESTIMATE` | $\hat{\theta} < 0.0 \land L_s \le 0.0$ | **Jasprit Bumrah** ($\hat{\theta} = -0.20$ RPO, $S = +0.20$) |
| **Inconclusive Boundary** | **1** | `INCONCLUSIVE_EVIDENCE` | $\hat{\theta} > 0.0 \land U_s \ge 0.0$ | **Sunil Narine** ($\hat{\theta} = +0.39$ RPO, $S = -0.39$, $U_s = +0.16$) |
| **Established Peer-Beaters** | **68** | `BELOW_BASELINE_EVIDENCE` | $\hat{\theta} < \mu \land \text{balls} \ge 60$ | Maheesh Theekshana, Pathirana, Shaheen Afridi, Nathan Ellis |
| **Emerging Peer-Beaters** | **30** | `BELOW_BASELINE_EVIDENCE` | $\hat{\theta} < \mu \land 30 \le \text{balls} < 60$ | Nasum Ahmed, Vipraj Nigam, Ramon Simmonds, Sakib Hussain |
| **Total Outperforming Prior** | **100** | — | $\hat{\theta} < 1.822755960207317$ | — |

*Remainder of Qualified Bowling Population:* Exactly **139 bowlers** have $\hat{\theta} \ge \mu$, representing bowlers who concede more runs under pressure than the league average pressured bowler. Total qualified bowlers = $100 + 139 = \mathbf{239}$.

---

## 5. Non-Qualified Cohort Partitioning ($< 30$ Balls)

The dataset contains 903 players who participated in primary match deliveries but did not reach the 30-ball threshold under pressure:
- **Batters ($N = 546$):**
  - Minimum exposure: 0 to 29 legal pressure balls.
  - Reason code: 100% assigned `INSUFFICIENT_EXPOSURE_DELIVERIES`.
  - Dimension A: `NO_QUALIFYING_EXPOSURE`.
  - Dimension B: `NO_QUALIFYING_EXPOSURE`.
  - Watchlist cohort: `NON_QUALIFIED`.
- **Bowlers ($N = 357$):**
  - Minimum exposure: 0 to 29 legal pressure balls.
  - Reason code: 100% assigned `INSUFFICIENT_EXPOSURE_DELIVERIES`.
  - Dimension A: `NO_QUALIFYING_EXPOSURE`.
  - Dimension B: `NO_QUALIFYING_EXPOSURE`.
  - Watchlist cohort: `NON_QUALIFIED`.

This completes the exhaustive reconciliation of all populations and cohorts in ROYALS INTELLIGENCE v4.1.
