"""
Royals Intelligence - Open-Meteo Weather Adapter
Fetches environmental, pitch conditions, and dew-point telemetry for IPL stadiums.
"""

from pathlib import Path
from typing import List, Dict, Any, Optional
import json
import httpx

from app.acquisition.adapters.base import BaseSourceAdapter
from app.core.logging import logger

VENUE_COORDINATES: Dict[str, Dict[str, float]] = {
    "SMS_JAIPUR": {"latitude": 26.8939, "longitude": 75.8037},
    "BARS_GUWAHATI": {"latitude": 26.1511, "longitude": 91.7342},
    "WANKHEDE_MUMBAI": {"latitude": 18.9389, "longitude": 72.8258},
    "CHIDAMBARAM_CHENNAI": {"latitude": 13.0628, "longitude": 80.2793},
    "EDEN_KOLKATA": {"latitude": 22.5646, "longitude": 88.3433},
    "CHINNASWAMY_BLR": {"latitude": 12.9788, "longitude": 77.5996},
    "MODI_AHMEDABAD": {"latitude": 23.0919, "longitude": 72.5975},
}


class OpenMeteoWeatherAdapter(BaseSourceAdapter):
    """Adapter for Open-Meteo Historical & Forecast Meteorological API."""

    def __init__(self):
        super().__init__(
            source_id="open_meteo_historical",
            name="Open-Meteo Weather Archive",
            tier="TIER_1",
        )
        self.archive_base_url = "https://archive-api.open-meteo.com/v1/archive"

    async def verify_connectivity(self) -> Dict[str, Any]:
        """Validates API availability."""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                res = await client.get(
                    self.archive_base_url,
                    params={
                        "latitude": 26.8939,
                        "longitude": 75.8037,
                        "start_date": "2024-04-01",
                        "end_date": "2024-04-01",
                        "hourly": "temperature_2m",
                    }
                )
                return {
                    "source_id": self.source_id,
                    "is_accessible": res.status_code == 200,
                    "status_code": res.status_code,
                    "tier": self.tier,
                }
        except Exception as e:
            return {
                "source_id": self.source_id,
                "is_accessible": False,
                "error": str(e),
                "note": "Open-Meteo external service unreachable; offline mock telemetry fallback active.",
                "tier": self.tier,
            }

    async def fetch(self, target_params: Dict[str, Any], destination_dir: Path) -> List[Path]:
        """
        Fetches hourly weather data for a venue and date range.
        target_params:
        - 'venue_code': e.g. 'SMS_JAIPUR'
        - 'start_date': 'YYYY-MM-DD'
        - 'end_date': 'YYYY-MM-DD'
        """
        destination_dir.mkdir(parents=True, exist_ok=True)
        venue_code = target_params.get("venue_code", "SMS_JAIPUR")
        start_date = target_params.get("start_date", "2024-04-01")
        end_date = target_params.get("end_date", start_date)

        coords = VENUE_COORDINATES.get(venue_code, {"latitude": 26.8939, "longitude": 75.8037})
        out_file = destination_dir / f"weather_{venue_code}_{start_date}.json"

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.get(
                    self.archive_base_url,
                    params={
                        "latitude": coords["latitude"],
                        "longitude": coords["longitude"],
                        "start_date": start_date,
                        "end_date": end_date,
                        "hourly": ["temperature_2m", "relative_humidity_2m", "dew_point_2m", "wind_speed_10m", "surface_pressure"],
                    }
                )
                if res.status_code == 200:
                    with open(out_file, "w", encoding="utf-8") as f:
                        f.write(res.text)
                    return [out_file]
                else:
                    logger.warning(f"Open-Meteo returned status {res.status_code}")
                    return []
        except Exception as e:
            logger.warning(f"Failed to fetch weather from Open-Meteo: {e}")
            return []

    def parse_raw_artifact(self, file_path: Path) -> Dict[str, Any]:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
