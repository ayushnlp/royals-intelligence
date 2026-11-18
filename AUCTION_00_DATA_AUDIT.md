# ROYALS INTELLIGENCE — AUCTION-00 DATA AUDIT
## Comprehensive Dataset Audit & Discrepancy Reconciliation Report (Final Corrected Version)
**Domain:** RR Auction & Retention Intelligence (Stage AUCTION-00)  
**Execution Timestamp:** 2026-11-16T22:30:00+05:30  
**Repository State:** `main` @ `0f24302c61e3d4c070d0e669fc152830c9b2c4e1`  
**Primary Target File:** `data/raw/rajasthan_royals/round_1_data_pack/ipl_players.csv`  
**Protected Assets:** All 4 Protected Parquet Artifacts Verified Pristine (SHA-256 Hashes Intact)

---

## 1. Executive Summary & Purpose

Stage **AUCTION-00** performs a forensic data audit of the reference dataset `ipl_players.csv` and cross-examines it against the official Round 1 competition data pack (`ball_by_ball.csv`, `matches.csv`, `competitions.csv`, `competition_team_player_mapping.csv`, `playing_eleven.csv`, `teams.csv`).

The purpose of this audit is to:
1. Reconcile delivery count semantics: distinguish **200,999 total deliveries** from **192,709 legal deliveries** across **883 matches (867 with ball-by-ball delivery logs, 16 abandoned/no-play matches)**.
2. Reconcile the exact player and category counts for Rajasthan Royals and all 10 franchises in `ipl_players.csv`.
3. Correct previous preliminary classification discrepancies.
4. Investigate duplicate records (Ravi Bishnoi) and anomalous franchise associations.
5. Establish the true semantic nature of the supplied player CSV and decouple roster association from verified current squad membership.
6. Prevent the unverified or naive use of this reference dataset as an authoritative IPL 2027 retention list.

---

## 2. Delivery Count Semantics & Reconciliation

A critical audit distinction is maintained across all analytical pipelines:
* **Total Deliveries Ingested:** Exactly **200,999 total delivery rows** in `ball_by_ball.csv`.
* **Non-Legal Delivery Records:** Exactly **8,290 non-legal delivery records (7,714 wides + 576 no-balls)** comprising:
  - `extras_type == "wide"`: **7,714 records**
  - `extras_type == "Overstep"`: **576 records**
* **Strict Legal Deliveries:** Exactly **192,709 legal deliveries** ($200,999 - 8,290 = 192,709$).
* **Match Coverage:** Exactly **883 total matches** in `matches.csv`, of which **867 matches have ball-by-ball delivery records** (16 fixtures were abandoned without a ball bowled).

*Audit Correction:* Any prior phrasing referencing "200,999 legal deliveries" was a drafting semantic error. The mathematically verified baseline is **200,999 total deliveries and 192,709 legal deliveries**.

---

## 3. Forensic Profile of `ipl_players.csv`

### 3.1 File Attributes & Physical Verification
* **File Path:** `data/raw/rajasthan_royals/round_1_data_pack/ipl_players.csv`
* **File Size:** 23,561 bytes
* **Total Rows (excluding header):** 268 records
* **Total Columns:** 7 columns
* **Integrity Status:** Byte-for-byte preserved; read-only inspection.

### 3.2 Schema & Missing Value Inventory
| Column Name | Data Type | Non-Null Count | Null Count | Semantic Description |
| :--- | :--- | :--- | :--- | :--- |
| `Team` | `string` | 268 | 0 | Franchise identifier across 10 IPL teams |
| `Name` | `string` | 268 | 0 | Full player name (267 unique strings) |
| `Age` | `int64` | 268 | 0 | Integer player age (Min: 15, Median: 28, Max: 45) |
| `Role` | `string` | 268 | 0 | Playing role (`Bowler`, `All-rounder`, `Batter`, `Wicketkeeper-Batter`) |
| `Batting_Style` | `string` | 268 | 0 | Handedness (`Right-handed`, `Left-handed`) |
| `Bowling_Style` | `string` | 236 | 32 | Delivery arm and pace/spin description (Null for pure specialist batters/keepers) |
| `Spin_Type` | `string` | 236 | 32 | Spin category or `None (Pace)` (Null for pure specialist batters/keepers) |

*Audit Note on Null Values:* Exactly 32 records contain `NaN` in `Bowling_Style` and `Spin_Type`. Forensic cross-referencing reveals that these 32 records correspond exclusively to players classified under `Role == "Batter"` (15 players) or `Role == "Wicketkeeper-Batter"` (17 players) who do not bowl in competitive professional cricket.

### 3.3 League-Wide Franchise Roster Breakdown
The 268 player records are distributed across all 10 active IPL franchises as follows:

