# ROYALS INTELLIGENCE — AUCTION-00 DATA AVAILABILITY MATRIX
## Cross-Module Data Availability, Verification State & Provenance Registry (Final Corrected Version)
**Domain:** RR Auction & Retention Intelligence (Stage AUCTION-00)  
**Execution Timestamp:** 2026-11-16T22:30:00+05:30  
**Target Modules:** Module A (RR Retention), Module B (Uncapped Batters), Module C (Uncapped Bowlers)  
**Governance Standard:** Zero Fabricated Records | Explicit Provenance Classification

---

## 1. Classification Taxonomy

Every data dimension required for the Auction & Retention Intelligence platform is evaluated and assigned an authoritative state:

* **`VERIFIED`:** Ground truth exists within the official repository, protected Parquet artifacts, or sealed Round 1 data pack; fully validated with 100% confidence.
* **`PARTIALLY AVAILABLE`:** Present for a subset of the candidate universe (e.g. IPL players within 2022–2026 data pack) but absent for overseas or regional domestic leagues.
* **`MISSING`:** Entirely absent from local datasets; no file or column provides this attribute.
* **`REQUIRES EXTERNAL VERIFICATION`:** Cannot be inferred safely from internal data without corroboration from official governing body records (ICC, BCCI, national boards).

---

## 2. Comprehensive Data Availability Matrix

| Analytical Dimension | Data Field(s) | Module A: RR Retention | Module B: Uncapped Batters | Module C: Uncapped Bowlers | Authoritative In-Repo Source | Status Classification | Remediation / Verification Strategy |
| :--- | :--- | :---: | :---: | :---: | :--- | :--- | :--- |
| **Player Identity & Naming** | `player_id`, `canonical_name`, `source_name` | Mandatory | Mandatory | Mandatory | `competition_team_player_mapping.csv`, `ipl_players.csv` | **VERIFIED** | 91.4% direct string match; canonical deduplication via Player Identity Service. |
| **Player Nationality** | `country`, `is_indian`, `overseas_board` | Mandatory | Mandatory | Mandatory | Inferred from national team rows in mapping CSV; absent as explicit column | **PARTIALLY AVAILABLE** | 66 Indian and 196 Overseas players verified via national team rows; remaining 227 require board confirmation. |
| **Current RR Squad Membership** | `team_name`, `is_active_rr_squad` | Mandatory | Reference | Reference | `ipl_players.csv` (Rows 163–189: 27 rows) | **PARTIALLY AVAILABLE** | Listed in CSV, but dislocated from historical reality. **Must be confirmed via official BCCI retention circulars.** |
| **Historical IPL Performance** | Deliveries, Runs, Wickets, Phases, SR, Econ | Mandatory | Mandatory | Mandatory | `ball_by_ball.csv` (41 MB), `matches.csv` (883 matches) | **VERIFIED** | **200,999 total deliveries (192,709 legal deliveries, 8,290 non-legal delivery records (7,714 wides + 576 no-balls))** across 883 matches (867 with delivery logs). |
| **Domestic T20 Performance** | SMAT stats, Regional T20 leagues (UP, TNPL) | Optional | Critical | Critical | Absent from Round 1 CSV pack (only IPL & T20I included) | **MISSING** | Ingest verified SMAT / domestic T20 match records or evaluate on IPL sample with Bayesian shrinkage. |
| **Overseas Franchise Performance** | BBL, SA20, Hundred, CPL, PSL stats | Optional | Critical | Critical | Absent from Round 1 CSV pack | **MISSING** | Ingest Cricsheet Open franchise leagues for overseas uncapped candidates; apply provisional CQF normalization. |
| **Senior International Cap History** | Test, ODI, T20I appearances | Mandatory | Sovereign Gate | Sovereign Gate | Partially inferred (2022–2026 matches only in CSV pack) | **REQUIRES EXTERNAL VERIFICATION** | Matches from 2022–2026 provide positive caps. **Pre-2022 caps are NOT covered and require ICC/BCCI debut registry audit.** |
| **Age & Date of Birth** | `age`, `dob`, `dob_source` | Mandatory | Mandatory | Mandatory | `ipl_players.csv` (`Age` integer present); DOB absent | **PARTIALLY AVAILABLE** | Integer age available for 268 IPL players; exact DOB requires BCCI domestic birth registry. |
| **Auction Registration Status** | `is_registered_ipl_2027`, `auction_set` | Reference | Sovereign Gate | Sovereign Gate | Absent from all internal datasets | **REQUIRES EXTERNAL VERIFICATION** | Must query official IPL 2027 Auction Registered Player Longlist/Shortlist. Default to `PENDING`. |
| **Release & Retention Status** | `is_retained`, `is_released`, `rtm_eligible` | Mandatory | Critical | Critical | Absent from all internal datasets | **REQUIRES EXTERNAL VERIFICATION** | Must query official BCCI Retention & Release circular. Mark as `UNCONFIRMED_PENDING_CIRCULAR`. |
| **NOC & Overseas Availability** | `noc_status`, `available_window`, `bilateral_clash` | Critical | Critical | Critical | Absent from all internal datasets | **REQUIRES EXTERNAL VERIFICATION** | Must cross-reference ICC Future Tours Programme (FTP) and national board NOC releases. |
| **Salary & Auction Valuation** | `historical_price`, `retention_bracket`, `bid_ceiling` | Mandatory | Mandatory | Mandatory | Contract salaries absent from Round 1 pack | **REQUIRES EXTERNAL VERIFICATION** | Model economic valuation using historical archetype wage benchmarks; never fabricate official salaries. |
| **Role & Tactical Attributes** | `batting_style`, `bowling_style`, `spin_type` | Mandatory | Mandatory | Mandatory | `ipl_players.csv`, `ball_by_ball.csv` (telemetry) | **VERIFIED** | 100% verified across 268 players in CSV; empirical stroke and variation distribution verified. |

