"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { RefreshCw, ExternalLink } from "lucide-react";
import { fetchSystemHealth } from "@/lib/api";
import { SystemHealth } from "@/types";

const PAGE_TITLES: Record<string, string> = {
  "/": "Public Home",
  "/overview": "Executive Overview",
  "/pressure": "Pressure Intelligence",
  "/tactical": "Tactical Intelligence",
  "/uncapped": "Uncapped Intelligence",
  "/domestic": "Domestic & Matches",
  "/venues": "Venue & Pitch",
  "/acquisition": "Data Acquisition",
};

export const Header: React.FC = () => {
  const [health, setHealth] = useState<SystemHealth | null>(null);
  const [loading, setLoading] = useState(false);
  const pathname = usePathname();

  const checkHealth = async () => {
    setLoading(true);
    try {
      const data = await fetchSystemHealth();
      setHealth(data);
    } catch {
      setHealth(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    checkHealth();
    const interval = setInterval(checkHealth, 30000);
    return () => clearInterval(interval);
  }, []);

  const isHealthy = health?.status === "healthy";
  const currentPageTitle = pathname
    ? PAGE_TITLES[pathname] || "Intelligence Platform"
    : "Executive Overview";

  return (
    <header className="h-16 bg-white/95 backdrop-blur-md border-b border-[#31136C]/12 px-6 flex items-center justify-between sticky top-0 z-20">
      {/* Left: Breadcrumbs / Title */}
      <div className="flex items-center gap-2.5">
        <Link
          href="/"
          className="text-xs font-semibold text-[#31136C]/70 hover:text-[#950460] transition-colors"
        >
          Royals Intelligence
        </Link>
        <span className="text-[#31136C]/30 font-light">/</span>
        <h1 className="text-sm font-bold tracking-tight text-[#31136C]">
          {currentPageTitle}
        </h1>
      </div>

      {/* Right: Actions & Telemetry */}
      <div className="flex items-center gap-3 text-xs">
        {/* Link to public homepage if on dashboard */}
        {pathname !== "/" && (
          <Link
            href="/"
            className="hidden sm:inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-[#31136C]/15 bg-[#F7F6FB] hover:bg-[#950460]/10 text-[#31136C] hover:text-[#950460] text-xs font-semibold transition-colors"
          >
            <span>Public Home</span>
            <ExternalLink size={12} className="text-[#950460]" />
          </Link>
        )}

        {/* Live Engine Status Indicator */}
        <button
          onClick={checkHealth}
          title="Click to probe FastAPI health endpoint"
          className="flex items-center gap-2 px-3 py-1.5 rounded-lg border border-[#31136C]/15 bg-white hover:bg-[#F7F6FB] text-[#31136C] transition-colors cursor-pointer shadow-soft"
        >
          <span className="relative flex h-2 w-2">
            {isHealthy && (
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-[#950460] opacity-75" />
            )}
            <span
              className={`relative inline-flex rounded-full h-2 w-2 ${
                isHealthy ? "bg-[#950460]" : "bg-[#31136C]/40"
              }`}
            />
          </span>
          <span className="font-mono text-[11px] text-[#31136C]/70">
            Engine:{" "}
            <strong
              className={
                isHealthy
                  ? "text-[#950460] font-bold"
                  : "text-[#31136C]/60 font-semibold"
              }
            >
              {isHealthy ? "Online" : "Standby"}
            </strong>
          </span>
          <RefreshCw
            size={11}
            className={`text-[#31136C]/70 ${loading ? "animate-spin text-[#950460]" : ""}`}
          />
        </button>
      </div>
    </header>
  );
};