| Franchise (`Team`) | Total Rows | Bowler | All-rounder | Batter | Wicketkeeper-Batter |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Chennai Super Kings** | 29 | 11 | 10 | 4 | 4 |
| **Mumbai Indians** | 29 | 12 | 10 | 4 | 3 |
| **Kolkata Knight Riders** | 28 | 11 | 9 | 5 | 3 |
| **Rajasthan Royals** | **27** | **12** | **6** | **5** | **4** |
| **Sunrisers Hyderabad** | 27 | 10 | 7 | 5 | 5 |
| **Royal Challengers Bengaluru** | 26 | 10 | 8 | 4 | 4 |
| **Delhi Capitals** | 26 | 9 | 10 | 4 | 3 |
| **Lucknow Super Giants** | 26 | 11 | 7 | 5 | 3 |
| **Punjab Kings** | 25 | 9 | 8 | 5 | 3 |
| **Gujarat Titans** | 25 | 9 | 9 | 4 | 3 |
| **TOTAL** | **268** | **104** | **84** | **45** | **35** |

---

## 4. Rajasthan Royals Squad Audit & Reconciliation

### 4.1 Reconciled Category Breakdown (Exact Rows: 27)
Previous preliminary documentation cited 27 total RR players but approximated the role sub-counts as 8 Batters/Keepers, 5 All-rounders, and 14 Bowlers. This audit establishes the **exact, verified row-by-row categorization**:

* **Specialist Bowlers:** Exactly **12 rows** (44.4%)
* **All-rounders:** Exactly **6 rows** (22.2%)
* **Specialist Batters:** Exactly **5 rows** (18.5%)
* **Wicketkeeper-Batters:** Exactly **4 rows** (14.8%)
* **Combined Batting / Wicketkeeper Pool:** Exactly **9 rows** (33.3%)
* **Total RR Records in CSV:** **27 rows** (100.0%)

### 4.2 Granular Roster Inventory for Rajasthan Royals
| Row Index | Player Name | Age | Role | Batting Style | Bowling Style | Spin Type |
| :---: | :--- | :---: | :--- | :--- | :--- | :--- |
| 163 | **Riyan Parag** | 25 | All-rounder | Right-handed | Right-arm leg break | Leg Break |
| 164 | **Yashasvi Jaiswal** | 24 | Batter | Left-handed | Right-arm leg break | Leg Break |
| 165 | **Vaibhav Sooryavanshi** | 15 | Batter | Left-handed | Left-arm orthodox | Left-Arm Orthodox |
| 166 | **Dhruv Jurel** | 25 | Wicketkeeper-Batter | Right-handed | `NaN` | `NaN` |
| 167 | **Shimron Hetmyer** | 29 | Batter | Left-handed | Right-arm leg break | Leg Break |
| 168 | **Donovan Ferreira** | 28 | Wicketkeeper-Batter | Right-handed | Right-arm off break | Off Break |
| 169 | **Lhuan-dre Pretorius** | 20 | Wicketkeeper-Batter | Left-handed | `NaN` | `NaN` |
| 170 | **Shubham Dubey** | 32 | Batter | Left-handed | Right-arm off break | Off Break |
| 171 | **Aman Rao** | 22 | Batter | Right-handed | `NaN` | `NaN` |
| 172 | **Ravi Singh** | 24 | Wicketkeeper-Batter | Left-handed | `NaN` | `NaN` |
| 173 | **Ravindra Jadeja** | 37 | All-rounder | Left-handed | Left-arm orthodox | Left-Arm Orthodox |
| 174 | **Sam Curran** | 28 | All-rounder | Left-handed | Left-arm medium-fast | None (Pace) |
| 175 | **Dasun Shanaka** | 35 | All-rounder | Right-handed | Right-arm medium | None (Pace) |
| 176 | **Yudhvir Singh** | 29 | All-rounder | Right-handed | Right-arm fast-medium | None (Pace) |
| 177 | **Emanjot Singh Chahal** | 22 | All-rounder | Right-handed | Right-arm leg break | Leg Break |
| 178 | **Jofra Archer** | 31 | Bowler | Right-handed | Right-arm fast | None (Pace) |
| 179 | **Ravi Bishnoi** | 26 | Bowler | Right-handed | Right-arm leg break | Leg Break |
| 180 | **Tushar Deshpande** | 31 | Bowler | Left-handed | Right-arm medium | None (Pace) |
| 181 | **Nandre Burger** | 31 | Bowler | Left-handed | Left-arm fast-medium | None (Pace) |
| 182 | **Sandeep Sharma** | 33 | Bowler | Right-handed | Right-arm medium | None (Pace) |
| 183 | **Adam Milne** | 34 | Bowler | Right-handed | Right-arm fast | None (Pace) |
| 184 | **Kwena Maphaka** | 20 | Bowler | Left-handed | Left-arm fast-medium | None (Pace) |
| 185 | **Kuldeep Sen** | 30 | Bowler | Right-handed | Right-arm fast | None (Pace) |
| 186 | **Vignesh Puthur** | 25 | Bowler | Right-handed | Left-arm wrist spin | Left-Arm Wrist Spin |
| 187 | **Sushant Mishra** | 25 | Bowler | Left-handed | Left-arm fast-medium | None (Pace) |
| 188 | **Yash Raj Punja** | 22 | Bowler | Right-handed | Right-arm leg break | Leg Break |
| 189 | **Brijesh Sharma** | 27 | Bowler | Right-handed | Right-arm medium | None (Pace) |

