# ROYALS INTELLIGENCE — AUCTION-00 PLAYER IDENTITY DISCREPANCIES
## Entity Deduplication, Roster Dislocation & Identity Resolution Audit (Final Corrected Version)
**Domain:** RR Auction & Retention Intelligence (Stage AUCTION-00)  
**Execution Timestamp:** 2026-11-16T22:30:00+05:30  
**Focus:** Duplicate Records, Franchise Dislocations, Name Normalization & Unmapped Entities

---

## 1. Executive Summary

This report documents all player identity discrepancies, duplicate entries, roster dislocations, and canonical mapping challenges discovered during the forensic audit of `ipl_players.csv` and its reconciliation with `competition_team_player_mapping.csv` and `ball_by_ball.csv`.

The platform enforces **strict entity resolution**: raw strings from third-party CSV files are never treated as canonical primary keys. Every individual cricketer is resolved to a single, immutable `canonical_player_id`.

---

## 2. In-Depth Investigation: The Ravi Bishnoi Duplicate Anomaly

### 2.1 Empirical Discrepancy Record
In `data/raw/rajasthan_royals/round_1_data_pack/ipl_players.csv`, the exact player name `Ravi Bishnoi` appears twice across differing franchise affiliations:

```text
Row 179:
  Team:           Rajasthan Royals
  Name:           Ravi Bishnoi
  Age:            26
  Role:           Bowler
  Batting_Style:  Right-handed
  Bowling_Style:  Right-arm leg break
  Spin_Type:      Leg Break

Row 261:
  Team:           Lucknow Super Giants
  Name:           Ravi Bishnoi
  Age:            26
  Role:           Bowler
  Batting_Style:  Right-handed
  Bowling_Style:  Right-arm leg break
  Spin_Type:      Leg Break
```

