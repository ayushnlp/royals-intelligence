"""
Royals Intelligence - Cricket Data Normalization Layer
Normalizes team aliases, venue names, delivery phase tags, and player registry records.
"""

from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, date, timezone
from app.schemas.contracts.cricket_contracts import (
    BallByBallDelivery,
    DeliveryExtras,
    DismissalDetails,
    SourceReference,
)
from app.core.logging import logger

TEAM_ALIASES: Dict[str, str] = {
    # Rajasthan Royals
    "rajasthan royals": "RR",
    "rr": "RR",
    # Chennai Super Kings
    "chennai super kings": "CSK",
    "csk": "CSK",
    # Mumbai Indians
    "mumbai indians": "MI",
    "mi": "MI",
    # Kolkata Knight Riders
    "kolkata knight riders": "KKR",
    "kkr": "KKR",
    # Royal Challengers Bengaluru
    "royal challengers bengaluru": "RCB",
    "royal challengers bangalore": "RCB",
    "rcb": "RCB",
    # Sunrisers Hyderabad
    "sunrisers hyderabad": "SRH",
    "srh": "SRH",
    # Delhi Capitals
    "delhi capitals": "DC",
    "delhi daredevils": "DC",
    "dc": "DC",
    # Punjab Kings
    "punjab kings": "PBKS",
    "kings xi punjab": "PBKS",
    "pbks": "PBKS",
    "kxip": "PBKS",
    # Gujarat Titans
    "gujarat titans": "GT",
    "gt": "GT",
    # Lucknow Super Giants
    "lucknow super giants": "LSG",
    "lsg": "LSG",
    # Historical IPL Franchises
    "deccan chargers": "DC_HIST",
    "rising pune supergiant": "RPS",
    "rising pune supergiants": "RPS",
    "gujarat lions": "GL",
    "pune warriors": "PWI",
    "kochi tuskers kerala": "KTK",
}

VENUE_ALIASES: Dict[str, str] = {
    "sawai mansingh stadium": "SMS_JAIPUR",
    "sawai mansingh stadium, jaipur": "SMS_JAIPUR",
    "barsapara cricket stadium": "BARS_GUWAHATI",
    "barsapara cricket stadium, guwahati": "BARS_GUWAHATI",
    "aca stadium, barsapara": "BARS_GUWAHATI",
    "wankhede stadium": "WANKHEDE_MUMBAI",
    "wankhede stadium, mumbai": "WANKHEDE_MUMBAI",
    "ma chidambaram stadium": "CHIDAMBARAM_CHENNAI",
    "ma chidambaram stadium, chepauk": "CHIDAMBARAM_CHENNAI",
    "ma chidambaram stadium, chepauk, chennai": "CHIDAMBARAM_CHENNAI",
    "eden gardens": "EDEN_KOLKATA",
    "eden gardens, kolkata": "EDEN_KOLKATA",
    "m chinnaswamy stadium": "CHINNASWAMY_BLR",
    "m. chinnaswamy stadium": "CHINNASWAMY_BLR",
    "m chinnaswamy stadium, bengaluru": "CHINNASWAMY_BLR",
    "narendra modi stadium": "MODI_AHMEDABAD",
    "narendra modi stadium, ahmedabad": "MODI_AHMEDABAD",
    "sardar patel stadium, motera": "MODI_AHMEDABAD",
    "arun jaitley stadium": "JAITLEY_DELHI",
    "arun jaitley stadium, delhi": "JAITLEY_DELHI",
    "feroz shah kotla": "JAITLEY_DELHI",
    "rajiv gandhi international stadium": "RGIC_HYDERABAD",
    "rajiv gandhi international stadium, uppal": "RGIC_HYDERABAD",
    "maharaja yadavindra singh international cricket stadium": "MULLANPUR_PBKS",
    "himachal pradesh cricket association stadium": "HPCA_DHARAMSHALA",
    "dharamsala": "HPCA_DHARAMSHALA",
    "bharat ratna shri atal bihari vajpayee ekana cricket stadium": "EKANA_LUCKNOW",
}


