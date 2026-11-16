# ROYALS INTELLIGENCE — DATASET-TO-FEATURE COMPATIBILITY MATRIX
**Document Version:** 1.0 (Rebaselined)  
**Authoritative Data Source:** Official Rajasthan Royals Round 1 Data Pack (`data/raw/rajasthan_royals/round_1_data_pack/`)  
**Scope:** Evaluation of 26 Planned Platform Features across Stages 0 through 13  
**Status:** Canonical Reference for Roadmap Rebaselining  

---

## 1. COMPATIBILITY CLASSIFICATION SYSTEM

Every planned platform capability is audited against the empirical fields of the official Rajasthan Royals dataset and categorized into one of three strict operational statuses:

1. **`FULLY SUPPORTED`**: Can be 100% computed, modeled, and exposed using exclusively the supplied 6 relational CSV files with zero external dependencies or synthetic assumptions.
2. **`PARTIALLY SUPPORTED`**: Core cricket aggregations are supported by the dataset, but complete execution requires documented external APIs (e.g., Open-Meteo CC-BY 4.0) or domain business heuristics (e.g., T20I appearance heuristic for uncapped status).
3. **`UNSUPPORTED / BLOCKED`**: Necessary telemetry or data fields are completely absent from the supplied data pack. Under the platform's Anti-Fabrication Governance Rule, these capabilities must NOT be mocked with synthetic numbers or unverified external scraping during competition execution.

---

## 2. 26-FEATURE COMPATIBILITY LEDGER

