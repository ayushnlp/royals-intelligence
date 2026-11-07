"""
Royals Intelligence - Cricsheet Open Data Adapter
Ingests verified ball-by-ball JSON match feeds conforming to Cricsheet specification.
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional
import httpx

from app.acquisition.adapters.base import BaseSourceAdapter
from app.core.logging import logger


class CricsheetAdapter(BaseSourceAdapter):
    """Adapter for Cricsheet Open Data Commons ODbL ball-by-ball datasets."""

    def __init__(self):
        super().__init__(
            source_id="cricsheet_open",
            name="Cricsheet Open Cricket Data",
            tier="TIER_1",
        )
        self.base_url = "https://cricsheet.org/downloads"

    async def verify_connectivity(self) -> Dict[str, Any]:
        """Probes Cricsheet endpoint availability with a lightweight HEAD request."""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                res = await client.head("https://cricsheet.org")
                is_ok = res.status_code < 400
                return {
                    "source_id": self.source_id,
                    "is_accessible": is_ok,
                    "status_code": res.status_code,
                    "tier": self.tier,
                }
        except Exception as e:
            return {
                "source_id": self.source_id,
                "is_accessible": False,
                "error": str(e),
                "note": "External network or proxy limitation; local offline match ingestion available.",
                "tier": self.tier,
            }

    async def fetch(self, target_params: Dict[str, Any], destination_dir: Path) -> List[Path]:
        """
        Fetches local or remote Cricsheet match files.
        Target params:
        - 'local_dir': path to local folder containing Cricsheet JSON files
        - 'file_paths': list of specific local paths
        """
        destination_dir.mkdir(parents=True, exist_ok=True)
        local_dir = target_params.get("local_dir")
        file_paths = target_params.get("file_paths", [])

        results: List[Path] = []
        if local_dir:
            src_path = Path(local_dir)
            if src_path.exists():
                for json_file in src_path.glob("*.json"):
                    results.append(json_file)

        for fp in file_paths:
            p = Path(fp)
            if p.exists() and p.suffix.lower() == ".json":
                results.append(p)

        logger.info(f"CricsheetAdapter discovered {len(results)} match files.")
        return results

    def parse_raw_artifact(self, file_path: Path) -> Dict[str, Any]:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

