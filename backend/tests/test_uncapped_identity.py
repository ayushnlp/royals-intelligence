"""
Royals Intelligence - Uncapped Player Identity & Eligibility Unit Tests
Validates name normalization, configurable age calculation, demographic conflict detection,
and competition-specific uncapped eligibility certification under verified and unverified rules.
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
    EligibilityRuleConfig,
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


@pytest.mark.unit
def test_player_name_normalization():
    """Verifies that player names with dots, whitespace, or initial quirks are standardized."""
    assert PlayerIdentityService.normalize_name("R. Parag") == "R Parag"
    assert PlayerIdentityService.normalize_name("   yashasvi   jaiswal  ") == "Yashasvi Jaiswal"
    assert PlayerIdentityService.normalize_name("A.B. de Villiers") == "Ab De Villiers"
    assert PlayerIdentityService.normalize_name("") == ""


@pytest.mark.unit
def test_age_calculation_from_reference_date():
    """Verifies age calculation is precise, requires an explicit cutoff, and never fabricates dates."""
    # 1. Valid verified DOB and confirmed reference date
    dob = date(2001, 11, 21)
    ref = date(2026, 11, 18)
    age = PlayerIdentityService.calculate_age(dob, ref)
    assert age is not None
    assert 24.8 <= age <= 25.1

    # 2. Missing DOB -> Must return None, never invent!
    assert PlayerIdentityService.calculate_age(None, ref) is None

    # 3. Missing / unconfirmed reference date -> Must return None (unresolved)!
    assert PlayerIdentityService.calculate_age(dob, None) is None

    # 4. Both None -> None
    assert PlayerIdentityService.calculate_age(None, None) is None

    # 5. Future DOB relative to reference date -> None (invalid)
    future_dob = date(2028, 1, 1)
    assert PlayerIdentityService.calculate_age(future_dob, ref) is None


@pytest.mark.unit
def test_conflict_detection():
    """Verifies detection of discrepancies between existing player and incoming data."""
    existing = PlayerModel(
        canonical_id="test_player",
        full_name="Test Batter",
        dob=date(2001, 5, 10),
        dob_source="BCCI Official Registry",
        dob_verified=True,
        batting_hand="Right",
        is_capped=False,
    )

    # 1. Clean data: No conflict
    clean_data = {"dob": date(2001, 5, 10), "batting_hand": "Right", "is_capped": False}
    assert len(PlayerIdentityService.detect_conflicts(existing, clean_data)) == 0

    # 2. DOB mismatch between sources
    bad_dob = {"dob": date(2002, 1, 15), "batting_hand": "Right"}
    conflicts = PlayerIdentityService.detect_conflicts(existing, bad_dob)
    assert len(conflicts) == 1
    assert "DOB mismatch" in conflicts[0]

    # 3. Invalid future DOB
    future_date = date(2030, 1, 1)
    bad_future = {"dob": future_date}
    conflicts = PlayerIdentityService.detect_conflicts(existing, bad_future)
    assert any("Invalid future DOB" in c for c in conflicts)

    # 4. Batting hand mismatch
    bad_hand = {"batting_hand": "Left"}
    conflicts = PlayerIdentityService.detect_conflicts(existing, bad_hand)
    assert len(conflicts) == 1
    assert "Batting hand mismatch" in conflicts[0]

    # 5. Cap status discrepancy
    bad_cap = {"is_capped": True}
    conflicts = PlayerIdentityService.detect_conflicts(existing, bad_cap)
    assert len(conflicts) == 1
    assert "Cap status discrepancy" in conflicts[0]


@pytest.mark.unit
def test_uncapped_eligibility_states_and_rules():
    """Verifies eligibility evaluation decoupling international cap facts from competition rules."""
    ref_date = date(2026, 12, 1)
    verified_rules = EligibilityRuleConfig(
        competition_id="ipl",
        season="2026",
        official_age_cutoff_date=ref_date,
        allow_five_year_retired_as_uncapped=True,
        require_verified_dob=True,
        is_rule_verified=True,
    )

    # 1. Verified uncapped player under confirmed rules
    p_valid = PlayerModel(
        canonical_id="p1",
        full_name="Valid Uncapped",
        dob=date(2002, 1, 1),
        dob_source="BCCI",
        dob_verified=True,
        is_capped=False,
    )
    status, reasons = PlayerIdentityService.evaluate_uncapped_eligibility(
        p_valid, rule_config=verified_rules, reference_date=ref_date
    )
    assert status == "CONFIRMED_UNCAPPED"

    # 2. Active Senior International -> Ineligible capped
    p_capped_active = PlayerModel(
        canonical_id="p2",
        full_name="Active International",
        dob=date(1995, 1, 1),
        dob_source="BCCI",
        dob_verified=True,
        is_capped=True,
        last_international_match_date=date(2024, 6, 15),  # Played in 2024 (< 5 yrs ago)
    )
    status, reasons = PlayerIdentityService.evaluate_uncapped_eligibility(
        p_capped_active, rule_config=verified_rules, reference_date=ref_date
    )
    assert status == "INELIGIBLE_CAPPED"
    assert "Active senior international representation" in reasons[0]

    # 3. 5-Year Retired International Exemption (IPL Rule 4.3)
    p_capped_retired_5yr = PlayerModel(
        canonical_id="p3",
        full_name="Retired Veteran",
        dob=date(1988, 7, 7),
        dob_source="BCCI",
        dob_verified=True,
        is_capped=True,
        last_international_match_date=date(2019, 7, 9),  # Last played July 2019 (> 5 yrs from Dec 2026)
    )
    status, reasons = PlayerIdentityService.evaluate_uncapped_eligibility(
        p_capped_retired_5yr, rule_config=verified_rules, reference_date=ref_date
    )
    assert status == "CONFIRMED_UNCAPPED"
    assert "5-year international inactivity clause" in reasons[0]

    # 4. Missing DOB -> PENDING_VERIFICATION (never fabricates eligibility)
    p_no_dob = PlayerModel(
        canonical_id="p4",
        full_name="Missing DOB Player",
        dob=None,
        is_capped=False,
    )
    status, reasons = PlayerIdentityService.evaluate_uncapped_eligibility(
        p_no_dob, rule_config=verified_rules, reference_date=ref_date
    )
    assert status == "PENDING_VERIFICATION"
    assert "Date of birth missing" in reasons[0]

    # 5. Unverified DOB provenance -> PENDING_VERIFICATION
    p_unverified_dob = PlayerModel(
        canonical_id="p5",
        full_name="Unverified Prospect",
        dob=date(2003, 3, 10),
        dob_source=None,
        dob_verified=False,
        is_capped=False,
    )
    status, reasons = PlayerIdentityService.evaluate_uncapped_eligibility(
        p_unverified_dob, rule_config=verified_rules, reference_date=ref_date
    )
    assert status == "PENDING_VERIFICATION"
    assert "Date of birth unverified" in reasons[0]

    # 6. Unverified Competition Regulations -> PENDING_VERIFICATION
    unverified_rules = EligibilityRuleConfig(
        competition_id="ipl",
        season="2027",
        is_rule_verified=False,
    )
    status, reasons = PlayerIdentityService.evaluate_uncapped_eligibility(
        p_valid, rule_config=unverified_rules
    )
    assert status == "PENDING_VERIFICATION"
    assert "remain pending formal release" in reasons[0]

    # 7. Flagged conflict takes precedence
    status, reasons = PlayerIdentityService.evaluate_uncapped_eligibility(
        p_valid, conflicts=["DOB mismatch detected across sources"], rule_config=verified_rules
    )
    assert status == "FLAGGED_CONFLICT"


@pytest.mark.unit
@pytest.mark.asyncio
async def test_resolve_or_create_player_workflow(async_test_session: AsyncSession):
    """Verifies idempotent player resolution, external identity creation, and profile building."""
    session = async_test_session
    ref_date = date(2026, 12, 1)
    rule_config = EligibilityRuleConfig(
        competition_id="ipl",
        season="2026",
        official_age_cutoff_date=ref_date,
        is_rule_verified=True,
    )

    # Ingest 1: New Player
    p1, prof1, created1, conflicts1 = await PlayerIdentityService.resolve_or_create_player(
        session=session,
        source_name="cricsheet",
        external_id="cric_priyansh_arya",
        name="Priyansh Arya",
        dob=date(2001, 1, 18),
        dob_source="Delhi Premier League",
        dob_verified=True,
        state_association="Delhi",
        primary_role="Top Order Batter",
        rule_config=rule_config,
        reference_date=ref_date,
    )
    assert created1 is True
    assert p1.full_name == "Priyansh Arya"
    assert prof1.eligibility_status == "CONFIRMED_UNCAPPED"
    assert prof1.calculated_age_at_cutoff is not None
    assert 25.0 <= prof1.calculated_age_at_cutoff <= 26.0
    assert len(conflicts1) == 0

    # Ingest 2: Re-ingest with same external identity -> idempotent match
    p2, prof2, created2, conflicts2 = await PlayerIdentityService.resolve_or_create_player(
        session=session,
        source_name="cricsheet",
        external_id="cric_priyansh_arya",
        name="Priyansh Arya",
        rule_config=rule_config,
        reference_date=ref_date,
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
        dob_source="BCCI",
        dob_verified=True,
        rule_config=rule_config,
        reference_date=ref_date,
    )
    assert created3 is False
    assert p3.id == p1.id  # Matched existing canonical player!
