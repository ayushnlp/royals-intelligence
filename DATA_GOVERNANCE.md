# ROYALS INTELLIGENCE — DATA GOVERNANCE POLICY & SPECIFICATION
**Platform:** ROYALS INTELLIGENCE v4.1  
**Target:** SupeRR Selector Season 2 — Round 1  
**Authority:** Official Rajasthan Royals Competition Data Pack  
**Classification:** Mandatory Data Quality & Modeling Governance Standard  

---

## 1. Governing Principles & Ethical Boundaries

ROYALS INTELLIGENCE enforces strict data governance protocols to guarantee that every insight, metric, and leaderboard entry is empirically grounded, mathematically defensible, and 100% reproducible.

### Mandatory Directives:
1. **Exclusively Official Source Data:** Analysis operates strictly and exclusively upon the official seven-file dataset supplied by the Rajasthan Royals analytics group in `data/raw/rajasthan_royals/round_1_data_pack/`.
2. **Zero Synthetic or Scraped Contamination:** Absolutely zero external web scraping (e.g. ESPNcricinfo, Cricbuzz), simulated match deliveries, synthetic birth dates, or hypothetical auction bids are introduced into the Round 1 analytical pipelines.
3. **Immutability of Raw Artifacts:** Raw source CSV files are write-protected and immutable. All transformations, state reconstructions, and analytical features are derived deterministically and stored in intermediate Parquet files.
4. **Global Evaluation Scope:** The evaluation population includes **ALL cricketers** in the dataset who meet sample exposure qualification criteria across the 2022–2026 IPL and Senior T20I matches. The evaluation is strictly global and empirical. It is **NOT** restricted to Rajasthan Royals players or uncapped players.
5. **Traceable Lineage & Provenance:** Every metric (e.g. PRI, Conservative Runs Saved, Delta SR) must be traceable back to exact ball-by-ball delivery rows in `ball_by_ball.csv`.

---

## 2. Official Source File Inventory & Cryptographic Baselines

Every file in the official data pack has been profiled, line-counted, and cryptographically fingerprinted using SHA-256:

| File Name | Format | Size on Disk | Record Count | Cryptographic SHA-256 Checksum | Schema Scope |
| :--- | :---: | :---: | :---: | :--- | :--- |
| **`ball_by_ball.csv`** | CSV | 41,071,609 bytes | 200,999 rows | `A3926F49D2C684DCA2A5D2DE535A02C5EE46EA654CA1E79DD31C69E7544E9889` | Deliveries, speeds, dismissals, strokes, pitch coordinates |
| **`matches.csv`** | CSV | 123,864 bytes | 883 rows | `BB100AB84B8B9A15160C1F2315CF675210131A30E779EC5079FD5403DCF56EEF` | Match dates, teams, venues, toss, match outcome |
| **`competitions.csv`** | CSV | 7,624 bytes | 141 rows | `507CEB7189F972D4E4F299DDCFC97F3C3247AF1913F6291106F161FA8353FD9B` | Tournament identifiers (IPL, T20I bilateral, ICC World Cup) |
| **`playing_eleven.csv`** | CSV | 966,287 bytes | 28,381 rows | `7517C73722A28D5D61C808CCF0CBED315A8780586D02E946EB9A7F5DAF011C27` | Match-day playing XIs, impact substitutions, captaincy |
| **`teams.csv`** | CSV | 6,922 bytes | 353 rows | `A65E5922A9B3BF49247B24FC9471782E700EFB31F8DCC5042923238B87C50A5D` | Franchise and national team names and codes |
| **`competition_team_player_mapping.csv`** | CSV | 462,969 bytes | 6,413 rows | `1DED4E42A933618572D6E2C3A521C3257EB1844FAB4456D567D77CBB2D3BBB12` | Player roster registrations and canonical IDs |
| **`venues.csv`** | CSV | Metadata | Verified | Standard | Ground names, cities, geographical references |

---

## 3. Cricket Domain Accounting & Invariant Rules

### 3.1 Delivery Legality & Counting Rules
- **The Categorical Code Trap:** In `ball_by_ball.csv`, the column `extras1_runs` contains categorical codes indicating the extra type:
  - `1`: Overstep No-Ball
  - `2`: Wide
  - `3`: Leg Byes
  - `4`: Byes
  - `5`: Other / Beamers
  - `6`: None (Standard Delivery)
  - `7`: Penalty
  Treating `extras1_runs` as integer run values corrupts run-rate calculations. Runs off the bat are strictly sourced from `runs`.
- **Governed Legal Deliveries (192,709 balls):**
  A delivery is strictly legal if and only if:
  $$\text{extras\_type} \notin \left[\text{"wide"}, \text{"Overstep"}\right]$$
  Illegal deliveries (wides: 6,564; oversteps: 1,726) are re-bowled and do not consume a legal ball from the bowler's over quota.
