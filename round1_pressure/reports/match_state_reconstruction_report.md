# ROYALS INTELLIGENCE — MATCH-STATE RECONSTRUCTION REPORT (R1-02)
**Generated:** 2026-11-10T19:04:13.820724+00:00  
**Architecture:** ROYALS INTELLIGENCE v4.1  
**Task:** R1-02 Delivery-Level Match-State Reconstruction  
**Status:** `MATCH_STATE_RECONSTRUCTION_ACCEPTED_AND_VERIFIED`  

---

## 1. Executive Summary & Verification Invariants

- **Total Source Deliveries Processed:** 200,999 (100% accounted for).
- **Strict Legal Deliveries:** 192,445 (Scenario A).
- **Permissive Legal Deliveries:** 192,709 (Scenario B; +264 ambiguous `other` treated as legal for sensitivity analysis).
- **Primary Analysis Scope:** 193,988 deliveries across IPL and Senior T20I matches (ordinary 1st & 2nd innings).
- **Wickets & Attribution Invariant:** 10,272 Bowler Wickets + 609 Non-Bowler Dismissals = 10,881 Total Dismissals.
- **Total Batter Runs Invariant:** 269,550 runs off the bat across all deliveries.

---

## 2. Strict vs. Permissive Scenario Comparison

| Metric | Scenario A (Strict) | Scenario B (Permissive) | Difference | Analysis Role |
| :--- | ---: | ---: | ---: | :--- |
| **Total Source Deliveries** | 200,999 | 200,999 | 0 | `RECONCILED` |
| **Total Legal Deliveries** | 192,445 | 192,709 | 264 | `264_AMBIGUOUS_OTHER_DELIVERIES_SENSITIVITY` |
| **Primary Scope Deliveries** | 193,988 | 193,988 | 0 | `RECONCILED` |
| **Primary Scope Legal Deliveries** | 185,692 | 185,951 | 259 | `RECONCILED` |
| **Bowler Credited Wickets** | 10,272 | 10,272 | 0 | `INVARIANT` |
| **Non Bowler Dismissals** | 609 | 609 | 0 | `INVARIANT` |
| **Total Dismissals** | 10,881 | 10,881 | 0 | `INVARIANT` |
| **Total Batter Runs Known** | 269,550 | 269,550 | 0 | `INVARIANT` |
| **Deliveries With Unconfirmed Extras** | 3,278 | 3,278 | 0 | `DOCUMENTED_UNCONFIRMED_EXTRAS` |

---

## 3. Score Reconstruction & Extras Reconciliation

- **Total Innings Profiled:** 1,724
- **Innings with `SCORE_COMPLETE`:** 329 (19.1%) — zero unconfirmed extras; exact score reconstruction mathematically verified.
- **Innings with `SCORE_INCOMPLETE`:** 1,395 (80.9%) — contains byes, legbyes, or penalty extras where exact run counts are unconfirmed without fabricating data.
- **Governance Rule:** Incomplete score state is explicitly flagged. Valid partial metrics (batter runs, bowler wickets, balls bowled, balls remaining, overs) are retained; no synthetic runs are added to force match result matches.

---

## 4. Revised Targets, Shortened Matches & DLS Coverage

- **Matches with Revised DLS Targets:** 23 matches.
- **Shortened Matches (Scheduled Balls < 120):** 34 matches (rain-curtailed, e.g. 5, 8, 11, 15 overs a side).
- **Target Formulation (2nd Innings):**
  - DLS Revised Target matches: `target = revised_target` (from `matches.csv`).
  - Standard 2nd Innings: `target = first_innings_total + 1`.
  - `runs_required = max(0, target - score_before)`.
  - `required_run_rate = (runs_required / (balls_remaining / 6.0))` (protected against division by zero).

---

## 5. Excluded Records and Scope Segregation

| Exclusion Category | Matches / Innings Count | Deliveries Count | Causal Reason & Scope Policy |
| :--- | ---: | ---: | :--- |
| **Abandoned Matches** | 16 matches | 0 | Abandoned without a ball bowled (weather/ground conditions). |
| **Emerging Tournaments** | 30 matches | 6,985 | Mens T20 Emerging Teams Asia Cup 2024 & Rising Stars 2025 excluded from primary Tier-1 IPL/T20I scope per Section 9. |
| **Super Overs** | 6 matches (12 innings) | 38 | Innings 3 and 4 segregated from ordinary 20-over match models. |

---

## 6. Generated Output Artifacts

All output tables are stored in snappy-compressed Parquet format:
- `round1_pressure/data/processed/delivery_states_strict.parquet`: Delivery states with `state_before` and `state_after` under strict legality.
- `round1_pressure/data/processed/delivery_states_permissive.parquet`: Delivery states under permissive legality (for sensitivity testing).
- `round1_pressure/data/processed/innings_state_summary.parquet`: Innings-level reconstructed metrics and completeness flags.
- `round1_pressure/data/processed/match_state_summary.parquet`: Match-level targets, shortened status, and innings totals.
- `round1_pressure/data/processed/excluded_innings.parquet`: Fully documented catalog of excluded matches, innings, and deliveries.
- `round1_pressure/data/processed/reconstruction_audit.parquet`: Scenario reconciliation table.