### 2.2 Historical Facts & Ground Truth:
1. **Franchise Reality:** Ravi Bishnoi represented Punjab Kings (PBKS) in IPL 2020 and 2021. Prior to the 2022 mega-auction, he was drafted by the newly formed Lucknow Super Giants (LSG) as one of their three pre-auction draft picks. He played for LSG across IPL 2022, 2023, and 2024.
2. **The Rajasthan Royals Dislocation:** Ravi Bishnoi has never officially played an IPL match for Rajasthan Royals in real-world tournament history through IPL 2024. His presence in Row 179 under `Rajasthan Royals` indicates that `ipl_players.csv` incorporates prospective simulation drafts, mock trade rosters, or unmerged pipeline data.
3. **Senior International Cap Audit:**
   - Test Caps: 0
   - ODI Debut: 6 October 2022 vs South Africa (Cap #246)
   - T20I Debut: 16 February 2022 vs West Indies (Cap #95)
   - Total Senior International Caps: 33+ appearances.
   - **Certification State:** `VERIFIED_CAPPED`. Bishnoi is strictly disqualified from all uncapped leaderboards (Modules B and C).
4. **Retention Engine Directive:** Because his active franchise contract is contested between RR and LSG in this file, Ravi Bishnoi **CANNOT be evaluated as a confirmed RR retention candidate** without official external contract corroboration.

---

## 3. League-Wide Franchise Roster Dislocations & Governance Principles

Forensic inspection confirms that `ipl_players.csv` captures a reshuffled post-2025 roster landscape, containing major relocations of franchise marquee pillars:

| Player Name | Age | CSV Franchise (`Team`) | Real-World Incumbent Franchise (2022–2024) | Semantic & Strategic Impact |
| :--- | :---: | :--- | :--- | :--- |
| **Sanju Samson** | 32 | **Chennai Super Kings** (Row 1) | **Rajasthan Royals** (Captain) | Long-standing RR captain and wicketkeeper-batter listed under CSK. |
| **Ravindra Jadeja** | 37 | **Rajasthan Royals** (Row 173) | **Chennai Super Kings** | 12-season CSK icon and core all-rounder listed under RR. |
| **Sam Curran** | 28 | **Rajasthan Royals** (Row 174) | **Punjab Kings** | Marquee England all-rounder listed under RR. |
| **Jos Buttler** | 36 | **Gujarat Titans** (Row 219) | **Rajasthan Royals** | Core RR opener and Orange Cap winner dislocated to GT. |
| **Yuzvendra Chahal** | 36 | **Punjab Kings** (Row 156) | **Rajasthan Royals** | RR's leading wicket-taker and Purple Cap winner dislocated to PBKS. |
| **Trent Boult** | 37 | **Mumbai Indians** (Row 49) | **Rajasthan Royals** | RR's powerplay pace spearhead dislocated to MI. |
| **David Miller** | 37 | **Delhi Capitals** (Row 116) | **Gujarat Titans** | Core GT middle-overs finisher dislocated to DC. |
| **Marcus Stoinis** | 37 | **Punjab Kings** (Row 146) | **Lucknow Super Giants** | Core LSG all-rounder dislocated to PBKS. |
| **Mitchell Starc** | 36 | **Delhi Capitals** (Row 131) | **Kolkata Knight Riders** | ₹24.75 Cr KKR pace signing dislocated to DC. |

### Governance Directives for Retention Universe:
To prevent ungrounded assumptions, the system enforces the following boundaries:
1. **Separation of Concepts:** The system strictly separates:
   - Supplied CSV franchise association (`Team == "Rajasthan Royals"` in `ipl_players.csv`).
   - Historical RR association (match scorecards 2022–2024).
   - Verified current RR squad membership (official BCCI/IPL contract filings).
   - Contract and retention status (official retention declarations).
2. **Prohibition of Unverified Classification:** The historical RR core (e.g. Samson, Jaiswal, Parag, Jurel, Sandeep Sharma, Hetmyer) **must NOT be classified as the current legal squad without authoritative contract evidence**.
3. **Sole Authoritative Candidate Universe:** The final retention candidate universe for Module A must be founded strictly on **verified current RR squad membership** once confirmed by official BCCI circulars.
4. **Provisional Benchmarking:** Prior to official circular release, any evaluations performed on the 27 rows of `ipl_players.csv` are explicitly tagged as `PROVISIONAL_BENCHMARK_EXPLORATION`.

---

## 4. Name Normalization & Canonical Resolution Challenges

When joining `ipl_players.csv` with `competition_team_player_mapping.csv` and `ball_by_ball.csv`, 244 of 267 names (91.4%) resolve via exact lowercase string matching. The remaining 23 entities require specific canonical aliasing rules:

| Raw CSV Name (`ipl_players.csv`) | Canonical Name in Mapping CSV | Entity ID in Data Pack | Resolution Rule |
| :--- | :--- | :---: | :--- |
| `Pat Cummins` | `Patrick Cummins` | 2736 | Expand informal first name (`Pat` &rarr; `Patrick`). |
| `Nitish Kumar Reddy` | `Nitish Reddy` | 8115 | Remove middle domestic name variant. |
| `Tilak Varma` | `Namboori Thakur Tilak Varma` | 7455 | Strip regional patronymic prefix. |
| `Vijaykumar Vyshak` | `Vyshak Vijay Kumar` | 8125 | Reorder South Indian naming inversion. |
| `Aman Hakim Khan` | `Aman Khan` | 7545 | Strip middle patronymic string. |
| `M Siddharth` | `Manimaran Siddharth` | 7460 | Expand initial to full Tamil given name. |
| `Prithvi Raj Yarra` | `Yarra Prithviraj` | 6185 | Invert surname prefix. |
| `Pravin Dubey` | `Praveen Dubey` | 4252 | Phonetic vowel normalization (`i` vs `ee`). |
| `Zak Foulkes` | `Zachary Foulkes` | 25890 | Nickname to formal registration name. |

---

## 5. Youth & Emerging Unmapped Entities

Several youth and emerging players in `ipl_players.csv` have zero deliveries in the historical 2022–2026 data pack (which contains 200,999 total deliveries and 192,709 legal deliveries) because they are newly drafted talents:

| Player Name | Age | Franchise | Role | Career Status & Provenance |
| :--- | :---: | :--- | :--- | :--- |
| **Vaibhav Sooryavanshi** | 15 | Rajasthan Royals | Batter | India U19 prodigy; youngest IPL signee. 0 senior caps (`VERIFIED_UNCAPPED`). |
| **Lhuan-dre Pretorius** | 20 | Rajasthan Royals | Wicketkeeper-Batter | South Africa U19 star; zero senior international caps (`VERIFIED_UNCAPPED`). |
| **Kwena Maphaka** | 20 | Rajasthan Royals | Bowler | South Africa senior T20I debut Aug 2024 (`VERIFIED_CAPPED`). |
| **Aman Rao** | 22 | Rajasthan Royals | Batter | Domestic emerging talent; pending senior match scorecard ingestion. |
| **Ravi Singh** | 24 | Rajasthan Royals | Wicketkeeper-Batter | Domestic wicketkeeper; pending match scorecard ingestion. |
| **Yash Raj Punja** | 22 | Rajasthan Royals | Bowler | Domestic leg-spinner; pending scorecard ingestion. |
| **Brijesh Sharma** | 27 | Rajasthan Royals | Bowler | Domestic medium-pacer; pending scorecard ingestion. |

### Policy for Unmapped Youth Candidates:
If an emerging candidate has zero historical deliveries in the Round 1 data pack, the ranking engine **must NOT assign arbitrary scores**. It must report:
`Performance Metric: Insufficient Historical Delivery Volume (Sample Size = 0 Balls)`.
Young uncapped players without match data remain in the scouting radar pool but cannot leapfrog proven performers on statistical leaderboards.
