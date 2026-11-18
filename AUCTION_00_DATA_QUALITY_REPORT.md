# ROYALS INTELLIGENCE — AUCTION-00 DATA QUALITY REPORT
## Programmatic Quality Verifications, Anomaly Detection & Issue Register
**Domain:** RR Auction & Retention Intelligence (Stage AUCTION-00)  
**Execution Timestamp:** 2026-11-18T07:27:00+05:30  
**Verification Service:** `backend/app/auction_intelligence/foundation/quality_audit.py`  
**Test Suite:** `backend/tests/auction/test_auction_00_foundation.py` (10/10 Passing)  
**Audit Status:** COMPLETE & VERIFIED

---

## 1. Executive Summary & Verification Metrics

Stage AUCTION-00 executes comprehensive, programmatic data quality checks across all 7 raw data assets in the Rajasthan Royals data pack.

| Dimension | Checked Population | Validated Metric | Anomaly Count | Quality Status |
| :--- | :--- | :--- | :---: | :---: |
| **Delivery Semantics** | 200,999 delivery rows | 192,709 legal / 8,290 extras | 0 | **VERIFIED** |
| **Match Coverage** | 883 match records | 867 with balls / 16 abandoned | 0 | **VERIFIED** |
| **Referential Integrity (BBB)** | 200,999 delivery rows | 100% foreign key match to matches.csv | 0 | **VERIFIED** |
| **Referential Integrity (P11)** | 20,413 team-sheet rows | 100% foreign key match to matches.csv | 0 | **VERIFIED** |
| **Duplicate Entity Audit** | 268 player records | 1 duplicate name (Ravi Bishnoi) | 1 (Reconciled) | **RESOLVED** |
| **Null Discipline Audit** | 268 player records | 32 null bowling styles (29 WK, 3 Bat) | 0 (Domain Valid) | **VALIDATED** |
| **Protected Parquet Hashes** | 4 Parquet files | 100% bitwise SHA-256 match | 0 | **INVARIANT** |

---

## 2. Delivery Count Semantics & Reconciliation

The data pack records 200,999 delivery rows in `ball_by_ball.csv`. Standard cricket analytics require strict differentiation between balls that count against the legal over limit and non-legal deliveries:

```mermaid
pie title Delivery Distribution in ball_by_ball.csv (200,999 Rows)
    "Strict Legal Deliveries (Standard)" : 189167
    "Leg-byes (Legal Deliveries)" : 2748
    "Wides (Non-Legal Deliveries)" : 7714
    "No-balls / Overstep (Non-Legal Deliveries)" : 576
    "Byes (Legal Deliveries)" : 529
    "Other Extras & Penalties (Legal)" : 265
```

### Breakdown of Extras & Legal Ball Count:
1. **Total Deliveries Ingested:** **200,999 rows**.
2. **Non-Legal Deliveries (Extras Balls):** **8,290 balls**
   - `extras_type == 'wide'`: **7,714 rows**
   - `extras_type == 'Overstep'`: **576 rows**
3. **Strict Legal Deliveries:** **192,709 balls** ($200,999 - 8,290 = 192,709$).
   - Deliveries with no extras (`extras_type == NaN`): **189,167 rows**
   - Deliveries with leg-byes (`extras_type == 'legbyes'`): **2,748 rows** (legal ball)
   - Deliveries with byes (`extras_type == 'byes'`): **529 rows** (legal ball)
   - Other legal delivery extras (`extras_type == 'other'`): **264 rows** (legal ball)
   - Penalty runs (`extras_type == 'Penalty'`): **1 row** (legal ball)

*Correction Note:* Any prior reference to "200,999 legal balls" was an informal colloquialism. The mathematical and legal baseline is exactly **192,709 legal deliveries**.

---

## 3. Match Coverage & Abandonment Audit

In `matches.csv`, exactly **883 fixtures** are cataloged:
- **Matches with Delivery Data:** **867 matches** have ball-by-ball delivery sequences in `ball_by_ball.csv`.
- **Abandoned / No-Play Matches:** Exactly **16 matches** have zero deliveries recorded. These represent rain washouts, abandoned group stage matches, or COVID-19 forfeitures.
- *Handling:* Abandoned matches are preserved for match-count auditing but filtered out of delivery-level and over-level metric calculations.

---

## 4. Null Value & Data Completeness Analysis

### 4.1 Bowling Styles in `ipl_players.csv`
- Total Records: 268
- Null `Bowling_Style`: Exactly **32 records**
- Null `Spin_Type`: Exactly **32 records**
- **Discipline Distribution of the 32 Nulls:**
  - `Wicketkeeper-Batter`: **29 players** (e.g., Sanju Samson, Dhruv Jurel, Lhuan-dre Pretorius, Ravi Singh)
  - `Batter`: **3 players** (Aman Rao, and two other specialist batters who do not bowl)
  - `Bowler`: **0 nulls** (100% complete)
  - `All-rounder`: **0 nulls** (100% complete)
- *Conclusion:* These nulls do not represent data corruption; they reflect genuine non-bowling specialist roles. No synthetic imputation is performed.

### 4.2 Sensor Telemetry Completeness in `ball_by_ball.csv`
- `bowl_speed`: Null in 120,405 rows (speed radar was not active or installed in all domestic venues).
- `stroke`: Null in 14,208 rows.
- `delivery_style`: Null in 12,301 rows.
- *Handling:* Telemetry-dependent models apply missingness masks rather than discarding rows.

---

## 5. Formal Data Quality Issues Register

| Issue ID | Dataset | Severity | Description | Affected Rows | Resolution Status | Remediation Action |
| :--- | :--- | :---: | :--- | :---: | :---: | :--- |
| **DQI-001** | `ipl_players.csv` | **INFORMATIONAL** | 32 null bowling styles for specialist batters and keepers. | 32 | **RESOLVED** | Confirmed domain-valid; no imputation needed. |
| **DQI-002** | `ipl_players.csv` | **MEDIUM** | Ravi Bishnoi duplicate row (Row 179 RR vs Row 261 LSG). | 2 | **RESOLVED** | Unified under canonical registry with source pointers preserved. |
| **DQI-003** | `ball_by_ball.csv` | **INFORMATIONAL** | Referential check: match_id FK to matches.csv. | 0 | **VERIFIED** | 100% of deliveries link to valid matches. Zero orphans. |
| **DQI-004** | `playing_eleven.csv`| **INFORMATIONAL** | Referential check: match_id FK to matches.csv. | 0 | **VERIFIED** | 100% of team-sheet rows link to valid matches. Zero orphans. |
| **DQI-005** | `matches.csv` | **LOW** | 16 matches abandoned without a ball bowled. | 16 | **RESOLVED** | Isolated and excluded from ball-level aggregations. |
