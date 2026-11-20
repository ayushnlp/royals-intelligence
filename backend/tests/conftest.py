"""
Royals Intelligence - Pytest Global Fixtures
"""

import sys
from pathlib import Path

# Ensure backend root is in sys.path
backend_dir = Path(__file__).resolve().parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as test_client:
        yield test_client


def pytest_collection_modifyitems(session, config, items):
    """
    Enforces the safe three-group test architecture:
    Every collected test must belong to EXACTLY ONE primary execution group:
      - Group A: 'unit' OR 'environment'
      - Group B: 'data_dependent'
      - Group C: 'data_integrity'
    Fails collection immediately if any test is unclassified or multiply classified.
    """
    primary_markers = {
        "unit": "A",
        "environment": "A",
        "data_dependent": "B",
        "data_integrity": "C",
    }
    unclassified = []
    multiply_classified = []

    for item in items:
        item_groups = {primary_markers[m.name] for m in item.iter_markers() if m.name in primary_markers}
        if len(item_groups) == 0:
            unclassified.append(item.nodeid)
        elif len(item_groups) > 1:
            matching = [m.name for m in item.iter_markers() if m.name in primary_markers]
            multiply_classified.append((item.nodeid, matching))

    if unclassified or multiply_classified:
        error_msgs = []
        if unclassified:
            error_msgs.append(
                f"UNCLASSIFIED TESTS DETECTED ({len(unclassified)} tests have no primary execution group marker):\n  "
                + "\n  ".join(unclassified[:10])
                + (f"\n  ... and {len(unclassified) - 10} more" if len(unclassified) > 10 else "")
            )
        if multiply_classified:
            error_msgs.append(
                f"MULTIPLY CLASSIFIED TESTS DETECTED ({len(multiply_classified)} tests belong to multiple groups):\n  "
                + "\n  ".join(f"{nid} -> {m}" for nid, m in multiply_classified[:10])
            )
        pytest.fail("\n\n".join(error_msgs), pytrace=False)
