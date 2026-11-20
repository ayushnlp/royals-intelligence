import {
  SystemHealth,
  IngestionRunData,
  CompetitionSeasonSummary,
  MatchSummaryItem,
  InningsAnalysisResponse,
  MatchScorecardResponse,
  PlayerDomesticSeasonStats,
  PlayerMatchHistoryItem,
  PlayerPhaseSplitDetail,
  AllRoundContributionResponse,
  DomesticPlayerSummary,
  PaginatedDomesticPlayersResponse,
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
  UncappedLeaderboardResponse,
  UncappedOverviewResponse,
  CricketDataSource,
  CoverageReportData,
  DatasetManifestData,
  UploadDatasetResponse,
  UncappedPlayerSummary,
  UncappedPlayerDetail,
} from "@/types";

/**
 * Dynamically resolves the API base URL based on environment.
 * In development: defaults to http://localhost:8000/api/v1
 * In production: strictly uses NEXT_PUBLIC_API_URL / NEXT_PUBLIC_API_BASE_URL,
 * or falls back to relative window.location.origin /api/v1 (never hardcoded localhost).
 */
export const getApiBaseUrl = (): string => {
  const envUrl = process.env.NEXT_PUBLIC_API_URL || process.env.NEXT_PUBLIC_API_BASE_URL;
  if (envUrl) {
    return envUrl.replace(/\/+$/, "");
  }
  if (typeof window !== "undefined") {
    // When running locally in browser (both dev server and local production preview)
    if (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1") {
      return `http://${window.location.hostname}:8000/api/v1`;
    }
    // Remote production deployment without explicit env var
    return `${window.location.origin}/api/v1`;
  }
  if (process.env.NODE_ENV === "production") {
    return "/api/v1";
  }
  return "http://localhost:8000/api/v1";
};

export const API_BASE_URL = getApiBaseUrl();

export class ApiError extends Error {
  public status?: number;
  public statusText?: string;
  public isNetworkError: boolean;
  public endpoint: string;

  constructor(
    message: string,
    options?: { status?: number; statusText?: string; isNetworkError?: boolean; endpoint?: string }
  ) {
    super(message);
    this.name = "ApiError";
    this.status = options?.status;
    this.statusText = options?.statusText;
    this.isNetworkError = Boolean(options?.isNetworkError);
    this.endpoint = options?.endpoint || "";
  }
}

/**
 * Centralized, type-safe API fetch wrapper with timeout and explicit error handling.
 * Never silently swallows network or HTTP errors into pseudo-empty records.
 */
export async function safeApiFetch<T>(
  endpoint: string,
  options?: RequestInit & { timeoutMs?: number }
): Promise<T> {
  const baseUrl = getApiBaseUrl();
  const cleanEndpoint = endpoint.startsWith("/") ? endpoint : `/${endpoint}`;
  const url = `${baseUrl}${cleanEndpoint}`;
  const timeoutMs = options?.timeoutMs ?? 15000;
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);

  let res: Response;
  try {
    res = await fetch(url, {
      cache: "no-store",
      ...options,
      signal: options?.signal || controller.signal,
    });
  } catch (err: any) {
    clearTimeout(timer);
    if (err.name === "AbortError") {
      throw new ApiError(
        `Request timed out after ${timeoutMs / 1000}s connecting to ${cleanEndpoint}`,
        { isNetworkError: true, endpoint: cleanEndpoint }
      );
    }
    throw new ApiError(
      `Network error connecting to backend service at ${baseUrl}: ${err.message || "Connection refused / unreachable"}`,
      { isNetworkError: true, endpoint: cleanEndpoint }
    );
  } finally {
    clearTimeout(timer);
  }

  if (!res.ok) {
    let errorDetail = "";
    try {
      const errJson = await res.json();
      errorDetail =
        typeof errJson.detail === "string"
          ? errJson.detail
          : JSON.stringify(errJson.detail || errJson.message || "");
    } catch {
      // non-JSON error body
    }
    throw new ApiError(
      errorDetail ? `API Error [${res.status}]: ${errorDetail}` : `API Error [${res.status}] ${res.statusText}`,
      { status: res.status, statusText: res.statusText, endpoint: cleanEndpoint }
    );
  }

  try {
    return await res.json();
  } catch (err: any) {
    throw new ApiError(
      `Invalid JSON response from ${cleanEndpoint}: ${err.message}`,
      { status: res.status, statusText: res.statusText, endpoint: cleanEndpoint }
    );
  }
}

