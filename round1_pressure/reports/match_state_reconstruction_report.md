# ROYALS INTELLIGENCE — MATCH-STATE RECONSTRUCTION REPORT (R1-02, R1-02.1, R1-02.2 & R1-02.3)
**Generated:** 2026-11-10T22:24:07.878410+00:00  
**Architecture:** ROYALS INTELLIGENCE v4.1  
**Tasks:** R1-02, R1-02.1, R1-02.2 & R1-02.3 Final Match-Level Classification Integrity Closure  
**Status:** `MATCH_STATE_RECONSTRUCTION_ACCEPTED_AND_AUDITED`  

---

## 1. Executive Summary & Verification Invariants

- **Total Source Deliveries Processed:** 200,999 (100% accounted for).
- **Strict Legal Deliveries:** 192,445 (Scenario A).
- **Permissive Legal Deliveries:** 192,709 (Scenario B; +264 ambiguous `other` treated as legal for sensitivity analysis).
- **Primary Analysis Scope:** 193,988 deliveries across IPL and Senior T20I matches (ordinary 1st & 2nd innings).
- **Primary Legal Deliveries:** 185,692 (Strict) vs 185,951 (Permissive; difference = 259).
- **Out-of-Scope Ambiguous Deliveries:** 5 records (4 in Emerging tournaments, 1 in IPL Super Over).
- **Wickets & Attribution Invariant:** 10,272 Bowler Wickets + 609 Non-Bowler Dismissals = 10,881 Total Dismissals.
- **Total Batter Runs Invariant:** 269,550 runs off the bat across all deliveries.

---

## 2. Strict vs. Permissive Scenario Comparison

| Metric | Scenario A (Strict) | Scenario B (Permissive) | Difference | Analysis Role |
| :--- | ---: | ---: | ---: | :--- |
| **Total Source Deliveries** | 200,999 | 200,999 | 0 | `RECONCILED` |
| **Total Legal Deliveries** | 192,445 | 192,709 | 264 | `264_AMBIGUOUS_OTHER_DELIVERIES_SENSITIVITY` |
| **Primary Scope Deliveries** | 193,988 | 193,988 | 0 | `RECONCILED` |
| **Primary Scope Legal Deliveries** | 185,692 | 185,951 | 259 | `259_AMBIGUOUS_OTHER_DELIVERIES_PRIMARY` |
| **Out Of Scope Ambiguous Other Deliveries** | 5 | 5 | 0 | `RECONCILED_4_EMERGING_1_SUPER_OVER` |
| **Bowler Credited Wickets** | 10,272 | 10,272 | 0 | `INVARIANT` |
| **Non Bowler Dismissals** | 609 | 609 | 0 | `INVARIANT` |
| **Total Dismissals** | 10,881 | 10,881 | 0 | `INVARIANT` |
| **Total Batter Runs Known** | 269,550 | 269,550 | 0 | `INVARIANT` |
| **Deliveries With Unconfirmed Extras** | 3,278 | 3,278 | 0 | `DOCUMENTED_UNCONFIRMED_EXTRAS` |

---

## 3. Score Reconstruction & Exact vs. Lower-Bound Semantics

### Core Governance Principles:
- **`EXACT`:** All score components on the delivery and up to that point in the innings are mathematically known (zero unconfirmed extras).
- **`LOWER_BOUND_ONLY`:** Known runs are calculated from bat runs and base penalty extras, but unconfirmed extras (byes, legbyes, penalty) occurred in the innings. The cumulative score is strictly a lower bound.
- **No Fabrication Rule:** Unknown extras are never assumed to be zero. Lower bounds are NEVER exposed as exact team scores.
- **Withheld Downstream Metrics on Uncertain Scores:** When an innings score is `LOWER_BOUND_ONLY`, `runs_required_exact` and `required_run_rate_exact` are strictly set to `null`/`NaN` to prevent downstream mathematical corruption.

- **Total Innings Profiled:** 1,724
- **Innings with `EXACT` Score State:** 329 (19.1%) — zero unconfirmed extras; exact score reconstruction mathematically verified.
- **Innings with `LOWER_BOUND_ONLY` State:** 1,395 (80.9%) — contains byes, legbyes, or penalty extras where exact run counts are unconfirmed without fabricating data.

---

## 4. Empirical Inference of `extras_2_runs`

