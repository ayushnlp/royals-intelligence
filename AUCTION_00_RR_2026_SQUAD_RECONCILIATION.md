# ROYALS INTELLIGENCE — AUCTION-00 RR 2026 SQUAD RECONCILIATION
## Rajasthan Royals Squad Baseline, Role Classification & Trade Governance
**Domain:** RR Auction & Retention Intelligence (Stage AUCTION-00)  
**Execution Timestamp:** 2026-11-18T07:26:30+05:30  
**Source Dataset:** `data/raw/rajasthan_royals/round_1_data_pack/ipl_players.csv`  
**Total Rajasthan Royals Rows:** Exactly 27 Records  
**Audit Status:** COMPLETE & VERIFIED

---

## 1. Executive Summary: The 27-Player Baseline

In the supplied reference dataset `ipl_players.csv`, exactly **27 rows** are registered under `Team == 'Rajasthan Royals'`.

A rigorous role audit classifies these 27 entries into four functional categories:

| Category | Player Count | % of RR Squad | Primary Disciplines |
| :--- | :---: | :---: | :--- |
| **Bowlers** | 12 | 44.4% | Right-arm fast (3), Medium-fast / Medium (6), Leg-break / Wrist spin (3) |
| **All-rounders** | 6 | 22.2% | Left-arm orthodox (1), Left-arm medium-fast (1), Leg break (2), Medium (2) |
| **Batters** | 5 | 18.5% | Left-handed (4), Right-handed (1) |
| **Wicketkeeper-Batters** | 4 | 14.8% | Right-handed (2), Left-handed (2) |
| **Total** | **27** | **100.0%** | Comprehensive Roster Snapshot |

---

## 2. Exhaustive Roster Ledger (All 27 Rajasthan Royals Records)

| Row Index | Player Name | Age | Assigned Role | Batting Style | Bowling Style | Spin Type | Governance / Trade Note |
| :---: | :--- | :---: | :--- | :--- | :--- | :--- | :--- |
| 163 | **Riyan Parag** | 22 | All-rounder | Right-handed | Right-arm leg break | Leg break | Core retention candidate |
| 164 | **Yashasvi Jaiswal** | 22 | Batter | Left-handed | Right-arm leg break | Leg break | Core retention candidate |
| 165 | **Vaibhav Sooryavanshi**| 13 | Batter | Left-handed | Left-arm orthodox | Orthodox | Uncapped domestic prodigy |
| 166 | **Dhruv Jurel** | 23 | Wicketkeeper-Batter | Right-handed | *None (null)* | *None (null)* | Core retention candidate |
| 167 | **Shimron Hetmyer** | 27 | Batter | Left-handed | Right-arm leg break | Leg break | Overseas finishing core |
| 168 | **Donovan Ferreira** | 26 | Wicketkeeper-Batter | Right-handed | Right-arm off break | Off break | Overseas utility keeper |
| 169 | **Lhuan-dre Pretorius** | 18 | Wicketkeeper-Batter | Left-handed | *None (null)* | *None (null)* | Overseas uncapped keeper |
| 170 | **Shubham Dubey** | 29 | Batter | Left-handed | Right-arm off break | Off break | Domestic uncapped batter |
| 171 | **Aman Rao** | 20 | Batter | Right-handed | *None (null)* | *None (null)* | Domestic development batter |
| 172 | **Ravi Singh** | 22 | Wicketkeeper-Batter | Left-handed | *None (null)* | *None (null)* | Domestic backup keeper |
| 173 | **Ravindra Jadeja** | 35 | All-rounder | Left-handed | Left-arm orthodox | Orthodox | **Trade Benchmark Note (Ex-CSK)** |
| 174 | **Sam Curran** | 26 | All-rounder | Left-handed | Left-arm medium-fast | *None* | **Trade Benchmark Note (Ex-PBKS)** |
| 175 | **Dasun Shanaka** | 32 | All-rounder | Right-handed | Right-arm medium | *None* | Overseas pace all-rounder |
| 176 | **Yudhvir Singh** | 26 | All-rounder | Right-handed | Right-arm fast-medium | *None* | Domestic pace all-rounder |
| 177 | **Emanjot Singh Chahal**| 24 | All-rounder | Right-handed | Right-arm leg break | Leg break | Domestic spin all-rounder |
| 178 | **Jofra Archer** | 29 | Bowler | Right-handed | Right-arm fast | *None* | Overseas express pace |
| 179 | **Ravi Bishnoi** | 24 | Bowler | Right-handed | Right-arm leg break | Googly | **Duplicate Row (also Row 261 LSG)**|
| 180 | **Tushar Deshpande** | 29 | Bowler | Left-handed | Right-arm medium | *None* | Domestic pace asset |
| 181 | **Nandre Burger** | 28 | Bowler | Left-handed | Left-arm fast-medium | *None* | Overseas left-arm pace |
| 182 | **Sandeep Sharma** | 31 | Bowler | Right-handed | Right-arm medium | *None* | Veteran domestic swing bowler |
| 183 | **Adam Milne** | 32 | Bowler | Right-handed | Right-arm fast | *None* | Overseas express pace |
| 184 | **Kwena Maphaka** | 18 | Bowler | Left-handed | Left-arm fast-medium | *None* | Overseas pace prodigy (Capped SA) |
| 185 | **Kuldeep Sen** | 27 | Bowler | Right-handed | Right-arm fast | *None* | Domestic express pace |
| 186 | **Vignesh Puthur** | 23 | Bowler | Right-handed | Left-arm wrist spin | Chinaman | Uncapped mystery spin asset |
| 187 | **Sushant Mishra** | 23 | Bowler | Left-handed | Left-arm fast-medium | *None* | Domestic left-arm pace |
| 188 | **Yash Raj Punja** | 21 | Bowler | Right-handed | Right-arm leg break | Leg break | Domestic development spinner |
| 189 | **Brijesh Sharma** | 22 | Bowler | Right-handed | Right-arm medium | *None* | Domestic development seamer |

