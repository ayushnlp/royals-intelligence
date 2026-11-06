"""
Royals Intelligence - Source Registry Manager
Loads, queries, and audits registered cricket data sources.
"""

import json
from pathlib import Path
from typing import List, Optional, Dict, Any
from app.core.config import settings, get_repo_root
from app.core.logging import logger


class SourceRegistryManager:
    """Manages cricket data source discovery, metadata, and reliability tiers."""

    def __init__(self, registry_path: Optional[Path] = None):
        if registry_path is None:
            root_dir = get_repo_root()
            self.registry_path = root_dir / "data" / "metadata" / "sources" / "source_registry.json"
        else:
            self.registry_path = Path(registry_path)
            
        self._cache: Optional[Dict[str, Any]] = None

    def _load(self) -> Dict[str, Any]:
        if self._cache is not None:
            return self._cache
            
        if not self.registry_path.exists():
            logger.warning(f"Source registry file not found at {self.registry_path}. Returning empty catalog.")
            return {"version": "1.0.0", "sources": [], "reliability_tiers": {}}

        try:
            with open(self.registry_path, "r", encoding="utf-8") as f:
                self._cache = json.load(f)
                return self._cache
        except Exception as exc:
            logger.error(f"Failed to parse source registry {self.registry_path}: {exc}")
            return {"version": "1.0.0", "sources": [], "reliability_tiers": {}}

    def list_sources(self, tier: Optional[str] = None, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """List registered sources with optional filtering by tier or category."""
        data = self._load()
        sources = data.get("sources", [])
        if tier:
            sources = [s for s in sources if s.get("tier") == tier]
        if category:
            sources = [s for s in sources if category.lower() in s.get("category", "").lower()]
        return sources

    def get_source(self, source_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve details for a specific registered data source."""
        sources = self.list_sources()
        for s in sources:
            if s.get("source_id") == source_id:
                return s
        return None

    def get_reliability_tiers(self) -> Dict[str, Any]:
        """Return the official reliability tier classifications and criteria."""
        return self._load().get("reliability_tiers", {})

    def check_source_availability(self, source_id: str) -> Dict[str, Any]:
        """Inspect operational accessibility and status of a data source."""
        source = self.get_source(source_id)
        if not source:
            return {"source_id": source_id, "status": "NOT_REGISTERED", "is_accessible": False}

        tier = source.get("tier")
        status = source.get("status", "unknown")

        if tier == "TIER_4":
            return {
                "source_id": source_id,
                "status": "RESTRICTED_MANUAL_ONLY",
                "is_accessible": False,
                "reason": "Direct web scraping is prohibited by Terms of Service. Manual CSV/JSON export supported."
            }

        return {
            "source_id": source_id,
            "status": "AVAILABLE" if status == "active" else status.upper(),
            "is_accessible": status == "active",
            "tier": tier,
            "access_method": source.get("access_method"),
            "rate_limits": source.get("rate_limits")
        }


# Singleton instance
source_registry = SourceRegistryManager()