- **Ambiguous Extras (`other` — 264 records):**
  Detailed over-by-over sequence auditing revealed that in 253 instances, the over proceeded to 6 legal balls excluding `other` (re-bowled beamers). In 11 instances, the innings concluded early. To ensure transparency, the pipeline maintains a dual record: Strict Legal (192,445) and Permissive Legal (192,709).
- **Penalty Delivery (1 record):**
  Match 16753, Innings 2, Over 6, Ball 4. Sequence auditing confirmed exactly 6 balls bowled in the over. Confirmed legal ball consumption.

---

### 3.2 Bowler Wicket Credit Rules
In accordance with MCC Law 32 and T20 standard playing conditions:
- **Bowler Wickets (10,489 wickets):** Strictly limited to dismissals where the bowler is directly credited:
  $$\text{Dismissal Type} \in \left[\text{"bowled"}, \text{"caught"}, \text{"lbw"}, \text{"stumped"}, \text{"hit wicket"}\right]$$
- **Non-Bowler Wickets (971 dismissals):** Strictly excluded from bowling average and strike-rate credit:
  - `RunOut` (959 dismissals)
  - `Retire Out` / `Retired Out` (9 dismissals)
  - `Obstructing the field` (3 dismissals, including normalized legacy spelling `'Obstracting the field'`)

---

### 3.3 Bowler Runs Conceded Accounting
Bowler runs conceded must include off-the-bat runs plus wides, oversteps, and penalty runs conceded by the bowler, while excluding byes and leg-byes:
$$\text{Bowler Runs Conceded} = \text{runs} + \mathbf{1}_{\text{wide}} + \mathbf{1}_{\text{overstep}} + \left(\mathbf{1}_{\text{wide or overstep}} \times \text{extras\_2\_runs}\right)$$
Byes and leg-byes are classified as fielding/wicketkeeping concessions and do not penalize the bowler.

---

### 3.4 Match Count Reconciliation (883 vs 867 Matches)
- `matches.csv` contains exactly **883 matches**.
- `ball_by_ball.csv` contains deliveries from exactly **867 matches**.
- **Reconciliation:** Exactly **16 matches** were abandoned or declared No Result without a single ball bowled (`result == "Match Abandoned"`, e.g. Match IDs 31281, 31284, 31288, 32610, 36210, 40761, 50189).
- These 16 matches are formally accounted for in documentation and excluded from delivery aggregation loops.

---

### 3.5 Radar Release Speed Quality Safeguards
- Radar release velocity is recorded for **123,113 deliveries (61.3% sensor coverage)**.
- **Governed Scaling Rule:** Raw values $\ge 500.0$ represent a 10x sensor multiplier calibration error (e.g. 1456.1 km/h) and are automatically divided by 10 (resulting in 145.61 km/h).
- **Physical Boundary Filter:** Extreme anomalous readings ($< 50.0$ km/h or $> 170.0$ km/h) represent offline or uncalibrated sensors and are filtered out of velocity distributions.

---

## 4. Evaluation Population & Sample Qualification Governance

### 4.1 Global Scope Directives
- **No Squad-Level Biases:** The evaluation evaluates all eligible international and franchise cricketers present in the dataset. Restricting shortlists to Rajasthan Royals players is strictly prohibited.
- **Discipline Segregation:** Batting reliability (Strike Rate differential under pressure) and bowling reliability (Economy / Runs Saved under pressure) are evaluated independently. Universal composite scores are forbidden.

### 4.2 Qualification Thresholds
To prevent small-sample volatility from distorting rankings:
- **Primary Batting Leaderboard:** $\ge 60$ legal pressure deliveries faced (or $\ge 50$ balls across $\ge 10$ matches).
- **Primary Bowling Leaderboard:** $\ge 60$ legal pressure deliveries bowled (or $\ge 50$ balls across $\ge 10$ matches).
- Candidates with fewer deliveries are categorized as `UNQUALIFIED_HIGH_HAZARD` or `EXPLORATORY_PROSPECT` and barred from Top 10 consideration.

---

## 5. Audit Trail & Checkpoint Immutability

1. **Accepted Production Checkpoint:** `6005022` (`feat(r1-06.2.3): final data-count reconciliation and statistical wording correction`).
2. **Deterministic Reproducibility:** Every leaderboard, report, and API response can be deterministically reproduced from `round1_pressure/src/` with zero random seed drift.
3. **Sealed Rankings:** The Top 10 Batters and Top 10 Bowlers Under Pressure are locked and cannot be altered without documented mathematical justification and explicit stakeholder approval.
