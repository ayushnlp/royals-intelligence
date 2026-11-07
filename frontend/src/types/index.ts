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

// Stage 3 Domestic Season & Match Intelligence Interfaces
export interface CompetitionSeasonSummary {
  competition_id: string;
  competition_name: string;
  competition_type: string;
  governing_body: string;
  season: string;
  is_domestic: boolean;
  match_count: number;
  teams_count: number;
  participating_teams: string[];
  has_ball_by_ball: boolean;
  validation_pass_rate: number;
  completeness_percentage: number;
  source_reference: string;
}

export interface MatchSummaryItem {
  match_id: string;
  external_match_id: string;
  competition_id: string;
  season: string;
  match_date: string;
  match_number?: number;
  home_team_code: string;
  home_team_name: string;
  away_team_code: string;
  away_team_name: string;
  venue_name: string;
  venue_city: string;
  winner_team_code?: string;
  win_margin?: string;
  result_outcome: string;
  has_ball_by_ball: boolean;
}

export interface BattingScorecardRow {
  player_id: string;
  player_name: string;
  is_uncapped: boolean;
  batting_position: number;
  runs: number;
  balls_faced: number;
  fours: number;
  sixes: number;
  strike_rate: number;
  is_out: boolean;
  dismissal_kind?: string;
  bowler_name?: string;
  fielder_name?: string;
  dot_balls?: number;
  powerplay_runs?: number;
  powerplay_balls?: number;
  middle_runs?: number;
  middle_balls?: number;
  death_runs?: number;
  death_balls?: number;
}

export interface BowlingScorecardRow {
  player_id: string;
  player_name: string;
  is_uncapped: boolean;
  overs: number;
  legal_balls: number;
  maidens: number;
  runs_conceded: number;
  bowler_wickets: number;
  economy_rate: number;
  dot_balls?: number;
  wides: number;
  noballs: number;
  powerplay_overs?: number;
  powerplay_wickets?: number;
  powerplay_runs?: number;
  death_overs?: number;
  death_wickets?: number;
  death_runs?: number;
}

export interface FallOfWicketItem {
  wicket_number: number;
  runs: number;
  over_display: number;
  batter_out_name: string;
  batter_out_id?: string;
}

export interface PartnershipItem {
  wicket_number: number;
  runs: number;
  balls: number;
  batter_1_name: string;
  batter_1_runs: number;
  batter_1_balls: number;
  batter_2_name: string;
  batter_2_runs: number;
  batter_2_balls: number;
  is_unbroken: boolean;
}

export interface PhaseSummaryMetrics {
  phase_name: string;
  overs_range: string;
  runs: number;
  wickets: number;
  run_rate: number;
  dot_ball_percentage?: number;
  boundary_runs: number;
}

export interface OverProgressionItem {
  over_number: number;
  runs_in_over: number;
  cumulative_runs: number;
  wickets_in_over: number;
  cumulative_wickets: number;
}

export interface InningsAnalysisResponse {
  match_id: string;
  innings_number: number;
  batting_team_code: string;
  batting_team_name: string;
  bowling_team_code: string;
  bowling_team_name: string;
  total_runs: number;
  wickets: number;
  overs_completed: number;
  run_rate: number;
  extras_total: number;
  extras_breakdown: Record<string, number>;
  batting_scorecards: BattingScorecardRow[];
  bowling_scorecards: BowlingScorecardRow[];
  fall_of_wickets: FallOfWicketItem[];
  partnerships: PartnershipItem[];
  phase_summaries: PhaseSummaryMetrics[];
  scoring_progression: OverProgressionItem[];
}

export interface MatchScorecardResponse {
  match_id: string;
  external_match_id: string;
  competition_id: string;
  competition_name: string;
  competition_type: string;
  season: string;
  match_date: string;
  venue_name: string;
  venue_city: string;
  pitch_soil_type?: string;
  home_team: { team_code: string; name: string };
  away_team: { team_code: string; name: string };
  toss_winner_code?: string;
  toss_decision?: string;
  winner_team_code?: string;
  win_margin?: string;
  player_of_match?: string;
  innings: InningsAnalysisResponse[];
  data_provenance: Record<string, any>;
}

export interface PlayerDomesticSeasonStats {
  competition_id: string;
  competition_name: string;
  competition_type: string;
  season: string;
  team_name: string;
  matches: number;
  innings_batted: number;
  runs: number;
  balls_faced: number;
  not_outs: number;
  batting_average?: number;
  strike_rate: number;
  fours: number;
  sixes: number;
  boundary_percentage: number;
  dot_ball_percentage?: number;
  balls_per_boundary?: number;
  high_score: number;
  high_score_not_out: boolean;
  scores_30_plus: number;
  fifties: number;
  hundreds: number;
  innings_bowled: number;
  overs_bowled: number;
  legal_balls: number;
  maidens: number;
  runs_conceded: number;
  bowler_wickets: number;
  bowling_average?: number;
  bowling_economy: number;
  bowling_strike_rate?: number;
  dot_balls_bowled?: number;
  catches: number;
  run_outs: number;
}

export interface PlayerMatchHistoryItem {
  match_id: string;
  match_date: string;
  competition_id: string;
  competition_name: string;
  season: string;
  opponent_team: string;
  venue_name: string;
  role_in_match: string;
  batting_runs?: number;
  batting_balls?: number;
  batting_strike_rate?: number;
  is_out?: boolean;
  dismissal_kind?: string;
  bowling_overs?: number;
  bowling_maidens?: number;
  bowling_runs?: number;
  bowler_wickets?: number;
  bowling_economy?: number;
  catches: number;
  run_outs: number;
  is_player_of_match: boolean;
}

export interface PlayerPhaseSplitDetail {
  phase: string;
  overs_range: string;
  batting_runs: number;
  batting_balls: number;
  batting_strike_rate: number;
  batting_fours: number;
  batting_sixes: number;
  batting_dot_percentage?: number;
  batting_dismissals: number;
  bowling_overs: number;
  bowling_legal_balls: number;
  bowling_runs_conceded: number;
  bowler_wickets: number;
  bowling_economy: number;
  bowling_dot_percentage?: number;
}

export interface AllRoundContributionResponse {
  player_id: string;
  full_name: string;
  canonical_id: string;
  eligibility_status: string;
  primary_role: string;
  domestic_team?: string;
  sample_size: {
    matches: number;
    innings_batted: number;
    innings_bowled: number;
    overs_bowled: number;
  };
  batting_summary: Record<string, any>;
  bowling_summary: Record<string, any>;
  fielding_summary: Record<string, any>;
  role_archetype_context: string;
  has_sufficient_sample: boolean;
}
