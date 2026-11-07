"""
Royals Intelligence - RR Proprietary Data Pack Unit Tests
Validates dynamic schema discovery, configurable column mapping, proprietary ingestion,
and strict confidential data masking boundaries.
"""

import pytest
import pytest_asyncio
from datetime import date
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.db.base import Base
import app.models
from app.services.proprietary.rr_data_pack_service import (
    RRDataPackService,
    ColumnMappingConfig,
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


def test_schema_discovery():
    """Tests analyzing sample rows to discover columns, detect types, and suggest mappings."""
    sample_rows = [
        {
            "player_name": "Ashutosh Sharma",
            "dob": "1998-09-15",
            "state_association": "Madhya Pradesh",
            "primary_role": "Middle Order Batter",
            "technical_rating": 8.5,
            "confidential_notes": "Very fast bat speed.",
            "is_rr_trialist": True,
        },
        {
            "player_name": "Vipraj Nigam",
            "dob": "2000-05-12",
            "state_association": "Uttar Pradesh",
            "primary_role": "All-Rounder",
            "technical_rating": 7.0,
            "confidential_notes": "Good wrist-spin control.",
            "is_rr_trialist": False,
        }
    ]

    result = RRDataPackService.discover_schema(sample_rows)
    assert len(result.detected_columns) == 7
    assert result.sample_row_count == 2
    assert result.recommended_mapping.name_col == "player_name"
    assert result.recommended_mapping.dob_col == "dob"
    assert result.recommended_mapping.technical_rating_col == "technical_rating"
    assert result.column_type_hints["technical_rating"] == "float"


def test_confidential_data_masking():
    """Verifies confidential scouting notes and scout identifiers are stripped for unauthorized roles."""
    sample_eval = {
        "id": "eval_01",
        "scout_identifier": "RR_SCOUT_DOMESTIC_NORTH",
        "confidential_notes": "Target for IPL 2027 auction finisher slot. Max bid INR 7.5 Cr.",
        "proprietary_notes": "Agent contact verified.",
        "strengths_summary": "High power hitting index.",
        "scouting_tier": "TARGET_A_LIST",
        "data_classification": "RR_PROPRIETARY_CONFIDENTIAL",
    }

    # 1. Public user -> Confidential fields masked
    public_masked = RRDataPackService.mask_confidential_data(sample_eval, user_role="public")
    assert "[RESTRICTED" in public_masked["confidential_notes"]
    assert "[RESTRICTED" in public_masked["proprietary_notes"]
    assert "[ANONYMIZED" in public_masked["scout_identifier"]
    assert public_masked["scouting_tier"] == "INTERNAL"

    # 2. RR Scout Admin -> Full access preserved
    admin_view = RRDataPackService.mask_confidential_data(sample_eval, user_role="rr_scout_admin")
    assert admin_view["confidential_notes"] == "Target for IPL 2027 auction finisher slot. Max bid INR 7.5 Cr."
    assert admin_view["scout_identifier"] == "RR_SCOUT_DOMESTIC_NORTH"
    assert admin_view["scouting_tier"] == "TARGET_A_LIST"


@pytest.mark.asyncio
async def test_proprietary_pack_ingestion(async_test_session: AsyncSession):
    """Verifies end-to-end ingestion of sample proprietary data pack records."""
    session = async_test_session

    records = [
        {
            "name": "Shashank Singh",
            "birth_date": "1991-11-21",
            "state": "Chhattisgarh",
            "role": "Finisher",
            "tech_score": 8.5,
            "secret_notes": "Prioritize in auction.",
            "trialist": "true",
        },
        {
            "name": "Unverified Prospect",
            "birth_date": None,  # Missing DOB!
            "state": "Assam",
            "role": "Pace Bowler",
            "tech_score": 7.0,
            "secret_notes": "Trial pending.",
            "trialist": "false",
        }
    ]

    mapping = ColumnMappingConfig(
        name_col="name",
        dob_col="birth_date",
        state_association_col="state",
        primary_role_col="role",
        technical_rating_col="tech_score",
        confidential_notes_col="secret_notes",
        is_trialist_col="trialist",
    )

    summary = await RRDataPackService.ingest_proprietary_pack(
        session=session,
        records=records,
        mapping=mapping,
        dataset_key="rr_pack_test_nov8",
    )

    assert summary.total_rows_parsed == 2
    assert summary.players_created == 2
    assert summary.missing_dob_count == 1
    assert summary.evaluations_recorded == 2
    assert len(summary.missing_field_reports) == 1
    assert summary.missing_field_reports[0]["player_name"] == "Unverified Prospect"
