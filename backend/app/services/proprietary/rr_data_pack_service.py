"""
Royals Intelligence - Rajasthan Royals Proprietary Data Pack Compatibility Engine
Handles dynamic schema discovery, configurable column mapping, player resolution,
conflict/missing-field auditing, and strict security isolation for confidential scout data.
"""

import uuid
from datetime import date, datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.scouting import (
    UncappedPlayerProfileModel,
    ScoutingEvaluationModel,
)
from app.models.governance import (
    DataSourceModel,
    DataQualityRecordModel,
)
from app.services.identity.player_identity_service import PlayerIdentityService


class ColumnMappingConfig(BaseModel):
    """
    Configurable column mapping to adapt to the upcoming 8 November RR data pack.
    Permits mapping any arbitrary CSV or JSON schema to canonical attributes.
    """
    name_col: str = Field(default="player_name", description="Column containing player's full name")
    external_id_col: Optional[str] = Field(default=None, description="Column with RR internal or source ID")
    dob_col: Optional[str] = Field(default="dob", description="Column with date of birth (YYYY-MM-DD or DD/MM/YYYY)")
    state_association_col: Optional[str] = Field(default="state_association", description="State cricket association column")
    primary_role_col: Optional[str] = Field(default="primary_role", description="Role column (e.g. Batter, Bowler)")
    batting_hand_col: Optional[str] = Field(default="batting_hand", description="Batting hand (Right/Left)")
    bowling_style_col: Optional[str] = Field(default="bowling_style", description="Bowling style description")
    
    # Scouting & Evaluation columns
    scout_id_col: Optional[str] = Field(default="scout_id", description="Scout code or name")
    evaluation_date_col: Optional[str] = Field(default="evaluation_date", description="Assessment date")
    technical_rating_col: Optional[str] = Field(default="technical_rating", description="1-10 skill rating")
    temperament_rating_col: Optional[str] = Field(default="temperament_rating", description="1-10 temperament rating")
    athleticism_rating_col: Optional[str] = Field(default="athleticism_rating", description="1-10 athleticism rating")
    tactical_iq_rating_col: Optional[str] = Field(default="tactical_iq_rating", description="1-10 tactical IQ rating")
    potential_rating_col: Optional[str] = Field(default="potential_rating", description="1-10 ceiling potential rating")
    strengths_col: Optional[str] = Field(default="strengths", description="Strengths summary")
    development_col: Optional[str] = Field(default="development_areas", description="Development points")
    recommendation_col: Optional[str] = Field(default="recommendation", description="Scout recommendation")
    confidential_notes_col: Optional[str] = Field(default="confidential_notes", description="Restricted scout notes")
    is_trialist_col: Optional[str] = Field(default="is_rr_trialist", description="Boolean or string flag for RR trialists")


class SchemaDiscoveryResult(BaseModel):
    """Schema discovery summary analyzing incoming candidate columns and types."""
    detected_columns: List[str]
    sample_row_count: int
    recommended_mapping: ColumnMappingConfig
    column_type_hints: Dict[str, str]
    unmapped_columns: List[str]


class RRDataPackIngestionSummary(BaseModel):
    """Execution telemetry for RR proprietary data pack ingestion."""
    dataset_key: str
    total_rows_parsed: int
    players_created: int
    players_matched_existing: int
    conflicts_detected: int
    missing_dob_count: int
    evaluations_recorded: int
    conflict_reports: List[Dict[str, Any]] = Field(default_factory=list)
    missing_field_reports: List[Dict[str, Any]] = Field(default_factory=list)
    data_classification: str = "RR_PROPRIETARY_CONFIDENTIAL"


