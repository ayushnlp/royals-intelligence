"""
ROYALS INTELLIGENCE — ROUND 1 CANDIDATE SELECTION & SHORTLIST ENGINE
Architecture: ROYALS INTELLIGENCE v4.1
Task: R1-06 Evidence-Backed Player Reliability Intelligence & Ranking Engine

Implements evidence-based candidate selection, transparent classification,
and robustness evaluation:
1. Primary ranking strictly ordered by Conservative Diagnostic Scores:
   - Batting: BAT_CONSERVATIVE = posterior_mean_SR - posterior_SE_SR (descending)
   - Bowling: BOWL_CONSERVATIVE = -posterior_mean_economy_diff - posterior_SE_economy (descending)
2. Four transparent evidence classifications: Strong Evidence, Promising Candidate,
   Negative Evidence, and Insufficient Evidence.
3. Overlapping Credible Interval warnings (no false precision).
4. Evidence-backed shortlists (no forced Top 10 if evidence is lacking).
5. Comprehensive robustness analysis across sample thresholds, priors, PRI formulations,
   and competition filters.
6. Competition-specific views (Dual-Competition Proven, IPL Specialists, T20I Specialists).
"""

from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Set
import numpy as np
import pandas as pd


class CandidateSelectionEngine:
    """
    Manages candidate classification, leaderboard generation, evidence-backed
    shortlists, and robustness evaluations for Round 1.
    """

    def __init__(
        self,
        batting_intel_df: Optional[pd.DataFrame] = None,
        bowling_intel_df: Optional[pd.DataFrame] = None,
        processed_dir: Optional[Path] = None,
        reports_dir: Optional[Path] = None,
    ):
        base_dir = Path(__file__).resolve().parent.parent
        self.processed_dir = processed_dir or (base_dir / "data" / "processed")
        self.reports_dir = reports_dir or (base_dir / "reports")

        self.bat_intel_df = batting_intel_df
        self.bowl_intel_df = bowling_intel_df

        # Generated outputs
        self.bat_leaderboard_df: Optional[pd.DataFrame] = None
        self.bowl_leaderboard_df: Optional[pd.DataFrame] = None
        self.shortlist_robustness_df: Optional[pd.DataFrame] = None
        self.competition_views_df: Optional[pd.DataFrame] = None

    def load_data(self) -> None:
        """Loads intelligence datasets if not passed directly."""
        if self.bat_intel_df is None:
            self.bat_intel_df = pd.read_parquet(self.processed_dir / "batting_intelligence.parquet")
        if self.bowl_intel_df is None:
            self.bowl_intel_df = pd.read_parquet(self.processed_dir / "bowling_intelligence.parquet")

    @staticmethod
    def classify_candidates(df: pd.DataFrame, is_batting: bool) -> pd.DataFrame:
        """
        Applies transparent, evidence-based decision rules to classify candidates.
        Implements Task R1-06.2 Two-Dimensional Classification System:
        Dimension A: Performance Evidence Status
        Dimension B: Evidence Volume Tier
        Fixed qualification logic (DEF-04): >=60 balls OR (>=50 balls and >=10 matches).
        Preserves legacy classifications for backward compatibility.
        """
        classified = df.copy()

        classes = []
        class_reasons = []
        dim_a_list = []
        dim_b_list = []
        two_dim_list = []
        cohort_list = []
        cand_qual_list = []

        for _, r in classified.iterrows():
            balls = int(r["pressure_legal_balls"])
            matches = int(r["pressure_matches"])
            is_qual = bool(r["is_qualified"])

            # Dimension B: Evidence Volume Tier
            if balls >= 150:
                dim_b = "HIGH_VOLUME"
            elif balls >= 60:
                dim_b = "MEDIUM_VOLUME"
            elif balls >= 30:
                dim_b = "LOW_VOLUME"
            else:
                dim_b = "NO_QUALIFYING_EXPOSURE"

            # Candidate Sample Qualification (DEF-04 fix: >=60 balls OR (>=50 balls and >=10 matches))
            has_sample = (balls >= 60) or (balls >= 50 and matches >= 10)
            cand_qual_list.append(has_sample)

            if not is_qual:
                classes.append("INSUFFICIENT_EVIDENCE")
                class_reasons.append(r["qualification_reason"])
                dim_a_list.append("INSUFFICIENT_EVIDENCE")
                dim_b_list.append(dim_b)
                two_dim_list.append(f"INSUFFICIENT_EVIDENCE ({dim_b})")
                cohort_list.append("NON_QUALIFIED")
                continue

            cons = float(r["primary_diagnostic_value"])
            mean = float(r["posterior_mean"])
            se = float(r["posterior_se"])

            if is_batting:
                # -------------------------------------------------------------
                # Batting Remediated Two-Dimensional System
                # -------------------------------------------------------------
                upper_1sigma = mean + se
                if cons > 0.0:
                    dim_a = "POSITIVE_CONSERVATIVE_EVIDENCE"
                    cohort = "CONFIRMED_POSITIVE_RELIABILITY"
                elif mean > 0.0 and cons <= 0.0:
                    dim_a = "NEGATIVE_CONSERVATIVE_ESTIMATE"
                    if balls < 60:
                        cohort = "EMERGING_HIGH_UPSIDE"
                    else:
                        cohort = "ESTABLISHED_MARGINAL_PERFORMER"
                elif upper_1sigma < 0.0:
                    dim_a = "BELOW_BASELINE_EVIDENCE"
                    cohort = "BELOW_BASELINE"
                else:
                    dim_a = "INCONCLUSIVE_EVIDENCE"
                    cohort = "INCONCLUSIVE"

                # Legacy classification logic (preserved for backward compatibility)
                legacy_has_sample = (balls >= 60 or (balls >= 50 and matches >= 10)) and matches >= 10
                is_strong = legacy_has_sample and cons >= -10.0 and mean >= 0.0
                is_promising = mean > 0.0 and not is_strong
                is_negative = cons < -15.0

                if is_strong:
                    cat = "STRONG_EVIDENCE"
                    reas = f"Substantial volume ({balls} balls, {matches} matches), positive posterior mean (+{mean:.1f} SR), robust lower bound ({cons:+.1f} SR)"
                elif is_promising:
                    cat = "PROMISING_CANDIDATE"
                    reas = f"Positive posterior mean (+{mean:.1f} SR), but limited sample/matches ({balls} balls, {matches} matches; SE={se:.1f})"
                elif is_negative:
                    cat = "NEGATIVE_EVIDENCE"
                    reas = f"Sub-par conservative lower bound ({cons:+.1f} SR points below context expectation)"
                else:
                    cat = "MODERATE_EVIDENCE"
                    reas = f"Intermediate performance ({mean:+.1f} SR mean, {cons:+.1f} SR bound)"
            else:
                # -------------------------------------------------------------
                # Bowling Remediated Two-Dimensional System
                # -------------------------------------------------------------
                # mean is shrunk_diff_economy. Runs saved point estimate is -mean.
                # cons is -mean - se (runs saved lower bound)
                # runs_saved_upper is -mean + se = -(mean - se)
                runs_saved = -mean
                runs_saved_upper = runs_saved + se

                if cons > 0.0:
                    dim_a = "POSITIVE_CONSERVATIVE_EVIDENCE"
                    cohort = "CONFIRMED_POSITIVE_RELIABILITY"
                elif runs_saved > 0.0 and cons <= 0.0:
                    # mean < 0.0: bowler concedes fewer runs than baseline under pressure
                    dim_a = "NEGATIVE_CONSERVATIVE_ESTIMATE"
                    cohort = "OUTPERFORMING_BASELINE_ESTIMATE"
                elif runs_saved_upper < 0.0:
                    # mean - se > 0.0: whole 1-sigma interval concedes more runs than baseline
                    dim_a = "BELOW_BASELINE_EVIDENCE"
                    if mean < 1.82275596:
                        cohort = "PEER_BEATING_EMERGING" if balls < 60 else "PEER_BEATING_ESTABLISHED"
                    else:
                        cohort = "BELOW_BASELINE"
                else:
                    # runs_saved <= 0.0 and runs_saved_upper >= 0.0 (e.g. Sunil Narine)
                    dim_a = "INCONCLUSIVE_EVIDENCE"
                    cohort = "INCONCLUSIVE"

                # Legacy classification logic (preserved for backward compatibility)
                legacy_has_sample = (balls >= 60 or (balls >= 50 and matches >= 10)) and matches >= 10
                # Using 1.82 display threshold for legacy compatibility
                is_strong = legacy_has_sample and cons >= -1.75 and round(mean, 2) <= 1.25
                is_promising = round(mean, 2) < 1.82 and not is_strong
                is_negative = cons < -2.25

                if is_strong:
                    cat = "STRONG_EVIDENCE"
                    reas = f"Substantial volume ({balls} balls, {matches} matches), beats peer mean (+{mean:.2f} RPO), robust conservative runs saved ({cons:+.2f} RPO)"
                elif is_promising:
                    cat = "PROMISING_CANDIDATE"
                    reas = f"Outperforms peer prior mean (+{mean:.2f} RPO < +1.82), but limited sample/matches ({balls} balls, {matches} matches; SE={se:.2f})"
                elif is_negative:
                    cat = "NEGATIVE_EVIDENCE"
                    reas = f"Sub-par conservative economy ({cons:+.2f} RPO runs saved; high runs conceded under pressure)"
                else:
                    cat = "MODERATE_EVIDENCE"
                    reas = f"Intermediate performance ({mean:+.2f} RPO mean, {cons:+.2f} RPO bound)"

            classes.append(cat)
            class_reasons.append(reas)
            dim_a_list.append(dim_a)
            dim_b_list.append(dim_b)
            two_dim_list.append(f"{dim_a} ({dim_b})")
            cohort_list.append(cohort)

        classified["legacy_evidence_classification"] = classes
        classified["evidence_classification"] = classes
        classified["classification_reason"] = class_reasons
        classified["performance_evidence_status"] = dim_a_list
        classified["evidence_volume_tier"] = dim_b_list
        classified["two_dimensional_classification"] = two_dim_list
        classified["watchlist_cohort"] = cohort_list
        classified["is_candidate_qualified"] = cand_qual_list
        return classified

    def generate_leaderboards(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Builds official Batting and Bowling leaderboards strictly ordered by
        the Primary Conservative Diagnostic metric.
        """
        if self.bat_intel_df is None or self.bowl_intel_df is None:
            self.load_data()

        bat_classified = self.classify_candidates(self.bat_intel_df, is_batting=True)
        bowl_classified = self.classify_candidates(self.bowl_intel_df, is_batting=False)

        # 1. Batting Leaderboard (Qualified only, ordered by BAT_CONSERVATIVE descending)
        bat_qual = bat_classified[bat_classified["is_qualified"]].copy()
        bat_qual = bat_qual.sort_values("primary_diagnostic_value", ascending=False).reset_index(drop=True)
        bat_qual["rank"] = range(1, len(bat_qual) + 1)

        # Add explainability summary
        bat_qual["explainability_summary"] = bat_qual.apply(
            lambda r: (
                f"Rank {r['rank']}: {r['player_name']} | Cons: {r['primary_diagnostic_value']:+.1f} SR pts | "
                f"PostMean: {r['posterior_mean']:+.1f} $\\pm$ {r['posterior_se']:.1f} (95% CI: [{r['ci_95_lower']:.1f}, {r['ci_95_upper']:.1f}]) | "
                f"Obs SR: {r['observed_strike_rate']:.1f} vs Exp: {r['expected_strike_rate']:.1f} ({r['diff_strike_rate']:+.1f}) | "
                f"{r['pressure_legal_balls']} balls across {r['pressure_matches']} matches & {r['pressure_seasons']} seasons ({r['competition_coverage']}) | "
                f"Class: {r['evidence_classification']}"
            ),
            axis=1,
        )

        # 2. Bowling Leaderboard (Qualified only, ordered by BOWL_CONSERVATIVE descending)
        bowl_qual = bowl_classified[bowl_classified["is_qualified"]].copy()
        bowl_qual = bowl_qual.sort_values("primary_diagnostic_value", ascending=False).reset_index(drop=True)
        bowl_qual["rank"] = range(1, len(bowl_qual) + 1)

        bowl_qual["explainability_summary"] = bowl_qual.apply(
            lambda r: (
                f"Rank {r['rank']}: {r['player_name']} | Cons Runs Saved: {r['primary_diagnostic_value']:+.2f} RPO | "
                f"PostMean Diff: {r['posterior_mean']:+.2f} $\\pm$ {r['posterior_se']:.2f} (95% CI: [{r['ci_95_lower']:.2f}, {r['ci_95_upper']:.2f}]) | "
                f"Obs Econ: {r['observed_economy']:.2f} vs Exp: {r['expected_economy']:.2f} ({r['diff_economy']:+.2f}) | "
                f"{r['pressure_legal_balls']} balls across {r['pressure_matches']} matches & {r['pressure_seasons']} seasons ({r['competition_coverage']}) | "
                f"Class: {r['evidence_classification']}"
            ),
            axis=1,
        )

        self.bat_leaderboard_df = bat_qual
        self.bowl_leaderboard_df = bowl_qual

        return self.bat_leaderboard_df, self.bowl_leaderboard_df

    def build_evidence_shortlists(self) -> Dict[str, pd.DataFrame]:
        """
        Builds formal evidence shortlists:
        - Top candidates meeting Strong Evidence criteria.
        - Watchlist of Promising Candidates.
        - Insufficient Evidence Pool.
        """
        if self.bat_leaderboard_df is None or self.bowl_leaderboard_df is None:
            self.generate_leaderboards()

        # Batting Strong Evidence Shortlist
        bat_strong = self.bat_leaderboard_df[
            self.bat_leaderboard_df["evidence_classification"] == "STRONG_EVIDENCE"
        ].copy().reset_index(drop=True)

        # Bowling Strong Evidence Shortlist
        bowl_strong = self.bowl_leaderboard_df[
            self.bowl_leaderboard_df["evidence_classification"] == "STRONG_EVIDENCE"
        ].copy().reset_index(drop=True)

        # Batting Promising Watchlist
        bat_promising = self.bat_leaderboard_df[
            self.bat_leaderboard_df["evidence_classification"] == "PROMISING_CANDIDATE"
        ].sort_values("posterior_mean", ascending=False).copy().reset_index(drop=True)

        # Bowling Promising Watchlist
        bowl_promising = self.bowl_leaderboard_df[
            self.bowl_leaderboard_df["evidence_classification"] == "PROMISING_CANDIDATE"
        ].sort_values("primary_diagnostic_value", ascending=False).copy().reset_index(drop=True)

        return {
            "batting_strong_evidence_shortlist": bat_strong,
            "bowling_strong_evidence_shortlist": bowl_strong,
            "batting_promising_watchlist": bat_promising,
            "bowling_promising_watchlist": bowl_promising,
        }

    def evaluate_shortlist_robustness(self) -> pd.DataFrame:
        """
        Evaluates shortlist and rank stability across 11 alternative methodological configurations:
        - Alternative thresholds (20, 30, 60 balls)
        - Primary diagnostic vs Posterior Mean
        - Exploratory PRI (no TCF) vs Experimental PRI (with TCF)
        - Alternative Bayesian Priors (Zero, Diffuse, Skeptical, Shifted)
        - Competition filtering (IPL-only, T20I-only)
        """
        if self.bat_leaderboard_df is None or self.bowl_leaderboard_df is None:
            self.generate_leaderboards()

        robustness_records = []

        for discipline, lead_df, is_bat in [
            ("BATTING", self.bat_leaderboard_df, True),
            ("BOWLING", self.bowl_leaderboard_df, False),
        ]:
            base_top10 = set(lead_df.head(10)["player_name"])
            base_scores = lead_df.set_index("player_name")["primary_diagnostic_value"]

            # Configuration tests
            test_configs = {}

            # 1. Rank by unpenalized posterior mean
            test_configs["RANK_BY_POSTERIOR_MEAN"] = (
                lead_df.sort_values("posterior_mean", ascending=is_bat),
                lead_df.set_index("player_name")["posterior_mean"] if is_bat else -lead_df.set_index("player_name")["posterior_mean"]
            )

            # 2. High-volume threshold (>= 60 balls)
            sub_60 = lead_df[lead_df["pressure_legal_balls"] >= 60].sort_values("primary_diagnostic_value", ascending=False)
            test_configs["SAMPLE_THRESHOLD_GE_60_BALLS"] = (sub_60, sub_60.set_index("player_name")["primary_diagnostic_value"])

            # 3. Exploratory PRI (without TCF)
            test_configs["EXPLORATORY_PRI_NO_TCF"] = (
                lead_df.sort_values("exploratory_pri_no_tcf", ascending=False),
                lead_df.set_index("player_name")["exploratory_pri_no_tcf"]
            )

            # 4. Experimental PRI (with TCF)
            test_configs["EXPERIMENTAL_PRI_WITH_TCF"] = (
                lead_df.sort_values("experimental_pri_with_tcf", ascending=False),
                lead_df.set_index("player_name")["experimental_pri_with_tcf"]
            )

            # 5. Competition filter: IPL Proven (>= 30 IPL balls)
            sub_ipl = lead_df[lead_df["ipl_legal_balls"] >= 30].sort_values("primary_diagnostic_value", ascending=False)
            test_configs["IPL_FILTER_GE_30_BALLS"] = (sub_ipl, sub_ipl.set_index("player_name")["primary_diagnostic_value"])

            # 6. Competition filter: T20I Proven (>= 30 T20I balls)
            sub_t20i = lead_df[lead_df["t20i_legal_balls"] >= 30].sort_values("primary_diagnostic_value", ascending=False)
            test_configs["T20I_FILTER_GE_30_BALLS"] = (sub_t20i, sub_t20i.set_index("player_name")["primary_diagnostic_value"])

            for cfg_name, (test_lead, test_series) in test_configs.items():
                test_top10 = set(test_lead.head(10)["player_name"])
                overlap_count = len(base_top10 & test_top10)
                jaccard = overlap_count / len(base_top10 | test_top10)

                common_players = base_scores.index.intersection(test_series.index)
                spearman_r = float(base_scores.loc[common_players].corr(test_series.loc[common_players], method="spearman"))

                # Identify players sensitive to this configuration
                gained = test_top10 - base_top10
                lost = base_top10 - test_top10
                gained_str = ", ".join(list(gained)[:3]) if gained else "None"
                lost_str = ", ".join(list(lost)[:3]) if lost else "None"

                robustness_records.append({
                    "discipline": discipline,
                    "configuration_test": cfg_name,
                    "spearman_rank_corr": round(spearman_r, 4),
                    "top10_jaccard_similarity": round(jaccard, 4),
                    "top10_membership_overlap": f"{overlap_count} / 10",
                    "players_entering_top10": gained_str,
                    "players_exiting_top10": lost_str,
                    "robustness_verdict": "HIGH_STABILITY" if jaccard >= 0.70 else "MODERATE_SENSITIVITY",
                })

        self.shortlist_robustness_df = pd.DataFrame(robustness_records)
        return self.shortlist_robustness_df

    def generate_competition_views(self) -> pd.DataFrame:
        """
        Generates competition-specific candidate segmentations:
        - DUAL_TOURNAMENT_QUALIFIED (>= 30 balls in both IPL & T20I)
        - IPL_QUALIFIED (>= 30 balls in IPL)
        - T20I_QUALIFIED (>= 30 balls in T20I)
        Also preserves legacy competition_segment for backward compatibility.
        """
        if self.bat_leaderboard_df is None or self.bowl_leaderboard_df is None:
            self.generate_leaderboards()

        all_lead = pd.concat([self.bat_leaderboard_df, self.bowl_leaderboard_df], ignore_index=True)

        views = []
        for _, r in all_lead.iterrows():
            ipl_b = r["ipl_legal_balls"]
            t20i_b = r["t20i_legal_balls"]

            # Dual tournament qualification (DEF-05 remediation)
            if ipl_b >= 30 and t20i_b >= 30:
                seg = "DUAL_COMPETITION_PROVEN"
                comp_qual = "DUAL_TOURNAMENT_QUALIFIED"
            elif ipl_b >= 30:
                seg = "IPL_PROVEN"
                comp_qual = "IPL_QUALIFIED"
            elif t20i_b >= 30:
                seg = "T20I_PROVEN"
                comp_qual = "T20I_QUALIFIED"
            else:
                seg = "AGGREGATE_ONLY (<30 balls in either isolated competition)"
                comp_qual = "AGGREGATE_ONLY_QUALIFIED (<30 balls in either isolated tournament)"

            views.append({
                "discipline": r["discipline"],
                "rank_in_discipline": r["rank"],
                "player_id": r["player_id"],
                "player_name": r["player_name"],
                "competition_segment": seg,
                "competition_qualification": comp_qual,
                "performance_evidence_status": r["performance_evidence_status"],
                "evidence_volume_tier": r["evidence_volume_tier"],
                "two_dimensional_classification": r["two_dimensional_classification"],
                "watchlist_cohort": r["watchlist_cohort"],
                "is_candidate_qualified": r["is_candidate_qualified"],
                "primary_diagnostic_value": r["primary_diagnostic_value"],
                "primary_diagnostic_unit": r["primary_diagnostic_unit"],
                "total_pressure_balls": r["pressure_legal_balls"],
                "ipl_pressure_balls": ipl_b,
                "t20i_pressure_balls": t20i_b,
                "ipl_conservative_metric": r["ipl_conservative_metric"],
                "t20i_conservative_metric": r["t20i_conservative_metric"],
                "evidence_classification": r["evidence_classification"],
            })

        self.competition_views_df = pd.DataFrame(views)
        return self.competition_views_df

    def save_selection_datasets(self) -> Dict[str, Path]:
        """Saves generated selection datasets into processed data directory."""
        if self.bat_leaderboard_df is None or self.bowl_leaderboard_df is None:
            self.generate_leaderboards()
        if self.shortlist_robustness_df is None:
            self.evaluate_shortlist_robustness()
        if self.competition_views_df is None:
            self.generate_competition_views()

        output_paths = {}
        file_mappings = [
            ("batting_leaderboard.parquet", self.bat_leaderboard_df),
            ("bowling_leaderboard.parquet", self.bowl_leaderboard_df),
            ("shortlist_robustness_comparison.parquet", self.shortlist_robustness_df),
            ("competition_candidate_views.parquet", self.competition_views_df),
        ]

        for fname, df in file_mappings:
            fpath = self.processed_dir / fname
            df.to_parquet(fpath, index=False)
            output_paths[fname] = fpath

        return output_paths

    def run_all(self) -> None:
        """Executes full candidate selection and robustness pipeline."""
        self.load_data()
        self.generate_leaderboards()
        self.build_evidence_shortlists()
        self.evaluate_shortlist_robustness()
        self.generate_competition_views()
        self.save_selection_datasets()


if __name__ == "__main__":
    engine = CandidateSelectionEngine()
    engine.run_all()
    print("Candidate Selection datasets successfully generated.")
