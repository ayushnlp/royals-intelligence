# ROYALS INTELLIGENCE — AUCTION-00 BLOCKERS REGISTER
## External Dependencies, Regulatory Uncertainty & Risk Mitigation Ledger
**Domain:** RR Auction & Retention Intelligence (Stage AUCTION-00)  
**Execution Timestamp:** 2026-11-18T07:27:30+05:30  
**Audit Status:** COMPLETE & VERIFIED

---

## 1. Executive Summary

This register tracks all critical external dependencies, regulatory circular requirements, data pack limitations, and contractual ambiguities that impact the RR Auction & Retention Intelligence workstream.

Each blocker is assigned a formal identifier, severity rating, responsible owner, analytical impact assessment, and verified mitigation strategy.

---

## 2. Comprehensive Dependency & Blocker Ledger

| Blocker ID | Domain | Severity | Description & Dependency | Impact on Pipeline | Mitigation & Contingency Strategy |
| :--- | :--- | :---: | :--- | :--- | :--- |
| **BLK-001** | Regulatory | **HIGH** | **BCCI IPL 2027 Retention Circular:** Official BCCI notification regarding total salary purse (e.g., ₹120 Cr vs ₹125 Cr), maximum retentions permitted (e.g., 5 capped + 1 uncapped vs 4+2), and Right-To-Match (RTM) rules. | Impacts AUCTION-03 salary cap deductions and AUCTION-09 RTM valuation simulation. | **Mitigation:** Implement parametric scenario modeling in AUCTION-03. Default to accepted 2025–2027 circular parameters (₹18 Cr, ₹14 Cr, ₹11 Cr, ₹4 Cr uncapped) while maintaining flexible purse sliders in UI. |
| **BLK-002** | Contractual | **MEDIUM** | **RR Contract Roster Decoupling:** Sanju Samson listed under CSK (Row 1) and Jadeja/Curran listed under RR (Rows 173–174) in `ipl_players.csv`. Actual legal player contracts are not publicly registered. | Creates uncertainty in candidate pool for AUCTION-05 retention recommendations. | **Mitigation:** Evaluate the 27 RR rows in `ipl_players.csv` as a strictly defined provisional research baseline. Clearly disclose trade assumptions and provide alternative scenario rankings excluding traded assets. |
| **BLK-003** | Data | **MEDIUM** | **Pre-2022 Senior Cap Telemetry Blindspot:** Official data pack ball-by-ball starts in 2022. Earlier senior international appearances (Test/ODI/T20I prior to 2022) cannot be verified from ball_by_ball.csv alone. | Risk of false-negative uncapped classification for veteran domestic players. | **Mitigation:** AUCTION-02 implements an independent external verification ledger cross-referenced against historical ICC debut records and BCCI match archives. |
| **BLK-004** | Telemetry | **LOW** | **Missing Ball Speed Telemetry:** 120,405 delivery rows in `ball_by_ball.csv` have null `bowl_speed` due to venue radar limitations in domestic state games. | High-pace impact metrics cannot rely purely on radar speed km/h. | **Mitigation:** AUCTION-07 bowling intelligence uses phase-level strike rates, dot ball percentages, and dismissal styles rather than raw velocity where radar data is missing. |
| **BLK-005** | Availability | **MEDIUM** | **Overseas Player NOC & National Duty:** Uncapped overseas players (e.g., South Africa, West Indies, Australia domestic players) subject to bilateral series and domestic franchise overlap. | Risk of auctioning for unavailable overseas talent. | **Mitigation:** Integrate national calendar availability checks into AUCTION-06 and AUCTION-07 candidate eligibility gates. |
| **BLK-006** | Data Pack | **INFORMATIONAL** | **Duplicate Entity Attribution:** Ravi Bishnoi registered under both RR (Row 179) and LSG (Row 261) in `ipl_players.csv`. | Risk of fragmented statistics or double-counting in auction pools. | **Mitigation:** AUCTION-01 canonical registry unifies identity under `RR-PLAYER-00179/00261` with source pointers preserved. |

---

## 3. Governance Resolution Protocol

1. **No Silent Approximations:** When regulatory or contractual parameters are unconfirmed, models must never hard-code hidden assumptions. All scenarios must be parameterized and surfaced via API flags.
2. **Conservative Eligibility Rule:** If a candidate's senior cap status remains unverified (`PENDING_VERIFICATION`), the candidate is disqualified from the uncapped target pools until verified.
3. **Escalation Path:** Contractual discrepancies are escalated to the Rajasthan Royals Analytics Steering Committee for legal verification before live war-room deployment.
