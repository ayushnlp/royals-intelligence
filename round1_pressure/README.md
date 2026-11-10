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
│   ├── processed/                  # Normalized match-state & pressure delivery tables (.gitignored)
│   └── outputs/                    # QA summary JSON, validation logs, deterministic outputs
├── reports/
│   └── data_quality_report.md      # Auto-generated comprehensive data audit and domain trap report
├── src/
│   ├── __init__.py
│   ├── load_qa.py                  # Core DatasetQAEngine profiling and validation class
│   └── 01_load_qa.py               # Executable deterministic data quality runner script
├── tests/
│   └── test_data_qa.py             # 11 focused pytest test cases validating data integrity
├── requirements.txt                # Lightweight dependencies (pandas, numpy, pyyaml, pytest)
└── README.md                       # Package documentation and usage guide
```

---

## 3. Critical Cricket Domain Findings (R1-01)

1. **Extras Code Trap (`extras1_runs`):**
   - In `ball_by_ball.csv`, `extras1_runs` is a **categorical ID code** (1: Overstep, 2: wide, 3: legbyes, 4: byes, 5: other, 6: NONE, 7: Penalty), NOT a numerical run amount.
   - `runs` is strictly runs scored off the bat. Never calculate total runs as `runs + extras1_runs`.
2. **Legal Deliveries (`over_ball_num`):**
   - `over_ball_num` is a sequential delivery counter that reaches up to 13 in overs with illegal deliveries.
   - A delivery is legal iff `extras_type not in ['wide', 'Overstep', 'other']` (or `extras1_runs not in [1, 2, 5]`).
3. **Bowling Attribution:**
   - RunOuts (600), Retire Outs (6), and Obstructing the field (3) must strictly be excluded from bowler wickets and bowling averages.
4. **Super Overs:**
   - Innings 3 (25 deliveries) and Innings 4 (13 deliveries) across 6 matches are Super Overs and must be segregated from standard innings datasets.
5. **Bowling Speed Sensor Anomalies:**
   - 38.7% of deliveries have `bowl_speed == 0.0`. Implausible speeds (`-1.0` kph and up to `1456.1` kph) exist and require sensor filtering before use.
6. **Canonical `player_id` Key:**
   - Exactly 7 player names belong to multiple distinct individuals (e.g. Abdul Samad [SRH Indian batter vs Pakistani international]; Rashid Khan [Afghanistan superstar vs UAE cricketer]).
   - Never merge players on `player_name`. `player_id` is the sole canonical key.

---

## 4. How to Run R1-01 Data QA

### Run QA Profiling & Report Generation:
```bash
python round1_pressure/src/01_load_qa.py
```

### Run QA Test Suite:
```bash
pytest round1_pressure/tests/test_data_qa.py -v
```
