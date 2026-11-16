"""
Royals Intelligence - Official Dataset Cricket Intelligence Engine
Stage 5 Core Tactical Analytics Service

Directly leverages the 200,999 delivery records and granular tactical fields
(stroke, delivery_style, over_or_around, on_or_off, bowl_speed) from the
official Rajasthan Royals Round 1 Data Pack.
"""

from pathlib import Path
from typing import Optional, List, Dict, Any
import numpy as np
import pandas as pd
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Pydantic Schemas for Tactical Analytics
# ---------------------------------------------------------------------------

class TacticalPhaseSplit(BaseModel):
    """Performance metrics segregated by match phase."""
    phase: str
    total_balls: int = 0
    legal_balls: int = 0
    runs: int = 0
    wickets: int = 0
    strike_rate: Optional[float] = None
    economy_rate: Optional[float] = None
    average: Optional[float] = None
    dot_ball_percentage: float = 0.0
    boundary_percentage: float = 0.0
    balls_per_wicket: Optional[float] = None


class TacticalStrokeProfile(BaseModel):
    """Efficiency and risk metrics for a specific shot stroke."""
    stroke: str
    deliveries_faced: int = 0
    runs_scored: int = 0
    dismissals: int = 0
    runs_per_shot: float = 0.0
    dismissal_rate_pct: float = 0.0
    boundary_pct: float = 0.0


class DeliveryStyleProfile(BaseModel):
    """Effectiveness and wicket-taking threat for a bowling delivery style."""
    delivery_style: str
    deliveries_bowled: int = 0
    runs_conceded: int = 0
    wickets: int = 0
    dot_balls: int = 0
    economy_rate: float = 0.0
    bowling_average: Optional[float] = None
    dot_ball_pct: float = 0.0


class HandednessSplit(BaseModel):
    """4-way cross-split of batter stance and bowling style."""
    batting_type: str
    pace_or_spin: str
    balls_faced: int = 0
    runs_scored: int = 0
    wickets: int = 0
    strike_rate: float = 0.0
    economy_rate: float = 0.0
    bowling_average: Optional[float] = None
    boundary_pct: float = 0.0
    dot_pct: float = 0.0


class HeadToHeadMatchupProfile(BaseModel):
    """Direct micro-battle between a specific striker and bowler."""
    striker_id: int
    striker_name: str
    bowler_id: int
    bowler_name: str
    balls_faced: int = 0
    legal_balls: int = 0
    runs_scored: int = 0
    dismissals: int = 0
    fours: int = 0
    sixes: int = 0
    dot_balls: int = 0
    strike_rate: float = 0.0
    dot_ball_pct: float = 0.0
    boundary_pct: float = 0.0


# ---------------------------------------------------------------------------
# Core Tactical Intelligence Engine
# ---------------------------------------------------------------------------

