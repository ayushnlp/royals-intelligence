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

export interface UploadDatasetResponse {
  status: string;
  message: string;
  filename: string;
  size_bytes: number;
  sha256_hash: string;
  competition_id: string;
  season: string;
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
export interface DomesticSeasonSummary {
  season: string;
  label: string;
  has_data: boolean;
  competition_count: number;
  total_matches: number;
  competitions: string[];
}

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
  statistical_coverage_status?: string;
  data_note?: string;
}

export interface DomesticPlayerSummary {
  canonical_id: number;
  player_id: string;
  player_name: string;
  canonical_key?: string;
  eligibility_status: string;
  is_uncapped: boolean;
  role?: string;
  team?: string;
  batting_style?: string;
  bowling_style?: string;
  caps_count: number;
  match_count: number;
  statistical_coverage_status: string;
  notes?: string;
}

export interface PaginatedDomesticPlayersResponse {
  items: DomesticPlayerSummary[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
  filters_applied?: Record<string, any>;
}


// --- Stage 4: Venue, Pitch & Weather Intelligence Interfaces ---

export interface BoundaryDimensions {
  straight_m?: number;
  off_boundary_m?: number;
  leg_boundary_m?: number;
  dimension_source?: string;
  is_verified: boolean;
  status: string; // 'VERIFIED', 'PARTIALLY_AVAILABLE', 'UNAVAILABLE'
}

export interface VenueSummaryItem {
  venue_id: string;
  venue_code: string;
  name: string;
  city: string;
  state?: string;
  country: string;
  is_rr_home: boolean;
  rr_venue_type: string;
  latitude?: number;
  longitude?: number;
  coordinates_source?: string;
  altitude_m?: number;
  pitch_soil_type?: string;
  matches_hosted_count: number;
  competitions_hosted: string[];
  data_completeness_pct: number;
}

export interface VenueDetailResponse {
  venue_id: string;
  venue_code: string;
  name: string;
  city: string;
  state?: string;
  country: string;
  is_rr_home: boolean;
  rr_venue_type: string;
  latitude?: number;
  longitude?: number;
  coordinates_source?: string;
  altitude_m?: number;
  pitch_soil_type?: string;
  aliases: string[];
  boundary_dimensions: BoundaryDimensions;
  surface_details: Record<string, any>;
  stadium_capacity?: number;
  floodlights_certified: boolean;
  matches_hosted_count: number;
  competitions_hosted: string[];
  provenance: Record<string, any>;
}

export interface VenueScoringTrendsResponse {
  venue_code: string;
  venue_name: string;
  matches_evaluated: number;
  date_range_evaluated: string;
  avg_first_innings_score: number;
  avg_second_innings_score: number;
  highest_total_recorded: number;
  highest_total_match?: string;
  lowest_total_recorded: number;
  lowest_total_match?: string;
  toss_decision_stats: Record<string, number>;
  match_outcome_by_innings: Record<string, number>;
  avg_wickets_per_innings: number;
  phase_scoring_rates: Record<string, number>;
  sample_size_confidence: string;
  sample_size_warning?: string;
  is_fallback_data: boolean;
}

export interface PitchEvidenceAnalysisResponse {
  venue_code: string;
  venue_name: string;
  pitch_soil_type: string;
  observed_pace_vs_spin: {
    pace_wickets_share_pct: number;
    spin_wickets_share_pct: number;
    pace_economy: number;
    spin_economy: number;
    pace_average?: number;
    spin_average?: number;
    pace_strike_rate?: number;
    spin_strike_rate?: number;
  };
  boundary_patterns: {
    boundary_runs_pct: number;
    fours_per_match: number;
    sixes_per_match: number;
  };
  dot_ball_patterns: {
    dot_ball_pct: number;
  };
  wickets_per_match: number;
  conditions_evidence_classification: string;
  observed_statistical_summary: string;
  expert_reported_summary?: string;
  sample_matches_evaluated: number;
  deliveries_evaluated: number;
  date_range_evaluated: string;
  evidence_confidence: string;
  limitations_disclaimer: string;
  is_fallback_data: boolean;
}

export interface WeatherObservationItem {
  venue_code: string;
  observation_time: string;
  phase_in_match: string;
  temperature_c: number;
  relative_humidity_pct: number;
  dew_point_c: number;
  dew_severity_risk: string;
  precipitation_mm: number;
  wind_speed_kph: number;
  wind_direction_deg: number;
  wind_direction_compass: string;
  cloud_cover_pct: number;
  weather_condition: string;
  is_forecast: boolean;
  source_attribution: string;
  retrieval_timestamp: string;
  reliability: string;
}

export interface MatchWeatherContextResponse {
  match_id: string;
  match_date: string;
  venue_code: string;
  venue_name: string;
  is_night_match: boolean;
  observations: WeatherObservationItem[];
  dew_impact_assessment: string;
  temperature_swing_c?: number;
  humidity_swing_pct?: number;
  historical_scoring_context: Record<string, any>;
  pitch_evidence_summary: string;
  provenance: Record<string, any>;
}

export interface WeatherSourceStatusResponse {
  source_id: string;
  source_name: string;
  tier: string;
  status: string;
  is_accessible: boolean;
  licensing: Record<string, string>;
  api_endpoint: string;
  rate_limit_policy: string;
  cached_records_count: number;
  last_verified_timestamp: string;
}

export interface UncappedPlayerVenuePerformanceResponse {
  player_id: string;
  player_name: string;
  is_uncapped: boolean;
  eligibility_status: string;
  venue_code: string;
  venue_name: string;
  matches_at_venue: number;
  batting_at_venue: Record<string, any>;
  bowling_at_venue: Record<string, any>;
  sample_size_confidence: string;
  sample_size_warning?: string;
  role_archetype: string;
}

// ===========================================================================
// STAGE 5: TACTICAL CRICKET INTELLIGENCE API CONTRACTS
// ===========================================================================

export interface TacticalDatasetSummaryResponse {
  total_deliveries: number;
  legal_deliveries: number;
  total_matches_with_deliveries: number;
  total_unique_strikers: number;
  total_unique_bowlers: number;
  total_runs_off_bat: number;
  total_wickets_fallen: number;
  total_bowler_wickets: number;
  overall_run_rate_per_6_balls: number;
  valid_radar_speed_records: number;
  data_provenance: string;
  generated_at: string;
}

export interface TacticalPhaseSplitItem {
  phase: string;
  total_balls: number;
  legal_balls: number;
  runs: number;
  wickets: number;
  strike_rate?: number | null;
  economy_rate?: number | null;
  average?: number | null;
  dot_ball_percentage: number;
  boundary_percentage: number;
  balls_per_wicket?: number | null;
}

export interface TacticalPhaseResponse {
  striker_id?: number | null;
  striker_name?: string | null;
  bowler_id?: number | null;
  bowler_name?: string | null;
  phases: Record<string, TacticalPhaseSplitItem>;
  data_provenance: string;
}

export interface TacticalStrokeItem {
  stroke: string;
  deliveries_faced: number;
  runs_scored: number;
  dismissals: number;
  runs_per_shot: number;
  dismissal_rate_pct: number;
  boundary_pct: number;
}

export interface TacticalStrokesResponse {
  striker_id?: number | null;
  striker_name?: string | null;
  total_strokes_analyzed: number;
  strokes: TacticalStrokeItem[];
  data_provenance: string;
}

export interface HandednessSplitItem {
  batting_type: string;
  pace_or_spin: string;
  balls_faced: number;
  runs_scored: number;
  wickets: number;
  strike_rate: number;
  economy_rate: number;
  bowling_average?: number | null;
  boundary_pct: number;
  dot_pct: number;
}

export interface HandednessMatrixResponse {
  striker_id?: number | null;
  striker_name?: string | null;
  bowler_id?: number | null;
  bowler_name?: string | null;
  matrix: HandednessSplitItem[];
  data_provenance: string;
}

export interface DeliveryStyleItem {
  delivery_style: string;
  deliveries_bowled: number;
  runs_conceded: number;
  wickets: number;
  dot_balls: number;
  economy_rate: number;
  bowling_average?: number | null;
  dot_ball_pct: number;
}

export interface DeliveryStylesResponse {
  bowler_id?: number | null;
  bowler_name?: string | null;
  total_styles_analyzed: number;
  styles: DeliveryStyleItem[];
  data_provenance: string;
}

export interface SpeedBrackets {
  slow_under_110: number;
  medium_110_to_125: number;
  fast_medium_125_to_140: number;
  express_over_140: number;
}

export interface FastestBowlerItem {
  bowler_id: number;
  bowler_name: string;
  valid_deliveries: number;
  mean_speed_kmh: number;
  max_speed_kmh: number;
  express_balls_count: number;
}

export interface SpeedProfileResponse {
  bowler_id?: number | null;
  bowler_name?: string | null;
  total_deliveries?: number | null;
  overall_valid_speed_deliveries?: number | null;
  valid_speed_deliveries?: number | null;
  speed_coverage_pct: number;
  mean_speed_kmh?: number | null;
  median_speed_kmh?: number | null;
  min_speed_kmh?: number | null;
  max_speed_kmh?: number | null;
  std_speed_kmh?: number | null;
  speed_brackets?: SpeedBrackets | null;
  top_fastest_bowlers?: FastestBowlerItem[] | null;
  sensor_safeguards_applied: boolean;
  data_quality_note: string;
  data_provenance: string;
}

export interface PlayerTacticalProfileResponse {
  player_id: number;
  player_name: string;
  is_batter: boolean;
  is_bowler: boolean;
  batting_profile?: {
    total_runs: number;
    balls_faced: number;
    strike_rate: number;
    fours: number;
    sixes: number;
    boundary_pct: number;
    dot_ball_pct: number;
    phase_splits: Record<string, TacticalPhaseSplitItem>;
    top_strokes: TacticalStrokeItem[];
    handedness_splits: HandednessSplitItem[];
  } | null;
  bowling_profile?: {
    total_wickets: number;
    legal_balls: number;
    runs_conceded: number;
    economy_rate: number;
    bowling_average?: number | null;
    dot_ball_pct: number;
    phase_splits: Record<string, TacticalPhaseSplitItem>;
    top_variations: DeliveryStyleItem[];
    speed_profile: SpeedProfileResponse;
  } | null;
  data_provenance: string;
}

export interface DeathOverPerformerBattingItem {
  striker_id: number;
  striker_name: string;
  runs: number;
  balls: number;
  fours: number;
  sixes: number;
  strike_rate: number;
  boundary_pct: number;
  dot_pct: number;
}

export interface DeathOverPerformerBowlingItem {
  bowler_id: number;
  bowler_name: string;
  bowling_type: string;
  legal_balls: number;
  runs: number;
  wickets: number;
  economy: number;
  average?: number | null;
  dot_pct: number;
}

export interface DeathOversRankingResponse {
  discipline: string;
  min_balls_threshold: number;
  batting_finishers?: DeathOverPerformerBattingItem[] | null;
  bowling_containment?: DeathOverPerformerBowlingItem[] | null;
  data_provenance: string;
}

export interface HeadToHeadMatchupResponse {
  striker_id: number;
  striker_name: string;
  bowler_id: number;
  bowler_name: string;
  balls_faced: number;
  legal_balls: number;
  runs_scored: number;
  dismissals: number;
  fours: number;
  sixes: number;
  dot_balls: number;
  strike_rate: number;
  dot_ball_pct: number;
  boundary_pct: number;
  data_provenance: string;
}

export interface PlayerLookupItem {
  player_id: number;
  player_name: string;
  is_batter: boolean;
  is_bowler: boolean;
  total_deliveries: number;
}

// ===========================================================================
// STAGE 5 / ROUND 1: PRESSURE ANALYTICS & RELIABILITY API CONTRACTS
// ===========================================================================

export interface PressureOverviewResponse {
  challenge_title: string;
  governing_dataset: string;
  total_deliveries: number;
  legal_deliveries: number;
  matches_with_deliveries: number;
  reconciled_abandoned_matches: number;
  total_competitions: number;
  strict_pressure_bowling_balls: number;
  strict_pressure_batting_balls: number;
  permissive_pressure_bowling_balls: number;
  permissive_pressure_batting_balls: number;
  death_overs_bowling_pressure_share_pct: number;
  death_overs_batting_pressure_share_pct: number;
  total_evaluated_batters: number;
  total_evaluated_bowlers: number;
  sample_qualification_threshold: string;
  governing_ranking_methodology: string;
  data_provenance: string;
}

export interface PressureLeaderboardBattingItem {
  rank: number;
  player_id: number;
  player_name: string;
  discipline: string;
  is_qualified: boolean;
  qualification_status: string;
  conservative_pri: number;
  posterior_mean: number;
  posterior_se: number;
  ci_95_lower: number;
  ci_95_upper: number;
  ci_95_width: number;
  shrinkage_weight: number;
  prob_exceed_baseline: number;
  prob_exceed_league_mean: number;
  observed_strike_rate: number;
  expected_strike_rate: number;
  diff_strike_rate: number;
  observed_boundary_pct: number;
  diff_boundary_pct: number;
  observed_dot_pct: number;
  diff_dot_pct: number;
  observed_dismissal_pct: number;
  diff_dismissal_pct: number;
  pressure_legal_balls: number;
  pressure_matches: number;
  pressure_seasons: number;
  ipl_legal_balls: number;
  t20i_legal_balls: number;
  competition_qualification: string;
  uncertainty_level: string;
  evidence_volume_tier: string;
  evidence_classification: string;
  two_dimensional_classification: string;
  explainability_summary: string;
}

export interface PressureLeaderboardBowlingItem {
  rank: number;
  player_id: number;
  player_name: string;
  discipline: string;
  is_qualified: boolean;
  qualification_status: string;
  conservative_runs_saved: number;
  posterior_mean: number;
  posterior_se: number;
  ci_95_lower: number;
  ci_95_upper: number;
  ci_95_width: number;
  shrinkage_weight: number;
  prob_exceed_baseline: number;
  prob_exceed_league_mean: number;
  observed_economy: number;
  expected_economy: number;
  diff_economy: number;
  observed_wicket_pct: number;
  diff_wicket_pct: number;
  observed_dot_pct: number;
  diff_dot_pct: number;
  observed_boundary_pct: number;
  diff_boundary_pct: number;
  pressure_legal_balls: number;
  pressure_matches: number;
  pressure_seasons: number;
  ipl_legal_balls: number;
  t20i_legal_balls: number;
  competition_qualification: string;
  uncertainty_level: string;
  evidence_volume_tier: string;
  evidence_classification: string;
  two_dimensional_classification: string;
  explainability_summary: string;
}

export interface PressureLeaderboardResponse {
  discipline_filter: string;
  qualified_only: boolean;
  batting_count: number;
  bowling_count: number;
  batting_leaderboard?: PressureLeaderboardBattingItem[] | null;
  bowling_leaderboard?: PressureLeaderboardBowlingItem[] | null;
  data_provenance: string;
}

export interface CandidateEvidenceQuestions {
  q1_why_considered: string;
  q2_pressure_deliveries: string;
  q3_matches_and_seasons: string;
  q4_observed_performance: string;
  q5_expected_performance: string;
  q6_conservative_diagnostic: string;
  q7_posterior_uncertainty: string;
  q8_credible_interval: string;
  q9_competition_support: string;
  q10_major_limitations: string;
  q11_sensitivity_to_assumptions: string;
}

export interface CandidateEvidenceProfileResponse {
  player_id: number;
  player_name: string;
  discipline: string;
  rank: number;
  governing_metric_name: string;
  governing_metric_value: number;
  posterior_mean: number;
  posterior_se: number;
  ci_95_lower: number;
  ci_95_upper: number;
  ci_95_width: number;
  shrinkage_weight: number;
  pressure_legal_balls: number;
  pressure_matches: number;
  ipl_legal_balls: number;
  t20i_legal_balls: number;
  competition_qualification: string;
  two_dimensional_classification: string;
  evidence_classification: string;
  uncertainty_level: string;
  evidence_questions: CandidateEvidenceQuestions;
  data_provenance: string;
}

export interface PressureMethodologyResponse {
  challenge_objective: string;
  pressure_definition: Record<string, any>;
  baseline_strata_12_cell: string[];
  bayesian_shrinkage_formulation: Record<string, string>;
  conservative_pri_formula: Record<string, string>;
  qualification_criteria: Record<string, any>;
  limitations: string[];
  data_provenance: string;
}

// ---------------------------------------------------------------------------
// Uncapped Player Intelligence Types
// ---------------------------------------------------------------------------

export interface UncappedBattingItem {
  uncapped_rank: number;
  overall_r1_rank: number;
  player_id: number;
  player_name: string;
  franchise: string;
  tactical_role: string;
  conservative_pri: number;
  posterior_mean: number;
  posterior_se: number;
  ci_95_lower: number;
  ci_95_upper: number;
  pressure_legal_balls: number;
  pressure_matches: number;
  observed_strike_rate: number;
  observed_boundary_pct: number;
  observed_dot_pct: number;
  eligibility_status: string;
  eligibility_reason: string;
  verification_source: string;
  verification_date: string;
  is_official_r1_qualified?: boolean;
  meets_active_gate?: boolean;
}

export interface UncappedBowlingItem {
  uncapped_rank: number;
  overall_r1_rank: number;
  player_id: number;
  player_name: string;
  franchise: string;
  tactical_role: string;
  conservative_runs_saved: number;
  posterior_mean: number;
  posterior_se: number;
  ci_95_lower: number;
  ci_95_upper: number;
  pressure_legal_balls: number;
  pressure_matches: number;
  observed_economy: number;
  observed_wicket_pct: number;
  observed_dot_pct: number;
  eligibility_status: string;
  eligibility_reason: string;
  verification_source: string;
  verification_date: string;
  is_official_r1_qualified?: boolean;
  meets_active_gate?: boolean;
}

export interface UncappedLeaderboardResponse {
  discipline_filter: string;
  qualified_only: boolean;
  batting_count: number;
  bowling_count: number;
  batting_leaderboard: UncappedBattingItem[] | null;
  bowling_leaderboard: UncappedBowlingItem[] | null;
  sample_gate: string;
  governing_statute: string;
  audit_date: string;
  min_balls_applied?: number;
  min_matches_applied?: number;
  is_exploratory_filter?: boolean;
  excluded_count?: number;
  total_pool_count?: number;
}

export interface UncappedOverviewResponse {
  total_verified_uncapped_batters: number;
  total_verified_uncapped_bowlers: number;
  top_uncapped_batter: string | null;
  top_uncapped_bowler: string | null;
  sample_gate_applied: string;
  governing_statute: string;
  audit_date: string;
  min_balls_applied?: number;
  min_matches_applied?: number;
  is_exploratory_filter?: boolean;
  total_pool_batters?: number;
  total_pool_bowlers?: number;
  excluded_batters_count?: number;
  excluded_bowlers_count?: number;
}


