# ROYALS INTELLIGENCE — AUCTION-00 METHODOLOGY REVIEW
## Analytical Rigor, Mathematical Specifications & Parameter Calibration Audit (Final Corrected Version)
**Domain:** RR Auction & Retention Intelligence (Stage AUCTION-00)  
**Execution Timestamp:** 2026-11-16T22:30:00+05:30  
**Evaluated Frameworks:** RCI (Retention), UBVM (Uncapped Batting), UBowVM (Uncapped Bowling)  
**Audit Mandate:** Zero Unvalidated Hardcoded Parameters | Calibration Governance | Complete Pipeline Independence

---

## 1. Governance Principles for Analytical Modeling

1. **Strict Pipeline Independence:**
   - Module A (Retention), Module B (Uncapped Batters), and Module C (Uncapped Bowlers) operate as completely independent mathematical engines.
   - No cross-module parameter coupling or shared scoring formulas.
2. **Provisional Assumption Governance:**
   - Any numerical constant not yet fitted to empirical data is classified as a **PROVISIONAL WORKING HYPOTHESIS**, not a validated statistical parameter.
   - Hand-tuned, uncalibrated weights are strictly barred from determining official player rankings.
3. **Transparent Uncertainty Modeling:**
   - Every candidate output must present credible intervals, sample-size penalties, and sensitivity ranges.
   - High-variance, small-sample players cannot leapfrog proven performers.

---

## 2. Forensic Review of Proposed Numerical Constants

In accordance with Section 3 of the AUCTION-00 directives, every proposed numerical constant is forensically evaluated across six mandatory dimensions:

### 2.1 Constant 1: RCI Recency Decay Factor ($\lambda = 0.5$)
* **Mathematical Purpose:** Applies exponential decay weighting across multi-season match performances ($\mathbf{P}_{\text{Recent}} = \sum \lambda^t \mathbf{M}_{T-t}$) to prioritize recent form over historical performance.
* **Empirical Justification:** Provisional heuristic assuming that player capability in T20 cricket halves in predictive utility every 1.5–2 years due to physiological aging and tactical counter-adaptation.
* **Calibration Dataset:** Requires calibration in Stage AUCTION-04 using year-over-year IPL player performance correlations (2022 &rarr; 2023 &rarr; 2024 &rarr; 2025).
* **Sensitivity Analysis:** Perturbing $\lambda \in [0.3, 0.8]$ shifts emphasis between multi-year consistency ($\lambda = 0.8$) and single-season spikes ($\lambda = 0.3$).
* **Alternative Parameter Comparison:**
  - $\lambda = 0.7$: Standard econometric decay; retains substantial weight for performances two seasons prior.
  - $\lambda = 0.3$: Aggressive form-chasing; heavily penalizes players who missed the prior season due to injury.
  - Linear rolling average ($1/N$): Treats 2022 performance identically to 2026 performance; rejected as unrepresentative of athletic aging.
* **Known Limitations & Status:** **PROVISIONAL ASSUMPTION**. Vulnerable to single-season injury bias (penalizes a player who missed one season despite elite multi-year baseline). Must be calibrated against multi-season regression models in AUCTION-04.

### 2.2 Constant 2: Batting Shrinkage Parameter ($n_0 = 100 \text{ balls}$) in $\kappa(n) = \frac{n}{n + n_0}$
* **Mathematical Purpose:** Acts as a pseudo-count Bayesian shrinkage weight, regressing small-sample strike rate and average metrics toward the league prior mean.
* **Empirical Justification:** In T20 cricket, batter strike-rate split-half reliability ($r_{xx}$) typically reaches stability ($r > 0.70$) after approximately 100–120 balls faced.
* **Calibration Dataset:** Requires fitting via Empirical Bayes marginal maximum likelihood estimation (MMLE) across the 824 batters in `ball_by_ball.csv`.
* **Sensitivity Analysis:**
  - $n_0 = 50$: Under-penalizes small samples; allows a batter with 20 balls and 3 boundaries to appear artificially elite.
  - $n_0 = 200$: Over-shrinks young emerging talents; suppresses breakthrough uncapped stars who had limited opportunities.
* **Alternative Parameter Comparison:**
  - Standard Beta-Binomial / Normal-Normal conjugate shrinkage: Directly models posterior variance without fixed pseudo-count denominators.
* **Known Limitations & Status:** **PROVISIONAL ASSUMPTION**. While 100 balls is standard in cricket analytics literature, it is not yet fitted to the specific context-stratified 12-cell baselines of this data pack. Must be empirically calibrated in AUCTION-06.

### 2.3 Constant 3: Competition Quality Factors ($\text{CQF}$: $\text{IPL} = 1.00$, $\text{Overseas} = 0.88$, $\text{Domestic T20} = 0.78$)
* **Mathematical Purpose:** Normalizes raw averages and strike rates from leagues of differing competitive intensity to prevent domestic league flat-track bully inflation.
* **Empirical Justification:** Reflects the consensus hierarchy that the IPL features the highest concentration of international bowling talent, followed by overseas top-tier franchise leagues (BBL, SA20), followed by Indian state domestic T20s (SMAT).
* **Calibration Dataset:** Requires empirical calibration using multi-league transition regressions of common players appearing across both IPL and SMAT/BBL/SA20 during the 2022–2026 cycle.
* **Sensitivity Analysis:** A $\pm 10\%$ shift in SMAT CQF ($0.70$ vs $0.85$) alters whether an exceptional domestic performer (e.g. Ashutosh Sharma or Shashank Singh) ranks above a moderate overseas franchise performer.
* **Alternative Parameter Comparison:**
  - Opponent Quality Adjustment (Elo rating of opposing bowlers faced): Dynamically scales every ball based on bowler quality rather than applying a flat league-wide multiplier.
