import {
  SystemHealth,
  CompetitionSeasonSummary,
  MatchSummaryItem,
  InningsAnalysisResponse,
  MatchScorecardResponse,
  PlayerDomesticSeasonStats,
  PlayerMatchHistoryItem,
  PlayerPhaseSplitDetail,
  AllRoundContributionResponse,
  VenueSummaryItem,
  VenueDetailResponse,
  VenueScoringTrendsResponse,
  PitchEvidenceAnalysisResponse,
  WeatherObservationItem,
  MatchWeatherContextResponse,
  WeatherSourceStatusResponse,
  UncappedPlayerVenuePerformanceResponse,
  TacticalDatasetSummaryResponse,
  TacticalPhaseResponse,
  TacticalStrokesResponse,
  HandednessMatrixResponse,
  DeliveryStylesResponse,
  SpeedProfileResponse,
  PlayerTacticalProfileResponse,
  DeathOversRankingResponse,
  HeadToHeadMatchupResponse,
  PlayerLookupItem,
  PressureOverviewResponse,
  PressureLeaderboardResponse,
  CandidateEvidenceProfileResponse,
  PressureMethodologyResponse,
} from "@/types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export async function fetchSystemHealth(): Promise<SystemHealth> {
  try {
    const res = await fetch(`${API_BASE_URL}/health`, {
      cache: "no-store",
    });
    if (!res.ok) {
      throw new Error(`HTTP error! status: ${res.status}`);
    }
    return await res.json();
  } catch (error) {
    return {
      status: "degraded_standby",
      project: "Royals Intelligence",
      version: "0.1.0-stage0",
      environment: process.env.NEXT_PUBLIC_ENVIRONMENT || "development",
      timestamp: new Date().toISOString(),
      components: {
        database: {
          status: "standby_offline",
          engine: "postgresql+asyncpg",
          note: "Backend API offline or database initialization pending.",
        },
        redis: {
          status: "standby",
          note: "Task queue broker standby.",
        },
      },
    };
  }
}

export async function fetchSources() {
  try {
    const res = await fetch(`${API_BASE_URL}/acquisition/sources`, { cache: "no-store" });
    if (!res.ok) throw new Error("Failed to fetch sources");
    return await res.json();
  } catch (e) {
    return [];
  }
}

export async function fetchCoverage() {
  try {
    const res = await fetch(`${API_BASE_URL}/acquisition/coverage`, { cache: "no-store" });
    if (!res.ok) throw new Error("Failed to fetch coverage");
    return await res.json();
  } catch (e) {
    return null;
  }
}

export async function fetchIngestionRuns() {
  try {
    const res = await fetch(`${API_BASE_URL}/acquisition/runs`, { cache: "no-store" });
    if (!res.ok) throw new Error("Failed to fetch runs");
    return await res.json();
  } catch (e) {
    return [];
  }
}

export async function fetchDatasets() {
  try {
    const res = await fetch(`${API_BASE_URL}/acquisition/datasets`, { cache: "no-store" });
    if (!res.ok) throw new Error("Failed to fetch datasets");
    return await res.json();
  } catch (e) {
    return [];
  }
}

// --- Stage 2: Uncapped Players & Analytics API ---

export async function fetchUncappedPlayers(params?: {
  eligibility?: string;
  tier?: string;
  role?: string;
  state?: string;
  trialist_only?: boolean;
}) {
  try {
    const searchParams = new URLSearchParams();
    if (params?.eligibility) searchParams.append("eligibility", params.eligibility);
    if (params?.tier) searchParams.append("tier", params.tier);
    if (params?.role) searchParams.append("role", params.role);
    if (params?.state) searchParams.append("state", params.state);
    if (params?.trialist_only) searchParams.append("trialist_only", "true");

    const qs = searchParams.toString();
    const url = `${API_BASE_URL}/players${qs ? `?${qs}` : ""}`;
    const res = await fetch(url, { cache: "no-store" });
    if (!res.ok) throw new Error("Failed to fetch uncapped players");
    return await res.json();
  } catch (e) {
    return [];
  }
}

export async function fetchUncappedPlayerDetail(playerId: string) {
  try {
    const res = await fetch(`${API_BASE_URL}/players/${playerId}`, { cache: "no-store" });
    if (!res.ok) throw new Error("Failed to fetch player detail");
    return await res.json();
  } catch (e) {
    return null;
  }
}