// ============================================================================
// Core Health & Diagnostics
// ============================================================================

export async function fetchSystemHealth(): Promise<SystemHealth> {
  return await safeApiFetch<SystemHealth>("/health");
}

// ============================================================================
// Stage 1: Data Acquisition & Provenance Hub
// ============================================================================

export async function fetchSources(tier?: string, category?: string): Promise<CricketDataSource[]> {
  const query = new URLSearchParams();
  if (tier) query.set("tier", tier);
  if (category) query.set("category", category);
  const qs = query.toString();
  return await safeApiFetch<CricketDataSource[]>(`/acquisition/sources${qs ? `?${qs}` : ""}`);
}

export async function fetchCoverage(): Promise<CoverageReportData> {
  return await safeApiFetch<CoverageReportData>("/acquisition/coverage");
}

export async function fetchIngestionRuns(limit: number = 50): Promise<IngestionRunData[]> {
  try {
    return await safeApiFetch<IngestionRunData[]>(`/acquisition/runs?limit=${limit}`);
  } catch (err: any) {
    if (err instanceof ApiError && err.status === 404) {
      return await safeApiFetch<IngestionRunData[]>(`/acquisition/ingestion-runs?limit=${limit}`);
    }
    throw err;
  }
}

export async function fetchDatasets(): Promise<DatasetManifestData[]> {
  return await safeApiFetch<DatasetManifestData[]>("/acquisition/datasets");
}

export async function uploadDataset(formData: FormData): Promise<UploadDatasetResponse> {
  return await safeApiFetch<UploadDatasetResponse>("/acquisition/upload", {
    method: "POST",
    body: formData,
  });
}

// ============================================================================
// Stage 2: Uncapped Players, Eligibility & Scouting
// ============================================================================

const SCOUT_ADMIN_TOKEN = process.env.NEXT_PUBLIC_SCOUT_ADMIN_TOKEN || "rr_scout_admin_secret_token_2026";

export async function fetchUncappedPlayers(params?: {
  eligibility?: string;
  tier?: string;
  role?: string;
  state?: string;
  trialist_only?: boolean;
}): Promise<UncappedPlayerSummary[]> {
  const query = new URLSearchParams();
  if (params?.eligibility) query.append("eligibility", params.eligibility);
  if (params?.tier) query.append("tier", params.tier);
  if (params?.role) query.append("role", params.role);
  if (params?.state) query.append("state", params.state);
  if (params?.trialist_only) query.append("trialist_only", "true");

  const qs = query.toString();
  return await safeApiFetch<UncappedPlayerSummary[]>(`/players${qs ? `?${qs}` : ""}`);
}

export async function fetchUncappedPlayerDetail(playerId: string): Promise<UncappedPlayerDetail> {
  return await safeApiFetch<UncappedPlayerDetail>(`/players/${playerId}`);
}

export async function verifyPlayerEligibility(
  playerId: string,
  payload: { new_status: string; verification_notes: string; verified_by?: string }
): Promise<any> {
  return await safeApiFetch(`/players/${playerId}/verify-eligibility`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${SCOUT_ADMIN_TOKEN}`,
    },
    body: JSON.stringify(payload),
  });
}

export async function fetchPlayerBatting(playerId: string): Promise<any> {
  return await safeApiFetch(`/analytics/players/${playerId}/batting`);
}

export async function fetchPlayerBowling(playerId: string): Promise<any> {
  return await safeApiFetch(`/analytics/players/${playerId}/bowling`);
}

export async function fetchPlayerRecentForm(
  playerId: string,
  lastN: number = 5,
  discipline: string = "batting"
): Promise<any> {
  return await safeApiFetch(
    `/analytics/players/${playerId}/recent-form?last_n=${lastN}&discipline=${discipline}`
  );
}

export async function discoverProprietarySchema(sampleRows: any[]): Promise<any> {
  return await safeApiFetch("/proprietary/discover-schema", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${SCOUT_ADMIN_TOKEN}`,
    },
    body: JSON.stringify({ sample_rows: sampleRows }),
  });
}

