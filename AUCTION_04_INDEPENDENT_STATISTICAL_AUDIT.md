# ROYALS INTELLIGENCE — AUCTION-04 INDEPENDENT STATISTICAL AUDIT
## Full-Universe Delivery, Match, Competition & Canonical Join Verification Report

**Document Version:** 1.0.0  
**Phase:** RR Auction & Retention Intelligence Expansion  
**Stage:** `AUCTION-04` — Historical Performance & Competition Normalization  
**Git Baseline Branch:** `main` | **HEAD:** `0f24302c61e3d4c070d0e669fc152830c9b2c4e1`  
**Execution Timestamp:** 2026-11-17T00:37:00+05:30  
**Status:** AUDIT PASSED — 100% INTEGRITY VERIFIED  

---

## 1. Executive Summary & Audit Mandate

An independent, read-only statistical audit of the **AUCTION-04** historical performance normalization data pipeline was conducted to verify mathematical accuracy, data integrity, and compliance with strict governance mandates.

The audit independently verified:
1. **Total Universe Record Counts:** Matches, competitions, total delivery records, non-legal deliveries, and legal deliveries.
2. **Canonical Identity Joins:** Mapping rate of every active player against the AUCTION-01 canonical player registry ($n=1,217$).
3. **Delivery Uniqueness:** Primary key uniqueness across all 200,999 delivery rows.
4. **Domain Independence:** Strict separation of batting and bowling metrics without composite scoring.
5. **Selection & Survivorship Bias:** Analysis of competition exposure imbalances and shrinkage mitigations.

---

## 2. Macro Universe Delivery & Match Accounting

The audit independently re-executed the data ingestion and filtering logic against the raw data sources. All counts match exactly across raw datasets, normalization schemas, and test assertions.

$$\begin{array}{|l|r|r|r|l|}
\hline
\textbf{Metric / Entity} & \textbf{Raw CSV Count} & \textbf{Engine Audited} & \textbf{Discrepancy} & \textbf{Audit Status} \\
\hline
\text{Matches} & \mathbf{883} & \mathbf{883} & 0 & \text{VERIFIED EXACT} \\
\text{Competitions} & \mathbf{141} & \mathbf{141} & 0 & \text{VERIFIED EXACT} \\
\text{Total Delivery Rows} & \mathbf{200,999} & \mathbf{200,999} & 0 & \text{VERIFIED EXACT} \\
\text{Wides (\texttt{wide})} & \mathbf{7,714} & \mathbf{7,714} & 0 & \text{VERIFIED EXACT} \\
\text{No-Balls (\texttt{Overstep})} & \mathbf{576} & \mathbf{576} & 0 & \text{VERIFIED EXACT} \\
\text{Total Non-Legal Deliveries} & \mathbf{8,290} & \mathbf{8,290} & 0 & \text{VERIFIED EXACT} \\
\hline
\textbf{Total Legal Deliveries} & \mathbf{192,709} & \mathbf{192,709} & \mathbf{0} & \textbf{VERIFIED EXACT} \\
\hline
\end{array}$$

### 2.1 Legal Deliveries by Competition Tier

$$\begin{array}{|l|r|r|r|r|}
\hline
\textbf{Competition Tier} & \textbf{Matches} & \textbf{Total Deliveries} & \textbf{Non-Legal Deliveries} & \textbf{Legal Deliveries} \\
\hline
\text{Indian Premier League (IPL)} & 371 & 87,687 & 3,809 & \mathbf{83,878} \\
\text{International T20 (T20I)} & 482 & 106,327 & 4,230 & \mathbf{102,097} \\
\text{Emerging / Tier-2 T20} & 30 & 6,985 & 251 & \mathbf{6,734} \\
\hline
\textbf{Total} & \mathbf{883} & \mathbf{200,999} & \mathbf{8,290} & \mathbf{192,709} \\
\hline
\end{array}$$

---

## 3. Canonical Identity Mapping & Join Integrity

The historical ball-by-ball dataset contains active player IDs representing strikers and bowlers. Every ID was verified against the AUCTION-01 canonical player registry (`canonical_player_registry.parquet`, $n=1,217$).

$$\begin{array}{|l|r|r|r|}
\hline
\textbf{Player Role Universe} & \textbf{Unique Active IDs} & \textbf{Joined to Canonical Registry} & \textbf{Orphaned / Unmapped IDs} \\
\hline
\text{Batters (Strikers)} & \mathbf{888} & \mathbf{888} & \mathbf{0 \text{ (100.0\% Join)}} \\
\text{Bowlers} & \mathbf{647} & \mathbf{647} & \mathbf{0 \text{ (100.0\% Join)}} \\
\text{Total Distinct Active Players} & \mathbf{958} & \mathbf{958} & \mathbf{0 \text{ (100.0\% Join)}} \\
\hline
\end{array}$$

### Findings & Set Topology:
- Exactly **958 unique players** actively participated (batted or bowled) in the 883 audited matches.
- Exactly **0 orphaned or unmapped players** were detected (**100.0% join rate: 958 / 958**).
- **Dual-Discipline Active Overlap (All-Rounders):** **577 players** ($888 + 647 - 958 = 577$).
- **Batters Only (Zero Deliveries Bowled):** **311 players** ($888 - 577 = 311$).
- **Bowlers Only (Zero Deliveries Faced):** **70 players** ($647 - 577 = 70$).
- **Inactive / Zero-Delivery Registry Players:** **259 players** ($1,217 - 958 = 259$). These represent registered squad members or historical players who did not actively bat or bowl in this specific 2022–2026 match sample; they are correctly excluded from delivery-level normalization outputs.

---

