"""
Royals Intelligence - Manual Import Adapter
Compliant import route for structured user/scout-supplied datasets without web scraping.
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
import pandas as pd

from app.acquisition.adapters.base import BaseSourceAdapter
from app.core.logging import logger


class ManualImportAdapter(BaseSourceAdapter):
    """Adapter for compliant user-supplied manual JSON and CSV datasets."""

    def __init__(self):
        super().__init__(
            source_id="manual_import",
            name="Compliant Manual Dataset Import",
            tier="TIER_3",
        )

    async def verify_connectivity(self) -> Dict[str, Any]:
        """Local filesystem adapter is always accessible."""
        return {
            "source_id": self.source_id,
            "is_accessible": True,
            "status": "OPERATIONAL",
            "tier": self.tier,
        }

    async def fetch(self, target_params: Dict[str, Any], destination_dir: Path) -> List[Path]:
        """Collects files specified in target_params."""
        paths = target_params.get("file_paths", [])
        valid_paths = [Path(p) for p in paths if Path(p).exists()]
        return valid_paths

    def parse_raw_artifact(self, file_path: Path) -> Dict[str, Any]:
        suffix = file_path.suffix.lower()
        if suffix == ".json":
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        elif suffix == ".csv":
            df = pd.read_csv(file_path)
            return {"format": "csv", "records": df.to_dict(orient="records")}
        else:
            raise ValueError(f"Unsupported file format '{suffix}' for manual import.")

