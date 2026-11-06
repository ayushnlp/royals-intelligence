"""
Royals Intelligence - Cricket Data Validation Engine
Performs structural, cricket-rules, and data-integrity quality checks on raw match data.
"""

from typing import Dict, Any, List, Tuple, Set
from app.schemas.contracts.ingestion_contracts import ValidationSummary, ValidationErrorItem
from app.core.logging import logger


class CricketDataValidator:
    """Validates structural and cricket-specific integrity of match datasets."""

    @staticmethod
    def validate_cricsheet_match_dict(match_data: Dict[str, Any], match_id: str) -> ValidationSummary:
        """
        Comprehensive validation of a single Cricsheet JSON match structure.
        Returns a detailed ValidationSummary.
        """
        errors: List[ValidationErrorItem] = []
        warnings: List[ValidationErrorItem] = []
        total_checks = 0
        valid_checks = 0
        duplicates = 0

        # --- 1. Structural Checks ---
        total_checks += 1
        if not isinstance(match_data, dict):
            errors.append(ValidationErrorItem(
                record_identifier=match_id,
                error_type="STRUCTURAL_ERROR",
                message="Match data root must be a JSON object / dictionary.",
                severity="CRITICAL"
            ))
            return ValidationSummary(
                total_records=1,
                valid_records=0,
                rejected_records=1,
                warning_count=0,
                duplicate_records_detected=0,
                completeness_percentage=0.0,
                errors=errors,
                passed=False
            )
        valid_checks += 1

        # Check required top-level keys
        for key in ["info", "innings"]:
            total_checks += 1
            if key not in match_data:
                errors.append(ValidationErrorItem(
                    record_identifier=match_id,
                    error_type="MISSING_REQUIRED_KEY",
                    field_name=key,
                    message=f"Root object is missing mandatory section '{key}'.",
                    severity="CRITICAL"
                ))
            else:
                valid_checks += 1

        info = match_data.get("info", {})
        innings_list = match_data.get("innings", [])

        # --- 2. Match Info Checks ---
        required_info_fields = ["teams", "dates", "match_type"]
        for field in required_info_fields:
            total_checks += 1
            if field not in info or not info[field]:
                errors.append(ValidationErrorItem(
                    record_identifier=f"{match_id}.info",
                    error_type="MISSING_INFO_FIELD",
                    field_name=field,
                    message=f"Match info section missing '{field}'.",
                    severity="CRITICAL"
                ))
            else:
                valid_checks += 1

        teams = info.get("teams", [])
        total_checks += 1
        if len(teams) != 2:
            errors.append(ValidationErrorItem(
                record_identifier=f"{match_id}.info.teams",
                error_type="INVALID_TEAMS_COUNT",
                message=f"Match must feature exactly 2 teams. Found: {len(teams)}",
                severity="CRITICAL"
            ))
        else:
            valid_checks += 1

        # Check players registry if present
        players_dict = info.get("players", {})
        if players_dict:
            for team_name, squad in players_dict.items():
                total_checks += 1
                if not isinstance(squad, list) or len(squad) < 11:
                    warnings.append(ValidationErrorItem(
                        record_identifier=f"{match_id}.players.{team_name}",
                        error_type="SQUAD_SIZE_WARNING",
                        message=f"Team '{team_name}' listed with {len(squad)} players (standard Playing XI is 11+).",
                        severity="WARNING"
                    ))
                else:
                    valid_checks += 1

        # --- 3. Cricket Deliveries & Innings Checks ---
        total_checks += 1
        if not isinstance(innings_list, list) or len(innings_list) == 0:
            errors.append(ValidationErrorItem(
                record_identifier=f"{match_id}.innings",
                error_type="EMPTY_INNINGS_ERROR",
                message="Match contains no innings records.",
                severity="CRITICAL"
            ))
        else:
            valid_checks += 1

        seen_deliveries: Set[Tuple[int, int, int]] = set()

        for innings_idx, innings in enumerate(innings_list, start=1):
            team_batting = innings.get("team")
            overs = innings.get("overs", [])

            total_checks += 1
            if not team_batting:
                errors.append(ValidationErrorItem(
                    record_identifier=f"{match_id}.innings[{innings_idx}]",
                    error_type="MISSING_BATTING_TEAM",
                    message=f"Innings {innings_idx} does not specify batting team.",
                    severity="CRITICAL"
                ))
            else:
                valid_checks += 1

            prev_over_num = -1
            for over in overs:
                over_num = over.get("over", 0)
                total_checks += 1
                # Check over monotonicity
                if over_num < prev_over_num:
                    errors.append(ValidationErrorItem(
                        record_identifier=f"{match_id}.innings[{innings_idx}].over[{over_num}]",
                        error_type="NON_MONOTONIC_OVER",
                        message=f"Over sequence decreased from {prev_over_num} to {over_num}.",
                        severity="CRITICAL"
                    ))
                else:
                    valid_checks += 1
                prev_over_num = over_num

                deliveries = over.get("deliveries", [])
                for ball_idx, delivery in enumerate(deliveries, start=1):
                    total_checks += 1
                    delivery_key = (innings_idx, over_num, ball_idx)
                    if delivery_key in seen_deliveries:
                        duplicates += 1
                        warnings.append(ValidationErrorItem(
                            record_identifier=f"{match_id}.innings[{innings_idx}].over[{over_num}].ball[{ball_idx}]",
                            error_type="DUPLICATE_DELIVERY",
                            message=f"Duplicate delivery sequence key {delivery_key}.",
                            severity="WARNING"
                        ))
                    else:
                        seen_deliveries.add(delivery_key)

                    # Delivery essential actors
                    striker = delivery.get("batter")
                    non_striker = delivery.get("non_striker")
                    bowler = delivery.get("bowler")
                    runs = delivery.get("runs", {})

                    if not (striker and non_striker and bowler):
                        errors.append(ValidationErrorItem(
                            record_identifier=f"{match_id}.innings[{innings_idx}].over[{over_num}].ball[{ball_idx}]",
                            error_type="MISSING_DELIVERY_ACTORS",
                            message="Delivery missing batter, non_striker, or bowler identifier.",
                            severity="CRITICAL"
                        ))
                        continue

                    # Run arithmetic check: batter + extras == total
                    batter_runs = runs.get("batter", 0)
                    extras_runs = runs.get("extras", 0)
                    total_runs = runs.get("total", 0)

                    if batter_runs + extras_runs != total_runs:
                        errors.append(ValidationErrorItem(
                            record_identifier=f"{match_id}.innings[{innings_idx}].over[{over_num}].ball[{ball_idx}]",
                            error_type="ARITHMETIC_MISMATCH",
                            field_name="runs.total",
                            message=f"Arithmetic mismatch: batter ({batter_runs}) + extras ({extras_runs}) != total ({total_runs}).",
                            severity="CRITICAL"
                        ))
                    else:
                        valid_checks += 1

                    # Wicket dismissal consistency check
                    if "wickets" in delivery:
                        for w in delivery["wickets"]:
                            total_checks += 1
                            kind = w.get("kind")
                            player_out = w.get("player_out")
                            if not player_out:
                                errors.append(ValidationErrorItem(
                                    record_identifier=f"{match_id}.over[{over_num}].wicket",
                                    error_type="DISMISSAL_MISSING_PLAYER",
                                    message="Dismissal record missing 'player_out'.",
                                    severity="CRITICAL"
                                ))
                            elif kind == "caught" and not w.get("fielders"):
                                warnings.append(ValidationErrorItem(
                                    record_identifier=f"{match_id}.over[{over_num}].wicket",
                                    error_type="CAUGHT_WITHOUT_FIELDER",
                                    message=f"Caught dismissal for '{player_out}' missing fielder attribution.",
                                    severity="WARNING"
                                ))
                            else:
                                valid_checks += 1

        # Summary calculation
        all_issues = errors + warnings
        has_critical = any(e.severity == "CRITICAL" for e in errors)
        completeness = round((valid_checks / total_checks) * 100, 2) if total_checks > 0 else 0.0

        return ValidationSummary(
            total_records=total_checks,
            valid_records=valid_checks,
            rejected_records=len(errors),
            warning_count=len(warnings),
            duplicate_records_detected=duplicates,
            completeness_percentage=completeness,
            errors=all_issues,
            passed=(not has_critical)
        )
