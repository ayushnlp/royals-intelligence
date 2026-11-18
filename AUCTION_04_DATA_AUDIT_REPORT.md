# ROYALS INTELLIGENCE — AUCTION-04 DATA AUDIT REPORT
## Historical Performance Dataset Coverage & Canonical Identity Integrity Audit

**Document Version:** 1.0.0  
**Phase:** RR Auction & Retention Intelligence Expansion  
**Stage:** `AUCTION-04` — Historical Performance & Competition Normalization  
**Git Baseline Branch:** `main` | **HEAD:** `0f24302c61e3d4c070d0e669fc152830c9b2c4e1`  
**Execution Timestamp:** 2026-11-17T00:26:00+05:30  
**Status:** COMPREHENSIVE DATA AUDIT COMPLETE — 100% CANONICAL JOIN VERIFIED

---

## 1. Executive Summary & Audit Mandate

Before modifying data-processing pipelines or computing performance normalizations, **AUCTION-04** mandates an independent audit of all available raw match and delivery records in `data/raw/rajasthan_royals/round_1_data_pack/` to establish exact data coverage boundaries, canonical join integrity, and data quality constraints.

---

## 2. Macro Dataset Inventory & Structure

The underlying historical performance corpus comprises seven core datasets:

$$\begin{array}{|l|r|r|l|}
\hline
\textbf{Raw File Name} & \textbf{Total Rows} & \textbf{Columns} & \textbf{Analytical Domain / Primary Keys} \\
\hline
\texttt{ball\_by\_ball.csv} & \mathbf{200,999} & 33 & \text{Delivery-level event stream: } (\texttt{match\_id, innings, overid, over\_ball\_num}) \\
\texttt{matches.csv} & \mathbf{883} & 22 & \text{Match metadata, date, venue, result: } (\texttt{match\_id}) \\
\texttt{competitions.csv} & \mathbf{141} & 4 & \text{Tournament metadata, season, format: } (\texttt{comp\_id}) \\
\texttt{playing\_eleven.csv} & \mathbf{28,381} & 9 & \text{Team sheets, batting order, played status: } (\texttt{match\_id, player\_id}) \\
\texttt{competition\_team\_player\_mapping.csv} & \mathbf{6,413} & 6 & \text{Squad registrations: } (\texttt{comp\_id, team\_id, player\_id}) \\
\texttt{teams.csv} & \mathbf{353} & 3 & \text{Team names and competition mappings: } (\texttt{comp\_id, team\_id}) \\
\texttt{ipl\_players.csv} & \mathbf{268} & 7 & \text{Historical reference roster (reconciled in AUCTION-03)} \\
\hline
\end{array}$$

---

## 3. Competition Coverage & Format Distribution

Across the 883 matches, the dataset is stratified into three distinct competition tiers:

$$\begin{array}{|l|r|r|r|l|}
\hline
\textbf{Competition Tier} & \textbf{Competitions} & \textbf{Matches} & \textbf{Total Deliveries} & \textbf{Seasons \& Tournaments Included} \\
\hline
\textbf{1. Indian Premier League (IPL)} & \mathbf{5} & \mathbf{371} & \mathbf{87,687} & \begin{array}{l} \text{IPL 2022 (74), IPL 2023 (74), IPL 2024 (74),} \\ \text{IPL 2025 (75), IPL 2026 (74).} \end{array} \\
\hline
\textbf{2. International T20 (T20I)} & \mathbf{134} & \mathbf{482} & \mathbf{106,327} & \begin{array}{l} \text{Senior Bilateral T20I Series \& Continental} \\ \text{T20I Tournaments (2022–2026).} \end{array} \\
\hline
\textbf{3. Emerging / Tier-2 T20} & \mathbf{2} & \mathbf{30} & \mathbf{6,985} & \begin{array}{l} \text{Men's T20 Emerging Teams Asia Cup 2024 (15),} \\ \text{Asia Cup Rising Stars 2025 (15).} \end{array} \\
\hline
\textbf{Total Audited Performance Universe} & \mathbf{141} & \mathbf{883} & \mathbf{200,999} & \textbf{Complete Delivery Coverage Verified} \\
\hline
\end{array}$$

### Delivery Breakdown Semantics:
- **Total Delivery Records:** **200,999**
- **Non-Legal Delivery Records:** **8,290** (7,714 `wide` + 576 `Overstep`)
- **Legal Delivery Records:** **192,709** ($200,999 - 8,290 = 192,709$)
  - IPL Legal Balls: **83,878**
  - T20I Legal Balls: **102,097**
  - Emerging T20 Legal Balls: **6,734**

---

## 4. Canonical Player Identity Join Verification

A core architectural vulnerability in data integration is player identity mismatch between delivery records and canonical registries.

### 4.1 Join Audit Results:
- **Total Unique Strikers in `ball_by_ball.csv`:** **888 players**
- **Total Unique Bowlers in `ball_by_ball.csv`:** **647 players**
- **Combined Active Delivery Players:** **958 unique players**
- **Canonical Registry Join Rate:** **100.0% (958 out of 958 active players match canonical IDs in `canonical_player_registry.parquet`).**
- **Unmapped or Orphan Delivery IDs:** **0 (Zero).**

---

## 5. Coverage Limitations & Data Gaps Identified

1. **Absence of Domestic State Leagues (Ranji / VHT / SMAT) in `ball_by_ball.csv`:**
   - The delivery event stream covers IPL (2022–2026), international T20Is, and ACC Emerging/Rising Stars T20 tournaments.
   - Domestic state tournaments (e.g. Ranji Trophy red-ball, Vijay Hazare 50-over, and standalone SMAT domestic delivery logs) are not provided at the ball-by-ball level in the Round 1 data pack.
   - *Governance Treatment:* Domestic uncapped players who have limited IPL/T20I exposure are evaluated strictly within the available delivery records, with empirical Bayesian shrinkage applied to prevent sample-size distortions.
2. **Missing Ball Speed & Stroke Labels:**
   - The fields `bowl_speed` and `stroke` in `ball_by_ball.csv` have missing values across certain international venues where radar tracking was unavailable.
   - *Governance Treatment:* The core normalization methodology relies on deterministic score, ball, extra, dismissal, and phase attributes, avoiding reliance on incomplete radar fields.
3. **Format Purity:**
   - All 883 matches are strictly 20-over T20/T20I format fixtures. There is zero contamination from First-Class, Test, or 50-over matches within `ball_by_ball.csv`.
