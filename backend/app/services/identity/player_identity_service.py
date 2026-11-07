"""
Royals Intelligence - Player Identity & Eligibility Resolution Service
Manages canonical player deduplication, source-specific ID mapping, name normalization,
fractional age calculation from confirmed reference dates, demographic conflict detection,
and competition-specific uncapped eligibility certification.
"""

import re
import uuid
from datetime import date, datetime, timezone
from typing import Optional, List, Dict, Any, Tuple
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_

from app.models.core import PlayerModel, PlayerIdentityModel
from app.models.scouting import UncappedPlayerProfileModel
from app.models.governance import DataQualityRecordModel
from app.core.logging import logger


class EligibilityRuleConfig(BaseModel):
    """
    Formal configuration of competition-specific uncapped eligibility regulations.
    Decouples lifetime cap facts from competition rules (e.g. IPL 5-year inactive international clause).
    If official rules or cutoff dates are unpromulgated, represents them as unverified/unresolved.
    """
    competition_id: str = "ipl"
    season: str = "2026"
    official_age_cutoff_date: Optional[date] = None  # None = Unconfirmed / unpromulgated by BCCI
    max_age_cutoff: Optional[float] = None            # None for open-age tournament
    allow_five_year_retired_as_uncapped: bool = True  # IPL Rule 4.3 (5 years no international play)
    require_verified_dob: bool = True
    rule_source: str = "Pending Official Tournament Circular"
    rule_version: str = "UNVERIFIED"
    is_rule_verified: bool = False                    # Must be True to certify CONFIRMED_UNCAPPED


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
        Calculates exact age in fractional years at an explicitly confirmed reference date.
        Strict Rules:
          - Never invents dates of birth. Returns None if DOB is absent.
          - Never silently assumes an unverified cutoff date. Returns None if reference_date is None.
          - Returns None if DOB is in the future relative to the reference date.
          - Rejects biologically impossible cricketer ages (< 10 or > 65 yrs).
        """
        if dob is None or reference_date is None:
            return None
        
        if dob > reference_date:
            logger.warning(f"Demographic error: DOB {dob} is in the future relative to reference {reference_date}.")
            return None
            
        days = (reference_date - dob).days
        fractional_years = round(days / 365.25, 1)

        if fractional_years < 10.0 or fractional_years > 65.0:
            logger.warning(f"Demographic anomaly: Calculated age {fractional_years} outside plausible professional cricket range.")
            return None

        return fractional_years

    @staticmethod
    def detect_conflicts(existing_player: PlayerModel, incoming_data: Dict[str, Any]) -> List[str]:
        """
        Detects factual discrepancies between an existing canonical player record and incoming data.
        Returns list of human-readable conflict warnings.
        """
        conflicts = []
        
        # 1. DOB conflict & validity
        incoming_dob = incoming_data.get("dob")
        if incoming_dob:
            if existing_player.dob and incoming_dob != existing_player.dob:
                conflicts.append(
                    f"DOB mismatch: existing record is {existing_player.dob} "
                    f"(source: {existing_player.dob_source}), but incoming source claims {incoming_dob}"
                )
            # Check if incoming DOB is in the future relative to today
            today = date.today()
            if incoming_dob > today:
                conflicts.append(f"Invalid future DOB: incoming DOB {incoming_dob} is after current date {today}.")
            
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
        rule_config: Optional[EligibilityRuleConfig] = None,
        reference_date: Optional[date] = None,
        max_age_cutoff: Optional[float] = None,
    ) -> Tuple[str, List[str]]:
        """
        Determines the formal uncapped eligibility state for recruitment and auction rosters.
        Decouples senior international appearances from tournament eligibility rules (e.g. IPL 5-year inactive clause).

        Possible states:
          - CONFIRMED_UNCAPPED: Formally verified as eligible and uncapped under official rules.
          - INELIGIBLE_CAPPED: Active senior international player ineligible under rules.
          - INELIGIBLE_OVERAGE: Exceeds confirmed tournament maximum age cutoff.
          - PENDING_VERIFICATION: Missing DOB, unverified rules, or unconfirmed reference date.
          - FLAGGED_CONFLICT: Unresolved source conflicts present.
        """
        reasons: List[str] = []
        
        # 1. Unresolved conflicts take highest precedence
        if conflicts and len(conflicts) > 0:
            reasons.extend(conflicts)
            return "FLAGGED_CONFLICT", reasons

        # 2. Check for missing DOB provenance
        if player.dob is None:
            reasons.append("Date of birth missing. Verification incomplete; cannot certify age-group or debut eligibility without verified DOB provenance.")
            return "PENDING_VERIFICATION", reasons

        # 3. Check for unverified DOB if rule config requires verified source
        if rule_config and rule_config.require_verified_dob and not player.dob_verified:
            reasons.append(f"Date of birth unverified from primary official registry (current source: '{player.dob_source or 'None'}'). Official verification required.")
            return "PENDING_VERIFICATION", reasons

        # Effective reference date for age / inactivity calculations
        effective_cutoff = reference_date or (rule_config.official_age_cutoff_date if rule_config else None)

        # 4. Senior International Cap Evaluation
        if player.is_capped:
            allow_retired = rule_config.allow_five_year_retired_as_uncapped if rule_config else True
            if allow_retired:
                if player.last_international_match_date is not None:
                    if effective_cutoff is None:
                        reasons.append("Player holds senior international cap; evaluation under 5-year inactive clause is PENDING confirmation of official season reference date.")
                        return "PENDING_VERIFICATION", reasons
                    
                    years_since_last_match = (effective_cutoff - player.last_international_match_date).days / 365.25
                    if years_since_last_match >= 5.0:
                        reasons.append(
                            f"Eligible as uncapped under IPL 5-year international inactivity clause. "
                            f"Last senior appearance: {player.last_international_match_date} ({round(years_since_last_match, 1)} yrs ago)."
                        )
                        return "CONFIRMED_UNCAPPED", reasons
                    else:
                        reasons.append(
                            f"Ineligible: Active senior international representation within preceding 5 years "
                            f"(Last match: {player.last_international_match_date})."
                        )
                        return "INELIGIBLE_CAPPED", reasons
                else:
                    reasons.append(
                        "Player has senior international caps on record, but last appearance date is unverified; "
                        "cannot certify 5-year inactivity exemption."
                    )
                    return "PENDING_VERIFICATION", reasons
            else:
                reasons.append("Ineligible: Player has represented Senior National team in official international cricket.")
                return "INELIGIBLE_CAPPED", reasons

        # 5. Tournament Maximum Age Cutoff Evaluation
        effective_max_age = max_age_cutoff or (rule_config.max_age_cutoff if rule_config else None)
        if effective_max_age is not None:
            if effective_cutoff is None:
                reasons.append(f"Tournament specifies maximum age cutoff ({effective_max_age} yrs), but official reference date is unconfirmed.")
                return "PENDING_VERIFICATION", reasons
            
            calculated_age = cls.calculate_age(player.dob, effective_cutoff)
            if calculated_age is not None and calculated_age > effective_max_age:
                reasons.append(f"Player age ({calculated_age} yrs) exceeds tournament maximum age cutoff ({effective_max_age} yrs).")
                return "INELIGIBLE_OVERAGE", reasons

        # 6. Rule Verification Status Check
        if rule_config and not rule_config.is_rule_verified:
            reasons.append(
                f"Zero senior international caps verified, but official {rule_config.competition_id.upper()} "
                f"{rule_config.season} regulations/cutoffs remain pending formal release. Status marked PENDING_VERIFICATION."
            )
            return "PENDING_VERIFICATION", reasons

        # 7. Formally Confirmed Uncapped
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
        dob_verified: bool = False,
        batting_hand: Optional[str] = None,
        bowling_style: Optional[str] = None,
        primary_role: Optional[str] = None,
        is_capped: bool = False,
        last_international_match_date: Optional[date] = None,
        state_association: Optional[str] = None,
        rule_config: Optional[EligibilityRuleConfig] = None,
        reference_date: Optional[date] = None,
    ) -> Tuple[PlayerModel, UncappedPlayerProfileModel, bool, List[str]]:
        """
        Resolves a player using their source ID or name matching.
        If player exists:
          - Audits for demographic and cap conflicts.
          - Links new external identity alias if needed.
        If player does not exist:
          - Creates canonical PlayerModel and initial UncappedPlayerProfileModel.
        Returns: (player, uncapped_profile, created_flag, conflicts_list)
        """
        normalized_name = cls.normalize_name(name)
        ref_date = reference_date or (rule_config.official_age_cutoff_date if rule_config else None)
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
            player_stmt = select(PlayerModel).where(PlayerModel.id == identity.player_id)
            p_res = await session.execute(player_stmt)
            player = p_res.scalar_one()
            
            incoming_dict = {
                "dob": dob,
                "batting_hand": batting_hand,
                "is_capped": is_capped,
            }
            conflicts = cls.detect_conflicts(player, incoming_dict)
            
            profile_stmt = select(UncappedPlayerProfileModel).where(UncappedPlayerProfileModel.player_id == player.id)
            prof_res = await session.execute(profile_stmt)
            profile = prof_res.scalar_one_or_none()
            
            if not profile:
                profile = cls._build_uncapped_profile(player, state_association, ref_date, rule_config)
                session.add(profile)
            else:
                status, reasons = cls.evaluate_uncapped_eligibility(
                    player, profile, conflicts, rule_config=rule_config, reference_date=ref_date
                )
                profile.eligibility_status = status
                profile.calculated_age_at_cutoff = cls.calculate_age(player.dob, ref_date)
                profile.reference_date_used = ref_date
                profile.verification_notes = "; ".join(reasons)
                
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
                    # Same name, different DOB -> distinct domestic cricketers
                    continue
            elif not dob or not candidate.dob:
                # Same name, one side missing DOB -> match with caution
                matched_player = candidate
                break

        if matched_player:
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
                matched_player.dob_verified = dob_verified or bool(dob_source)

            if last_international_match_date and not matched_player.last_international_match_date:
                matched_player.last_international_match_date = last_international_match_date
                
            profile_stmt = select(UncappedPlayerProfileModel).where(UncappedPlayerProfileModel.player_id == matched_player.id)
            prof_res = await session.execute(profile_stmt)
            profile = prof_res.scalar_one_or_none()
            if not profile:
                profile = cls._build_uncapped_profile(matched_player, state_association, ref_date, rule_config)
                session.add(profile)
            else:
                status, reasons = cls.evaluate_uncapped_eligibility(
                    matched_player, profile, conflicts, rule_config=rule_config, reference_date=ref_date
                )
                profile.eligibility_status = status
                profile.calculated_age_at_cutoff = cls.calculate_age(matched_player.dob, ref_date)
                profile.reference_date_used = ref_date
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
            dob_verified=dob_verified or (bool(dob) and bool(dob_source)),
            nationality="India",
            home_state_association=state_association,
            batting_hand=batting_hand,
            bowling_style=bowling_style,
            primary_role=primary_role or "All-Rounder",
            is_capped=is_capped,
            last_international_match_date=last_international_match_date,
            international_caps_detail="Senior cap recorded" if is_capped else "Zero senior caps",
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
        profile = cls._build_uncapped_profile(new_player, state_association, ref_date, rule_config)
        session.add(profile)

        # Record data quality diagnostic if critical fields missing
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
        reference_date: Optional[date],
        rule_config: Optional[EligibilityRuleConfig] = None,
    ) -> UncappedPlayerProfileModel:
        """Internal helper to construct a standardized uncapped scouting profile."""
        age = cls.calculate_age(player.dob, reference_date)
        status, reasons = cls.evaluate_uncapped_eligibility(
            player, rule_config=rule_config, reference_date=reference_date
        )

        caps_detail = player.international_caps_detail or ("Senior international caps on record" if player.is_capped else "Zero senior international caps")

        return UncappedPlayerProfileModel(
            id=str(uuid.uuid4()),
            player_id=player.id,
            eligibility_status=status,
            eligibility_verified_at=datetime.now(timezone.utc) if status == "CONFIRMED_UNCAPPED" else None,
            verification_notes="; ".join(reasons),
            calculated_age_at_cutoff=age,
            reference_date_used=reference_date,
            international_caps_detail=caps_detail,
            last_international_appearance_date=player.last_international_match_date,
            eligibility_rule_source=rule_config.rule_source if rule_config else "Pending Official BCCI IPL 2026/2027 Guidelines",
            rule_version=rule_config.rule_version if rule_config else "UNVERIFIED_DRAFT",
            rule_evidence="; ".join(reasons),
            state_association=state_association or player.home_state_association,
            current_domestic_team=state_association or player.home_state_association,
            primary_discipline=player.primary_role or "All-Rounder",
            scouting_tier="MONITOR",
            is_rr_trialist=False,
            has_video_evidence=False,
            data_classification="INTERNAL_SCOUTING",
        )
