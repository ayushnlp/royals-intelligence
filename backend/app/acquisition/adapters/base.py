"""
Royals Intelligence - Base Source Adapter Interface
Defines the standard contract that all cricket data source adapters must implement.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime


class BaseSourceAdapter(ABC):
    """Abstract Base Class for all ingestion source adapters."""

    def __init__(self, source_id: str, name: str, tier: str):
        self.source_id = source_id
        self.name = name
        self.tier = tier

    @abstractmethod
    async def verify_connectivity(self) -> Dict[str, Any]:
        """Verify network or filesystem connectivity to the source."""
        pass

    @abstractmethod
    async def fetch(self, target_params: Dict[str, Any], destination_dir: Path) -> List[Path]:
        """
        Fetch or ingest source data into destination directory.
        Returns list of local file paths created.
        """
        pass

    @abstractmethod
    def parse_raw_artifact(self, file_path: Path) -> Dict[str, Any]:
        """
        Parse raw source file (JSON/CSV) into intermediate Python dictionary representation.
        """
        pass

