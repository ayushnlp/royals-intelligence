# ROYALS INTELLIGENCE — ROUND 1 PRESSURE DETECTION & SITUATION CLASSIFICATION REPORT
**Generated:** 2026-11-18T17:00:06.421024+00:00  
**Architecture:** ROYALS INTELLIGENCE v4.1  
**Task:** R1-03 — Pressure Detection and Situation Classification Engine  
**Status:** `PRESSURE_DETECTION_VALIDATED_AND_BENCHMARKED`  

---

## 1. Executive Summary

- **Primary Scope Deliveries Analyzed:** 193,988 deliveries across IPL (2022–2026) and Senior T20I (2022–2026).
- **Batting Pressure Deliveries (Recommended `BAT_COMPOSITE_HIGH`):** 33,005 deliveries (17.01% of primary scope).
- **Batting Player Coverage:** 692 unique batters evaluated under pressure across 794 matches.
- **Bowling Pressure Deliveries (Recommended `BOWL_COMPOSITE_HIGH`):** 39,436 deliveries (20.33% of primary scope).
- **Bowling Player Coverage:** 480 unique bowlers evaluated under pressure across 822 matches.
- **Discipline Independence:** Batting and bowling pressure situations are modeled independently and asymmetric to reflect true cricket mechanics.
- **Separation of Exposure & Outcome:** Pressure detection uses state *before* delivery only; boundary, dot, or wicket outcomes are strictly decoupled from situational classification.
- **Strict Score Uncertainty Adherence:** Exact RRR is computed only on verified exact states (6,748 deliveries); lower-bound scores and unresolved DLS targets strictly withhold exact metrics.

---

## 2. Mathematical Framework & Candidate Definitions

### Core Methodological Principles:
1. **Empirical Quantile Benchmarking:** Rather than choosing arbitrary cutoffs (e.g. 10 or 12 RRR), candidate thresholds are explicitly anchored to empirical percentiles across all 193,988 primary deliveries.
2. **Dual-Layer Architecture:**
   - **Score-Dependent Layer (Exact Chase):** Operates on the subset of 2nd innings deliveries where exact cumulative team scores and verified targets exist.
   - **Score-Independent Structural Layer:** Operates across all 193,988 deliveries using robust structural invariants (phase transitions, legal balls bowled, wickets lost, and wickets in hand).
3. **Score Uncertainty Protection (R1-02.3 Contract):** When an innings score is `LOWER_BOUND_ONLY`, `runs_required_exact` and `required_run_rate_exact` are withheld (`null`). Lower-bound scores are never treated as exact scores.

### Candidate Definitions Comparison Table:

