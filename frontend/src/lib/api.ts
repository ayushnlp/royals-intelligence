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
