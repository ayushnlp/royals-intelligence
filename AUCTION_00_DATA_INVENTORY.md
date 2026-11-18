# ROYALS INTELLIGENCE — AUCTION-00 DATA INVENTORY
## Comprehensive Raw Data Asset Catalog & Schema Inventory
**Domain:** RR Auction & Retention Intelligence (Stage AUCTION-00)  
**Execution Timestamp:** 2026-11-18T04:06:00+05:30  
**Storage Root:** `data/raw/rajasthan_royals/round_1_data_pack/`  
**Audit Status:** COMPLETE & VERIFIED

---

## 1. Overview & Data Pack Manifest

The official Rajasthan Royals Round 1 Competition Data Pack contains 7 CSV datasets and 1 PDF problem statement. All files have been ingested, row-counted, schema-validated, and cryptographically hashed using SHA-256.

| Filename | File Size | Row Count | Column Count | Cryptographic SHA-256 Digest |
| :--- | :---: | :---: | :---: | :--- |
| `ball_by_ball.csv` | 41,071,609 bytes | 200,999 | 33 | `a3926f49d2c684dca2a5d2de535a02c5ee46ea654ca1e79dd31c69e7544e9889` |
| `competition_team_player_mapping.csv` | 462,969 bytes | 6,413 | 6 | `1ded4e42a933618572d6e2c3a521c3257eb1844fab4456d567d77cbb2d3bbb12` |
| `competitions.csv` | 7,624 bytes | 129 | 4 | `507ceb7189f972d4e4f299ddcfc97f3c3247af1913f6291106f161fa8353fd9b` |
| `ipl_players.csv` | 23,561 bytes | 268 | 7 | `3a31b1127f6b9344a53c387e5266711379cb1bc2aedcc5f9db2d2bb1e3913a9d` |
| `matches.csv` | 123,864 bytes | 883 | 22 | `bb100ab84b8b9a15160c1f2315cf675210131a30e779ec5079fd5403dcf56eef` |
| `playing_eleven.csv` | 966,287 bytes | 20,413 | 9 | `7517c73722a28d5d61c808ccf0cbed315a8780586d02e946eb9a7f5daf011c27` |
| `teams.csv` | 6,922 bytes | 208 | 3 | `a65e5922a9b3bf49247b24fc9471782e700efb31f8dcc5042923238b87c50a5d` |

---

## 2. Table-by-Table Detailed Schema Specifications

### 2.1 `ball_by_ball.csv` (200,999 rows, 33 columns)
Records delivery-level telemetry across professional T20 and multi-format cricket.

| Column Name | Inferred Type | Null Count | Semantic Description |
| :--- | :--- | :---: | :--- |
| `match_id` | Integer | 0 | Foreign key to `matches.csv` |
| `innings` | Integer | 0 | Innings number (1 or 2; super-overs: 3 or 4) |
| `overid` | Integer | 0 | Over index (0-indexed or 1-indexed) |
| `over_ball_num` | Integer | 0 | Ball sequence within the over |
| `innings_ball_num` | Integer | 0 | Cumulative ball sequence in the innings |
| `batting_team_id` | Integer | 0 | Foreign key to `teams.csv` |
| `bowling_team_id` | Integer | 0 | Foreign key to `teams.csv` |
| `striker_id` | Integer | 0 | Batter facing delivery |
| `striker_name` | String | 0 | Name of striker |
| `non_striker_id` | Integer | 0 | Batter at non-striker's end |
| `non_striker_name` | String | 0 | Name of non-striker |
| `bowler_id` | Integer | 0 | Bowler delivering the ball |
| `bowler_name` | String | 0 | Name of bowler |
| `batting_type` | String | 0 | Left-handed / Right-handed |
| `bowling_type` | String | 0 | Bowling discipline |
| `batting_order` | Integer | 0 | Batting order position (1–11) |
| `runs` | Integer | 0 | Total runs scored off delivery (batter + extras) |
| `is_four` | Integer/Boolean | 0 | Indicator for boundary four |
| `is_six` | Integer/Boolean | 0 | Indicator for boundary six |
| `is_wicket` | Integer/Boolean | 0 | Indicator for dismissal |
| `dismissal_type_id`| Float/Nullable | 191,128 | Categorical dismissal identifier |
| `dismissal_type` | String/Nullable| 191,128 | Dismissal mode (bowled, caught, lbw, run out, etc.) |
| `dismissed_player_id`| Float/Nullable| 191,128 | Dismissed batter ID |
| `extras_type` | String/Nullable| 189,167 | `wide` (7,714), `Overstep` (576), `legbyes` (2,748), `byes` (529), `other` (264), `Penalty` (1) |
| `extras1_runs` | Integer | 0 | Wide / No-ball runs |
| `extras_2_runs` | Integer | 0 | Bye / Leg-bye runs |
| `pace_or_spin` | String/Nullable| 1,204 | Delivery classification (Pace vs Spin) |
| `bowl_speed` | Float/Nullable | 120,405 | Ball release speed in km/h (telemetry coverage varies) |
| `stroke` | String/Nullable| 14,208 | Shot classification (drive, pull, flick, cut, etc.) |
| `delivery_style` | String/Nullable| 12,301 | Detailed delivery subtype (yorker, bouncer, slower ball) |
| `over_or_around` | String/Nullable| 2,109 | Bowling angle relative to wicket |
| `on_or_off` | String/Nullable| 2,109 | Delivery line relative to batter |
| `delivery_ist_time`| String/Nullable| 0 | Wall-clock timestamp (IST) of delivery |