| Discipline | Definition ID | Threshold Level | Scope Dependency | Deliveries | Scope % | Matches | Players | Status |
| :--- | :--- | :--- | :--- | ---: | ---: | ---: | ---: | :--- |
| **BATTING** | `BAT_CHASE_RRR_P75` | P75 | `EXACT_REQUIRED` | 1,679 | 0.9% | 51 | 138 | `SENSITIVITY_ALTERNATIVE` |
| **BATTING** | `BAT_CHASE_RRR_P85` | P85 | `EXACT_REQUIRED` | 1,011 | 0.5% | 32 | 104 | `RECOMMENDED_CHASE_COMPONENT` |
| **BATTING** | `BAT_CHASE_RRR_P90` | P90 | `EXACT_REQUIRED` | 656 | 0.3% | 26 | 72 | `SENSITIVITY_ALTERNATIVE` |
| **BATTING** | `BAT_COLLAPSE_EARLY_W2` | MODERATE | `INDEPENDENT` | 12,216 | 6.3% | 631 | 357 | `SENSITIVITY_ALTERNATIVE` |
| **BATTING** | `BAT_COLLAPSE_EARLY_W3` | HIGH | `INDEPENDENT` | 3,797 | 2.0% | 336 | 256 | `RECOMMENDED_STRUCTURAL_COMPONENT` |
| **BATTING** | `BAT_DEPLETED_WICKETS_W4` | MODERATE | `INDEPENDENT` | 23,085 | 11.9% | 724 | 597 | `SENSITIVITY_ALTERNATIVE` |
| **BATTING** | `BAT_DEPLETED_WICKETS_W3` | HIGH | `INDEPENDENT` | 12,921 | 6.7% | 619 | 508 | `RECOMMENDED_STRUCTURAL_COMPONENT` |
| **BATTING** | `BAT_DEATH_ACCEL_W5` | HIGH | `INDEPENDENT` | 26,130 | 13.5% | 774 | 640 | `RECOMMENDED_STRUCTURAL_COMPONENT` |
| **BATTING** | `BAT_COMPOSITE_MODERATE` | MODERATE | `INDEPENDENT` | 53,137 | 27.4% | 824 | 768 | `SENSITIVITY_ALTERNATIVE` |
| **BATTING** | `BAT_COMPOSITE_HIGH` | HIGH | `INDEPENDENT` | 33,005 | 17.0% | 794 | 692 | `RECOMMENDED_PRIMARY` |
| **BATTING** | `BAT_COMPOSITE_EXTREME` | EXTREME | `INDEPENDENT` | 12,628 | 6.5% | 631 | 543 | `SENSITIVITY_ALTERNATIVE` |
| **BOWLING** | `BOWL_DEFEND_TIGHT_DEATH_P75` | P75 | `EXACT_REQUIRED` | 220 | 0.1% | 14 | 31 | `SENSITIVITY_ALTERNATIVE` |
| **BOWLING** | `BOWL_DEFEND_TIGHT_DEATH_P85` | P85 | `EXACT_REQUIRED` | 148 | 0.1% | 14 | 28 | `RECOMMENDED_CHASE_COMPONENT` |
| **BOWLING** | `BOWL_DEFEND_TIGHT_DEATH_P90` | P90 | `EXACT_REQUIRED` | 103 | 0.1% | 10 | 18 | `SENSITIVITY_ALTERNATIVE` |
| **BOWLING** | `BOWL_ASSAULT_HIGH_WICKETS_MID` | MODERATE | `INDEPENDENT` | 42,065 | 21.7% | 801 | 493 | `SENSITIVITY_ALTERNATIVE` |
| **BOWLING** | `BOWL_ASSAULT_HIGH_WICKETS_DEATH` | HIGH | `INDEPENDENT` | 17,373 | 9.0% | 667 | 394 | `RECOMMENDED_STRUCTURAL_COMPONENT` |
| **BOWLING** | `BOWL_DEATH_FINAL18` | HIGH | `INDEPENDENT` | 24,729 | 12.8% | 811 | 423 | `RECOMMENDED_STRUCTURAL_COMPONENT` |
| **BOWLING** | `BOWL_DEATH_FINAL12` | EXTREME | `INDEPENDENT` | 15,744 | 8.1% | 807 | 372 | `SENSITIVITY_ALTERNATIVE` |
| **BOWLING** | `BOWL_PP_DAMAGE_CONTROL_W0` | HIGH | `INDEPENDENT` | 4,860 | 2.5% | 443 | 265 | `RECOMMENDED_STRUCTURAL_COMPONENT` |
| **BOWLING** | `BOWL_COMPOSITE_MODERATE` | MODERATE | `INDEPENDENT` | 48,106 | 24.8% | 827 | 499 | `SENSITIVITY_ALTERNATIVE` |
| **BOWLING** | `BOWL_COMPOSITE_HIGH` | HIGH | `INDEPENDENT` | 39,436 | 20.3% | 822 | 480 | `RECOMMENDED_PRIMARY` |
| **BOWLING** | `BOWL_COMPOSITE_EXTREME` | EXTREME | `INDEPENDENT` | 23,125 | 11.9% | 808 | 420 | `SENSITIVITY_ALTERNATIVE` |

---

## 3. Audit & Reconciliation Invariants (R1-03.1 Targeted Audit)

### A. Primary Delivery Population Reconciliation:

