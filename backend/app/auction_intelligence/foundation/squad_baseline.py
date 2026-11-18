"""
Royals Intelligence - RR Auction & Retention Intelligence
AUCTION-00: Rajasthan Royals 2026 Squad Baseline Service.
"""

from pathlib import Path
from typing import Dict, Any, List, Optional
import pandas as pd

from app.core.config import get_repo_root
from app.core.logging import logger
from app.schemas.auction.foundation import (
    RRSquadRoleBreakdown,
    RRSquadPlayerEntry,
)
from app.auction_intelligence.foundation.data_ingestion import DataIngestionService

# Known trade and contract governance disclaimers in the supplied data pack
DISCLAIMERS = {
    "Sanju Samson": (
        "Listed under Chennai Super Kings (CSK) in ipl_players.csv (Row 1). "
        "Historical captain of Rajasthan Royals (2021-2024). Decoupled contract status."
    ),
    "Ravindra Jadeja": (
        "Listed under Rajasthan Royals (RR) in ipl_players.csv (Row 173). "
        "Historical CSK franchise stalwart; included as RR benchmark entry in data pack."
    ),
    "Sam Curran": (
        "Listed under Rajasthan Royals (RR) in ipl_players.csv (Row 174). "
        "Historical PBKS franchise entry; included as RR benchmark entry in data pack."
    ),
    "Ravi Bishnoi": (
        "Appears twice in ipl_players.csv: Row 179 (RR) and Row 261 (LSG). "
        "Single physical individual with dual-franchise historical attribution."
    ),
}


class RRSquadBaselineService:
    """Extracts and reconciles the Rajasthan Royals 2026 squad baseline from raw data."""

    def __init__(self, ingestion_service: Optional[DataIngestionService] = None):
        self.ingestion = ingestion_service or DataIngestionService()

    def get_squad_entries(self) -> List[RRSquadPlayerEntry]:
        """Loads and parses the 27 RR player entries in ipl_players.csv."""
        players_df = self.ingestion.load_dataset("ipl_players.csv")
        rr_df = players_df[players_df["Team"] == "Rajasthan Royals"].copy()

        entries: List[RRSquadPlayerEntry] = []
        for idx, row in rr_df.iterrows():
            name = str(row["Name"]).strip()
            role = str(row["Role"]).strip()
            batting_style = str(row["Batting_Style"]).strip()
            bowling_style = str(row["Bowling_Style"]).strip() if pd.notna(row["Bowling_Style"]) else None
            spin_type = str(row["Spin_Type"]).strip() if pd.notna(row["Spin_Type"]) else None

            disclaimer = DISCLAIMERS.get(name)

            entries.append(
                RRSquadPlayerEntry(
                    player_id=int(idx),
                    player_name=name,
                    role=role,
                    batting_style=batting_style,
                    bowling_style=bowling_style,
                    spin_type=spin_type,
                    disclaimer_flag=disclaimer,
                )
            )
        return entries

    def get_role_breakdown(self) -> RRSquadRoleBreakdown:
        """Returns the role breakdown for the 27 RR players."""
        entries = self.get_squad_entries()
        bowlers = sum(1 for e in entries if e.role == "Bowler")
        all_rounders = sum(1 for e in entries if e.role == "All-rounder")
        batters = sum(1 for e in entries if e.role == "Batter")
        keepers = sum(1 for e in entries if e.role == "Wicketkeeper-Batter")

        return RRSquadRoleBreakdown(
            bowlers=bowlers,
            all_rounders=all_rounders,
            batters=batters,
            wicketkeeper_batters=keepers,
            total_players=len(entries),
        )

    def get_disclaimer_audit(self) -> Dict[str, str]:
        """Returns all player disclaimers for the squad baseline."""
        return DISCLAIMERS.copy()