---

## 5. Duplicate Identity Investigation: Ravi Bishnoi

### 5.1 The Duplicate Conflict
Across all 268 records in `ipl_players.csv`, exactly one player name appears in duplicate:
* **Record 1 (Row 179):** `Team: Rajasthan Royals` | `Name: Ravi Bishnoi` | `Age: 26` | `Role: Bowler` | `Bowling_Style: Right-arm leg break` | `Spin_Type: Leg Break`
* **Record 2 (Row 261):** `Team: Lucknow Super Giants` | `Name: Ravi Bishnoi` | `Age: 26` | `Role: Bowler` | `Bowling_Style: Right-arm leg break` | `Spin_Type: Leg Break`

### 5.2 Forensic Analysis & Historical Provenance:
1. **Franchise Reality:** Ravi Bishnoi was drafted by Lucknow Super Giants ahead of the 2022 season and represented LSG as their primary spinner through IPL 2022, 2023, and 2024.
2. **Duplicate Anomaly:** The simultaneous appearance of Bishnoi under both RR and LSG indicates that `ipl_players.csv` is an uncurated simulation, draft board, or multi-source merge where player transfers or exploratory trades were partially logged without removing the incumbent franchise record.
3. **Cap Status:** Ravi Bishnoi made his senior international debut for India in February 2022 (T20I) and October 2022 (ODI), possessing over 30 international caps. He is **`VERIFIED_CAPPED`**.
4. **Retention Engine Directive:** Because his active franchise contract is contested between RR and LSG in this file, Ravi Bishnoi **CANNOT be evaluated as a confirmed RR retention candidate** without official external contract corroboration.

---

## 6. Retention Candidate Governance: Decoupling Roster Concepts

### 6.1 The Four Decoupled Roster & Contract Concepts
To prevent unverified assumptions from contaminating retention analysis, the platform enforces strict semantic separation across four distinct concepts:

1. **Supplied CSV Franchise Association (`Team == "Rajasthan Royals"` in `ipl_players.csv`):**
   - 27 specific rows in an unverified reference dataset.
   - Contains major dislocations (e.g. Sanju Samson dislocated to CSK; Ravindra Jadeja and Sam Curran assigned to RR; Ravi Bishnoi duplicated in LSG).
   - *Status:* Benchmark reference dataset only; **NOT legal contract proof**.
2. **Historical RR Association (2022–2024 Match Play):**
   - Players who appeared for Rajasthan Royals in official match scorecards during the 2022–2024 seasons in `matches.csv` / `playing_eleven.csv`.
   - *Status:* Verified historical performance fact; **does NOT prove current 2026/2027 contract status**. Do not classify the historical RR core as the current legal squad without authoritative squad or contract evidence.
3. **Verified Current RR Squad Membership:**
   - Legally contracted players on Rajasthan Royals' official roster as certified by official BCCI/IPL Governing Council filings for the active season.
   - *Status:* **PENDING AUTHORITATIVE BCCI RETENTION CIRCULAR**.
4. **Contract & Retention Status:**
   - Official retention declarations under IPL governing rules (e.g. retained under official salary deduction brackets or released to the auction pool).
   - *Status:* **PENDING OFFICIAL FRANCHISE SUBMISSION**.

### 6.2 Mandatory Retention Candidate Governance Rule
* **Authoritative Candidate Universe:** The final retention candidate universe for Module A **must be based strictly on verified current squad membership** once confirmed by official BCCI circulars.
* **Provisional Benchmark Testing:** Until official circulars are released, evaluations performed on the 27 rows of `ipl_players.csv` are labeled **`PROVISIONAL_BENCHMARK_EXPLORATION`** and must never be represented as official retention decisions.

---

## 7. Audit Conclusion & Non-Regression Invariants

1. **Delivery Count Semantics Reconciled:** Verified **200,999 total deliveries (192,709 legal deliveries, 8,290 non-legal delivery records (7,714 wides + 576 no-balls)) across 883 matches (867 with ball-by-ball delivery records)**.
2. **Category Counts Resolved:** Rajasthan Royals squad verified at exactly **27 rows: 12 Bowlers, 6 All-rounders, 5 Batters, 4 Wicketkeeper-Batters**.
3. **Duplicate Isolated:** The only duplicate entity in the file is `Ravi Bishnoi` (RR vs LSG).
4. **Retention Governance Locked:** Candidate universe restricted to verified current squad membership upon official circular availability; provisional benchmark clearly labeled.
5. **Platform Preserved:** No production code, API endpoints, or database tables were modified during this audit.
6. **Protected Parquet Hashes:** All four Round 1 Parquet artifacts remain 100% verified and pristine.
