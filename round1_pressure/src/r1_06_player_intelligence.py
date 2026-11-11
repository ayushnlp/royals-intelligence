"""
ROYALS INTELLIGENCE — ROUND 1 PLAYER RELIABILITY INTELLIGENCE ENGINE
Architecture: ROYALS INTELLIGENCE v4.1
Task: R1-06 Evidence-Backed Player Reliability Intelligence & Ranking Engine

Constructs comprehensive, independent intelligence profiles for all batters and bowlers
participating in primary ordinary matches. Integrates:
1. Primary diagnostic metrics in native units:
   - Batting: BAT_CONSERVATIVE = posterior_mean_SR - posterior_SE_SR (strike-rate points)
   - Bowling: BOWL_CONSERVATIVE = -posterior_mean_economy_diff - posterior_SE_economy (runs saved/over)
2. Statistical uncertainty bounds: posterior SE, 95% Credible Intervals, shrinkage weights.
3. Model-derived exceedance probabilities against baseline and pressured peers.
4. Multi-season, multi-match, and phase-level context distributions.
5. Strict, transparent qualification framework with explicit non-qualification reasons for all excluded players.
6. Competition-specific exposure and performance accounting (IPL vs Senior T20I).
7. Exploratory PRI (without TCF) and experimental PRI (with TCF) references.
"""

from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import numpy as np
import pandas as pd
from scipy.stats import norm