class DatasetCricketIntelligenceEngine:
    """
    Tactical intelligence service operating directly on the official
    Rajasthan Royals dataset with strictly governed cricket domain rules.
    """

    def __init__(self, data_dir: Optional[Path] = None):
        if data_dir is None:
            # Default to repo root standard location
            base_dir = Path(__file__).resolve().parent.parent.parent.parent
            self.data_dir = base_dir / "data" / "raw" / "rajasthan_royals" / "round_1_data_pack"
        else:
            self.data_dir = Path(data_dir)

        self._bbb_df: Optional[pd.DataFrame] = None
        self._matches_df: Optional[pd.DataFrame] = None
        self._competitions_df: Optional[pd.DataFrame] = None
        self._teams_df: Optional[pd.DataFrame] = None
        self._p11_df: Optional[pd.DataFrame] = None
        self._mapping_df: Optional[pd.DataFrame] = None
        self._player_names_map: Dict[int, str] = {}
        self._striker_ids: set[int] = set()
        self._bowler_ids: set[int] = set()
        self._is_loaded = False

    def load_data(self) -> None:
        """Loads and pre-processes the official data pack with domain safeguards."""
        if self._is_loaded:
            return

        if not self.data_dir.exists():
            raise FileNotFoundError(f"Official data pack directory not found: {self.data_dir}")

        # 1. Load mapping and build player lookup dict
        mapping_path = self.data_dir / "competition_team_player_mapping.csv"
        if mapping_path.exists():
            self._mapping_df = pd.read_csv(mapping_path)
            self._player_names_map = dict(
                zip(self._mapping_df["player_id"], self._mapping_df["player_name"])
            )

        # 2. Load matches & competitions
        matches_path = self.data_dir / "matches.csv"
        if matches_path.exists():
            self._matches_df = pd.read_csv(matches_path)

        comp_path = self.data_dir / "competitions.csv"
        if comp_path.exists():
            self._competitions_df = pd.read_csv(comp_path)

        teams_path = self.data_dir / "teams.csv"
        if teams_path.exists():
            self._teams_df = pd.read_csv(teams_path)

        p11_path = self.data_dir / "playing_eleven.csv"
        if p11_path.exists():
            self._p11_df = pd.read_csv(p11_path)

        # 3. Load ball-by-ball and apply domain cleaning
        bbb_path = self.data_dir / "ball_by_ball.csv"
        if bbb_path.exists():
            bbb = pd.read_csv(bbb_path)

            # Clean speed sensor anomalies (e.g., 1456.1 -> 145.61 km/h)
            raw_speed = bbb["bowl_speed"].fillna(0.0).astype(float)
            cleaned_speed = raw_speed.copy()
            cleaned_speed[raw_speed >= 500.0] = raw_speed[raw_speed >= 500.0] / 10.0
            cleaned_speed[(cleaned_speed < 50.0) | (cleaned_speed > 170.0)] = 0.0
            bbb["clean_bowl_speed"] = cleaned_speed

            # Identify strictly legal deliveries (re-bowled deliveries excluded)
            bbb["is_legal_delivery"] = ~bbb["extras_type"].isin(["wide", "Overstep"])

            # Governed Bowler Runs Conceded
            is_wide = (bbb["extras_type"] == "wide").astype(int)
            is_nb = (bbb["extras_type"] == "Overstep").astype(int)
            aux_runs = ((is_wide == 1) | (is_nb == 1)) & (bbb["extras_2_runs"] > 0)
            bowler_runs = bbb["runs"] + is_wide + is_nb + (aux_runs.astype(int) * bbb["extras_2_runs"])
            bbb["bowler_runs_conceded"] = bowler_runs

            # Governed Bowler Wickets (Exclude RunOut, Retired Out, Obstructing Field)
            non_bowler_dismissals = ["RunOut", "Retire Out", "Obstracting the field", "Obstructing the field"]
            bbb["is_bowler_wicket"] = bbb["is_wicket"] & ~bbb["dismissal_type"].isin(non_bowler_dismissals)

            # Match Phase Assignment (1-indexed overid)
            def assign_phase(o: int) -> str:
                if o <= 6:
                    return "Powerplay"
                elif o <= 15:
                    return "Middle"
                else:
                    return "Death"

            bbb["phase"] = bbb["overid"].apply(assign_phase)

            # Also populate player names in map from bbb if missing in mapping
            strikers = bbb[["striker_id", "striker_name"]].drop_duplicates()
            for _, r in strikers.iterrows():
                if r["striker_id"] not in self._player_names_map:
                    self._player_names_map[int(r["striker_id"])] = str(r["striker_name"])

            bowlers = bbb[["bowler_id", "bowler_name"]].drop_duplicates()
            for _, r in bowlers.iterrows():
                if r["bowler_id"] not in self._player_names_map:
                    self._player_names_map[int(r["bowler_id"])] = str(r["bowler_name"])

            # Cache distinct striker and bowler ID sets
            self._striker_ids = set(strikers["striker_id"].dropna().astype(int).tolist())
            self._bowler_ids = set(bowlers["bowler_id"].dropna().astype(int).tolist())

            self._bbb_df = bbb

        self._is_loaded = True

    @property
    def bbb(self) -> pd.DataFrame:
        if not self._is_loaded or self._bbb_df is None:
            self.load_data()
        return self._bbb_df

    def get_player_name(self, player_id: int) -> Optional[str]:
        """Resolves player ID to canonical name."""
        if not self._is_loaded:
            self.load_data()
        return self._player_names_map.get(player_id)

    def is_known_player(self, player_id: int) -> bool:
        """Checks if player exists in dataset."""
        if not self._is_loaded:
            self.load_data()
        return player_id in self._player_names_map

    def search_players(self, query: str = "", limit: int = 20) -> List[Dict[str, Any]]:
        """Searches players in dataset by name."""
        if not self._is_loaded:
            self.load_data()

        q = query.strip().lower()
        results = []
        # Sort keys to ensure stable ordering
        for pid in sorted(self._player_names_map.keys()):
            name = self._player_names_map[pid]
            if not q or q in name.lower():
                results.append({
                    "player_id": int(pid),
                    "player_name": name,
                    "is_batter": int(pid) in self._striker_ids,
                    "is_bowler": int(pid) in self._bowler_ids,
                    "total_deliveries": 0,
                })
                if len(results) >= limit:
                    break
        return results

    def get_dataset_summary(self) -> Dict[str, Any]:
        """Returns verified empirical totals across the official data pack."""
        df = self.bbb
        legal_balls = int(df["is_legal_delivery"].sum())
        total_runs_off_bat = int(df["runs"].sum())
        total_wickets = int(df["is_wicket"].sum())
        bowler_wickets = int(df["is_bowler_wicket"].sum())

        return {
            "total_deliveries": len(df),
            "legal_deliveries": legal_balls,
            "total_matches_with_deliveries": int(df["match_id"].nunique()),
            "total_unique_strikers": int(df["striker_id"].nunique()),
            "total_unique_bowlers": int(df["bowler_id"].nunique()),
            "total_runs_off_bat": total_runs_off_bat,
            "total_wickets_fallen": total_wickets,
            "total_bowler_wickets": bowler_wickets,
            "overall_run_rate_per_6_balls": round(total_runs_off_bat / legal_balls * 6.0, 2),
            "valid_radar_speed_records": int((df["clean_bowl_speed"] > 0).sum()),
            "data_provenance": "Official Rajasthan Royals Round 1 Data Pack",
        }

    def get_phase_splits(
        self,
        striker_id: Optional[int] = None,
        bowler_id: Optional[int] = None,
        phase: Optional[str] = None,
    ) -> Dict[str, TacticalPhaseSplit]:
        """
        Calculates Powerplay, Middle, and Death phase splits overall,
        or filtered for a specific batter or bowler.
        """
        df = self.bbb
        if striker_id is not None:
            df = df[df["striker_id"] == striker_id]
        elif bowler_id is not None:
            df = df[df["bowler_id"] == bowler_id]

        target_phases = [phase] if phase else ["Powerplay", "Middle", "Death"]
        splits: Dict[str, TacticalPhaseSplit] = {}

        for phase_name in target_phases:
            pdf = df[df["phase"] == phase_name]
            total_balls = len(pdf)
            legal_balls = int(pdf["is_legal_delivery"].sum())

            if total_balls == 0:
                splits[phase_name] = TacticalPhaseSplit(phase=phase_name)
                continue

            if striker_id is not None:
                runs = int(pdf["runs"].sum())
                wickets = int((pdf["dismissed_player_id"] == striker_id).sum())
                dots = int((pdf["runs"] == 0).sum())
                boundaries = int((pdf["is_four"] | pdf["is_six"]).sum())
                sr = round((runs / total_balls) * 100.0, 2)
                avg = round(runs / wickets, 2) if wickets > 0 else None
                bpw = round(total_balls / wickets, 1) if wickets > 0 else None
                splits[phase_name] = TacticalPhaseSplit(
                    phase=phase_name,
                    total_balls=total_balls,
                    legal_balls=legal_balls,
                    runs=runs,
                    wickets=wickets,
                    strike_rate=sr,
                    average=avg,
                    dot_ball_percentage=round((dots / total_balls) * 100.0, 2),
                    boundary_percentage=round((boundaries / total_balls) * 100.0, 2),
                    balls_per_wicket=bpw,
                )
            elif bowler_id is not None:
                runs = int(pdf["bowler_runs_conceded"].sum())
                wickets = int(pdf["is_bowler_wicket"].sum())
                dots = int((pdf["bowler_runs_conceded"] == 0).sum())
                econ = round((runs / legal_balls) * 6.0, 2) if legal_balls > 0 else None
                avg = round(runs / wickets, 2) if wickets > 0 else None
                bpw = round(legal_balls / wickets, 1) if wickets > 0 else None
                splits[phase_name] = TacticalPhaseSplit(
                    phase=phase_name,
                    total_balls=total_balls,
                    legal_balls=legal_balls,
                    runs=runs,
                    wickets=wickets,
                    economy_rate=econ,
                    average=avg,
                    dot_ball_percentage=round((dots / total_balls) * 100.0, 2),
                    boundary_percentage=round(((pdf["is_four"] | pdf["is_six"]).sum() / total_balls) * 100.0, 2),
                    balls_per_wicket=bpw,
                )
            else:
                runs = int(pdf["runs"].sum())
                wickets = int(pdf["is_bowler_wicket"].sum())
                dots = int((pdf["runs"] == 0).sum())
                boundaries = int((pdf["is_four"] | pdf["is_six"]).sum())
                rr = round((runs / legal_balls) * 6.0, 2) if legal_balls > 0 else None
                bpw = round(legal_balls / wickets, 1) if wickets > 0 else None
                splits[phase_name] = TacticalPhaseSplit(
                    phase=phase_name,
                    total_balls=total_balls,
                    legal_balls=legal_balls,
                    runs=runs,
                    wickets=wickets,
                    economy_rate=rr,
                    dot_ball_percentage=round((dots / total_balls) * 100.0, 2),
                    boundary_percentage=round((boundaries / total_balls) * 100.0, 2),
                    balls_per_wicket=bpw,
                )

        return splits

    def get_handedness_matrix(
        self,
        striker_id: Optional[int] = None,
        bowler_id: Optional[int] = None,
        batting_type: Optional[str] = None,
        pace_or_spin: Optional[str] = None,
    ) -> List[HandednessSplit]:
        """Computes the 4-way stance/bowling cross-split, with optional player filters."""
        df = self.bbb
        if striker_id is not None:
            df = df[df["striker_id"] == striker_id]
        if bowler_id is not None:
            df = df[df["bowler_id"] == bowler_id]

        target_btypes = [batting_type] if batting_type else ["RHB", "LHB"]
        target_ps = [pace_or_spin] if pace_or_spin else ["Pace", "Spin"]

        matrix: List[HandednessSplit] = []
        for btype in target_btypes:
            for ps in target_ps:
                sub = df[(df["batting_type"] == btype) & (df["pace_or_spin"] == ps)]
                balls = len(sub)
                legal_balls = int(sub["is_legal_delivery"].sum())
                runs = int(sub["runs"].sum())
                bowler_runs = int(sub["bowler_runs_conceded"].sum())
                wickets = int(sub["is_bowler_wicket"].sum())
                dots = int((sub["runs"] == 0).sum())
                boundaries = int((sub["is_four"] | sub["is_six"]).sum())

                sr = round((runs / balls) * 100.0, 2) if balls > 0 else 0.0
                econ = round((bowler_runs / legal_balls) * 6.0, 2) if legal_balls > 0 else 0.0
                avg = round(bowler_runs / wickets, 2) if wickets > 0 else None

                matrix.append(
                    HandednessSplit(
                        batting_type=btype,
                        pace_or_spin=ps,
                        balls_faced=balls,
                        runs_scored=runs,
                        wickets=wickets,
                        strike_rate=sr,
                        economy_rate=econ,
                        bowling_average=avg,
                        boundary_pct=round((boundaries / balls) * 100.0, 2) if balls > 0 else 0.0,
                        dot_pct=round((dots / balls) * 100.0, 2) if balls > 0 else 0.0,
                    )
                )

        return matrix

    def get_top_strokes(
        self,
        min_balls: int = 100,
        striker_id: Optional[int] = None,
        stroke_name: Optional[str] = None,
    ) -> List[TacticalStrokeProfile]:
        """Profiles stroke efficiency across all batters or for a single batter."""
        df = self.bbb[self.bbb["stroke"].notna()]
        if striker_id is not None:
            df = df[df["striker_id"] == striker_id]
        if stroke_name is not None:
            df = df[df["stroke"].str.lower() == stroke_name.lower()]

        if df.empty:
            return []

        agg = df.groupby("stroke").agg(
            deliveries=("match_id", "count"),
            runs=("runs", "sum"),
            dismissals=("is_wicket", "sum"),
            boundaries=("is_four", lambda x: (x | df.loc[x.index, "is_six"]).sum()),
        ).reset_index()

        agg = agg[agg["deliveries"] >= min_balls]
        if agg.empty:
            return []

        agg["runs_per_shot"] = (agg["runs"] / agg["deliveries"]).round(2)
        agg["dismissal_rate_pct"] = ((agg["dismissals"] / agg["deliveries"]) * 100.0).round(2)
        agg["boundary_pct"] = ((agg["boundaries"] / agg["deliveries"]) * 100.0).round(2)

        results = []
        for _, row in agg.sort_values(by="deliveries", ascending=False).iterrows():
            results.append(
                TacticalStrokeProfile(
                    stroke=row["stroke"],
                    deliveries_faced=int(row["deliveries"]),
                    runs_scored=int(row["runs"]),
                    dismissals=int(row["dismissals"]),
                    runs_per_shot=float(row["runs_per_shot"]),
                    dismissal_rate_pct=float(row["dismissal_rate_pct"]),
                    boundary_pct=float(row["boundary_pct"]),
                )
            )
        return results

    def get_top_delivery_styles(
        self,
        min_balls: int = 100,
        bowler_id: Optional[int] = None,
        delivery_style_name: Optional[str] = None,
    ) -> List[DeliveryStyleProfile]:
        """Profiles bowling variations and movement styles."""
        df = self.bbb[self.bbb["delivery_style"].notna()]
        if bowler_id is not None:
            df = df[df["bowler_id"] == bowler_id]
        if delivery_style_name is not None:
            df = df[df["delivery_style"].str.lower() == delivery_style_name.lower()]

        if df.empty:
            return []

        agg = df.groupby("delivery_style").agg(
            deliveries=("is_legal_delivery", "sum"),
            runs=("bowler_runs_conceded", "sum"),
            wickets=("is_bowler_wicket", "sum"),
            dots=("bowler_runs_conceded", lambda x: (x == 0).sum()),
        ).reset_index()

        agg = agg[agg["deliveries"] >= min_balls]
        if agg.empty:
            return []

        agg["economy"] = ((agg["runs"] / agg["deliveries"]) * 6.0).round(2)
        agg["average"] = (agg["runs"] / agg["wickets"].replace(0, np.nan)).round(2)
        agg["dot_pct"] = ((agg["dots"] / agg["deliveries"]) * 100.0).round(2)

        results = []
        for _, row in agg.sort_values(by="deliveries", ascending=False).iterrows():
            avg_val = float(row["average"]) if pd.notna(row["average"]) else None
            results.append(
                DeliveryStyleProfile(
                    delivery_style=row["delivery_style"],
                    deliveries_bowled=int(row["deliveries"]),
                    runs_conceded=int(row["runs"]),
                    wickets=int(row["wickets"]),
                    dot_balls=int(row["dots"]),
                    economy_rate=float(row["economy"]),
                    bowling_average=avg_val,
                    dot_ball_pct=float(row["dot_pct"]),
                )
            )
        return results

    def get_bowling_speed_profile(
        self,
        bowler_id: Optional[int] = None,
        min_balls: int = 30,
        top_n: int = 10,
    ) -> Dict[str, Any]:
        """
        Extracts delivery speed profile with radar sensor-quality safeguards.
        Scales 10x sensor anomalies (speeds >= 500 scaled by /10) and filters offline sensors.
        """
        df = self.bbb
        if bowler_id is not None:
            bdf = df[df["bowler_id"] == bowler_id]
            if bdf.empty:
                return {}

            bowler_name = self.get_player_name(bowler_id) or str(bdf["bowler_name"].iloc[0])
            total_delivs = len(bdf)
            valid_speeds = bdf[bdf["clean_bowl_speed"] > 0]["clean_bowl_speed"]
            valid_count = len(valid_speeds)

            if valid_count == 0:
                return {
                    "bowler_id": bowler_id,
                    "bowler_name": bowler_name,
                    "total_deliveries": total_delivs,
                    "valid_speed_deliveries": 0,
                    "speed_coverage_pct": 0.0,
                    "mean_speed_kmh": None,
                    "median_speed_kmh": None,
                    "min_speed_kmh": None,
                    "max_speed_kmh": None,
                    "std_speed_kmh": None,
                    "speed_brackets": {
                        "slow_under_110": 0,
                        "medium_110_to_125": 0,
                        "fast_medium_125_to_140": 0,
                        "express_over_140": 0,
                    },
                    "sensor_safeguards_applied": True,
                    "data_quality_note": "No valid radar sensor telemetry recorded for this bowler.",
                }

            mean_s = round(float(valid_speeds.mean()), 1)
            med_s = round(float(valid_speeds.median()), 1)
            min_s = round(float(valid_speeds.min()), 1)
            max_s = round(float(valid_speeds.max()), 1)
            std_s = round(float(valid_speeds.std()), 1) if valid_count > 1 else 0.0

            brackets = {
                "slow_under_110": int((valid_speeds < 110.0).sum()),
                "medium_110_to_125": int(((valid_speeds >= 110.0) & (valid_speeds < 125.0)).sum()),
                "fast_medium_125_to_140": int(((valid_speeds >= 125.0) & (valid_speeds < 140.0)).sum()),
                "express_over_140": int((valid_speeds >= 140.0).sum()),
            }

            return {
                "bowler_id": bowler_id,
                "bowler_name": bowler_name,
                "total_deliveries": total_delivs,
                "valid_speed_deliveries": valid_count,
                "speed_coverage_pct": round((valid_count / total_delivs) * 100.0, 1),
                "mean_speed_kmh": mean_s,
                "median_speed_kmh": med_s,
                "min_speed_kmh": min_s,
                "max_speed_kmh": max_s,
                "std_speed_kmh": std_s,
                "speed_brackets": brackets,
                "sensor_safeguards_applied": True,
                "data_quality_note": "Governed scaling applied to raw readings >= 500 km/h; offline sensors (<50 km/h) excluded.",
            }
        else:
            # Overall tournament speed profile
            valid_speeds = df[df["clean_bowl_speed"] > 0]
            total_delivs = len(df)
            valid_count = len(valid_speeds)

            bowler_agg = valid_speeds.groupby(["bowler_id", "bowler_name"]).agg(
                valid_balls=("clean_bowl_speed", "count"),
                mean_speed=("clean_bowl_speed", "mean"),
                max_speed=("clean_bowl_speed", "max"),
                express_balls=("clean_bowl_speed", lambda x: (x >= 140.0).sum()),
            ).reset_index()

            qualified = bowler_agg[bowler_agg["valid_balls"] >= min_balls]
            top_mean = qualified.sort_values(by="mean_speed", ascending=False).head(top_n)

            fastest_bowlers = []
            for _, r in top_mean.iterrows():
                fastest_bowlers.append({
                    "bowler_id": int(r["bowler_id"]),
                    "bowler_name": str(r["bowler_name"]),
                    "valid_deliveries": int(r["valid_balls"]),
                    "mean_speed_kmh": round(float(r["mean_speed"]), 1),
                    "max_speed_kmh": round(float(r["max_speed"]), 1),
                    "express_balls_count": int(r["express_balls"]),
                })

            all_speeds = valid_speeds["clean_bowl_speed"]
            return {
                "overall_valid_speed_deliveries": valid_count,
                "speed_coverage_pct": round((valid_count / total_delivs) * 100.0, 1),
                "mean_speed_kmh": round(float(all_speeds.mean()), 1),
                "median_speed_kmh": round(float(all_speeds.median()), 1),
                "min_speed_kmh": round(float(all_speeds.min()), 1),
                "max_speed_kmh": round(float(all_speeds.max()), 1),
                "top_fastest_bowlers": fastest_bowlers,
                "sensor_safeguards_applied": True,
                "data_quality_note": "Governed scaling applied to raw readings >= 500 km/h; offline sensors (<50 km/h) excluded.",
            }

    def get_player_tactical_profile(self, player_id: int) -> Optional[Dict[str, Any]]:
        """Synthesizes complete multi-dimensional tactical profile for an individual player."""
        if not self.is_known_player(player_id):
            return None

        player_name = self.get_player_name(player_id) or "Unknown Player"
        df = self.bbb
        batted_df = df[df["striker_id"] == player_id]
        bowled_df = df[df["bowler_id"] == player_id]

        is_batter = len(batted_df) > 0
        is_bowler = len(bowled_df) > 0

        batting_profile = None
        if is_batter:
            total_runs = int(batted_df["runs"].sum())
            total_balls = len(batted_df)
            fours = int(batted_df["is_four"].sum())
            sixes = int(batted_df["is_six"].sum())
            dots = int((batted_df["runs"] == 0).sum())
            sr = round((total_runs / total_balls) * 100.0, 2)
            bdry_pct = round(((fours + sixes) / total_balls) * 100.0, 2)
            dot_pct = round((dots / total_balls) * 100.0, 2)
            phases = self.get_phase_splits(striker_id=player_id)
            strokes = self.get_top_strokes(min_balls=5, striker_id=player_id)
            handedness = self.get_handedness_matrix(striker_id=player_id)

            batting_profile = {
                "total_runs": total_runs,
                "balls_faced": total_balls,
                "strike_rate": sr,
                "fours": fours,
                "sixes": sixes,
                "boundary_pct": bdry_pct,
                "dot_ball_pct": dot_pct,
                "phase_splits": {k: v.model_dump() for k, v in phases.items()},
                "top_strokes": [s.model_dump() for s in strokes[:5]],
                "handedness_splits": [h.model_dump() for h in handedness],
            }

        bowling_profile = None
        if is_bowler:
            legal_balls = int(bowled_df["is_legal_delivery"].sum())
            runs = int(bowled_df["bowler_runs_conceded"].sum())
            wickets = int(bowled_df["is_bowler_wicket"].sum())
            dots = int((bowled_df["bowler_runs_conceded"] == 0).sum())
            econ = round((runs / legal_balls) * 6.0, 2) if legal_balls > 0 else 0.0
            avg = round(runs / wickets, 2) if wickets > 0 else None
            dot_pct = round((dots / len(bowled_df)) * 100.0, 2)
            phases = self.get_phase_splits(bowler_id=player_id)
            variations = self.get_top_delivery_styles(min_balls=5, bowler_id=player_id)
            speed = self.get_bowling_speed_profile(bowler_id=player_id)

            bowling_profile = {
                "total_wickets": wickets,
                "legal_balls": legal_balls,
                "runs_conceded": runs,
                "economy_rate": econ,
                "bowling_average": avg,
                "dot_ball_pct": dot_pct,
                "phase_splits": {k: v.model_dump() for k, v in phases.items()},
                "top_variations": [v.model_dump() for v in variations[:5]],
                "speed_profile": speed,
            }

        return {
            "player_id": player_id,
            "player_name": player_name,
            "is_batter": is_batter,
            "is_bowler": is_bowler,
            "batting_profile": batting_profile,
            "bowling_profile": bowling_profile,
        }

    def get_top_death_batters(self, min_balls: int = 100, top_n: int = 10) -> List[Dict[str, Any]]:
        """Identifies elite finishers in overs 16–20."""
        df = self.bbb[self.bbb["phase"] == "Death"]
        agg = df.groupby(["striker_id", "striker_name"]).agg(
            runs=("runs", "sum"),
            balls=("match_id", "count"),
            fours=("is_four", "sum"),
            sixes=("is_six", "sum"),
            dots=("runs", lambda x: (x == 0).sum()),
        ).reset_index()

        agg = agg[agg["balls"] >= min_balls]
        agg["strike_rate"] = ((agg["runs"] / agg["balls"]) * 100.0).round(2)
        agg["boundary_pct"] = (((agg["fours"] + agg["sixes"]) / agg["balls"]) * 100.0).round(2)
        agg["dot_pct"] = ((agg["dots"] / agg["balls"]) * 100.0).round(2)

        top_df = agg.sort_values(by="strike_rate", ascending=False).head(top_n)
        return top_df.to_dict(orient="records")

    def get_top_death_bowlers(self, min_balls: int = 150, top_n: int = 10) -> List[Dict[str, Any]]:
        """Identifies elite containment and wicket-taking bowlers in overs 16–20."""
        df = self.bbb[self.bbb["phase"] == "Death"]
        agg = df.groupby(["bowler_id", "bowler_name", "bowling_type"]).agg(
            legal_balls=("is_legal_delivery", "sum"),
            runs=("bowler_runs_conceded", "sum"),
            wickets=("is_bowler_wicket", "sum"),
            dots=("bowler_runs_conceded", lambda x: (x == 0).sum()),
        ).reset_index()

        agg = agg[agg["legal_balls"] >= min_balls]
        agg["economy"] = ((agg["runs"] / agg["legal_balls"]) * 6.0).round(2)
        agg["average"] = (agg["runs"] / agg["wickets"].replace(0, np.nan)).round(2)
        agg["dot_pct"] = ((agg["dots"] / agg["legal_balls"]) * 100.0).round(2)

        top_df = agg.sort_values(by="economy", ascending=True).head(top_n)
        return top_df.to_dict(orient="records")

    def get_head_to_head(self, striker_id: int, bowler_id: int) -> Optional[HeadToHeadMatchupProfile]:
        """Extracts the exact historical micro-battle between a batter and bowler."""
        df = self.bbb[(self.bbb["striker_id"] == striker_id) & (self.bbb["bowler_id"] == bowler_id)]
        if df.empty:
            return None

        balls = len(df)
        legal_balls = int(df["is_legal_delivery"].sum())
        runs = int(df["runs"].sum())
        dismissals = int(df["is_bowler_wicket"].sum())
        fours = int(df["is_four"].sum())
        sixes = int(df["is_six"].sum())
        dots = int((df["runs"] == 0).sum())

        striker_name = self.get_player_name(striker_id) or str(df["striker_name"].iloc[0])
        bowler_name = self.get_player_name(bowler_id) or str(df["bowler_name"].iloc[0])

        sr = round((runs / balls) * 100.0, 2) if balls > 0 else 0.0
        dot_pct = round((dots / balls) * 100.0, 2) if balls > 0 else 0.0
        boundary_pct = round(((fours + sixes) / balls) * 100.0, 2) if balls > 0 else 0.0

        return HeadToHeadMatchupProfile(
            striker_id=striker_id,
            striker_name=striker_name,
            bowler_id=bowler_id,
            bowler_name=bowler_name,
            balls_faced=balls,
            legal_balls=legal_balls,
            runs_scored=runs,
            dismissals=dismissals,
            fours=fours,
            sixes=sixes,
            dot_balls=dots,
            strike_rate=sr,
            dot_ball_pct=dot_pct,
            boundary_pct=boundary_pct,
        )

    def get_rajasthan_royals_squad_intelligence(self) -> List[Dict[str, Any]]:
        """Extracts tactical intelligence dossiers for core Rajasthan Royals players."""
        rr_players = [
            {"id": 813, "name": "Jos Buttler", "role": "Wicketkeeper-Batter"},
            {"id": 2258, "name": "Sanju Samson", "role": "Captain / Top-Order Batter"},
            {"id": 6819, "name": "Yashasvi Jaiswal", "role": "Opener / Aggressor"},
            {"id": 6423, "name": "Riyan Parag", "role": "Middle-Order Batter"},
            {"id": 3297, "name": "Shimron Hetmyer", "role": "Middle/Death Finisher"},
            {"id": 1612, "name": "Yuzvendra Chahal", "role": "Leg-Break Specialist"},
            {"id": 2320, "name": "Trent Boult", "role": "Left-Arm Fast Spearhead"},
        ]

        dossiers = []
        for p in rr_players:
            pid = p["id"]
            phases = self.get_phase_splits(
                striker_id=pid if "Batter" in p["role"] or "Finisher" in p["role"] or "Aggressor" in p["role"] else None,
                bowler_id=pid if "Specialist" in p["role"] or "Spearhead" in p["role"] else None,
            )
            dossiers.append({
                "player_id": pid,
                "player_name": p["name"],
                "role": p["role"],
                "phase_profiles": {k: v.model_dump() for k, v in phases.items()},
            })

        return dossiers
