# ROYALS INTELLIGENCE — ROUND 1 DATA QUALITY & REPOSITORY AUDIT REPORT
**Generated:** 2026-11-10T18:35:02.950563+00:00  
**Competition Target:** SupeRR Selector Season 2 — Round 1  
**Core Objective:** *Identify the Most Reliable Players Under Pressure*  
**Audit Status:** `DATASET_QA_PASSED_WITH_CRITICAL_TRAPS_DOCUMENTED`  

---

## 1. Executive Summary & File Profiles

| Dataset File | Rows | Columns | Exact Duplicates | Primary Key Candidates | Memory Profile |
| :--- | :---: | :---: | :---: | :--- | :--- |
| `ball_by_ball.csv` | 200,999 | 33 | 0 | Verified | Valid |
| `matches.csv` | 883 | 22 | 0 | Verified | Valid |
| `competitions.csv` | 141 | 4 | 0 | Verified | Valid |
| `teams.csv` | 353 | 3 | 0 | Verified | Valid |
| `playing_eleven.csv` | 28,381 | 9 | 0 | Verified | Valid |
| `competition_team_player_mapping.csv` | 6,413 | 6 | 0 | Verified | Valid |

---

## 2. Referential Integrity & Relational Joins

- **Matches $\to$ Competitions:** 883 matches across 138 competitions. Orphaned comps: `0` (100% valid).
- **Matches $\to$ Ball-by-Ball Deliveries:** 867 matches have ball-by-ball records. **16 matches have zero deliveries** (100% of these were abandoned without a ball bowled).
- **Matches $\to$ Playing Eleven:** 880 matches have lineups. 3 matches missing lineups were abandoned prior to toss.
- **Ball-by-Ball $\to$ Player Mapping:** All 959 distinct delivery players are verified in player mapping (0 missing).

---

## 3. Evidence-Based Cricket Delivery Classification (R1-01.1 Corrected)

### Full Delivery Classification Evidence Table

| Category | Record Count | Legal | Illegal | Ambiguous | Evidence & Sequence Behavior |
| :--- | ---: | ---: | ---: | ---: | :--- |
| **Standard (No Extras)** | 189,167 | 189,167 | 0 | 0 | Standard delivery off bat; advances over; batter credited with runs; normal dismissals allowed. |
| **`wide`** | 7,714 | 0 | 7,714 | 0 | Illegal delivery; re-bowled in every over; `over_ball_num` increments without advancing legal balls. `runs == 0`. |
| **`Overstep`** | 576 | 0 | 576 | 0 | Front-foot no-ball; re-bowled in every over; free hit follows. Batter runs count; restricted dismissals. |
| **`legbyes`** | 2,748 | 2,748 | 0 | 0 | Ball strikes pad/body; consumes a legal ball in over; no re-bowl. `runs == 0` (not off bat). |
| **`byes`** | 529 | 529 | 0 | 0 | Ball beats batter without contact; consumes a legal ball in over; no re-bowl. `runs == 0`. |
| **`Penalty`** | 1 | 1 | 0 | 0 | Match 16753, Inn 2, Over 6, Ball 4. Exactly 6 balls bowled in over; concluded normally without re-bowl. |
| **`other`** | 264 | 0 | 0 | 264 | Sequence evidence: re-bowled in 253/264 overs (116 beamers, 72 high full tosses, 0 bowled/caught). Schema labels ambiguously as 'other'. |
| **TOTAL** | **200,999** | **192,445** | **8,290** | **264** | **Strict Legal: 192,445 / Permissive Legal: 192,709** |

---

## 4. Critical Cricket Domain Traps & Governance

### Trap A: Extras Code Trap (`extras1_runs` vs `runs`)
> [!CAUTION]
> **`extras1_runs` is a CATEGORICAL ID CODE, NOT NUMERICAL RUNS!**
> - 1 = Overstep (No Ball)
> - 2 = wide
> - 3 = legbyes
> - 4 = byes
> - 5 = other
> - 6 = NONE (Normal delivery)
> - 7 = Penalty
> Blindly summing `runs + extras1_runs` adds 6 runs to every standard ball! `runs` represents batter runs off the bat only.

