"""
Royals Intelligence - Database Models Registry
Re-exports all SQLAlchemy 2.0 models and registers them with Base.metadata.
"""

from app.models.core import (
    CompetitionModel,
    SeasonModel,
    TeamModel,
    VenueModel,
    PlayerModel,
    PlayerIdentityModel,
    PlayerRoleModel,
    MatchModel,
    InningsModel,
    PlayerParticipationModel,
    MatchWeatherModel,
    VenuePitchReportModel,
)
from app.models.performance import (
    BattingScorecardModel,
    BowlingScorecardModel,
    BallByBallDeliveryModel,
    FieldingContributionModel,
    PartnershipModel,
    PlayerMatchPerformanceModel,
)
from app.models.governance import (
    DataSourceModel,
    DatasetModel,
    IngestionRunModel,
    DatasetManifestModel,
    ValidationResultModel,
    SourceReferenceModel,
    DataQualityRecordModel,
)
from app.models.scouting import (
    UncappedPlayerProfileModel,
    PlayerPerformanceSnapshotModel,
    PlayerRoleAssessmentModel,
    ScoutingEvaluationModel,
    ScoutingEvidenceModel,
    PlayerComparisonModel,
)

__all__ = [
    # Core entities
    "CompetitionModel",
    "SeasonModel",
    "TeamModel",
    "VenueModel",
    "PlayerModel",
    "PlayerIdentityModel",
    "PlayerRoleModel",
    "MatchModel",
    "InningsModel",
    "PlayerParticipationModel",
    "MatchWeatherModel",
    "VenuePitchReportModel",
    # Performance entities
    "BattingScorecardModel",
    "BowlingScorecardModel",
    "BallByBallDeliveryModel",
    "FieldingContributionModel",
    "PartnershipModel",
    "PlayerMatchPerformanceModel",
    # Governance entities
    "DataSourceModel",
    "DatasetModel",
    "IngestionRunModel",
    "DatasetManifestModel",
    "ValidationResultModel",
    "SourceReferenceModel",
    "DataQualityRecordModel",
    # Scouting entities (Uncapped)
    "UncappedPlayerProfileModel",
    "PlayerPerformanceSnapshotModel",
    "PlayerRoleAssessmentModel",
    "ScoutingEvaluationModel",
    "ScoutingEvidenceModel",
    "PlayerComparisonModel",
]
