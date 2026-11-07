import { SystemHealth } from "@/types";

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
