"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { ExternalLink } from "lucide-react";
import { fetchSystemHealth } from "@/lib/api";
import { SystemHealth } from "@/types";
import { ConnectionWaveform } from "@/components/ui/ConnectionWaveform";

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
    <header className="h-16 bg-white/95 backdrop-blur-md border-b border-[#E7EAF0] px-6 flex items-center justify-between sticky top-0 z-20">
      {/* Left: Breadcrumbs / Title */}
      <div className="flex items-center gap-2.5">
        <Link
          href="/"
          className="text-xs font-semibold text-[#74658F] hover:text-[#E4005A] transition-colors"
        >
          Royals Intelligence
        </Link>
        <span className="text-[#17294B]/30 font-light">/</span>
        <h1 className="text-sm font-bold tracking-tight text-[#17294B]">
          {currentPageTitle}
        </h1>
      </div>

      {/* Right: Actions & Telemetry */}
      <div className="flex items-center gap-3 text-xs">
        {/* Link to public homepage if on dashboard */}
        {pathname !== "/" && (
          <Link
            href="/"
            className="hidden sm:inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-[#E7EAF0] bg-[#FCE8F0] hover:bg-[#950460]/10 text-[#17294B] hover:text-[#E4005A] text-xs font-semibold transition-colors"
          >
            <span>Public Home</span>
            <ExternalLink size={12} className="text-[#E4005A]" />
          </Link>
        )}

        {/* Live Engine Connection Waveform Indicator */}
        <ConnectionWaveform
          isHealthy={isHealthy}
          isProbing={loading}
          onProbe={checkHealth}
        />
      </div>
    </header>
  );
};