| # | Feature / Analytical Capability | Target Stage | Source CSV & Column Mappings | Compatibility Status | Data Governance Notes & Implementation Constraints |
| :---: | :--- | :---: | :--- | :---: | :--- |
| **01** | **Ball-by-Ball Ingestion & Pipeline** | Stage 1 | `ball_by_ball.csv` (all 33 cols) | **FULLY SUPPORTED** | 200,999 deliveries across 867 matches. Validated natural key `(match_id, innings, overid, over_ball_num)`. |
| **02** | **Competition & Tournament Directory** | Stage 1 | `competitions.csv` (`comp_id`, `comp_name`, `match_format`, `season`) | **FULLY SUPPORTED** | 141 tournaments (134 T20I, 7 T20 leagues including IPL 2022–2026). |
| **03** | **Franchise & Squad Participation** | Stage 1/2 | `teams.csv` (`comp_id`, `team_id`, `team_name`) | **FULLY SUPPORTED** | 38 unique team entities mapped to tournament appearances. |
| **04** | **Match Context & Progression** | Stage 3 | `matches.csv` (`match_id`, `venue_id`, `toss_opted`, `result`) | **FULLY SUPPORTED** | 883 matches with toss, venue, stage, captains, and revised DLS overs/targets. |
| **05** | **Canonical Player Identity Resolution** | Stage 2 | `competition_team_player_mapping.csv` (`player_id`, `player_name`) | **FULLY SUPPORTED** | 1,217 canonical player IDs resolved to official names with 100% referential integrity. |
| **06** | **Powerplay Phase Mastery (Overs 1–6)** | Stage 5 | `ball_by_ball.csv` (`overid` $\le 6$, `runs`, `is_wicket`, `is_four`, `is_six`) | **FULLY SUPPORTED** | 53,504 Powerplay deliveries. Computes strike rates, dot %, boundary %, and early wicket survival. |
| **07** | **Middle Overs Spin/Pace Control (7–15)** | Stage 5 | `ball_by_ball.csv` (`overid` $7..15$, `pace_or_spin`, `runs`) | **FULLY SUPPORTED** | 93,126 Middle overs deliveries. Evaluates strike rotation, boundary control, and spin squeeze. |
| **08** | **Death Overs Execution & Acceleration (16–20)** | Stage 5 | `ball_by_ball.csv` (`overid` $\ge 16$, `runs`, `stroke`, `delivery_style`) | **FULLY SUPPORTED** | 54,369 Death overs deliveries. Granular execution under high scoring pressure. |
| **09** | **Handedness Matchup Splits (RHB/LHB vs Pace/Spin)** | Stage 5/6 | `ball_by_ball.csv` (`batting_type`, `pace_or_spin`) | **FULLY SUPPORTED** | 131,006 RHB and 69,993 LHB balls. Perfect matrix cross-referencing against Pace (123,886) and Spin (77,113). |
| **10** | **Granular Bowling Sub-Disciplines** | Stage 5 | `ball_by_ball.csv` (`bowling_type`) | **FULLY SUPPORTED** | 12 distinct styles (Right-arm Leg-Break, Right-arm Fast, Slow left-arm orthodox, etc.). |
| **11** | **Shot Stroke Efficiency & Dismissal Risk** | Stage 5 | `ball_by_ball.csv` (`stroke`, `runs`, `is_wicket`) | **FULLY SUPPORTED** | 30 tactical strokes (Pull shot, Cover Drive, Flick, Scoop, Reverse Sweep, etc.). 96.9% complete. |
| **12** | **Delivery Variation & Seam/Spin Style** | Stage 5 | `ball_by_ball.csv` (`delivery_style`) | **FULLY SUPPORTED** | 34 styles (Seamed In, Slower Ball, Leg Break, Googly, Off Cutter, Inswing, etc.). 99.8% complete. |
| **13** | **Bowling Angle Tactics (Over vs Around)** | Stage 5 | `ball_by_ball.csv` (`over_or_around`) | **FULLY SUPPORTED** | 154,670 Over-the-wicket vs 45,922 Around-the-wicket deliveries. Angle-adjusted efficiency. |
| **14** | **Field Sector Scoring (Off-side vs On-side)** | Stage 5 | `ball_by_ball.csv` (`on_or_off`) | **FULLY SUPPORTED** | 104,875 Off-side vs 96,124 On-side deliveries. Identifies wagon-wheel side dominance. |
| **15** | **Radar Release Speed Analytics (km/h)** | Stage 5/10 | `ball_by_ball.csv` (`bowl_speed`) | **FULLY SUPPORTED** | 123,137 deliveries (61.3%) have valid radar speed. Identifies express pace ($\ge 140\text{ km/h}$) and spin release velocity. |
| **16** | **Situational Pressure Index & PRI** | Round 1 / Stage 5 | `ball_by_ball.csv` + match context (`round1_pressure`) | **FULLY SUPPORTED** | Pressure index (PI $\ge 60$) and Bayesian Player Reliability Index (PRI) fully validated in Round 1. |
| **17** | **Head-to-Head Batter vs Bowler Matchups** | Stage 6 | `ball_by_ball.csv` (`striker_id`, `bowler_id`) | **FULLY SUPPORTED** | 200,999 delivery micro-battles across 888 batters and 647 bowlers with Empirical Bayes shrinkage. |
| **18** | **Impact Player Substitution Optimization** | Stage 7 | `playing_eleven.csv` (`is_impact`, `is_impact_off`) | **FULLY SUPPORTED** | 558 sub-ins and 558 sub-outs in IPL 2023–2026. Powers batting-first vs bowling-first substitution models. |
| **19** | **Captaincy & Toss Decision Intelligence** | Stage 8 | `matches.csv` (`toss_win_team_id`, `toss_opted`, `captains`) | **FULLY SUPPORTED** | Analyzes franchise captaincy choices, venue chase biases, and toss win-to-match win conversion. |
| **20** | **Knockout vs League Phase Differential** | Stage 8 | `matches.csv` (`knock_out`, `stage`) | **FULLY SUPPORTED** | 56 playoff/knockout matches vs 827 league fixtures. Quantifies "big-match temperament". |
| **21** | **Venue Historical Scoring Trends & Par** | Stage 4 | `matches.csv` (`venue_id`) + `ball_by_ball.csv` | **FULLY SUPPORTED** | 98 grounds. Computes 1st/2nd innings par, chasing win %, pace/spin share, and phase run rates. |
| **22** | **Physical Boundary Dimensions (Meters)** | Stage 4 | Boundary blueprints / survey measurements | **UNSUPPORTED / BLOCKED** | **ABSENT from CSVs.** Stage 4 enforced strict anti-guessing rule: unmeasured venues marked `None` / `NOT_SURVEYED`. |
| **23** | **Micro-Climate Weather & Dew Telemetry** | Stage 4 | In-situ sensors / Open-Meteo CC-BY 4.0 API | **PARTIALLY SUPPORTED** | **ABSENT from CSVs.** Integrated in Stage 4 via Open-Meteo API using stadium geographic coordinates. |
| **24** | **Player Age & Development Curves** | Stage 10 | Player Date of Birth (DOB) | **UNSUPPORTED / BLOCKED** | **ABSENT from CSVs.** `playing_eleven` and `mapping` contain no DOB. Age-based curves cannot fabricate dates. |
| **25** | **Uncapped vs Capped Player Eligibility** | Stage 2/10 | International cap verification | **PARTIALLY SUPPORTED** | International appearances are verifiable via `competitions.csv` (`match_format == 'T20I'`), but official BCCI rules require external squad gazette. |
| **26** | **Auction Valuation & Purse Forecasting** | Stage 12 | Player salaries, contracts, auction bids | **UNSUPPORTED / BLOCKED** | **ABSENT from CSVs.** Strictly prohibited by competition governance rules. Excluded from core analytics. |

---

## 3. SUMMARY COMPATIBILITY AUDIT METRICS

```
+---------------------------------------------------------------------------------+
| TOTAL PLANNED PLATFORM FEATURES AUDITED: 26                                    |
+---------------------------------------------------------------------------------+
| [1] FULLY SUPPORTED (Dataset Alone):       21 features  (80.8%)                 |
| [2] PARTIALLY SUPPORTED (External API):     2 features  ( 7.7%)                 |
| [3] UNSUPPORTED / STRICTLY BLOCKED:          3 features  (11.5%)                 |
+---------------------------------------------------------------------------------+
```

### Strategic Implications for Rajasthan Royals Platform Architecture:

1. **Unprecedented Tactical Depth:**  
   The presence of `stroke` (30 shot types), `delivery_style` (34 variation styles), `over_or_around` (bowling angles), `on_or_off` (fielding sectors), and `bowl_speed` (radar velocity) provides immense analytical power. Stages 5, 6, 7, and 8 can deliver elite tactical intelligence that far exceeds standard cricket analytics platforms.

2. **Strict Anti-Fabrication Boundary:**  
   Because player dates of birth and auction salaries are completely absent, all models must strictly operate on **on-field performance metrics, experience ball counts, tactical efficiency, and empirical reliability**, completely barring synthetic salaries, arbitrary age curves, or simulated bidding wars.