// Client-side authentication token for Rajasthan Royals scout administrator operations
const SCOUT_ADMIN_TOKEN = process.env.NEXT_PUBLIC_SCOUT_ADMIN_TOKEN || "rr_scout_admin_secret_token_2026";

export async function verifyPlayerEligibility(
  playerId: string,
  payload: { new_status: string; verification_notes: string; verified_by?: string }
) {
  const res = await fetch(`${API_BASE_URL}/players/${playerId}/verify-eligibility`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${SCOUT_ADMIN_TOKEN}`,
    },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error("Failed to verify eligibility");
  return await res.json();
}

export async function fetchPlayerBatting(playerId: string) {
  try {
    const res = await fetch(`${API_BASE_URL}/analytics/players/${playerId}/batting`, { cache: "no-store" });
    if (!res.ok) throw new Error("Failed to fetch batting analytics");
    return await res.json();
  } catch (e) {
    return null;
  }
}

export async function fetchPlayerBowling(playerId: string) {
  try {
    const res = await fetch(`${API_BASE_URL}/analytics/players/${playerId}/bowling`, { cache: "no-store" });
    if (!res.ok) throw new Error("Failed to fetch bowling analytics");
    return await res.json();
  } catch (e) {
    return null;
  }
}

export async function fetchPlayerRecentForm(playerId: string, lastN: number = 5, discipline: string = "batting") {
  try {
    const res = await fetch(
      `${API_BASE_URL}/analytics/players/${playerId}/recent-form?last_n=${lastN}&discipline=${discipline}`,
      { cache: "no-store" }
    );
    if (!res.ok) throw new Error("Failed to fetch recent form");
    return await res.json();
  } catch (e) {
    return null;
  }
}

export async function discoverProprietarySchema(sampleRows: any[]) {
  const res = await fetch(`${API_BASE_URL}/proprietary/discover-schema`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${SCOUT_ADMIN_TOKEN}`,
    },
    body: JSON.stringify({ sample_rows: sampleRows }),
  });
  if (!res.ok) throw new Error("Failed to discover schema");
  return await res.json();
}

