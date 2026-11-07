"""
Royals Intelligence - Player Identity & Eligibility Resolution Service
Manages canonical player deduplication, source-specific ID mapping, name aliases,
age calculation from reference dates, conflict detection, and strict uncapped eligibility.
"""

import re
import uuid
from datetime import date, datetime
from typing import Optional, List, Dict, Any, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_

from app.models.core import PlayerModel, PlayerIdentityModel
from app.models.scouting import UncappedPlayerProfileModel
from app.models.governance import DataQualityRecordModel
from app.core.logging import logger

# Default competition reference date for IPL 2026 / 2027 recruitment decisions
DEFAULT_COMPETITION_REFERENCE_DATE = date(2026, 11, 18)


class PlayerIdentityService:
    """Enterprise service for player identity, deduplication, conflict auditing, and eligibility."""

    @staticmethod
    def normalize_name(raw_name: str) -> str:
        """
        Standardizes a cricket player name.
        Removes dots from initials, strips whitespace, converts to title case.
        e.g., 'R. Parag' -> 'R Parag', 'A.B. de Villiers' -> 'Ab De Villiers'
        """
        if not raw_name:
            return ""
        # Remove dots completely from initials: 'A.B. de Villiers' -> 'AB de Villiers'
        cleaned = raw_name.replace(".", "")
        # Collapse multiple spaces
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        return cleaned.title()

    @staticmethod
    def calculate_age(dob: Optional[date], reference_date: Optional[date] = None) -> Optional[float]:
        """
        Calculates exact age in fractional years at a configurable reference date.
        Strict rule: Never invents dates of birth. Returns None if DOB is absent.
        """
        if dob is None:
            return None
        
        ref = reference_date or DEFAULT_COMPETITION_REFERENCE_DATE
        if dob > ref:
            return 0.0
            
        days = (ref - dob).days
        # Standard Gregorian year approximation
        return round(days / 365.25, 1)

    @staticmethod
    def detect_conflicts(existing_player: PlayerModel, incoming_data: Dict[str, Any]) -> List[str]:
        """
        Detects factual discrepancies between an existing canonical player record and incoming data.
        Returns list of human-readable conflict warnings.
        """
        conflicts = []
        
        # 1. DOB conflict
        incoming_dob = incoming_data.get("dob")
        if incoming_dob and existing_player.dob and incoming_dob != existing_player.dob:
            conflicts.append(
                f"DOB mismatch: existing record is {existing_player.dob} "
                f"(source: {existing_player.dob_source}), but incoming source claims {incoming_dob}"
            )
            
        # 2. Batting hand conflict
        incoming_batting_hand = incoming_data.get("batting_hand")
        if (
            incoming_batting_hand
            and existing_player.batting_hand
            and incoming_batting_hand.lower() != existing_player.batting_hand.lower()
        ):
            conflicts.append(
                f"Batting hand mismatch: existing record is {existing_player.batting_hand}, "
                f"incoming claim is {incoming_batting_hand}"
            )
            
        # 3. Senior cap status conflict
        incoming_capped = incoming_data.get("is_capped")
        if incoming_capped is not None and incoming_capped != existing_player.is_capped:
            conflicts.append(
                f"Cap status discrepancy: existing record is is_capped={existing_player.is_capped}, "
                f"incoming source reports is_capped={incoming_capped}"
            )
            
        return conflicts

    @classmethod
    def evaluate_uncapped_eligibility(
        cls,
        player: PlayerModel,
        profile: Optional[UncappedPlayerProfileModel] = None,
        conflicts: Optional[List[str]] = None,
        max_age_cutoff: Optional[float] = None,
        reference_date: Optional[date] = None,
    ) -> Tuple[str, List[str]]:
        """
        Determines the formal uncapped eligibility state for recruitment and auction rosters.
        Possible states:
          - CONFIRMED_UNCAPPED: Formally verified as eligible and uncapped.
          - SUSPECTED_CAPPED: Evidence of senior international cap detected.
          - INELIGIBLE_OVERAGE: Exceeds specified age threshold.
          - PENDING_VERIFICATION: Missing critical demographic/provenance proof (e.g. DOB missing).
          - FLAGGED_CONFLICT: Unresolved source conflicts present.
        """
        reasons = []
        
        # 1. Check senior cap status
        if player.is_capped:
            reasons.append("Player has represented Senior National team in official international cricket.")
            return "SUSPECTED_CAPPED", reasons

        # 2. Check for active unverified conflicts
        if conflicts and len(conflicts) > 0:
            reasons.extend(conflicts)
            return "FLAGGED_CONFLICT", reasons

        # 3. Check for missing DOB
        if player.dob is None:
            reasons.append("Date of birth missing. Verification incomplete; cannot certify age-group or debut eligibility.")
            return "PENDING_VERIFICATION", reasons

        # 4. Check for age cutoff if specified by tournament rules
        age = cls.calculate_age(player.dob, reference_date)
        if max_age_cutoff is not None and age is not None and age > max_age_cutoff:
            reasons.append(f"Player age ({age} yrs) exceeds tournament maximum age cutoff ({max_age_cutoff} yrs).")
            return "INELIGIBLE_OVERAGE", reasons

        # 5. Passed all checks
        reasons.append("Confirmed uncapped: Zero senior international caps and valid domestic registration verified.")
        return "CONFIRMED_UNCAPPED", reasons

    @classmethod
    async def resolve_or_create_player(
        cls,
        session: AsyncSession,
        source_name: str,
        external_id: str,
        name: str,
        dob: Optional[date] = None,
        dob_source: Optional[str] = None,
        batting_hand: Optional[str] = None,
        bowling_style: Optional[str] = None,
        primary_role: Optional[str] = None,
        is_capped: bool = False,
        state_association: Optional[str] = None,
        reference_date: Optional[date] = None,
    ) -> Tuple[PlayerModel, UncappedPlayerProfileModel, bool, List[str]]:
        """
        Resolves a player using their source ID or name matching.
        If player exists:
          - Audits for conflicts.
          - Links new external identity alias if needed.
        If player does not exist:
          - Creates canonical PlayerModel and initial UncappedPlayerProfileModel.
        Returns: (player, uncapped_profile, created_flag, conflicts_list)
        """
        normalized_name = cls.normalize_name(name)
        ref_date = reference_date or DEFAULT_COMPETITION_REFERENCE_DATE
        conflicts: List[str] = []
        
        # 1. First search by external identity link
        identity_stmt = (
            select(PlayerIdentityModel)
            .where(
                PlayerIdentityModel.source_name == source_name,
                PlayerIdentityModel.external_player_id == str(external_id)
            )
        )
        res = await session.execute(identity_stmt)
        identity = res.scalar_one_or_none()

        if identity:
            # Player already linked via this external source
            player_stmt = select(PlayerModel).where(PlayerModel.id == identity.player_id)
            p_res = await session.execute(player_stmt)
            player = p_res.scalar_one()
            
            # Check for incoming conflicts
            incoming_dict = {
                "dob": dob,
                "batting_hand": batting_hand,
                "is_capped": is_capped,
            }
            conflicts = cls.detect_conflicts(player, incoming_dict)
            
            # Retrieve or create profile
            profile_stmt = select(UncappedPlayerProfileModel).where(UncappedPlayerProfileModel.player_id == player.id)
            prof_res = await session.execute(profile_stmt)
            profile = prof_res.scalar_one_or_none()
            
            if not profile:
                profile = cls._build_uncapped_profile(player, state_association, ref_date)
                session.add(profile)
                
            return player, profile, False, conflicts

        # 2. Second search by normalized name and DOB
        candidate_stmt = select(PlayerModel).where(PlayerModel.full_name == normalized_name)
        c_res = await session.execute(candidate_stmt)
        candidates = c_res.scalars().all()

        matched_player: Optional[PlayerModel] = None
        for candidate in candidates:
            if dob and candidate.dob:
                if candidate.dob == dob:
                    matched_player = candidate
                    break
                else:
                    # Same name, different DOB -> Different players (e.g., two domestic players with common name)
                    continue
            elif not dob or not candidate.dob:
                # Name matches, one side missing DOB -> match with caution
                matched_player = candidate
                break

        if matched_player:
            # Audit conflicts
            incoming_dict = {
                "dob": dob,
                "batting_hand": batting_hand,
                "is_capped": is_capped,
            }
            conflicts = cls.detect_conflicts(matched_player, incoming_dict)
            
            # Link new external identity
            new_identity = PlayerIdentityModel(
                id=str(uuid.uuid4()),
                player_id=matched_player.id,
                source_name=source_name,
                external_player_id=str(external_id),
                name_as_source=name,
                confidence_score=0.95 if not conflicts else 0.70,
                conflict_notes="; ".join(conflicts) if conflicts else None
            )
            session.add(new_identity)
            
            # Update DOB if previously missing and newly provided with provenance
            if matched_player.dob is None and dob is not None:
                matched_player.dob = dob
                matched_player.dob_source = dob_source or source_name
                matched_player.dob_verified = True
                
            # Retrieve or create profile
            profile_stmt = select(UncappedPlayerProfileModel).where(UncappedPlayerProfileModel.player_id == matched_player.id)
            prof_res = await session.execute(profile_stmt)
            profile = prof_res.scalar_one_or_none()
            if not profile:
                profile = cls._build_uncapped_profile(matched_player, state_association, ref_date)
                session.add(profile)
            else:
                # Recalculate age and eligibility
                status, reasons = cls.evaluate_uncapped_eligibility(matched_player, profile, conflicts, reference_date=ref_date)
                profile.eligibility_status = status
                profile.calculated_age_at_cutoff = cls.calculate_age(matched_player.dob, ref_date)
                profile.verification_notes = "; ".join(reasons)

            return matched_player, profile, False, conflicts

        # 3. Create brand new canonical player
        canonical_slug = f"{normalized_name.lower().replace(' ', '_')}_{str(uuid.uuid4())[:6]}"
        player_pk = str(uuid.uuid4())
        new_player = PlayerModel(
            id=player_pk,
            canonical_id=canonical_slug,
            full_name=normalized_name,
            known_as=name,
            dob=dob,
            dob_source=dob_source if dob else None,
            dob_verified=True if dob else False,
            nationality="India",
            home_state_association=state_association,
            batting_hand=batting_hand,
            bowling_style=bowling_style,
            primary_role=primary_role or "All-Rounder",
            is_capped=is_capped,
        )
        session.add(new_player)
        await session.flush()  # populate new_player.id

        # Add external identity link
        new_identity = PlayerIdentityModel(
            id=str(uuid.uuid4()),
            player_id=new_player.id,
            source_name=source_name,
            external_player_id=str(external_id),
            name_as_source=name,
            confidence_score=1.0,
        )
        session.add(new_identity)

        # Build uncapped scouting profile
        profile = cls._build_uncapped_profile(new_player, state_association, ref_date)
        session.add(profile)

        # Record data quality diagnostic if DOB is missing
        if dob is None:
            quality_record = DataQualityRecordModel(
                id=str(uuid.uuid4()),
                entity_type="player",
                entity_id=new_player.id,
                completeness_score=60.0,
                has_conflicts=False,
                missing_fields="dob, dob_source",
                is_quarantined=False,
            )
            session.add(quality_record)

        return new_player, profile, True, []

    @classmethod
    def _build_uncapped_profile(
        cls,
        player: PlayerModel,
        state_association: Optional[str],
        reference_date: date,
    ) -> UncappedPlayerProfileModel:
        """Internal helper to construct a standardized uncapped scouting profile."""
        age = cls.calculate_age(player.dob, reference_date)
        status, reasons = cls.evaluate_uncapped_eligibility(player, reference_date=reference_date)

        return UncappedPlayerProfileModel(
            id=str(uuid.uuid4()),
            player_id=player.id,
            eligibility_status=status,
            eligibility_verified_at=datetime.utcnow() if status == "CONFIRMED_UNCAPPED" else None,
            verification_notes="; ".join(reasons),
            calculated_age_at_cutoff=age,
            reference_date_used=reference_date,
            state_association=state_association or player.home_state_association,
            current_domestic_team=state_association or player.home_state_association,
            primary_discipline=player.primary_role or "All-Rounder",
            scouting_tier="MONITOR",
            is_rr_trialist=False,
            has_video_evidence=False,
            data_classification="INTERNAL_SCOUTING",
        )
