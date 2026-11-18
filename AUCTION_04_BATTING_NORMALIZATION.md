# ROYALS INTELLIGENCE — AUCTION-04 BATTING NORMALIZATION
## Independent Batting Performance Normalization & Phase Profile Report

**Document Version:** 1.0.0  
**Phase:** RR Auction & Retention Intelligence Expansion  
**Stage:** `AUCTION-04` — Historical Performance & Competition Normalization  
**Git Baseline Branch:** `main` | **HEAD:** `0f24302c61e3d4c070d0e669fc152830c9b2c4e1`  
**Execution Timestamp:** 2026-11-17T00:27:00+05:30  
**Status:** INDEPENDENT BATTING PROFILES COMPUTED & PERSISTED

---

## 1. Executive Summary & Batting Domain Scope

In accordance with strict AUCTION-04 guidelines, batting performance is modeled as an **independent, self-contained analytical domain**. It is never blended with bowling metrics into a composite player score.

### 1.1 Universe Scale:
- **Total Batters Evaluated:** **888 unique canonical players** with batting delivery records in `ball_by_ball.csv`.
- **Sample-Qualified Batters:** **564 players** meeting the minimum sample qualification threshold ($\ge 30$ legal balls faced).
- **High-Confidence Sample:** **284 players** with $\ge 200$ legal balls faced.

---

## 2. Statistical Metric Definitions & Mathematical Formulas

$$\begin{array}{|l|l|l|}
\hline
\textbf{Batting Metric} & \textbf{Notation} & \textbf{Mathematical Formulation \& Operational Definition} \\
\hline
\textbf{Raw Strike Rate} & \text{SR}_{\text{raw}} & \text{SR}_{\text{raw}} = \frac{\text{Runs}}{\text{Legal Balls Faced}} \times 100.0 \\
\hline
\textbf{Batting Average} & \text{Avg}_{\text{raw}} & \text{Avg}_{\text{raw}} = \frac{\text{Runs}}{\text{Dismissals}} \quad (\text{if Dismissals } > 0, \text{ else } \text{None}) \\
\hline
\textbf{Boundary Frequency} & \text{Bnd}\% & \text{Bnd}\% = \frac{\text{Fours} + \text{Sixes}}{\text{Legal Balls Faced}} \times 100.0 \\
\hline
\textbf{Dot Ball Frequency} & \text{Dot}\% & \text{Dot}\% = \frac{\text{Legal Balls with 0 Runs}}{\text{Legal Balls Faced}} \times 100.0 \\
\hline
\textbf{Comp-Weighted SR} & \text{SR}_{\text{comp}} & \text{SR}_{\text{comp}} = \frac{\sum_{k} \text{Runs}_k \times (1 / w_{\text{score}, k})}{\text{Legal Balls Faced}} \times 100.0 \\
\hline
\textbf{Shrunk Strike Rate} & \text{SR}_{\text{shrunk}} & \text{SR}_{\text{shrunk}} = \left(\frac{N}{N + 60}\right) \text{SR}_{\text{comp}} + \left(\frac{60}{N + 60}\right) 147.35 \\
\hline
\textbf{Scoring Efficiency} & \text{Eff}_{\text{norm}} & \text{Eff}_{\text{norm}} = \left(\frac{\text{SR}_{\text{shrunk}}}{147.35}\right) \times 100.0 \\
\hline
\end{array}$$

---

## 3. Phase-Specific Batting Decomposition

Every batter's profile includes deterministic splits across T20 game phases:
1. **Powerplay (Overs 0–5):** Field restrictions (2 fielders outside 30-yard circle). Evaluates boundary generation through the infield and aerial powerplay utilization.
2. **Middle Overs (Overs 6–14):** Field spread (5 fielders out). Evaluates strike rotation, spin-hitting efficiency, and low dot-ball maintenance.
3. **Death Overs (Overs 15–19):** High-risk acceleration phase. Evaluates boundary hitting against yorkers and slower balls under maximum pressure.

---

## 4. Stratified Player Profile Audits (Representative Cohort)

The table below audits a representative sample across Rajasthan Royals contracted candidates, audited uncapped domestic talents, and international benchmarks:

| Canonical ID | Player Name | Legal Balls | Runs | Raw SR | Boundary \% | Dot \% | Shrunk SR | Scoring Eff | Conf Tier | Qualified |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **6819** | Yashasvi Jaiswal | 2,148 | 3,312 | 154.19 | 22.86% | 34.12% | **153.92** | 104.46% | `HIGH` | **YES** |
| **6423** | Riyan Parag | 982 | 1,462 | 148.88 | 18.23% | 35.13% | **148.79** | 100.98% | `HIGH` | **YES** |
| **7260** | Dhruv Jurel | 384 | 568 | 147.92 | 17.71% | 33.85% | **147.84** | 100.33% | `HIGH` | **YES** |
| **3297** | Shimron Hetmyer | 1,124 | 1,744 | 155.16 | 20.20% | 34.61% | **154.76** | 105.03% | `HIGH` | **YES** |
| **8101** | Ashutosh Sharma | 114 | 189 | 165.79 | 21.05% | 33.33% | **159.43** | 108.20% | `MEDIUM` | **YES** |
| **25669** | Priyansh Arya | 78 | 122 | 156.41 | 20.51% | 35.90% | **152.47** | 103.47% | `MEDIUM` | **YES** |
| **6460** | Ayush Badoni | 621 | 868 | 139.77 | 16.43% | 36.23% | **140.44** | 95.31% | `HIGH` | **YES** |
| **7059** | Nehal Wadhera | 242 | 349 | 144.21 | 18.18% | 35.54% | **144.83** | 98.29% | `HIGH` | **YES** |
| **19714** | Abishek Porel | 312 | 438 | 140.38 | 18.59% | 36.54% | **141.50** | 96.03% | `HIGH` | **YES** |
| **47** | Virat Kohli | 2,842 | 3,921 | 137.97 | 16.29% | 32.16% | **138.16** | 93.76% | `HIGH` | **YES** |

### Key Observations:
1. **Shrinkage Mechanics in Action:**
   - Ashutosh Sharma's raw SR of **165.79** across 114 balls shrinks to **159.43**, accurately adjusting for sample size while preserving his elite power-hitting signal.
   - Yashasvi Jaiswal's massive sample size (2,148 balls) experiences minimal shrinkage ($154.19 \rightarrow 153.92$), demonstrating sample stability.
2. **Phase Reliability Separation & Exposure Independence:**
   - Dhruv Jurel displays an elite Death Overs (15–19) strike rate exceeding 178.0, identifying his specialized finishing profile.
   - Importantly, phase confidence is evaluated independently per phase: while Jurel has `HIGH` overall sample confidence, his phase confidence is tracked separately based on phase-specific legal ball counts ($N_{\text{phase}} \ge 60$ for HIGH, $20-59$ for MEDIUM, $<20$ for LOW).
   - This eliminates the statistical flaw where batters with high overall volume automatically inherit high confidence in phases where they rarely bat (e.g. MS Dhoni in the Powerplay, or Jason Roy at the Death).
