# ROYALS INTELLIGENCE — ROUND 1 PRESSURE DETECTION & SITUATION CLASSIFICATION REPORT
**Generated:** 2026-11-10T22:53:50.461633+00:00  
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

## 3. Threshold Selection Rationale & Empirical Benchmarks

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

## 4. Coverage Summary (Recommended Definitions)

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

## 5. Strict vs. Permissive Sensitivity Analysis

The 259 ambiguous `other` deliveries in the primary scope were evaluated across Scenario A (Strict, treated as re-bowled/illegal) and Scenario B (Permissive, treated as legal):
- **Scenario A (Strict) Batting Pressure Events:** 34,342 deliveries.
- **Scenario B (Permissive) Batting Pressure Events:** 34,342 deliveries.
- **Net Batting Difference:** 0 deliveries (< 0.05% variance).
- **Scenario A (Strict) Bowling Pressure Events:** 40,686 deliveries.
- **Scenario B (Permissive) Bowling Pressure Events:** 40,768 deliveries.
- **Net Bowling Difference:** 82 deliveries (< 0.05% variance).
The sensitivity analysis demonstrates that the ambiguous `other` deliveries do not materially alter pressure exposure classifications.

---

## 6. Score Uncertainty Handling & Dimensions Preserved

In strict compliance with the R1-02.3 downstream governance contract:
- **Zero Invented Targets:** The 4 unresolved DLS matches (20182, 23674, 24822, 28334) retain `target_source = 'DLS_METHOD_UNRECORDED_TARGET'`; exact RRR is strictly withheld (`null`).
- **Lower-Bound Score Protection:** In all 107,083 lower-bound primary deliveries, exact RRR is withheld (`null`), but valid structural dimensions (`PHASE`, `BALLS_REM`, `WKTS_REM`, `LEGAL_BALLS`) are fully preserved.
- **Provenanced Audit Fields:** Every output record in the pressure events Parquet files includes explicit `dimensions_available` and `dimensions_withheld` strings for complete auditing.

---

## 7. Limitations & Recommendations for Subsequent Tasks

### Known Limitations:
1. **Exact Chase Coverage:** Only 6,748 of 91,934 chase deliveries have exact score tracking due to unconfirmed extras in matches without official innings score sheets. While score-independent metrics provide full coverage, exact chase demand is measurable only on the exact subset.
2. **Sensor Speed Gaps:** Bowler release speed is missing on 38.7% of deliveries and should remain a secondary telemetry feature rather than a core pressure determinant.

### Recommendations for Task R1-04 (Expected Performance Baselines):
1. Use `is_bat_composite_high` (33,005 deliveries) and `is_bowl_composite_high` (39,436 deliveries) as the primary pressure exposure definitions.
2. Retain `BAT_CHASE_RRR_P85` and `BOWL_DEFEND_TIGHT_DEATH_P85` as specialized high-leverage chase benchmarks for sensitivity testing.
3. Construct player baseline performance (expected runs, expected wickets, boundary rate) under ordinary situations before calculating pressure deltas.

---

## 8. Output Artifacts Generated

- `round1_pressure/data/processed/batting_pressure_events_strict.parquet`: 200,999 delivery rows with batting pressure candidate flags and situational metrics.
- `round1_pressure/data/processed/bowling_pressure_events_strict.parquet`: 200,999 delivery rows with bowling pressure candidate flags and situational metrics.
- `round1_pressure/data/processed/batting_pressure_events_permissive.parquet`: Permissive scenario batting pressure events.
- `round1_pressure/data/processed/bowling_pressure_events_permissive.parquet`: Permissive scenario bowling pressure events.
- `round1_pressure/data/processed/pressure_definition_comparison.parquet`: Comprehensive profiling of all candidate definitions across disciplines.
- `round1_pressure/data/processed/pressure_coverage_summary.parquet`: Detailed coverage breakdowns by tournament tier, phase, innings, and score completeness.
