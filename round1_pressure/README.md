# ROYALS INTELLIGENCE — ROUND 1 PRESSURE ANALYSIS PACKAGE

## 1. Objective & Scope

This package (`round1_pressure/`) is a standalone, isolated analysis module within `royals-intelligence` built specifically for the **SupeRR Selector Season 2 — Round 1** challenge:

> **"Identify the Most Reliable Players Under Pressure"**

The analytical pipeline will generate two independent rankings:
1. **Top 10 Batters Under Pressure**
2. **Top 10 Bowlers Under Pressure**

The analytical methodology will use mathematical modelling, probability theory, statistics, AI/ML, Bayesian reliability, explainability, and sensitivity analysis.

---

## 2. Package Architecture

```text
round1_pressure/
├── config/
│   └── dataset_config.yaml         # Dataset paths, expected schemas, cricket rules, extras code mapping
├── data/
│   ├── raw/                        # Raw competition CSV files (strictly ignored by .gitignore)
│   ├── processed/                  # Normalized match-state Parquet tables (.gitignored)
│   │   ├── delivery_states_strict.parquet
│   │   ├── delivery_states_permissive.parquet
│   │   ├── innings_state_summary.parquet
│   │   ├── match_state_summary.parquet
│   │   ├── excluded_innings.parquet
│   │   └── reconstruction_audit.parquet
│   └── outputs/                    # QA summary JSON, validation logs, deterministic outputs
├── reports/
│   ├── data_quality_report.md      # Auto-generated comprehensive data audit and domain trap report
│   └── match_state_reconstruction_report.md # Deterministic match-state reconstruction report (R1-02)
├── src/
│   ├── __init__.py
│   ├── load_qa.py                  # Core DatasetQAEngine profiling and validation class
│   ├── 01_load_qa.py               # Executable deterministic data quality runner script
│   ├── match_state.py              # Core MatchStateEngine delivery-level state reconstruction
│   └── 02_reconstruct_match_state.py # Executable deterministic match-state reconstruction runner
├── tests/
│   ├── test_data_qa.py             # 15 focused pytest test cases validating data integrity and delivery legality
│   └── test_match_state.py         # 16 focused pytest test cases validating match-state reconstruction
├── requirements.txt                # Lightweight dependencies (pandas, numpy, pyyaml, pytest, pyarrow)
└── README.md                       # Package documentation and usage guide
```

---

## 3. Critical Cricket Domain Findings (R1-01 & R1-01.1)

1. **Extras Code Trap (`extras1_runs`):**
   - In `ball_by_ball.csv`, `extras1_runs` is a **categorical ID code** (1: Overstep, 2: wide, 3: legbyes, 4: byes, 5: other, 6: NONE, 7: Penalty), NOT a numerical run amount.
   - `runs` is strictly runs scored off the bat. Never calculate total runs as `runs + extras1_runs`.
2. **Evidence-Based Delivery Legality & Sequence Verification (R1-01.1):**
   - **Total Deliveries:** 200,999.
   - **Confirmed Legal Extras:** `legbyes` (2,748), `byes` (529), `Penalty` (1) + Standard (189,167) = **192,445**.
   - **Penalty Investigation:** Match 16753, Inn 2, Over 6, Ball 4. Exactly 6 deliveries bowled in over (`over_ball_num` 1–6). Consumed 1 legal ball without re-bowl. Confirmed Legal.
   - **Confirmed Illegal Extras:** `wide` (7,714), `Overstep` (576) = **8,290** (always re-bowled).
   - **Ambiguous Extras (`other` - 264 records):**
     - Delivery styles: 116 beamers (above waist), 72 high full tosses, 16 bouncers, 60 other.
     - Dismissals: 0 bowled, 0 caught, 0 LBW (261 NaN, 3 run outs) — proving batters cannot be caught/bowled on these deliveries under no-ball laws.
     - Sequence behavior: In 253 of 264 overs, the over reached 6 legal balls excluding `other` (re-bowled). In remaining 11 instances, the innings ended early (10 target chased mid-over, 1 Super Over).
     - Status: Retained as explicitly ambiguous rather than forcing an artificial classification.
     - Dual Metrics: **Strict Legal Total: 192,445** vs **Permissive Legal Total: 192,709** (`unresolved_deliveries_count: 264`).
