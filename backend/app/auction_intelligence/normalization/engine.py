"""
AUCTION-04: Historical Performance & Competition Normalization Engine.

Computes empirical competition benchmarks across IPL, T20I, and Tier-2 Emerging T20,
and derives independent, normalized batting and bowling profiles with empirical Bayesian shrinkage
and phase-specific splits for all canonical players.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
import numpy as np
import pandas as pd

from app.schemas.auction.normalization import (
    CompetitionBenchmark,
    PhaseBattingSplit,
    PhaseBowlingSplit,
    NormalizedBattingProfile,
    NormalizedBowlingProfile,
    NormalizationSummary,
)


class CompetitionNormalizationEngine:
    """Core processing engine for AUCTION-04 historical performance normalization."""

    def __init__(self, raw_data_dir: Optional[Path] = None, processed_dir: Optional[Path] = None):
        self.repo_root = Path(__file__).resolve().parent.parent.parent.parent.parent
        self.raw_data_dir = raw_data_dir or (self.repo_root / "data" / "raw" / "rajasthan_royals" / "round_1_data_pack")
        self.processed_dir = processed_dir or (self.repo_root / "data" / "processed" / "auction_intelligence")
        self.processed_dir.mkdir(parents=True, exist_ok=True)

        self.benchmarks: Dict[str, CompetitionBenchmark] = {}
        self.batting_profiles: Dict[int, NormalizedBattingProfile] = {}
        self.bowling_profiles: Dict[int, NormalizedBowlingProfile] = {}
        self.summary: Optional[NormalizationSummary] = None

    def execute_full_normalization(self) -> Tuple[Dict[str, CompetitionBenchmark], Dict[int, NormalizedBattingProfile], Dict[int, NormalizedBowlingProfile], NormalizationSummary]:
        """Runs the complete deterministic normalization pipeline and persists all artifacts."""
        # 1. Load raw datasets
        bbb_df = pd.read_csv(self.raw_data_dir / "ball_by_ball.csv")
        matches_df = pd.read_csv(self.raw_data_dir / "matches.csv")
        comps_df = pd.read_csv(self.raw_data_dir / "competitions.csv")
        can_df = pd.read_parquet(self.processed_dir / "canonical_player_registry.parquet")

        # 2. Enrich ball-by-ball with competition context
        m_c = matches_df[["match_id", "comp_id"]].merge(
            comps_df[["comp_id", "comp_name", "match_format", "season"]],
            on="comp_id",
            how="left"
        )
        df = bbb_df.merge(m_c, on="match_id", how="left")

        # Identify legal vs non-legal deliveries (8,290 non-legal = 7,714 wides + 576 Overstep)
        df["is_non_legal"] = df["extras_type"].isin(["wide", "Overstep"])
        df["is_legal"] = ~df["is_non_legal"]

        # Classify competition tiers
        def assign_tier(cname: str) -> str:
            s = str(cname)
            if "IPL" in s:
                return "IPL"
            elif "Emerging" in s or "Rising Stars" in s:
                return "Emerging_T20"
            else:
                return "T20I"

        df["comp_tier"] = df["comp_name"].apply(assign_tier)

        # 3. Compute empirical competition tier benchmarks
        self._compute_competition_benchmarks(df)

        # 4. Compute normalized batting profiles
        self._compute_batting_profiles(df, can_df)

        # 5. Compute normalized bowling profiles
        self._compute_bowling_profiles(df, can_df)

        # 6. Create macro summary
        total_legal = int(df["is_legal"].sum())
        self.summary = NormalizationSummary(
            total_canonical_players=len(can_df),
            total_ball_by_ball_deliveries=len(df),
            total_legal_deliveries=total_legal,
            total_matches_audited=len(matches_df),
            total_batters_evaluated=len(self.batting_profiles),
            qualified_batters_count=sum(1 for p in self.batting_profiles.values() if p.is_sample_qualified),
            total_bowlers_evaluated=len(self.bowling_profiles),
            qualified_bowlers_count=sum(1 for p in self.bowling_profiles.values() if p.is_sample_qualified),
            benchmarks=self.benchmarks,
        )

        # 7. Run empirical sensitivity analysis
        self.run_sensitivity_analysis()

        # 8. Persist all derived datasets
        self._save_artifacts()

        return self.benchmarks, self.batting_profiles, self.bowling_profiles, self.summary

    def _compute_competition_benchmarks(self, df: pd.DataFrame) -> None:
        """Derives empirical league-level benchmarks across IPL, T20I, and Emerging_T20."""
        # Calculate base aggregate metrics per tier
        tier_groups = df.groupby("comp_tier")
        temp_benchmarks: Dict[str, Dict[str, Any]] = {}

        for tier_name, grp in tier_groups:
            tot_del = len(grp)
            legal_del = int(grp["is_legal"].sum())
            bat_runs = int(grp["runs"].sum())
            
            # Accurate cricket bowler conceded runs:
            # - Wides: 1 penalty run charged to bowler
            # - Overstep/other: 1 penalty run + runs off bat + extras_2_runs auxiliary
            # - Byes/legbyes/Penalty: 0 runs charged to bowler (fielding extras)
            # - Standard deliveries: runs off bat
            is_wide = grp["extras_type"] == "wide"
            is_nb = grp["extras_type"].isin(["Overstep", "other"])
            is_fielding = grp["extras_type"].isin(["byes", "legbyes", "Penalty"])
            e2 = grp["extras_2_runs"].fillna(0)

            bowler_conceded_arr = np.where(
                is_wide,
                1,
                np.where(
                    is_nb,
                    grp["runs"].fillna(0) + 1 + e2,
                    np.where(
                        is_fielding,
                        0,
                        grp["runs"].fillna(0)
                    )
                )
            )
            bowler_runs = int(bowler_conceded_arr.sum())

            # Confirmed match total runs = batter runs + bowler extras + fielding extras
            fielding_extras = int(is_fielding.sum())
            wides_count = int(is_wide.sum())
            nb_extras = int((is_nb.astype(int) + e2 * is_nb.astype(int)).sum())
            tot_runs = bat_runs + wides_count + nb_extras + fielding_extras

            # Bowler credited wickets (exclude run out, retired out, retired hurt, obstructing the field)
            uncredited = ["run out", "runout", "retired out", "retired hurt", "obstructing the field"]
            bowler_wkts = int((grp["is_wicket"] & (~grp["dismissal_type"].str.lower().isin(uncredited))).sum())
            total_wkts = int(grp["is_wicket"].sum())

            fours = int(grp["is_four"].sum())
            sixes = int(grp["is_six"].sum())
            dots = int(((grp["runs"] == 0) & grp["is_legal"]).sum())

            run_rate = (tot_runs / legal_del) * 6.0 if legal_del > 0 else 0.0
            bowler_econ = (bowler_runs / legal_del) * 6.0 if legal_del > 0 else 0.0
            strike_rate = (bat_runs / legal_del) * 100.0 if legal_del > 0 else 0.0
            boundary_pct = ((fours + sixes) / legal_del) * 100.0 if legal_del > 0 else 0.0
            dot_pct = (dots / legal_del) * 100.0 if legal_del > 0 else 0.0
            wickets_per_ball = total_wkts / legal_del if legal_del > 0 else 0.0
            runs_per_wicket = tot_runs / total_wkts if total_wkts > 0 else 0.0

            temp_benchmarks[tier_name] = {
                "total_deliveries": tot_del,
                "legal_deliveries": legal_del,
                "total_runs": tot_runs,
                "batter_runs": bat_runs,
                "total_bowler_conceded_runs": bowler_runs,
                "total_wickets": total_wkts,
                "bowler_credited_wickets": bowler_wkts,
                "benchmark_run_rate": round(run_rate, 4),
                "benchmark_bowling_economy": round(bowler_econ, 4),
                "benchmark_strike_rate": round(strike_rate, 4),
                "benchmark_boundary_pct": round(boundary_pct, 4),
                "benchmark_dot_pct": round(dot_pct, 4),
                "benchmark_wickets_per_ball": round(wickets_per_ball, 6),
                "benchmark_runs_per_wicket": round(runs_per_wicket, 4),
            }

        # Use IPL as anchor benchmark (1.000)
        ipl_sr = temp_benchmarks["IPL"]["benchmark_strike_rate"]
        ipl_bnd = temp_benchmarks["IPL"]["benchmark_boundary_pct"]

        self.benchmarks.clear()
        for tier_name, data in temp_benchmarks.items():
            rel_scoring = round(data["benchmark_strike_rate"] / ipl_sr, 4)
            rel_boundary = round(data["benchmark_boundary_pct"] / ipl_bnd, 4)

            self.benchmarks[tier_name] = CompetitionBenchmark(
                competition_tier=tier_name,
                total_deliveries=data["total_deliveries"],
                legal_deliveries=data["legal_deliveries"],
                total_runs=data["total_runs"],
                batter_runs=data["batter_runs"],
                total_bowler_conceded_runs=data["total_bowler_conceded_runs"],
                total_wickets=data["total_wickets"],
                bowler_credited_wickets=data["bowler_credited_wickets"],
                benchmark_run_rate=data["benchmark_run_rate"],
                benchmark_bowling_economy=data["benchmark_bowling_economy"],
                benchmark_strike_rate=data["benchmark_strike_rate"],
                benchmark_boundary_pct=data["benchmark_boundary_pct"],
                benchmark_dot_pct=data["benchmark_dot_pct"],
                benchmark_wickets_per_ball=data["benchmark_wickets_per_ball"],
                benchmark_runs_per_wicket=data["benchmark_runs_per_wicket"],
                relative_scoring_index=rel_scoring,
                relative_boundary_index=rel_boundary,
            )

    def _compute_batting_profiles(self, df: pd.DataFrame, can_df: pd.DataFrame) -> None:
        """Derives normalized batting performance for all strikers in the dataset."""
        can_lookup = {
            int(r["canonical_id"]): (str(r["canonical_key"]), str(r["canonical_name"]))
            for _, r in can_df.iterrows()
        }

        # Filter strictly for striker deliveries
        strikers_df = df.dropna(subset=["striker_id"]).copy()
        strikers_df["striker_id"] = strikers_df["striker_id"].astype(int)

        # Baseline IPL Strike Rate for shrinkage prior
        ipl_prior_sr = self.benchmarks["IPL"].benchmark_strike_rate
        m_shrinkage = 60.0  # Empirical prior weight: 60 balls (approx 10 overs)

        self.batting_profiles.clear()

        # Group by striker
        for pid, pgrp in strikers_df.groupby("striker_id"):
            if pid not in can_lookup:
                continue

            can_key, can_name = can_lookup[pid]
            total_matches = pgrp["match_id"].nunique()
            innings_batted = pgrp.groupby(["match_id", "innings"]).ngroups
            
            legal_mask = pgrp["is_legal"]
            legal_pgrp = pgrp[legal_mask]
            legal_balls = len(legal_pgrp)
            
            raw_runs = int(pgrp["runs"].sum())
            fours = int(pgrp["is_four"].sum())
            sixes = int(pgrp["is_six"].sum())
            dots = int(((pgrp["runs"] == 0) & legal_mask).sum())

            # Count actual dismissals of this batter
            dismissals = int((pgrp["is_wicket"] & (pgrp["dismissed_player_id"] == pid)).sum())

            raw_sr = (raw_runs / legal_balls) * 100.0 if legal_balls > 0 else 0.0
            bat_avg = (raw_runs / dismissals) if dismissals > 0 else None
            boundary_pct = ((fours + sixes) / legal_balls) * 100.0 if legal_balls > 0 else 0.0
            dot_pct = (dots / legal_balls) * 100.0 if legal_balls > 0 else 0.0

            # Competition-Weighted Strike Rate:
            # Adjust runs in each tier by the inverse of the relative scoring index
            weighted_runs = 0.0
            for tier_name, tier_sub in legal_pgrp.groupby("comp_tier"):
                tier_rel_idx = self.benchmarks[tier_name].relative_scoring_index
                tier_adjustment = 1.0 / tier_rel_idx if tier_rel_idx > 0 else 1.0
                weighted_runs += tier_sub["runs"].sum() * tier_adjustment

            comp_weighted_sr = (weighted_runs / legal_balls) * 100.0 if legal_balls > 0 else 0.0

            # Empirical Bayesian Shrinkage towards IPL prior mean
            shrunk_sr = (
                (legal_balls / (legal_balls + m_shrinkage)) * comp_weighted_sr
                + (m_shrinkage / (legal_balls + m_shrinkage)) * ipl_prior_sr
            ) if legal_balls > 0 else ipl_prior_sr

            # Normalized efficiency vs IPL benchmark (100 = average IPL batter)
            norm_efficiency = (shrunk_sr / ipl_prior_sr) * 100.0

            # Sample Confidence Tier
            if legal_balls >= 200:
                conf_tier = "HIGH"
            elif legal_balls >= 60:
                conf_tier = "MEDIUM"
            else:
                conf_tier = "LOW"

            is_qualified = legal_balls >= 30

            # Phase-Specific Splits
            phase_splits = {}
            for phase_name, (ov_start, ov_end) in [
                ("Powerplay", (0, 5)),
                ("Middle", (6, 14)),
                ("Death", (15, 19)),
            ]:
                phase_mask = legal_mask & (pgrp["overid"] >= ov_start) & (pgrp["overid"] <= ov_end)
                phase_pgrp = pgrp[phase_mask]
                ph_balls = len(phase_pgrp)
                ph_runs = int(phase_pgrp["runs"].sum())
                ph_outs = int((pgrp["is_wicket"] & (pgrp["dismissed_player_id"] == pid) & (pgrp["overid"] >= ov_start) & (pgrp["overid"] <= ov_end)).sum())
                ph_sr = (ph_runs / ph_balls) * 100.0 if ph_balls > 0 else 0.0
                ph_dots = int((phase_pgrp["runs"] == 0).sum())
                ph_bnds = int((phase_pgrp["is_four"] | phase_pgrp["is_six"]).sum())
                ph_conf = "HIGH" if ph_balls >= 60 else ("MEDIUM" if ph_balls >= 20 else "LOW")
                ph_qual = ph_balls >= 20

                phase_splits[phase_name] = PhaseBattingSplit(
                    phase_name=phase_name,
                    balls_faced=ph_balls,
                    runs_scored=ph_runs,
                    dismissals=ph_outs,
                    strike_rate=round(ph_sr, 2),
                    dot_pct=round((ph_dots / ph_balls) * 100.0, 2) if ph_balls > 0 else 0.0,
                    boundary_pct=round((ph_bnds / ph_balls) * 100.0, 2) if ph_balls > 0 else 0.0,
                    phase_confidence_tier=ph_conf,
                    is_phase_qualified=ph_qual,
                )

            self.batting_profiles[pid] = NormalizedBattingProfile(
                canonical_id=pid,
                canonical_key=can_key,
                canonical_name=can_name,
                total_matches=total_matches,
                innings_batted=innings_batted,
                legal_balls_faced=legal_balls,
                raw_runs_scored=raw_runs,
                dismissals=dismissals,
                fours_count=fours,
                sixes_count=sixes,
                dots_faced=dots,
                raw_strike_rate=round(raw_sr, 2),
                raw_batting_average=round(bat_avg, 2) if bat_avg is not None else None,
                boundary_pct=round(boundary_pct, 2),
                dot_pct=round(dot_pct, 2),
                competition_weighted_sr_index=round(comp_weighted_sr, 2),
                shrunk_strike_rate=round(shrunk_sr, 2),
                normalized_scoring_efficiency=round(norm_efficiency, 2),
                sample_confidence_tier=conf_tier,
                is_sample_qualified=is_qualified,
                phase_splits=phase_splits,
            )

    def _compute_bowling_profiles(self, df: pd.DataFrame, can_df: pd.DataFrame) -> None:
        """Derives normalized bowling performance for all bowlers in the dataset."""
        can_lookup = {
            int(r["canonical_id"]): (str(r["canonical_key"]), str(r["canonical_name"]))
            for _, r in can_df.iterrows()
        }

        # Filter strictly for bowler deliveries
        bowlers_df = df.dropna(subset=["bowler_id"]).copy()
        bowlers_df["bowler_id"] = bowlers_df["bowler_id"].astype(int)

        # Baseline IPL Bowling Economy for shrinkage prior
        ipl_prior_econ = self.benchmarks["IPL"].benchmark_bowling_economy  # 9.1258 RPO
        m_shrinkage_balls = 60.0  # Provisional empirical shrinkage parameter (equivalent to 10 overs)

        self.bowling_profiles.clear()

        # Bowler runs conceded = runs off bat + wides/noball extras (exclude byes and legbyes)
        is_wide = bowlers_df["extras_type"] == "wide"
        is_nb = bowlers_df["extras_type"].isin(["Overstep", "other"])
        is_fielding = bowlers_df["extras_type"].isin(["byes", "legbyes", "Penalty"])
        e2 = bowlers_df["extras_2_runs"].fillna(0)

        bowlers_df["bowler_conceded_runs"] = np.where(
            is_wide,
            1,
            np.where(
                is_nb,
                bowlers_df["runs"].fillna(0) + 1 + e2,
                np.where(
                    is_fielding,
                    0,
                    bowlers_df["runs"].fillna(0)
                )
            )
        )

        # Bowler credited wickets (exclude run out, retired out, retired hurt, obstructing the field)
        uncredited_dismissals = ["run out", "runout", "retired out", "retired hurt", "obstructing the field"]
        bowlers_df["is_bowler_wicket"] = bowlers_df["is_wicket"] & (~bowlers_df["dismissal_type"].str.lower().isin(uncredited_dismissals))

        # Group by bowler
        for pid, pgrp in bowlers_df.groupby("bowler_id"):
            if pid not in can_lookup:
                continue

            can_key, can_name = can_lookup[pid]
            total_matches = pgrp["match_id"].nunique()
            innings_bowled = pgrp.groupby(["match_id", "innings"]).ngroups
            
            legal_mask = pgrp["is_legal"]
            legal_pgrp = pgrp[legal_mask]
            legal_balls = len(legal_pgrp)
            overs_bowled = round(legal_balls / 6.0, 1)

            runs_conceded = int(pgrp["bowler_conceded_runs"].sum())
            wickets = int(pgrp["is_bowler_wicket"].sum())
            dots = int(((pgrp["bowler_conceded_runs"] == 0) & legal_mask).sum())
            boundaries = int(((pgrp["is_four"] | pgrp["is_six"]) & legal_mask).sum())

            raw_econ = (runs_conceded / legal_balls) * 6.0 if legal_balls > 0 else 0.0
            bowling_sr = (legal_balls / wickets) if wickets > 0 else None
            bowling_avg = (runs_conceded / wickets) if wickets > 0 else None
            dot_pct = (dots / legal_balls) * 100.0 if legal_balls > 0 else 0.0
            bnd_pct = (boundaries / legal_balls) * 100.0 if legal_balls > 0 else 0.0

            # Competition-Weighted Economy Rate:
            # Adjust bowler runs conceded in each tier by the inverse of relative scoring index
            weighted_conceded = 0.0
            for tier_name, tier_sub in pgrp.groupby("comp_tier"):
                tier_rel_idx = self.benchmarks[tier_name].relative_scoring_index
                tier_adjustment = 1.0 / tier_rel_idx if tier_rel_idx > 0 else 1.0
                weighted_conceded += tier_sub["bowler_conceded_runs"].sum() * tier_adjustment

            comp_weighted_econ = (weighted_conceded / legal_balls) * 6.0 if legal_balls > 0 else 0.0

            # Empirical Bayesian Shrinkage towards IPL prior mean economy
            shrunk_econ = (
                (legal_balls / (legal_balls + m_shrinkage_balls)) * comp_weighted_econ
                + (m_shrinkage_balls / (legal_balls + m_shrinkage_balls)) * ipl_prior_econ
            ) if legal_balls > 0 else ipl_prior_econ

            # Normalized economy efficiency (higher is better: IPL benchmark / player economy * 100)
            norm_econ_efficiency = (ipl_prior_econ / shrunk_econ) * 100.0 if shrunk_econ > 0 else 100.0

            # Sample Confidence Tier
            if legal_balls >= 200:
                conf_tier = "HIGH"
            elif legal_balls >= 60:
                conf_tier = "MEDIUM"
            else:
                conf_tier = "LOW"

            is_qualified = legal_balls >= 30

            # Phase-Specific Splits
            phase_splits = {}
            for phase_name, (ov_start, ov_end) in [
                ("Powerplay", (0, 5)),
                ("Middle", (6, 14)),
                ("Death", (15, 19)),
            ]:
                phase_mask = legal_mask & (pgrp["overid"] >= ov_start) & (pgrp["overid"] <= ov_end)
                phase_pgrp = pgrp[phase_mask]
                ph_balls = len(phase_pgrp)
                ph_runs = int(pgrp[pgrp["overid"].between(ov_start, ov_end)]["bowler_conceded_runs"].sum())
                ph_wkts = int(pgrp[pgrp["overid"].between(ov_start, ov_end)]["is_bowler_wicket"].sum())
                ph_econ = (ph_runs / ph_balls) * 6.0 if ph_balls > 0 else 0.0
                ph_dots = int(((phase_pgrp["bowler_conceded_runs"] == 0)).sum())
                ph_bnds = int((phase_pgrp["is_four"] | phase_pgrp["is_six"]).sum())
                ph_conf = "HIGH" if ph_balls >= 60 else ("MEDIUM" if ph_balls >= 20 else "LOW")
                ph_qual = ph_balls >= 20

                phase_splits[phase_name] = PhaseBowlingSplit(
                    phase_name=phase_name,
                    balls_bowled=ph_balls,
                    runs_conceded=ph_runs,
                    wickets_taken=ph_wkts,
                    economy_rate=round(ph_econ, 2),
                    dot_pct=round((ph_dots / ph_balls) * 100.0, 2) if ph_balls > 0 else 0.0,
                    boundary_pct=round((ph_bnds / ph_balls) * 100.0, 2) if ph_balls > 0 else 0.0,
                    phase_confidence_tier=ph_conf,
                    is_phase_qualified=ph_qual,
                )

            self.bowling_profiles[pid] = NormalizedBowlingProfile(
                canonical_id=pid,
                canonical_key=can_key,
                canonical_name=can_name,
                total_matches=total_matches,
                innings_bowled=innings_bowled,
                legal_balls_bowled=legal_balls,
                overs_bowled=overs_bowled,
                raw_runs_conceded=runs_conceded,
                wickets_taken=wickets,
                dots_bowled=dots,
                boundaries_conceded=boundaries,
                raw_economy_rate=round(raw_econ, 2),
                raw_bowling_strike_rate=round(bowling_sr, 2) if bowling_sr is not None else None,
                raw_bowling_average=round(bowling_avg, 2) if bowling_avg is not None else None,
                dot_pct=round(dot_pct, 2),
                boundary_conceded_pct=round(bnd_pct, 2),
                competition_weighted_economy_index=round(comp_weighted_econ, 2),
                shrunk_economy_rate=round(shrunk_econ, 2),
                normalized_economy_efficiency=round(norm_econ_efficiency, 2),
                sample_confidence_tier=conf_tier,
                is_sample_qualified=is_qualified,
                phase_splits=phase_splits,
            )

    def _save_artifacts(self) -> None:
        """Serializes all normalized profiles and benchmarks deterministically to disk."""
        # 1. Benchmarks JSON
        benchmarks_path = self.processed_dir / "competition_normalization_benchmarks.json"
        benchmarks_data = {k: v.model_dump() for k, v in self.benchmarks.items()}
        with open(benchmarks_path, "w", encoding="utf-8") as f:
            json.dump(benchmarks_data, f, indent=2)

        # 2. Batting profiles Parquet & JSON
        batting_records = [p.model_dump() for p in self.batting_profiles.values()]
        batting_df = pd.DataFrame(batting_records)
        batting_parquet_path = self.processed_dir / "normalized_batting_performance.parquet"
        batting_json_path = self.processed_dir / "normalized_batting_performance.json"
        
        # Flatten phase splits for clean parquet serialization
        batting_df_flat = batting_df.copy()
        batting_df_flat["phase_splits_json"] = batting_df_flat["phase_splits"].apply(json.dumps)
        batting_df_flat = batting_df_flat.drop(columns=["phase_splits"])
        batting_df_flat.to_parquet(batting_parquet_path, index=False)

        with open(batting_json_path, "w", encoding="utf-8") as f:
            json.dump(batting_records, f, indent=2)

        # 3. Bowling profiles Parquet & JSON
        bowling_records = [p.model_dump() for p in self.bowling_profiles.values()]
        bowling_df = pd.DataFrame(bowling_records)
        bowling_parquet_path = self.processed_dir / "normalized_bowling_performance.parquet"
        bowling_json_path = self.processed_dir / "normalized_bowling_performance.json"

        bowling_df_flat = bowling_df.copy()
        bowling_df_flat["phase_splits_json"] = bowling_df_flat["phase_splits"].apply(json.dumps)
        bowling_df_flat = bowling_df_flat.drop(columns=["phase_splits"])
        bowling_df_flat.to_parquet(bowling_parquet_path, index=False)

        with open(bowling_json_path, "w", encoding="utf-8") as f:
            json.dump(bowling_records, f, indent=2)

        # 4. Summary JSON
        if self.summary:
            summary_path = self.processed_dir / "normalization_summary.json"
            with open(summary_path, "w", encoding="utf-8") as f:
                json.dump(self.summary.model_dump(), f, indent=2)

    def run_sensitivity_analysis(self) -> Dict[str, Any]:
        """Runs empirical sensitivity analyses across shrinkage parameters, competition indices, and phase exposure."""
        ipl_sr = self.benchmarks["IPL"].benchmark_strike_rate
        ipl_econ = self.benchmarks["IPL"].benchmark_bowling_economy

        m_values = [30, 60, 100, 200]
        batting_sensitivity = {m: {"mean_shrunk_sr": 0.0, "brackets": {}} for m in m_values}
        bowling_sensitivity = {m: {"mean_shrunk_econ": 0.0, "brackets": {}} for m in m_values}

        brackets = [
            ("micro", 1, 29),
            ("low", 30, 59),
            ("medium", 60, 199),
            ("high", 200, 100000),
        ]

        # Batting sensitivity across m
        for m in m_values:
            bracket_res = {}
            for b_name, b_min, b_max in brackets:
                p_subset = [p for p in self.batting_profiles.values() if b_min <= p.legal_balls_faced <= b_max]
                if p_subset:
                    shrunk_sub = [
                        ((p.legal_balls_faced / (p.legal_balls_faced + m)) * p.competition_weighted_sr_index +
                         (m / (p.legal_balls_faced + m)) * ipl_sr)
                        for p in p_subset
                    ]
                    mean_val = float(np.mean(shrunk_sub))
                    bracket_res[b_name] = {
                        "count": len(p_subset),
                        "mean_shrunk_sr": round(mean_val, 2),
                        "mean_shrinkage_delta": round(float(np.mean([abs(s - p.competition_weighted_sr_index) for s, p in zip(shrunk_sub, p_subset)])), 2),
                    }
                else:
                    bracket_res[b_name] = {"count": 0, "mean_shrunk_sr": None, "mean_shrinkage_delta": None}
            all_shrunk = [
                ((p.legal_balls_faced / (p.legal_balls_faced + m)) * p.competition_weighted_sr_index +
                 (m / (p.legal_balls_faced + m)) * ipl_sr)
                for p in self.batting_profiles.values()
            ]
            batting_sensitivity[m]["mean_shrunk_sr"] = round(float(np.mean(all_shrunk)), 2)
            batting_sensitivity[m]["brackets"] = bracket_res

        # Bowling sensitivity across m
        for m in m_values:
            bracket_res = {}
            for b_name, b_min, b_max in brackets:
                p_subset = [p for p in self.bowling_profiles.values() if b_min <= p.legal_balls_bowled <= b_max]
                if p_subset:
                    shrunk_sub = [
                        ((p.legal_balls_bowled / (p.legal_balls_bowled + m)) * p.competition_weighted_economy_index +
                         (m / (p.legal_balls_bowled + m)) * ipl_econ)
                        for p in p_subset
                    ]
                    mean_val = float(np.mean(shrunk_sub))
                    bracket_res[b_name] = {
                        "count": len(p_subset),
                        "mean_shrunk_econ": round(mean_val, 2),
                        "mean_shrinkage_delta": round(float(np.mean([abs(s - p.competition_weighted_economy_index) for s, p in zip(shrunk_sub, p_subset)])), 2),
                    }
                else:
                    bracket_res[b_name] = {"count": 0, "mean_shrunk_econ": None, "mean_shrinkage_delta": None}
            all_shrunk = [
                ((p.legal_balls_bowled / (p.legal_balls_bowled + m)) * p.competition_weighted_economy_index +
                 (m / (p.legal_balls_bowled + m)) * ipl_econ)
                for p in self.bowling_profiles.values()
            ]
            bowling_sensitivity[m]["mean_shrunk_econ"] = round(float(np.mean(all_shrunk)), 2)
            bowling_sensitivity[m]["brackets"] = bracket_res

        # Phase exposure independence audit
        high_batters = [p for p in self.batting_profiles.values() if p.sample_confidence_tier == "HIGH"]
        high_batters_with_low_phase = 0
        phase_discrepancy_details = []
        for p in high_batters:
            low_phases = [ph_name for ph_name, ph_split in p.phase_splits.items() if ph_split.phase_confidence_tier == "LOW"]
            if low_phases:
                high_batters_with_low_phase += 1
                if len(phase_discrepancy_details) < 10:
                    phase_discrepancy_details.append({
                        "canonical_id": p.canonical_id,
                        "canonical_name": p.canonical_name,
                        "overall_balls": p.legal_balls_faced,
                        "low_phases": low_phases,
                    })

        high_bowlers = [p for p in self.bowling_profiles.values() if p.sample_confidence_tier == "HIGH"]
        high_bowlers_with_low_phase = 0
        for p in high_bowlers:
            low_phases = [ph_name for ph_name, ph_split in p.phase_splits.items() if ph_split.phase_confidence_tier == "LOW"]
            if low_phases:
                high_bowlers_with_low_phase += 1

        sensitivity_report = {
            "shrinkage_parameters_evaluated": m_values,
            "batting_sensitivity": batting_sensitivity,
            "bowling_sensitivity": bowling_sensitivity,
            "phase_exposure_independence": {
                "total_high_tier_batters": len(high_batters),
                "high_batters_with_at_least_one_low_phase": high_batters_with_low_phase,
                "high_batters_low_phase_pct": round((high_batters_with_low_phase / len(high_batters)) * 100.0, 2) if high_batters else 0.0,
                "total_high_tier_bowlers": len(high_bowlers),
                "high_bowlers_with_at_least_one_low_phase": high_bowlers_with_low_phase,
                "high_bowlers_low_phase_pct": round((high_bowlers_with_low_phase / len(high_bowlers)) * 100.0, 2) if high_bowlers else 0.0,
                "sample_phase_discrepancies": phase_discrepancy_details,
            },
        }

        # Save sensitivity summary
        sens_path = self.processed_dir / "sensitivity_analysis_summary.json"
        with open(sens_path, "w", encoding="utf-8") as f:
            json.dump(sensitivity_report, f, indent=2)

        return sensitivity_report
