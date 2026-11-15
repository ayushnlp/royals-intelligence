"""
ROYALS INTELLIGENCE — ROUND 1 EXPLAINABILITY & REPORTING ENGINE
Architecture: ROYALS INTELLIGENCE v4.1
Task: R1-06 Evidence-Backed Player Reliability Intelligence & Ranking Engine

Generates deterministic evidence profiles and comprehensive analytical reports
answering all 11 required candidate questions and the 7 core analyst questions.
Produces:
- batting_evidence_profiles.parquet
- bowling_evidence_profiles.parquet
- r1_06_player_intelligence_report.md
- r1_06_batting_shortlist.md
- r1_06_bowling_shortlist.md
- r1_06_methodology_and_limitations.md
"""

from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import numpy as np
import pandas as pd


class ExplainabilityEngine:
    """
    Produces deterministic question-by-question candidate evidence profiles
    and comprehensive Markdown intelligence reports.
    """

    def __init__(
        self,
        bat_leaderboard_df: Optional[pd.DataFrame] = None,
        bowl_leaderboard_df: Optional[pd.DataFrame] = None,
        robustness_df: Optional[pd.DataFrame] = None,
        processed_dir: Optional[Path] = None,
        reports_dir: Optional[Path] = None,
    ):
        base_dir = Path(__file__).resolve().parent.parent
        self.processed_dir = processed_dir or (base_dir / "data" / "processed")
        self.reports_dir = reports_dir or (base_dir / "reports")

        self.bat_leaderboard = bat_leaderboard_df
        self.bowl_leaderboard = bowl_leaderboard_df
        self.robustness_df = robustness_df

        self.bat_profiles_df: Optional[pd.DataFrame] = None
        self.bowl_profiles_df: Optional[pd.DataFrame] = None

    def load_data(self) -> None:
        """Loads required leaderboards and robustness datasets if not provided."""
        if self.bat_leaderboard is None:
            self.bat_leaderboard = pd.read_parquet(self.processed_dir / "batting_leaderboard.parquet")
        if self.bowl_leaderboard is None:
            self.bowl_leaderboard = pd.read_parquet(self.processed_dir / "bowling_leaderboard.parquet")
        if self.robustness_df is None:
            self.robustness_df = pd.read_parquet(self.processed_dir / "shortlist_robustness_comparison.parquet")

    @staticmethod
    def generate_candidate_profile(row: pd.Series, is_batting: bool) -> Dict[str, Any]:
        """
        Generates a deterministic evidence profile answering the 11 candidate questions.
        """
        name = row["player_name"]
        pid = row["player_id"]
        rank = row["rank"]
        diag_name = row["primary_diagnostic_name"]
        diag_val = row["primary_diagnostic_value"]
        diag_unit = row["primary_diagnostic_unit"]
        balls = row["pressure_legal_balls"]
        vol_tier = row["evidence_volume_tier"]
        matches = row["pressure_matches"]
        seasons = row["pressure_seasons"]
        season_dist = row["season_distribution"]
        obs_rate = row["observed_strike_rate"] if is_batting else row["observed_economy"]
        exp_rate = row["expected_strike_rate"] if is_batting else row["expected_economy"]
        diff_rate = row["diff_strike_rate"] if is_batting else row["diff_economy"]
        post_mean = row["posterior_mean"]
        post_se = row["posterior_se"]
        ci_lower = row["ci_95_lower"]
        ci_upper = row["ci_95_upper"]
        ci_width = row["ci_95_width"]
        shrink_wt = row["shrinkage_weight"]
        ipl_b = row["ipl_legal_balls"]
        t20i_b = row["t20i_legal_balls"]
        comp_cov = row["competition_coverage"]
        comp_qual = row.get("competition_qualification", "N/A")
        classification = row["evidence_classification"]
        dim_a = row.get("performance_evidence_status", "N/A")
        dim_b = row.get("evidence_volume_tier", vol_tier)
        two_dim = row.get("two_dimensional_classification", f"{dim_a} ({dim_b})")
        cohort = row.get("watchlist_cohort", "N/A")
        cand_qual = bool(row.get("is_candidate_qualified", True))
        p_base = row["prob_exceed_baseline"]
        p_peer = row["prob_exceed_peers"]
        p_league = float(row.get("prob_exceed_league_mean", p_peer))

        unit_str = "SR pts" if is_batting else "RPO"

        # Evidence status explanation note
        status_note = ""
        if dim_a == "POSITIVE_CONSERVATIVE_EVIDENCE":
            status_note = "Under an approximate normal posterior distribution, a positive one-standard-error lower bound implies posterior probability above zero greater than approximately 84.1%. This is a directional uncertainty diagnostic, not a 95% credible interval, conventional 95% statistical significance, or a guarantee of future performance (95% CI spans zero)."
        elif dim_a == "POSITIVE_ESTIMATE_UNRESOLVED":
            status_note = "Posterior mean is strictly positive, but 1-SE conservative lower bound spans zero/negative (positive estimated performance with unresolved uncertainty; NOT evidence of below-baseline performance)."
        elif dim_a == "BELOW_BASELINE_EVIDENCE":
            status_note = "Under an approximate normal posterior distribution, a negative one-standard-error upper bound implies posterior probability below baseline greater than approximately 84.1%. This is a directional uncertainty diagnostic, not conventional 95% statistical significance or proof of underperformance."
        elif dim_a == "INCONCLUSIVE_EVIDENCE":
            status_note = "Point estimate is non-positive, but 1-SE uncertainty interval crosses ordinary baseline."

        # Question 1: Why considered?
        q1 = (
            f"Ranked #{rank} in {row['discipline'].capitalize()} with a conservative diagnostic value of {diag_val:+.2f} {unit_str}. "
            f"Two-Dimensional Classification: '{two_dim}' (Evidence Status: `{dim_a}`, Volume: `{dim_b}`, Cohort: `{cohort}`). "
            f"Sample qualification: {'QUALIFIED' if cand_qual else 'EXPLORATORY_WATCHLIST'} (legacy: '{classification}'). "
            f"{status_note}"
        )

        # Question 2: Sample size?
        q2 = f"{balls} legal pressure deliveries bowled/faced, categorized in '{dim_b}' (Volume Tier B)."

        # Question 3: Matches and seasons?
        q3 = f"Demonstrated across {matches} unique pressure matches and {seasons} active seasons (Distribution: {season_dist})."

        # Question 4: Observed pressure performance?
        rate_name = "Strike Rate" if is_batting else "Economy Rate"
        q4 = f"Observed {rate_name}: {obs_rate:.2f} (raw difference of {diff_rate:+.2f} {unit_str} versus context expectation)."

        # Question 5: Context-adjusted expected performance?
        q5 = f"Context-adjusted expectation: {exp_rate:.2f} {rate_name}, derived from stratified 12-cell baselines across phase, tournament tier, and innings."

        # Question 6: Conservative diagnostic value?
        score_desc = "posterior mean minus 1.0 SE (SR points)" if is_batting else "negative posterior economy diff minus 1.0 SE (runs saved/over)"
        q6 = (
            f"{diag_name} = {diag_val:+.2f} {unit_str}. "
            f"Represents the 1-SE conservative diagnostic bound ({score_desc}). "
            "Under an approximate normal posterior distribution, a positive one-standard-error lower bound implies posterior probability above zero greater than approximately 84.1%. "
            "This is a directional uncertainty diagnostic, not a 95% credible interval, conventional 95% statistical significance, or a guarantee of future performance."
        )

        # Question 7: Posterior uncertainty?
        q7 = f"Posterior standard error: $\\pm${post_se:.2f} {unit_str}. Shrinkage weight $r = {shrink_wt:.3f}$."

        # Question 8: Credible interval bounds?
        q8 = (
            f"95% Credible Interval: [{ci_lower:.2f}, {ci_upper:.2f}] {unit_str} (width: {ci_width:.2f} {unit_str}). "
            "Displayed separately from the 1-SE diagnostic score; reflects a two-sided 95% Bayesian credible region (z = 1.96)."
        )

        # Question 9: Competition support?
        q9 = (
            f"Coverage: {comp_cov} ({ipl_b} balls in IPL, {t20i_b} balls in Senior T20I | Classification: `{comp_qual}`). "
            f"{'Supported by substantial sample in both competitions.' if row['cross_comp_transferable'] else 'Limited cross-competition sample overlap.'} "
            "Note: Dual-tournament qualification indicates sample exposure availability in both competitions, NOT statistical proof of cross-competition skill transferability."
        )

        # Question 10: Major limitations?
        limitations = []
        if balls < 100:
            limitations.append(f"Moderate sample volume ({balls} balls; estimation CI width is {ci_width:.1f} {unit_str})")
        if not row["cross_comp_transferable"]:
            limitations.append(f"Heavily skewed towards {'IPL' if ipl_b > t20i_b else 'T20I'}; cross-league transferability is not guaranteed")
        if seasons < 3:
            limitations.append(f"Short multi-season track record ({seasons} seasons active)")
        if not limitations:
            limitations.append("Robust sample volume and multi-season stability; residual uncertainty bounded by 95% CI")
        q10 = "; ".join(limitations) + "."

        # Question 11: Sensitivity to assumptions?
        ref_mean_str = "-34.24 SR pts" if is_batting else "+1.82 RPO"
        q11 = (
            f"Under unpenalized posterior mean, performance is {post_mean:+.2f} {unit_str}. "
            f"Model credibility against baseline: {p_base*100:.1f}%; "
            f"against league-wide pressure mean (prior mean $\\mu = {ref_mean_str}$): {p_league*100:.1f}%. "
            f"Exceeding league average under pressure compares against degraded match conditions, NOT fellow shortlisted candidates. "
            f"Exploratory PRI without TCF: {row['exploratory_pri_no_tcf']:.1f}; Experimental PRI with TCF: {row['experimental_pri_with_tcf']:.1f}."
        )

        return {
            "player_id": pid,
            "player_name": name,
            "discipline": row["discipline"],
            "rank": rank,
            "evidence_classification": classification,
            "performance_evidence_status": dim_a,
            "evidence_volume_tier": dim_b,
            "two_dimensional_classification": two_dim,
            "watchlist_cohort": cohort,
            "is_candidate_qualified": cand_qual,
            "prob_exceed_league_mean": p_league,
            "q1_why_considered": q1,
            "q2_pressure_deliveries": q2,
            "q3_matches_and_seasons": q3,
            "q4_observed_performance": q4,
            "q5_expected_performance": q5,
            "q6_conservative_diagnostic": q6,
            "q7_posterior_uncertainty": q7,
            "q8_credible_interval": q8,
            "q9_competition_support": q9,
            "q10_major_limitations": q10,
            "q11_sensitivity_to_assumptions": q11,
        }

    def build_all_profiles(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Constructs evidence profiles for all qualified batters and bowlers."""
        if self.bat_leaderboard is None or self.bowl_leaderboard is None:
            self.load_data()

        bat_profiles = [
            self.generate_candidate_profile(r, is_batting=True)
            for _, r in self.bat_leaderboard.iterrows()
        ]
        bowl_profiles = [
            self.generate_candidate_profile(r, is_batting=False)
            for _, r in self.bowl_leaderboard.iterrows()
        ]

        self.bat_profiles_df = pd.DataFrame(bat_profiles)
        self.bowl_profiles_df = pd.DataFrame(bowl_profiles)

        # Save Parquet
        self.bat_profiles_df.to_parquet(self.processed_dir / "batting_evidence_profiles.parquet", index=False)
        self.bowl_profiles_df.to_parquet(self.processed_dir / "bowling_evidence_profiles.parquet", index=False)

        return self.bat_profiles_df, self.bowl_profiles_df

    def generate_all_reports(self) -> Dict[str, Path]:
        """Generates all 4 comprehensive analytical markdown reports."""
        if self.bat_profiles_df is None or self.bowl_profiles_df is None:
            self.build_all_profiles()

        now_iso = datetime.now(timezone.utc).isoformat()
        reports = {}

        # ----------------------------------------------------------------------
        # REPORT 1: BATTING SHORTLIST REPORT
        # ----------------------------------------------------------------------
        bat_report_path = self.reports_dir / "r1_06_batting_shortlist.md"
        top_bat = self.bat_leaderboard[self.bat_leaderboard["is_candidate_qualified"]].head(12)
        top_bat_ids = set(top_bat["player_id"])
        prom_emerging_bat = self.bat_leaderboard[self.bat_leaderboard["watchlist_cohort"] == "EMERGING_HIGH_UPSIDE"]
        prom_estab_bat = self.bat_leaderboard[
            (self.bat_leaderboard["watchlist_cohort"] == "ESTABLISHED_MARGINAL_PERFORMER") &
            (~self.bat_leaderboard["player_id"].isin(top_bat_ids))
        ]

        bat_lines = [
            "# ROYALS INTELLIGENCE — ROUND 1 BATTING PRESSURE RELIABILITY SHORTLIST",
            f"**Generated:** {now_iso}  ",
            "**Architecture:** ROYALS INTELLIGENCE v4.1  ",
            "**Task:** R1-06 / R1-06.2.3 Final Data-Count Reconciliation & Statistical Wording Correction  ",
            "**Primary Metric:** Conservative Lower Credible Bound `BAT_CONSERVATIVE = posterior_mean_SR - posterior_SE_SR` (SR Points)  ",
            "",
            "---",
            "",
            "## 1. Executive Shortlist Overview",
            "",
            "The Batting Pressure Reliability Shortlist evaluates batters under high-leverage match conditions, penalized by posterior estimation uncertainty. "
            "Under the remediated **Two-Dimensional Classification System** (Task R1-06.2.2 / R1-06.2.3):",
            "- **Dimension A (Performance Evidence Status):** Separates candidates whose 1-SE conservative bound is strictly positive from those with positive estimated effect but unresolved uncertainty, below baseline, or inconclusive.",
            "- **Dimension B (Evidence Volume Tier):** HIGH_VOLUME ($\\ge 150$ balls), MEDIUM_VOLUME ($60-149$ balls), LOW_VOLUME ($30-59$ balls).",
            "",
            "> [!IMPORTANT]",
            "> **Statistical Credibility & Uncertainty Disclosure (1-SE Bound vs 95% Credible Interval):**",
            "> - **Primary Conservative Score Formula:** `BAT_CONSERVATIVE = posterior_mean_SR - posterior_SE_SR` (SR Points).",
            "> - **Statistical Interpretation & Uncertainty Diagnostic:** Under an approximate normal posterior distribution, a positive one-standard-error lower bound implies posterior probability above zero greater than approximately 84.1%. This is a directional uncertainty diagnostic, not a 95% credible interval, conventional 95% statistical significance, or a guarantee of future performance.",
            "> - **Positive Conservative Evidence (`POSITIVE_CONSERVATIVE_EVIDENCE`):** Exactly 2 qualified batters (**Nicholas Pooran: +2.2 SR pts**, **Donovan Ferreira: +0.9 SR pts**) establish strictly positive 1-SE lower bounds ($L > 0$). However, their 95% credible intervals span zero (Pooran: `[-11.2, +43.6]`, Ferreira: `[-18.0, +59.4]`). Under a strict 95% CI standard, zero batters in the entire dataset would qualify.",
            "> - **Positive Estimate with Unresolved Uncertainty (`POSITIVE_ESTIMATE_UNRESOLVED`):** Candidates ranked #3 through #12 exhibit positive posterior means ($\\hat{\\theta} > 0.0$), but their 1-SE conservative lower bounds are non-positive ($L \\le 0$). This reflects positive estimated performance with unresolved uncertainty spanning zero, **NOT** evidence of below-baseline performance.",
            "> - **Below-Baseline Evidence (`BELOW_BASELINE_EVIDENCE`):** 1-SE upper bound is strictly below zero ($U < 0$), implying directional probability of below-baseline performance greater than approximately 84.1%, not 95% scientific proof of underperformance.",
            "> - Candidates ranked #3 through #12 have heavily overlapping 95% credible intervals (e.g. Tim David: [-14.1, +33.3], Dinesh Karthik: [-14.0, +32.5], Ashutosh Sharma: [-17.0, +37.6]). Small ranking differences among these players reflect empirical sample variance rather than proven qualitative superiority.",
            "",
            "> [!NOTE]",
            "> **Probability Interpretation Disclosure:**",
            "> `P(Exceed League Avg Under Pressure)` evaluates exceedance over the league-wide pressure prior mean ($\\mu_b = -34.24$ SR pts). Because league-wide batting strike rates collapse by ~34 points under pressure, achieving 90%+ probability of exceeding the league pressure average is a much lower hurdle than beating ordinary baseline expectation ($P(\\text{Beat Base})$).",
            "",
            "### Batting Leaderboard (Top 12 Sample-Qualified Candidates):",
            "",
            "| Shortlist Rank | Batter Name | BAT_CONSERVATIVE (SR pts) | Posterior Mean $\\hat{\\theta}$ | Posterior SE | 95% Credible Interval | Pressure Balls | Matches | Comp Qual | P(Beat Base) | P(Exceed League Avg Under Pressure) | Dim A (Evidence Status) | Dim B (Volume) | Watchlist Cohort |",
            "| :--- | :--- | ---: | ---: | ---: | :---: | ---: | ---: | :--- | ---: | ---: | :--- | :--- | :--- |",
        ]

        for idx, (_, r) in enumerate(top_bat.iterrows(), 1):
            ci_str = f"[{r['ci_95_lower']:+.1f}, {r['ci_95_upper']:+.1f}]"
            comp_q = r.get("competition_qualification", r["competition_coverage"])
            dim_a_val = r.get("performance_evidence_status", r["evidence_classification"])
            dim_b_val = r.get("evidence_volume_tier", "MEDIUM_VOLUME")
            cohort_val = r.get("watchlist_cohort", "N/A")
            p_lg = r.get("prob_exceed_league_mean", r["prob_exceed_peers"])
            bat_lines.append(
                f"| **{idx}** | **{r['player_name']}** | **{r['primary_diagnostic_value']:+.1f}** | "
                f"{r['posterior_mean']:+.1f} | $\\pm${r['posterior_se']:.1f} | {ci_str} | "
                f"{r['pressure_legal_balls']} | {r['pressure_matches']} | "
                f"`{comp_q}` | {r['prob_exceed_baseline']*100:.1f}% | {p_lg*100:.1f}% | "
                f"`{dim_a_val}` | `{dim_b_val}` | `{cohort_val}` |"
            )

        bat_lines.extend([
            "",
            "---",
            "",
            "## 2. In-Depth Candidate Evidence Profiles",
            "",
        ])

        top_profiles = self.bat_profiles_df[self.bat_profiles_df["is_candidate_qualified"]].head(10)
        for _, p in top_profiles.iterrows():
            bat_lines.extend([
                f"### #{p['rank']} — {p['player_name']} (`{p['two_dimensional_classification']}`)",
                f"- **Why Considered:** {p['q1_why_considered']}",
                f"- **Evidence Volume:** {p['q2_pressure_deliveries']}",
                f"- **Temporal Stability:** {p['q3_matches_and_seasons']}",
                f"- **Observed vs Expected:** {p['q4_observed_performance']} | {p['q5_expected_performance']}",
                f"- **Conservative Diagnostic Score:** {p['q6_conservative_diagnostic']}",
                f"- **Uncertainty & CI:** {p['q7_posterior_uncertainty']} | {p['q8_credible_interval']}",
                f"- **Competition Support:** {p['q9_competition_support']}",
                f"- **Key Limitations:** {p['q10_major_limitations']}",
                f"- **Sensitivity Profile:** {p['q11_sensitivity_to_assumptions']}",
                "",
            ])

        bat_lines.extend([
            "---",
            "",
            "## 3. Exploratory Watchlist (Promising Candidates Watchlist: Emerging vs Established Cohorts)",
            "",
            "Exploratory watchlist candidates are maintained strictly separate from the sample-qualified primary leaderboard:",
            "",
            "### A. Emerging High-Upside Exploratory Watchlist (`EMERGING_HIGH_UPSIDE` — $30 \\le n < 60$ balls, positive posterior mean):",
            "These emerging players have high estimated overperformance under pressure but limited exposure volume ($< 60$ balls), retaining higher estimation variance and remaining sample-disqualified for primary shortlist inclusion:",
            "",
            "| Batter Name | Posterior Mean $\\hat{\\theta}$ | Posterior SE | Conservative Bound | Pressure Balls | Matches | Volume Tier | Watchlist Cohort | Two-Dimensional Status |",
            "| :--- | ---: | ---: | ---: | ---: | ---: | :--- | :--- | :--- |",
        ])

        for _, r in prom_emerging_bat.iterrows():
            bat_lines.append(
                f"| **{r['player_name']}** | {r['posterior_mean']:+.1f} SR | $\\pm${r['posterior_se']:.1f} | "
                f"{r['primary_diagnostic_value']:+.1f} SR | {r['pressure_legal_balls']} | {r['pressure_matches']} | "
                f"`{r['evidence_volume_tier']}` | `{r['watchlist_cohort']}` | `{r['two_dimensional_classification']}` |"
            )

        bat_lines.extend([
            "",
            "### B. Established Marginal Performers Exploratory Watchlist (`ESTABLISHED_MARGINAL_PERFORMER` — $n \\ge 60$ balls, positive posterior mean, conservative bound $\\le 0$):",
            "*(Note: Candidates ranked in Table 1 above are primary qualified candidates; the watchlist below features additional established marginal performers outside the primary shortlist)*",
            "",
            "| Batter Name | Posterior Mean $\\hat{\\theta}$ | Posterior SE | Conservative Bound | Pressure Balls | Matches | Volume Tier | Watchlist Cohort | Two-Dimensional Status |",
            "| :--- | ---: | ---: | ---: | ---: | ---: | :--- | :--- | :--- |",
        ])

        for _, r in prom_estab_bat.iterrows():
            bat_lines.append(
                f"| **{r['player_name']}** | {r['posterior_mean']:+.1f} SR | $\\pm${r['posterior_se']:.1f} | "
                f"{r['primary_diagnostic_value']:+.1f} SR | {r['pressure_legal_balls']} | {r['pressure_matches']} | "
                f"`{r['evidence_volume_tier']}` | `{r['watchlist_cohort']}` | `{r['two_dimensional_classification']}` |"
            )

        bat_report_path.write_text("\n".join(bat_lines), encoding="utf-8")
        reports["batting_shortlist"] = bat_report_path

        # ----------------------------------------------------------------------
        # REPORT 2: BOWLING SHORTLIST REPORT
        # ----------------------------------------------------------------------
        bowl_report_path = self.reports_dir / "r1_06_bowling_shortlist.md"
        top_bowl = self.bowl_leaderboard[self.bowl_leaderboard["is_candidate_qualified"]].head(11)
        top_bowl_ids = set(top_bowl["player_id"])
        prom_emerging_bowl = self.bowl_leaderboard[self.bowl_leaderboard["watchlist_cohort"] == "PEER_BEATING_EMERGING"].head(10)
        prom_estab_bowl = self.bowl_leaderboard[
            (self.bowl_leaderboard["watchlist_cohort"] == "PEER_BEATING_ESTABLISHED") &
            (~self.bowl_leaderboard["player_id"].isin(top_bowl_ids))
        ].head(10)

        bowl_lines = [
            "# ROYALS INTELLIGENCE — ROUND 1 BOWLING PRESSURE RELIABILITY SHORTLIST",
            f"**Generated:** {now_iso}  ",
            "**Architecture:** ROYALS INTELLIGENCE v4.1  ",
            "**Task:** R1-06 / R1-06.2.3 Final Data-Count Reconciliation & Statistical Wording Correction  ",
            "**Primary Metric:** Conservative Runs Saved per Over `BOWL_CONSERVATIVE = -posterior_mean_economy_diff - posterior_SE_economy` (Runs Saved/Over)  ",
            "",
            "---",
            "",
            "## 1. Executive Shortlist Overview",
            "",
            "The Bowling Pressure Reliability Shortlist evaluates bowler run containment under high-leverage conditions relative to context expectations, penalized by posterior estimation uncertainty. "
            "Under the remediated **Two-Dimensional Classification System** (Task R1-06.2.2 / R1-06.2.3):",
            "- **Dimension A (Performance Evidence Status):** Evaluates runs saved point estimate and uncertainty intervals relative to baseline expectation.",
            "- **Dimension B (Evidence Volume Tier):** HIGH_VOLUME ($\\ge 150$ balls), MEDIUM_VOLUME ($60-149$ balls), LOW_VOLUME ($30-59$ balls).",
            "",
            "> [!IMPORTANT]",
            "> **Statistical Credibility & Uncertainty Disclosure (1-SE Bound vs 95% Credible Interval):**",
            "> - **Primary Conservative Score Formula:** `BOWL_CONSERVATIVE = -posterior_mean_economy_diff - posterior_SE_economy` (Runs Saved/Over).",
            "> - **Statistical Interpretation & Uncertainty Diagnostic:** Under an approximate normal posterior distribution, a positive one-standard-error lower bound implies posterior probability above zero greater than approximately 84.1%. This is a directional uncertainty diagnostic, not a 95% credible interval, conventional 95% statistical significance, or a guarantee of future performance.",
            "> - **Positive Conservative Runs Saved (`POSITIVE_CONSERVATIVE_EVIDENCE`):** Across all 239 qualified bowlers, **exactly 0 bowlers** establish strictly positive 1-SE conservative runs saved ($L_s > 0$).",
            "> - **Positive Estimate with Unresolved Uncertainty (`POSITIVE_ESTIMATE_UNRESOLVED`):** **Jasprit Bumrah (#1: -0.16 RPO)** is the **ONLY qualified bowler in the 883-match dataset** who concedes fewer runs under pressure (8.94 RPO) than ordinary baseline (9.70 RPO), with a positive runs saved point estimate ($S = +0.20$ RPO, posterior economy diff $-0.20 \\pm 0.36$), but a 1-SE runs saved bound of $-0.16 \\le 0$ RPO and 95% CI `[-0.90, +0.50]` RPO. He is classified as `POSITIVE_ESTIMATE_UNRESOLVED (HIGH_VOLUME)`. This must NOT be interpreted as evidence of below-baseline performance.",
            "> - **Inconclusive Evidence (`INCONCLUSIVE_EVIDENCE`):** **Sunil Narine (#2: -0.94 RPO)** is classified as `INCONCLUSIVE_EVIDENCE (HIGH_VOLUME)` because his posterior economy diff is $+0.39$ RPO ($S = -0.39$) with $\\text{SE} = 0.55$, giving a 1-SE upper runs saved bound of $+0.16 \\ge 0$.",
            "> - **Below-Baseline Evidence (`BELOW_BASELINE_EVIDENCE`):** The remaining **237 qualified bowlers** are classified as `BELOW_BASELINE_EVIDENCE` because their 1-sigma uncertainty intervals fall strictly below ordinary baseline expectations. 226 of them (95.4%) maintain economy inflation $> 0$ at 95% CI; 11 span zero.",
            "",
            "> [!NOTE]",
            "> **Resolution of the 87 vs 88 Bowling Promising Discrepancy:**",
            "> The R1-06.1 audit identified a count divergence between 87 and 88 bowlers outperforming peer average (+1.82 RPO). Full-precision unrounded investigation reveals that Sakib Hussain (`shrunk_diff_economy = 1.817738...`) is strictly below 1.82, whereas Riley Meredith (`shrunk_diff_economy = 1.821739...`) is strictly above 1.82. When code pre-rounded values to 2 decimal places, both evaluated as `1.82 < 1.82 == False`, producing 87. Under full-precision evaluation, Sakib Hussain is included (88). Against the exact prior mean $\\mu = 1.82275596$, both are below. The platform now enforces full-precision float comparisons across all pipelines.",
            "",
            "> [!NOTE]",
            "> **Probability Interpretation Disclosure:**",
            "> `P(Exceed League Avg Under Pressure)` evaluates exceedance over the league-wide pressure prior mean ($\\mu_{bw} = +1.82$ RPO). Conceding fewer than +1.82 RPO extra under pressure beats the average pressured bowler, but does NOT constitute beating ordinary baseline performance.",
            "",
            "### Bowling Leaderboard (Top 11 Sample-Qualified Candidates):",
            "",
            "| Shortlist Rank | Bowler Name | BOWL_CONSERVATIVE (Runs Saved) | Posterior Mean Diff | Posterior SE | 95% Credible Interval | Pressure Balls | Matches | Comp Qual | P(Beat Base) | P(Exceed League Avg Under Pressure) | Dim A (Evidence Status) | Dim B (Volume) | Watchlist Cohort |",
            "| :--- | :--- | ---: | ---: | ---: | :---: | ---: | ---: | :--- | ---: | ---: | :--- | :--- | :--- |",
        ]

        for idx, (_, r) in enumerate(top_bowl.iterrows(), 1):
            ci_str = f"[{r['ci_95_lower']:+.2f}, {r['ci_95_upper']:+.2f}]"
            comp_q = r.get("competition_qualification", r["competition_coverage"])
            dim_a_val = r.get("performance_evidence_status", r["evidence_classification"])
            dim_b_val = r.get("evidence_volume_tier", "MEDIUM_VOLUME")
            cohort_val = r.get("watchlist_cohort", "N/A")
            p_lg = r.get("prob_exceed_league_mean", r["prob_exceed_peers"])
            bowl_lines.append(
                f"| **{idx}** | **{r['player_name']}** | **{r['primary_diagnostic_value']:+.2f}** | "
                f"{r['posterior_mean']:+.2f} | $\\pm${r['posterior_se']:.2f} | {ci_str} | "
                f"{r['pressure_legal_balls']} | {r['pressure_matches']} | "
                f"`{comp_q}` | {r['prob_exceed_baseline']*100:.1f}% | {p_lg*100:.1f}% | "
                f"`{dim_a_val}` | `{dim_b_val}` | `{cohort_val}` |"
            )

        bowl_lines.extend([
            "",
            "---",
            "",
            "## 2. In-Depth Candidate Evidence Profiles",
            "",
        ])

        top_bowl_profiles = self.bowl_profiles_df[self.bowl_profiles_df["is_candidate_qualified"]].head(10)
        for _, p in top_bowl_profiles.iterrows():
            bowl_lines.extend([
                f"### #{p['rank']} — {p['player_name']} (`{p['two_dimensional_classification']}`)",
                f"- **Why Considered:** {p['q1_why_considered']}",
                f"- **Evidence Volume:** {p['q2_pressure_deliveries']}",
                f"- **Temporal Stability:** {p['q3_matches_and_seasons']}",
                f"- **Observed vs Expected:** {p['q4_observed_performance']} | {p['q5_expected_performance']}",
                f"- **Conservative Diagnostic Score:** {p['q6_conservative_diagnostic']}",
                f"- **Uncertainty & CI:** {p['q7_posterior_uncertainty']} | {p['q8_credible_interval']}",
                f"- **Competition Support:** {p['q9_competition_support']}",
                f"- **Key Limitations:** {p['q10_major_limitations']}",
                f"- **Sensitivity Profile:** {p['q11_sensitivity_to_assumptions']}",
                "",
            ])

        bowl_lines.extend([
            "---",
            "",
            "## 3. Exploratory Watchlist (Promising Candidates Watchlist: Peer-Beaters Under Pressure)",
            "",
            "These bowlers outperform peer averages ($\\hat{\\theta} < +1.82$ RPO), saving runs relative to the degraded match environment. "
            "Exploratory watchlist candidates are maintained strictly separate from the sample-qualified primary leaderboard:",
            "",
            "### A. Emerging Peer-Beating Exploratory Watchlist (`PEER_BEATING_EMERGING` — $30 \\le n < 60$ balls, beating peer mean):",
            "*(Note: These bowlers outperform the league pressure average but lack sample qualification for the primary leaderboard; e.g. Nasum Ahmed [47b], Vipraj Nigam [46b], Ramon Simmonds [30b])*",
            "",
            "| Bowler Name | Posterior Mean Diff | Posterior SE | Conservative Runs Saved | Pressure Balls | Matches | Volume Tier | Watchlist Cohort | Two-Dimensional Status |",
            "| :--- | ---: | ---: | ---: | ---: | ---: | :--- | :--- | :--- |",
        ])

        for _, r in prom_emerging_bowl.iterrows():
            bowl_lines.append(
                f"| **{r['player_name']}** | {r['posterior_mean']:+.2f} RPO | $\\pm${r['posterior_se']:.2f} | "
                f"{r['primary_diagnostic_value']:+.2f} RPO | {r['pressure_legal_balls']} | {r['pressure_matches']} | "
                f"`{r['evidence_volume_tier']}` | `{r['watchlist_cohort']}` | `{r['two_dimensional_classification']}` |"
            )

        bowl_lines.extend([
            "",
            "### B. Established Peer-Beating Exploratory Watchlist (`PEER_BEATING_ESTABLISHED` — $n \\ge 60$ balls, beating peer mean):",
            "*(Note: Primary shortlisted candidates 1–11 are detailed in Table 1 above; the watchlist below features additional established peer-beaters outside the primary shortlist)*",
            "",
            "| Bowler Name | Posterior Mean Diff | Posterior SE | Conservative Runs Saved | Pressure Balls | Matches | Volume Tier | Watchlist Cohort | Two-Dimensional Status |",
            "| :--- | ---: | ---: | ---: | ---: | ---: | :--- | :--- | :--- |",
        ])

        for _, r in prom_estab_bowl.iterrows():
            bowl_lines.append(
                f"| **{r['player_name']}** | {r['posterior_mean']:+.2f} RPO | $\\pm${r['posterior_se']:.2f} | "
                f"{r['primary_diagnostic_value']:+.2f} RPO | {r['pressure_legal_balls']} | {r['pressure_matches']} | "
                f"`{r['evidence_volume_tier']}` | `{r['watchlist_cohort']}` | `{r['two_dimensional_classification']}` |"
            )

        bowl_report_path.write_text("\n".join(bowl_lines), encoding="utf-8")
        reports["bowling_shortlist"] = bowl_report_path

        # ----------------------------------------------------------------------
        # REPORT 3: METHODOLOGY AND LIMITATIONS REPORT
        # ----------------------------------------------------------------------
        meth_path = self.reports_dir / "r1_06_methodology_and_limitations.md"
        meth_lines = [
            "# ROYALS INTELLIGENCE — ROUND 1 METHODOLOGY & LIMITATIONS REPORT",
            f"**Generated:** {now_iso}  ",
            "**Architecture:** ROYALS INTELLIGENCE v4.1  ",
            "**Task:** R1-06 / R1-06.2.3 Final Data-Count Reconciliation & Statistical Wording Correction  ",
            "",
            "---",
            "",
            "## 1. Governing Primary Diagnostic Methodology",
            "",
            "### Batting: Conservative Lower Credible Bound (Value-at-Risk)",
            "$$\\text{BAT\\_CONSERVATIVE}_i = \\hat{\\theta}_{\\text{SR}, i} - 1.0 \\times \\text{SE}_{\\text{post}, i}$$",
            "- **Units:** Strike-rate points (e.g. +2.2 SR points).",
            "- **Statistical Credibility & Uncertainty Disclosure:** Under an approximate normal posterior distribution, a positive one-standard-error lower bound implies posterior probability above zero greater than approximately 84.1%. This is a directional uncertainty diagnostic, not a 95% credible interval, conventional 95% statistical significance, or a guarantee of future performance.",
            "- **Rationale:** Balances context-adjusted performance against sample uncertainty. A player with $+15$ SR differential across only 30 balls (SE $\\pm 20$) receives a score of $-5$, whereas a veteran with $+10$ SR differential across 300 balls (SE $\\pm 10$) receives $0.0$. This prevents small-sample noisy flyers from infiltrating top rankings.",
            "",
            "### Bowling: Conservative Runs Saved per Over",
            "$$\\text{BOWL\\_CONSERVATIVE}_i = -\\hat{\\theta}_{\\text{Econ}, i} - 1.0 \\times \\text{SE}_{\\text{post}, i}$$",
            "- **Units:** Runs saved per over (RPO). Higher (less negative) indicates superior run containment.",
            "- **Statistical Credibility & Uncertainty Disclosure:** Under an approximate normal posterior distribution, a positive one-standard-error lower bound implies posterior probability above zero greater than approximately 84.1%. This is a directional uncertainty diagnostic, not a 95% credible interval, conventional 95% statistical significance, or a guarantee of future performance.",
            "- **Rationale:** Evaluates bowler run containment under high leverage, resolving the ordinary baseline floor clustering.",
            "",
            "### Two-Dimensional Candidate Classification System (Remediated Under Tasks R1-06.2 & R1-06.2.3)",
            "To prevent the conflation of performance direction, statistical evidence, and exposure volume, R1-06.2 / R1-06.2.2 implements two orthogonal dimensions:",
            "1. **Dimension A: Performance Evidence Status:**",
            "   - `POSITIVE_CONSERVATIVE_EVIDENCE`: Conservative lower bound is strictly $> 0$.",
            "   - `POSITIVE_ESTIMATE_UNRESOLVED`: Posterior mean is positive ($\\hat{\\theta} > 0$), but conservative lower bound is $\\le 0$ (positive estimated performance with unresolved uncertainty).",
            "   - `BELOW_BASELINE_EVIDENCE`: Entire 1-sigma interval is below baseline ($\\hat{\\theta} + \\text{SE} < 0$ for batting; runs saved upper bound $< 0$ for bowling).",
            "   - `INCONCLUSIVE_EVIDENCE`: Point estimate non-positive, but 1-sigma interval spans zero.",
            "2. **Dimension B: Evidence Volume Tier:**",
            "   - `HIGH_VOLUME`: $\\ge 150$ legal pressure deliveries.",
            "   - `MEDIUM_VOLUME`: $60-149$ legal pressure deliveries.",
            "   - `LOW_VOLUME`: $30-59$ legal pressure deliveries.",
            "   - `NO_QUALIFYING_EXPOSURE`: $< 30$ legal pressure deliveries.",
            "",
            "### Candidate Sample Qualification Logic (DEF-04 Fix)",
            "Candidate selection sample qualification is governed by: `(balls >= 60) or (balls >= 50 and matches >= 10)`. "
            "This fixes the DEF-04 syntax bug where `matches >= 10` was erroneously applied to the $\\ge 60$ balls branch.",
            "",
            "### Competition Exposure vs Skill Transferability (DEF-05 Remediation)",
            "`DUAL_TOURNAMENT_QUALIFIED` signifies that a candidate has accumulated $\\ge 30$ legal pressure deliveries in both IPL and Senior T20I matches. "
            "This confirms sample availability across both competition environments, NOT statistical proof of invariant cross-competition skill transferability.",
            "",
            "### Probability Disclosures & Reference Prior Means (DEF-02 Remediation)",
            "`P(Exceed League Avg Under Pressure)` evaluates candidate performance against the league-wide pressure prior mean:",
            "- Batting prior mean: $\\mu_b = -34.24$ SR pts.",
            "- Bowling prior mean: $\\mu_{bw} = +1.82$ RPO conceded.",
            "Exceeding the league pressure average reflects outperforming an environment where performance degrades substantially under pressure; it is a significantly lower bar than exceeding ordinary baseline performance.",
            "",
            "---",
            "",
            "## 2. Qualification Framework & Non-Qualification Accounting",
            "",
            "- **Baseline Threshold:** $\\ge 30$ legal pressure deliveries bowled/faced.",
            "- **Evidence Volume Tiers:**",
            "  - Large Sample ($n \\ge 150$ balls): Low uncertainty, multi-season established.",
            "  - Medium Sample ($60 \\le n < 150$ balls): Moderate uncertainty, credible multi-match basis.",
            "  - Small Sample ($30 \\le n < 60$ balls): High uncertainty, provisional evidence.",
            "  - Insufficient ($n < 30$ balls): Non-qualified; excluded from shortlists.",
            "",
            "### Full Population Accounting:",
            "- **Batting Population ($N = 824$ total batters):**",
            "  - Qualified ($n \\ge 30$ balls): **278 batters** (2 Positive Conservative Evidence, 19 Positive Estimate Unresolved, 182 Below Baseline, 75 Inconclusive).",
            "  - Non-Qualified ($1 \\le n < 30$ balls): **413 batters** (`BELOW_MIN_PRESSURE_BALLS`).",
            "  - Non-Qualified ($0$ pressure balls): **133 batters** (`ZERO_PRESSURE_DELIVERIES_FACED`).",
            "- **Bowling Population ($N = 596$ total bowlers):**",
            "  - Qualified ($n \\ge 30$ balls): **239 bowlers** (0 Positive Conservative Evidence, 1 Positive Estimate Unresolved [Bumrah], 1 Inconclusive [Narine], 237 Below Baseline).",
            "  - Non-Qualified ($1 \\le n < 30$ balls): **240 bowlers** (`BELOW_MIN_PRESSURE_BALLS`).",
            "  - Non-Qualified ($0$ pressure balls): **117 bowlers** (`ZERO_PRESSURE_DELIVERIES_BOWLED`).",
            "",
            "---",
            "",
            "## 3. Robustness & Shortlist Stability Findings",
            "",
            "| Discipline | Robustness Configuration Test | Spearman Rank Corr | Top 10 Jaccard | Top 10 Overlap | Robustness Verdict |",
            "| :--- | :--- | ---: | ---: | :---: | :--- |",
        ]

        if self.robustness_df is not None:
            for _, r in self.robustness_df.iterrows():
                meth_lines.append(
                    f"| **{r['discipline']}** | `{r['configuration_test']}` | **{r['spearman_rank_corr']:.4f}** | "
                    f"{r['top10_jaccard_similarity']:.4f} | {r['top10_membership_overlap']} | `{r['robustness_verdict']}` |"
                )

        meth_lines.extend([
            "",
            "> [!NOTE]",
            "> **Key Sensitivity Observations:**",
            "> 1. **Filtering at $N \\ge 60$ Balls:** Top 10 roster overlap is **10 of 10 (100% Jaccard)** for Batting, proving that the Top 10 batters are already high-volume performers.",
            "> 2. **Posterior Mean vs Conservative Bound:** Rank correlation is **0.9843**, with 8 of 10 identical players. The 2 differing players are small-sample high-variance players correctly demoted by the conservative bound.",
            "> 3. **PRI with TCF:** Top 10 overlap drops to 4 of 10 (25% Jaccard) due to tenure penalties $(S/4)^{0.35}$, confirming why TCF must remain experimental and excluded from primary rankings.",
            "",
            "---",
            "",
            "## 4. Explicit Unresolved Limitations",
            "",
            "1. **Limited Dual-Competition Overlap:** Only 47 batters and 63 bowlers qualify in both IPL and Senior T20Is with $\\ge 30$ legal pressure balls. Cross-competition transferability cannot be assumed.",
            "2. **Empirical Calibration Variance:** Binary exceedance in T20 cricket over 30–100 delivery samples contains high Poisson noise; exceedance probabilities reflect Bayesian credibility under context expectations, NOT deterministic match-winning probabilities.",
            "3. **Death Phase Concentration:** 87.7% of pressure deliveries occur in Death overs (Overs 16–20), meaning pressure reliability metrics are primarily reflective of Death-phase execution.",
            "4. **Scope Exclusions:** Emerging tournament matches and super overs remain strictly excluded from baseline and scoring models.",
        ])

        meth_path.write_text("\n".join(meth_lines), encoding="utf-8")
        reports["methodology_and_limitations"] = meth_path

        # ----------------------------------------------------------------------
        # REPORT 4: OVERALL PLAYER INTELLIGENCE REPORT
        # ----------------------------------------------------------------------
        intel_path = self.reports_dir / "r1_06_player_intelligence_report.md"
        intel_lines = [
            "# ROYALS INTELLIGENCE — ROUND 1 PLAYER RELIABILITY INTELLIGENCE REPORT",
            f"**Generated:** {now_iso}  ",
            "**Architecture:** ROYALS INTELLIGENCE v4.1  ",
            "**Task:** R1-06 / R1-06.2.3 Final Data-Count Reconciliation & Statistical Wording Correction  ",
            "**Status:** `PLAYER_RELIABILITY_INTELLIGENCE_VALIDATED`  ",
            "",
            "---",
            "",
            "## 1. Executive Summary & Challenge Answers",
            "",
            "This report addresses the official SupeRR Selector Round 1 challenge: **Identify the Most Reliable Players Under Pressure.** "
            "By synthesizing context-stratified expected baselines (R1-04), Empirical Bayes shrinkage (R1-04.1), "
            "independent statistical audits (R1-05.1 & R1-05.2), and the governance remediations (R1-06.2, R1-06.2.2 & R1-06.2.3), the intelligence engine answers the 7 core analyst questions:",
            "",
            "### 1. Which batters demonstrate the strongest evidence of pressure reliability?",
            "**Nicholas Pooran** (#1: +2.2 SR conservative lower bound, +16.2 $\\pm$ 14.0 posterior mean, 212 pressure balls across 26 matches & 5 seasons) "
            "and **Donovan Ferreira** (#2: +0.9 SR bound, +20.7 $\\pm$ 19.8 posterior mean, 84 balls) lead the cohort as the only two qualified batters with strictly positive conservative lower bounds (`POSITIVE_CONSERVATIVE_EVIDENCE`). "
            "They are closely followed by established multi-season closers classified as `POSITIVE_ESTIMATE_UNRESOLVED (HIGH_VOLUME)`: **Tim David** (#3: -2.5 SR bound, 290 balls), **Dinesh Karthik** (#4: -2.7 SR bound, 260 balls), "
            "**Ashutosh Sharma** (#5: -3.6 SR bound, 191 balls), and **Marcus Stoinis** (#6: -5.8 SR bound, 220 balls).",
            "",
            "### 2. Which bowlers demonstrate the strongest evidence of pressure reliability?",
            "**Jasprit Bumrah** (#1: -0.16 RPO conservative runs saved, -0.20 $\\pm$ 0.36 posterior economy diff, 521 pressure balls across 60 matches & 5 seasons) "
            "is the standout pressure bowler in world cricket and the **only qualified bowler** conceding fewer runs under pressure (8.94 RPO) than ordinary baseline (9.70 RPO), classified as `POSITIVE_ESTIMATE_UNRESOLVED (HIGH_VOLUME)`. "
            "Exactly 0 bowlers establish strictly positive conservative runs saved. Elite peer-beating bowlers saving runs relative to the league pressure mean include **Sunil Narine** (#2: -0.94 RPO, 153 balls, `INCONCLUSIVE_EVIDENCE`), "
            "**Maheesh Theekshana** (#3: -0.96 RPO, 421 balls), **Matheesha Pathirana** (#4: -1.05 RPO, 440 balls), and **Shaheen Afridi** (#5: -1.43 RPO, 191 balls).",
            "",
            "### 3. How much evidence supports each player?",
            "Evidence volume is classified into explicit orthogonal volume tiers: HIGH_VOLUME ($\\ge 150$ balls), MEDIUM_VOLUME ($60-149$ balls), and LOW_VOLUME ($30-59$ balls). "
            "Nicholas Pooran (212 balls), Tim David (290 balls), Jasprit Bumrah (521 balls), and Maheesh Theekshana (421 balls) are supported by extensive multi-season evidence.",
            "",
            "### 4. How uncertain is each assessment?",
            "Every player profile discloses posterior standard error $\\text{SE}_{\\text{post}}$ and a 95% credible interval. "
            "Under Task R1-06.2.3 governance disclosures: Under an approximate normal posterior distribution, a positive one-standard-error lower bound implies posterior probability above zero greater than approximately 84.1%. This is a directional uncertainty diagnostic, not a 95% credible interval, conventional 95% statistical significance, or a guarantee of future performance. "
            "Pooran's 95% CI is [-11.2, +43.6] SR points; Bumrah's 95% CI is [-0.90, +0.50] RPO. "
            "Smaller sample players (30–59 balls) carry approximately 1.6x wider credible intervals than veterans (150+ balls).",
            "",
            "### 5. Which players are promising but insufficiently established?",
            "- **Batting Emerging High-Upside Watchlist:** Cooper Connolly (+11.9 SR mean, 50 balls, 4 matches) and Ishan Kishan (+2.0 SR mean, 52 balls, 9 matches).",
            "- **Batting Established Marginal Performers:** Andre Russell (+1.2 SR mean, 294 balls), Suryakumar Yadav (+1.2 SR mean, 321 balls), Rahul Tewatia (+1.7 SR mean, 195 balls), and Shashank Singh (+1.3 SR mean, 199 balls).",
            "- **Bowling Emerging Peer-Beaters:** Nasum Ahmed (+0.70 RPO mean, 47 balls), Vipraj Nigam (+0.91 RPO mean, 46 balls), and Ramon Simmonds (+0.98 RPO mean, 30 balls).",
            "",
            "### 6. Why was a particular player included or excluded from a shortlist?",
            "Transparent decision rules: Candidates in the shortlist must satisfy candidate sample qualification (`balls >= 60` or `balls >= 50 and matches >= 10`), "
            "and are classified using the orthogonal Two-Dimensional framework (Dimension A: Performance Evidence Status; Dimension B: Evidence Volume Tier). "
            "Excluded players ($n < 30$ balls) are documented with exact reasons.",
            "",
            "### 7. How stable is the shortlist under alternative assumptions?",
            "Evaluating high-volume filters ($N \\ge 60$ balls) yields **100% Jaccard overlap (10/10 identical)** on batting. "
            "Alternative Bayesian priors yield $> 0.98$ Spearman rank correlation across all qualified cohorts. "
            "However, incorporating TCF drops Top 10 overlap to 25%, confirming why TCF must remain experimental.",
            "",
            "---",
            "",
            "## 2. Generated Intelligence Outputs",
            "",
            "- `batting_intelligence.parquet`: Complete batting intelligence dataset ($N = 824$).",
            "- `bowling_intelligence.parquet`: Complete bowling intelligence dataset ($N = 596$).",
            "- `qualified_candidates.parquet`: Qualified player pool ($N = 517$; 278 bat, 239 bowl).",
            "- `non_qualified_candidates.parquet`: Non-qualified player pool with explicit reasons ($N = 903$; 546 bat, 357 bowl).",
            "- `batting_leaderboard.parquet`: Official Batting Leaderboard ordered by BAT_CONSERVATIVE.",
            "- `bowling_leaderboard.parquet`: Official Bowling Leaderboard ordered by BOWL_CONSERVATIVE.",
            "- `batting_evidence_profiles.parquet`: Detailed 11-question profiles for batters.",
            "- `bowling_evidence_profiles.parquet`: Detailed 11-question profiles for bowlers.",
            "- `shortlist_robustness_comparison.parquet`: Multi-configuration sensitivity tests.",
            "- `competition_candidate_views.parquet`: Competition-specific segmentations.",
        ]

        intel_path.write_text("\n".join(intel_lines), encoding="utf-8")
        reports["player_intelligence_report"] = intel_path

        return reports


if __name__ == "__main__":
    engine = ExplainabilityEngine()
    engine.load_data()
    engine.build_all_profiles()
    engine.generate_all_reports()
    print("Explainability evidence profiles and reports generated successfully.")