export async function ingestProprietaryPack(payload: {
  records: any[];
  column_mapping?: any;
  dataset_key?: string;
}): Promise<any> {
  return await safeApiFetch("/proprietary/ingest-pack", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${SCOUT_ADMIN_TOKEN}`,
    },
    body: JSON.stringify(payload),
  });
}

export async function fetchPlayerEvaluations(playerId: string, userRole: string = "public"): Promise<any[]> {
  const headers: Record<string, string> = {};
  if (userRole === "rr_scout_admin") {
    headers["Authorization"] = `Bearer ${SCOUT_ADMIN_TOKEN}`;
  }
  return await safeApiFetch<any[]>(`/proprietary/evaluations/${playerId}`, { headers });
}

// ============================================================================
// Stage 3: Domestic Season and Match Intelligence API
// ============================================================================

export async function fetchDomesticCompetitions(): Promise<CompetitionSeasonSummary[]> {
  return await safeApiFetch<CompetitionSeasonSummary[]>("/domestic/competitions");
}

export async function fetchSeasonMatches(
  competitionId: string,
  season: string,
  params?: { team?: string; page?: number; page_size?: number }
): Promise<{ total: number; page: number; page_size: number; matches: MatchSummaryItem[] }> {
  const query = new URLSearchParams();
  if (params?.team) query.append("team", params.team);
  if (params?.page) query.append("page", String(params.page));
  if (params?.page_size) query.append("page_size", String(params.page_size));

  const qs = query.toString();
  const data = await safeApiFetch<any>(
    `/domestic/seasons/${competitionId}/${season}/matches${qs ? `?${qs}` : ""}`
  );
  return {
    total: data.total ?? data.total_matches ?? 0,
    page: data.page ?? 1,
    page_size: data.page_size ?? 20,
    matches: data.matches ?? [],
  };
}

export async function fetchSeasonSummary(
  competitionId: string,
  season: string
): Promise<CompetitionSeasonSummary> {
  return await safeApiFetch<CompetitionSeasonSummary>(
    `/domestic/seasons/${competitionId}/${season}/summary`
  );
}

export async function fetchMatchScorecard(matchId: string): Promise<MatchScorecardResponse> {
  return await safeApiFetch<MatchScorecardResponse>(`/domestic/matches/${matchId}`);
}

export async function fetchInningsAnalysis(
  matchId: string,
  inningsNumber: number
): Promise<InningsAnalysisResponse> {
  return await safeApiFetch<InningsAnalysisResponse>(
    `/domestic/matches/${matchId}/innings/${inningsNumber}`
  );
}

export async function fetchPlayerDomesticStats(
  playerId: string,
  competitionId?: string
): Promise<PlayerDomesticSeasonStats[]> {
  const qs = competitionId ? `?competition_id=${encodeURIComponent(competitionId)}` : "";
  return await safeApiFetch<PlayerDomesticSeasonStats[]>(
    `/domestic/players/${playerId}/season-stats${qs}`
  );
}

export async function fetchPlayerMatchHistory(
  playerId: string,
  params?: { competition_id?: string; season?: string; page?: number; page_size?: number }
): Promise<{ total: number; page: number; page_size: number; history: PlayerMatchHistoryItem[] }> {
  const query = new URLSearchParams();
  if (params?.competition_id) query.append("competition_id", params.competition_id);
  if (params?.season) query.append("season", params.season);
  if (params?.page) query.append("page", String(params.page));
  if (params?.page_size) query.append("page_size", String(params.page_size));

  const qs = query.toString();
  const data = await safeApiFetch<any>(
    `/domestic/players/${playerId}/match-history${qs ? `?${qs}` : ""}`
  );
  return {
    total: data.total ?? data.total_matches ?? 0,
    page: data.page ?? 1,
    page_size: data.page_size ?? 20,
    history: data.history ?? data.matches ?? [],
  };
}

export async function fetchPlayerPhaseSplits(
  playerId: string,
  competitionId?: string
): Promise<PlayerPhaseSplitDetail[]> {
  const qs = competitionId ? `?competition_id=${encodeURIComponent(competitionId)}` : "";
  return await safeApiFetch<PlayerPhaseSplitDetail[]>(
    `/domestic/players/${playerId}/phase-splits${qs}`
  );
}

export async function fetchPlayerAllRoundSummary(
  playerId: string
): Promise<AllRoundContributionResponse> {
  return await safeApiFetch<AllRoundContributionResponse>(
    `/domestic/players/${playerId}/all-round-summary`
  );
}

export interface DomesticPlayersQueryParams {
  page?: number;
  page_size?: number;
  search?: string;
  eligibility_status?: string;
  role?: string;
  team?: string;
  competition?: string;
  season?: string;
}

export async function fetchDomesticPlayers(
  params?: DomesticPlayersQueryParams
): Promise<PaginatedDomesticPlayersResponse> {
  const query = new URLSearchParams();
  if (params?.page) query.append("page", String(params.page));
  if (params?.page_size) query.append("page_size", String(params.page_size));
  if (params?.search) query.append("search", params.search);
  if (params?.eligibility_status) query.append("eligibility_status", params.eligibility_status);
  if (params?.role) query.append("role", params.role);
  if (params?.team) query.append("team", params.team);
  if (params?.competition) query.append("competition", params.competition);
  if (params?.season) query.append("season", params.season);

  const qs = query.toString();
  return await safeApiFetch<PaginatedDomesticPlayersResponse>(`/domestic/players${qs ? `?${qs}` : ""}`);
}

// ============================================================================
// Stage 4: Venue, Pitch & Weather Intelligence API
// ============================================================================

export async function fetchVenues(rrOnly: boolean = false): Promise<VenueSummaryItem[]> {
  const qs = rrOnly ? "?rr_only=true" : "";
  return await safeApiFetch<VenueSummaryItem[]>(`/venues${qs}`);
}

export async function fetchVenueDetail(venueId: string): Promise<VenueDetailResponse> {
  return await safeApiFetch<VenueDetailResponse>(`/venues/${venueId}`);
}

export async function fetchVenueScoringTrends(venueId: string): Promise<VenueScoringTrendsResponse> {
  return await safeApiFetch<VenueScoringTrendsResponse>(`/venues/${venueId}/scoring-trends`);
}

export async function fetchVenuePitchAnalysis(venueId: string): Promise<PitchEvidenceAnalysisResponse> {
  return await safeApiFetch<PitchEvidenceAnalysisResponse>(`/venues/${venueId}/pitch-analysis`);
}

export async function fetchPlayerVenuePerformance(
  venueId: string,
  playerId: string
): Promise<UncappedPlayerVenuePerformanceResponse> {
  return await safeApiFetch<UncappedPlayerVenuePerformanceResponse>(
    `/venues/${venueId}/player-performance?player_id=${encodeURIComponent(playerId)}`
  );
}

export async function fetchMatchWeatherContext(matchId: string): Promise<MatchWeatherContextResponse> {
  return await safeApiFetch<MatchWeatherContextResponse>(`/weather/match/${matchId}`);
}

export async function fetchHistoricalWeather(
  venueCode: string,
  matchDate: string
): Promise<WeatherObservationItem[]> {
  return await safeApiFetch<WeatherObservationItem[]>(
    `/weather/historical?venue_code=${encodeURIComponent(venueCode)}&match_date=${encodeURIComponent(matchDate)}`
  );
}

export async function fetchWeatherForecast(
  venueCode: string,
  daysAhead: number = 7
): Promise<WeatherObservationItem[]> {
  return await safeApiFetch<WeatherObservationItem[]>(
    `/weather/forecast?venue_code=${encodeURIComponent(venueCode)}&days_ahead=${daysAhead}`
  );
}

export async function fetchWeatherSourceStatus(): Promise<WeatherSourceStatusResponse> {
  return await safeApiFetch<WeatherSourceStatusResponse>("/weather/source-status");
}

// ============================================================================
// Stage 5: Dataset-Driven Tactical Cricket Intelligence API
// ============================================================================

export async function fetchTacticalSummary(): Promise<TacticalDatasetSummaryResponse> {
  return await safeApiFetch<TacticalDatasetSummaryResponse>("/analytics/tactical/summary");
}

export async function fetchTacticalPhases(params?: {
  striker_id?: number;
  bowler_id?: number;
  phase?: string;
}): Promise<TacticalPhaseResponse> {
  const query = new URLSearchParams();
  if (params?.striker_id !== undefined) query.set("striker_id", params.striker_id.toString());
  if (params?.bowler_id !== undefined) query.set("bowler_id", params.bowler_id.toString());
  if (params?.phase) query.set("phase", params.phase);

  const qs = query.toString();
  return await safeApiFetch<TacticalPhaseResponse>(`/analytics/tactical/phases${qs ? `?${qs}` : ""}`);
}

export async function fetchTacticalStrokes(params?: {
  striker_id?: number;
  stroke?: string;
  min_balls?: number;
}): Promise<TacticalStrokesResponse> {
  const query = new URLSearchParams();
  if (params?.striker_id !== undefined) query.set("striker_id", params.striker_id.toString());
  if (params?.stroke) query.set("stroke", params.stroke);
  if (params?.min_balls !== undefined) query.set("min_balls", params.min_balls.toString());

  const qs = query.toString();
  return await safeApiFetch<TacticalStrokesResponse>(`/analytics/tactical/strokes${qs ? `?${qs}` : ""}`);
}

export async function fetchTacticalHandedness(params?: {
  batting_type?: string;
  pace_or_spin?: string;
  striker_id?: number;
  bowler_id?: number;
}): Promise<HandednessMatrixResponse> {
  const query = new URLSearchParams();
  if (params?.batting_type) query.set("batting_type", params.batting_type);
  if (params?.pace_or_spin) query.set("pace_or_spin", params.pace_or_spin);
  if (params?.striker_id !== undefined) query.set("striker_id", params.striker_id.toString());
  if (params?.bowler_id !== undefined) query.set("bowler_id", params.bowler_id.toString());

  const qs = query.toString();
  return await safeApiFetch<HandednessMatrixResponse>(`/analytics/tactical/handedness${qs ? `?${qs}` : ""}`);
}

export async function fetchTacticalVariations(params?: {
  bowler_id?: number;
  delivery_style?: string;
  min_balls?: number;
}): Promise<DeliveryStylesResponse> {
  const query = new URLSearchParams();
  if (params?.bowler_id !== undefined) query.set("bowler_id", params.bowler_id.toString());
  if (params?.delivery_style) query.set("delivery_style", params.delivery_style);
  if (params?.min_balls !== undefined) query.set("min_balls", params.min_balls.toString());

  const qs = query.toString();
  return await safeApiFetch<DeliveryStylesResponse>(`/analytics/tactical/variations${qs ? `?${qs}` : ""}`);
}

export async function fetchTacticalSpeedProfiles(params?: {
  bowler_id?: number;
  min_balls?: number;
  top_n?: number;
}): Promise<SpeedProfileResponse> {
  const query = new URLSearchParams();
  if (params?.bowler_id !== undefined) query.set("bowler_id", params.bowler_id.toString());
  if (params?.min_balls !== undefined) query.set("min_balls", params.min_balls.toString());
  if (params?.top_n !== undefined) query.set("top_n", params.top_n.toString());

  const qs = query.toString();
  return await safeApiFetch<SpeedProfileResponse>(`/analytics/tactical/speed-profiles${qs ? `?${qs}` : ""}`);
}

export async function fetchPlayerTacticalProfile(playerId: number): Promise<PlayerTacticalProfileResponse> {
  return await safeApiFetch<PlayerTacticalProfileResponse>(`/analytics/tactical/players/${playerId}`);
}

export async function fetchTacticalDeathOvers(params?: {
  discipline?: string;
  min_balls?: number;
  limit?: number;
}): Promise<DeathOversRankingResponse> {
  const query = new URLSearchParams();
  if (params?.discipline) query.set("discipline", params.discipline);
  if (params?.min_balls !== undefined) query.set("min_balls", params.min_balls.toString());
  if (params?.limit !== undefined) query.set("limit", params.limit.toString());

  const qs = query.toString();
  return await safeApiFetch<DeathOversRankingResponse>(`/analytics/tactical/death-overs${qs ? `?${qs}` : ""}`);
}

export async function fetchTacticalMatchup(
  strikerId: number,
  bowlerId: number
): Promise<HeadToHeadMatchupResponse> {
  return await safeApiFetch<HeadToHeadMatchupResponse>(
    `/analytics/tactical/matchups?striker_id=${strikerId}&bowler_id=${bowlerId}`
  );
}

export async function fetchTacticalPlayers(
  query: string = "",
  limit: number = 25
): Promise<PlayerLookupItem[]> {
  const url = `/analytics/tactical/players?query=${encodeURIComponent(query)}&limit=${limit}`;
  return await safeApiFetch<PlayerLookupItem[]>(url);
}

// ============================================================================
// Round 1 Pressure Analytics & Reliability API (SupeRR Selector Challenge)
// ============================================================================

export async function fetchPressureOverview(): Promise<PressureOverviewResponse> {
  return await safeApiFetch<PressureOverviewResponse>("/analytics/pressure/overview");
}

export async function fetchPressureLeaderboards(params?: {
  discipline?: string;
  limit?: number;
  qualified_only?: boolean;
}): Promise<PressureLeaderboardResponse> {
  const query = new URLSearchParams();
  if (params?.discipline) query.set("discipline", params.discipline);
  if (params?.limit !== undefined) query.set("limit", params.limit.toString());
  if (params?.qualified_only !== undefined) query.set("qualified_only", params.qualified_only.toString());

  const qs = query.toString();
  return await safeApiFetch<PressureLeaderboardResponse>(
    `/analytics/pressure/leaderboards${qs ? `?${qs}` : ""}`
  );
}

export async function fetchCandidateProfile(
  playerId: number,
  discipline?: string
): Promise<CandidateEvidenceProfileResponse> {
  const query = new URLSearchParams();
  if (discipline) query.set("discipline", discipline);
  const qs = query.toString();
  return await safeApiFetch<CandidateEvidenceProfileResponse>(
    `/analytics/pressure/candidates/${playerId}${qs ? `?${qs}` : ""}`
  );
}

export async function fetchPressureMethodology(): Promise<PressureMethodologyResponse> {
  return await safeApiFetch<PressureMethodologyResponse>("/analytics/pressure/methodology");
}

export async function fetchUncappedOverview(params?: {
  min_balls?: number;
  min_matches?: number;
}): Promise<UncappedOverviewResponse> {
  const query = new URLSearchParams();
  if (params?.min_balls !== undefined) query.set("min_balls", params.min_balls.toString());
  if (params?.min_matches !== undefined) query.set("min_matches", params.min_matches.toString());

  const qs = query.toString();
  return await safeApiFetch<UncappedOverviewResponse>(
    `/analytics/uncapped/overview${qs ? `?${qs}` : ""}`
  );
}

export async function fetchUncappedLeaderboards(params?: {
  discipline?: string;
  limit?: number;
  qualified_only?: boolean;
  min_balls?: number;
  min_matches?: number;
}): Promise<UncappedLeaderboardResponse> {
  const query = new URLSearchParams();
  if (params?.discipline) query.set("discipline", params.discipline);
  if (params?.limit !== undefined) query.set("limit", params.limit.toString());
  if (params?.qualified_only !== undefined) query.set("qualified_only", params.qualified_only.toString());
  if (params?.min_balls !== undefined) query.set("min_balls", params.min_balls.toString());
  if (params?.min_matches !== undefined) query.set("min_matches", params.min_matches.toString());

  const qs = query.toString();
  return await safeApiFetch<UncappedLeaderboardResponse>(
    `/analytics/uncapped/leaderboards${qs ? `?${qs}` : ""}`
  );
}

export async function fetchPlayerEligibility(playerId: number, playerName?: string): Promise<any> {
  const query = new URLSearchParams();
  if (playerName) query.set("player_name", playerName);
  const qs = query.toString();
  return await safeApiFetch(`/analytics/uncapped/eligibility/${playerId}${qs ? `?${qs}` : ""}`);
}
