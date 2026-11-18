"use client";

import React, { useEffect, useState } from "react";
import { usePathname } from "next/navigation";
import { Shield, FileText, CheckCircle2, AlertTriangle, RefreshCw } from "lucide-react";
import { fetchSystemHealth } from "@/lib/api";
import { SystemHealth } from "@/types";

const PAGE_TITLES: Record<string, string> = {
  "/": "Executive Overview",
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
    const data = await fetchSystemHealth();
    setHealth(data);
    setLoading(false);
  };

  useEffect(() => {
    checkHealth();
    const interval = setInterval(checkHealth, 30000);
    return () => clearInterval(interval);
  }, []);

  const isHealthy = health?.status === "healthy";
  const currentPageTitle = pathname ? PAGE_TITLES[pathname] || "Intelligence Platform" : "Executive Overview";

  return (
    <header className="h-16 bg-white/95 backdrop-blur-sm border-b border-slate-200/60 px-6 flex items-center justify-between sticky top-0 z-20">
      {/* Left: Breadcrumb / Page Title */}
      <div className="flex items-center gap-2.5">
        <span className="text-xs font-medium text-slate-400">
          Royals Intelligence
        </span>
        <span className="text-slate-300 font-light">/</span>
        <h2 className="text-sm font-semibold tracking-tight text-slate-900">
          {currentPageTitle}
        </h2>
      </div>

      {/* Right: Telemetry & Navigation Actions */}
      <div className="flex items-center gap-5 text-xs">
        {/* Understated API Status Indicator */}
        <button
          onClick={checkHealth}
          title="Click to re-check API connectivity"
          className="flex items-center gap-2 text-slate-600 hover:text-slate-900 transition-colors cursor-pointer py-1"
        >
          <span className="relative flex h-2 w-2">
            {isHealthy && (
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75" />
            )}
            <span
              className={`relative inline-flex rounded-full h-2 w-2 ${
                isHealthy ? "bg-emerald-500" : "bg-amber-500"
              }`}
            />
          </span>
          <span className="font-mono text-[11px] text-slate-500">
            API: <strong className={isHealthy ? "text-emerald-700 font-semibold" : "text-amber-700 font-semibold"}>{isHealthy ? "Online" : "Standby"}</strong>
          </span>
          {loading && <RefreshCw size={11} className="animate-spin text-slate-400" />}
        </button>

        <span className="h-3.5 w-px bg-slate-200" />

        {/* RR Operations Link */}
        <div className="hidden sm:flex items-center gap-1.5 text-slate-600 hover:text-slate-900 transition-colors">
          <Shield size={13} className="text-[#D6B56D]" />
          <span className="font-medium text-[11px]">RR Operations</span>
        </div>

        {/* Documentation Link */}
        <a
          href="https://github.com/rajasthanroyals/royals-intelligence"
          target="_blank"
          rel="noopener noreferrer"
          className="hidden sm:flex items-center gap-1 text-slate-500 hover:text-[#E91E8F] transition-colors"
        >
          <FileText size={13} />
          <span className="font-medium text-[11px]">Docs</span>
        </a>
      </div>
    </header>
  );
};
