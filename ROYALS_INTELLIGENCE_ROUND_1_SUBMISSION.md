# ROYALS INTELLIGENCE — SupeRR Selector Season 2 (Round 1)
# The Most Reliable Players Under Pressure: Analytical Framework & Verified Leaderboards

**Platform:** ROYALS INTELLIGENCE v4.1  
**Competition Target:** Rajasthan Royals — SupeRR Selector Season 2 (Round 1)  
**Challenge Objective:** Identify the Most Reliable Players Under Pressure  
**Controlling Dataset:** Official Rajasthan Royals Competition Data Pack (2022–2026)  
**Dataset Baseline:** Exactly 200,999 Deliveries | 883 Matches | 141 Tournaments (IPL & Senior T20Is)  
**Accepted Checkpoint:** `6005022` (`feat(r1-06.2.3): final data-count reconciliation and statistical wording correction`)  
**Document Classification:** Official Round 1 Competition Deliverable & Methodology Report  

---

## 1. TITLE & EXECUTIVE SUMMARY

### 1.1 Executive Overview
ROYALS INTELLIGENCE presents an evidence-backed, mathematically audited, and statistically governed decision system engineered to resolve the core challenge of **SupeRR Selector Season 2 (Round 1)**: distinguishing cricketers who consistently rise to the occasion under acute match pressure from those whose performance deteriorates.

Traditional cricket analysis often relies on raw, unadjusted averages or isolated match-winning highlights, which conflate player quality with batting order, match phase, and sample size volatility. ROYALS INTELLIGENCE addresses these flaws through a rigorous five-stage analytical architecture:
1. **Dynamic Match-State Reconstruction:** Evaluates game leverage ball-by-ball across 200,999 deliveries, adjusting for required run rates, wickets in hand, balls remaining, and chase context.
2. **Context-Stratified Ordinary Baselines:** Constructs empirical benchmarks across 12 distinct match-context strata (phase $\times$ tournament tier $\times$ innings) to eliminate structural phase and venue biases.
3. **Hierarchical Empirical Bayes Shrinkage:** Pulls small-sample noise towards empirical league priors, establishing robust posterior performance distributions for every player.
4. **Conservative Value-at-Risk Ranking:** Ranks candidates strictly by their **one-standard-error lower credible bound** (Conservative PRI), prioritizing high-volume, low-uncertainty dependability over small-sample outliers.
5. **Two-Dimensional Classification & Sample Qualification:** Strictly separates performance direction from sample exposure, requiring $\ge 60$ balls (or $\ge 50$ balls and $\ge 10$ matches) for primary leaderboard eligibility.

---

### 1.2 Official Unstop Submission Selection Guide
The tables below provide the exact, verified Top 10 rankings to be selected in the Unstop dropdown fields, cross-referenced with primary statistical diagnostics:

#### Top 10 Batters Under Pressure (Unstop Dropdown Guide)
| Selection Rank | Player Name | Governing Metric: Conservative PRI | Posterior Mean Difference ($\hat{\theta}$) | Estimation Uncertainty (SE) | 95% Bayesian Credible Region | Pressure Balls | Matches | Tournament Qualification |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Rank 1** | **Nicholas Pooran** | **+2.2 SR pts** | +16.2 SR pts | $\pm 14.0$ | [-11.2, +43.6] | 212 | 26 | `DUAL_TOURNAMENT_QUALIFIED` |
| **Rank 2** | **Donovan Ferreira** | **+0.9 SR pts** | +20.7 SR pts | $\pm 19.8$ | [-18.0, +59.4] | 84 | 13 | `IPL_QUALIFIED` |
| **Rank 3** | **Tim David** | **-2.5 SR pts** | +9.6 SR pts | $\pm 12.1$ | [-14.1, +33.3] | 290 | 33 | `DUAL_TOURNAMENT_QUALIFIED` |
| **Rank 4** | **Dinesh Karthik** | **-2.7 SR pts** | +9.2 SR pts | $\pm 11.9$ | [-14.1, +32.6] | 260 | 30 | `DUAL_TOURNAMENT_QUALIFIED` |
| **Rank 5** | **Ashutosh Sharma** | **-3.6 SR pts** | +10.3 SR pts | $\pm 13.9$ | [-17.0, +37.6] | 191 | 20 | `IPL_QUALIFIED` |
| **Rank 6** | **Marcus Stoinis** | **-5.8 SR pts** | +7.1 SR pts | $\pm 12.9$ | [-18.1, +32.3] | 220 | 32 | `DUAL_TOURNAMENT_QUALIFIED` |
| **Rank 7** | **Naman Dhir** | **-6.9 SR pts** | +7.9 SR pts | $\pm 14.9$ | [-21.2, +37.1] | 145 | 18 | `IPL_QUALIFIED` |
| **Rank 8** | **Rinku Singh** | **-7.0 SR pts** | +3.4 SR pts | $\pm 10.4$ | [-17.0, +23.8] | 363 | 48 | `DUAL_TOURNAMENT_QUALIFIED` |
| **Rank 9** | **Tristan Stubbs** | **-8.2 SR pts** | +2.4 SR pts | $\pm 10.5$ | [-18.3, +23.0] | 266 | 33 | `DUAL_TOURNAMENT_QUALIFIED` |
| **Rank 10** | **Sherfane Rutherford**| **-8.2 SR pts** | +6.9 SR pts | $\pm 15.1$ | [-22.7, +36.6] | 151 | 21 | `DUAL_TOURNAMENT_QUALIFIED` |

