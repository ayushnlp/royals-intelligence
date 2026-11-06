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
  status: "Stage 0 Initialized" | "Data integration pending";
  description: string;
}

export interface NavItem {
  title: string;
  href: string;
  iconName: string;
  badge?: string;
  disabled?: boolean;
}
