"use client";

import React, { useEffect, useState } from "react";
import { Server, Shield, FileText, CheckCircle2, AlertTriangle, RefreshCw } from "lucide-react";
import { fetchSystemHealth } from "@/lib/api";
import { SystemHealth } from "@/types";

export const Header: React.FC = () => {
  const [health, setHealth] = useState<SystemHealth | null>(null);
  const [loading, setLoading] = useState(false);

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

  return (
    <header className="h-16 bg-white border-b border-slate-200/80 px-6 flex items-center justify-between sticky top-0 z-20">
      {/* Left: Breadcrumb / Section Header */}
      <div className="flex items-center gap-3">
        <div className="flex items-center gap-2">
          <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
            Royals Intelligence
          </span>
          <span className="text-slate-300">/</span>
          <h2 className="text-sm font-bold text-[#101C37]">
            Platform Overview & Architecture Initialization
          </h2>
        </div>
        <span className="hidden sm:inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-mono font-semibold bg-pink-50 text-[#E91E8F] border border-pink-200">
          STAGE 0
        </span>
      </div>

      {/* Right: Telemetry & Actions */}
      <div className="flex items-center gap-4">
        {/* Backend Connectivity Indicator */}
        <button
          onClick={checkHealth}
          title="Click to re-check API connectivity"
          className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-50 border border-slate-200 text-xs text-slate-700 hover:bg-slate-100 transition-colors"
        >
          <Server size={14} className="text-[#101C37]" />
          <span className="hidden md:inline font-mono text-[11px]">API:</span>
          {isHealthy ? (
            <span className="flex items-center gap-1 font-mono text-[11px] font-semibold text-emerald-600">
              <CheckCircle2 size={13} />
              ONLINE
            </span>
          ) : (
            <span className="flex items-center gap-1 font-mono text-[11px] font-semibold text-amber-600">
              <AlertTriangle size={13} />
              STANDBY
            </span>
          )}
          {loading && <RefreshCw size={12} className="animate-spin text-slate-400" />}
        </button>

        {/* Confidentiality Pill */}
        <div className="hidden lg:flex items-center gap-1.5 text-xs text-slate-500 bg-slate-50 border border-slate-200 px-3 py-1.5 rounded-lg">
          <Shield size={14} className="text-[#D6B56D]" />
          <span className="font-semibold text-slate-700">RR Operations</span>
        </div>

        {/* Documentation Link Pill */}
        <a
          href="https://github.com/rajasthanroyals/royals-intelligence"
          target="_blank"
          rel="noopener noreferrer"
          className="hidden sm:flex items-center gap-1 text-xs text-slate-600 hover:text-[#E91E8F] transition-colors"
        >
          <FileText size={14} />
          <span>Docs</span>
        </a>
      </div>
    </header>
  );
};