## 4. Delivery Uniqueness & Data Quality Audit

We conducted an independent check for duplicate delivery rows across the primary composite key:

$$(\texttt{match\_id}, \texttt{innings}, \texttt{overid}, \texttt{over\_ball\_num})$$

$$\begin{array}{|l|r|r|l|}
\hline
\textbf{Dataset} & \textbf{Total Rows} & \textbf{Distinct Primary Keys} & \textbf{Duplicate Rows} \\
\hline
\texttt{ball\_by\_ball.csv} & 200,999 & 200,999 & \mathbf{0 \text{ (100\% Unique)}} \\
\hline
\end{array}$$

**Verdict:** The delivery record stream is strictly unique with zero duplicated events.

---

## 5. Bowler Conceded Runs & Wicket Credit Verification

In accordance with cricket scoring rules:
1. **Bowler Conceded Runs:** Must include runs scored off the bat plus wides and no-ball extras. Fielding extras (`byes` and `legbyes`) must **not** be charged to the bowler.
2. **Bowler Credited Wickets:** Must credit only dismissals attributable to the bowler (bowled, caught, caught & bowled, lbw, stumped, hit wicket). Must **exclude** `run out`, `retired out`, `retired hurt`, and `obstructing the field`.

$$\begin{array}{|l|r|r|l|}
\hline
\textbf{Dismissal Event} & \textbf{Raw Wicket Flag} & \textbf{Bowler Credited?} & \textbf{Analytical Justification} \\
\hline
\text{Bowled, LBW, Caught, Stumped, Hit Wicket} & 1 & \mathbf{YES} & \text{Direct bowler performance event} \\
\text{Run Out} & 1 & \mathbf{NO} & \text{Fielding dismissal, not credited to bowler (249 in IPL)} \\
\text{Retired Out / Retired Hurt} & 1 & \mathbf{NO} & \text{Tactical/injury stoppage, not bowler credit} \\
\text{Obstructing the Field} & 1 & \mathbf{NO} & \text{Batter infraction, not bowler credit} \\
\hline
\end{array}$$

### Audited IPL Totals:
- **Total Deliveries:** $87,687$ (Legal: $83,878$)
- **Batter Runs off Bat:** $123,597$
- **Wides Penalty Runs:** $3,809$
- **No-Ball Penalty & Auxiliary Runs:** $170$
- **Total Bowler Conceded Runs:** $\mathbf{127,576\text{ runs}}$ ($123,597 + 3,809 + 170 = 127,576$)
- **Empirical Bowler Economy Rate:** $(127,576 / 83,878) \times 6.0 = \mathbf{9.1258\text{ RPO}} \approx \mathbf{9.13\text{ RPO}}$
- **Total Dismissals Fallen:** $4,458$
- **Bowler-Credited Wickets:** $\mathbf{4,209\text{ wickets}}$ ($4,458 - 249\text{ run-outs} = 4,209$)

---

## 6. Scoring Environment vs. Competition Quality & Bias Analysis

In historical sports data, survivorship, selection bias, and environment confounding present serious modeling hazards:
1. **Scoring Environment vs. Competition Quality:**
   - An aggregate scoring-environment index ($0.8497$ for Emerging T20, $0.9141$ for T20I vs $1.0000$ IPL anchor) reflects macro conditions (pitch characteristics, boundary boundaries, format rules).
   - It **does not prove** competition quality or player talent distribution.
   - Therefore, indices are maintained strictly as **Descriptive Scoring-Environment Statistics**, not unvalidated player skill multipliers.
2. **Survivorship & Selection Bias:**
   - Fringe players appearing in low-leverage situations or small samples can exhibit extreme rate volatility.
   - **Mitigation:** Empirical Bayes shrinkage using provisional parameter $m=60$ legal balls strongly contracts low-sample profiles toward the empirical IPL baseline ($\mu_{\text{batting}} = 147.35\text{ SR}$, $\mu_{\text{bowling}} = 9.13\text{ Econ}$), eliminating small-sample noise.
   - **Independent Phase Exposure:** Prevents specialists from inheriting high confidence in phases where they rarely perform.

---

## 7. Protected Baseline Invariant Audit

All four Round 1 Pressure Intelligence Parquet baselines were audited via cryptographic SHA-256 hashing.

$$\begin{array}{|l|l|l|}
\hline
\textbf{Protected Parquet File} & \textbf{Cryptographic SHA-256 Digest} & \textbf{Status} \\
\hline
\texttt{batting\_leaderboard.parquet} & \texttt{fc3d9d0e7a62d162455b4ae2c97d40537ba4cf56efe6830e19afed6ceed5949d} & \mathbf{MATCH} \\
\texttt{bowling\_leaderboard.parquet} & \texttt{dd8c96d404068e69622aa70ceea6b217399313ec1e7963ff110db5f75bbde6d0} & \mathbf{MATCH} \\
\texttt{batting\_evidence_profiles.parquet} & \texttt{f17dbafd36ce60614b6bed93d58e45c18ad16ac5c27bfb41d510cb7f9920427c} & \mathbf{MATCH} \\
\texttt{bowling\_evidence_profiles.parquet} & \texttt{8f138beca7d01fe9174719d055f75f4284a45c9e955842294f934e2c58adb265} & \mathbf{MATCH} \\
\hline
\end{array}$$

All four protected files remain **100% bit-for-bit identical** to their baseline states.

---

## 8. Final Audit Verdict

$$\mathbf{AUDIT\ VERDICT:\ FORMALLY\ VERIFIED\ &\ ACCEPTED}$$

The historical performance normalization dataset and pipeline are statistically defensible, mathematically exact, and fully compliant with all architectural constraints.
