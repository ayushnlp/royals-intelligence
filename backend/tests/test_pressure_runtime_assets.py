"""
Royals Intelligence - Pressure Runtime Asset Resolution Tests
Verifies deterministic resolution of the four required Pressure Intelligence Parquet datasets
across local repo paths, custom DATA_DIR mounts, and missing-asset fallback diagnostics.
"""

import os
import shutil
import tempfile
from pathlib import Path
import pytest
import pandas as pd
from fastapi.testclient import TestClient

from app.analytics.pressure_intelligence import PressureIntelligenceEngine
from app.analytics.uncapped_pressure_intelligence import UncappedPressureIntelligenceService
from app.core.config import resolve_asset_path


@pytest.mark.unit
def test_resolve_pressure_assets_in_local_layout():
    """Confirms all four pressure artifacts resolve successfully in local repository layout."""
    for filename in [
        "batting_leaderboard.parquet",
        "bowling_leaderboard.parquet",
        "batting_evidence_profiles.parquet",
        "bowling_evidence_profiles.parquet",
    ]:
        path = resolve_asset_path(filename, required=True)
        assert path.exists(), f"Failed to locate {filename}"
        assert path.stat().st_size > 0


@pytest.mark.unit
def test_pressure_engine_loads_and_preserves_analytical_metrics():
    """Confirms PressureIntelligenceEngine loads real data and preserves governing metrics."""
    engine = PressureIntelligenceEngine()
    engine.load_data()
    overview = engine.get_overview()

    # Analytical Invariants
    assert overview["strict_pressure_bowling_balls"] == 37014
    assert overview["strict_pressure_batting_balls"] == 31163
    assert overview["death_overs_bowling_pressure_share_pct"] == 87.28
    assert overview["total_evaluated_batters"] == 278
    assert overview["total_evaluated_bowlers"] == 239

    batters = engine.get_batting_leaderboard(limit=10, qualified_only=True)
    assert len(batters) == 10
    assert batters[0]["rank"] == 1
    assert batters[0]["player_name"] == "Nicholas Pooran"

    bowlers = engine.get_bowling_leaderboard(limit=10, qualified_only=True)
    assert len(bowlers) == 10
    assert bowlers[0]["rank"] == 1
    assert bowlers[0]["player_name"] == "Jasprit Bumrah"


@pytest.mark.unit
def test_pressure_engine_resolves_from_custom_data_dir():
    """Confirms engine loads from an externally mounted DATA_DIR (simulating Render Persistent Disk)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        pressure_dir = tmp_path / "pressure"
        pressure_dir.mkdir(parents=True, exist_ok=True)

        # Copy original parquets to temporary mounted path
        repo_pressure = resolve_asset_path("batting_leaderboard.parquet").parent
        for f in [
            "batting_leaderboard.parquet",
            "bowling_leaderboard.parquet",
            "batting_evidence_profiles.parquet",
            "bowling_evidence_profiles.parquet",
        ]:
            shutil.copy2(repo_pressure / f, pressure_dir / f)

        orig_data_dir = os.environ.get("DATA_DIR")
        try:
            os.environ["DATA_DIR"] = str(tmp_path)
            engine = PressureIntelligenceEngine()
            engine.load_data()
            assert engine._is_loaded is True
            overview = engine.get_overview()
            assert overview["strict_pressure_batting_balls"] == 31163
        finally:
            if orig_data_dir is not None:
                os.environ["DATA_DIR"] = orig_data_dir
            else:
                os.environ.pop("DATA_DIR", None)


@pytest.mark.unit
def test_pressure_engine_fails_descriptively_when_assets_missing():
    """Confirms engine raises descriptive FileNotFoundError without fake fallbacks when assets are missing."""
    with tempfile.TemporaryDirectory() as empty_tmp:
        engine = PressureIntelligenceEngine(data_dir=Path(empty_tmp))
        with pytest.raises(FileNotFoundError) as exc_info:
            engine.load_data()
        assert "Required Pressure Intelligence dataset missing" in str(exc_info.value)
        assert engine._is_loaded is False


@pytest.mark.unit
def test_uncapped_service_resolves_pressure_assets():
    """Confirms UncappedPressureIntelligenceService successfully resolves assets via resolve_asset_path."""
    service = UncappedPressureIntelligenceService()
    service.load_data()
    assert service._is_loaded is True
    assert service._batting_lb is not None and not service._batting_lb.empty
    assert service._bowling_lb is not None and not service._bowling_lb.empty
