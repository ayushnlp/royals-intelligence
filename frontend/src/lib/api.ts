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