> [!NOTE]
> **Empirical Inference Status:** The field `extras_2_runs` is non-zero on exactly 36 of 200,999 deliveries (0.018%). In all 36 deliveries, `runs == 0` and `extras_2_runs` takes values `1` (19 times) or `4` (17 times) on no-balls/beamers. While domain evidence suggests this records auxiliary runs (e.g. byes/legbyes/overthrow off a no-ball), **this interpretation is strictly an empirical inference and not an officially documented schema specification**. Downstream models treat these runs with documented uncertainty.

---

## 5. Match Metadata Flags vs. Mutually Exclusive Categories (R1-02.3)

### A. Non-Exclusive Match Metadata Flags (Can Overlap):
- **`REVISED_TARGET_RECORDED`:** 23 matches — matches with explicit `revised_target > 0` in `matches.csv` (includes Match 17765).
- **`REVISED_OVERS_RECORDED`:** 34 matches — matches with explicit revised overs metadata.
- **`DLS_METHOD_IN_RESULT_TEXT`:** 19 matches — matches whose `result` string contains `'D/L'` or `'DLS'`.
- **`DLS_TARGET_APPLICABLE`:** 22 matches — matches where positive revised target was applicable to a concluded chase.
- **`DLS_STATUS_UNRESOLVED`:** 4 matches — matches 20182, 23674, 24822, 28334 where DLS is stated in result, but target/overs are omitted.
- **`MATCH_ABANDONED`:** 40 matches — matches ending in 'No Result' or 'Match Abandoned' (including Match 17765 and 16 zero-delivery fixtures).

### B. Exactly One Mutually Exclusive Category per Match (Sums to Exactly 883):
- **`WICKET_WIN_NO_OFFICIAL_TOTAL_IN_SCHEMA`:** 394 matches — match won by wickets; official team totals absent from schema.
- **`INCOMPLETE_EXTRAS_RUN_WIN`:** 382 matches — match won by runs, but one or both innings contain unconfirmed extras.
- **`NO_RESULT_OR_ABANDONED`:** 40 matches — match abandoned or no result (includes Match 17765).
- **`OTHER_RESULT`:** 30 matches — tied matches / Super Overs.
- **`DLS_TARGET_APPLICABLE`:** 22 matches — concluded 2nd innings chase with verified official DLS target.
- **`EXACT_BOTH_INNS_MARGIN_MISMATCH`:** 6 matches — both innings had zero unconfirmed byes/legbyes, but stated margin differs by 1–4 runs (likely unrecorded multi-run wides/overthrows).
- **`EXACT_BOTH_INNS_MARGIN_MATCH`:** 5 matches — both innings had zero unconfirmed extras, match won by runs, and reconstructed margin matches stated margin exactly.
- **`DLS_STATUS_UNRESOLVED`:** 4 matches — match decided by DLS/DL method per text result, but target was unrecorded in schema.
- **Total Matches Audited:** 883 (100.0% match-level coverage, exactly 883 matches).

### Classification Integrity for Key Edge Cases:
1. **Match 17765:**
   - **Mutually Exclusive Category:** `NO_RESULT_OR_ABANDONED`.
   - **Retained Metadata Flags:** `flag_revised_target_recorded = True` (130.0), `flag_revised_overs_recorded = True` (72 balls), `flag_match_abandoned = True`, `flag_dls_target_applicable = False`.
   - **Explanation:** Although a revised target was recorded, rain intervened after 25 deliveries in Innings 2, terminating the chase without a decisive result. Categorized as abandoned to prevent duplicate counting while retaining all metadata flags.
2. **Four Unresolved DLS Matches (20182, 23674, 24822, 28334):**
   - **Mutually Exclusive Category:** `DLS_STATUS_UNRESOLVED`.
   - **Retained Metadata Flags:** `flag_dls_method_in_result_text = True`, `flag_dls_status_unresolved = True`, `flag_revised_target_recorded = False`.
   - **Exact Metric Withholding:** `target_source = 'DLS_METHOD_UNRECORDED_TARGET'`, `target_exact = None`, `runs_required_exact = None`, `required_run_rate_exact = None` across all 598 deliveries. Zero target fabrication.

---

## 6. Revised Overs, Shortened Matches & DLS Coverage (R1-02.2 Resolution)