| Population Segment | Strict Scenario | Permissive Scenario | Scope Status | Filtering & Denominator Logic |
| :--- | ---: | ---: | :--- | :--- |
| **Total Raw Deliveries** | 200,999 | 200,999 | `ALL_DELIVERIES` | Full raw `ball_by_ball.csv` dataset. |
| **Emerging Tournaments (comps 2670, 3289)** | 6,985 | 6,985 | `EXCLUDED` | Asian Cricket Council Emerging / Rising Stars tournaments. |
| **Senior Super Overs (inns 3, 4)** | 26 | 26 | `EXCLUDED` | Ties in IPL / T20I matches (5 in comp 2542, 10 in 2725, 7 in 3133, 4 in 3298). |
| **Total Excluded Deliveries** | 7,011 | 7,011 | `EXCLUDED` | Comprises 6,985 emerging balls + 26 senior super over balls. |
| **Total Primary Scope Deliveries Bowled** | 193,988 | 193,988 | `PRIMARY_TOTAL` | 200,999 - 7,011. All deliveries bowled in primary ordinary innings. |
| **Primary Legal Deliveries** | 185,692 | 185,951 | `PRIMARY_LEGAL` | Strict: excludes 259 `other` extras; Permissive: includes 259 `other`. |
| **Primary Illegal Deliveries** | 8,296 | 8,037 | `PRIMARY_ILLEGAL` | Strict: 7,720 wides + 576 oversteps; Permissive: 7,461 wides + 576 oversteps. |
| **Generated Event Parquet Rows** | 200,999 | 200,999 | `SAVED_OUTPUT` | Full row-level parity maintained with `is_primary_scope` flags. |

### B. Score Completeness & Chase Demand Reconciliation:

| Metric / Subpopulation | Deliveries | Unique Matches | Denominator | RRR Availability & Provenance |
| :--- | ---: | ---: | :--- | :--- |
| **Primary Scope Total** | 193,988 | 837 | Primary Scope | Overall primary analysis baseline. |
| **Innings 1 Deliveries** | 102,054 | 837 | Primary Scope | Target & RRR not applicable to 1st innings. |
| - *Inn 1 EXACT score* | 45,536 | 827 | Innings 1 | Zero unconfirmed extras in innings. |
| - *Inn 1 LOWER_BOUND_ONLY score* | 56,518 | 687 | Innings 1 | Contains unconfirmed byes/legbyes/penalties. |
| **Innings 2 Deliveries (Chases)** | 91,934 | 815 | Primary Scope | Chase scoring demand evaluated where exact. |
| - *Inn 2 EXACT score* | 41,369 | 802 | Innings 2 | Exact team total available. |
| - *Inn 2 LOWER_BOUND_ONLY score* | 50,565 | 660 | Innings 2 | Exact team total withheld (`null`). |
| **Innings 2 Target Classifications:** | | | | |
| - *FIRST_INNINGS_EXACT_PLUS_ONE* | 14,555 | 131 | Innings 2 | Inn 1 score exact; target is verified exact. |
| - *DLS_REVISED_TARGET* | 1,641 | 23 | Innings 2 | Official revised target from `matches.csv`. |
| - *FIRST_INNINGS_LOWER_BOUND_PLUS_ONE* | 75,400 | 657 | Innings 2 | Inn 1 had unconfirmed extras; target is lower bound. |
| - *DLS_METHOD_UNRECORDED_TARGET* | 338 | 4 | Innings 2 | Unresolved DLS matches; target strictly withheld. |
| **Exact Chase Deliveries (RRR Available)** | **6,748** | **51** | Innings 2 | Both target exact AND current score exact (6,175 + 573). |
| **Exact Chase Metrics Withheld** | **187,240** | **837** | Primary Scope | 193,988 - 6,748 (All non-exact-chase deliveries). |

### C. Batting Composite Set-Overlap Analysis (`BAT_COMPOSITE_HIGH`):

The recommended primary batting definition is rigorously defined by 4 components:
$$\text{BAT\_COMPOSITE\_HIGH} = \text{CHASE\_P85} \lor \text{COLLAPSE\_W3} \lor \text{DEPLETED\_W3} \lor \text{DEATH\_ACCEL\_W5}$$