export async function ingestProprietaryPack(payload: {
  records: any[];
  column_mapping?: any;
  dataset_key?: string;
}) {
  const res = await fetch(`${API_BASE_URL}/proprietary/ingest-pack`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${SCOUT_ADMIN_TOKEN}`,
    },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error("Failed to ingest proprietary pack");
  return await res.json();
}

export async function fetchPlayerEvaluations(playerId: string, userRole: string = "public") {
  try {
    const headers: Record<string, string> = {};
    if (userRole === "rr_scout_admin") {
      headers["Authorization"] = `Bearer ${SCOUT_ADMIN_TOKEN}`;
    }
    const res = await fetch(`${API_BASE_URL}/proprietary/evaluations/${playerId}`, {
      headers,
      cache: "no-store",
    });
    if (!res.ok) throw new Error("Failed to fetch evaluations");
    return await res.json();
  } catch (e) {
    return [];
  }
}

// --- Stage 3: Domestic Season and Match Intelligence API ---

export async function fetchDomesticCompetitions(): Promise<CompetitionSeasonSummary[]> {
  try {
    const res = await fetch(`${API_BASE_URL}/domestic/competitions`, { cache: "no-store" });
    if (!res.ok) throw new Error("Failed to fetch domestic competitions");
    return await res.json();
  } catch (e) {
    return [];
  }
}

export async function fetchSeasonMatches(
  competitionId: string,
  season: string,
  params?: { team?: string; page?: number; page_size?: number }
): Promise<{ total: number; page: number; page_size: number; matches: MatchSummaryItem[] }> {
  try {
    const searchParams = new URLSearchParams();
    if (params?.team) searchParams.append("team", params.team);
    if (params?.page) searchParams.append("page", String(params.page));
    if (params?.page_size) searchParams.append("page_size", String(params.page_size));

    const qs = searchParams.toString();
    const url = `${API_BASE_URL}/domestic/seasons/${competitionId}/${season}/matches${qs ? `?${qs}` : ""}`;
    const res = await fetch(url, { cache: "no-store" });
    if (!res.ok) throw new Error("Failed to fetch season matches");
    return await res.json();
  } catch (e) {
    return { total: 0, page: 1, page_size: 20, matches: [] };
  }
}

export async function fetchSeasonSummary(
  competitionId: string,
  season: string
): Promise<CompetitionSeasonSummary | null> {
  try {
    const res = await fetch(`${API_BASE_URL}/domestic/seasons/${competitionId}/${season}/summary`, {
      cache: "no-store",
    });
    if (!res.ok) throw new Error("Failed to fetch season summary");
    return await res.json();
  } catch (e) {
    return null;
  }
}

export async function fetchMatchScorecard(matchId: string): Promise<MatchScorecardResponse | null> {
  try {
    const res = await fetch(`${API_BASE_URL}/domestic/matches/${matchId}`, { cache: "no-store" });
    if (!res.ok) throw new Error("Failed to fetch match scorecard");
    return await res.json();
  } catch (e) {
    return null;
  }
}

export async function fetchInningsAnalysis(
  matchId: string,
  inningsNumber: number
): Promise<InningsAnalysisResponse | null> {
  try {
    const res = await fetch(`${API_BASE_URL}/domestic/matches/${matchId}/innings/${inningsNumber}`, {
      cache: "no-store",
    });
    if (!res.ok) throw new Error("Failed to fetch innings analysis");
    return await res.json();
  } catch (e) {
    return null;
  }
}

export async function fetchPlayerDomesticStats(
  playerId: string,
  competitionId?: string
): Promise<PlayerDomesticSeasonStats[]> {
  try {
    const qs = competitionId ? `?competition_id=${encodeURIComponent(competitionId)}` : "";
    const res = await fetch(`${API_BASE_URL}/domestic/players/${playerId}/season-stats${qs}`, {
      cache: "no-store",
    });
    if (!res.ok) throw new Error("Failed to fetch player domestic season stats");
    return await res.json();
  } catch (e) {
    return [];
  }
}

export async function fetchPlayerMatchHistory(
  playerId: string,
  params?: { competition_id?: string; season?: string; page?: number; page_size?: number }
): Promise<{ total: number; page: number; page_size: number; history: PlayerMatchHistoryItem[] }> {
  try {
    const searchParams = new URLSearchParams();
    if (params?.competition_id) searchParams.append("competition_id", params.competition_id);
    if (params?.season) searchParams.append("season", params.season);
    if (params?.page) searchParams.append("page", String(params.page));
    if (params?.page_size) searchParams.append("page_size", String(params.page_size));

    const qs = searchParams.toString();
    const url = `${API_BASE_URL}/domestic/players/${playerId}/match-history${qs ? `?${qs}` : ""}`;
    const res = await fetch(url, { cache: "no-store" });
    if (!res.ok) throw new Error("Failed to fetch player match history");
    return await res.json();
  } catch (e) {
    return { total: 0, page: 1, page_size: 20, history: [] };
  }
}

export async function fetchPlayerPhaseSplits(
  playerId: string,
  competitionId?: string
): Promise<PlayerPhaseSplitDetail[]> {
  try {
    const qs = competitionId ? `?competition_id=${encodeURIComponent(competitionId)}` : "";
    const res = await fetch(`${API_BASE_URL}/domestic/players/${playerId}/phase-splits${qs}`, {
      cache: "no-store",
    });
    if (!res.ok) throw new Error("Failed to fetch player phase splits");
    return await res.json();
  } catch (e) {
    return [];
  }
}

export async function fetchPlayerAllRoundSummary(
  playerId: string
): Promise<AllRoundContributionResponse | null> {
  try {
    const res = await fetch(`${API_BASE_URL}/domestic/players/${playerId}/all-round-summary`, {
      cache: "no-store",
    });
    if (!res.ok) throw new Error("Failed to fetch player all-round summary");
    return await res.json();
  } catch (e) {
    return null;
  }
}

// --- Stage 4: Venue, Pitch & Weather Intelligence API ---

export async function fetchVenues(rrOnly: boolean = false): Promise<VenueSummaryItem[]> {
  try {
    const qs = rrOnly ? "?rr_only=true" : "";
    const res = await fetch(`${API_BASE_URL}/venues${qs}`, { cache: "no-store" });
    if (!res.ok) throw new Error("Failed to fetch venues");
    return await res.json();
  } catch (e) {
    return [];
  }
}

export async function fetchVenueDetail(venueId: string): Promise<VenueDetailResponse | null> {
  try {
    const res = await fetch(`${API_BASE_URL}/venues/${venueId}`, { cache: "no-store" });
    if (!res.ok) throw new Error("Failed to fetch venue detail");
    return await res.json();
  } catch (e) {
    return null;
  }
}

export async function fetchVenueScoringTrends(venueId: string): Promise<VenueScoringTrendsResponse | null> {
  try {
    const res = await fetch(`${API_BASE_URL}/venues/${venueId}/scoring-trends`, { cache: "no-store" });
    if (!res.ok) throw new Error("Failed to fetch scoring trends");
    return await res.json();
  } catch (e) {
    return null;
  }
}

export async function fetchVenuePitchAnalysis(venueId: string): Promise<PitchEvidenceAnalysisResponse | null> {
  try {
    const res = await fetch(`${API_BASE_URL}/venues/${venueId}/pitch-analysis`, { cache: "no-store" });
    if (!res.ok) throw new Error("Failed to fetch pitch analysis");
    return await res.json();
  } catch (e) {
    return null;
  }
}

export async function fetchPlayerVenuePerformance(
  venueId: string,
  playerId: string
): Promise<UncappedPlayerVenuePerformanceResponse | null> {
  try {
    const res = await fetch(
      `${API_BASE_URL}/venues/${venueId}/player-performance?player_id=${encodeURIComponent(playerId)}`,
      { cache: "no-store" }
    );
    if (!res.ok) throw new Error("Failed to fetch player venue performance");
    return await res.json();
  } catch (e) {
    return null;
  }
}

export async function fetchMatchWeatherContext(matchId: string): Promise<MatchWeatherContextResponse | null> {
  try {
    const res = await fetch(`${API_BASE_URL}/weather/match/${matchId}`, { cache: "no-store" });
    if (!res.ok) throw new Error("Failed to fetch match weather context");
    return await res.json();
  } catch (e) {
    return null;
  }
}

export async function fetchHistoricalWeather(
  venueCode: string,
  matchDate: string
): Promise<WeatherObservationItem[]> {
  try {
    const res = await fetch(
      `${API_BASE_URL}/weather/historical?venue_code=${encodeURIComponent(venueCode)}&match_date=${encodeURIComponent(matchDate)}`,
      { cache: "no-store" }
    );
    if (!res.ok) throw new Error("Failed to fetch historical weather");
    return await res.json();
  } catch (e) {
    return [];
  }
}

export async function fetchWeatherForecast(
  venueCode: string,
  daysAhead: number = 7
): Promise<WeatherObservationItem[]> {
  try {
    const res = await fetch(
      `${API_BASE_URL}/weather/forecast?venue_code=${encodeURIComponent(venueCode)}&days_ahead=${daysAhead}`,
      { cache: "no-store" }
    );
    if (!res.ok) throw new Error("Failed to fetch weather forecast");
    return await res.json();
  } catch (e) {
    return [];
  }
}

export async function fetchWeatherSourceStatus(): Promise<WeatherSourceStatusResponse | null> {
  try {
    const res = await fetch(`${API_BASE_URL}/weather/source-status`, { cache: "no-store" });
    if (!res.ok) throw new Error("Failed to fetch weather source status");
    return await res.json();
  } catch (e) {
    return null;
  }
}

// ============================================================================
// Stage 5: Dataset-Driven Tactical Cricket Intelligence API
// ============================================================================

export async function fetchTacticalSummary(): Promise<TacticalDatasetSummaryResponse | null> {
  try {
    const res = await fetch(`${API_BASE_URL}/analytics/tactical/summary`, { cache: "no-store" });
    if (!res.ok) throw new Error("Failed to fetch tactical dataset summary");
    return await res.json();
  } catch (e) {
    return null;
  }
}

export async function fetchTacticalPhases(params?: {
  striker_id?: number;
  bowler_id?: number;
  phase?: string;
}): Promise<TacticalPhaseResponse | null> {
  try {
    const query = new URLSearchParams();
    if (params?.striker_id !== undefined) query.set("striker_id", params.striker_id.toString());
    if (params?.bowler_id !== undefined) query.set("bowler_id", params.bowler_id.toString());
    if (params?.phase) query.set("phase", params.phase);

    const queryString = query.toString();
    const url = `${API_BASE_URL}/analytics/tactical/phases${queryString ? `?${queryString}` : ""}`;
    const res = await fetch(url, { cache: "no-store" });
    if (!res.ok) throw new Error("Failed to fetch phase performance");
    return await res.json();
  } catch (e) {
    return null;
  }
}

export async function fetchTacticalStrokes(params?: {
  striker_id?: number;
  stroke?: string;
  min_balls?: number;
}): Promise<TacticalStrokesResponse | null> {
  try {
    const query = new URLSearchParams();
    if (params?.striker_id !== undefined) query.set("striker_id", params.striker_id.toString());
    if (params?.stroke) query.set("stroke", params.stroke);
    if (params?.min_balls !== undefined) query.set("min_balls", params.min_balls.toString());

    const queryString = query.toString();
    const url = `${API_BASE_URL}/analytics/tactical/strokes${queryString ? `?${queryString}` : ""}`;
    const res = await fetch(url, { cache: "no-store" });
    if (!res.ok) throw new Error("Failed to fetch stroke efficiency");
    return await res.json();
  } catch (e) {
    return null;
  }
}

export async function fetchTacticalHandedness(params?: {
  batting_type?: string;
  pace_or_spin?: string;
  striker_id?: number;
  bowler_id?: number;
}): Promise<HandednessMatrixResponse | null> {
  try {
    const query = new URLSearchParams();
    if (params?.batting_type) query.set("batting_type", params.batting_type);
    if (params?.pace_or_spin) query.set("pace_or_spin", params.pace_or_spin);
    if (params?.striker_id !== undefined) query.set("striker_id", params.striker_id.toString());
    if (params?.bowler_id !== undefined) query.set("bowler_id", params.bowler_id.toString());

    const queryString = query.toString();
    const url = `${API_BASE_URL}/analytics/tactical/handedness${queryString ? `?${queryString}` : ""}`;
    const res = await fetch(url, { cache: "no-store" });
    if (!res.ok) throw new Error("Failed to fetch handedness matrix");
    return await res.json();
  } catch (e) {
    return null;
  }
}

export async function fetchTacticalVariations(params?: {
  bowler_id?: number;
  delivery_style?: string;
  min_balls?: number;
}): Promise<DeliveryStylesResponse | null> {
  try {
    const query = new URLSearchParams();
    if (params?.bowler_id !== undefined) query.set("bowler_id", params.bowler_id.toString());
    if (params?.delivery_style) query.set("delivery_style", params.delivery_style);
    if (params?.min_balls !== undefined) query.set("min_balls", params.min_balls.toString());

    const queryString = query.toString();
    const url = `${API_BASE_URL}/analytics/tactical/variations${queryString ? `?${queryString}` : ""}`;
    const res = await fetch(url, { cache: "no-store" });
    if (!res.ok) throw new Error("Failed to fetch delivery variations");
    return await res.json();
  } catch (e) {
    return null;
  }
}

export async function fetchTacticalSpeedProfiles(params?: {
  bowler_id?: number;
  min_balls?: number;
  top_n?: number;
}): Promise<SpeedProfileResponse | null> {
  try {
    const query = new URLSearchParams();
    if (params?.bowler_id !== undefined) query.set("bowler_id", params.bowler_id.toString());
    if (params?.min_balls !== undefined) query.set("min_balls", params.min_balls.toString());
    if (params?.top_n !== undefined) query.set("top_n", params.top_n.toString());

    const queryString = query.toString();
    const url = `${API_BASE_URL}/analytics/tactical/speed-profiles${queryString ? `?${queryString}` : ""}`;
    const res = await fetch(url, { cache: "no-store" });
    if (!res.ok) throw new Error("Failed to fetch speed profiles");
    return await res.json();
  } catch (e) {
    return null;
  }
}

export async function fetchPlayerTacticalProfile(playerId: number): Promise<PlayerTacticalProfileResponse | null> {
  try {
    const res = await fetch(`${API_BASE_URL}/analytics/tactical/players/${playerId}`, { cache: "no-store" });
    if (!res.ok) throw new Error(`Failed to fetch tactical profile for player ${playerId}`);
    return await res.json();
  } catch (e) {
    return null;
  }
}

export async function fetchTacticalDeathOvers(params?: {
  discipline?: string;
  min_balls?: number;
  limit?: number;
}): Promise<DeathOversRankingResponse | null> {
  try {
    const query = new URLSearchParams();
    if (params?.discipline) query.set("discipline", params.discipline);
    if (params?.min_balls !== undefined) query.set("min_balls", params.min_balls.toString());
    if (params?.limit !== undefined) query.set("limit", params.limit.toString());

    const queryString = query.toString();
    const url = `${API_BASE_URL}/analytics/tactical/death-overs${queryString ? `?${queryString}` : ""}`;
    const res = await fetch(url, { cache: "no-store" });
    if (!res.ok) throw new Error("Failed to fetch death overs rankings");
    return await res.json();
  } catch (e) {
    return null;
  }
}

export async function fetchTacticalMatchup(
  strikerId: number,
  bowlerId: number
): Promise<HeadToHeadMatchupResponse | null> {
  try {
    const res = await fetch(
      `${API_BASE_URL}/analytics/tactical/matchups?striker_id=${strikerId}&bowler_id=${bowlerId}`,
      { cache: "no-store" }
    );
    if (!res.ok) throw new Error("Failed to fetch head-to-head matchup");
    return await res.json();
  } catch (e) {
    return null;
  }
}

export async function fetchTacticalPlayers(
  query: string = "",
  limit: number = 25
): Promise<PlayerLookupItem[]> {
  try {
    const url = `${API_BASE_URL}/analytics/tactical/players?query=${encodeURIComponent(query)}&limit=${limit}`;
    const res = await fetch(url, { cache: "no-store" });
    if (!res.ok) throw new Error("Failed to fetch players");
    return await res.json();
  } catch (e) {
    return [];
  }
}

// ============================================================================
// Round 1 Pressure Analytics & Reliability API (SupeRR Selector Challenge)
// ============================================================================

export async function fetchPressureOverview(): Promise<PressureOverviewResponse | null> {
  try {
    const res = await fetch(`${API_BASE_URL}/analytics/pressure/overview`, { cache: "no-store" });
    if (!res.ok) throw new Error("Failed to fetch pressure overview");
    return await res.json();
  } catch (e) {
    return null;
  }
}

export async function fetchPressureLeaderboards(params?: {
  discipline?: string;
  limit?: number;
  qualified_only?: boolean;
}): Promise<PressureLeaderboardResponse | null> {
  try {
    const query = new URLSearchParams();
    if (params?.discipline) query.set("discipline", params.discipline);
    if (params?.limit !== undefined) query.set("limit", params.limit.toString());
    if (params?.qualified_only !== undefined) query.set("qualified_only", params.qualified_only.toString());

    const queryString = query.toString();
    const url = `${API_BASE_URL}/analytics/pressure/leaderboards${queryString ? `?${queryString}` : ""}`;
    const res = await fetch(url, { cache: "no-store" });
    if (!res.ok) throw new Error("Failed to fetch pressure leaderboards");
    return await res.json();
  } catch (e) {
    return null;
  }
}

export async function fetchCandidateProfile(
  playerId: number,
  discipline?: string
): Promise<CandidateEvidenceProfileResponse | null> {
  try {
    const query = new URLSearchParams();
    if (discipline) query.set("discipline", discipline);
    const queryString = query.toString();
    const url = `${API_BASE_URL}/analytics/pressure/candidates/${playerId}${queryString ? `?${queryString}` : ""}`;
    const res = await fetch(url, { cache: "no-store" });
    if (!res.ok) throw new Error(`Failed to fetch candidate profile for player ${playerId}`);
    return await res.json();
  } catch (e) {
    return null;
  }
}

export async function fetchPressureMethodology(): Promise<PressureMethodologyResponse | null> {
  try {
    const res = await fetch(`${API_BASE_URL}/analytics/pressure/methodology`, { cache: "no-store" });
    if (!res.ok) throw new Error("Failed to fetch pressure methodology");
    return await res.json();
  } catch (e) {
    return null;
  }
}