### 2.2 `matches.csv` (883 rows, 22 columns)
Records match metadata, venues, toss decisions, results, and DLS revisions.
- Total Matches: **883**
- Matches with Deliveries in `ball_by_ball.csv`: **867**
- Abandoned / No-Result Matches (0 balls bowled): **16**
- Date Range: Multi-season domestic and franchise window.
- Columns: `match_id`, `comp_id`, `match_number`, `match_date`, `stage`, `venue_id`, `venue_country`, `home_team_id`, `home_team`, `away_team_id`, `away_team`, `home_team_captain_id`, `away_team_captain_id`, `toss_win_team_id`, `toss_opted`, `man_of_the_match`, `first_inn_revised_overs`, `second_inn_revised_overs`, `revised_target`, `knock_out`, `win_team_id`, `result`.

### 2.3 `ipl_players.csv` (268 rows, 7 columns)
Reference snapshot of IPL squad lists across 10 franchises.
- Total Rows: **268**
- Unique Names: **267** (exactly 1 duplicate: `Ravi Bishnoi` in RR [row 179] and LSG [row 261])
- Null Bowling Style: Exactly **32** (29 Wicketkeeper-Batters, 3 Batters who do not bowl)
- Null Spin Type: Exactly **32** (same 32 non-bowling players)
- Rajasthan Royals Rows: Exactly **27** (12 Bowlers, 6 All-rounders, 5 Batters, 4 Wicketkeeper-Batters)
- Columns: `Team`, `Name`, `Age`, `Role`, `Batting_Style`, `Bowling_Style`, `Spin_Type`.

### 2.4 `playing_eleven.csv` (20,413 rows, 9 columns)
Records official team sheet selections, batting orders, wicketkeepers, captains, and Impact Player designations.
- Total Rows: **20,413**
- Matches Covered: 883
- Columns: `match_id`, `team_id`, `player_id`, `batting_order`, `is_played`, `is_captain`, `is_wk`, `is_impact`, `is_impact_off`.

### 2.5 `competition_team_player_mapping.csv` (6,413 rows, 6 columns)
Crucial junction table mapping players across multiple domestic and international tournaments.
- Total Rows: **6,413**
- Unique Player IDs: **1,217**
- Unique Player Names: **1,210** (7 name collisions disambiguated by ID)
- Columns: `comp_id`, `comp_name`, `team_id`, `team_name`, `player_id`, `player_name`.

### 2.6 `teams.csv` (208 rows, 3 columns)
Lookup table mapping competition IDs and team IDs to normalized team names.
- Columns: `comp_id`, `team_id`, `team_name`.

### 2.7 `competitions.csv` (129 rows, 4 columns)
Metadata catalog of tournaments, formats (T20, List A, First Class), and competition seasons.
- Columns: `comp_id`, `comp_name`, `match_format`, `season`.