| Component / Intersection | Deliveries | Unique Matches | Unique Batters | Overlap Description |
| :--- | ---: | ---: | ---: | :--- |
| $C_1$: `BAT_COLLAPSE_EARLY_W3` | 3,797 | 336 | 256 | Powerplay with >= 3 wickets lost. |
| $C_2$: `BAT_DEPLETED_WICKETS_W3` | 12,921 | 619 | 508 | Middle/Death with <= 3 wickets in hand. |
| $C_3$: `BAT_CHASE_RRR_P85` | 1,011 | 32 | 104 | Exact chase with RRR >= 13.0. |
| $C_4$: `BAT_DEATH_ACCEL_W5` | 26,130 | 774 | 640 | Death overs (16-20) with <= 5 wickets in hand. |
| $C_1 \cap C_2$ (Collapse & Depleted) | 0 | 0 | 0 | Disjoint phases (Powerplay vs Middle/Death). |
| $C_1 \cap C_3$ (Collapse & Chase) | 23 | 4 | 7 | Severe early collapse in steep exact chase. |
| $C_1 \cap C_4$ (Collapse & Death) | 0 | 0 | 0 | Disjoint phases (Powerplay vs Death). |
| $C_2 \cap C_3$ (Depleted & Chase) | 194 | 22 | 47 | Depleted tail in steep exact chase. |
| $C_2 \cap C_4$ (Depleted & Death) | 10,465 | 599 | 496 | Death overs with <= 3 wickets in hand. |
| $C_3 \cap C_4$ (Chase & Death) | 300 | 25 | 60 | High RRR chase in death overs. |
| $C_2 \cap C_3 \cap C_4$ (3-Way) | 128 | 18 | 36 | Death chase with RRR >= 13.0 & <= 3 wickets in hand. |
| **Exact Union (Inclusion-Exclusion)** | **33,005** | **794** | **692** | $\sum S_1 (43,859) - \sum S_2 (10,982) + \sum S_3 (128) - S_4 (0)$. |
| - *Union in Death Phase* | 26,185 | 774 | 642 | 60.19% of death phase deliveries. |
| - *Union in Powerplay Phase* | 3,924 | 337 | 262 | 6.42% of powerplay phase deliveries. |
| - *Union in Middle Phase* | 2,896 | 326 | 280 | 3.24% of middle phase deliveries. |

### D. Bowling Composite Set-Overlap Analysis (`BOWL_COMPOSITE_HIGH`):

The recommended primary bowling definition is rigorously defined by 4 components:
$$\text{BOWL\_COMPOSITE\_HIGH} = \text{ASSAULT\_DEATH} \lor \text{FINAL18} \lor \text{PP\_W0} \lor \text{DEF\_P85}$$

| Component / Intersection | Deliveries | Unique Matches | Unique Bowlers | Overlap Description |
| :--- | ---: | ---: | ---: | :--- |
| $B_1$: `BOWL_ASSAULT_HIGH_WICKETS_DEATH` | 17,373 | 667 | 394 | Death overs with >= 6 batting wickets in hand. |
| $B_2$: `BOWL_DEATH_FINAL18` | 24,729 | 811 | 423 | Overs 18-20 (final 18 scheduled balls). |
| $B_3$: `BOWL_PP_DAMAGE_CONTROL_W0` | 4,860 | 443 | 265 | Powerplay overs 5-6 with 0 wickets taken. |
| $B_4$: `BOWL_DEFEND_TIGHT_DEATH_P85` | 148 | 14 | 28 | Death chase defending target with RRR <= 8.5. |
| $B_1 \cap B_2$ (Assault & Final18) | 7,535 | 585 | 363 | Final 18 balls against conserved batting wickets. |
| $B_1 \cap B_3$ (Assault & PP) | 0 | 0 | 0 | Disjoint phases (Death vs Powerplay). |
| $B_1 \cap B_4$ (Assault & Defend) | 134 | 14 | 28 | Defending tight margin with >= 6 wickets in hand. |
| $B_2 \cap B_3$ (Final18 & PP) | 0 | 0 | 0 | Disjoint phases (Death vs Powerplay). |
| $B_2 \cap B_4$ (Final18 & Defend) | 49 | 10 | 17 | Final 18 balls defending tight margin. |
| $B_3 \cap B_4$ (PP & Defend) | 0 | 0 | 0 | Disjoint phases (Powerplay vs Death). |
| $B_1 \cap B_2 \cap B_4$ (3-Way) | 44 | 10 | 17 | Final 18 balls defending tight margin vs set lineup. |
| **Exact Union (Inclusion-Exclusion)** | **39,436** | **822** | **480** | $\sum S_1 (47,110) - \sum S_2 (7,718) + \sum S_3 (44) - S_4 (0)$. |
| - *Union in Death Phase* | 34,576 | 821 | 467 | 79.48% of death phase deliveries. |
| - *Union in Powerplay Phase* | 4,860 | 443 | 265 | 7.95% of powerplay phase deliveries. |
| - *Union in Middle Phase* | 0 | 0 | 0 | Middle phase assault quarantined to moderate candidate. |