*(Note: In Table 1, Candidates #11 Rovman Powell [-8.8 SR pts] and #12 Aiden Markram [-9.0 SR pts] represent verified sample-qualified reserve alternates).*

---

#### Top 10 Bowlers Under Pressure (Unstop Dropdown Guide)
| Selection Rank | Player Name | Governing Metric: Conservative Runs Saved | Posterior Mean Difference ($\hat{\theta}$) | Estimation Uncertainty (SE) | 95% Bayesian Credible Region | Pressure Balls | Matches | Tournament Qualification |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Rank 1** | **Jasprit Bumrah** | **-0.16 RPO** | -0.20 RPO | $\pm 0.36$ | [-0.90, +0.50] | 521 | 60 | `DUAL_TOURNAMENT_QUALIFIED` |
| **Rank 2** | **Sunil Narine** | **-0.94 RPO** | +0.39 RPO | $\pm 0.55$ | [-0.68, +1.47] | 153 | 24 | `IPL_QUALIFIED` |
| **Rank 3** | **Maheesh Theekshana**| **-0.96 RPO** | +0.55 RPO | $\pm 0.41$ | [-0.25, +1.35] | 421 | 58 | `DUAL_TOURNAMENT_QUALIFIED` |
| **Rank 4** | **Matheesha Pathirana**| **-1.05 RPO** | +0.63 RPO | $\pm 0.41$ | [-0.18, +1.44] | 440 | 44 | `DUAL_TOURNAMENT_QUALIFIED` |
| **Rank 5** | **Shaheen Afridi** | **-1.43 RPO** | +0.91 RPO | $\pm 0.52$ | [-0.10, +1.92] | 191 | 31 | `T20I_QUALIFIED` |
| **Rank 6** | **Mustafizur Rahman** | **-1.47 RPO** | +1.09 RPO | $\pm 0.38$ | [+0.35, +1.84] | 578 | 61 | `DUAL_TOURNAMENT_QUALIFIED` |
| **Rank 7** | **Richard Ngarava** | **-1.56 RPO** | +1.10 RPO | $\pm 0.46$ | [+0.19, +2.01] | 287 | 34 | `T20I_QUALIFIED` |
| **Rank 8** | **Lungi Ngidi** | **-1.65 RPO** | +1.13 RPO | $\pm 0.53$ | [+0.09, +2.16] | 222 | 26 | `DUAL_TOURNAMENT_QUALIFIED` |
| **Rank 9** | **Ravichandran Ashwin**| **-1.67 RPO** | +1.11 RPO | $\pm 0.57$ | [-0.00, +2.22] | 147 | 21 | `IPL_QUALIFIED` |
| **Rank 10** | **Hasan Mahmud** | **-1.69 RPO** | +1.08 RPO | $\pm 0.61$ | [-0.11, +2.28] | 90 | 11 | `T20I_QUALIFIED` |

*(Note: In Table 1, Candidate #11 Nathan Ellis [-1.71 RPO] represents a verified sample-qualified reserve alternate).*

---

## 2. CHALLENGE OBJECTIVE & EVALUATION SCOPE

### 2.1 The Official SupeRR Selector Challenge
The official problem statement issued by the Rajasthan Royals analytics group specifies:
> *"Build a data-driven system that measures how batters and bowlers perform in high-pressure match situations compared with their usual performance levels. Use your system to identify and rank the players who deliver most consistently when it matters."*

The challenge explicitly requires:
- **Two Ordered Top-10 Lists:** The 10 best-performing batters and 10 best-performing bowlers under pressure (Rank 1 through 10, no repeats).
- **A Comprehensive Methodology Report:** Detailing pressure definition, performance measurement, fair comparisons (sample sizes, IPL vs T20I), empirical evidence, and reliability/limitations.

### 2.2 Evaluation Population Boundaries
To ensure absolute scientific integrity:
- **Global Population Scope:** The evaluation evaluates **ALL players** present in the supplied dataset across the 2022–2026 seasons.
- **No Squad Restrictions:** The evaluation is strictly global and empirical. It is **NOT** restricted to Rajasthan Royals players, Indian domestic players, or uncapped players. Every player who meets sample exposure thresholds is evaluated on an equal statistical footing.
- **Strict Discipline Separation:** In accordance with cricket principles, batting and bowling are evaluated independently. Universal composite or all-rounder index scores are strictly segregated from primary leaderboards to avoid conflating fundamentally distinct skill distributions.

---

## 3. DATASET PROVENANCE & COVERAGE

### 3.1 Source Dataset Inventory & Verification
The ROYALS INTELLIGENCE pipeline operates strictly upon the official competition dataset supplied for SupeRR Selector Season 2. Every file was inspected, row-counted, and cryptographically verified via SHA-256:

| Dataset Filename | Format | File Size | Exact Row Count | Cryptographic SHA-256 Checksum |
| :--- | :---: | :---: | :---: | :--- |
| `ball_by_ball.csv` | CSV | 41,071,609 bytes (39.17 MB) | 200,999 records | `A3926F49D2C684DCA2A5D2DE535A02C5EE46EA654CA1E79DD31C69E7544E9889` |
| `matches.csv` | CSV | 123,864 bytes (0.12 MB) | 883 records | `BB100AB84B8B9A15160C1F2315CF675210131A30E779EC5079FD5403DCF56EEF` |
| `competitions.csv` | CSV | 7,624 bytes (0.01 MB) | 141 records | `507CEB7189F972D4E4F299DDCFC97F3C3247AF1913F6291106F161FA8353FD9B` |
| `playing_eleven.csv` | CSV | 966,287 bytes (0.92 MB) | 28,381 records | `7517C73722A28D5D61C808CCF0CBED315A8780586D02E946EB9A7F5DAF011C27` |
| `teams.csv` | CSV | 6,922 bytes (0.01 MB) | 353 records | `A65E5922A9B3BF49247B24FC9471782E700EFB31F8DCC5042923238B87C50A5D` |
| `competition_team_player_mapping.csv` | CSV | 462,969 bytes (0.44 MB) | 6,413 records | `1DED4E42A933618572D6E2C3A521C3257EB1844FAB4456D567D77CBB2D3BBB12` |

### 3.2 Delivery Legality & Counting Reconciliation
Task R1-06.2.3 definitively resolved all historical reporting discrepancies:
- **Established QA Baseline:** Exactly **200,999 delivery rows** across **883 matches**.
- **Match Accounting:** Exactly **867 matches** contain ball-by-ball delivery logs (averaging 231.83 balls per match). Exactly **16 matches** were abandoned or declared No Result without a single ball bowled (accounting for the 883 total match records).
- **Zero Synthetic Contamination:** Zero external web scraping, simulated balls, or synthetic auction data were introduced. The pipeline is 100% deterministic and reproducible.

---

## 4. PRESSURE SITUATION DEFINITION

### 4.1 Multi-Factor High-Leverage Framework
Pressure in T20 cricket is multi-dimensional. A fixed definition (e.g., "overs 16–20 only") fails to capture game leverage because a team chasing 40 off 30 with 9 wickets in hand is not under pressure, whereas a team defending 15 off 12 in a semifinal is under intense pressure.

ROYALS INTELLIGENCE models pressure ball-by-ball using five contextual signals:
1. **Required Run Rate (RRR):** For chasing innings (Innings 2), required run rate per over relative to par.
2. **Balls Remaining ($B_{\text{rem}}$):** Closeness to innings completion ($B_{\text{rem}} \le 36$).
3. **Wickets in Hand ($W_{\text{rem}}$):** Batting collapse severity ($W_{\text{rem}} \le 4$).
4. **Contest Margin / Score Proximity:** In 1st innings, score deficit relative to projected venue par.
5. **Innings Leverage & Stage:** Elimination/knockout status and match phase.

### 4.2 Strict vs. Permissive Pressure Regimes
Two analytical definitions were implemented and cross-audited:
- **Strict Pressure (Governing Primary Scope):** High-leverage, game-critical deliveries only.
  - *Chasing (Innings 2):* $\text{RRR} \ge 9.0$ with $B_{\text{rem}} \le 36$, OR any situation where $\text{RRR} \ge 12.0$, OR late-innings close finishes ($B_{\text{rem}} \le 18$ with runs required $\le 36$ and wickets in hand $\le 5$).
  - *Setting Target (Innings 1):* Overs 16–20 where team has lost $\ge 4$ wickets, OR overs 18–20 in any contested match.
  - *Coverage:* Exactly **37,014 legal bowling deliveries** and **31,163 legal batting deliveries**.
- **Permissive Pressure (Secondary Sensitivity Scope):** Broader situational filter capturing all deliveries where win probability volatility is elevated ($\pm 8\%$ WPA per over).
  - *Coverage:* Exactly 47,820 bowling deliveries and 40,518 batting deliveries.

### 4.3 Death-Overs Concentration
A foundational empirical finding of Stage R1-03:
- **Bowling Pressure:** **87.28%** of all strict pressure deliveries occur in the death overs (overs 16–20) (32,307 of 37,014 legal balls).
- **Batting Pressure:** **78.95%** of all strict pressure deliveries occur in the death overs (24,603 of 31,163 legal balls).
This reflects the tactical reality of modern T20 cricket: game-deciding leverage overwhelmingly clusters in the final five overs of both innings.

---

## 5. PERFORMANCE MEASUREMENT & ORDINARY BASELINES

### 5.1 Why Raw Averages Fail
Evaluating players by raw strike rate or raw economy under pressure produces severe bias:
- A death-overs specialist batting in overs 18–20 has an expected baseline strike rate of 165+, whereas an opener batting in the middle overs has an expected baseline of 130.
- A death-overs bowler bowling overs 19 and 20 has an expected economy baseline of 10.5+ RPO, whereas a powerplay specialist has an expected baseline of 7.2 RPO.
Comparing their raw pressure numbers without adjusting for entry point and phase severely distorts candidate quality.

### 5.2 Context-Stratified 12-Cell Baseline Engine
ROYALS INTELLIGENCE constructs individual, context-weighted expected baselines for every delivery by stratifying the entire non-pressure (ordinary) dataset into **12 distinct context cells**:
$$\text{Cell} = \text{Phase } (\text{Powerplay, Middle, Death}) \times \text{Tournament Tier } (\text{IPL, Senior T20I}) \times \text{Innings } (\text{1st Innings, 2nd Innings})$$

For each candidate, the expected performance under pressure is the weighted sum of their personal ball exposure across these 12 context cells:
$$\text{Expected\_SR}_i = \frac{\sum_{c=1}^{12} \text{Balls}_{i, c} \cdot \overline{\text{SR}}_c}{\text{Total Legal Pressure Balls}_i}$$
$$\text{Expected\_Economy}_i = \frac{\sum_{c=1}^{12} \text{Balls}_{i, c} \cdot \overline{\text{Econ}}_c}{\text{Total Legal Pressure Balls}_i}$$

### 5.3 Performance Differentials
The raw performance differential measures how much a player out- or under-performs context expectations:
- **Batting Differential:** $\text{diff\_SR}_i = \text{Observed\_SR}_i - \text{Expected\_SR}_i$ (Strike-rate points; positive is superior).
- **Bowling Differential:** $\text{diff\_economy}_i = \text{Observed\_Economy}_i - \text{Expected\_Economy}_i$ (Runs per over; negative indicates superior containment).
- **Bowling Runs Saved per Over:** $\text{Runs\_Saved}_i = -\text{diff\_economy}_i$ (Inverts economy diff so that positive represents saving runs).

---

## 6. BAYESIAN RELIABILITY METHODOLOGY & PRI INTERPRETATION

### 6.1 Empirical Bayes Hierarchical Shrinkage
Raw differentials in cricket samples are heavily influenced by small-sample noise. A batter with 32 balls who hit three sixes might boast a $+35$ SR differential, while a veteran with 350 balls sits at $+10$. 

To eliminate small-sample bias, ROYALS INTELLIGENCE applies empirical Bayes shrinkage:
$$\hat{\theta}_i = (1 - r_i) \cdot \mu + r_i \cdot \text{diff}_i$$
where:
- $\mu$ is the empirical league prior mean under pressure:
  - **Batting Prior:** $\mu_b = -34.238444$ SR pts (on average, batters strike 34.24 points slower under pressure).
  - **Bowling Prior:** $\mu_{\text{bw}} = +1.822756$ RPO (on average, bowlers concede 1.82 runs/over more under pressure).
- $\tau$ is the empirical between-player standard deviation:
  - $\tau_b = 32.937741$ SR pts (wide spread in batting adaptability).
  - $\tau_{\text{bw}} = 0.770593$ RPO (tighter distribution among specialist bowlers).
- $r_i = \frac{\tau^2}{\tau^2 + \sigma_i^2}$ is the shrinkage reliability weight ($0 \le r_i \le 1$), where $\sigma_i^2$ is individual sampling variance.
- $\text{SE}_{\text{post}, i} = \sqrt{\frac{1}{\frac{1}{\tau^2} + \frac{1}{\sigma_i^2}}}$ is the posterior standard error.

### 6.2 Governing Primary Ranking Metric: Conservative Lower Credible Bound
To select players who deliver consistently and reliably, rankings are governed by the **Conservative Lower Credible Bound (Value-at-Risk at 1 Standard Error)**:

$$\text{BAT\_CONSERVATIVE}_i = \hat{\theta}_{\text{SR}, i} - 1.0 \times \text{SE}_{\text{post}, i}$$
$$\text{BOWL\_CONSERVATIVE}_i = -\hat{\theta}_{\text{Econ}, i} - 1.0 \times \text{SE}_{\text{post}, i}$$

#### Rigorous Statistical Uncertainty Disclosure:
> **"Under an approximate normal posterior distribution, a positive one-standard-error lower bound implies posterior probability above zero greater than approximately 84.1%. This is a directional uncertainty diagnostic, not a 95% credible interval, conventional 95% statistical significance, or a guarantee of future performance."**

### 6.3 Interpretation of Score Directions

#### Batting Direction (Higher / More Positive is Better):
- $\text{BAT\_CONSERVATIVE} > 0$: Strong statistical evidence of outperforming ordinary baseline under pressure even after a 1-sigma penalty (Nicholas Pooran: $+2.2$, Donovan Ferreira: $+0.9$).
- $\text{BAT\_CONSERVATIVE} \le 0$ with $\hat{\theta}_{\text{SR}} > 0$: Positive estimated overperformance, but estimation uncertainty spans zero (Tim David, Dinesh Karthik, Ashutosh Sharma).

#### Bowling Direction (Higher / Less Negative is Better):
- All bowling conservative scores are sorted **descending** (`ascending=False`):
  $$-0.16 > -0.94 > -0.96 > -1.05 > -1.43 > -1.47 > -1.56 > -1.65 > -1.67 > -1.69$$
- **Why Bowling Scores Are Negative:** Because death overs are structurally hostile to bowlers, the league prior is $+1.82$ RPO conceded. Only **Jasprit Bumrah** has a negative posterior economy differential ($\hat{\theta}_{\text{Econ}} = -0.20$ RPO). All other bowlers concede $+0.39$ to $+1.13$ RPO above ordinary baseline.
- **Peer-Beaters vs. Baseline:** Relative to ordinary middle-overs cricket, bowlers concede slightly more runs; but **relative to the $+1.82$ RPO league prior under pressure**, all 10 bowlers are elite peer-beaters ($P(\text{Beat League Prior}) \ge 88.7\%$ for all 10). Bumrah ranks #1 at $-0.16$ RPO, outclassing all peers.

---

## 7. FAIR COMPARISON & SAMPLE QUALIFICATION

### 7.1 Two-Tier Exposure & Qualification Rules
To ensure fairness across tournaments and prevent low-sample flyers from displacing established performers:
1. **Tier 1: Minimum Exposure Filter:** $\ge 30$ legal pressure deliveries faced or bowled. Excludes players with zero or trivial pressure appearances.
2. **Tier 2: Candidate Sample Qualification Rule (Locked in R1-06.2):**
   $$\text{Qualified Candidate} \iff (\text{Balls} \ge 60) \lor (\text{Balls} \ge 50 \land \text{Matches} \ge 10)$$

### 7.2 Population Hierarchy Accounting
- **Batting Population ($N = 824$ total batters):**
  - Evaluated: 824
  - Minimum Exposure ($n \ge 30$ balls): 278
  - Sample-Qualified: **161**
  - Primary Table 1 Shortlist: **10** (plus 2 reserve alternates)
  - Remaining Qualified Cohort: 149
  - Exploratory Emerging Watchlist ($n < 60$ balls): 2 (Cooper Connolly, Ishan Kishan)
  - Exploratory Established Watchlist: 17
- **Bowling Population ($N = 596$ total bowlers):**
  - Evaluated: 596
  - Minimum Exposure ($n \ge 30$ balls): 239
  - Sample-Qualified: **168**
  - Primary Table 1 Shortlist: **10** (plus 1 reserve alternate)
  - Remaining Qualified Cohort: 157
  - Exploratory Emerging Watchlist ($n < 60$ balls): 30 (including Nasum Ahmed, Vipraj Nigam, Ramon Simmonds)
  - Exploratory Established Watchlist: 68

### 7.3 Tournament Classification (IPL vs. Senior T20I)
- `DUAL_TOURNAMENT_QUALIFIED`: Candidate accumulated $\ge 30$ legal pressure deliveries in **both** IPL and Senior T20Is. Confirms sample availability across both competition environments.
- `IPL_QUALIFIED`: Candidate qualified primarily through IPL exposure ($< 30$ balls in T20Is).
- `T20I_QUALIFIED`: Candidate qualified primarily through Senior T20I exposure ($< 30$ balls in IPL).

---

## 8. TOP 10 BATTERS UNDER PRESSURE (TABLE 1)

The verified Top 10 Batters Under Pressure, ordered strictly by **Conservative PRI ($	ext{BAT\_CONSERVATIVE}$)**:

| Rank | Batter Name | BAT_CONSERVATIVE (SR pts) | Posterior Mean $\hat{\theta}$ | Posterior SE | 95% Credible Interval | Pressure Balls | Matches | Tournament Qualification | P(Beat Base) | P(Exceed League Avg) | Two-Dimensional Classification |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | **Nicholas Pooran** | **+2.2** | +16.2 | $\pm 14.0$ | [-11.2, +43.6] | 212 | 26 | `DUAL_TOURNAMENT_QUALIFIED` | 87.7% | 100.0% | `POSITIVE_CONSERVATIVE_EVIDENCE (HIGH_VOLUME)` |
| **2** | **Donovan Ferreira** | **+0.9** | +20.7 | $\pm 19.8$ | [-18.0, +59.4] | 84 | 13 | `IPL_QUALIFIED` | 85.2% | 99.7% | `POSITIVE_CONSERVATIVE_EVIDENCE (MEDIUM_VOLUME)` |
| **3** | **Tim David** | **-2.5** | +9.6 | $\pm 12.1$ | [-14.1, +33.3] | 290 | 33 | `DUAL_TOURNAMENT_QUALIFIED` | 78.6% | 100.0% | `POSITIVE_ESTIMATE_UNRESOLVED (HIGH_VOLUME)` |
| **4** | **Dinesh Karthik** | **-2.7** | +9.2 | $\pm 11.9$ | [-14.1, +32.6] | 260 | 30 | `DUAL_TOURNAMENT_QUALIFIED` | 78.1% | 100.0% | `POSITIVE_ESTIMATE_UNRESOLVED (HIGH_VOLUME)` |
| **5** | **Ashutosh Sharma** | **-3.6** | +10.3 | $\pm 13.9$ | [-17.0, +37.6] | 191 | 20 | `IPL_QUALIFIED` | 77.0% | 99.9% | `POSITIVE_ESTIMATE_UNRESOLVED (HIGH_VOLUME)` |
| **6** | **Marcus Stoinis** | **-5.8** | +7.1 | $\pm 12.9$ | [-18.1, +32.3] | 220 | 32 | `DUAL_TOURNAMENT_QUALIFIED` | 70.9% | 99.9% | `POSITIVE_ESTIMATE_UNRESOLVED (HIGH_VOLUME)` |
| **7** | **Naman Dhir** | **-6.9** | +7.9 | $\pm 14.9$ | [-21.2, +37.1] | 145 | 18 | `IPL_QUALIFIED` | 70.4% | 99.8% | `POSITIVE_ESTIMATE_UNRESOLVED (MEDIUM_VOLUME)` |
| **8** | **Rinku Singh** | **-7.0** | +3.4 | $\pm 10.4$ | [-17.0, +23.8] | 363 | 48 | `DUAL_TOURNAMENT_QUALIFIED` | 62.8% | 100.0% | `POSITIVE_ESTIMATE_UNRESOLVED (HIGH_VOLUME)` |
| **9** | **Tristan Stubbs** | **-8.2** | +2.4 | $\pm 10.5$ | [-18.3, +23.0] | 266 | 33 | `DUAL_TOURNAMENT_QUALIFIED` | 58.9% | 100.0% | `POSITIVE_ESTIMATE_UNRESOLVED (HIGH_VOLUME)` |
| **10** | **Sherfane Rutherford**| **-8.2** | +6.9 | $\pm 15.1$ | [-22.7, +36.6] | 151 | 21 | `DUAL_TOURNAMENT_QUALIFIED` | 67.7% | 99.7% | `POSITIVE_ESTIMATE_UNRESOLVED (HIGH_VOLUME)` |

- **Sample-Qualified Alternates / Reserves:**
  - Rank 11: **Rovman Powell** (Conservative PRI: **-8.8 SR pts**, Posterior: +1.7, SE: $\pm 10.5$, 342 balls, 47 matches, `DUAL_TOURNAMENT_QUALIFIED`).
  - Rank 12: **Aiden Markram** (Conservative PRI: **-9.0 SR pts**, Posterior: +5.7, SE: $\pm 14.7$, 133 balls, 13 matches, `DUAL_TOURNAMENT_QUALIFIED`).

---

## 9. TOP 10 BOWLERS UNDER PRESSURE (TABLE 1)

The verified Top 10 Bowlers Under Pressure, ordered strictly by **Conservative Runs Saved per Over ($	ext{BOWL\_CONSERVATIVE}$ descending)**:

| Rank | Bowler Name | BOWL_CONSERVATIVE (Runs Saved) | Posterior Mean Diff | Posterior SE | 95% Credible Interval | Pressure Balls | Matches | Tournament Qualification | P(Beat Base) | P(Exceed League Avg) | Two-Dimensional Classification |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | **Jasprit Bumrah** | **-0.16 RPO** | -0.20 RPO | $\pm 0.36$ | [-0.90, +0.50] | 521 | 60 | `DUAL_TOURNAMENT_QUALIFIED` | 71.1% | 100.0% | `POSITIVE_ESTIMATE_UNRESOLVED (HIGH_VOLUME)` |
| **2** | **Sunil Narine** | **-0.94 RPO** | +0.39 RPO | $\pm 0.55$ | [-0.68, +1.47] | 153 | 24 | `IPL_QUALIFIED` | 23.8% | 99.5% | `INCONCLUSIVE_EVIDENCE (HIGH_VOLUME)` |
| **3** | **Maheesh Theekshana**| **-0.96 RPO** | +0.55 RPO | $\pm 0.41$ | [-0.25, +1.35] | 421 | 58 | `DUAL_TOURNAMENT_QUALIFIED` | 9.0% | 99.9% | `BELOW_BASELINE_EVIDENCE (HIGH_VOLUME)` |
| **4** | **Matheesha Pathirana**| **-1.05 RPO** | +0.63 RPO | $\pm 0.41$ | [-0.18, +1.44] | 440 | 44 | `DUAL_TOURNAMENT_QUALIFIED` | 6.2% | 99.8% | `BELOW_BASELINE_EVIDENCE (HIGH_VOLUME)` |
| **5** | **Shaheen Afridi** | **-1.43 RPO** | +0.91 RPO | $\pm 0.52$ | [-0.10, +1.92] | 191 | 31 | `T20I_QUALIFIED` | 3.8% | 96.1% | `BELOW_BASELINE_EVIDENCE (HIGH_VOLUME)` |
| **6** | **Mustafizur Rahman** | **-1.47 RPO** | +1.09 RPO | $\pm 0.38$ | [+0.35, +1.84] | 578 | 61 | `DUAL_TOURNAMENT_QUALIFIED` | 0.2% | 97.2% | `BELOW_BASELINE_EVIDENCE (HIGH_VOLUME)` |
| **7** | **Richard Ngarava** | **-1.56 RPO** | +1.10 RPO | $\pm 0.46$ | [+0.19, +2.01] | 287 | 34 | `T20I_QUALIFIED` | 0.9% | 94.1% | `BELOW_BASELINE_EVIDENCE (HIGH_VOLUME)` |
| **8** | **Lungi Ngidi** | **-1.65 RPO** | +1.13 RPO | $\pm 0.53$ | [+0.09, +2.16] | 222 | 26 | `DUAL_TOURNAMENT_QUALIFIED` | 1.6% | 90.7% | `BELOW_BASELINE_EVIDENCE (HIGH_VOLUME)` |
| **9** | **Ravichandran Ashwin**| **-1.67 RPO** | +1.11 RPO | $\pm 0.57$ | [-0.00, +2.22] | 147 | 21 | `IPL_QUALIFIED` | 2.5% | 89.6% | `BELOW_BASELINE_EVIDENCE (MEDIUM_VOLUME)` |
| **10** | **Hasan Mahmud** | **-1.69 RPO** | +1.08 RPO | $\pm 0.61$ | [-0.11, +2.28] | 90 | 11 | `T20I_QUALIFIED` | 3.7% | 88.7% | `BELOW_BASELINE_EVIDENCE (MEDIUM_VOLUME)` |

- **Sample-Qualified Alternate / Reserve:**
  - Rank 11: **Nathan Ellis** (Conservative Runs Saved: **-1.71 RPO**, Posterior: +1.24, SE: $\pm 0.46$, 347 balls, 35 matches, `DUAL_TOURNAMENT_QUALIFIED`).

---

## 10. INDIVIDUAL EVIDENCE CARDS FOR ALL 20 SELECTED PLAYERS

The candidate profiles below present the complete 11-dimension evidentiary audit for every player in the official submission Top 10 rosters. Profile headings are renumbered sequentially from **Rank 1 to Rank 10** for both disciplines.

---

### Part A: Batting Candidate Evidence Cards (Rank 1 to 10)

### Rank 1 — Nicholas Pooran (`POSITIVE_CONSERVATIVE_EVIDENCE (HIGH_VOLUME)`)
- **Why Considered:** Ranked #1 in Batting with a conservative diagnostic value of +2.25 SR pts. Two-Dimensional Classification: 'POSITIVE_CONSERVATIVE_EVIDENCE (HIGH_VOLUME)' (Evidence Status: `POSITIVE_CONSERVATIVE_EVIDENCE`, Volume: `HIGH_VOLUME`, Cohort: `CONFIRMED_POSITIVE_RELIABILITY`). Sample qualification: QUALIFIED (legacy: 'STRONG_EVIDENCE'). Under an approximate normal posterior distribution, a positive one-standard-error lower bound implies posterior probability above zero greater than approximately 84.1%. This is a directional uncertainty diagnostic, not a 95% credible interval, conventional 95% statistical significance, or a guarantee of future performance (95% CI spans zero).
- **Evidence Volume:** 212 legal pressure deliveries bowled/faced, categorized in 'HIGH_VOLUME' (Volume Tier B).
- **Temporal Stability:** Demonstrated across 26 unique pressure matches and 5 active seasons (Distribution: 2022: 47b, 2023: 49b, 2024: 102b, 2025: 4b, 2026: 10b).
- **Observed vs Expected:** Observed Strike Rate: 190.57 (raw difference of +27.31 SR pts versus context expectation). | Context-adjusted expectation: 163.25 Strike Rate, derived from stratified 12-cell baselines across phase, tournament tier, and innings.
- **Conservative Diagnostic Score:** BAT_CONSERVATIVE = +2.25 SR pts. Represents the 1-SE conservative diagnostic bound (posterior mean minus 1.0 SE (SR points)). Under an approximate normal posterior distribution, a positive one-standard-error lower bound implies posterior probability above zero greater than approximately 84.1%. This is a directional uncertainty diagnostic, not a 95% credible interval, conventional 95% statistical significance, or a guarantee of future performance.
- **Uncertainty & CI:** Posterior standard error: $\pm$13.98 SR pts. Shrinkage weight $r = 0.820$. | 95% Credible Interval: [-11.17, 43.63] SR pts (width: 54.80 SR pts). Displayed separately from the 1-SE diagnostic score; reflects a two-sided 95% Bayesian credible region (z = 1.96).
- **Competition Support:** Coverage: BOTH (144 balls in IPL, 68 balls in Senior T20I | Classification: `DUAL_TOURNAMENT_QUALIFIED`). Supported by substantial sample in both competitions. Note: Dual-tournament qualification indicates sample exposure availability in both competitions, NOT statistical proof of cross-competition skill transferability.
- **Key Limitations:** Robust sample volume and multi-season stability; residual uncertainty bounded by 95% CI.
- **Sensitivity Profile:** Under unpenalized posterior mean, performance is +16.23 SR pts. Model credibility against baseline: 87.7%; against league-wide pressure mean (prior mean $\mu = -34.24 SR pts$): 100.0%. Exceeding league average under pressure compares against degraded match conditions, NOT fellow shortlisted candidates. Exploratory PRI without TCF: 95.2; Experimental PRI with TCF: 83.4.

---

### Rank 2 — Donovan Ferreira (`POSITIVE_CONSERVATIVE_EVIDENCE (MEDIUM_VOLUME)`)
- **Why Considered:** Ranked #2 in Batting with a conservative diagnostic value of +0.93 SR pts. Two-Dimensional Classification: 'POSITIVE_CONSERVATIVE_EVIDENCE (MEDIUM_VOLUME)' (Evidence Status: `POSITIVE_CONSERVATIVE_EVIDENCE`, Volume: `MEDIUM_VOLUME`, Cohort: `CONFIRMED_POSITIVE_RELIABILITY`). Sample qualification: QUALIFIED (legacy: 'STRONG_EVIDENCE'). Under an approximate normal posterior distribution, a positive one-standard-error lower bound implies posterior probability above zero greater than approximately 84.1%. This is a directional uncertainty diagnostic, not a 95% credible interval, conventional 95% statistical significance, or a guarantee of future performance (95% CI spans zero).
- **Evidence Volume:** 84 legal pressure deliveries bowled/faced, categorized in 'MEDIUM_VOLUME' (Volume Tier B).
- **Temporal Stability:** Demonstrated across 13 unique pressure matches and 4 active seasons (Distribution: 2023: 14b, 2024: 8b, 2025: 18b, 2026: 44b).
- **Observed vs Expected:** Observed Strike Rate: 220.24 (raw difference of +51.60 SR pts versus context expectation). | Context-adjusted expectation: 168.64 Strike Rate, derived from stratified 12-cell baselines across phase, tournament tier, and innings.
- **Conservative Diagnostic Score:** BAT_CONSERVATIVE = +0.93 SR pts. Represents the 1-SE conservative diagnostic bound (posterior mean minus 1.0 SE (SR points)). Under an approximate normal posterior distribution, a positive one-standard-error lower bound implies posterior probability above zero greater than approximately 84.1%. This is a directional uncertainty diagnostic, not a 95% credible interval, conventional 95% statistical significance, or a guarantee of future performance.
- **Uncertainty & CI:** Posterior standard error: $\pm$19.76 SR pts. Shrinkage weight $r = 0.640$. | 95% Credible Interval: [-18.05, 59.43] SR pts (width: 77.47 SR pts). Displayed separately from the 1-SE diagnostic score; reflects a two-sided 95% Bayesian credible region (z = 1.96).
- **Competition Support:** Coverage: BOTH (55 balls in IPL, 29 balls in Senior T20I | Classification: `IPL_QUALIFIED`). Limited cross-competition sample overlap. Note: Dual-tournament qualification indicates sample exposure availability in both competitions, NOT statistical proof of cross-competition skill transferability.
- **Key Limitations:** Moderate sample volume (84 balls; estimation CI width is 77.5 SR pts); Heavily skewed towards IPL; cross-league transferability is not guaranteed.
- **Sensitivity Profile:** Under unpenalized posterior mean, performance is +20.69 SR pts. Model credibility against baseline: 85.2%; against league-wide pressure mean (prior mean $\mu = -34.24 SR pts$): 99.7%. Exceeding league average under pressure compares against degraded match conditions, NOT fellow shortlisted candidates. Exploratory PRI without TCF: 98.1; Experimental PRI with TCF: 94.7.

---

### Rank 3 — Tim David (`POSITIVE_ESTIMATE_UNRESOLVED (HIGH_VOLUME)`)
- **Why Considered:** Ranked #3 in Batting with a conservative diagnostic value of -2.53 SR pts. Two-Dimensional Classification: 'POSITIVE_ESTIMATE_UNRESOLVED (HIGH_VOLUME)' (Evidence Status: `POSITIVE_ESTIMATE_UNRESOLVED`, Volume: `HIGH_VOLUME`, Cohort: `ESTABLISHED_MARGINAL_PERFORMER`). Sample qualification: QUALIFIED (legacy: 'STRONG_EVIDENCE'). Posterior mean is strictly positive, but 1-SE conservative lower bound spans zero/negative (positive estimated performance with unresolved uncertainty; NOT evidence of below-baseline performance).
- **Evidence Volume:** 290 legal pressure deliveries bowled/faced, categorized in 'HIGH_VOLUME' (Volume Tier B).
- **Temporal Stability:** Demonstrated across 33 unique pressure matches and 5 active seasons (Distribution: 2022: 50b, 2023: 24b, 2024: 89b, 2025: 109b, 2026: 18b).
- **Observed vs Expected:** Observed Strike Rate: 190.34 (raw difference of +16.42 SR pts versus context expectation). | Context-adjusted expectation: 173.93 Strike Rate, derived from stratified 12-cell baselines across phase, tournament tier, and innings.
- **Conservative Diagnostic Score:** BAT_CONSERVATIVE = -2.53 SR pts. Represents the 1-SE conservative diagnostic bound (posterior mean minus 1.0 SE (SR points)). Under an approximate normal posterior distribution, a positive one-standard-error lower bound implies posterior probability above zero greater than approximately 84.1%. This is a directional uncertainty diagnostic, not a 95% credible interval, conventional 95% statistical significance, or a guarantee of future performance.
- **Uncertainty & CI:** Posterior standard error: $\pm$12.10 SR pts. Shrinkage weight $r = 0.865$. | 95% Credible Interval: [-14.14, 33.30] SR pts (width: 47.44 SR pts). Displayed separately from the 1-SE diagnostic score; reflects a two-sided 95% Bayesian credible region (z = 1.96).
- **Competition Support:** Coverage: BOTH (198 balls in IPL, 92 balls in Senior T20I | Classification: `DUAL_TOURNAMENT_QUALIFIED`). Supported by substantial sample in both competitions. Note: Dual-tournament qualification indicates sample exposure availability in both competitions, NOT statistical proof of cross-competition skill transferability.
- **Key Limitations:** Robust sample volume and multi-season stability; residual uncertainty bounded by 95% CI.
- **Sensitivity Profile:** Under unpenalized posterior mean, performance is +9.58 SR pts. Model credibility against baseline: 78.6%; against league-wide pressure mean (prior mean $\mu = -34.24 SR pts$): 100.0%. Exceeding league average under pressure compares against degraded match conditions, NOT fellow shortlisted candidates. Exploratory PRI without TCF: 89.6; Experimental PRI with TCF: 95.5.

---

### Rank 4 — Dinesh Karthik (`POSITIVE_ESTIMATE_UNRESOLVED (HIGH_VOLUME)`)
- **Why Considered:** Ranked #4 in Batting with a conservative diagnostic value of -2.67 SR pts. Two-Dimensional Classification: 'POSITIVE_ESTIMATE_UNRESOLVED (HIGH_VOLUME)' (Evidence Status: `POSITIVE_ESTIMATE_UNRESOLVED`, Volume: `HIGH_VOLUME`, Cohort: `ESTABLISHED_MARGINAL_PERFORMER`). Sample qualification: QUALIFIED (legacy: 'STRONG_EVIDENCE'). Posterior mean is strictly positive, but 1-SE conservative lower bound spans zero/negative (positive estimated performance with unresolved uncertainty; NOT evidence of below-baseline performance).
- **Evidence Volume:** 260 legal pressure deliveries bowled/faced, categorized in 'HIGH_VOLUME' (Volume Tier B).
- **Temporal Stability:** Demonstrated across 30 unique pressure matches and 3 active seasons (Distribution: 2022: 122b, 2022/23: 6b, 2023: 35b, 2024: 97b).
- **Observed vs Expected:** Observed Strike Rate: 194.62 (raw difference of +15.79 SR pts versus context expectation). | Context-adjusted expectation: 178.83 Strike Rate, derived from stratified 12-cell baselines across phase, tournament tier, and innings.
- **Conservative Diagnostic Score:** BAT_CONSERVATIVE = -2.67 SR pts. Represents the 1-SE conservative diagnostic bound (posterior mean minus 1.0 SE (SR points)). Under an approximate normal posterior distribution, a positive one-standard-error lower bound implies posterior probability above zero greater than approximately 84.1%. This is a directional uncertainty diagnostic, not a 95% credible interval, conventional 95% statistical significance, or a guarantee of future performance.
- **Uncertainty & CI:** Posterior standard error: $\pm$11.91 SR pts. Shrinkage weight $r = 0.869$. | 95% Credible Interval: [-14.10, 32.59] SR pts (width: 46.69 SR pts). Displayed separately from the 1-SE diagnostic score; reflects a two-sided 95% Bayesian credible region (z = 1.96).
- **Competition Support:** Coverage: BOTH (194 balls in IPL, 66 balls in Senior T20I | Classification: `DUAL_TOURNAMENT_QUALIFIED`). Supported by substantial sample in both competitions. Note: Dual-tournament qualification indicates sample exposure availability in both competitions, NOT statistical proof of cross-competition skill transferability.
- **Key Limitations:** Robust sample volume and multi-season stability; residual uncertainty bounded by 95% CI.
- **Sensitivity Profile:** Under unpenalized posterior mean, performance is +9.24 SR pts. Model credibility against baseline: 78.1%; against league-wide pressure mean (prior mean $\mu = -34.24 SR pts$): 100.0%. Exceeding league average under pressure compares against degraded match conditions, NOT fellow shortlisted candidates. Exploratory PRI without TCF: 92.6; Experimental PRI with TCF: 86.9.

---

### Rank 5 — Ashutosh Sharma (`POSITIVE_ESTIMATE_UNRESOLVED (HIGH_VOLUME)`)
- **Why Considered:** Ranked #5 in Batting with a conservative diagnostic value of -3.63 SR pts. Two-Dimensional Classification: 'POSITIVE_ESTIMATE_UNRESOLVED (HIGH_VOLUME)' (Evidence Status: `POSITIVE_ESTIMATE_UNRESOLVED`, Volume: `HIGH_VOLUME`, Cohort: `ESTABLISHED_MARGINAL_PERFORMER`). Sample qualification: QUALIFIED (legacy: 'STRONG_EVIDENCE'). Posterior mean is strictly positive, but 1-SE conservative lower bound spans zero/negative (positive estimated performance with unresolved uncertainty; NOT evidence of below-baseline performance).
- **Evidence Volume:** 191 legal pressure deliveries bowled/faced, categorized in 'HIGH_VOLUME' (Volume Tier B).
- **Temporal Stability:** Demonstrated across 20 unique pressure matches and 3 active seasons (Distribution: 2024: 73b, 2025: 69b, 2026: 49b).
- **Observed vs Expected:** Observed Strike Rate: 197.38 (raw difference of +19.99 SR pts versus context expectation). | Context-adjusted expectation: 177.39 Strike Rate, derived from stratified 12-cell baselines across phase, tournament tier, and innings.
- **Conservative Diagnostic Score:** BAT_CONSERVATIVE = -3.63 SR pts. Represents the 1-SE conservative diagnostic bound (posterior mean minus 1.0 SE (SR points)). Under an approximate normal posterior distribution, a positive one-standard-error lower bound implies posterior probability above zero greater than approximately 84.1%. This is a directional uncertainty diagnostic, not a 95% credible interval, conventional 95% statistical significance, or a guarantee of future performance.
- **Uncertainty & CI:** Posterior standard error: $\pm$13.93 SR pts. Shrinkage weight $r = 0.821$. | 95% Credible Interval: [-16.99, 37.59] SR pts (width: 54.59 SR pts). Displayed separately from the 1-SE diagnostic score; reflects a two-sided 95% Bayesian credible region (z = 1.96).
- **Competition Support:** Coverage: IPL_ONLY (191 balls in IPL, 0 balls in Senior T20I | Classification: `IPL_QUALIFIED`). Limited cross-competition sample overlap. Note: Dual-tournament qualification indicates sample exposure availability in both competitions, NOT statistical proof of cross-competition skill transferability.
- **Key Limitations:** Heavily skewed towards IPL; cross-league transferability is not guaranteed.
- **Sensitivity Profile:** Under unpenalized posterior mean, performance is +10.30 SR pts. Model credibility against baseline: 77.0%; against league-wide pressure mean (prior mean $\mu = -34.24 SR pts$): 99.9%. Exceeding league average under pressure compares against degraded match conditions, NOT fellow shortlisted candidates. Exploratory PRI without TCF: 91.3; Experimental PRI with TCF: 87.5.

---

### Rank 6 — Marcus Stoinis (`POSITIVE_ESTIMATE_UNRESOLVED (HIGH_VOLUME)`)
- **Why Considered:** Ranked #6 in Batting with a conservative diagnostic value of -5.77 SR pts. Two-Dimensional Classification: 'POSITIVE_ESTIMATE_UNRESOLVED (HIGH_VOLUME)' (Evidence Status: `POSITIVE_ESTIMATE_UNRESOLVED`, Volume: `HIGH_VOLUME`, Cohort: `ESTABLISHED_MARGINAL_PERFORMER`). Sample qualification: QUALIFIED (legacy: 'STRONG_EVIDENCE'). Posterior mean is strictly positive, but 1-SE conservative lower bound spans zero/negative (positive estimated performance with unresolved uncertainty; NOT evidence of below-baseline performance).
- **Evidence Volume:** 220 legal pressure deliveries bowled/faced, categorized in 'HIGH_VOLUME' (Volume Tier B).
- **Temporal Stability:** Demonstrated across 32 unique pressure matches and 5 active seasons (Distribution: 2022: 61b, 2023: 28b, 2024: 12b, 2025: 71b, 2026: 48b).
- **Observed vs Expected:** Observed Strike Rate: 181.36 (raw difference of +14.54 SR pts versus context expectation). | Context-adjusted expectation: 166.83 Strike Rate, derived from stratified 12-cell baselines across phase, tournament tier, and innings.
- **Conservative Diagnostic Score:** BAT_CONSERVATIVE = -5.77 SR pts. Represents the 1-SE conservative diagnostic bound (posterior mean minus 1.0 SE (SR points)). Under an approximate normal posterior distribution, a positive one-standard-error lower bound implies posterior probability above zero greater than approximately 84.1%. This is a directional uncertainty diagnostic, not a 95% credible interval, conventional 95% statistical significance, or a guarantee of future performance.
- **Uncertainty & CI:** Posterior standard error: $\pm$12.87 SR pts. Shrinkage weight $r = 0.847$. | 95% Credible Interval: [-18.13, 32.31] SR pts (width: 50.44 SR pts). Displayed separately from the 1-SE diagnostic score; reflects a two-sided 95% Bayesian credible region (z = 1.96).
- **Competition Support:** Coverage: BOTH (156 balls in IPL, 64 balls in Senior T20I | Classification: `DUAL_TOURNAMENT_QUALIFIED`). Supported by substantial sample in both competitions. Note: Dual-tournament qualification indicates sample exposure availability in both competitions, NOT statistical proof of cross-competition skill transferability.
- **Key Limitations:** Robust sample volume and multi-season stability; residual uncertainty bounded by 95% CI.
- **Sensitivity Profile:** Under unpenalized posterior mean, performance is +7.09 SR pts. Model credibility against baseline: 70.9%; against league-wide pressure mean (prior mean $\mu = -34.24 SR pts$): 99.9%. Exceeding league average under pressure compares against degraded match conditions, NOT fellow shortlisted candidates. Exploratory PRI without TCF: 90.0; Experimental PRI with TCF: 78.8.

---

### Rank 7 — Naman Dhir (`POSITIVE_ESTIMATE_UNRESOLVED (MEDIUM_VOLUME)`)
- **Why Considered:** Ranked #7 in Batting with a conservative diagnostic value of -6.91 SR pts. Two-Dimensional Classification: 'POSITIVE_ESTIMATE_UNRESOLVED (MEDIUM_VOLUME)' (Evidence Status: `POSITIVE_ESTIMATE_UNRESOLVED`, Volume: `MEDIUM_VOLUME`, Cohort: `ESTABLISHED_MARGINAL_PERFORMER`). Sample qualification: QUALIFIED (legacy: 'STRONG_EVIDENCE'). Posterior mean is strictly positive, but 1-SE conservative lower bound spans zero/negative (positive estimated performance with unresolved uncertainty; NOT evidence of below-baseline performance).
- **Evidence Volume:** 145 legal pressure deliveries bowled/faced, categorized in 'MEDIUM_VOLUME' (Volume Tier B).
- **Temporal Stability:** Demonstrated across 18 unique pressure matches and 3 active seasons (Distribution: 2024: 28b, 2025: 68b, 2026: 49b).
- **Observed vs Expected:** Observed Strike Rate: 193.79 (raw difference of +18.72 SR pts versus context expectation). | Context-adjusted expectation: 175.07 Strike Rate, derived from stratified 12-cell baselines across phase, tournament tier, and innings.
- **Conservative Diagnostic Score:** BAT_CONSERVATIVE = -6.91 SR pts. Represents the 1-SE conservative diagnostic bound (posterior mean minus 1.0 SE (SR points)). Under an approximate normal posterior distribution, a positive one-standard-error lower bound implies posterior probability above zero greater than approximately 84.1%. This is a directional uncertainty diagnostic, not a 95% credible interval, conventional 95% statistical significance, or a guarantee of future performance.
- **Uncertainty & CI:** Posterior standard error: $\pm$14.86 SR pts. Shrinkage weight $r = 0.797$. | 95% Credible Interval: [-21.17, 37.07] SR pts (width: 58.23 SR pts). Displayed separately from the 1-SE diagnostic score; reflects a two-sided 95% Bayesian credible region (z = 1.96).
- **Competition Support:** Coverage: BOTH (118 balls in IPL, 27 balls in Senior T20I | Classification: `IPL_QUALIFIED`). Limited cross-competition sample overlap. Note: Dual-tournament qualification indicates sample exposure availability in both competitions, NOT statistical proof of cross-competition skill transferability.
- **Key Limitations:** Heavily skewed towards IPL; cross-league transferability is not guaranteed.
- **Sensitivity Profile:** Under unpenalized posterior mean, performance is +7.95 SR pts. Model credibility against baseline: 70.4%; against league-wide pressure mean (prior mean $\mu = -34.24 SR pts$): 99.8%. Exceeding league average under pressure compares against degraded match conditions, NOT fellow shortlisted candidates. Exploratory PRI without TCF: 92.6; Experimental PRI with TCF: 91.9.

---

### Rank 8 — Rinku Singh (`POSITIVE_ESTIMATE_UNRESOLVED (HIGH_VOLUME)`)
- **Why Considered:** Ranked #8 in Batting with a conservative diagnostic value of -7.02 SR pts. Two-Dimensional Classification: 'POSITIVE_ESTIMATE_UNRESOLVED (HIGH_VOLUME)' (Evidence Status: `POSITIVE_ESTIMATE_UNRESOLVED`, Volume: `HIGH_VOLUME`, Cohort: `ESTABLISHED_MARGINAL_PERFORMER`). Sample qualification: QUALIFIED (legacy: 'STRONG_EVIDENCE'). Posterior mean is strictly positive, but 1-SE conservative lower bound spans zero/negative (positive estimated performance with unresolved uncertainty; NOT evidence of below-baseline performance).
- **Evidence Volume:** 363 legal pressure deliveries bowled/faced, categorized in 'HIGH_VOLUME' (Volume Tier B).
- **Temporal Stability:** Demonstrated across 48 unique pressure matches and 5 active seasons (Distribution: 2022: 50b, 2023: 140b, 2024: 57b, 2025: 51b, 2026: 65b).
- **Observed vs Expected:** Observed Strike Rate: 181.27 (raw difference of +7.57 SR pts versus context expectation). | Context-adjusted expectation: 173.70 Strike Rate, derived from stratified 12-cell baselines across phase, tournament tier, and innings.
- **Conservative Diagnostic Score:** BAT_CONSERVATIVE = -7.02 SR pts. Represents the 1-SE conservative diagnostic bound (posterior mean minus 1.0 SE (SR points)). Under an approximate normal posterior distribution, a positive one-standard-error lower bound implies posterior probability above zero greater than approximately 84.1%. This is a directional uncertainty diagnostic, not a 95% credible interval, conventional 95% statistical significance, or a guarantee of future performance.
- **Uncertainty & CI:** Posterior standard error: $\pm$10.41 SR pts. Shrinkage weight $r = 0.900$. | 95% Credible Interval: [-17.01, 23.79] SR pts (width: 40.80 SR pts). Displayed separately from the 1-SE diagnostic score; reflects a two-sided 95% Bayesian credible region (z = 1.96).
- **Competition Support:** Coverage: BOTH (280 balls in IPL, 83 balls in Senior T20I | Classification: `DUAL_TOURNAMENT_QUALIFIED`). Supported by substantial sample in both competitions. Note: Dual-tournament qualification indicates sample exposure availability in both competitions, NOT statistical proof of cross-competition skill transferability.
- **Key Limitations:** Robust sample volume and multi-season stability; residual uncertainty bounded by 95% CI.
- **Sensitivity Profile:** Under unpenalized posterior mean, performance is +3.39 SR pts. Model credibility against baseline: 62.8%; against league-wide pressure mean (prior mean $\mu = -34.24 SR pts$): 100.0%. Exceeding league average under pressure compares against degraded match conditions, NOT fellow shortlisted candidates. Exploratory PRI without TCF: 87.9; Experimental PRI with TCF: 93.4.

---

### Rank 9 — Tristan Stubbs (`POSITIVE_ESTIMATE_UNRESOLVED (HIGH_VOLUME)`)
- **Why Considered:** Ranked #9 in Batting with a conservative diagnostic value of -8.17 SR pts. Two-Dimensional Classification: 'POSITIVE_ESTIMATE_UNRESOLVED (HIGH_VOLUME)' (Evidence Status: `POSITIVE_ESTIMATE_UNRESOLVED`, Volume: `HIGH_VOLUME`, Cohort: `ESTABLISHED_MARGINAL_PERFORMER`). Sample qualification: QUALIFIED (legacy: 'STRONG_EVIDENCE'). Posterior mean is strictly positive, but 1-SE conservative lower bound spans zero/negative (positive estimated performance with unresolved uncertainty; NOT evidence of below-baseline performance).
- **Evidence Volume:** 266 legal pressure deliveries bowled/faced, categorized in 'HIGH_VOLUME' (Volume Tier B).
- **Temporal Stability:** Demonstrated across 33 unique pressure matches and 5 active seasons (Distribution: 2022: 11b, 2022/23: 1b, 2023: 13b, 2024: 94b, 2025: 71b, 2026: 76b).
- **Observed vs Expected:** Observed Strike Rate: 167.29 (raw difference of +6.55 SR pts versus context expectation). | Context-adjusted expectation: 160.74 Strike Rate, derived from stratified 12-cell baselines across phase, tournament tier, and innings.
- **Conservative Diagnostic Score:** BAT_CONSERVATIVE = -8.17 SR pts. Represents the 1-SE conservative diagnostic bound (posterior mean minus 1.0 SE (SR points)). Under an approximate normal posterior distribution, a positive one-standard-error lower bound implies posterior probability above zero greater than approximately 84.1%. This is a directional uncertainty diagnostic, not a 95% credible interval, conventional 95% statistical significance, or a guarantee of future performance.
- **Uncertainty & CI:** Posterior standard error: $\pm$10.54 SR pts. Shrinkage weight $r = 0.898$. | 95% Credible Interval: [-18.29, 23.03] SR pts (width: 41.32 SR pts). Displayed separately from the 1-SE diagnostic score; reflects a two-sided 95% Bayesian credible region (z = 1.96).
- **Competition Support:** Coverage: BOTH (169 balls in IPL, 97 balls in Senior T20I | Classification: `DUAL_TOURNAMENT_QUALIFIED`). Supported by substantial sample in both competitions. Note: Dual-tournament qualification indicates sample exposure availability in both competitions, NOT statistical proof of cross-competition skill transferability.
- **Key Limitations:** Robust sample volume and multi-season stability; residual uncertainty bounded by 95% CI.
- **Sensitivity Profile:** Under unpenalized posterior mean, performance is +2.37 SR pts. Model credibility against baseline: 58.9%; against league-wide pressure mean (prior mean $\mu = -34.24 SR pts$): 100.0%. Exceeding league average under pressure compares against degraded match conditions, NOT fellow shortlisted candidates. Exploratory PRI without TCF: 89.4; Experimental PRI with TCF: 86.5.

---

### Rank 10 — Sherfane Rutherford (`POSITIVE_ESTIMATE_UNRESOLVED (HIGH_VOLUME)`)
- **Why Considered:** Ranked #10 in Batting with a conservative diagnostic value of -8.18 SR pts. Two-Dimensional Classification: 'POSITIVE_ESTIMATE_UNRESOLVED (HIGH_VOLUME)' (Evidence Status: `POSITIVE_ESTIMATE_UNRESOLVED`, Volume: `HIGH_VOLUME`, Cohort: `ESTABLISHED_MARGINAL_PERFORMER`). Sample qualification: QUALIFIED (legacy: 'STRONG_EVIDENCE'). Posterior mean is strictly positive, but 1-SE conservative lower bound spans zero/negative (positive estimated performance with unresolved uncertainty; NOT evidence of below-baseline performance).
- **Evidence Volume:** 151 legal pressure deliveries bowled/faced, categorized in 'HIGH_VOLUME' (Volume Tier B).
- **Temporal Stability:** Demonstrated across 21 unique pressure matches and 5 active seasons (Distribution: 2022: 16b, 2023: 8b, 2024: 43b, 2025: 25b, 2026: 59b).
- **Observed vs Expected:** Observed Strike Rate: 178.15 (raw difference of +17.93 SR pts versus context expectation). | Context-adjusted expectation: 160.21 Strike Rate, derived from stratified 12-cell baselines across phase, tournament tier, and innings.
- **Conservative Diagnostic Score:** BAT_CONSERVATIVE = -8.18 SR pts. Represents the 1-SE conservative diagnostic bound (posterior mean minus 1.0 SE (SR points)). Under an approximate normal posterior distribution, a positive one-standard-error lower bound implies posterior probability above zero greater than approximately 84.1%. This is a directional uncertainty diagnostic, not a 95% credible interval, conventional 95% statistical significance, or a guarantee of future performance.
- **Uncertainty & CI:** Posterior standard error: $\pm$15.12 SR pts. Shrinkage weight $r = 0.789$. | 95% Credible Interval: [-22.69, 36.57] SR pts (width: 59.26 SR pts). Displayed separately from the 1-SE diagnostic score; reflects a two-sided 95% Bayesian credible region (z = 1.96).
- **Competition Support:** Coverage: BOTH (40 balls in IPL, 111 balls in Senior T20I | Classification: `DUAL_TOURNAMENT_QUALIFIED`). Supported by substantial sample in both competitions. Note: Dual-tournament qualification indicates sample exposure availability in both competitions, NOT statistical proof of cross-competition skill transferability.
- **Key Limitations:** Robust sample volume and multi-season stability; residual uncertainty bounded by 95% CI.
- **Sensitivity Profile:** Under unpenalized posterior mean, performance is +6.94 SR pts. Model credibility against baseline: 67.7%; against league-wide pressure mean (prior mean $\mu = -34.24 SR pts$): 99.7%. Exceeding league average under pressure compares against degraded match conditions, NOT fellow shortlisted candidates. Exploratory PRI without TCF: 89.2; Experimental PRI with TCF: 78.1.

---

---


### Part B: Bowling Candidate Evidence Cards (Rank 1 to 10)

### Rank 1 — Jasprit Bumrah (`POSITIVE_ESTIMATE_UNRESOLVED (HIGH_VOLUME)`)
- **Why Considered:** Ranked #1 in Bowling with a conservative diagnostic value of -0.16 RPO. Two-Dimensional Classification: 'POSITIVE_ESTIMATE_UNRESOLVED (HIGH_VOLUME)' (Evidence Status: `POSITIVE_ESTIMATE_UNRESOLVED`, Volume: `HIGH_VOLUME`, Cohort: `OUTPERFORMING_BASELINE_ESTIMATE`). Sample qualification: QUALIFIED (legacy: 'STRONG_EVIDENCE'). Posterior mean is strictly positive, but 1-SE conservative lower bound spans zero/negative (positive estimated performance with unresolved uncertainty; NOT evidence of below-baseline performance).
- **Evidence Volume:** 521 legal pressure deliveries bowled/faced, categorized in 'HIGH_VOLUME' (Volume Tier B).
- **Temporal Stability:** Demonstrated across 60 unique pressure matches and 5 active seasons (Distribution: 2022: 116b, 2023: 12b, 2024: 101b, 2025: 155b, 2026: 137b).
- **Observed vs Expected:** Observed Economy Rate: 7.37 (raw difference of -0.76 RPO versus context expectation). | Context-adjusted expectation: 8.13 Economy Rate, derived from stratified 12-cell baselines across phase, tournament tier, and innings.
- **Conservative Diagnostic Score:** BOWL_CONSERVATIVE = -0.16 RPO. Represents the 1-SE conservative diagnostic bound (negative posterior economy diff minus 1.0 SE (runs saved/over)). Under an approximate normal posterior distribution, a positive one-standard-error lower bound implies posterior probability above zero greater than approximately 84.1%. This is a directional uncertainty diagnostic, not a 95% credible interval, conventional 95% statistical significance, or a guarantee of future performance.
- **Uncertainty & CI:** Posterior standard error: $\pm$0.36 RPO. Shrinkage weight $r = 0.783$. | 95% Credible Interval: [-0.90, 0.50] RPO (width: 1.41 RPO). Displayed separately from the 1-SE diagnostic score; reflects a two-sided 95% Bayesian credible region (z = 1.96).
- **Competition Support:** Coverage: BOTH (388 balls in IPL, 133 balls in Senior T20I | Classification: `DUAL_TOURNAMENT_QUALIFIED`). Supported by substantial sample in both competitions. Note: Dual-tournament qualification indicates sample exposure availability in both competitions, NOT statistical proof of cross-competition skill transferability.
- **Key Limitations:** Robust sample volume and multi-season stability; residual uncertainty bounded by 95% CI.
- **Sensitivity Profile:** Under unpenalized posterior mean, performance is -0.20 RPO. Model credibility against baseline: 71.1%; against league-wide pressure mean (prior mean $\mu = +1.82 RPO$): 100.0%. Exceeding league average under pressure compares against degraded match conditions, NOT fellow shortlisted candidates. Exploratory PRI without TCF: 100.0; Experimental PRI with TCF: 100.0.

---

### Rank 2 — Sunil Narine (`INCONCLUSIVE_EVIDENCE (HIGH_VOLUME)`)
- **Why Considered:** Ranked #2 in Bowling with a conservative diagnostic value of -0.94 RPO. Two-Dimensional Classification: 'INCONCLUSIVE_EVIDENCE (HIGH_VOLUME)' (Evidence Status: `INCONCLUSIVE_EVIDENCE`, Volume: `HIGH_VOLUME`, Cohort: `INCONCLUSIVE`). Sample qualification: QUALIFIED (legacy: 'STRONG_EVIDENCE'). Point estimate is non-positive, but 1-SE uncertainty interval crosses ordinary baseline.
- **Evidence Volume:** 153 legal pressure deliveries bowled/faced, categorized in 'HIGH_VOLUME' (Volume Tier B).
- **Temporal Stability:** Demonstrated across 24 unique pressure matches and 5 active seasons (Distribution: 2022: 48b, 2023: 37b, 2024: 18b, 2025: 12b, 2026: 38b).
- **Observed vs Expected:** Observed Economy Rate: 7.14 (raw difference of -1.08 RPO versus context expectation). | Context-adjusted expectation: 8.21 Economy Rate, derived from stratified 12-cell baselines across phase, tournament tier, and innings.
- **Conservative Diagnostic Score:** BOWL_CONSERVATIVE = -0.94 RPO. Represents the 1-SE conservative diagnostic bound (negative posterior economy diff minus 1.0 SE (runs saved/over)). Under an approximate normal posterior distribution, a positive one-standard-error lower bound implies posterior probability above zero greater than approximately 84.1%. This is a directional uncertainty diagnostic, not a 95% credible interval, conventional 95% statistical significance, or a guarantee of future performance.
- **Uncertainty & CI:** Posterior standard error: $\pm$0.55 RPO. Shrinkage weight $r = 0.494$. | 95% Credible Interval: [-0.68, 1.47] RPO (width: 2.15 RPO). Displayed separately from the 1-SE diagnostic score; reflects a two-sided 95% Bayesian credible region (z = 1.96).
- **Competition Support:** Coverage: IPL_ONLY (153 balls in IPL, 0 balls in Senior T20I | Classification: `IPL_QUALIFIED`). Limited cross-competition sample overlap. Note: Dual-tournament qualification indicates sample exposure availability in both competitions, NOT statistical proof of cross-competition skill transferability.
- **Key Limitations:** Heavily skewed towards IPL; cross-league transferability is not guaranteed.
- **Sensitivity Profile:** Under unpenalized posterior mean, performance is +0.39 RPO. Model credibility against baseline: 23.8%; against league-wide pressure mean (prior mean $\mu = +1.82 RPO$): 99.5%. Exceeding league average under pressure compares against degraded match conditions, NOT fellow shortlisted candidates. Exploratory PRI without TCF: 92.0; Experimental PRI with TCF: 95.7.

---

### Rank 3 — Maheesh Theekshana (`BELOW_BASELINE_EVIDENCE (HIGH_VOLUME)`)
- **Why Considered:** Ranked #3 in Bowling with a conservative diagnostic value of -0.96 RPO. Two-Dimensional Classification: 'BELOW_BASELINE_EVIDENCE (HIGH_VOLUME)' (Evidence Status: `BELOW_BASELINE_EVIDENCE`, Volume: `HIGH_VOLUME`, Cohort: `PEER_BEATING_ESTABLISHED`). Sample qualification: QUALIFIED (legacy: 'STRONG_EVIDENCE'). Under an approximate normal posterior distribution, a negative one-standard-error upper bound implies posterior probability below baseline greater than approximately 84.1%. This is a directional uncertainty diagnostic, not conventional 95% statistical significance or proof of underperformance.
- **Evidence Volume:** 421 legal pressure deliveries bowled/faced, categorized in 'HIGH_VOLUME' (Volume Tier B).
- **Temporal Stability:** Demonstrated across 58 unique pressure matches and 5 active seasons (Distribution: 2022: 100b, 2023: 60b, 2024: 82b, 2024/25: 18b, 2025: 120b, 2026: 41b).
- **Observed vs Expected:** Observed Economy Rate: 8.08 (raw difference of +0.05 RPO versus context expectation). | Context-adjusted expectation: 8.03 Economy Rate, derived from stratified 12-cell baselines across phase, tournament tier, and innings.
- **Conservative Diagnostic Score:** BOWL_CONSERVATIVE = -0.96 RPO. Represents the 1-SE conservative diagnostic bound (negative posterior economy diff minus 1.0 SE (runs saved/over)). Under an approximate normal posterior distribution, a positive one-standard-error lower bound implies posterior probability above zero greater than approximately 84.1%. This is a directional uncertainty diagnostic, not a 95% credible interval, conventional 95% statistical significance, or a guarantee of future performance.
- **Uncertainty & CI:** Posterior standard error: $\pm$0.41 RPO. Shrinkage weight $r = 0.717$. | 95% Credible Interval: [-0.25, 1.35] RPO (width: 1.61 RPO). Displayed separately from the 1-SE diagnostic score; reflects a two-sided 95% Bayesian credible region (z = 1.96).
- **Competition Support:** Coverage: BOTH (179 balls in IPL, 242 balls in Senior T20I | Classification: `DUAL_TOURNAMENT_QUALIFIED`). Supported by substantial sample in both competitions. Note: Dual-tournament qualification indicates sample exposure availability in both competitions, NOT statistical proof of cross-competition skill transferability.
- **Key Limitations:** Robust sample volume and multi-season stability; residual uncertainty bounded by 95% CI.
- **Sensitivity Profile:** Under unpenalized posterior mean, performance is +0.55 RPO. Model credibility against baseline: 9.0%; against league-wide pressure mean (prior mean $\mu = +1.82 RPO$): 99.9%. Exceeding league average under pressure compares against degraded match conditions, NOT fellow shortlisted candidates. Exploratory PRI without TCF: 80.1; Experimental PRI with TCF: 96.2.

---

### Rank 4 — Matheesha Pathirana (`BELOW_BASELINE_EVIDENCE (HIGH_VOLUME)`)
- **Why Considered:** Ranked #4 in Bowling with a conservative diagnostic value of -1.05 RPO. Two-Dimensional Classification: 'BELOW_BASELINE_EVIDENCE (HIGH_VOLUME)' (Evidence Status: `BELOW_BASELINE_EVIDENCE`, Volume: `HIGH_VOLUME`, Cohort: `PEER_BEATING_ESTABLISHED`). Sample qualification: QUALIFIED (legacy: 'STRONG_EVIDENCE'). Under an approximate normal posterior distribution, a negative one-standard-error upper bound implies posterior probability below baseline greater than approximately 84.1%. This is a directional uncertainty diagnostic, not conventional 95% statistical significance or proof of underperformance.
- **Evidence Volume:** 440 legal pressure deliveries bowled/faced, categorized in 'HIGH_VOLUME' (Volume Tier B).
- **Temporal Stability:** Demonstrated across 44 unique pressure matches and 5 active seasons (Distribution: 2022: 17b, 2023: 140b, 2024: 122b, 2024/25: 6b, 2025: 137b, 2026: 18b).
- **Observed vs Expected:** Observed Economy Rate: 8.29 (raw difference of +0.16 RPO versus context expectation). | Context-adjusted expectation: 8.14 Economy Rate, derived from stratified 12-cell baselines across phase, tournament tier, and innings.
- **Conservative Diagnostic Score:** BOWL_CONSERVATIVE = -1.05 RPO. Represents the 1-SE conservative diagnostic bound (negative posterior economy diff minus 1.0 SE (runs saved/over)). Under an approximate normal posterior distribution, a positive one-standard-error lower bound implies posterior probability above zero greater than approximately 84.1%. This is a directional uncertainty diagnostic, not a 95% credible interval, conventional 95% statistical significance, or a guarantee of future performance.
- **Uncertainty & CI:** Posterior standard error: $\pm$0.41 RPO. Shrinkage weight $r = 0.713$. | 95% Credible Interval: [-0.18, 1.44] RPO (width: 1.62 RPO). Displayed separately from the 1-SE diagnostic score; reflects a two-sided 95% Bayesian credible region (z = 1.96).
- **Competition Support:** Coverage: BOTH (336 balls in IPL, 104 balls in Senior T20I | Classification: `DUAL_TOURNAMENT_QUALIFIED`). Supported by substantial sample in both competitions. Note: Dual-tournament qualification indicates sample exposure availability in both competitions, NOT statistical proof of cross-competition skill transferability.
- **Key Limitations:** Robust sample volume and multi-season stability; residual uncertainty bounded by 95% CI.
- **Sensitivity Profile:** Under unpenalized posterior mean, performance is +0.63 RPO. Model credibility against baseline: 6.2%; against league-wide pressure mean (prior mean $\mu = +1.82 RPO$): 99.8%. Exceeding league average under pressure compares against degraded match conditions, NOT fellow shortlisted candidates. Exploratory PRI without TCF: 85.2; Experimental PRI with TCF: 97.2.

---

### Rank 5 — Shaheen Afridi (`BELOW_BASELINE_EVIDENCE (HIGH_VOLUME)`)
- **Why Considered:** Ranked #5 in Bowling with a conservative diagnostic value of -1.43 RPO. Two-Dimensional Classification: 'BELOW_BASELINE_EVIDENCE (HIGH_VOLUME)' (Evidence Status: `BELOW_BASELINE_EVIDENCE`, Volume: `HIGH_VOLUME`, Cohort: `PEER_BEATING_ESTABLISHED`). Sample qualification: QUALIFIED (legacy: 'STRONG_EVIDENCE'). Under an approximate normal posterior distribution, a negative one-standard-error upper bound implies posterior probability below baseline greater than approximately 84.1%. This is a directional uncertainty diagnostic, not conventional 95% statistical significance or proof of underperformance.
- **Evidence Volume:** 191 legal pressure deliveries bowled/faced, categorized in 'HIGH_VOLUME' (Volume Tier B).
- **Temporal Stability:** Demonstrated across 31 unique pressure matches and 4 active seasons (Distribution: 2023: 30b, 2024: 60b, 2025: 95b, 2026: 6b).
- **Observed vs Expected:** Observed Economy Rate: 8.04 (raw difference of +0.18 RPO versus context expectation). | Context-adjusted expectation: 7.87 Economy Rate, derived from stratified 12-cell baselines across phase, tournament tier, and innings.
- **Conservative Diagnostic Score:** BOWL_CONSERVATIVE = -1.43 RPO. Represents the 1-SE conservative diagnostic bound (negative posterior economy diff minus 1.0 SE (runs saved/over)). Under an approximate normal posterior distribution, a positive one-standard-error lower bound implies posterior probability above zero greater than approximately 84.1%. This is a directional uncertainty diagnostic, not a 95% credible interval, conventional 95% statistical significance, or a guarantee of future performance.
- **Uncertainty & CI:** Posterior standard error: $\pm$0.52 RPO. Shrinkage weight $r = 0.552$. | 95% Credible Interval: [-0.10, 1.92] RPO (width: 2.02 RPO). Displayed separately from the 1-SE diagnostic score; reflects a two-sided 95% Bayesian credible region (z = 1.96).
- **Competition Support:** Coverage: T20I_ONLY (0 balls in IPL, 191 balls in Senior T20I | Classification: `T20I_QUALIFIED`). Limited cross-competition sample overlap. Note: Dual-tournament qualification indicates sample exposure availability in both competitions, NOT statistical proof of cross-competition skill transferability.
- **Key Limitations:** Heavily skewed towards T20I; cross-league transferability is not guaranteed.
- **Sensitivity Profile:** Under unpenalized posterior mean, performance is +0.91 RPO. Model credibility against baseline: 3.8%; against league-wide pressure mean (prior mean $\mu = +1.82 RPO$): 96.1%. Exceeding league average under pressure compares against degraded match conditions, NOT fellow shortlisted candidates. Exploratory PRI without TCF: 76.2; Experimental PRI with TCF: 88.9.

---

### Rank 6 — Mustafizur Rahman (`BELOW_BASELINE_EVIDENCE (HIGH_VOLUME)`)
- **Why Considered:** Ranked #6 in Bowling with a conservative diagnostic value of -1.47 RPO. Two-Dimensional Classification: 'BELOW_BASELINE_EVIDENCE (HIGH_VOLUME)' (Evidence Status: `BELOW_BASELINE_EVIDENCE`, Volume: `HIGH_VOLUME`, Cohort: `PEER_BEATING_ESTABLISHED`). Sample qualification: QUALIFIED (legacy: 'STRONG_EVIDENCE'). Under an approximate normal posterior distribution, a negative one-standard-error upper bound implies posterior probability below baseline greater than approximately 84.1%. This is a directional uncertainty diagnostic, not conventional 95% statistical significance or proof of underperformance.
- **Evidence Volume:** 578 legal pressure deliveries bowled/faced, categorized in 'HIGH_VOLUME' (Volume Tier B).
- **Temporal Stability:** Demonstrated across 61 unique pressure matches and 5 active seasons (Distribution: 2022: 126b, 2022/23: 18b, 2023: 84b, 2024: 140b, 2025: 192b, 2026: 18b).
- **Observed vs Expected:** Observed Economy Rate: 8.93 (raw difference of +0.86 RPO versus context expectation). | Context-adjusted expectation: 8.07 Economy Rate, derived from stratified 12-cell baselines across phase, tournament tier, and innings.
- **Conservative Diagnostic Score:** BOWL_CONSERVATIVE = -1.47 RPO. Represents the 1-SE conservative diagnostic bound (negative posterior economy diff minus 1.0 SE (runs saved/over)). Under an approximate normal posterior distribution, a positive one-standard-error lower bound implies posterior probability above zero greater than approximately 84.1%. This is a directional uncertainty diagnostic, not a 95% credible interval, conventional 95% statistical significance, or a guarantee of future performance.
- **Uncertainty & CI:** Posterior standard error: $\pm$0.38 RPO. Shrinkage weight $r = 0.756$. | 95% Credible Interval: [0.35, 1.84] RPO (width: 1.49 RPO). Displayed separately from the 1-SE diagnostic score; reflects a two-sided 95% Bayesian credible region (z = 1.96).
- **Competition Support:** Coverage: BOTH (216 balls in IPL, 362 balls in Senior T20I | Classification: `DUAL_TOURNAMENT_QUALIFIED`). Supported by substantial sample in both competitions. Note: Dual-tournament qualification indicates sample exposure availability in both competitions, NOT statistical proof of cross-competition skill transferability.
- **Key Limitations:** Robust sample volume and multi-season stability; residual uncertainty bounded by 95% CI.
- **Sensitivity Profile:** Under unpenalized posterior mean, performance is +1.09 RPO. Model credibility against baseline: 0.2%; against league-wide pressure mean (prior mean $\mu = +1.82 RPO$): 97.2%. Exceeding league average under pressure compares against degraded match conditions, NOT fellow shortlisted candidates. Exploratory PRI without TCF: 69.2; Experimental PRI with TCF: 74.0.

---

### Rank 7 — Richard Ngarava (`BELOW_BASELINE_EVIDENCE (HIGH_VOLUME)`)
- **Why Considered:** Ranked #7 in Bowling with a conservative diagnostic value of -1.56 RPO. Two-Dimensional Classification: 'BELOW_BASELINE_EVIDENCE (HIGH_VOLUME)' (Evidence Status: `BELOW_BASELINE_EVIDENCE`, Volume: `HIGH_VOLUME`, Cohort: `PEER_BEATING_ESTABLISHED`). Sample qualification: QUALIFIED (legacy: 'STRONG_EVIDENCE'). Under an approximate normal posterior distribution, a negative one-standard-error upper bound implies posterior probability below baseline greater than approximately 84.1%. This is a directional uncertainty diagnostic, not conventional 95% statistical significance or proof of underperformance.
- **Evidence Volume:** 287 legal pressure deliveries bowled/faced, categorized in 'HIGH_VOLUME' (Volume Tier B).
- **Temporal Stability:** Demonstrated across 34 unique pressure matches and 5 active seasons (Distribution: 2022: 15b, 2023: 24b, 2023/24: 20b, 2024: 114b, 2025: 84b, 2026: 30b).
- **Observed vs Expected:** Observed Economy Rate: 8.51 (raw difference of +0.69 RPO versus context expectation). | Context-adjusted expectation: 7.82 Economy Rate, derived from stratified 12-cell baselines across phase, tournament tier, and innings.
- **Conservative Diagnostic Score:** BOWL_CONSERVATIVE = -1.56 RPO. Represents the 1-SE conservative diagnostic bound (negative posterior economy diff minus 1.0 SE (runs saved/over)). Under an approximate normal posterior distribution, a positive one-standard-error lower bound implies posterior probability above zero greater than approximately 84.1%. This is a directional uncertainty diagnostic, not a 95% credible interval, conventional 95% statistical significance, or a guarantee of future performance.
- **Uncertainty & CI:** Posterior standard error: $\pm$0.46 RPO. Shrinkage weight $r = 0.638$. | 95% Credible Interval: [0.19, 2.01] RPO (width: 1.82 RPO). Displayed separately from the 1-SE diagnostic score; reflects a two-sided 95% Bayesian credible region (z = 1.96).
- **Competition Support:** Coverage: T20I_ONLY (0 balls in IPL, 287 balls in Senior T20I | Classification: `T20I_QUALIFIED`). Limited cross-competition sample overlap. Note: Dual-tournament qualification indicates sample exposure availability in both competitions, NOT statistical proof of cross-competition skill transferability.
- **Key Limitations:** Heavily skewed towards T20I; cross-league transferability is not guaranteed.
- **Sensitivity Profile:** Under unpenalized posterior mean, performance is +1.10 RPO. Model credibility against baseline: 0.9%; against league-wide pressure mean (prior mean $\mu = +1.82 RPO$): 94.1%. Exceeding league average under pressure compares against degraded match conditions, NOT fellow shortlisted candidates. Exploratory PRI without TCF: 66.1; Experimental PRI with TCF: 70.1.

---

### Rank 8 — Lungi Ngidi (`BELOW_BASELINE_EVIDENCE (HIGH_VOLUME)`)
- **Why Considered:** Ranked #8 in Bowling with a conservative diagnostic value of -1.65 RPO. Two-Dimensional Classification: 'BELOW_BASELINE_EVIDENCE (HIGH_VOLUME)' (Evidence Status: `BELOW_BASELINE_EVIDENCE`, Volume: `HIGH_VOLUME`, Cohort: `PEER_BEATING_ESTABLISHED`). Sample qualification: QUALIFIED (legacy: 'STRONG_EVIDENCE'). Under an approximate normal posterior distribution, a negative one-standard-error upper bound implies posterior probability below baseline greater than approximately 84.1%. This is a directional uncertainty diagnostic, not conventional 95% statistical significance or proof of underperformance.
- **Evidence Volume:** 222 legal pressure deliveries bowled/faced, categorized in 'HIGH_VOLUME' (Volume Tier B).
- **Temporal Stability:** Demonstrated across 26 unique pressure matches and 5 active seasons (Distribution: 2022: 30b, 2022/23: 12b, 2023: 12b, 2024: 30b, 2025: 34b, 2026: 104b).
- **Observed vs Expected:** Observed Economy Rate: 8.57 (raw difference of +0.51 RPO versus context expectation). | Context-adjusted expectation: 8.06 Economy Rate, derived from stratified 12-cell baselines across phase, tournament tier, and innings.
- **Conservative Diagnostic Score:** BOWL_CONSERVATIVE = -1.65 RPO. Represents the 1-SE conservative diagnostic bound (negative posterior economy diff minus 1.0 SE (runs saved/over)). Under an approximate normal posterior distribution, a positive one-standard-error lower bound implies posterior probability above zero greater than approximately 84.1%. This is a directional uncertainty diagnostic, not a 95% credible interval, conventional 95% statistical significance, or a guarantee of future performance.
- **Uncertainty & CI:** Posterior standard error: $\pm$0.53 RPO. Shrinkage weight $r = 0.532$. | 95% Credible Interval: [0.09, 2.16] RPO (width: 2.07 RPO). Displayed separately from the 1-SE diagnostic score; reflects a two-sided 95% Bayesian credible region (z = 1.96).
- **Competition Support:** Coverage: BOTH (116 balls in IPL, 106 balls in Senior T20I | Classification: `DUAL_TOURNAMENT_QUALIFIED`). Supported by substantial sample in both competitions. Note: Dual-tournament qualification indicates sample exposure availability in both competitions, NOT statistical proof of cross-competition skill transferability.
- **Key Limitations:** Robust sample volume and multi-season stability; residual uncertainty bounded by 95% CI.
- **Sensitivity Profile:** Under unpenalized posterior mean, performance is +1.13 RPO. Model credibility against baseline: 1.6%; against league-wide pressure mean (prior mean $\mu = +1.82 RPO$): 90.7%. Exceeding league average under pressure compares against degraded match conditions, NOT fellow shortlisted candidates. Exploratory PRI without TCF: 74.7; Experimental PRI with TCF: 86.6.

---

### Rank 9 — Ravichandran Ashwin (`BELOW_BASELINE_EVIDENCE (MEDIUM_VOLUME)`)
- **Why Considered:** Ranked #9 in Bowling with a conservative diagnostic value of -1.67 RPO. Two-Dimensional Classification: 'BELOW_BASELINE_EVIDENCE (MEDIUM_VOLUME)' (Evidence Status: `BELOW_BASELINE_EVIDENCE`, Volume: `MEDIUM_VOLUME`, Cohort: `PEER_BEATING_ESTABLISHED`). Sample qualification: QUALIFIED (legacy: 'STRONG_EVIDENCE'). Under an approximate normal posterior distribution, a negative one-standard-error upper bound implies posterior probability below baseline greater than approximately 84.1%. This is a directional uncertainty diagnostic, not conventional 95% statistical significance or proof of underperformance.
- **Evidence Volume:** 147 legal pressure deliveries bowled/faced, categorized in 'MEDIUM_VOLUME' (Volume Tier B).
- **Temporal Stability:** Demonstrated across 21 unique pressure matches and 4 active seasons (Distribution: 2022: 61b, 2023: 36b, 2024: 38b, 2025: 12b).
- **Observed vs Expected:** Observed Economy Rate: 8.45 (raw difference of +0.27 RPO versus context expectation). | Context-adjusted expectation: 8.18 Economy Rate, derived from stratified 12-cell baselines across phase, tournament tier, and innings.
- **Conservative Diagnostic Score:** BOWL_CONSERVATIVE = -1.67 RPO. Represents the 1-SE conservative diagnostic bound (negative posterior economy diff minus 1.0 SE (runs saved/over)). Under an approximate normal posterior distribution, a positive one-standard-error lower bound implies posterior probability above zero greater than approximately 84.1%. This is a directional uncertainty diagnostic, not a 95% credible interval, conventional 95% statistical significance, or a guarantee of future performance.
- **Uncertainty & CI:** Posterior standard error: $\pm$0.57 RPO. Shrinkage weight $r = 0.459$. | 95% Credible Interval: [-0.00, 2.22] RPO (width: 2.22 RPO). Displayed separately from the 1-SE diagnostic score; reflects a two-sided 95% Bayesian credible region (z = 1.96).
- **Competition Support:** Coverage: IPL_DOMINANT (129 balls in IPL, 18 balls in Senior T20I | Classification: `IPL_QUALIFIED`). Limited cross-competition sample overlap. Note: Dual-tournament qualification indicates sample exposure availability in both competitions, NOT statistical proof of cross-competition skill transferability.
- **Key Limitations:** Heavily skewed towards IPL; cross-league transferability is not guaranteed.
- **Sensitivity Profile:** Under unpenalized posterior mean, performance is +1.11 RPO. Model credibility against baseline: 2.5%; against league-wide pressure mean (prior mean $\mu = +1.82 RPO$): 89.6%. Exceeding league average under pressure compares against degraded match conditions, NOT fellow shortlisted candidates. Exploratory PRI without TCF: 62.0; Experimental PRI with TCF: 62.7.

---

### Rank 10 — Hasan Mahmud (`BELOW_BASELINE_EVIDENCE (MEDIUM_VOLUME)`)
- **Why Considered:** Ranked #10 in Bowling with a conservative diagnostic value of -1.69 RPO. Two-Dimensional Classification: 'BELOW_BASELINE_EVIDENCE (MEDIUM_VOLUME)' (Evidence Status: `BELOW_BASELINE_EVIDENCE`, Volume: `MEDIUM_VOLUME`, Cohort: `PEER_BEATING_ESTABLISHED`). Sample qualification: QUALIFIED (legacy: 'STRONG_EVIDENCE'). Under an approximate normal posterior distribution, a negative one-standard-error upper bound implies posterior probability below baseline greater than approximately 84.1%. This is a directional uncertainty diagnostic, not conventional 95% statistical significance or proof of underperformance.
- **Evidence Volume:** 90 legal pressure deliveries bowled/faced, categorized in 'MEDIUM_VOLUME' (Volume Tier B).
- **Temporal Stability:** Demonstrated across 11 unique pressure matches and 4 active seasons (Distribution: 2022: 12b, 2022/23: 18b, 2023: 24b, 2024: 5b, 2025: 31b).
- **Observed vs Expected:** Observed Economy Rate: 7.67 (raw difference of -0.14 RPO versus context expectation). | Context-adjusted expectation: 7.81 Economy Rate, derived from stratified 12-cell baselines across phase, tournament tier, and innings.
- **Conservative Diagnostic Score:** BOWL_CONSERVATIVE = -1.69 RPO. Represents the 1-SE conservative diagnostic bound (negative posterior economy diff minus 1.0 SE (runs saved/over)). Under an approximate normal posterior distribution, a positive one-standard-error lower bound implies posterior probability above zero greater than approximately 84.1%. This is a directional uncertainty diagnostic, not a 95% credible interval, conventional 95% statistical significance, or a guarantee of future performance.
- **Uncertainty & CI:** Posterior standard error: $\pm$0.61 RPO. Shrinkage weight $r = 0.375$. | 95% Credible Interval: [-0.11, 2.28] RPO (width: 2.39 RPO). Displayed separately from the 1-SE diagnostic score; reflects a two-sided 95% Bayesian credible region (z = 1.96).
- **Competition Support:** Coverage: T20I_ONLY (0 balls in IPL, 90 balls in Senior T20I | Classification: `T20I_QUALIFIED`). Limited cross-competition sample overlap. Note: Dual-tournament qualification indicates sample exposure availability in both competitions, NOT statistical proof of cross-competition skill transferability.
- **Key Limitations:** Moderate sample volume (90 balls; estimation CI width is 2.4 RPO); Heavily skewed towards T20I; cross-league transferability is not guaranteed.
- **Sensitivity Profile:** Under unpenalized posterior mean, performance is +1.08 RPO. Model credibility against baseline: 3.7%; against league-wide pressure mean (prior mean $\mu = +1.82 RPO$): 88.7%. Exceeding league average under pressure compares against degraded match conditions, NOT fellow shortlisted candidates. Exploratory PRI without TCF: 78.3; Experimental PRI with TCF: 83.0.

---

---

## 11. STATISTICAL UNCERTAINTY & LIMITATIONS

### 11.1 Chronological Out-of-Sample Validation
In Stage R1-05.2, temporal stability was audited by training ordinary baselines and Bayesian priors strictly on historical data (2022–2024) and predicting out-of-sample pressure performance in 2025–2026:
- **Batting Out-of-Sample Correlation:** Out-of-sample strike rate differential correlated with posterior expectations at $r = 0.584$ (Pearson) and $\rho = 0.562$ (Spearman), with zero data leakage.
- **Bowling Out-of-Sample Correlation:** Out-of-sample economy differential correlated at $r = 0.612$ (Pearson) and $\rho = 0.598$ (Spearman).
- **Shrinkage Gain:** In both disciplines, Empirical Bayes shrinkage reduced out-of-sample root mean squared error (RMSE) by **18.4%** compared to unadjusted raw differentials.

### 11.2 Sensitivity & Jaccard Stability Analysis
Shortlist stability was evaluated across 11 perturbation scenarios:
- **Filtering at $n \ge 60$ Balls:** Top 10 roster overlap is **10 of 10 (100% Jaccard)** for Batting, confirming that the Top 10 batters are robust high-volume performers.
- **Posterior Mean vs. Conservative Bound:** Rank correlation is **0.9843** in Batting and **0.9751** in Bowling. The conservative diagnostic demotes high-variance small-sample flyers without perturbing established veterans.
- **Tournament Context Stability:** Top 10 Jaccard overlap under IPL-only filtering is 1.0000 in Batting and 0.5385 in Bowling, reflecting that Bowling depth relies on global T20I pacers (Shaheen, Ngarava, Hasan Mahmud).

### 11.3 Explicit Analytical Limitations
1. **Death Phase Concentration:** 87.28% of bowling pressure deliveries and 78.95% of batting pressure deliveries occur in overs 16–20. Pressure reliability metrics primarily reflect death-overs execution and should be interpreted alongside phase role requirements.
2. **Poisson Noise in Boundary Events:** Individual boundary events in samples of 30–60 balls carry inherent variance. Conservative lower bounds explicitly account for this by penalizing wide standard errors.
3. **Cross-Competition Transferability:** Only 47 batters and 63 bowlers qualify in both IPL and Senior T20Is with $\ge 30$ balls. While tournament tier is controlled in baseline modeling, invariant skill transferability between international bilaterals and high-octane IPL matches cannot be assumed.

---

## 12. METHODOLOGY & REPRODUCIBILITY NOTES

### 12.1 Execution Pipeline
The entire ROYALS INTELLIGENCE Round 1 analytics pipeline is 100% automated, deterministic, and locally reproducible:

```text
1. Data Loading & QA:
   python round1_pressure/src/01_load_qa.py
   -> Validates 200,999 deliveries, 883 matches, schema integrity, and dismissal credits.

2. Match State Reconstruction:
   python round1_pressure/src/02_reconstruct_match_state.py
   -> Computes over-by-over match state, DLS targets, and required run rates.

3. Pressure Detection:
   python round1_pressure/src/03_detect_pressure.py
   -> Classifies strict and permissive leverage events across 200,999 balls.

4. Baseline Estimation & Empirical Bayes:
   python round1_pressure/src/04_expected_performance.py
   -> Estimates 12-cell stratified baselines and fits empirical priors.

5. Reliability Scoring & PRI Engine:
   python round1_pressure/src/05_player_reliability.py
   -> Calculates posterior means, standard errors, and conservative bounds.

6. Intelligence Profiling & Shortlists:
   python round1_pressure/src/r1_06_player_intelligence.py
   python round1_pressure/src/r1_06_explainability.py
   -> Formats leaderboards, 1-SE uncertainty disclosures, and evidence profiles.
```

### 12.2 Verification Test Suite
The underlying analytical engines are protected by 25 regression test files:
- `backend/tests/`: **61 / 61 tests passing** (FastAPI backend, data models, proprietary data pack security).
- `round1_pressure/tests/`: **196 regression tests** covering data QA, match reconstruction, Bayesian baselines, shrinkage, leaderboard ordering, and population accounting.

---
*Report compiled by ROYALS INTELLIGENCE v4.1 for official submission to Rajasthan Royals SupeRR Selector Season 2 (Round 1).*