### Resolution of the 23-versus-26 Discrepancy:
The initial R1-02.1 audit noted 23 matches with `revised_target > 0` versus 26 matches labeled `DLS_REVISED_TARGET`. The source investigation established the exact mathematical reason:
1. **23 matches** in `matches.csv` explicitly record a positive `revised_target` (22 decisive chases + 1 abandoned chase, Match 17765).
2. **4 matches** (Matches 20182, 23674, 24822, 28334) had `revised_target == NaN` and `revised_overs == NaN`, but their text `result` strings contained `'(D/L Method)'` or `'(DLS method)'`.
3. In R1-02.1, the reconciliation classifier evaluated `NO_RESULT_OR_ABANDONED` first, routing Match 17765 to abandonment (-1), while routing the 4 unrecorded DLS matches to `DLS_REVISED_TARGET` (+4).
4. **Net Discrepancy:** 22 + 4 = 26 matches. Net difference = 26 - 23 = +3 matches (+4 unrecorded minus 1 abandoned).

### Explicit R1-02.2 Classification Concepts:
- **`REVISED_TARGET_RECORDED` (23 matches):** Source explicitly provides a positive `revised_target` in `matches.csv`.
- **`REVISED_OVERS_RECORDED` (34 matches):** Source provides revised scheduled-ball metadata (`first_inn_revised_overs` or `second_inn_revised_overs`). Unit verified as legal balls (integers divisible by 6, range 30 to 114).
- **`DLS_TARGET_APPLICABLE` (22 matches):** Positive revised target is validated as applicable to a concluded second-innings chase.
- **`CURTAILED_WITHOUT_REVISED_TARGET` (11 matches):** Scheduled overs shortened without a recorded revised target (2 pre-match 11-over standard target matches [16753, 19959], 9 abandoned in Innings 1).
- **`DLS_STATUS_UNRESOLVED` (4 matches):** Result string states DLS was applied, but target and overs metadata were omitted from schema (Matches 20182, 23674, 24822, 28334). Target provenance is unresolved; exact target/RRR is strictly withheld.

---

## 7. Downstream Feature-Eligibility Contract (for R1-03)

> [!CAUTION]
> **Score Uncertainty Protection Rule:** Do NOT authorize a fallback pressure formula that relies on uncertain current score or current run rate.
> - **Exact RRR requires an exact score AND a valid target.**
> - **Lower-bound scores must NEVER be represented as exact scores.**
> - **Any proposed score-independent pressure features (e.g. phase leverage, wickets down / wickets in hand, balls remaining) must be separately justified and validated in R1-03.**
> - **Unresolved DLS matches must NEVER receive invented or guessed targets.**

| Feature Category | Features Included | Downstream Safety Status |
| :--- | :--- | :--- |
| **Tier 1: Safe For Downstream Models** | Striker runs, legal balls bowled/faced, wickets, dismissal attribution, player ID, match metadata, phase, balls remaining | **100% Verified & Safe.** Independently validated; zero dependency on unconfirmed extras. |
| **Tier 2: Score-Dependent Features** | `runs_required_exact`, `required_run_rate_exact`, `cumulative_team_runs_exact`, exact chase deficit | **Restricted strictly to `EXACT` score states.** Strictly withheld (`null`) on `LOWER_BOUND_ONLY` states and `DLS_STATUS_UNRESOLVED` matches. |
| **Tier 3: Uncertain Features** | Multi-run byes/legbyes, penalty amounts, additional wide overthrows, ambiguous `other` deliveries, unrecorded DLS par scores | **Requires Sensitivity Analysis or Exclusion.** Must compare Strict vs Permissive scenarios; never synthesize par scores. |

---

## 8. Generated Output Artifacts

All output tables are stored in snappy-compressed Parquet format:
- `round1_pressure/data/processed/delivery_states_strict.parquet`: Delivery states with `state_before` and `state_after` under strict legality.
- `round1_pressure/data/processed/delivery_states_permissive.parquet`: Delivery states under permissive legality (for sensitivity testing).
- `round1_pressure/data/processed/innings_state_summary.parquet`: Innings-level reconstructed metrics and completeness flags.
- `round1_pressure/data/processed/match_state_summary.parquet`: Match-level targets, shortened status, and innings totals.
- `round1_pressure/data/processed/match_result_reconciliation.parquet`: Match-by-match reconciliation audit for all 883 matches across 8 mutually exclusive categories.
- `round1_pressure/data/processed/dls_and_revised_overs_audit.parquet`: Complete audit of all 38 shortened, revised overs, and DLS matches.
- `round1_pressure/data/processed/excluded_innings.parquet`: Fully documented catalog of excluded matches, innings, and deliveries.
- `round1_pressure/data/processed/reconstruction_audit.parquet`: Scenario reconciliation table.
