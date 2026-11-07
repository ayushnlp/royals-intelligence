"use client";

import React, { useState } from "react";
import Link from "next/link";
import {
  LayoutDashboard,
  DownloadCloud,
  Swords,
  MapPin,
  TrendingUp,
  Target,
  Users,
  Gavel,
  Activity,
  ChevronLeft,
  ChevronRight,
  ShieldCheck,
  Database,
} from "lucide-react";
import { cn } from "@/lib/utils";

interface SidebarProps {
  className?: string;
}

export const Sidebar: React.FC<SidebarProps> = ({ className }) => {
  const [collapsed, setCollapsed] = useState(false);

  const navItems = [
    {
      title: "System Overview",
      href: "/",
      icon: LayoutDashboard,
      active: false,
      stage: "Stage 0",
    },
    {
      title: "Data Acquisition",
      href: "/acquisition",
      icon: DownloadCloud,
      active: true,
      stage: "Stage 1",
    },
    {
      title: "Uncapped Scouting",
      href: "/uncapped",
      icon: Users,
      active: true,
      stage: "Stage 2",
    },
    {
      title: "Domestic & Matches",
      href: "/domestic",
      icon: Swords,
      active: true,
      stage: "Stage 3",
    },
    {
      title: "Venue & Pitch",
      href: "/venues",
      icon: MapPin,
      active: true,
      stage: "Stage 4",
    },
    {
      title: "Batting Diagnostics",
      href: "#",
      icon: TrendingUp,
      active: false,
      badge: "Pending",
      stage: "Stage 3",
    },
    {
      title: "Bowling Mechanics",
      href: "#",
      icon: Target,
      active: false,
      badge: "Pending",
      stage: "Stage 4",
    },
    {
      title: "Talent Scouting",
      href: "#",
      icon: Users,
      active: false,
      badge: "Pending",
      stage: "Stage 8",
    },
    {
      title: "IPL 2027 Auction",
      href: "#",
      icon: Gavel,
      active: false,
      badge: "Pending",
      stage: "Stage 12",
    },
    {
      title: "Health & Schema",
      href: "#health",
      icon: Activity,
      active: false,
      stage: "Active",
    },
  ];

  return (
    <aside
      className={cn(
        "relative flex flex-col bg-[#101C37] text-white transition-all duration-300 z-30 min-h-screen border-r border-[#1A2B50]",
        collapsed ? "w-20" : "w-64",
        className
      )}
    >
      {/* Brand Header */}
      <div className="flex items-center justify-between px-4 py-5 border-b border-[#1A2B50]">
        {!collapsed && (
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-[#E91E8F] to-[#D6B56D] p-0.5 shadow-md flex items-center justify-center">
              <div className="w-full h-full bg-[#101C37] rounded-[10px] flex items-center justify-center">
                <span className="font-extrabold text-lg text-transparent bg-clip-text bg-gradient-to-r from-[#E91E8F] to-[#D6B56D]">
                  RR
                </span>
              </div>
            </div>
            <div>
              <h1 className="font-bold text-sm tracking-wide leading-none text-white">
                ROYALS
              </h1>
              <p className="text-[10px] font-mono tracking-widest text-[#D6B56D] mt-1 font-semibold uppercase">
                INTELLIGENCE
              </p>
            </div>
          </div>
        )}

        {collapsed && (
          <div className="mx-auto w-10 h-10 rounded-xl bg-gradient-to-tr from-[#E91E8F] to-[#D6B56D] p-0.5 shadow-md flex items-center justify-center">
            <div className="w-full h-full bg-[#101C37] rounded-[10px] flex items-center justify-center">
              <span className="font-extrabold text-sm text-[#E91E8F]">RR</span>
            </div>
          </div>
        )}

        <button
          onClick={() => setCollapsed(!collapsed)}
          className="hidden md:flex p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-[#1A2B50] transition-colors"
          aria-label={collapsed ? "Expand sidebar" : "Collapse sidebar"}
        >
          {collapsed ? <ChevronRight size={18} /> : <ChevronLeft size={18} />}
        </button>
      </div>

      {/* Campaign Badge */}
      {!collapsed && (
        <div className="mx-4 my-3 px-3 py-2 rounded-lg bg-[#1A2B50]/60 border border-[#1A2B50] flex items-center justify-between">
          <div className="flex items-center gap-2">
            <ShieldCheck size={14} className="text-[#D6B56D]" />
            <span className="text-[11px] font-semibold text-slate-200">IPL 2026 Season</span>
          </div>
          <span className="text-[10px] font-mono font-bold text-[#E91E8F]">RR 2027</span>
        </div>
      )}

      {/* Navigation Links */}
      <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
        {navItems.map((item, index) => {
          const Icon = item.icon;
          return (
            <Link
              key={index}
              href={item.href}
              className={cn(
                "flex items-center gap-3 px-3 py-2.5 rounded-lg text-xs font-medium transition-all group relative",
                item.active
                  ? "bg-[#E91E8F] text-white shadow-sm"
                  : "text-slate-300 hover:bg-[#1A2B50] hover:text-white"
              )}
            >
              <Icon
                size={18}
                className={cn(
                  "shrink-0 transition-colors",
                  item.active ? "text-white" : "text-slate-400 group-hover:text-[#E91E8F]"
                )}
              />

              {!collapsed && (
                <div className="flex items-center justify-between w-full">
                  <span>{item.title}</span>
                  {item.badge ? (
                    <span className="text-[9px] font-mono font-bold px-1.5 py-0.5 rounded bg-[#101C37] text-slate-400 border border-[#1A2B50]">
                      {item.stage}
                    </span>
                  ) : (
                    item.stage && (
                      <span className="text-[9px] font-mono font-semibold text-[#D6B56D]">
                        {item.stage}
                      </span>
                    )
                  )}
                </div>
              )}

              {/* Tooltip on collapse */}
              {collapsed && (
                <div className="absolute left-full ml-3 px-2 py-1 rounded bg-[#0B1220] border border-[#1A2B50] text-xs font-medium whitespace-nowrap opacity-0 group-hover:opacity-100 pointer-events-none transition-opacity z-50">
                  {item.title} ({item.stage})
                </div>
              )}
            </Link>
          );
        })}
      </nav>

      {/* Footer Info */}
      <div className="p-4 border-t border-[#1A2B50] bg-[#0B1220]/60">
        {!collapsed ? (
          <div className="space-y-2">
            <div className="flex items-center justify-between text-[11px] text-slate-400">
              <span className="flex items-center gap-1.5">
                <Database size={13} className="text-[#D6B56D]" /> Architecture
              </span>
              <span className="font-mono text-emerald-400 font-semibold">STAGE 0</span>
            </div>
            <div className="w-full bg-[#1A2B50] rounded-full h-1.5 overflow-hidden">
              <div className="bg-gradient-to-r from-[#E91E8F] to-[#D6B56D] h-full w-[15%]" />
            </div>
            <p className="text-[10px] text-slate-500 font-mono">
              Stage 1 of 13 Ingestion Active
            </p>
          </div>
        ) : (
          <div className="flex justify-center text-emerald-400">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
          </div>
        )}
      </div>
    </aside>
  );
};
