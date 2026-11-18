"""
Royals Intelligence - Verification Tests for Official RR Squad & Retention
Validates the official IPL 2026 Full Squad and IPL 2027 Pre-Auction Retention/Trade/Release announcements.
"""

import json
from pathlib import Path
import pytest

from app.auction_intelligence.foundation.rr_squad_official_data import (
    RR_IPL_2026_FULL_SQUAD,
    RR_IPL_2027_RETAINED_PLAYERS,
    RR_IPL_2027_TRADED_IN_PLAYERS,
    RR_IPL_2027_TRADED_OUT_PLAYERS,
    RR_IPL_2027_RELEASED_PLAYERS,
    get_pre_auction_squad_summary,
)
from app.auction_intelligence.foundation.squad_baseline import RRSquadBaselineService
from app.auction_intelligence.retention.engine import RajasthanRoyalsRetentionEngine

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent


def test_official_2026_full_squad_breakdown():
    """Verifies the exact 27-player composition and leadership of the IPL 2026 RR squad."""
    squad = RR_IPL_2026_FULL_SQUAD
    assert squad["captain"] == "Riyan Parag"
    assert squad["total_squad_size"] == 27
    
    disciplines = squad["disciplines"]
    batters = disciplines["batters"]
    keepers = disciplines["wicket_keepers"]
    all_rounders = disciplines["all_rounders"]
    bowlers = disciplines["bowlers"]

    assert len(batters) == 5
    assert len(keepers) == 4
    assert len(all_rounders) == 6
    assert len(bowlers) == 12
    assert len(batters) + len(keepers) + len(all_rounders) + len(bowlers) == 27

    # Check Batters
    batter_names = [p["name"] for p in batters]
    expected_batters = ["Yashasvi Jaiswal", "Vaibhav Sooryavanshi", "Shimron Hetmyer", "Shubham Dubey", "Aman Rao Perala"]
    assert batter_names == expected_batters

    # Check Wicket-Keepers
    keeper_names = [p["name"] for p in keepers]
    expected_keepers = ["Dhruv Jurel", "Donovan Ferreira", "Lhuan-dre Pretorius", "Ravi Singh"]
    assert keeper_names == expected_keepers

    # Check All-Rounders
    ar_names = [p["name"] for p in all_rounders]
    expected_ar = ["Riyan Parag", "Ravindra Jadeja", "Sam Curran", "Dasun Shanaka", "Yudhvir Singh Charak", "Emanjot Singh Chahal"]
    assert ar_names == expected_ar

    # Check Bowlers
    bowler_names = [p["name"] for p in bowlers]
    expected_bowlers = [
        "Jofra Archer", "Ravi Bishnoi", "Sandeep Sharma", "Tushar Deshpande",
        "Nandre Burger", "Adam Milne", "Kwena Maphaka", "Kuldeep Sen",
        "Sushant Mishra", "Vignesh Puthur", "Brijesh Sharma", "Yash Raj Punja",
    ]
    assert bowler_names == expected_bowlers

    # Check Mid-season withdrawals and replacements
    withdrawals = [p for disc in disciplines.values() for p in disc if p.get("status") == "Withdrawn mid-season"]
    replacements = [p for disc in disciplines.values() for p in disc if p.get("status") == "Replacement"]
    assert len(withdrawals) == 2
    assert {p["name"] for p in withdrawals} == {"Sam Curran", "Ravi Singh"}
    assert len(replacements) == 2
    assert {p["name"] for p in replacements} == {"Dasun Shanaka", "Emanjot Singh Chahal"}


def test_official_2027_retention_list():
    """Verifies that exactly 17 players are retained ahead of the IPL 2027 auction."""
    retained = RR_IPL_2027_RETAINED_PLAYERS
    assert len(retained) == 17
    
    # Captain must be Riyan Parag
    assert retained[0]["name"] == "Riyan Parag"
    assert retained[0]["is_captain"] is True

    expected_retained_names = [
        "Riyan Parag", "Yashasvi Jaiswal", "Vaibhav Sooryavanshi", "Ravindra Jadeja",
        "Dhruv Jurel", "Jofra Archer", "Ravi Bishnoi", "Sandeep Sharma",
        "Nandre Burger", "Donovan Ferreira", "Lhuan-dre Pretorius", "Dasun Shanaka",
        "Shubham Dubey", "Aman Rao Perala", "Sushant Mishra", "Brijesh Sharma",
        "Yash Raj Punja",
    ]
    actual_retained_names = [p["name"] for p in retained]
    assert actual_retained_names == expected_retained_names


def test_official_2027_trades_and_releases():
    """Verifies traded-in (2), traded-out (1), and released (9) players."""
    traded_in = RR_IPL_2027_TRADED_IN_PLAYERS
    assert len(traded_in) == 2
    shami = next(p for p in traded_in if p["name"] == "Mohammed Shami")
    assert shami["traded_from"] == "Lucknow Super Giants"
    assert shami["trade_fee_inr_cr"] == 8.0

    siddharth = next(p for p in traded_in if p["name"] == "Manimaran Siddharth")
    assert siddharth["traded_from"] == "Lucknow Super Giants"
    assert siddharth["trade_fee_inr_cr"] == 0.75

    # Traded Out
    traded_out = RR_IPL_2027_TRADED_OUT_PLAYERS
    assert len(traded_out) == 1
    assert traded_out[0]["name"] == "Sam Curran"
    assert traded_out[0]["traded_to"] == "Lucknow Super Giants"
    assert traded_out[0]["trade_fee_inr_cr"] == 2.4

    # Released (9)
    released = RR_IPL_2027_RELEASED_PLAYERS
    assert len(released) == 9
    expected_released_names = [
        "Shimron Hetmyer", "Tushar Deshpande", "Adam Milne", "Kwena Maphaka",
        "Kuldeep Sen", "Yudhvir Singh Charak", "Vignesh Puthur", "Ravi Singh",
        "Emanjot Singh Chahal",
    ]
    actual_released_names = [p["name"] for p in released]
    assert actual_released_names == expected_released_names


def test_squad_reconciliation_total_balance():
    """Verifies that 17 Retained + 9 Released + 1 Traded Out == 27 original roster."""
    retained_count = len(RR_IPL_2027_RETAINED_PLAYERS)
    released_count = len(RR_IPL_2027_RELEASED_PLAYERS)
    traded_out_count = len(RR_IPL_2027_TRADED_OUT_PLAYERS)
    assert retained_count + released_count + traded_out_count == 27


def test_pre_auction_squad_summary_metrics():
    """Verifies current squad size (19), available slots (6), and overseas slots (3)."""
    summary = get_pre_auction_squad_summary()
    assert summary["total_current_squad_size"] == 19
    assert summary["retained_players_count"] == 17
    assert summary["traded_in_players_count"] == 2
    assert summary["traded_out_players_count"] == 1
    assert summary["released_players_count"] == 9
    assert summary["overseas_players_count"] == 5
    assert summary["indian_players_count"] == 14
    assert summary["available_auction_slots"] == 6
    assert summary["available_overseas_slots"] == 3


def test_processed_json_artifact_integrity():
    """Verifies that data/processed/auction_intelligence/rr_official_squad_retention_2027.json matches."""
    json_path = REPO_ROOT / "data" / "processed" / "auction_intelligence" / "rr_official_squad_retention_2027.json"
    assert json_path.exists()
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert "ipl_2026_full_squad" in data
    assert "ipl_2027_retention_and_release" in data
    assert data["ipl_2027_retention_and_release"]["total_current_squad_size"] == 19