class RRDataPackService:
    """Service governing RR proprietary data packs, column mapping, and access boundaries."""

    @staticmethod
    def discover_schema(sample_rows: List[Dict[str, Any]]) -> SchemaDiscoveryResult:
        """
        Inspects sample rows from an incoming data file to detect headers, types,
        and generate a smart recommended mapping.
        """
        if not sample_rows:
            return SchemaDiscoveryResult(
                detected_columns=[],
                sample_row_count=0,
                recommended_mapping=ColumnMappingConfig(),
                column_type_hints={},
                unmapped_columns=[]
            )

        detected_columns = list(sample_rows[0].keys())
        type_hints: Dict[str, str] = {}
        
        # Detect types
        for col in detected_columns:
            non_null_val = next((row[col] for row in sample_rows if row.get(col) is not None), None)
            if non_null_val is None:
                type_hints[col] = "unknown_null"
            elif isinstance(non_null_val, bool):
                type_hints[col] = "boolean"
            elif isinstance(non_null_val, int):
                type_hints[col] = "integer"
            elif isinstance(non_null_val, float):
                type_hints[col] = "float"
            else:
                str_val = str(non_null_val).strip()
                # Check date
                if any(delim in str_val for delim in ["-", "/"]) and len(str_val) in [8, 9, 10]:
                    type_hints[col] = "date_candidate"
                else:
                    type_hints[col] = "string"

        # Build recommended mapping based on fuzzy keyword matching
        mapping = ColumnMappingConfig()
        lowered_map = {col.lower().replace(" ", "_"): col for col in detected_columns}

        def match_col(keywords: List[str], default_val: Optional[str]) -> Optional[str]:
            for kw in keywords:
                for low, orig in lowered_map.items():
                    if kw in low:
                        return orig
            return default_val if default_val in detected_columns else None

        mapping.name_col = match_col(["name", "player", "player_name", "athlete"], "player_name") or detected_columns[0]
        mapping.dob_col = match_col(["dob", "birth", "date_of_birth"], "dob")
        mapping.state_association_col = match_col(["state", "association", "team", "domestic"], "state_association")
        mapping.primary_role_col = match_col(["role", "discipline", "category"], "primary_role")
        mapping.batting_hand_col = match_col(["batting_hand", "batting_style", "bats"], "batting_hand")
        mapping.bowling_style_col = match_col(["bowling_style", "bowl", "bowling_type"], "bowling_style")
        mapping.technical_rating_col = match_col(["tech", "skill", "technique"], "technical_rating")
        mapping.potential_rating_col = match_col(["potential", "ceiling", "future"], "potential_rating")
        mapping.confidential_notes_col = match_col(["notes", "scout_notes", "confidential", "comments"], "confidential_notes")

        mapped_values = set(mapping.model_dump().values())
        unmapped = [col for col in detected_columns if col not in mapped_values]

        return SchemaDiscoveryResult(
            detected_columns=detected_columns,
            sample_row_count=len(sample_rows),
            recommended_mapping=mapping,
            column_type_hints=type_hints,
            unmapped_columns=unmapped,
        )

    @staticmethod
    def mask_confidential_data(data: Dict[str, Any], user_role: str = "public") -> Dict[str, Any]:
        """
        Enforces strict security boundary around RR proprietary scouting notes.
        Masks confidential scout comments and internal ratings unless user has RR scout privileges.
        """
        sanitized = dict(data)
        if user_role not in ["rr_scout_admin", "rr_lead_analyst", "super_admin"]:
            if "confidential_notes" in sanitized:
                sanitized["confidential_notes"] = "[RESTRICTED - RAJASTHAN ROYALS PROPRIETARY]"
            if "proprietary_notes" in sanitized:
                sanitized["proprietary_notes"] = "[RESTRICTED - RAJASTHAN ROYALS PROPRIETARY]"
            if "scout_identifier" in sanitized:
                sanitized["scout_identifier"] = "[ANONYMIZED_RR_SCOUT]"
            if "scouting_tier" in sanitized and sanitized.get("data_classification") == "RR_PROPRIETARY_CONFIDENTIAL":
                sanitized["scouting_tier"] = "INTERNAL"
        return sanitized

    @classmethod
    async def ingest_proprietary_pack(
        cls,
        session: AsyncSession,
        records: List[Dict[str, Any]],
        mapping: ColumnMappingConfig,
        dataset_key: str = "rr_uncapped_pack_2026",
        source_id: str = "rr_scouting",
        reference_date: Optional[date] = None,
    ) -> RRDataPackIngestionSummary:
        """
        Ingests a batch of records from the Rajasthan Royals proprietary data pack.
        Performs field mapping, player identity resolution, conflict detection,
        and creates confidential scouting evaluations.
        """
        ref_date = reference_date
        created_count = 0
        matched_count = 0
        conflict_count = 0
        missing_dob_count = 0
        evaluations_count = 0
        conflict_reports: List[Dict[str, Any]] = []
        missing_field_reports: List[Dict[str, Any]] = []

        # Ensure registered data source exists
        src_stmt = select(DataSourceModel).where(DataSourceModel.source_id == source_id)
        src_res = await session.execute(src_stmt)
        data_source = src_res.scalar_one_or_none()

        if not data_source:
            data_source = DataSourceModel(
                source_id=source_id,
                name="Rajasthan Royals Proprietary Scouting Pack",
                tier="TIER_3",
                category="PROPRIETARY_SCOUTING",
                access_method="INTERNAL_SECURE_TRANSFER",
                license_type="CONFIDENTIAL_RR_INTERNAL",
                update_frequency="AD_HOC",
                data_classification="RR_PROPRIETARY_CONFIDENTIAL",
            )
            session.add(data_source)
            await session.flush()

        for idx, row in enumerate(records):
            # Extract player name
            raw_name = row.get(mapping.name_col)
            if not raw_name:
                continue

            # Extract external ID
            ext_id = row.get(mapping.external_id_col) if mapping.external_id_col else f"rr_scout_row_{idx+1}"

            # Parse DOB
            parsed_dob: Optional[date] = None
            raw_dob = row.get(mapping.dob_col) if mapping.dob_col else None
            if raw_dob:
                if isinstance(raw_dob, date):
                    parsed_dob = raw_dob
                elif isinstance(raw_dob, str):
                    try:
                        # Attempt ISO YYYY-MM-DD
                        parsed_dob = datetime.strptime(raw_dob.strip(), "%Y-%m-%d").date()
                    except ValueError:
                        try:
                            # Attempt DD/MM/YYYY
                            parsed_dob = datetime.strptime(raw_dob.strip(), "%d/%m/%Y").date()
                        except ValueError:
                            parsed_dob = None

            if parsed_dob is None:
                missing_dob_count += 1
                missing_field_reports.append({
                    "row_index": idx + 1,
                    "player_name": raw_name,
                    "missing_field": "dob",
                    "action_taken": "Flagged as PENDING_VERIFICATION; age set to None",
                })

            # Extract demographics
            state_assoc = str(row.get(mapping.state_association_col)) if mapping.state_association_col and row.get(mapping.state_association_col) else None
            role = str(row.get(mapping.primary_role_col)) if mapping.primary_role_col and row.get(mapping.primary_role_col) else "All-Rounder"
            batting_hand = str(row.get(mapping.batting_hand_col)) if mapping.batting_hand_col and row.get(mapping.batting_hand_col) else None
            bowling_style = str(row.get(mapping.bowling_style_col)) if mapping.bowling_style_col and row.get(mapping.bowling_style_col) else None

            # Resolve or create player
            player, profile, was_created, conflicts = await PlayerIdentityService.resolve_or_create_player(
                session=session,
                source_name=source_id,
                external_id=str(ext_id),
                name=str(raw_name),
                dob=parsed_dob,
                dob_source=source_id if parsed_dob else None,
                batting_hand=batting_hand,
                bowling_style=bowling_style,
                primary_role=role,
                is_capped=False,
                state_association=state_assoc,
                reference_date=ref_date,
            )

            if was_created:
                created_count += 1
            else:
                matched_count += 1

            if conflicts:
                conflict_count += 1
                conflict_reports.append({
                    "row_index": idx + 1,
                    "player_name": player.full_name,
                    "conflicts": conflicts,
                })
                # Update quality record
                quality_stmt = select(DataQualityRecordModel).where(DataQualityRecordModel.entity_id == player.id)
                q_res = await session.execute(quality_stmt)
                q_rec = q_res.scalar_one_or_none()
                if not q_rec:
                    q_rec = DataQualityRecordModel(
                        entity_type="player",
                        entity_id=player.id,
                        completeness_score=75.0,
                        has_conflicts=True,
                        conflict_details="; ".join(conflicts),
                    )
                    session.add(q_rec)
                else:
                    q_rec.has_conflicts = True
                    q_rec.conflict_details = "; ".join(conflicts)

            # Check trialist flag
            if mapping.is_trialist_col and row.get(mapping.is_trialist_col):
                val = str(row[mapping.is_trialist_col]).lower()
                profile.is_rr_trialist = val in ["true", "1", "yes", "trialist"]

            # Record scouting evaluation if ratings or notes exist
            tech_rating = row.get(mapping.technical_rating_col)
            conf_notes = row.get(mapping.confidential_notes_col)
            if tech_rating is not None or conf_notes is not None:
                def safe_float(v: Any, default: float = 6.0) -> float:
                    try:
                        return float(v)
                    except (ValueError, TypeError):
                        return default

                eval_record = ScoutingEvaluationModel(
                    id=str(uuid.uuid4()),
                    uncapped_profile_id=profile.id,
                    scout_identifier=str(row.get(mapping.scout_id_col) or "RR_SCOUT_DOMESTIC"),
                    evaluation_date=ref_date or date.today(),
                    competition_or_trial="Domestic Scouting Pack 2026",
                    technical_skill_rating=safe_float(tech_rating, 6.5),
                    temperament_rating=safe_float(row.get(mapping.temperament_rating_col), 6.5),
                    athleticism_rating=safe_float(row.get(mapping.athleticism_rating_col), 7.0),
                    tactical_iq_rating=safe_float(row.get(mapping.tactical_iq_rating_col), 6.5),
                    ceiling_potential_rating=safe_float(row.get(mapping.potential_rating_col), 7.5),
                    strengths_summary=str(row.get(mapping.strengths_col) or "Identified via RR domestic scouting screening."),
                    development_areas=str(row.get(mapping.development_col) or "Requires exposure against high-pace variations."),
                    scout_recommendation=str(row.get(mapping.recommendation_col) or "SHORTLIST"),
                    proprietary_notes=str(conf_notes) if conf_notes else None,
                    data_classification="RR_PROPRIETARY_CONFIDENTIAL",
                )
                session.add(eval_record)
                evaluations_count += 1

        await session.flush()

        return RRDataPackIngestionSummary(
            dataset_key=dataset_key,
            total_rows_parsed=len(records),
            players_created=created_count,
            players_matched_existing=matched_count,
            conflicts_detected=conflict_count,
            missing_dob_count=missing_dob_count,
            evaluations_recorded=evaluations_count,
            conflict_reports=conflict_reports,
            missing_field_reports=missing_field_reports,
            data_classification="RR_PROPRIETARY_CONFIDENTIAL",
        )
