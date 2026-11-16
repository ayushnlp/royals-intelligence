# ROYALS INTELLIGENCE — DATASET INVENTORY & PROFILING REPORT
**Platform:** Rajasthan Royals Cricket Intelligence & IPL Decision Support System  
**Dataset Source:** Official Rajasthan Royals Round 1 Data Pack (`data/raw/rajasthan_royals/round_1_data_pack/`)  
**Audit Timestamp:** 2026-11-16T15:35:00+05:30  
**Verification Mode:** Exhaustive Ball-by-Ball & Entity Profiling (Zero Synthetic Injections)  

---

## 1. EXECUTIVE SUMMARY & DATA PACK OVERVIEW

The primary dataset powering the ROYALS INTELLIGENCE platform consists of the official, proprietary data pack provided for the Rajasthan Royals SupeRR Selector Season 2 competition. The pack contains **six relational CSV files** and the **official challenge problem statement specification (PDF)**, totaling **42.9 MB** of raw data.

The data encompasses **883 elite T20 matches** played between **22 January 2022 and 1 November 2026** across **17 countries** and **98 international and franchise venues**. This includes five full Indian Premier League seasons (**IPL 2022, 2023, 2024, 2025, and 2026**), key Asian developmental tournaments (**Men's T20 Emerging Teams Asia Cup 2024**, **Asia Cup Rising Stars 2025**), and **134 T20 International (T20I) tournaments/series**.

The core granular engine is driven by **200,999 ball-by-ball delivery records**, capturing tactical attributes such as batter handedness, bowler style, ball release speed (radar telemetry), stroke classification, delivery variation/movement, field direction sector, and wicket dismissals.

### Summary Inventory Table

| File Name | File Size | Row Count | Column Count | Primary Key / Natural Key | Description & Tactical Utility |
| :--- | :---: | :---: | :---: | :---: | :--- |
| `ball_by_ball.csv` | 41,071,609 B | 200,999 | 33 | `(match_id, innings, overid, over_ball_num)` | Granular ball-by-ball deliveries with stroke, delivery style, speed, and dismissals. |
| `competitions.csv` | 7,624 B | 141 | 4 | `comp_id` | Catalog of 134 T20I series and 7 domestic/regional T20 leagues (IPL 2022–2026). |
| `teams.csv` | 6,922 B | 353 | 3 | `(comp_id, team_id)` | Competition-specific team participation mappings (38 unique teams). |
| `matches.csv` | 123,864 B | 883 | 22 | `match_id` | Match-level metadata: dates, venues, captains, toss decisions, results, and revised targets. |
| `playing_eleven.csv` | 966,287 B | 28,381 | 9 | `(match_id, team_id, player_id)` | Playing XI rosters with captaincy, wicketkeeper, batting order, and Impact Player tags. |
| `competition_team_player_mapping.csv` | 462,969 B | 6,413 | 6 | `(comp_id, team_id, player_id)` | Entity resolution linking player IDs (1,217 unique) to canonical player names. |
| `Round_1_Problem_Statement...pdf` | 254,082 B | 7 pages | N/A | Document | Official competition specification defining Round 1 player evaluation requirements. |

---

## 2. DETAILED FILE PROFILES & FIELD DICTIONARIES

### 2.1. `ball_by_ball.csv` (200,999 rows, 33 columns)

This file constitutes the primary tactical foundation for all player reliability, matchup modeling, and tactical optimization engines.

| Column Name | Data Type | Null Count | Null % | Unique Values | Sample Value | Tactical & Engineering Definition |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| `match_id` | `int64` | 0 | 0.0% | 867 | `13511` | Foreign key referencing `matches.match_id`. Exactly 867 matches have delivery data. |
| `innings` | `int64` | 0 | 0.0% | 4 | `1` | Innings number (1 = first innings, 2 = chase, 3/4 = Super Over innings). |
| `overid` | `int64` | 0 | 0.0% | 20 | `1` | 1-indexed over number (1 to 20). 1–6 = Powerplay, 7–15 = Middle, 16–20 = Death. |
| `over_ball_num` | `int64` | 0 | 0.0% | 13 | `1` | Sequential delivery counter within the over (1 up to 13 due to illegal deliveries). |
| `innings_ball_num` | `int64` | 0 | 0.0% | 136 | `1` | Cumulative sequential delivery counter within the entire innings. |
| `batting_team_id` | `int64` | 0 | 0.0% | 38 | `22` | Team ID of the batting side (e.g., 3 = Rajasthan Royals). |
| `bowling_team_id` | `int64` | 0 | 0.0% | 38 | `28` | Team ID of the bowling side. |
| `striker_id` | `int64` | 0 | 0.0% | 888 | `1187` | Unique identifier of the batter facing the delivery. |
| `striker_name` | `string` | 0 | 0.0% | 885 | `Jason Roy` | Display name of the striker. |
| `non_striker_id` | `int64` | 0 | 0.0% | 867 | `6273` | Unique identifier of the non-striker. |
| `non_striker_name` | `string` | 0 | 0.0% | 864 | `Tom Banton` | Display name of the non-striker. |
| `bowler_id` | `int64` | 0 | 0.0% | 647 | `1772` | Unique identifier of the bowler delivering the ball. |
| `bowler_name` | `string` | 0 | 0.0% | 646 | `Sheldon Cottrell` | Display name of the bowler. |
| `batting_type` | `string` | 0 | 0.0% | 2 | `RHB` | Batter stance: `RHB` (131,006 deliveries, 65.2%) or `LHB` (69,993 deliveries, 34.8%). |
| `bowling_type` | `string` | 0 | 0.0% | 12 | `Left-arm fast-medium` | 12 distinct bowling sub-disciplines (e.g., Right-arm Leg-Break, Right-arm Fast). |
| `batting_order` | `int64` | 0 | 0.0% | 13 | `1` | Batter's entry/lineup position (1 = opener up to 11 = tailender). |
| `runs` | `int64` | 0 | 0.0% | 7 | `0` | **Runs scored strictly off the bat** (values 0, 1, 2, 3, 4, 5, 6). |
| `is_four` | `bool` | 0 | 0.0% | 2 | `False` | True if the delivery resulted in a boundary 4 off the bat (24,196 occurrences). |
| `is_six` | `bool` | 0 | 0.0% | 2 | `False` | True if the delivery resulted in a 6 off the bat (11,043 occurrences). |
| `is_wicket` | `bool` | 0 | 0.0% | 2 | `False` | True if a dismissal occurred on this delivery (10,881 occurrences). |
| `dismissal_type_id` | `float64` | 190,118 | 94.6% | 8 | `1.0` | Categorical numerical code for dismissal type. |
| `dismissal_type` | `string` | 190,118 | 94.6% | 9 | `Caught` | Dismissal method: Caught (7,557), Bowled (1,775), LBW (709), RunOut (600), Stump (214), Hit Wicket (17), Retire Out (6), Obstructing field (3). |
| `dismissed_player_id` | `float64` | 190,107 | 94.6% | 814 | `1187.0` | Player ID of the dismissed batter. |
| `extras_type` | `string` | 189,167 | 94.1% | 6 | `wide` | Type of extra: `wide` (7,714), `legbyes` (2,748), `Overstep` (576), `byes` (529), `other` (264), `Penalty` (1). |
| `extras1_runs` | `int64` | 0 | 0.0% | 7 | `6` | **CRITICAL ENUM CODE (DO NOT SUM):** 1=Overstep, 2=wide, 3=legbyes, 4=byes, 5=other, 6=NONE, 7=Penalty. |
| `extras_2_runs` | `int64` | 0 | 0.0% | 3 | `0` | Auxiliary extras runs conceded on no-balls/beamers (non-zero on only 36 deliveries). |
| `pace_or_spin` | `string` | 0 | 0.0% | 2 | `Pace` | High-level bowling classification: `Pace` (123,886 balls, 61.6%) vs `Spin` (77,113 balls, 38.4%). |
| `bowl_speed` | `float64` | 0 | 0.0% | 1,033 | `0.0` | Radar delivery release speed in km/h. 123,137 deliveries (61.3%) have valid telemetry. |
| `stroke` | `string` | 6,158 | 3.1% | 30 | `Cover Drive` | Shot type classification (e.g., Pull shot 24.6K, Cover Drive 20.8K, Worked 20.8K). |
| `delivery_style` | `string` | 391 | 0.2% | 34 | `Inswing` | Ball trajectory & seam movement (e.g., Seamed In 22.1K, Orthodox 19.2K, Leg Break 15.4K). |
| `over_or_around` | `string` | 407 | 0.2% | 2 | `Over` | Bowling angle relative to the wicket: `Over` the wicket (154,670, 77.1%) vs `Around` the wicket (45,922, 22.9%). |
| `on_or_off` | `string` | 0 | 0.0% | 2 | `Off-side` | Ground sector targeted: `Off-side` (104,875, 52.2%) vs `On-side` (96,124, 47.8%). |
| `delivery_ist_time` | `string` | 0 | 0.0% | 200,826 | `2022-01-23...` | Timestamp of delivery recording in UTC/IST. |

---

### 2.2. `competitions.csv` (141 rows, 4 columns)

Defines the tournament landscape and season categorization.

| Column Name | Data Type | Null Count | Null % | Unique Values | Sample Value | Tactical & Engineering Definition |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| `comp_id` | `int64` | 0 | 0.0% | 141 | `3395` | Primary key identifying the tournament or series. |
| `comp_name` | `string` | 0 | 0.0% | 141 | `IPL 2024` | Formal competition title. |
| `match_format` | `string` | 0 | 0.0% | 2 | `T20I` | Format tier: `T20I` (134 international series) vs `T20` (7 domestic/regional leagues). |
| `season` | `string` | 0 | 0.0% | 8 | `2024` | Season designation (2022, 2023, 2024, 2025, 2026, 2022/23, 2023/24, 2024/25). |

#### Tournament Breakdown:
- **Major Domestic Franchise Tournaments (7):**
  - `[1358]` IPL 2022 (Season 2022)
  - `[1715]` IPL 2023 (Season 2023)
  - `[2193]` IPL 2024 (Season 2024)
  - `[2725]` IPL 2025 (Season 2025)
  - `[3298]` IPL 2026 (Season 2026)
  - `[2670]` Men's T20 Emerging Teams Asia Cup 2024
  - `[3289]` Asia Cup Rising Stars 2025
- **International T20 Competitions (134):**
  - Includes ICC T20 World Cup qualifiers, bilateral series involving India, Australia, England, South Africa, West Indies, New Zealand, Pakistan, Sri Lanka, Afghanistan, Bangladesh, and emerging ICC nations.

---

### 2.3. `teams.csv` (353 rows, 3 columns)

Maps 38 unique team entities across all 141 competitions.

| Column Name | Data Type | Null Count | Null % | Unique Values | Sample Value | Tactical & Engineering Definition |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| `comp_id` | `int64` | 0 | 0.0% | 141 | `1331` | Foreign key referencing `competitions.comp_id`. |
| `team_id` | `int64` | 0 | 0.0% | 38 | `3` | Unique team entity identifier. Team `3` = Rajasthan Royals. |
| `team_name` | `string` | 0 | 0.0% | 38 | `Rajasthan Royals` | Canonical team franchise or national team name. |

---

### 2.4. `matches.csv` (883 rows, 22 columns)

Provides match context, venue associations, toss choices, and official match outcomes.

| Column Name | Data Type | Null Count | Null % | Unique Values | Sample Value | Tactical & Engineering Definition |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| `match_id` | `int64` | 0 | 0.0% | 883 | `13511` | Primary key uniquely identifying each fixture. |
| `comp_id` | `int64` | 0 | 0.0% | 138 | `1331` | Foreign key referencing `competitions.comp_id`. |
| `match_number` | `int64` | 0 | 0.0% | 75 | `1` | Sequential match number within the tournament. |
| `match_date` | `string` | 0 | 0.0% | 686 | `2022-01-22` | Date of match (YYYY-MM-DD format). |
| `stage` | `string` | 0 | 0.0% | 7 | `League` | Match tier: League (827), Semi Final (20), Final (14), Qualifier 1 (7), Qualifier 2 (7), Eliminator (7), 3rd Place Play-off (1). |
| `venue_id` | `int64` | 0 | 0.0% | 98 | `54` | Foreign key identifying ground location (98 unique stadiums). |
| `venue_country` | `string` | 0 | 0.0% | 17 | `India` | Host country of venue (India, West Indies, Australia, UAE, England, etc.). |
| `home_team_id` | `int64` | 0 | 0.0% | 36 | `3` | Designated home team entity ID. |
| `home_team` | `string` | 0 | 0.0% | 36 | `Rajasthan Royals` | Designated home team name. |
| `away_team_id` | `int64` | 0 | 0.0% | 36 | `28` | Designated away team entity ID. |
| `away_team` | `string` | 0 | 0.0% | 36 | `West Indies` | Designated away team name. |
| `home_team_captain_id` | `float64` | 44 | 5.0% | 89 | `2258.0` | Player ID of home captain (e.g., 2258 = Sanju Samson). |
| `away_team_captain_id` | `float64` | 45 | 5.1% | 98 | `478.0` | Player ID of away captain. |
| `toss_win_team_id` | `float64` | 15 | 1.7% | 37 | `3.0` | Team ID winning the pre-match coin toss. |
| `toss_opted` | `string` | 15 | 1.7% | 2 | `Fielding` | Decision made at toss: `Fielding` (618 matches, 71.2%) vs `Batting` (250 matches, 28.8%). |
| `man_of_the_match` | `int64` | 0 | 0.0% | 293 | `2258` | Player ID awarded Player of the Match (0 = unawarded/abandoned). |
| `first_inn_revised_overs` | `float64` | 858 | 97.2% | 13 | `114.0` | Revised scheduled overs in rain-curtailed 1st innings. |
| `second_inn_revised_overs` | `float64` | 858 | 97.2% | 12 | `114.0` | Revised scheduled overs in rain-curtailed 2nd innings. |
| `revised_target` | `float64` | 860 | 97.4% | 23 | `143.0` | Official revised target under DLS / VJD calculations. |
| `knock_out` | `int64` | 0 | 0.0% | 2 | `0` | Binary indicator: 1 = Knockout / Playoff match (56 matches), 0 = League. |
| `win_team_id` | `float64` | 41 | 4.6% | 36 | `3.0` | Team ID of victorious side (null in 41 no-result/tied matches). |
| `result` | `string` | 0 | 0.0% | 670 | `Rajasthan Royals Won by 6 Wickets` | Official match result description string. |

---

### 2.5. `playing_eleven.csv` (28,381 rows, 9 columns)

Captures roster submissions, batting orders, specialized roles, and in-match substitutions.

| Column Name | Data Type | Null Count | Null % | Unique Values | Sample Value | Tactical & Engineering Definition |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| `match_id` | `int64` | 0 | 0.0% | 880 | `13511` | Foreign key referencing `matches.match_id`. |
| `team_id` | `int64` | 0 | 0.0% | 38 | `3` | Foreign key referencing `teams.team_id`. |
| `player_id` | `int64` | 0 | 0.0% | 1,082 | `2258` | Unique player ID in the match squad. |
| `batting_order` | `float64` | 8,678 | 30.6% | 13 | `3.0` | Stated batting position in team lineup (1 to 11). |
| `is_played` | `bool` | 0 | 0.0% | 2 | `True` | True if the player actively took the field or batted/bowled. |
| `is_captain` | `object` | 8,667 | 30.5% | 2 | `True` | True if the player served as team captain in this match. |
| `is_wk` | `object` | 8,667 | 30.5% | 2 | `True` | True if the player served as the designated wicketkeeper. |
| `is_impact` | `int64` | 0 | 0.0% | 2 | `1` | Binary flag: 1 = Substituted onto the field as an **Impact Player** (558 instances). |
| `is_impact_off` | `int64` | 0 | 0.0% | 2 | `1` | Binary flag: 1 = Substituted off the field for an **Impact Player** (558 instances). |

---

### 2.6. `competition_team_player_mapping.csv` (6,413 rows, 6 columns)

The definitive canonical identity mapping table resolving player IDs and names across all tournaments and franchises.

| Column Name | Data Type | Null Count | Null % | Unique Values | Sample Value | Tactical & Engineering Definition |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| `comp_id` | `int64` | 0 | 0.0% | 140 | `2193` | Foreign key referencing `competitions.comp_id`. |
| `comp_name` | `string` | 0 | 0.0% | 140 | `IPL 2024` | Competition name string. |
| `team_id` | `int64` | 0 | 0.0% | 38 | `3` | Foreign key referencing `teams.team_id`. |
| `team_name` | `string` | 0 | 0.0% | 38 | `Rajasthan Royals` | Team franchise / national name. |
| `player_id` | `int64` | 0 | 0.0% | 1,217 | `6819` | Canonical unique player identifier. |
| `player_name` | `string` | 0 | 0.0% | 1,210 | `Yashasvi Jaiswal` | Canonical player full name. |

---

## 3. RELATIONAL INTEGRITY & LINKAGE VERIFICATION

An automated referential integrity check was executed across the entire data pack with 100% mathematical closure:

1. **Deliveries to Matches Linkage:**  
   - $\text{BBB Matches} \subseteq \text{Matches}$: **TRUE** (0 orphan matches in `ball_by_ball.csv`).
   - 867 of 883 matches have full ball-by-ball delivery records. The remaining 16 matches were abandoned without a ball bowled due to rain or adverse conditions.
2. **Matches to Competitions Linkage:**  
   - $\text{Matches Competitions} \subseteq \text{Competitions}$: **TRUE** (0 orphan competitions).
3. **Playing XI to Entity Mapping Linkage:**  
   - $\text{P11 Players} \subseteq \text{Player Mapping}$: **TRUE** (1,082 unique players in `playing_eleven.csv` all resolve to canonical mapping entries).
4. **Deliveries to Entity Mapping Linkage:**  
   - $\text{BBB Players (Strikers } \cup \text{ Bowlers)} \subseteq \text{Player Mapping}$: **TRUE** (0 unmapped players across 200,999 deliveries).
5. **Delivery Natural Key Uniqueness:**  
   - Natural key composite `(match_id, innings, overid, over_ball_num)` has **0 duplicates** across all 200,999 rows, proving 100% delivery row uniqueness.