---

## 4. Threshold Selection Rationale & Empirical Benchmarks

### Batting Situations:
- **Chase Scoring Demand:** In 2nd innings exact chases (6,748 deliveries), median RRR is 9.64. The 75th percentile is 11.48 RRR, the 85th percentile is 12.99 RRR, and the 90th percentile is 14.35 RRR. We benchmark `P75` at >= 11.5 RRR, `P85` at >= 13.0 RRR, and `P90` at >= 14.5 RRR.
- **Top-Order Collapse:** Across 61,117 Powerplay deliveries, 0 wickets lost occurs 50.4% of the time, 1 wicket lost occurs 29.6%, 2 wickets lost occurs 13.8%, and >= 3 wickets lost occurs in only 6.2% of deliveries. Losing >= 3 wickets in the Powerplay represents severe fragility (top 6.2% most pressured starts).
- **Wicket Depletion:** In Middle and Death overs, median wickets remaining is 7 (Middle) and 5 (Death). Batting with <= 3 wickets in hand occurs in only 9.7% of middle/death deliveries, representing imminent risk of innings termination.
- **Death Phase Acceleration:** Overs 16–20 with <= 5 wickets in hand (26,130 deliveries) filters out low-pressure death chases where 6+ wickets remain and victory is virtually assured.

### Bowling Situations:
- **Defending Tight Target at Death:** Bowling in overs 16–20 where chasing team requires <= 8.5 RRR with >= 5 wickets in hand (148 deliveries). The bowler has a razor-thin margin for error; every boundary conceded heavily favors the batting side.
- **Assault Against Conserved Wickets:** Bowling when the batting lineup has conserved wickets (Death overs with >= 6 wickets in hand; 17,373 deliveries). Batters attack with zero preservation constraints, maximizing boundary threat against the bowler.
- **Death Final Overs (Overs 18–20):** Bowling the final 18 balls of an innings (24,729 deliveries) where batters are committed to swinging on every delivery.
- **Powerplay Defensive Damage Control:** Bowling overs 5–6 of the Powerplay when the opposing opening partnership is intact (4,860 deliveries).

---

## 5. Coverage Summary (Recommended Definitions)

| Dimension | Dimension Value | Batting Pressured Delivs | Batting % | Batting Players | Bowling Pressured Delivs | Bowling % | Bowling Players |
| :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| **Tournament Tier** | Senior T20I | 19,175 | 18.0% | 550 | 20,359 | 19.1% | 384 |
| **Tournament Tier** | IPL | 13,830 | 15.8% | 297 | 19,077 | 21.8% | 218 |
| **Innings** | 1 | 16,860 | 16.5% | 542 | 23,468 | 23.0% | 396 |
| **Innings** | 2 | 16,145 | 17.6% | 592 | 15,968 | 17.4% | 385 |
| **Innings Phase** | POWERPLAY | 3,924 | 6.4% | 262 | 4,860 | 8.0% | 265 |
| **Innings Phase** | MIDDLE | 2,896 | 3.2% | 280 | 0 | 0.0% | 0 |
| **Innings Phase** | DEATH | 26,185 | 60.2% | 642 | 34,576 | 79.5% | 467 |
| **Score Completeness** | EXACT | 8,685 | 10.0% | 448 | 10,426 | 12.0% | 331 |
| **Score Completeness** | LOWER_BOUND_ONLY | 24,320 | 22.7% | 649 | 29,010 | 27.1% | 448 |

---

## 6. Strict vs. Permissive Sensitivity Analysis

The 259 ambiguous `other` deliveries in the primary scope (and 5 out-of-scope records) were evaluated across Scenario A (Strict legality: treated as re-bowled/illegal per sequence evidence) and Scenario B (Permissive legality: treated as legal):

