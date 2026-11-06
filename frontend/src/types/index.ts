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