---

## 3. Forensic Roster Dislocations & Trade Context

Inspection of `ipl_players.csv` reveals three significant franchise roster dislocations that must be accounted for during analytical modeling:

### 3.1 Sanju Samson (Listed under Chennai Super Kings)
- **Record:** Row 1 in `ipl_players.csv` lists `Sanju Samson` under `Team == 'Chennai Super Kings'`.
- **Context:** Samson served as the celebrated captain and wicketkeeper of Rajasthan Royals throughout the 2021–2024 cycle.
- **Analytical Governance:** Samson's historical performance data (2022–2024) is fully preserved within the RR match telemetry, but in AUCTION-05 retention modeling, he is not assumed to be automatically locked to RR without legal contract confirmation.

### 3.2 Ravindra Jadeja & Sam Curran (Listed under Rajasthan Royals)
- **Record:** Row 173 lists `Ravindra Jadeja` and Row 174 lists `Sam Curran` under `Rajasthan Royals`.
- **Context:** Historically, Jadeja was a cornerstone of CSK and Curran of PBKS/CSK. Their inclusion under RR in `ipl_players.csv` reflects trade-simulation or prospective draft-pool modeling within the competition data pack.
- **Analytical Governance:** While evaluated within the 27-player RR baseline, retention recommendations must disclose their external franchise origin.

### 3.3 Ravi Bishnoi (Duplicate Attribution)
- **Record:** Bishnoi appears at Row 179 (RR) and Row 261 (LSG).
- **Governance:** Unified under canonical entity `RR-PLAYER-00179` / `RR-PLAYER-00261` with dual-franchise historical attribution.

---

## 4. Mid-Season Squad Replacements During IPL 2026

During the IPL 2026 campaign, two squad members were officially withdrawn and replaced:
- **Sam Curran** (withdrawn mid-season due to national duties/injury) $\rightarrow$ replaced by **Dasun Shanaka** (Overseas pace all-rounder).
- **Ravi Singh** (withdrawn mid-season) $\rightarrow$ replaced by **Emanjot Singh Chahal** (Domestic spin all-rounder).

---

## 5. Official IPL 2027 Retention & Release Ledger (Announced Ahead of Dec 16, 2026 Mini-Auction)

Ahead of the IPL 2027 mini-auction on December 16, 2026, Rajasthan Royals officially confirmed the retention of 17 players from their existing roster, added 2 players via trades, traded out 1 player, and released 9 players.

### 5.1 Retained Players (17)
1. **Riyan Parag** (Captain, All-rounder)
2. **Yashasvi Jaiswal** (Batter)
3. **Vaibhav Sooryavanshi** (Batter)
4. **Ravindra Jadeja** (All-rounder)
5. **Dhruv Jurel** (Wicket-Keeper)
6. **Jofra Archer** (Overseas - ENG, Bowler)
7. **Ravi Bishnoi** (Bowler)
8. **Sandeep Sharma** (Bowler)
9. **Nandre Burger** (Overseas - SA, Bowler)
10. **Donovan Ferreira** (Overseas - SA, Wicket-Keeper)
11. **Lhuan-dre Pretorius** (Overseas - SA, Wicket-Keeper)
12. **Dasun Shanaka** (Overseas - SL, All-rounder)
13. **Shubham Dubey** (Batter)
14. **Aman Rao Perala** (Batter)
15. **Sushant Mishra** (Bowler)
16. **Brijesh Sharma** (Bowler)
17. **Yash Raj Punja** (Bowler)

### 5.2 Traded-In Players (2)
18. **Mohammed Shami** (Traded in from Lucknow Super Giants for ₹8 crore, Bowler)
19. **Manimaran Siddharth** (Traded in from Lucknow Super Giants for ₹75 lakh, Bowler)

### 5.3 Traded-Out Player (1)
- **Sam Curran** (Traded to Lucknow Super Giants for ₹2.4 crore, All-rounder)

### 5.4 Released Players (9)
1. **Shimron Hetmyer** (Overseas - WI, Batter)
2. **Tushar Deshpande** (Bowler)
3. **Adam Milne** (Overseas - NZ, Bowler)
4. **Kwena Maphaka** (Overseas - SA, Bowler)
5. **Kuldeep Sen** (Bowler)
6. **Yudhvir Singh Charak** (All-rounder)
7. **Vignesh Puthur** (Bowler)
8. **Ravi Singh** (Wicket-Keeper)
9. **Emanjot Singh Chahal** (All-rounder)

### 5.5 Pre-Auction Roster Summary
- **Current Active Squad:** 19 players (14 Indian, 5 Overseas)
- **Squad Slots Available for Auction:** Exactly 6 slots (maximum squad limit: 25)
- **Overseas Slots Available for Auction:** Exactly 3 slots (maximum overseas limit: 8)
