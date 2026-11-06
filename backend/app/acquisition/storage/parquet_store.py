"""
Royals Intelligence - Columnar Parquet Storage Layer
Converts normalized delivery and match events into partitioned Apache Parquet datasets.
"""

from pathlib import Path
from typing import List, Dict, Any, Optional
import pandas as pd
from app.core.logging import logger
from app.core.config import get_repo_root


class ParquetStorageManager:
    """Manages high-performance columnar storage for ball-by-ball deliveries and matches."""

    def __init__(self, processed_dir: Optional[Path] = None):
        if processed_dir is None:
            root_dir = get_repo_root()
            self.processed_dir = root_dir / "data" / "processed"
        else:
            self.processed_dir = Path(processed_dir)

        self.ball_by_ball_dir = self.processed_dir / "ball_by_ball"
        self.matches_dir = self.processed_dir / "matches"
        self.ball_by_ball_dir.mkdir(parents=True, exist_ok=True)
        self.matches_dir.mkdir(parents=True, exist_ok=True)

    def write_deliveries_parquet(self, deliveries: List[Dict[str, Any]], season: str) -> Path:
        """
        Writes deliveries to a season-partitioned parquet file.
        Appends or creates data/processed/ball_by_ball/season={season}/deliveries.parquet
        """
        if not deliveries:
            logger.warning("No deliveries provided to write_deliveries_parquet.")
            partition_dir = self.ball_by_ball_dir / f"season={season}"
            partition_dir.mkdir(parents=True, exist_ok=True)
            return partition_dir / "deliveries.parquet"

        clean_season = str(season).replace(" ", "_").replace("/", "_")
        partition_dir = self.ball_by_ball_dir / f"season={clean_season}"
        partition_dir.mkdir(parents=True, exist_ok=True)
        target_path = partition_dir / "deliveries.parquet"

        new_df = pd.DataFrame(deliveries)

        if target_path.exists():
            try:
                existing_df = pd.read_parquet(target_path)
                # Deduplicate based on (match_id, innings_number, over_number, ball_in_over)
                combined_df = pd.concat([existing_df, new_df], ignore_index=True)
                combined_df.drop_duplicates(
                    subset=["match_id", "innings_number", "over_number", "ball_in_over"],
                    keep="last",
                    inplace=True
                )
                combined_df.to_parquet(target_path, index=False, engine="pyarrow", compression="snappy")
                logger.info(f"Updated parquet partition {target_path} (total rows: {len(combined_df)})")
                return target_path
            except Exception as e:
                logger.error(f"Error appending to existing parquet {target_path}: {e}. Overwriting.")

        new_df.to_parquet(target_path, index=False, engine="pyarrow", compression="snappy")
        logger.info(f"Created new parquet partition {target_path} ({len(new_df)} deliveries)")
        return target_path

    def write_matches_parquet(self, matches: List[Dict[str, Any]]) -> Path:
        """
        Writes or updates the global matches parquet catalog at data/processed/matches/matches.parquet
        """
        target_path = self.matches_dir / "matches.parquet"
        if not matches:
            return target_path

        new_df = pd.DataFrame(matches)

        if target_path.exists():
            try:
                existing_df = pd.read_parquet(target_path)
                combined_df = pd.concat([existing_df, new_df], ignore_index=True)
                combined_df.drop_duplicates(subset=["match_id"], keep="last", inplace=True)
                combined_df.to_parquet(target_path, index=False, engine="pyarrow", compression="snappy")
                logger.info(f"Updated matches parquet {target_path} (total matches: {len(combined_df)})")
                return target_path
            except Exception as e:
                logger.error(f"Error appending to matches parquet {target_path}: {e}")

        new_df.to_parquet(target_path, index=False, engine="pyarrow", compression="snappy")
        logger.info(f"Created matches parquet {target_path} ({len(new_df)} matches)")
        return target_path

    def query_deliveries(
        self,
        season: Optional[str] = None,
        match_id: Optional[str] = None,
        batter: Optional[str] = None,
        bowler: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Query delivery events with fast predicate pushdown over Parquet files.
        """
        files_to_read: List[Path] = []
        if season:
            clean_season = str(season).replace(" ", "_").replace("/", "_")
            p = self.ball_by_ball_dir / f"season={clean_season}" / "deliveries.parquet"
            if p.exists():
                files_to_read.append(p)
        else:
            files_to_read = list(self.ball_by_ball_dir.glob("season=*/deliveries.parquet"))

        if not files_to_read:
            return pd.DataFrame()

        df_list = []
        for fp in files_to_read:
            try:
                df = pd.read_parquet(fp)
                if match_id:
                    df = df[df["match_id"] == match_id]
                if batter:
                    df = df[df["striker"].str.lower() == batter.lower()]
                if bowler:
                    df = df[df["bowler"].str.lower() == bowler.lower()]
                df_list.append(df)
            except Exception as e:
                logger.error(f"Error reading parquet file {fp}: {e}")

        if not df_list:
            return pd.DataFrame()
        return pd.concat(df_list, ignore_index=True)

    def get_storage_stats(self) -> Dict[str, Any]:
        """Calculates total indexed matches, deliveries, and partition summaries."""
        partitions = [p.name for p in self.ball_by_ball_dir.glob("season=*")]
        total_deliveries = 0
        for fp in self.ball_by_ball_dir.glob("season=*/deliveries.parquet"):
            try:
                df = pd.read_parquet(fp, columns=["match_id"])
                total_deliveries += len(df)
            except Exception:
                pass

        total_matches = 0
        matches_file = self.matches_dir / "matches.parquet"
        if matches_file.exists():
            try:
                df_matches = pd.read_parquet(matches_file)
                total_matches = len(df_matches)
            except Exception:
                pass

        return {
            "total_matches_indexed": total_matches,
            "total_deliveries_indexed": total_deliveries,
            "seasons_partitioned": partitions,
            "partitions_count": len(partitions),
        }