class CricketDataNormalizer:
    """Normalizes raw cricket entities into consistent codes, categories, and tabular formats."""

    @staticmethod
    def normalize_team(team_name: str) -> str:
        """Returns standard team code (e.g. 'RR') or original uppercase name if unregistered."""
        clean = team_name.strip().lower()
        return TEAM_ALIASES.get(clean, team_name.strip())

    @staticmethod
    def normalize_venue(venue_name: str) -> str:
        """Returns canonical venue code (e.g. 'SMS_JAIPUR') or cleaned venue string."""
        clean = venue_name.strip().lower()
        return VENUE_ALIASES.get(clean, venue_name.strip())

    @staticmethod
    def get_phase(over_number: int) -> str:
        """
        Determines the T20 match phase:
        - 0 to 5 (overs 1-6): Powerplay
        - 6 to 14 (overs 7-15): Middle
        - 15 to 19 (overs 16-20): Death
        """
        if over_number <= 5:
            return "Powerplay"
        elif over_number <= 14:
            return "Middle"
        return "Death"

    @classmethod
    def flatten_match_deliveries(
        cls,
        raw_match: Dict[str, Any],
        match_id: str,
        source_ref: SourceReference
    ) -> List[Dict[str, Any]]:
        """
        Transforms nested Cricsheet JSON innings/overs structure into a flat list of normalized deliveries.
        """
        info = raw_match.get("info", {})
        innings_list = raw_match.get("innings", [])
        season = str(info.get("season", "unknown"))
        dates = info.get("dates", [])
        match_date_str = str(dates[0]) if dates else datetime.now(timezone.utc).strftime("%Y-%m-%d")
        venue_str = str(info.get("venue", "Unknown Venue"))
        venue_code = cls.normalize_venue(venue_str)
        teams = info.get("teams", ["Team A", "Team B"])
        team1 = cls.normalize_team(teams[0]) if len(teams) > 0 else "UNK1"
        team2 = cls.normalize_team(teams[1]) if len(teams) > 1 else "UNK2"

        flattened_deliveries: List[Dict[str, Any]] = []

        for innings_idx, innings in enumerate(innings_list, start=1):
            batting_team_raw = innings.get("team", "")
            batting_team = cls.normalize_team(batting_team_raw)
            bowling_team = team2 if batting_team == team1 else team1

            overs = innings.get("overs", [])
            for over in overs:
                over_num = int(over.get("over", 0))
                phase = cls.get_phase(over_num)

                deliveries = over.get("deliveries", [])
                for ball_idx, delivery in enumerate(deliveries, start=1):
                    striker = delivery.get("batter", "")
                    non_striker = delivery.get("non_striker", "")
                    bowler = delivery.get("bowler", "")
                    runs_dict = delivery.get("runs", {})
                    batter_runs = int(runs_dict.get("batter", 0))
                    extras_runs = int(runs_dict.get("extras", 0))
                    total_runs = int(runs_dict.get("total", batter_runs + extras_runs))

                    extras_dict = delivery.get("extras", {})
                    wides = int(extras_dict.get("wides", 0))
                    noballs = int(extras_dict.get("noballs", 0))
                    legbyes = int(extras_dict.get("legbyes", 0))
                    byes = int(extras_dict.get("byes", 0))
                    penalty = int(extras_dict.get("penalty", 0))

                    is_legal = (wides == 0 and noballs == 0)
                    is_boundary_four = (batter_runs == 4)
                    is_boundary_six = (batter_runs == 6)
                    is_dot_ball = (total_runs == 0 and is_legal)

                    is_wicket = "wickets" in delivery and len(delivery["wickets"]) > 0
                    dismissal_kind = None
                    player_dismissed = None
                    fielders_str = ""

                    if is_wicket:
                        w = delivery["wickets"][0]
                        dismissal_kind = w.get("kind")
                        player_dismissed = w.get("player_out")
                        fielders = w.get("fielders", [])
                        fielders_str = ", ".join(f.get("name", "") if isinstance(f, dict) else str(f) for f in fielders)

                    # Precise over display: e.g. 0.1 for first ball of over 0
                    over_display = round(over_num + (ball_idx / 10.0), 1)

                    flat_row = {
                        "match_id": match_id,
                        "season": season,
                        "match_date": match_date_str,
                        "venue_code": venue_code,
                        "venue_name": venue_str,
                        "innings_number": innings_idx,
                        "batting_team": batting_team,
                        "bowling_team": bowling_team,
                        "over_number": over_num,
                        "ball_in_over": ball_idx,
                        "over_display": over_display,
                        "phase": phase,
                        "striker": striker,
                        "non_striker": non_striker,
                        "bowler": bowler,
                        "batter_runs": batter_runs,
                        "extra_runs": extras_runs,
                        "total_runs": total_runs,
                        "is_legal": is_legal,
                        "is_dot_ball": is_dot_ball,
                        "is_boundary_four": is_boundary_four,
                        "is_boundary_six": is_boundary_six,
                        "wides": wides,
                        "noballs": noballs,
                        "legbyes": legbyes,
                        "byes": byes,
                        "is_wicket": is_wicket,
                        "dismissal_kind": dismissal_kind,
                        "player_dismissed": player_dismissed,
                        "fielders": fielders_str,
                        # Telemetry fields: strictly None unless source explicitly provides them
                        "release_speed_kph": None,
                        "delivery_classification": None,
                        "source_id": source_ref.source_id,
                    }
                    flattened_deliveries.append(flat_row)

        return flattened_deliveries

    @classmethod
    def extract_match_summary(
        cls,
        raw_match: Dict[str, Any],
        match_id: str,
        source_ref: SourceReference
    ) -> Dict[str, Any]:
        """Extracts normalized high-level match metadata."""
        info = raw_match.get("info", {})
        season = str(info.get("season", "unknown"))
        dates = info.get("dates", [])
        match_date = str(dates[0]) if dates else datetime.now(timezone.utc).strftime("%Y-%m-%d")
        venue_str = str(info.get("venue", "Unknown Venue"))
        venue_code = cls.normalize_venue(venue_str)
        teams = info.get("teams", ["Team A", "Team B"])
        team1 = cls.normalize_team(teams[0]) if len(teams) > 0 else "UNK1"
        team2 = cls.normalize_team(teams[1]) if len(teams) > 1 else "UNK2"

        toss = info.get("toss", {})
        toss_winner = cls.normalize_team(toss.get("winner", ""))
        toss_decision = str(toss.get("decision", "unknown"))

        outcome = info.get("outcome", {})
        winner = cls.normalize_team(outcome.get("winner", "")) if "winner" in outcome else None
        by_dict = outcome.get("by", {})
        win_by_runs = by_dict.get("runs")
        win_by_wickets = by_dict.get("wickets")
        pom = info.get("player_of_match", [])
        player_of_match = str(pom[0]) if pom else None

        return {
            "match_id": match_id,
            "competition_id": "ipl" if "ipl" in season.lower() or "ipl" in str(info.get("event", {}).get("name", "")).lower() else "cricket_t20",
            "season": season,
            "match_date": match_date,
            "venue_code": venue_code,
            "venue_name": venue_str,
            "team1": team1,
            "team2": team2,
            "toss_winner": toss_winner,
            "toss_decision": toss_decision,
            "winner": winner,
            "win_by_runs": win_by_runs,
            "win_by_wickets": win_by_wickets,
            "player_of_match": player_of_match,
            "source_id": source_ref.source_id,
            "ingested_at": source_ref.ingested_at.isoformat(),
        }
