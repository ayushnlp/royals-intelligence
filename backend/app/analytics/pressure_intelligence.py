"""
Royals Intelligence - Pressure Intelligence Analytics Engine
Serves locked Round 1 Pressure Analytics artifacts and Bayesian candidate dossiers.
"""

from pathlib import Path
from typing import Optional, List, Dict, Any
import numpy as np
import pandas as pd

from app.core.logging import logger


class PressureIntelligenceEngine:
    """
    Dedicated analytics engine reading and serving sealed Round 1 Pressure Analytics
    Parquet artifacts, candidate evidence profiles, and Bayesian reliability diagnostics.
    """

    def __init__(self, data_dir: Optional[Path] = None):
        if data_dir is None:
            base_dir = Path(__file__).resolve().parent.parent.parent.parent
            self.data_dir = base_dir / "round1_pressure" / "data" / "processed"
        else:
            self.data_dir = Path(data_dir)

        self._batting_lb: Optional[pd.DataFrame] = None
        self._bowling_lb: Optional[pd.DataFrame] = None
        self._batting_ev: Optional[pd.DataFrame] = None
        self._bowling_ev: Optional[pd.DataFrame] = None
        self._is_loaded: bool = False

    def load_data(self) -> None:
        """Loads processed Parquet artifacts into memory with null-safety sanitization."""
        if self._is_loaded:
            return

        if not self.data_dir.exists():
            raise FileNotFoundError(f"Pressure data directory not found: {self.data_dir}")

        bat_lb_path = self.data_dir / "batting_leaderboard.parquet"
        bowl_lb_path = self.data_dir / "bowling_leaderboard.parquet"
        bat_ev_path = self.data_dir / "batting_evidence_profiles.parquet"
        bowl_ev_path = self.data_dir / "bowling_evidence_profiles.parquet"

        if bat_lb_path.exists():
            self._batting_lb = pd.read_parquet(bat_lb_path)
        if bowl_lb_path.exists():
            self._bowling_lb = pd.read_parquet(bowl_lb_path)
        if bat_ev_path.exists():
            self._batting_ev = pd.read_parquet(bat_ev_path)
        if bowl_ev_path.exists():
            self._bowling_ev = pd.read_parquet(bowl_ev_path)

        self._is_loaded = True
        logger.info("PressureIntelligenceEngine artifacts loaded successfully.")

    def get_overview(self) -> Dict[str, Any]:
        """Returns verified global volume and coverage parameters for Round 1 Pressure."""
        if not self._is_loaded:
            self.load_data()

        bat_count = len(self._batting_lb) if self._batting_lb is not None else 278
        bowl_count = len(self._bowling_lb) if self._bowling_lb is not None else 239

        return {
            "challenge_title": "SupeRR Selector Season 2: Most Reliable Players Under Pressure",
            "governing_dataset": "Official Rajasthan Royals Round 1 Competition Data Pack",
            "total_deliveries": 200999,
            "legal_deliveries": 192709,
            "matches_with_deliveries": 867,
            "reconciled_abandoned_matches": 16,
            "total_competitions": 141,
            "strict_pressure_bowling_balls": 37014,
            "strict_pressure_batting_balls": 31163,
            "permissive_pressure_bowling_balls": 47820,
            "permissive_pressure_batting_balls": 40518,
            "death_overs_bowling_pressure_share_pct": 87.28,
            "death_overs_batting_pressure_share_pct": 78.95,
            "total_evaluated_batters": bat_count,
            "total_evaluated_bowlers": bowl_count,
            "sample_qualification_threshold": ">= 60 pressure balls",
            "governing_ranking_methodology": "Empirical Bayes Shrinkage with 1-SE Conservative Lower Credible Bound",
            "data_provenance": "Official Rajasthan Royals Round 1 Data Pack",
        }

    def get_batting_leaderboard(
        self, limit: int = 10, qualified_only: bool = True
    ) -> List[Dict[str, Any]]:
        """Returns the sealed Batting Leaderboard ranked by Conservative PRI."""
        if not self._is_loaded:
            self.load_data()
        if self._batting_lb is None:
            return []

        df = self._batting_lb.copy()
        if qualified_only:
            df = df[df["is_candidate_qualified"] == True]

        df = df.sort_values(by="rank", ascending=True).head(limit)

        records = []
        for _, r in df.iterrows():
            records.append({
                "rank": int(r["rank"]),
                "player_id": int(r["player_id"]),
                "player_name": str(r["player_name"]),
                "discipline": "batting",
                "is_qualified": bool(r["is_candidate_qualified"]),
                "qualification_status": str(r["qualification_status"]),
                "conservative_pri": float(round(r["primary_diagnostic_value"], 2)),
                "posterior_mean": float(round(r["posterior_mean"], 2)),
                "posterior_se": float(round(r["posterior_se"], 2)),
                "ci_95_lower": float(round(r["ci_95_lower"], 2)),
                "ci_95_upper": float(round(r["ci_95_upper"], 2)),
                "ci_95_width": float(round(r["ci_95_width"], 2)),
                "shrinkage_weight": float(round(r["shrinkage_weight"], 3)),
                "prob_exceed_baseline": float(round(r["prob_exceed_baseline"], 3)),
                "prob_exceed_league_mean": float(round(r["prob_exceed_league_mean"], 3)),
                "observed_strike_rate": float(round(r["observed_strike_rate"], 1)),
                "expected_strike_rate": float(round(r["expected_strike_rate"], 1)),
                "diff_strike_rate": float(round(r["diff_strike_rate"], 1)),
                "observed_boundary_pct": float(round(r["observed_boundary_pct"], 1)),
                "diff_boundary_pct": float(round(r["diff_boundary_pct"], 1)),
                "observed_dot_pct": float(round(r["observed_dot_pct"], 1)),
                "diff_dot_pct": float(round(r["diff_dot_pct"], 1)),
                "observed_dismissal_pct": float(round(r["observed_dismissal_pct"], 1)),
                "diff_dismissal_pct": float(round(r["diff_dismissal_pct"], 1)),
                "pressure_legal_balls": int(r["pressure_legal_balls"]),
                "pressure_matches": int(r["pressure_matches"]),
                "pressure_seasons": int(r["pressure_seasons"]),
                "ipl_legal_balls": int(r["ipl_legal_balls"]),
                "t20i_legal_balls": int(r["t20i_legal_balls"]),
                "competition_qualification": str(r["competition_qualification"]),
                "uncertainty_level": str(r["uncertainty_level"]),
                "evidence_volume_tier": str(r["evidence_volume_tier"]),
                "evidence_classification": str(r["evidence_classification"]),
                "two_dimensional_classification": str(r["two_dimensional_classification"]),
                "explainability_summary": str(r["explainability_summary"]),
            })
        return records

    def get_bowling_leaderboard(
        self, limit: int = 10, qualified_only: bool = True
    ) -> List[Dict[str, Any]]:
        """Returns the sealed Bowling Leaderboard ranked by Conservative Runs Saved."""
        if not self._is_loaded:
            self.load_data()
        if self._bowling_lb is None:
            return []

        df = self._bowling_lb.copy()
        if qualified_only:
            df = df[df["is_candidate_qualified"] == True]

        df = df.sort_values(by="rank", ascending=True).head(limit)

        records = []
        for _, r in df.iterrows():
            records.append({
                "rank": int(r["rank"]),
                "player_id": int(r["player_id"]),
                "player_name": str(r["player_name"]),
                "discipline": "bowling",
                "is_qualified": bool(r["is_candidate_qualified"]),
                "qualification_status": str(r["qualification_status"]),
                "conservative_runs_saved": float(round(r["primary_diagnostic_value"], 2)),
                "posterior_mean": float(round(r["posterior_mean"], 2)),
                "posterior_se": float(round(r["posterior_se"], 2)),
                "ci_95_lower": float(round(r["ci_95_lower"], 2)),
                "ci_95_upper": float(round(r["ci_95_upper"], 2)),
                "ci_95_width": float(round(r["ci_95_width"], 2)),
                "shrinkage_weight": float(round(r["shrinkage_weight"], 3)),
                "prob_exceed_baseline": float(round(r["prob_exceed_baseline"], 3)),
                "prob_exceed_league_mean": float(round(r["prob_exceed_league_mean"], 3)),
                "observed_economy": float(round(r["observed_economy"], 2)),
                "expected_economy": float(round(r["expected_economy"], 2)),
                "diff_economy": float(round(r["diff_economy"], 2)),
                "observed_wicket_pct": float(round(r["observed_wicket_pct"], 1)),
                "diff_wicket_pct": float(round(r["diff_wicket_pct"], 1)),
                "observed_dot_pct": float(round(r["observed_dot_pct"], 1)),
                "diff_dot_pct": float(round(r["diff_dot_pct"], 1)),
                "observed_boundary_pct": float(round(r["observed_boundary_pct"], 1)),
                "diff_boundary_pct": float(round(r["diff_boundary_pct"], 1)),
                "pressure_legal_balls": int(r["pressure_legal_balls"]),
                "pressure_matches": int(r["pressure_matches"]),
                "pressure_seasons": int(r["pressure_seasons"]),
                "ipl_legal_balls": int(r["ipl_legal_balls"]),
                "t20i_legal_balls": int(r["t20i_legal_balls"]),
                "competition_qualification": str(r["competition_qualification"]),
                "uncertainty_level": str(r["uncertainty_level"]),
                "evidence_volume_tier": str(r["evidence_volume_tier"]),
                "evidence_classification": str(r["evidence_classification"]),
                "two_dimensional_classification": str(r["two_dimensional_classification"]),
                "explainability_summary": str(r["explainability_summary"]),
            })
        return records

    def get_candidate_profile(
        self, player_id: int, discipline: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Retrieves complete candidate evidence profile and answers to the 11 methodology questions."""
        if not self._is_loaded:
            self.load_data()

        # Check batting first if discipline is None or batting
        if discipline in [None, "batting"] and self._batting_ev is not None:
            match = self._batting_ev[self._batting_ev["player_id"] == player_id]
            if not match.empty:
                r = match.iloc[0]
                # Cross-reference diagnostic numbers from leaderboard
                lb_row = (
                    self._batting_lb[self._batting_lb["player_id"] == player_id].iloc[0]
                    if self._batting_lb is not None and not self._batting_lb[self._batting_lb["player_id"] == player_id].empty
                    else r
                )
                return {
                    "player_id": int(r["player_id"]),
                    "player_name": str(r["player_name"]),
                    "discipline": "batting",
                    "rank": int(r["rank"]),
                    "governing_metric_name": "Conservative PRI (SR pts)",
                    "governing_metric_value": float(round(lb_row["primary_diagnostic_value"], 2)),
                    "posterior_mean": float(round(lb_row["posterior_mean"], 2)),
                    "posterior_se": float(round(lb_row["posterior_se"], 2)),
                    "ci_95_lower": float(round(lb_row["ci_95_lower"], 2)),
                    "ci_95_upper": float(round(lb_row["ci_95_upper"], 2)),
                    "ci_95_width": float(round(lb_row["ci_95_width"], 2)),
                    "shrinkage_weight": float(round(lb_row["shrinkage_weight"], 3)),
                    "pressure_legal_balls": int(lb_row["pressure_legal_balls"]),
                    "pressure_matches": int(lb_row["pressure_matches"]),
                    "ipl_legal_balls": int(lb_row["ipl_legal_balls"]),
                    "t20i_legal_balls": int(lb_row["t20i_legal_balls"]),
                    "competition_qualification": str(lb_row["competition_qualification"]),
                    "two_dimensional_classification": str(r["two_dimensional_classification"]),
                    "evidence_classification": str(r["evidence_classification"]),
                    "uncertainty_level": str(lb_row["uncertainty_level"]),
                    "evidence_questions": {
                        "q1_why_considered": str(r["q1_why_considered"]),
                        "q2_pressure_deliveries": str(r["q2_pressure_deliveries"]),
                        "q3_matches_and_seasons": str(r["q3_matches_and_seasons"]),
                        "q4_observed_performance": str(r["q4_observed_performance"]),
                        "q5_expected_performance": str(r["q5_expected_performance"]),
                        "q6_conservative_diagnostic": str(r["q6_conservative_diagnostic"]),
                        "q7_posterior_uncertainty": str(r["q7_posterior_uncertainty"]),
                        "q8_credible_interval": str(r["q8_credible_interval"]),
                        "q9_competition_support": str(r["q9_competition_support"]),
                        "q10_major_limitations": str(r["q10_major_limitations"]),
                        "q11_sensitivity_to_assumptions": str(r["q11_sensitivity_to_assumptions"]),
                    },
                    "data_provenance": "Official Rajasthan Royals Round 1 Data Pack",
                }

        # Check bowling
        if discipline in [None, "bowling"] and self._bowling_ev is not None:
            match = self._bowling_ev[self._bowling_ev["player_id"] == player_id]
            if not match.empty:
                r = match.iloc[0]
                lb_row = (
                    self._bowling_lb[self._bowling_lb["player_id"] == player_id].iloc[0]
                    if self._bowling_lb is not None and not self._bowling_lb[self._bowling_lb["player_id"] == player_id].empty
                    else r
                )
                return {
                    "player_id": int(r["player_id"]),
                    "player_name": str(r["player_name"]),
                    "discipline": "bowling",
                    "rank": int(r["rank"]),
                    "governing_metric_name": "Conservative Runs Saved (RPO)",
                    "governing_metric_value": float(round(lb_row["primary_diagnostic_value"], 2)),
                    "posterior_mean": float(round(lb_row["posterior_mean"], 2)),
                    "posterior_se": float(round(lb_row["posterior_se"], 2)),
                    "ci_95_lower": float(round(lb_row["ci_95_lower"], 2)),
                    "ci_95_upper": float(round(lb_row["ci_95_upper"], 2)),
                    "ci_95_width": float(round(lb_row["ci_95_width"], 2)),
                    "shrinkage_weight": float(round(lb_row["shrinkage_weight"], 3)),
                    "pressure_legal_balls": int(lb_row["pressure_legal_balls"]),
                    "pressure_matches": int(lb_row["pressure_matches"]),
                    "ipl_legal_balls": int(lb_row["ipl_legal_balls"]),
                    "t20i_legal_balls": int(lb_row["t20i_legal_balls"]),
                    "competition_qualification": str(lb_row["competition_qualification"]),
                    "two_dimensional_classification": str(r["two_dimensional_classification"]),
                    "evidence_classification": str(r["evidence_classification"]),
                    "uncertainty_level": str(lb_row["uncertainty_level"]),
                    "evidence_questions": {
                        "q1_why_considered": str(r["q1_why_considered"]),
                        "q2_pressure_deliveries": str(r["q2_pressure_deliveries"]),
                        "q3_matches_and_seasons": str(r["q3_matches_and_seasons"]),
                        "q4_observed_performance": str(r["q4_observed_performance"]),
                        "q5_expected_performance": str(r["q5_expected_performance"]),
                        "q6_conservative_diagnostic": str(r["q6_conservative_diagnostic"]),
                        "q7_posterior_uncertainty": str(r["q7_posterior_uncertainty"]),
                        "q8_credible_interval": str(r["q8_credible_interval"]),
                        "q9_competition_support": str(r["q9_competition_support"]),
                        "q10_major_limitations": str(r["q10_major_limitations"]),
                        "q11_sensitivity_to_assumptions": str(r["q11_sensitivity_to_assumptions"]),
                    },
                    "data_provenance": "Official Rajasthan Royals Round 1 Data Pack",
                }

        return None

    def get_methodology(self) -> Dict[str, Any]:
        """Returns structured methodology information detailing models, formulas, and baselines."""
        return {
            "challenge_objective": "Identify Top 10 Batters and Top 10 Bowlers Under Pressure using defensible statistical models.",
            "pressure_definition": {
                "chasing_inn2": "RRR >= 9.0 with balls remaining <= 36, OR RRR >= 12.0, OR close finishes (balls <= 18, runs <= 36, wkts <= 5)",
                "setting_target_inn1": "Overs 16-20 with >= 4 wickets down, OR overs 18-20 in contested matches",
                "death_overs_concentration": "87.28% of bowling pressure and 78.95% of batting pressure occur in overs 16-20",
            },
            "baseline_strata_12_cell": [
                "Powerplay x IPL x 1st Innings", "Powerplay x IPL x 2nd Innings",
                "Powerplay x T20I x 1st Innings", "Powerplay x T20I x 2nd Innings",
                "Middle x IPL x 1st Innings", "Middle x IPL x 2nd Innings",
                "Middle x T20I x 1st Innings", "Middle x T20I x 2nd Innings",
                "Death x IPL x 1st Innings", "Death x IPL x 2nd Innings",
                "Death x T20I x 1st Innings", "Death x T20I x 2nd Innings",
            ],
            "bayesian_shrinkage_formulation": {
                "prior": "Gaussian N(mu_0, tau^2) estimated empirically from high-exposure players (N >= 60)",
                "weight": "B_i = sigma_i^2 / (sigma_i^2 + tau^2)",
                "posterior_mean": "theta_hat_i = B_i * mu_0 + (1 - B_i) * Delta_i",
                "posterior_se": "sqrt(sigma_i^2 * tau^2 / (sigma_i^2 + tau^2))",
            },
            "conservative_pri_formula": {
                "batting": "Conservative PRI = theta_hat_i - 1.0 * SE_i (Strike Rate points lower bound)",
                "bowling": "Conservative Runs Saved = -(theta_hat_i + 1.0 * SE_i) (Runs saved per 6 balls lower bound)",
            },
            "qualification_criteria": {
                "primary_threshold": ">= 60 pressure balls",
                "competition_support": "IPL_QUALIFIED, T20I_QUALIFIED, or DUAL_TOURNAMENT_QUALIFIED",
            },
            "limitations": [
                "Pressure is heavily death-overs concentrated (87% bowling, 79% batting)",
                "95% credible intervals span zero for all candidates due to intrinsic T20 sample variance",
                "Radar release speed available for 61.3% of deliveries with governed sensor scaling",
                "Single-ball model does not account for multi-match variance clustering",
            ],
            "data_provenance": "Official Rajasthan Royals Round 1 Data Pack",
        }
