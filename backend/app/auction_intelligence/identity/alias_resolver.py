"""
Royals Intelligence - RR Auction & Retention Intelligence
Alias Resolver & Canonical Name Normalization Service.
Stage: AUCTION-01
"""

import re
from typing import Optional, Dict, Tuple


# Explicit mapping from third-party / informal name strings to (canonical_player_id, canonical_name)
KNOWN_NAME_ALIASES: Dict[str, Tuple[int, str]] = {
    "pat cummins": (1758, "Patrick Cummins"),
    "ms dhoni": (8, "Mahendra Singh Dhoni"),
    "kl rahul": (953, "Lokesh Rahul"),
    "will jacks": (6272, "William Jacks"),
    "shahrukh khan": (3782, "M Shahrukh Khan"),
    "raj angad bawa": (26834, "Raj Bawa"),
    "lhuan-dre pretorius": (43798, "Lhuan Pretorius"),
    "harnoor singh": (26911, "Harnoor Pannu"),
    "mohammad izhar": (71311, "Mohd Izhar"),
    "tejasvi singh dahiya": (58135, "Tejasvi Dahiya"),
    "smaran ravichandran": (33067, "Ravichandran Smaran"),
    "onkar tarmale": (66513, "Omkar Tarmale"),
    "yash raj punja": (41503, "Yash Punja"),
    "aman rao": (47523, "Aman Rao Perala"),
    "nitish kumar reddy": (8221, "Nitish Reddy"),
    "tilak varma": (7897, "Namboori Tilak Varma"),
    "vijaykumar vyshak": (4487, "Vyshak Kumar"),
    "aman hakim khan": (20894, "Aman Khan"),
    "m siddharth": (6237, "Manimaran Siddharth"),
    "prithvi raj yarra": (6351, "Yarra Prithviraj"),
    "pravin dubey": (2790, "Praveen Dubey"),
    "zak foulkes": (29066, "Zakary Foulkes"),
    "nishant sindhu": (26830, "Nishant Kumar Sindhu"),
}

# Explicit entity disambiguation for duplicate names sharing identical strings
KNOWN_DISAMBIGUATION_MAP: Dict[Tuple[str, str], int] = {
    # (Player Name, Team / Country) -> canonical_id
    ("abdul samad", "sunrisers hyderabad"): 7446,
    ("abdul samad", "lucknow super giants"): 7446,
    ("abdul samad", "pakistan"): 6922,
    ("abdul samad", "pakistan a"): 6922,
    ("rashid khan", "gujarat titans"): 4722,
    ("rashid khan", "afghanistan"): 4722,
    ("rashid khan", "nepal"): 20172,
    ("haider ali", "pakistan"): 7338,
    ("haider ali", "pakistan a"): 7338,
    ("haider ali", "united arab emirates"): 28756,
}


class AliasResolver:
    """Robust resolver for cricket player names, aliases, and identity disambiguation."""

    @staticmethod
    def clean_string(raw_name: str) -> str:
        """Normalizes name: removes periods, hyphens to spaces, collapses whitespace, lowers."""
        if not raw_name:
            return ""
        s = raw_name.lower().replace(".", "").replace("-", " ")
        s = re.sub(r"\s+", " ", s).strip()
        return s

    @classmethod
    def resolve_alias(
        cls,
        raw_name: str,
        team_context: Optional[str] = None
    ) -> Optional[Tuple[int, str]]:
        """
        Resolves a raw name string to its (canonical_id, canonical_name).
        Checks:
        1. Contextual disambiguation (if name is shared by multiple people).
        2. Exact known alias dictionary.
        3. Cleaned string alias dictionary.
        """
        if not raw_name:
            return None
            
        cleaned = cls.clean_string(raw_name)
        raw_lower = raw_name.lower().strip()

        # 1. Contextual Disambiguation
        if team_context:
            t_clean = team_context.lower().strip()
            if (raw_lower, t_clean) in KNOWN_DISAMBIGUATION_MAP:
                cid = KNOWN_DISAMBIGUATION_MAP[(raw_lower, t_clean)]
                return (cid, raw_name)
            if (cleaned, t_clean) in KNOWN_DISAMBIGUATION_MAP:
                cid = KNOWN_DISAMBIGUATION_MAP[(cleaned, t_clean)]
                return (cid, raw_name)

        # 2. Direct Alias Map Check
        if raw_lower in KNOWN_NAME_ALIASES:
            return KNOWN_NAME_ALIASES[raw_lower]

        # 3. Cleaned Match
        for alias_key, val in KNOWN_NAME_ALIASES.items():
            if cls.clean_string(alias_key) == cleaned:
                return val

        return None
