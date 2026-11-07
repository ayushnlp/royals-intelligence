export interface SystemHealth {
  status: "healthy" | "degraded_standby" | "unhealthy" | "checking";
  project: string;
  version: string;
  environment: string;
  timestamp: string;
  components?: {
    database?: {
      status: string;
      engine?: string;
      latency_ms?: number;
      pool_size?: number;
      detail?: string;
      note?: string;
    };
    redis?: {
      status: string;
      detail?: string;
      note?: string;
    };
  };
}

export interface AnalyticalModule {
  id: string;
  number: number;
  title: string;
  category: "In-Season" | "Match & Venue" | "Player Performance" | "Talent & Scouting" | "Auction & Roster" | "Core Science";
  stage: number;
  status: "Stage 0 Initialized" | "Stage 1 Active" | "Data integration pending";
  description: string;
}

export interface NavItem {
  title: string;
  href: string;
  iconName: string;
  badge?: string;
  disabled?: boolean;
}

export interface CricketDataSource {
  source_id: string;
  name: string;
  tier: "TIER_1" | "TIER_2" | "TIER_3" | "TIER_4";
  category: string;
  status: string;
  update_frequency: string;
  access_method: string;
  licensing: {
    license_name: string;
    commercial_use_permitted: boolean;
    attribution_required: boolean;
    attribution_text?: string;
  };
  reliability_assessment: string;
}

export interface CompetitionCoverageItem {
  competition_id: string;
  competition_name: string;
  season: string;
  total_scheduled_matches?: number;
  matches_acquired: number;
  ball_by_ball_available: number;
  scorecards_available: number;
  squads_available: boolean;
  status: "ACQUIRED" | "PARTIALLY_ACQUIRED" | "UNAVAILABLE" | "MANUALLY_SUPPLIED";
  data_gaps: string[];
}

export interface CoverageReportData {
  generated_at: string;
  primary_season: string;
  competitions: CompetitionCoverageItem[];
  total_matches_acquired: number;
  total_deliveries_indexed: number;
  total_players_registered: number;
  sources_active: number;
}

export interface IngestionRunData {
  run_id: string;
  source_id: string;
  competition_id: string;
  season: string;
  status: "PENDING" | "IN_PROGRESS" | "COMPLETED" | "FAILED" | "PARTIALLY_COMPLETED";
  started_at: string;
  completed_at?: string;
  duration_seconds?: number;
  validation?: {
    total_records: number;
    valid_records: number;
    rejected_records: number;
    warning_count: number;
    completeness_percentage: number;
    passed: boolean;
  };
  idempotent_skips: number;
  metadata?: {
    matches_processed?: number;
    deliveries_indexed?: number;
  };
}

export interface DatasetManifestData {
  dataset_id: string;
  competition_id: string;
  season: string;
  source_id: string;
  version: string;
  created_at: string;
  total_matches: number;
  total_deliveries: number;
  validation_status: string;
  completeness_percentage: number;
}

// --- Stage 2: Uncapped Players, Eligibility & Analytics ---

export type EligibilityStatus =
  | "CONFIRMED_UNCAPPED"
  | "SUSPECTED_CAPPED"
  | "INELIGIBLE_OVERAGE"
  | "PENDING_VERIFICATION"
  | "FLAGGED_CONFLICT";

export type ScoutingTier =
  | "TARGET_A_LIST"
  | "WATCHLIST_HIGH"
  | "MONITOR"
  | "BACKUP";

export interface IdentityItem {
  source_name: string;
  external_player_id: string;
  confidence_score: number;
}

export interface UncappedPlayerSummary {
  id: string;
  canonical_id: string;
  full_name: string;
  known_as?: string;
  dob?: string;
  calculated_age?: number;
  home_state_association?: string;
  primary_role?: string;
  batting_hand?: string;
  bowling_style?: string;
  is_capped: boolean;
  eligibility_status: EligibilityStatus;
  scouting_tier: ScoutingTier;
  is_rr_trialist: boolean;
}

export interface UncappedPlayerDetail extends UncappedPlayerSummary {
  identities: IdentityItem[];
  dob_source?: string;
  dob_verified: boolean;
  verification_notes?: string;
  reference_date_used?: string;
  created_at: string;
}

export interface PhaseMetrics {
  phase: string;
  runs: number;
  balls: number;
  wickets: number;
  strike_rate: number;
  economy_rate: number;
  boundary_percentage: number;
  dot_ball_percentage: number;
}

export interface BattingAggregates {
  player_id: string;
  innings_count: number;
  runs: number;
  balls_faced: number;
  fours: number;
  sixes: number;
  strike_rate: number;
  batting_average?: number;
  dismissals: number;
  dot_balls: number;
  dot_ball_percentage: number;
  boundary_percentage: number;
  high_score: number;
  phase_splits: Record<string, PhaseMetrics>;
}

export interface BowlingAggregates {
  player_id: string;
  innings_count: number;
  overs: number;
  legal_balls: number;
  runs_conceded: number;
  wickets: number;
  economy_rate: number;
  bowling_average?: number;
  bowling_strike_rate?: number;
  dot_balls: number;
  dot_ball_percentage: number;
  phase_splits: Record<string, PhaseMetrics>;
}

export interface MatchScorecardItem {
  match_id: string;
  match_date: string;
  opposition_team: string;
  venue_name: string;
  runs_or_wickets_display: string;
  strike_rate_or_economy: number;
}

export interface RecentFormWindow {
  player_id: string;
  window_size: number;
  innings_evaluated: number;
  aggregate_metric_summary: string;
  recent_matches: MatchScorecardItem[];
}

export interface ColumnMappingConfig {
  name_col: string;
  external_id_col?: string;
  dob_col?: string;
  state_association_col?: string;
  primary_role_col?: string;
  batting_hand_col?: string;
  bowling_style_col?: string;
  technical_rating_col?: string;
  potential_rating_col?: string;
  confidential_notes_col?: string;
  is_trialist_col?: string;
}

export interface SchemaDiscoveryResult {
  detected_columns: string[];
  sample_row_count: number;
  recommended_mapping: ColumnMappingConfig;
  column_type_hints: Record<string, string>;
  unmapped_columns: string[];
}

export interface RRDataPackIngestionSummary {
  dataset_key: string;
  total_rows_parsed: number;
  players_created: number;
  players_matched_existing: number;
  conflicts_detected: number;
  missing_dob_count: number;
  evaluations_recorded: number;
  conflict_reports: Array<{ row_index: number; player_name: string; conflicts: string[] }>;
  missing_field_reports: Array<{ row_index: number; player_name: string; missing_field: string; action_taken: string }>;
  data_classification: string;
}

export interface EvaluationItem {
  id: string;
  uncapped_profile_id: string;
  scout_identifier: string;
  evaluation_date: string;
  competition_or_trial: string;
  technical_skill_rating: number;
  temperament_rating: number;
  athleticism_rating: number;
  tactical_iq_rating: number;
  ceiling_potential_rating: number;
  strengths_summary: string;
  development_areas: string;
  scout_recommendation: string;
  proprietary_notes?: string;
  data_classification: string;
}
