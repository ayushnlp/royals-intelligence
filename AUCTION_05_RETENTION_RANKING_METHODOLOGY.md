# ROYALS INTELLIGENCE — AUCTION-05 RETENTION RANKING METHODOLOGY
## Multi-Dimensional Retention Decision Engine for Rajasthan Royals

**Document Version:** 1.0.0  
**Phase:** RR Auction & Retention Intelligence Expansion  
**Stage:** `AUCTION-05` — Retention Ranking Engine  
**Git Baseline Branch:** `main` | **HEAD:** `0f24302c61e3d4c070d0e669fc152830c9b2c4e1`  
**Execution Timestamp:** 2026-11-17T01:42:00+05:30  
**Status:** IMPLEMENTED, AUDITED & 100% GREEN

---

## 1. Executive Summary & Objective

The objective of **AUCTION-05** is to design and implement a transparent, statistically defensible, and reproducible decision model that produces **exactly 3 Rajasthan Royals retention recommendations** from the verified eligible 2026 contracted squad baseline.

### Core Architectural Mandates:
1. **Strict Evidence Gating:** Only players possessing `pre_auction_2027_contract_status == "VERIFIED_CURRENT_CONTRACT"` are eligible for the retention ranking candidate pool ($N=11$).
2. **Quarantine of Unconfirmed Roster Members:** Active squad members whose 2027 contract extensions are not confirmed by official pre-2025 multi-year documentation ($N=14$) are quarantined under `PENDING_VERIFICATION` and excluded from the retention pool.
3. **Strict Exclusion of Traded / Released Personnel:** Traded players (Sanju Samson to CSK, Nitish Rana to DC) and pre-auction released players are strictly barred from the retention decision engine.
4. **No Mandatory Role Quotas:** The engine does not artificially force arbitrary quotas (e.g., forcing 1 pacer, 1 spinner, 1 batter); rankings are driven strictly by composite multi-dimensional asset value.
5. **No Data Fabrication:** Missing empirical attributes (e.g., bowling statistics for pure batters or age where unverified) are preserved as missing/neutral, never fabricated into false zeros.

---

## 2. Multi-Dimensional Retention Evaluation Framework

The retention decision model computes 7 independent, normalized component scores on a $[0.0, 100.0]$ scale for each eligible candidate.

$$\text{Composite Retention Score } (S_{\text{composite}}) = \sum_{k=1}^{7} w_k \cdot S_k$$

Where $\sum_{k=1}^{7} w_k = 1.00$.

| Dimension ($k$) | Name | Weight ($w_k$) | Empirical Basis & Mathematical Formulation | Provenance Source |
| :---: | :--- | :---: | :--- | :--- |
| **1** | **Player Performance & Impact ($S_{\text{perf}}$)** | $0.25$ | Empirical scoring efficiency and shrunk strike rate / economy rate relative to AUCTION-04 priors ($\mu_{0,\text{bat}}=147.35$, $\mu_{0,\text{bowl}}=9.13$ RPO). Dual-discipline all-rounders receive primary + $0.25 \times$ secondary contribution. | `normalized_batting_performance.parquet`, `normalized_bowling_performance.parquet` |
| **2** | **Squad Role Scarcity ($S_{\text{scarcity}}$)** | $0.20$ | Market scarcity in IPL auctions: Elite Indian LH top-order batter ($96.0$), Indian wicketkeeper-finisher ($95.0$), Indian batting all-rounder ($94.0$), Overseas pacer ($80.0$). | AUCTION-03 Retention Governance & Auction Market Dynamics |
| **3** | **Replacement Difficulty ($S_{\text{replace}}$)** | $0.20$ | Expected open-market bidding friction and purse volatility to acquire replacement value. Marquee assets ($98.0$, ₹18–22 Cr), High-friction assets ($92.0$–$94.0$, ₹12–17 Cr). | AUCTION-03 Salary Cap & Open-Market Bidding Simulator |
| **4** | **Squad Balance Contribution ($S_{\text{balance}}$)** | $0.15$ | Preservation of the 8-man overseas quota for tactical auction flexibility; complete Indian batting spine formation. Indian core ($93.0$–$96.0$) vs Overseas ($75.0$). | IPL Player Regulations (8 Overseas Squad / 4 Playing XI Constraint) |
| **5** | **Age & Career Stage ($S_{\text{age}}$)** | $0.05$ | T20 career value curve based strictly on verified chronological age: Peak prime window 23–26 ($96.0$–$100.0$), ascending youth 20–22 ($88.0$–$94.0$), veteran 31+ ($40.0$–$65.0$). | `canonical_player_registry.parquet` (`supplied_csv_age`) |
| **6** | **Consistency & Reliability ($S_{\text{reliability}}$)** | $0.05$ | Delivery volume across multiple tournament editions ($\ge 1000$ balls: $95.0$; $\ge 500$ balls: $88.0$; $\ge 150$ balls: $72.0$). | AUCTION-00 Delivery Database & AUCTION-04 Normalization |
| **7** | **Evidence Confidence ($S_{\text{confidence}}$)** | $0.10$ | AUCTION-04 audited confidence tiers: HIGH ($\ge 500$ balls faced or $\ge 300$ balls bowled: $100.0$), MEDIUM ($60.0$), LOW ($25.0$), NO_DATA ($0.0$). | AUCTION-04 Audited Sample Confidence Strata |