3. **Bowling Attribution & Spelling Normalization:**
   - RunOuts (600), Retire Outs (6), and Obstructing the field (3) must strictly be excluded from bowler wickets and bowling averages.
   - Dataset contains typo `'Obstracting the field'` (2 records) alongside `'Obstructing the field'` (1 record); normalized to 3 total.
   - Unknown dismissal guard rejects any unlisted dismissal type from bowler wicket credit.
   - Total bowler-credited wickets: **10,272** (Bowled: 1,775, Caught: 7,557, LBW: 709, Stump: 214, Hit Wicket: 17).
4. **Super Overs:**
   - Innings 3 (25 deliveries) and Innings 4 (13 deliveries) across 6 matches are Super Overs and must be segregated from standard innings datasets.
5. **Bowling Speed Sensor Anomalies:**
   - 38.7% of deliveries have `bowl_speed == 0.0`. Implausible speeds (`-1.0` kph and up to `1456.1` kph) exist and require sensor filtering before use.
6. **Canonical `player_id` Key:**
   - Exactly 7 player names belong to multiple distinct individuals (e.g. Abdul Samad [SRH Indian batter vs Pakistani international]; Rashid Khan [Afghanistan superstar vs UAE cricketer]).
   - Never merge players on `player_name`. `player_id` is the sole canonical key.

---

## 4. Match-State Reconstruction Governance (R1-02)

1. **Dual Scenarios (Strict vs Permissive):**
   - **Scenario A (Strict):** Treats ambiguous `other` deliveries as illegal/re-bowled. Confirmed legal balls: **192,445**.
   - **Scenario B (Permissive):** Treats ambiguous `other` deliveries as legal for sensitivity analysis. Permissive legal balls: **192,709**.
   - Both scenarios are fully generated as independent Parquet tables with explicit `state_before` and `state_after` for all variables.
2. **Scope Segregation:**
   - **Primary Analysis Scope:** 193,988 deliveries across IPL (2022–2026) and Senior T20I (2022–2026) ordinary innings.
   - **Excluded Tournaments:** 30 matches (6,985 deliveries) from Emerging Teams Asia Cup 2024 and Rising Stars 2025.
   - **Excluded Super Overs:** 38 deliveries across 6 matches.
   - **Abandoned Matches:** 16 matches with 0 deliveries.
   - All exclusions are cataloged in `excluded_innings.parquet`.
3. **Score Completeness Governance:**
   - Innings with zero unconfirmed extras (or exact mathematical match) are flagged `SCORE_COMPLETE` (329 innings).
   - Innings with unconfirmed extras (byes, legbyes, penalty) are flagged `SCORE_INCOMPLETE` (1,395 innings).
   - Valid partial metrics (batter runs, bowler wickets, balls bowled, balls remaining) are fully preserved without fabricating synthetic runs.
4. **Chase & DLS Rules:**
   - 23 matches with official revised DLS targets use the verified `revised_target` from `matches.csv`.
   - Ordinary 2nd innings use `target = first_innings_total + 1`.
   - 34 shortened matches use verified scheduled balls (e.g. 30, 48, 66, 90 balls).

---

## 5. Execution & Verification Commands

### Run Data QA (R1-01.1):
```bash
python round1_pressure/src/01_load_qa.py
pytest round1_pressure/tests/test_data_qa.py -v
```

### Run Match-State Reconstruction (R1-02):
```bash
python round1_pressure/src/02_reconstruct_match_state.py
pytest round1_pressure/tests/test_match_state.py -v
```

### Run Full Test Suite:
```bash
pytest round1_pressure/tests -v
```