---

## 3. Four Decoupled Roster & Contract Concepts for Retention

To maintain rigorous governance, the retention module decouples the candidate universe into four distinct conceptual layers:

1. **Supplied CSV Franchise Association:** The 27 players registered under `Team == "Rajasthan Royals"` in `ipl_players.csv` (exploratory reference dataset only).
2. **Historical RR Association:** Players who represented RR in 2022–2024 match scorecards. Does not prove active contract status. Do not classify historical RR core as current legal squad without contract evidence.
3. **Verified Current RR Squad Membership:** Legally contracted cricketers on Rajasthan Royals' official squad as registered with BCCI for the current cycle. **This forms the sole authoritative candidate universe for final retention decisions.**
4. **Contract & Retention Status:** Formal retention declarations submitted to the IPL Governing Council (Retained under Slot 1/2/3 deduction brackets or Released).

---

## 4. Senior International Cap Verification Protocols

Historical match coverage from 2022–2026 is **strictly insufficient** to certify all-time uncapped status because legends and senior players capped before 2022 (e.g. MS Dhoni, Ambati Rayudu, Robin Uthappa, Nathan Bracken, Jaydev Unadkat) have zero international appearances in the 2022–2026 dataset.

The engine establishes four immutable certification states:
* **`VERIFIED_UNCAPPED`:** Ground-truth evidence confirms exactly 0 appearances in Men's Test, 0 in Men's ODI, and 0 in Men's T20I cricket across their entire career.
* **`VERIFIED_CAPPED`:** Positive evidence confirms $\ge 1$ appearance in Men's Test, ODI, or T20I cricket. Disqualified from uncapped shortlists.
* **`PENDING_VERIFICATION`:** Career debut logs are incomplete or external registries have not yet been queried. Retained in the pending review pool; excluded from Top 10.
* **`CONFLICTING_EVIDENCE`:** Discrepancy between two authoritative sources (e.g., identity collision with another player of the same name). Flagged for manual audit.

### Independent Verification Procedure for Test, ODI, and T20I:
1. **Test Match Verification:** Query ICC and national board Test Cap Registries. Any appearance as an XI member or designated concussion substitute who batted/bowled constitutes a Test cap.
2. **ODI Match Verification:** Query ICC and national board ODI Cap Registries. Appearance in an official ICC Men's ODI constitutes an ODI cap.
3. **T20I Match Verification:** Query ICC Men's T20I Cap Registries. Involves cross-referencing bilateral series and ICC Men's T20 World Cups.
4. **U19 and 'A' Team Boundary:** Under-19 World Cup matches and unofficial 'A' team tour fixtures **do NOT constitute senior international caps**.

---

## 5. Execution Policy for Missing Attributes

1. **Strict Anti-Fabrication Rule:** Zero synthetic records. Under no circumstance may the engine invent dates of birth, international debut dates, retention prices, or NOC approvals.
2. **Fallback to Explicit State Flags:**
   - When DOB is absent: Display integer age from `ipl_players.csv` accompanied by `Age Verification: Integer Roster Reference (Exact DOB Pending Registry)`.
   - When Auction Registration is unannounced: Flag as `Auction Registration: Pending Official IPL 2027 Longlist`.
   - When Retention Circular is unreleased: Flag as `Contract Status: Unconfirmed Roster Association`.
3. **Audit Trail Mandate:** Every candidate record must store an immutable JSON evidence block recording the source, verification date, and status for each matrix dimension.