---

## 3. Mathematical Formulations of Component Scores

### 3.1 Dimension 1: Player Performance & Impact ($S_{\text{perf}}$)
For batters with $\ge 20$ legal balls:
$$S_{\text{bat}} = \text{clip}\left(50.0 + 1.5 \cdot (\text{SR}_{\text{shrunk}} - 147.35) + 1.5 \cdot (\text{BndryPct} - 18.0) - 0.5 \cdot (\text{DotPct} - 35.0), 20.0, 98.0\right)$$

For bowlers with $\ge 20$ legal balls:
$$S_{\text{bowl}} = \text{clip}\left(50.0 + 15.0 \cdot (9.13 - \text{Econ}_{\text{shrunk}}) + 1.0 \cdot (\text{DotPct} - 35.0) - 1.0 \cdot (\text{BndryConcPct} - 18.0), 20.0, 98.0\right)$$

For genuine all-rounders ($\text{Role} == \text{"All-rounder"}$ or both disciplines $\ge 60$ balls):
$$S_{\text{all-rounder}} = \text{clip}\left(\max(S_{\text{bat}}, S_{\text{bowl}}) + 0.25 \cdot \min(S_{\text{bat}}, S_{\text{bowl}}), 0.0, 100.0\right)$$

### 3.2 Dimension 5: Age & Career Stage Curve ($S_{\text{age}}$)
$$S_{\text{age}}(\text{Age}) = \begin{cases}
100.0 - 2.0 \cdot (\text{Age} - 24.0) & \text{if } 23.0 \le \text{Age} \le 26.0 \\
88.0 + 3.0 \cdot (\text{Age} - 20.0) & \text{if } 20.0 \le \text{Age} < 23.0 \\
90.0 - 4.0 \cdot (\text{Age} - 26.0) & \text{if } 26.0 < \text{Age} \le 29.0 \\
65.0 - 5.0 \cdot (\text{Age} - 30.0) & \text{if } 30.0 \le \text{Age} \le 32.0 \\
\max(40.0, 50.0 - 5.0 \cdot (\text{Age} - 32.0)) & \text{if } \text{Age} > 32.0 \\
68.0 & \text{if } \text{Age} < 20.0 \text{ (Developmental)} \\
50.0 & \text{if unverified (Neutral)}
\end{cases}$$

---

## 4. Eligible Candidate Pool Ranking Output

Executing the AUCTION-05 engine produces the following deterministic ranking for all 11 verified eligible candidates:

$$\begin{array}{|c|c|l|l|r|c|c|c|l|}
\hline
\textbf{Rank} & \textbf{ID} & \textbf{Player Name} & \textbf{Squad Role} & \textbf{Age} & \textbf{Caps} & \textbf{Composite} & \textbf{Repl. Friction} & \textbf{Recommendation Status} \\
\hline
\mathbf{1} & \mathbf{6819} & \textbf{Yashasvi Jaiswal} & \text{Batter (LH Opener)} & 24.0 & \text{CAPPED} & \mathbf{91.52} & \text{EXTREME} & \mathbf{\text{RECOMMENDED RETENTION \#1}} \\
\mathbf{2} & \mathbf{6423} & \textbf{Riyan Parag} & \text{All-rounder} & 25.0 & \text{CAPPED} & \mathbf{89.91} & \text{VERY\_HIGH} & \mathbf{\text{RECOMMENDED RETENTION \#2}} \\
\mathbf{3} & \mathbf{7260} & \textbf{Dhruv Jurel} & \text{Wicketkeeper-Batter} & 25.0 & \text{CAPPED} & \mathbf{86.30} & \text{VERY\_HIGH} & \mathbf{\text{RECOMMENDED RETENTION \#3}} \\
\hline
4 & 50284 & \text{Vaibhav Sooryavanshi} & \text{Batter (Youth)} & 15.0 & \text{CAPPED} & 82.25 & \text{LOW} & \text{Eligible Non-Retained (Auction / RTM)} \\
5 & 3297 & \text{Shimron Hetmyer} & \text{Batter (Overseas)} & 29.0 & \text{CAPPED} & 77.28 & \text{MODERATE} & \text{Eligible Non-Retained (Auction Target)} \\
6 & 3298 & \text{Jofra Archer} & \text{Bowler (Overseas)} & 31.0 & \text{CAPPED} & 75.60 & \text{HIGH} & \text{Eligible Non-Retained (Auction Target)} \\
7 & 2411 & \text{Sandeep Sharma} & \text{Bowler (Special Uncapped)} & 33.0 & \text{UNCAPPED*} & 70.03 & \text{MODERATE} & \text{Eligible Non-Retained (Auction Target)} \\
8 & 6806 & \text{Tushar Deshpande} & \text{Bowler (Pacer)} & 31.0 & \text{CAPPED} & 67.14 & \text{MODERATE} & \text{Eligible Non-Retained (Auction Target)} \\
9 & 25139 & \text{Shubham Dubey} & \text{Batter (Middle-Order)} & 32.0 & \text{UNCAPPED} & 64.62 & \text{LOW} & \text{Eligible Non-Retained (Auction Target)} \\
10 & 8580 & \text{Yudhvir Singh} & \text{All-rounder (Pace)} & 29.0 & \text{UNCAPPED} & 62.58 & \text{LOW} & \text{Eligible Non-Retained (Auction Target)} \\
11 & 26663 & \text{Kwena Maphaka} & \text{Bowler (Overseas)} & 20.0 & \text{CAPPED} & 58.65 & \text{LOW} & \text{Eligible Non-Retained (Auction Target)} \\
\hline
\end{array}$$

*\*Note on Sandeep Sharma: In AUCTION-02 senior international ledger, Sandeep Sharma is tracked under PENDING_VERIFICATION regarding historic 2015 T20I caps, but qualifies under IPL's special 5-year inactive uncapped rule. His 2027 contract is verified.*

---

## 5. Strategic Justification of Top 3 Retentions

### Recommendation #1: Yashasvi Jaiswal (ID: 6819) — Composite Score: 91.52
- **Positional Scarcity:** Elite Indian left-handed opening batter with high-pressure powerplay conversion.
- **Replacement Difficulty (EXTREME):** In an open auction, Jaiswal would attract intense bidding across 10 franchises with expected winning bid between ₹18.0 Cr and ₹22.0+ Cr.
- **Franchise Runway:** At 24.0 years old, Jaiswal provides Rajasthan Royals with a proven marquee anchor and a decade-long franchise horizon.
- **Sample Evidence:** 1,865 legal balls faced, shrunk strike rate $158.49$, boundary percentage $25.68\%$, HIGH sample confidence ($100.0/100$).

### Recommendation #2: Riyan Parag (ID: 6423) — Composite Score: 89.91
- **Positional Scarcity:** Prime Indian middle-order batter with spin bowling versatility.
- **Replacement Difficulty (VERY HIGH):** Indian batting all-rounders in their mid-20s are the rarest commodity in the IPL auction; expected open market cost ₹14.0–₹17.0 Cr.
- **Dual Impact:** Shrunk batting SR $152.61$ across 1,081 balls, combined with 260 legal balls bowled at an economy of $8.91$ RPO (superior to tournament baseline $9.13$).
- **Franchise Runway:** At 25.0 years old, Parag provides leadership continuity and core domestic stability.

### Recommendation #3: Dhruv Jurel (ID: 7260) — Composite Score: 86.30
- **Positional Scarcity:** Domestic Indian wicketkeeper-batter capable of batting #5–#7 and finishing matches under severe run-rate pressure.
- **Replacement Difficulty (VERY HIGH):** With Sanju Samson traded to CSK, retaining Jurel secures the primary wicketkeeper-finisher slot; expected auction price ₹12.0–₹15.0 Cr.
- **Sample Evidence:** 798 legal balls faced, shrunk strike rate $151.11$, HIGH sample confidence ($100.0/100$).
- **Squad Balance:** Retaining three Indian capped players leaves all 8 overseas squad slots available for targeted tactical bidding during the live auction.
