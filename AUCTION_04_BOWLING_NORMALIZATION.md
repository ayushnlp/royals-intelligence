# ROYALS INTELLIGENCE — AUCTION-04 BOWLING NORMALIZATION
## Independent Bowling Performance Normalization & Phase Profile Report

**Document Version:** 1.0.0  
**Phase:** RR Auction & Retention Intelligence Expansion  
**Stage:** `AUCTION-04` — Historical Performance & Competition Normalization  
**Git Baseline Branch:** `main` | **HEAD:** `0f24302c61e3d4c070d0e669fc152830c9b2c4e1`  
**Execution Timestamp:** 2026-11-17T00:27:30+05:30  
**Status:** INDEPENDENT BOWLING PROFILES COMPUTED & PERSISTED

---

## 1. Executive Summary & Bowling Domain Scope

In strict accordance with the AUCTION-04 mandate, bowling performance is modeled as an **independent, self-contained analytical domain**. It is never combined with batting metrics into a composite all-rounder score.

### 1.1 Universe Scale:
- **Total Bowlers Evaluated:** **647 unique canonical players** with bowling delivery records in `ball_by_ball.csv`.
- **Sample-Qualified Bowlers:** **520 players** meeting the minimum sample qualification threshold ($\ge 30$ legal balls bowled).
- **High-Confidence Sample:** **226 players** with $\ge 200$ legal balls bowled.

---

## 2. Statistical Metric Definitions & Mathematical Formulas

$$\begin{array}{|l|l|l|}
\hline
\textbf{Bowling Metric} & \textbf{Notation} & \textbf{Mathematical Formulation \& Operational Definition} \\
\hline
\textbf{Overs Bowled} & \text{Overs} & \text{Overs} = \frac{\text{Legal Balls Bowled}}{6.0} \\
\hline
\textbf{Raw Economy Rate} & \text{Econ}_{\text{raw}} & \text{Econ}_{\text{raw}} = \frac{\text{Bowler Runs Conceded}}{\text{Legal Balls Bowled}} \times 6.0 \quad (\text{Runs off bat} + \text{wides/noball extras}) \\
\hline
\textbf{Bowling Strike Rate} & \text{BSR} & \text{BSR} = \frac{\text{Legal Balls Bowled}}{\text{Bowler Wickets Taken}} \quad (\text{excludes run-outs \& retirements}) \\
\hline
\textbf{Dot Ball Frequency} & \text{Dot}\% & \text{Dot}\% = \frac{\text{Legal Balls with 0 Runs \& 0 Bowler Extras}}{\text{Legal Balls Bowled}} \times 100.0 \\
\hline
\textbf{Boundary Concession} & \text{Bnd\_Conc}\% & \text{Bnd\_Conc}\% = \frac{\text{Fours Conceded} + \text{Sixes Conceded}}{\text{Legal Balls Bowled}} \times 100.0 \\
\hline
\textbf{Comp-Weighted Econ} & \text{Econ}_{\text{comp}} & \text{Econ}_{\text{comp}} = \frac{\sum_{k} \text{Conceded}_k \times (1 / w_{\text{score}, k})}{\text{Legal Balls Bowled}} \times 6.0 \\
\hline
\textbf{Shrunk Economy Rate} & \text{Econ}_{\text{shrunk}} & \text{Econ}_{\text{shrunk}} = \left(\frac{N}{N + 60}\right) \text{Econ}_{\text{comp}} + \left(\frac{60}{N + 60}\right) 9.13 \quad (\text{Provisional } m=60) \\
\hline
\textbf{Economy Efficiency} & \text{Eff}_{\text{econ}} & \text{Eff}_{\text{econ}} = \left(\frac{9.13}{\text{Econ}_{\text{shrunk}}}\right) \times 100.0 \quad (\text{Higher is better; } >100 \text{ is superior to IPL average}) \\
\hline
\end{array}$$

---

## 3. Phase-Specific Bowling Decomposition

Every bowler's profile contains independent phase breakdowns:
1. **Powerplay Bowling (Overs 0–5):** Evaluates swing, seam movement, early wicket-taking threat, and boundary suppression against the hard new ball with field restrictions.
2. **Middle Overs Bowling (Overs 6–14):** Evaluates control, spin variations, run constriction, and breaking batting partnerships when 5 fielders are outside the circle.
3. **Death Overs Bowling (Overs 15–19):** High-leverage execution. Evaluates yorker accuracy, wide-line execution, slower-ball deception, and boundary prevention in the target acceleration zone.

---

## 4. Stratified Player Profile Audits (Representative Cohort)

The table below audits a representative sample across Rajasthan Royals contracted candidates, audited uncapped domestic pacers/spinners, and international benchmarks:

| Canonical ID | Player Name | Legal Balls | Overs | Runs Conc | Wkts | Raw Econ | Dot \% | Bnd Conc \% | Shrunk Econ | Econ Eff | Conf Tier |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **2411** | Sandeep Sharma | 965 | 160.8 | 1,457 | 39 | 9.06 | 36.89% | 18.03% | **9.06** | 100.69% | `HIGH` |
| **3298** | Jofra Archer | 1,261 | 210.2 | 1,876 | 71 | 8.93 | 42.11% | 17.21% | **9.24** | 98.77% | `HIGH` |
| **6806** | Tushar Deshpande | 1,039 | 173.2 | 1,721 | 54 | 9.94 | 33.30% | 19.83% | **9.92** | 91.97% | `HIGH` |
| **26663** | Kwena Maphaka | 308 | 51.3 | 544 | 15 | 10.60 | 33.77% | 22.08% | **10.97** | 83.17% | `HIGH` |
| **8746** | Vaibhav Arora | 896 | 149.3 | 1,450 | 48 | 9.71 | 35.83% | 19.20% | **9.72** | 93.90% | `HIGH` |
| **7327** | Rasikh Salam | 542 | 90.3 | 865 | 38 | 9.58 | 34.69% | 19.93% | **9.69** | 94.13% | `HIGH` |
| **27964** | Anshul Kamboj | 545 | 90.8 | 906 | 35 | 9.97 | 34.50% | 19.45% | **10.05** | 90.82% | `HIGH` |
| **6237** | M. Siddharth | 186 | 31.0 | 281 | 9 | 9.06 | 37.10% | 15.05% | **9.08** | 100.51% | `MEDIUM` |
| **36982** | Suyash Sharma | 900 | 150.0 | 1,294 | 32 | 8.63 | 36.33% | 16.44% | **8.78** | 103.97% | `HIGH` |
| **2933** | Jasprit Bumrah | 1,709 | 284.8 | 2,043 | 85 | 7.17 | 45.41% | 13.11% | **7.43** | 122.81% | `HIGH` |

### Key Observations:
1. **Shrinkage Control with Provisional Parameter ($m=60$):**
   - Empirical Bayes shrinkage uses the empirical IPL baseline ($\mu_0 = 9.13$ RPO) rather than arbitrary historical benchmarks.
   - Manimaran Siddharth's raw economy of **9.06** across 186 balls gently pulls toward the league anchor ($9.08$).
2. **Generational Benchmark Stability:**
   - Jasprit Bumrah delivers an extraordinary 7.17 raw economy across 1,709 legal deliveries (45.41% dot balls), achieving a 122.81% normalized economy efficiency relative to the IPL baseline.
3. **Independent Exposure Tracking:**
   - Bowler confidence is strictly evaluated per game phase. Specialists with limited sample in specific phases ($<20$ balls) are not misclassified as high-confidence in those phases. Phase qualification ($N_{\text{phase}} \ge 20$) and confidence tiers are computed independently for each phase.
