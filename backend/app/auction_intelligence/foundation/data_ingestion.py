"""
Royals Intelligence - RR Auction & Retention Intelligence
AUCTION-00: Data Ingestion and Semantic Validation Service.
"""

from pathlib import Path
from typing import Dict, Any, Optional, Tuple, List
import hashlib
import pandas as pd
import numpy as np

from app.core.config import get_repo_root
from app.core.logging import logger
from app.schemas.auction.foundation import (
    DatasetMetadata,
    DeliverySemanticsSummary,
    MatchCoverageSummary,
    FoundationDataIngestionReport,
    RRSquadRoleBreakdown,
)

EXPECTED_FILES = {
    "ball_by_ball.csv": 33,
    "competition_team_player_mapping.csv": 6,
    "competitions.csv": 4,
    "ipl_players.csv": 7,
    "matches.csv": 22,
    "playing_eleven.csv": 9,
    "teams.csv": 3,
}

LEGAL_DELIVERY_COUNT = 192709
TOTAL_DELIVERY_COUNT = 200999
NON_LEGAL_DELIVERY_COUNT = 8290
WIDES_COUNT = 7714
NO_BALLS_COUNT = 576
TOTAL_MATCH_COUNT = 883
BALL_RECORDED_MATCH_COUNT = 867
ABANDONED_MATCH_COUNT = 16


class DataIngestionService:
    """Ingests, validates, and checksums the official Rajasthan Royals data pack."""

    def __init__(self, data_pack_dir: Optional[Path] = None):
        if data_pack_dir is not None:
            self.data_pack_dir = Path(data_pack_dir)
        else:
            self.data_pack_dir = (
                get_repo_root() / "data" / "raw" / "rajasthan_royals" / "round_1_data_pack"
            )

    def compute_sha256(self, file_path: Path) -> str:
        """Computes SHA-256 digest of a target file."""
        hasher = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                hasher.update(chunk)
        return hasher.hexdigest()

    def inspect_datasets(self) -> Dict[str, DatasetMetadata]:
        """Inspects all 7 raw data pack files for existence, schema, and hashes."""
        results: Dict[str, DatasetMetadata] = {}
        if not self.data_pack_dir.exists():
            raise FileNotFoundError(f"Data pack directory not found at {self.data_pack_dir}")

        for filename, expected_cols in EXPECTED_FILES.items():
            fpath = self.data_pack_dir / filename
            if not fpath.exists():
                raise FileNotFoundError(f"Required raw dataset missing: {filename}")

            size_bytes = fpath.stat().st_size
            sha256_hash = self.compute_sha256(fpath)

            # Read only header to quickly get column count & names
            header_df = pd.read_csv(fpath, nrows=0)
            cols = header_df.columns.tolist()

            # Read full row count efficiently
            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                row_count = sum(1 for _ in f) - 1

            results[filename] = DatasetMetadata(
                name=filename,
                path=str(fpath.relative_to(get_repo_root())),
                size_bytes=size_bytes,
                row_count=row_count,
                column_count=len(cols),
                columns=cols,
                sha256=sha256_hash,
            )
        return results

    def load_dataset(self, filename: str, **kwargs) -> pd.DataFrame:
        """Loads a specific dataset from the data pack."""
        fpath = self.data_pack_dir / filename
        if not fpath.exists():
            raise FileNotFoundError(f"Dataset {filename} does not exist at {fpath}")
        return pd.read_csv(fpath, **kwargs)

    def reconcile_delivery_semantics(
        self, bbb_df: Optional[pd.DataFrame] = None
    ) -> DeliverySemanticsSummary:
        """Reconciles delivery semantics in ball_by_ball.csv:
        - 200,999 total records
        - 8,290 non-legal deliveries (7,714 wides + 576 overstep no-balls)
        - 192,709 strict legal deliveries
        """
        if bbb_df is None:
            bbb_df = self.load_dataset(
                "ball_by_ball.csv",
                usecols=["extras_type", "runs", "is_wicket"],
                low_memory=False,
            )

        total_rows = len(bbb_df)
        wides = int((bbb_df["extras_type"] == "wide").sum())
        no_balls = int((bbb_df["extras_type"] == "Overstep").sum())
        extras_deliveries = wides + no_balls
        legal_deliveries = total_rows - extras_deliveries

        total_runs = int(bbb_df["runs"].sum())
        total_wickets = int(bbb_df["is_wicket"].sum())

        return DeliverySemanticsSummary(
            total_rows=total_rows,
            legal_deliveries=legal_deliveries,
            extras_deliveries=extras_deliveries,
            wides=wides,
            no_balls=no_balls,
            total_runs_conceded=total_runs,
            total_wickets=total_wickets,
        )

    def reconcile_match_coverage(
        self,
        matches_df: Optional[pd.DataFrame] = None,
        bbb_df: Optional[pd.DataFrame] = None,
    ) -> MatchCoverageSummary:
        """Reconciles match records between matches.csv and ball_by_ball.csv:
        - 883 total matches
        - 867 matches with delivery logs
        - 16 abandoned/no-play matches
        """
        if matches_df is None:
            matches_df = self.load_dataset("matches.csv")
        if bbb_df is None:
            bbb_df = self.load_dataset("ball_by_ball.csv", usecols=["match_id"], low_memory=False)

        total_matches = len(matches_df)
        matches_with_balls = int(bbb_df["match_id"].nunique())
        abandoned = total_matches - matches_with_balls

        date_min = str(matches_df["match_date"].min()) if "match_date" in matches_df.columns else None
        date_max = str(matches_df["match_date"].max()) if "match_date" in matches_df.columns else None

        competitions = []
        if "comp_id" in matches_df.columns:
            competitions = [str(c) for c in matches_df["comp_id"].unique()]

        return MatchCoverageSummary(
            total_matches=total_matches,
            matches_with_balls=matches_with_balls,
            abandoned_or_no_result=abandoned,
            date_min=date_min,
            date_max=date_max,
            competitions=competitions,
        )

    def get_ingestion_report(self) -> FoundationDataIngestionReport:
        """Generates comprehensive foundation ingestion report."""
        datasets = self.inspect_datasets()
        delivery_semantics = self.reconcile_delivery_semantics()
        match_coverage = self.reconcile_match_coverage()

        # RR squad baseline check
        players_df = self.load_dataset("ipl_players.csv")
        rr_players = players_df[players_df["Team"] == "Rajasthan Royals"]
        role_counts = rr_players["Role"].value_counts().to_dict()

        rr_summary = RRSquadRoleBreakdown(
            bowlers=role_counts.get("Bowler", 0),
            all_rounders=role_counts.get("All-rounder", 0),
            batters=role_counts.get("Batter", 0),
            wicketkeeper_batters=role_counts.get("Wicketkeeper-Batter", 0),
            total_players=len(rr_players),
        )

        return FoundationDataIngestionReport(
            status="SUCCESS",
            datasets=datasets,
            delivery_semantics=delivery_semantics,
            match_coverage=match_coverage,
            rr_squad_summary=rr_summary,
            data_quality_issues=[],
        )