class PlayerIntelligenceEngine:
    """
    Constructs unified, fully explained player intelligence datasets
    for batters and bowlers across all primary ordinary matches.
    """

    IPL_COMP_IDS = {1358, 1715, 2193, 2725, 3298}
    QUALIFIED_BALLS_MIN = 30

    def __init__(
        self,
        processed_dir: Optional[Path] = None,
        reports_dir: Optional[Path] = None,
    ):
        base_dir = Path(__file__).resolve().parent.parent
        self.processed_dir = processed_dir or (base_dir / "data" / "processed")
        self.reports_dir = reports_dir or (base_dir / "reports")

        self.processed_dir.mkdir(parents=True, exist_ok=True)
        self.reports_dir.mkdir(parents=True, exist_ok=True)

        # Loaded Datasets
        self.bat_reliability_df: Optional[pd.DataFrame] = None
        self.bowl_reliability_df: Optional[pd.DataFrame] = None
        self.bat_events_df: Optional[pd.DataFrame] = None
        self.bowl_events_df: Optional[pd.DataFrame] = None
        self.deliv_states_df: Optional[pd.DataFrame] = None
        self.bayesian_summary_df: Optional[pd.DataFrame] = None

        # Generated Intelligence Datasets
        self.batting_intelligence_df: Optional[pd.DataFrame] = None
        self.bowling_intelligence_df: Optional[pd.DataFrame] = None
        self.qualified_candidates_df: Optional[pd.DataFrame] = None
        self.non_qualified_candidates_df: Optional[pd.DataFrame] = None

    def load_data(self) -> None:
        """Loads all required processed datasets from R1-03, R1-04, and R1-05."""
        self.bat_reliability_df = pd.read_parquet(self.processed_dir / "batting_pressure_reliability.parquet")
        self.bowl_reliability_df = pd.read_parquet(self.processed_dir / "bowling_pressure_reliability.parquet")
        self.bat_events_df = pd.read_parquet(self.processed_dir / "batting_pressure_events_strict.parquet")
        self.bowl_events_df = pd.read_parquet(self.processed_dir / "bowling_pressure_events_strict.parquet")
        self.deliv_states_df = pd.read_parquet(self.processed_dir / "delivery_states_strict.parquet")
        self.bayesian_summary_df = pd.read_parquet(self.processed_dir / "bayesian_shrinkage_summary.parquet")

        # Assign helper fields
        for df in [self.bat_events_df, self.bowl_events_df, self.deliv_states_df]:
            if "comp_tier" not in df.columns:
                df["comp_tier"] = np.where(df["comp_id"].isin(self.IPL_COMP_IDS), "IPL", "Senior T20I")

    @staticmethod
    def _min_max_scale(series: pd.Series) -> pd.Series:
        """Min-max scales series to 0-100 range across cohort."""
        s_min, s_max = series.min(), series.max()
        if s_max > s_min:
            return (series - s_min) / (s_max - s_min) * 100.0
        return pd.Series(50.0, index=series.index)

    def _build_season_distribution_map(self, df_events: pd.DataFrame, is_batting: bool) -> Dict[str, str]:
        """Builds a formatted string detailing seasonal ball counts for each player."""
        pres_mask = df_events["is_primary_scope"] & df_events["outcome_is_legal"] & df_events["is_pressure_event"]
        pres_df = df_events[pres_mask]
        player_col = "player_id"

        dist_map = {}
        for pid, grp in pres_df.groupby(player_col):
            season_counts = grp.groupby("season").size()
            parts = [f"{s}: {c}b" for s, c in season_counts.items()]
            dist_map[pid] = ", ".join(parts)
        return dist_map

    def _compute_competition_specific_metrics(
        self, df_events: pd.DataFrame, is_batting: bool
    ) -> Dict[str, Dict[str, Any]]:
        """
        Computes competition-specific sample counts and conservative performance
        separately for IPL and Senior T20I.
        """
        pres_mask = df_events["is_primary_scope"] & df_events["outcome_is_legal"] & df_events["is_pressure_event"]
        pres_df = df_events[pres_mask]

        run_col = "outcome_runs_batter" if is_batting else "outcome_conceded_runs"
        scale = 100.0 if is_batting else 6.0

        # Context baselines by competition
        ord_mask = df_events["is_primary_scope"] & df_events["outcome_is_legal"] & (~df_events["is_pressure_event"])
        ord_df = df_events[ord_mask]
        base_map = ord_df.groupby(
            ["comp_tier", "innings", "innings_phase"], observed=False
        )[run_col].mean().to_dict()

        pres_copy = pres_df.copy()
        pres_copy["exp_runs"] = pres_copy.apply(
            lambda r: base_map.get((r["comp_tier"], r["innings"], r["innings_phase"]), 1.3), axis=1
        )

        comp_records = {}
        for pid, grp in pres_copy.groupby("player_id"):
            ipl_grp = grp[grp["comp_tier"] == "IPL"]
            t20i_grp = grp[grp["comp_tier"] == "Senior T20I"]

            ipl_balls = len(ipl_grp)
            t20i_balls = len(t20i_grp)

            # IPL metrics
            if ipl_balls >= 20:
                ipl_obs = ipl_grp[run_col].sum()
                ipl_exp = ipl_grp["exp_runs"].sum()
                ipl_var = ipl_grp[run_col].var() if ipl_balls > 1 else 2.0
                ipl_diff = (ipl_obs - ipl_exp) / ipl_balls * scale
                ipl_se = (np.sqrt(ipl_var) / np.sqrt(ipl_balls)) * scale
                ipl_cons = (ipl_diff - ipl_se) if is_batting else (-ipl_diff - ipl_se)
            else:
                ipl_diff, ipl_se, ipl_cons = np.nan, np.nan, np.nan

            # T20I metrics
            if t20i_balls >= 20:
                t20i_obs = t20i_grp[run_col].sum()
                t20i_exp = t20i_grp["exp_runs"].sum()
                t20i_var = t20i_grp[run_col].var() if t20i_balls > 1 else 2.0
                t20i_diff = (t20i_obs - t20i_exp) / t20i_balls * scale
                t20i_se = (np.sqrt(t20i_var) / np.sqrt(t20i_balls)) * scale
                t20i_cons = (t20i_diff - t20i_se) if is_batting else (-t20i_diff - t20i_se)
            else:
                t20i_diff, t20i_se, t20i_cons = np.nan, np.nan, np.nan

            comp_records[pid] = {
                "ipl_pressure_balls": ipl_balls,
                "t20i_pressure_balls": t20i_balls,
                "ipl_diff": round(ipl_diff, 2) if not np.isnan(ipl_diff) else None,
                "ipl_se": round(ipl_se, 2) if not np.isnan(ipl_se) else None,
                "ipl_conservative_metric": round(ipl_cons, 2) if not np.isnan(ipl_cons) else None,
                "t20i_diff": round(t20i_diff, 2) if not np.isnan(t20i_diff) else None,
                "t20i_se": round(t20i_se, 2) if not np.isnan(t20i_se) else None,
                "t20i_conservative_metric": round(t20i_cons, 2) if not np.isnan(t20i_cons) else None,
            }

        return comp_records

    def build_batting_intelligence(self) -> pd.DataFrame:
        """Constructs complete batting reliability intelligence dataset for all batters."""
        df_rel = self.bat_reliability_df.copy()

        # Build maps
        season_dist_map = self._build_season_distribution_map(self.bat_events_df, is_batting=True)
        comp_metrics_map = self._compute_competition_specific_metrics(self.bat_events_df, is_batting=True)

        # Identify all batters in primary ordinary scope to capture 0-pressure ball batters
        prim_batters = self.deliv_states_df[self.deliv_states_df["is_primary_scope"]].groupby(
            ["striker_id", "striker_name"]
        ).size().reset_index().rename(columns={"striker_id": "player_id", "striker_name": "player_name", 0: "total_balls_faced"})

        existing_pids = set(df_rel["player_id"])
        zero_pressure_batters = prim_batters[~prim_batters["player_id"].isin(existing_pids)].copy()

        # Compute Exploratory PRI (without TCF) for qualified players
        qual_mask = df_rel["is_qualified"]
        qual_df = df_rel[qual_mask].copy()
        z_cons = self._min_max_scale(qual_df["score_conservative_bound"])
        z_bnd = self._min_max_scale(qual_df["diff_boundary_pct"])
        z_dot = self._min_max_scale(-qual_df["diff_dot_pct"])
        z_dism = self._min_max_scale(-qual_df["diff_dismissal_pct"])
        raw_pri_no_tcf = 0.45 * z_cons + 0.20 * z_bnd + 0.20 * z_dot + 0.15 * z_dism
        scaled_pri_no_tcf = self._min_max_scale(raw_pri_no_tcf)
        df_rel["exploratory_pri_no_tcf"] = np.nan
        df_rel.loc[qual_mask, "exploratory_pri_no_tcf"] = scaled_pri_no_tcf

        records = []
        for _, r in df_rel.iterrows():
            pid = r["player_id"]
            balls = int(r["pressure_legal_balls"])
            is_qual = bool(r["is_qualified"])

            # Evidence volume tier (Dimension B standard)
            if balls >= 150:
                vol_tier = "HIGH_VOLUME"
                legacy_vol_tier = "Large Sample (>=150 balls)"
                unc_level = "LOW"
            elif balls >= 60:
                vol_tier = "MEDIUM_VOLUME"
                legacy_vol_tier = "Medium Sample (60-149 balls)"
                unc_level = "MEDIUM"
            elif balls >= 30:
                vol_tier = "LOW_VOLUME"
                legacy_vol_tier = "Small Sample (30-59 balls)"
                unc_level = "HIGH"
            else:
                vol_tier = "NO_QUALIFYING_EXPOSURE"
                legacy_vol_tier = "Insufficient (<30 balls)"
                unc_level = "VERY_HIGH"

            # Qualification status and reason
            if is_qual:
                qual_status = "QUALIFIED"
                qual_reason = f"QUALIFIED_SAMPLE_GE_30_BALLS ({balls} balls)"
            else:
                qual_status = "NOT_QUALIFIED"
                qual_reason = f"BELOW_MIN_PRESSURE_BALLS: {balls} of 30 required balls"

            # Candidate sample qualification (DEF-04 fix: >=60 balls OR (>=50 balls and >=10 matches))
            cand_qual = bool((balls >= 60) or (balls >= 50 and int(r["pressure_matches"]) >= 10))

            # Competition coverage and qualification (DEF-05 remediation)
            ipl_b = int(r["ipl_legal_balls"])
            t20i_b = int(r["t20i_legal_balls"])
            if ipl_b >= 30 and t20i_b >= 30:
                comp_qual = "DUAL_TOURNAMENT_QUALIFIED"
            elif ipl_b >= 30:
                comp_qual = "IPL_QUALIFIED"
            elif t20i_b >= 30:
                comp_qual = "T20I_QUALIFIED"
            else:
                comp_qual = "AGGREGATE_ONLY_QUALIFIED (<30 balls in either isolated tournament)"

            if ipl_b >= 20 and t20i_b >= 20:
                comp_cov = "BOTH"
            elif ipl_b > 0 and t20i_b == 0:
                comp_cov = "IPL_ONLY"
            elif t20i_b > 0 and ipl_b == 0:
                comp_cov = "T20I_ONLY"
            elif ipl_b >= t20i_b:
                comp_cov = "IPL_DOMINANT"
            else:
                comp_cov = "T20I_DOMINANT"

            comp_data = comp_metrics_map.get(pid, {})
            dist_str = season_dist_map.get(pid, "None")

            post_mean = r["shrunk_diff_strike_rate"]
            post_se = r["posterior_se_strike_rate"]
            cons_bound = r["score_conservative_bound"]

            records.append({
                "player_id": pid,
                "player_name": r["player_name"],
                "discipline": "BATTING",
                "is_qualified": is_qual,
                "qualification_status": qual_status,
                "qualification_reason": qual_reason,
                "is_candidate_qualified": cand_qual,
                "evidence_volume_tier": vol_tier,
                "legacy_evidence_volume_tier": legacy_vol_tier,
                "uncertainty_level": unc_level,
                "primary_diagnostic_name": "BAT_CONSERVATIVE",
                "primary_diagnostic_value": float(cons_bound) if pd.notna(cons_bound) else np.nan,
                "primary_diagnostic_unit": "SR_POINTS",
                "posterior_mean": float(post_mean) if pd.notna(post_mean) else np.nan,
                "posterior_se": float(post_se) if pd.notna(post_se) else np.nan,
                "ci_95_lower": float(r["ci_95_lower_strike_rate"]) if pd.notna(r["ci_95_lower_strike_rate"]) else np.nan,
                "ci_95_upper": float(r["ci_95_upper_strike_rate"]) if pd.notna(r["ci_95_upper_strike_rate"]) else np.nan,
                "ci_95_width": float(r["ci_95_upper_strike_rate"] - r["ci_95_lower_strike_rate"]) if pd.notna(r["ci_95_lower_strike_rate"]) else np.nan,
                "shrinkage_weight": float(r["reliability_strike_rate"]) if pd.notna(r["reliability_strike_rate"]) else np.nan,
                "prob_exceed_baseline": float(r["prob_exceed_baseline"]) if pd.notna(r["prob_exceed_baseline"]) else np.nan,
                "prob_exceed_peers": float(r["prob_exceed_peer_mean"]) if pd.notna(r["prob_exceed_peer_mean"]) else np.nan,
                "prob_exceed_league_mean": float(r["prob_exceed_peer_mean"]) if pd.notna(r["prob_exceed_peer_mean"]) else np.nan,
                "observed_strike_rate": round(float(r["observed_strike_rate"]), 2),
                "expected_strike_rate": round(float(r["expected_strike_rate"]), 2),
                "diff_strike_rate": round(float(r["diff_strike_rate"]), 2),
                "observed_boundary_pct": round(float(r["observed_boundary_pct"]), 2),
                "diff_boundary_pct": round(float(r["diff_boundary_pct"]), 2),
                "observed_dot_pct": round(float(r["observed_dot_pct"]), 2),
                "diff_dot_pct": round(float(r["diff_dot_pct"]), 2),
                "observed_dismissal_pct": round(float(r["observed_dismissal_pct"]), 2),
                "diff_dismissal_pct": round(float(r["diff_dismissal_pct"]), 2),
                "pressure_legal_balls": balls,
                "pressure_matches": int(r["pressure_matches"]),
                "pressure_seasons": int(r["pressure_seasons"]),
                "season_span": str(r["season_span"]) if pd.notna(r["season_span"]) else "None",
                "season_distribution": dist_str,
                "ipl_legal_balls": ipl_b,
                "t20i_legal_balls": t20i_b,
                "competition_coverage": comp_cov,
                "competition_qualification": comp_qual,
                "ipl_conservative_metric": comp_data.get("ipl_conservative_metric"),
                "t20i_conservative_metric": comp_data.get("t20i_conservative_metric"),
                "cross_comp_transferable": (ipl_b >= 30 and t20i_b >= 30),
                "exploratory_pri_no_tcf": float(r["exploratory_pri_no_tcf"]) if pd.notna(r["exploratory_pri_no_tcf"]) else np.nan,
                "experimental_pri_with_tcf": float(r["composite_pri"]) if pd.notna(r["composite_pri"]) else np.nan,
                "temporal_consistency_score": float(r["temporal_consistency_score"]) if pd.notna(r["temporal_consistency_score"]) else np.nan,
            })

        # Append zero-pressure batters
        for _, zr in zero_pressure_batters.iterrows():
            records.append({
                "player_id": zr["player_id"],
                "player_name": zr["player_name"],
                "discipline": "BATTING",
                "is_qualified": False,
                "qualification_status": "NOT_QUALIFIED",
                "qualification_reason": "ZERO_PRESSURE_DELIVERIES_FACED (faced non-pressure balls only)",
                "is_candidate_qualified": False,
                "evidence_volume_tier": "NO_QUALIFYING_EXPOSURE",
                "legacy_evidence_volume_tier": "Insufficient (<30 balls)",
                "uncertainty_level": "VERY_HIGH",
                "primary_diagnostic_name": "BAT_CONSERVATIVE",
                "primary_diagnostic_value": np.nan,
                "primary_diagnostic_unit": "SR_POINTS",
                "posterior_mean": np.nan,
                "posterior_se": np.nan,
                "ci_95_lower": np.nan,
                "ci_95_upper": np.nan,
                "ci_95_width": np.nan,
                "shrinkage_weight": np.nan,
                "prob_exceed_baseline": np.nan,
                "prob_exceed_peers": np.nan,
                "prob_exceed_league_mean": np.nan,
                "observed_strike_rate": np.nan,
                "expected_strike_rate": np.nan,
                "diff_strike_rate": np.nan,
                "observed_boundary_pct": np.nan,
                "diff_boundary_pct": np.nan,
                "observed_dot_pct": np.nan,
                "diff_dot_pct": np.nan,
                "observed_dismissal_pct": np.nan,
                "diff_dismissal_pct": np.nan,
                "pressure_legal_balls": 0,
                "pressure_matches": 0,
                "pressure_seasons": 0,
                "season_span": "None",
                "season_distribution": "None (0 balls in pressure)",
                "ipl_legal_balls": 0,
                "t20i_legal_balls": 0,
                "competition_coverage": "NONE",
                "competition_qualification": "AGGREGATE_ONLY_QUALIFIED (<30 balls in either isolated tournament)",
                "ipl_conservative_metric": None,
                "t20i_conservative_metric": None,
                "cross_comp_transferable": False,
                "exploratory_pri_no_tcf": np.nan,
                "experimental_pri_with_tcf": np.nan,
                "temporal_consistency_score": np.nan,
            })

        self.batting_intelligence_df = pd.DataFrame(records)
        return self.batting_intelligence_df

    def build_bowling_intelligence(self) -> pd.DataFrame:
        """Constructs complete bowling reliability intelligence dataset for all bowlers."""
        df_rel = self.bowl_reliability_df.copy()

        season_dist_map = self._build_season_distribution_map(self.bowl_events_df, is_batting=False)
        comp_metrics_map = self._compute_competition_specific_metrics(self.bowl_events_df, is_batting=False)

        prim_bowlers = self.deliv_states_df[self.deliv_states_df["is_primary_scope"]].groupby(
            ["bowler_id", "bowler_name"]
        ).size().reset_index().rename(columns={"bowler_id": "player_id", "bowler_name": "player_name", 0: "total_balls_bowled"})

        existing_pids = set(df_rel["player_id"])
        zero_pressure_bowlers = prim_bowlers[~prim_bowlers["player_id"].isin(existing_pids)].copy()

        # Compute Exploratory PRI (without TCF) for qualified bowlers
        qual_mask = df_rel["is_qualified"]
        qual_df = df_rel[qual_mask].copy()
        z_cons = self._min_max_scale(qual_df["score_conservative_bound"])
        z_wkt = self._min_max_scale(qual_df["diff_wicket_pct"])
        z_dot = self._min_max_scale(qual_df["diff_dot_pct"])
        z_bnd = self._min_max_scale(-qual_df["diff_boundary_pct"])
        raw_pri_no_tcf = 0.45 * z_cons + 0.20 * z_wkt + 0.20 * z_dot + 0.15 * z_bnd
        scaled_pri_no_tcf = self._min_max_scale(raw_pri_no_tcf)
        df_rel["exploratory_pri_no_tcf"] = np.nan
        df_rel.loc[qual_mask, "exploratory_pri_no_tcf"] = scaled_pri_no_tcf

        records = []
        for _, r in df_rel.iterrows():
            pid = r["player_id"]
            balls = int(r["pressure_legal_balls"])
            is_qual = bool(r["is_qualified"])

            # Evidence volume tier (Dimension B standard)
            if balls >= 150:
                vol_tier = "HIGH_VOLUME"
                legacy_vol_tier = "Large Sample (>=150 balls)"
                unc_level = "LOW"
            elif balls >= 60:
                vol_tier = "MEDIUM_VOLUME"
                legacy_vol_tier = "Medium Sample (60-149 balls)"
                unc_level = "MEDIUM"
            elif balls >= 30:
                vol_tier = "LOW_VOLUME"
                legacy_vol_tier = "Small Sample (30-59 balls)"
                unc_level = "HIGH"
            else:
                vol_tier = "NO_QUALIFYING_EXPOSURE"
                legacy_vol_tier = "Insufficient (<30 balls)"
                unc_level = "VERY_HIGH"

            if is_qual:
                qual_status = "QUALIFIED"
                qual_reason = f"QUALIFIED_SAMPLE_GE_30_BALLS ({balls} balls)"
            else:
                qual_status = "NOT_QUALIFIED"
                qual_reason = f"BELOW_MIN_PRESSURE_BALLS: {balls} of 30 required balls"

            # Candidate sample qualification (DEF-04 fix: >=60 balls OR (>=50 balls and >=10 matches))
            cand_qual = bool((balls >= 60) or (balls >= 50 and int(r["pressure_matches"]) >= 10))

            # Competition coverage and qualification (DEF-05 remediation)
            ipl_b = int(r["ipl_legal_balls"])
            t20i_b = int(r["t20i_legal_balls"])
            if ipl_b >= 30 and t20i_b >= 30:
                comp_qual = "DUAL_TOURNAMENT_QUALIFIED"
            elif ipl_b >= 30:
                comp_qual = "IPL_QUALIFIED"
            elif t20i_b >= 30:
                comp_qual = "T20I_QUALIFIED"
            else:
                comp_qual = "AGGREGATE_ONLY_QUALIFIED (<30 balls in either isolated tournament)"

            if ipl_b >= 20 and t20i_b >= 20:
                comp_cov = "BOTH"
            elif ipl_b > 0 and t20i_b == 0:
                comp_cov = "IPL_ONLY"
            elif t20i_b > 0 and ipl_b == 0:
                comp_cov = "T20I_ONLY"
            elif ipl_b >= t20i_b:
                comp_cov = "IPL_DOMINANT"
            else:
                comp_cov = "T20I_DOMINANT"

            comp_data = comp_metrics_map.get(pid, {})
            dist_str = season_dist_map.get(pid, "None")

            post_mean = r["shrunk_diff_economy"]
            post_se = r["posterior_se_economy"]
            cons_bound = r["score_conservative_bound"]

            records.append({
                "player_id": pid,
                "player_name": r["player_name"],
                "discipline": "BOWLING",
                "is_qualified": is_qual,
                "qualification_status": qual_status,
                "qualification_reason": qual_reason,
                "is_candidate_qualified": cand_qual,
                "evidence_volume_tier": vol_tier,
                "legacy_evidence_volume_tier": legacy_vol_tier,
                "uncertainty_level": unc_level,
                "primary_diagnostic_name": "BOWL_CONSERVATIVE",
                "primary_diagnostic_value": float(cons_bound) if pd.notna(cons_bound) else np.nan,
                "primary_diagnostic_unit": "RUNS_SAVED_PER_OVER",
                "posterior_mean": float(post_mean) if pd.notna(post_mean) else np.nan,
                "posterior_se": float(post_se) if pd.notna(post_se) else np.nan,
                "ci_95_lower": float(r["ci_95_lower_economy"]) if pd.notna(r["ci_95_lower_economy"]) else np.nan,
                "ci_95_upper": float(r["ci_95_upper_economy"]) if pd.notna(r["ci_95_upper_economy"]) else np.nan,
                "ci_95_width": float(r["ci_95_upper_economy"] - r["ci_95_lower_economy"]) if pd.notna(r["ci_95_lower_economy"]) else np.nan,
                "shrinkage_weight": float(r["reliability_economy"]) if pd.notna(r["reliability_economy"]) else np.nan,
                "prob_exceed_baseline": float(r["prob_exceed_baseline"]) if pd.notna(r["prob_exceed_baseline"]) else np.nan,
                "prob_exceed_peers": float(r["prob_exceed_peer_mean"]) if pd.notna(r["prob_exceed_peer_mean"]) else np.nan,
                "prob_exceed_league_mean": float(r["prob_exceed_peer_mean"]) if pd.notna(r["prob_exceed_peer_mean"]) else np.nan,
                "observed_economy": round(float(r["observed_economy"]), 2),
                "expected_economy": round(float(r["expected_economy"]), 2),
                "diff_economy": round(float(r["diff_economy"]), 2),
                "observed_wicket_pct": round(float(r["observed_wicket_pct"]), 2),
                "diff_wicket_pct": round(float(r["diff_wicket_pct"]), 2),
                "observed_dot_pct": round(float(r["observed_dot_pct"]), 2),
                "diff_dot_pct": round(float(r["diff_dot_pct"]), 2),
                "observed_boundary_pct": round(float(r["observed_boundary_pct"]), 2),
                "diff_boundary_pct": round(float(r["diff_boundary_pct"]), 2),
                "pressure_legal_balls": balls,
                "pressure_matches": int(r["pressure_matches"]),
                "pressure_seasons": int(r["pressure_seasons"]),
                "season_span": str(r["season_span"]) if pd.notna(r["season_span"]) else "None",
                "season_distribution": dist_str,
                "ipl_legal_balls": ipl_b,
                "t20i_legal_balls": t20i_b,
                "competition_coverage": comp_cov,
                "competition_qualification": comp_qual,
                "ipl_conservative_metric": comp_data.get("ipl_conservative_metric"),
                "t20i_conservative_metric": comp_data.get("t20i_conservative_metric"),
                "cross_comp_transferable": (ipl_b >= 30 and t20i_b >= 30),
                "exploratory_pri_no_tcf": float(r["exploratory_pri_no_tcf"]) if pd.notna(r["exploratory_pri_no_tcf"]) else np.nan,
                "experimental_pri_with_tcf": float(r["composite_pri"]) if pd.notna(r["composite_pri"]) else np.nan,
                "temporal_consistency_score": float(r["temporal_consistency_score"]) if pd.notna(r["temporal_consistency_score"]) else np.nan,
            })

        # Append zero-pressure bowlers
        for _, zr in zero_pressure_bowlers.iterrows():
            records.append({
                "player_id": zr["player_id"],
                "player_name": zr["player_name"],
                "discipline": "BOWLING",
                "is_qualified": False,
                "qualification_status": "NOT_QUALIFIED",
                "qualification_reason": "ZERO_PRESSURE_DELIVERIES_BOWLED (bowled non-pressure balls only)",
                "is_candidate_qualified": False,
                "evidence_volume_tier": "NO_QUALIFYING_EXPOSURE",
                "legacy_evidence_volume_tier": "Insufficient (<30 balls)",
                "uncertainty_level": "VERY_HIGH",
                "primary_diagnostic_name": "BOWL_CONSERVATIVE",
                "primary_diagnostic_value": np.nan,
                "primary_diagnostic_unit": "RUNS_SAVED_PER_OVER",
                "posterior_mean": np.nan,
                "posterior_se": np.nan,
                "ci_95_lower": np.nan,
                "ci_95_upper": np.nan,
                "ci_95_width": np.nan,
                "shrinkage_weight": np.nan,
                "prob_exceed_baseline": np.nan,
                "prob_exceed_peers": np.nan,
                "prob_exceed_league_mean": np.nan,
                "observed_economy": np.nan,
                "expected_economy": np.nan,
                "diff_economy": np.nan,
                "observed_wicket_pct": np.nan,
                "diff_wicket_pct": np.nan,
                "observed_dot_pct": np.nan,
                "diff_dot_pct": np.nan,
                "observed_boundary_pct": np.nan,
                "diff_boundary_pct": np.nan,
                "pressure_legal_balls": 0,
                "pressure_matches": 0,
                "pressure_seasons": 0,
                "season_span": "None",
                "season_distribution": "None (0 balls in pressure)",
                "ipl_legal_balls": 0,
                "t20i_legal_balls": 0,
                "competition_coverage": "NONE",
                "competition_qualification": "AGGREGATE_ONLY_QUALIFIED (<30 balls in either isolated tournament)",
                "ipl_conservative_metric": None,
                "t20i_conservative_metric": None,
                "cross_comp_transferable": False,
                "exploratory_pri_no_tcf": np.nan,
                "experimental_pri_with_tcf": np.nan,
                "temporal_consistency_score": np.nan,
            })

        self.bowling_intelligence_df = pd.DataFrame(records)
        return self.bowling_intelligence_df

    def build_candidate_pools(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Separates intelligence records into Qualified and Non-Qualified candidate datasets."""
        if self.batting_intelligence_df is None:
            self.build_batting_intelligence()
        if self.bowling_intelligence_df is None:
            self.build_bowling_intelligence()

        all_df = pd.concat([self.batting_intelligence_df, self.bowling_intelligence_df], ignore_index=True)

        self.qualified_candidates_df = all_df[all_df["is_qualified"]].copy().reset_index(drop=True)
        self.non_qualified_candidates_df = all_df[~all_df["is_qualified"]].copy().reset_index(drop=True)

        return self.qualified_candidates_df, self.non_qualified_candidates_df

    def save_intelligence_datasets(self) -> Dict[str, Path]:
        """Saves generated intelligence datasets into processed data directory."""
        if self.qualified_candidates_df is None or self.non_qualified_candidates_df is None:
            self.build_candidate_pools()

        output_paths = {}
        file_mappings = [
            ("batting_intelligence.parquet", self.batting_intelligence_df),
            ("bowling_intelligence.parquet", self.bowling_intelligence_df),
            ("qualified_candidates.parquet", self.qualified_candidates_df),
            ("non_qualified_candidates.parquet", self.non_qualified_candidates_df),
        ]

        for fname, df in file_mappings:
            fpath = self.processed_dir / fname
            df.to_parquet(fpath, index=False)
            output_paths[fname] = fpath

        return output_paths

    def run_all(self) -> None:
        """Executes full intelligence generation pipeline."""
        self.load_data()
        self.build_batting_intelligence()
        self.build_bowling_intelligence()
        self.build_candidate_pools()
        self.save_intelligence_datasets()


if __name__ == "__main__":
    engine = PlayerIntelligenceEngine()
    engine.run_all()
    print("Player Intelligence datasets successfully generated.")