### Trap B: Legal Delivery Counting (`over_ball_num`)
> [!WARNING]
> **`over_ball_num` is a sequential delivery counter (up to 13 balls per over), NOT a legal-ball counter.**
> Across 32,350 overs, 6,710 contain illegal deliveries requiring re-bowls.
> **Correct Legal Delivery Rule:** `extras_type not in ['wide', 'Overstep']` (with `other` flagged as ambiguous).

### Trap C: Bowler Wicket Credit Attribution & Spelling Normalization
- **Bowler Credited Wickets:** 10,272 (Bowled, Caught, LBW, Stump, Hit Wicket).
- **Non-Bowler Dismissals:** 609 (RunOut: 600, Retire Out: 6, Obstructing: 3 normalized).
- **Spelling Normalization:** Dataset contains both `'Obstracting the field'` (2) and `'Obstructing the field'` (1). Both normalized to `'Obstructing the field'` and strictly excluded from bowler credit.
- **Unknown Dismissal Guard:** Any unknown dismissal type is rejected from bowler wicket credit by default.

### Trap D: Super Overs Segregation
- Standard Innings: Innings 1 (105,727 balls) & Innings 2 (95,234 balls).
- Super Overs: Innings 3 (25 balls) & Innings 4 (13 balls) across 6 matches: `[34429, 40725, 45512, 48027, 48029, 50359]`. Must be segregated from ordinary innings datasets.

### Trap E: Bowling Speed Sensor Anomalies
> [!WARNING]
> **38.7% of deliveries have `bowl_speed == 0.0`.** Furthermore, corrupt values such as `-1.0` and `1456.1` kph exist in raw data. Bowling speed must be strictly cleaned before use in pace-pressure analysis.

### Trap F: Player Name Duplication (Canonical `player_id`)
> [!IMPORTANT]
> **Never merge on `player_name`!** Exactly 7 player names belong to multiple distinct individuals (e.g. Abdul Samad [SRH Indian batter, ID 7446 vs Pakistan international, ID 6922]; Rashid Khan [Afghanistan superstar, ID 4722 vs UAE cricketer, ID 20172]). All analysis must use `player_id` as the sole canonical key.

### Trap G: Competition Classification
- **IPL (Tier-1 Franchise):** 371 matches across 5 seasons (2022–2026).
- **Senior T20I (International):** 482 matches across 134 competitions.
- **Emerging / A-Team:** 30 matches across 2 competitions (Emerging Asia Cup 2024 & Rising Stars 2025).

---

## 5. Match-State Reconstruction Readiness for R1-02

Match-state reconstruction is fully supported: Innings score, wickets, and legal balls can be derived from cumulative sums of legal deliveries. Chasing target = 1st innings total + 1 (or revised_target for the 23 DLS matches). Balls remaining = (20.0 * 6) - legal_balls_bowled (or revised_overs * 6). Runs required = target - current_score.

- **Revised Target Matches (DLS):** 23 matches recorded with revised targets.

---

## 6. R1-01.1 Acceptance Verification Checklist

- [x] `Penalty` delivery investigated: confirmed legal delivery in Match 16753, Inn 2, Over 6 (exactly 6 balls bowled).

- [x] `other` deliveries (264 records) investigated individually: 116 beamers, 72 high full tosses, 0 bowled/caught dismissals.

- [x] Sequence validation: re-bowled in 253/264 overs; 11 early-terminated overs.

- [x] Ambiguous delivery status retained and explicitly reported (`unresolved_deliveries_count: 264`).

- [x] Dual legal-ball metrics reported: Strict sequence (192,445) vs Permissive (192,709).

- [x] Dismissal spelling normalization implemented (`Obstracting` $\to$ `Obstructing`).

- [x] Unknown dismissals guard tested and verified.

- [x] Deterministic JSON summary and Markdown reports updated.
