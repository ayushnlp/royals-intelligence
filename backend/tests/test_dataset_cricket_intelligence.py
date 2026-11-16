"""
Unit & Integration Tests for Dataset Cricket Intelligence Engine
Stage 5 Core Tactical Analytics Service Verification
"""

import pytest
from pathlib import Path
from app.analytics.dataset_cricket_intelligence import (
    DatasetCricketIntelligenceEngine,
    TacticalPhaseSplit,
    TacticalStrokeProfile,
    DeliveryStyleProfile,
    HandednessSplit,
    HeadToHeadMatchupProfile,
)


@pytest.fixture(scope="module")
def intelligence_engine():
    """Initializes and loads the dataset engine once for the test module."""
    engine = DatasetCricketIntelligenceEngine()
    engine.load_data()
    return engine


def test_engine_initialization_and_summary(intelligence_engine):
    """Verifies that the engine loads the official data pack and reports exact aggregations."""
    summary = intelligence_engine.get_dataset_summary()
    assert summary["total_deliveries"] == 200999
    assert summary["legal_deliveries"] == 192709
    assert summary["total_matches_with_deliveries"] == 867
    assert summary["total_unique_strikers"] == 888
    assert summary["total_unique_bowlers"] == 647
    assert summary["total_runs_off_bat"] == 269550
    assert summary["total_wickets_fallen"] == 10881
    assert summary["total_bowler_wickets"] == 10272
    assert summary["overall_run_rate_per_6_balls"] > 7.0
    assert summary["valid_radar_speed_records"] > 120000


def test_phase_splits_overall(intelligence_engine):
    """Verifies tournament-wide phase splits (Powerplay, Middle, Death)."""
    splits = intelligence_engine.get_phase_splits()
    assert "Powerplay" in splits
    assert "Middle" in splits
    assert "Death" in splits

    pp = splits["Powerplay"]
    mid = splits["Middle"]
    death = splits["Death"]

    # Verify balls sum up to total deliveries
    assert pp.total_balls + mid.total_balls + death.total_balls == 200999
    # Powerplay has higher dot percentage than death
    assert pp.dot_ball_percentage > death.dot_ball_percentage
    # Death has higher run rate than Powerplay
    assert death.economy_rate > pp.economy_rate


def test_player_phase_splits(intelligence_engine):
    """Verifies phase splits for specific players (Jos Buttler batting, Yuzvendra Chahal bowling)."""
    # Jos Buttler (player_id 813)
    buttler_splits = intelligence_engine.get_phase_splits(striker_id=813)
    assert buttler_splits["Powerplay"].total_balls > 500
    assert buttler_splits["Powerplay"].runs > 800
    assert buttler_splits["Powerplay"].strike_rate > 130.0

    # Yuzvendra Chahal (player_id 1612)
    chahal_splits = intelligence_engine.get_phase_splits(bowler_id=1612)
    assert chahal_splits["Middle"].total_balls > 1000
    assert chahal_splits["Middle"].wickets > 70
    assert chahal_splits["Middle"].economy_rate < 9.5


def test_handedness_matrix(intelligence_engine):
    """Verifies 4-way stance/bowling cross-split."""
    matrix = intelligence_engine.get_handedness_matrix()
    assert len(matrix) == 4

    combos = {(m.batting_type, m.pace_or_spin) for m in matrix}
    assert ("RHB", "Pace") in combos
    assert ("RHB", "Spin") in combos
    assert ("LHB", "Pace") in combos
    assert ("LHB", "Spin") in combos

    for split in matrix:
        assert split.balls_faced > 20000
        assert split.strike_rate > 110.0
        assert split.economy_rate > 6.0
        assert 0.0 <= split.dot_pct <= 100.0


def test_tactical_strokes(intelligence_engine):
    """Verifies shot stroke classification and risk profiling."""
    strokes = intelligence_engine.get_top_strokes(min_balls=1000)
    assert len(strokes) >= 10

    stroke_names = [s.stroke for s in strokes]
    assert "Pull shot" in stroke_names
    assert "Cover Drive" in stroke_names
    assert "Worked" in stroke_names

    # Pull shot should have higher boundary percentage than Worked
    pull = next(s for s in strokes if s.stroke == "Pull shot")
    worked = next(s for s in strokes if s.stroke == "Worked")
    assert pull.boundary_pct > worked.boundary_pct
    assert worked.dismissal_rate_pct < 4.0


def test_delivery_styles(intelligence_engine):
    """Verifies bowling variation styles."""
    styles = intelligence_engine.get_top_delivery_styles(min_balls=500)
    assert len(styles) >= 10

    style_names = [s.delivery_style for s in styles]
    assert "Seamed In" in style_names
    assert "Leg Break" in style_names


def test_top_death_performers(intelligence_engine):
    """Verifies death overs ranking algorithms."""
    death_batters = intelligence_engine.get_top_death_batters(min_balls=100, top_n=5)
    assert len(death_batters) == 5
    # Suryakumar Yadav should be #1 with high strike rate
    assert death_batters[0]["striker_name"] == "Suryakumar Yadav"
    assert death_batters[0]["strike_rate"] > 200.0

    death_bowlers = intelligence_engine.get_top_death_bowlers(min_balls=150, top_n=5)
    assert len(death_bowlers) == 5
    # Sunil Narine or Jasprit Bumrah should be near top with low economy
    bowler_names = [b["bowler_name"] for b in death_bowlers]
    assert "Sunil Narine" in bowler_names or "Jasprit Bumrah" in bowler_names


def test_head_to_head_micro_battles(intelligence_engine):
    """Verifies direct head-to-head matchup calculations."""
    # Virat Kohli (47) vs Rashid Khan (4722)
    h2h = intelligence_engine.get_head_to_head(striker_id=47, bowler_id=4722)
    assert h2h is not None
    assert h2h.striker_name == "Virat Kohli"
    assert h2h.bowler_name == "Rashid Khan"
    assert h2h.balls_faced == 76
    assert h2h.runs_scored >= 100
    assert h2h.strike_rate >= 140.0

    # Non-existent pairing
    empty_h2h = intelligence_engine.get_head_to_head(striker_id=999999, bowler_id=888888)
    assert empty_h2h is None


def test_rajasthan_royals_squad_intelligence(intelligence_engine):
    """Verifies Rajasthan Royals squad intelligence dossier generation."""
    rr_dossiers = intelligence_engine.get_rajasthan_royals_squad_intelligence()
    assert len(rr_dossiers) >= 5

    names = [d["player_name"] for d in rr_dossiers]
    assert "Jos Buttler" in names
    assert "Sanju Samson" in names
    assert "Yashasvi Jaiswal" in names
    assert "Yuzvendra Chahal" in names
    assert "Trent Boult" in names

    for d in rr_dossiers:
        assert "phase_profiles" in d
        assert "Powerplay" in d["phase_profiles"]
        assert "Middle" in d["phase_profiles"]
        assert "Death" in d["phase_profiles"]
