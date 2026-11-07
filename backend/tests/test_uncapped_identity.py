"""
Royals Intelligence - Uncapped Player Identity & Eligibility Unit Tests
Validates name normalization, age calculation provenance, conflict detection,
and strict uncapped eligibility rules.
"""

import pytest
import pytest_asyncio
from datetime import date
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.db.base import Base
import app.models
from app.models.core import PlayerModel
from app.services.identity.player_identity_service import (
    PlayerIdentityService,
    DEFAULT_COMPETITION_REFERENCE_DATE,
)


@pytest_asyncio.fixture
async def async_test_session():
    """In-memory SQLite async engine and session for isolation and fast execution."""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async_session = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


def test_player_name_normalization():
    """Verifies that player names with dots, whitespace, or initial quirks are standardized."""
    assert PlayerIdentityService.normalize_name("R. Parag") == "R Parag"
    assert PlayerIdentityService.normalize_name("   yashasvi   jaiswal  ") == "Yashasvi Jaiswal"
    assert PlayerIdentityService.normalize_name("A.B. de Villiers") == "Ab De Villiers"
    assert PlayerIdentityService.normalize_name("") == ""


def test_age_calculation_from_reference_date():
    """Verifies age calculation is precise and never invents dates of birth."""
    # Born 2001-11-21, reference date 2026-11-18 -> 24.99 years -> 25.0
    dob = date(2001, 11, 21)
    ref = date(2026, 11, 18)
    age = PlayerIdentityService.calculate_age(dob, ref)
    assert age is not None
    assert 24.8 <= age <= 25.1

    # Missing DOB -> Must return None, never invent!
    assert PlayerIdentityService.calculate_age(None, ref) is None

    # Future DOB -> 0.0
    future_dob = date(2028, 1, 1)
    assert PlayerIdentityService.calculate_age(future_dob, ref) == 0.0


def test_conflict_detection():
    """Verifies detection of discrepancies between existing player and incoming data."""
    existing = PlayerModel(
        canonical_id="test_player",
        full_name="Test Batter",
        dob=date(2001, 5, 10),
        dob_source="BCCI",
        batting_hand="Right",
        is_capped=False,
    )

    # 1. No conflict
    clean_data = {"dob": date(2001, 5, 10), "batting_hand": "Right", "is_capped": False}
    assert len(PlayerIdentityService.detect_conflicts(existing, clean_data)) == 0

    # 2. DOB mismatch
    bad_dob = {"dob": date(2002, 1, 15), "batting_hand": "Right"}
    conflicts = PlayerIdentityService.detect_conflicts(existing, bad_dob)
    assert len(conflicts) == 1
    assert "DOB mismatch" in conflicts[0]

    # 3. Batting hand mismatch
    bad_hand = {"batting_hand": "Left"}
    conflicts = PlayerIdentityService.detect_conflicts(existing, bad_hand)
    assert len(conflicts) == 1
    assert "Batting hand mismatch" in conflicts[0]

    # 4. Cap status discrepancy
    bad_cap = {"is_capped": True}
    conflicts = PlayerIdentityService.detect_conflicts(existing, bad_cap)
    assert len(conflicts) == 1
    assert "Cap status discrepancy" in conflicts[0]


def test_uncapped_eligibility_states():
    """Verifies all 5 eligibility verification states."""
    ref = DEFAULT_COMPETITION_REFERENCE_DATE

    # 1. Confirmed uncapped
    p_valid = PlayerModel(canonical_id="p1", full_name="Valid Uncapped", dob=date(2002, 1, 1), is_capped=False)
    status, reasons = PlayerIdentityService.evaluate_uncapped_eligibility(p_valid, reference_date=ref)
    assert status == "CONFIRMED_UNCAPPED"

    # 2. Suspected capped (international appearance)
    p_capped = PlayerModel(canonical_id="p2", full_name="Capped Star", dob=date(1995, 1, 1), is_capped=True)
    status, reasons = PlayerIdentityService.evaluate_uncapped_eligibility(p_capped, reference_date=ref)
    assert status == "SUSPECTED_CAPPED"

    # 3. Missing DOB -> Pending verification
    p_no_dob = PlayerModel(canonical_id="p3", full_name="Missing DOB", dob=None, is_capped=False)
    status, reasons = PlayerIdentityService.evaluate_uncapped_eligibility(p_no_dob, reference_date=ref)
    assert status == "PENDING_VERIFICATION"

    # 4. Ineligible overage (e.g. U-23 tournament cutoff)
    p_overage = PlayerModel(canonical_id="p4", full_name="Veteran", dob=date(1995, 1, 1), is_capped=False)
    status, reasons = PlayerIdentityService.evaluate_uncapped_eligibility(p_overage, max_age_cutoff=23.0, reference_date=ref)
    assert status == "INELIGIBLE_OVERAGE"

    # 5. Flagged conflict
    conflicts = ["DOB mismatch between BCCI and Cricsheet"]
    status, reasons = PlayerIdentityService.evaluate_uncapped_eligibility(p_valid, conflicts=conflicts, reference_date=ref)
    assert status == "FLAGGED_CONFLICT"


@pytest.mark.asyncio
async def test_resolve_or_create_player_workflow(async_test_session: AsyncSession):
    """Verifies idempotent player resolution, external identity creation, and profile building."""
    session = async_test_session

    # Ingest 1: New Player
    p1, prof1, created1, conflicts1 = await PlayerIdentityService.resolve_or_create_player(
        session=session,
        source_name="cricsheet",
        external_id="cric_priyansh_arya",
        name="Priyansh Arya",
        dob=date(2001, 1, 18),
        dob_source="Delhi Premier League",
        state_association="Delhi",
        primary_role="Top Order Batter",
    )
    assert created1 is True
    assert p1.full_name == "Priyansh Arya"
    assert prof1.eligibility_status == "CONFIRMED_UNCAPPED"
    assert prof1.calculated_age_at_cutoff is not None
    assert len(conflicts1) == 0

    # Ingest 2: Re-ingest with same external identity -> idempotent match
    p2, prof2, created2, conflicts2 = await PlayerIdentityService.resolve_or_create_player(
        session=session,
        source_name="cricsheet",
        external_id="cric_priyansh_arya",
        name="Priyansh Arya",
    )
    assert created2 is False
    assert p2.id == p1.id
    assert len(conflicts2) == 0

    # Ingest 3: Ingest second source for same player with new source ID but same name & DOB
    p3, prof3, created3, conflicts3 = await PlayerIdentityService.resolve_or_create_player(
        session=session,
        source_name="bcci",
        external_id="BCCI_DPL_004",
        name="Priyansh Arya",
        dob=date(2001, 1, 18),
    )
    assert created3 is False
    assert p3.id == p1.id  # Matched existing!