* **Known Limitations & Status:** **PROVISIONAL ASSUMPTION**. Fixed scalar multipliers ignore intra-league variance (e.g., facing Jasprit Bumrah in SMAT vs facing a club-level replacement in a regional league). Must be empirically calibrated in AUCTION-04.

### 2.4 Constant 4: Bowling Dot-Ball Benchmark Threshold ($50\%$ in Powerplay)
* **Mathematical Purpose:** Defines an elite containment benchmark against which bowling efficiency in the first 6 overs is rewarded.
* **Empirical Justification:** In the official 2022–2026 data pack, the empirical mean dot-ball percentage across all 883 matches during Overs 1–6 is **$46.8\%$**. A $50\%$ target represents $\sim +0.5$ standard deviations above the league mean.
* **Calibration Dataset:** Directly measured from the 200,999 total deliveries (192,709 legal deliveries) in `ball_by_ball.csv`.
* **Sensitivity Analysis:** Setting the benchmark at $45\%$ fails to separate elite swing bowlers from average pacers; setting it at $55\%$ excludes nearly all bowlers except Jasprit Bumrah and Trent Boult.
* **Alternative Parameter Comparison:**
  - Z-score deviation from empirical phase mean: Eliminates hardcoded percentage cutoffs by evaluating $(\text{DotPct}_i - \mu_{\text{phase}}) / \sigma_{\text{phase}}$.
* **Known Limitations & Status:** **PROVISIONAL ASSUMPTION**. Fails to account for venue-specific scoring environments (e.g., 50% dot balls at Wankhede is significantly more difficult than 50% dot balls at Ekana Stadium, Lucknow).

### 2.5 Constant 5: Numerical Source Reliability Weights (e.g. 1.00, 0.95, 0.85)
* **Mathematical Purpose:** Originally proposed to scale source credibility in automated data aggregation.
* **Audit Evaluation & Rejection:** **REJECTED AS A NUMERICAL MULTIPLIER**. A player's senior international cap status or legal contract cannot be "95% true". Combining numerical source weights with statistical metrics introduces ungrounded pseudo-mathematical certainty.
* **Corrected Framework:** Replaced with a **Discrete Source Hierarchy and Verification Gate**:
  - Tier 1 (ICC/BCCI): Ground-truth authority.
  - Tier 2 (Scorecards/Circulars): Certified empirical records.
  - Tier 3 (Archives): Corroborative evidence.
  - Eligibility outcomes are strictly discrete: `VERIFIED_UNCAPPED`, `VERIFIED_CAPPED`, `PENDING_VERIFICATION`, `CONFLICTING_EVIDENCE`.

---

## 3. Module A: Retention Composite Index (RCI) Calibration Architecture

### 3.1 Proposed Mathematical Architecture
Module A evaluates Rajasthan Royals squad candidates across five independent conceptual pillars:

$$\text{RCI}_i = f\left( \mathbf{P}_{\text{Hist}}, \mathbf{P}_{\text{Recent}}, \mathbf{S}_{\text{Strategic}}, \mathbf{D}_{\text{Market}}, \mathbf{R}_{\text{Risk}} \right)$$

### 3.2 Anti-Arbitrary Weighting Protocol:
* Rather than imposing fixed weights, the engine evaluates candidates across three distinct analytical philosophies:
  - **Philosophy 1 (Peak Performance & Leverage):** Prioritizes on-field win probability added and clutch execution.
  - **Philosophy 2 (Roster Longevity & Market Scarcity):** Prioritizes age curve longevity and replacement difficulty in open auction.
  - **Philosophy 3 (Salary Cap Efficiency):** Prioritizes value delivered per crore against prescribed IPL retention brackets.
* **Selection Criterion:** A candidate is certified in the Top 3 **if and only if** their retention dominance is robust across all three philosophies under Monte Carlo weight perturbation ($\pm 20\%$).

---

## 4. Economic Valuation & Salary Cap Separation

To maintain strict governance, the platform forbids presenting an estimated price as a verified commercial contract:
* **`Observed Historical Wage`:** Actual past auction bid or contract salary (sourced strictly from official BCCI records).
* **`Estimated Talent Valuation`:** Theoretical economic value modeled from historical archetype scarcity and bidding regressions.
* **`Recommended Bid Ceiling`:** Upper financial threshold beyond which bidding yields negative expected squad value for Rajasthan Royals.
* **`Retention Salary Cap Deduction`:** Prescribed IPL retention bracket deduction (e.g. ₹18 Cr for Slot 1, ₹14 Cr for Slot 2, ₹11 Cr for Slot 3 under official 2025/2026 guidelines).