### Primary Analysis Scope (Denominator = 193,988 Deliveries):
- **Scenario A (Strict) Batting Pressure:** 33,005 deliveries (17.01%, 692 unique batters).
- **Scenario B (Permissive) Batting Pressure:** 33,005 deliveries (17.01%, 692 unique batters).
- **Net Batting Difference:** 0 deliveries (**0.000% variance**; 100% invariant).
- **Scenario A (Strict) Bowling Pressure:** 39,436 deliveries (20.33%, 480 unique bowlers).
- **Scenario B (Permissive) Bowling Pressure:** 39,516 deliveries (20.37%, 480 unique bowlers).
- **Net Bowling Difference:** 80 deliveries (**0.041% variance**; < 0.1% threshold).

### Full Dataset Scope (Denominator = 200,999 Records, including Emerging & Super Overs):
- **Strict Batting:** 34,342 vs **Permissive Batting:** 34,342 (Diff = 0).
- **Strict Bowling:** 40,686 vs **Permissive Bowling:** 40,768 (Diff = 82).

### Event-Level Sensitivity Investigation:
All 80 differing bowling deliveries in the primary scope occur strictly on cumulative legal ball boundary transitions: (1) 72 deliveries in Over 17 where treating earlier `other` deliveries as legal decrements `balls_remaining_before` from 19 to 18, triggering `BOWL_DEATH_FINAL18` one ball earlier; and (2) 8 deliveries in Over 4 (5th over) where `legal_balls_bowled_before` increments from 23 to 24 with 0 wickets lost, triggering `BOWL_PP_DAMAGE_CONTROL_W0` one ball earlier. Batting pressure evaluates `innings_phase == 'DEATH'` based strictly on `overid >= 16`, resulting in complete zero variance across all 193,988 deliveries. This proves extreme structural robustness of both classifications.

---

## 7. Score Uncertainty Handling & Dimensions Preserved

In strict compliance with the R1-02.3 downstream governance contract:
- **Zero Invented Targets:** The 4 unresolved DLS matches (20182, 23674, 24822, 28334) retain `target_source = 'DLS_METHOD_UNRECORDED_TARGET'`; exact RRR is strictly withheld (`null`).
- **Lower-Bound Score Protection:** In all 107,083 lower-bound primary deliveries, exact RRR is withheld (`null`), but valid structural dimensions (`PHASE`, `BALLS_REM`, `WKTS_REM`, `LEGAL_BALLS`) are fully preserved.
- **Provenanced Audit Fields:** Every output record in the pressure events Parquet files includes explicit `dimensions_available` and `dimensions_withheld` strings for complete auditing.

---

## 8. Limitations & Recommendations for Subsequent Tasks

### Known Limitations:
1. **Exact Chase Coverage:** Only 6,748 of 91,934 chase deliveries have exact score tracking due to unconfirmed extras in matches without official innings score sheets. While score-independent metrics provide full coverage, exact chase demand is measurable only on the exact subset.
2. **Sensor Speed Gaps:** Bowler release speed is missing on 38.7% of deliveries and should remain a secondary telemetry feature rather than a core pressure determinant.

### Recommendations for Task R1-04 (Expected Performance Baselines):
1. Use `is_bat_composite_high` (33,005 deliveries) and `is_bowl_composite_high` (39,436 deliveries) as the primary pressure exposure definitions.
2. Retain `BAT_CHASE_RRR_P85` and `BOWL_DEFEND_TIGHT_DEATH_P85` as specialized high-leverage chase benchmarks for sensitivity testing.
3. Construct player baseline performance (expected runs, expected wickets, boundary rate) under ordinary situations before calculating pressure deltas.

---

## 9. Output Artifacts Generated

- `round1_pressure/data/processed/batting_pressure_events_strict.parquet`: 200,999 delivery rows with batting pressure candidate flags and situational metrics.
- `round1_pressure/data/processed/bowling_pressure_events_strict.parquet`: 200,999 delivery rows with bowling pressure candidate flags and situational metrics.
- `round1_pressure/data/processed/batting_pressure_events_permissive.parquet`: Permissive scenario batting pressure events.
- `round1_pressure/data/processed/bowling_pressure_events_permissive.parquet`: Permissive scenario bowling pressure events.
- `round1_pressure/data/processed/pressure_definition_comparison.parquet`: Comprehensive profiling of all candidate definitions across disciplines.
- `round1_pressure/data/processed/pressure_coverage_summary.parquet`: Detailed coverage breakdowns by tournament tier, phase, innings, and score completeness.
