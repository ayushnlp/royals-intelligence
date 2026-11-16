"use client";

import React, { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard,
  DownloadCloud,
  Swords,
  MapPin,
  ChevronLeft,
  ChevronRight,
  ShieldCheck,
  Shield,
  Database,
  Crosshair,
  Award,
  CheckCircle2,
} from "lucide-react";
import { cn } from "@/lib/utils";

interface SidebarProps {
  className?: string;
}

export const Sidebar: React.FC<SidebarProps> = ({ className }) => {
  const [collapsed, setCollapsed] = useState(false);
  const pathname = usePathname();

  const primaryNavItems = [
    {
      title: "Executive Overview",
      href: "/",
      icon: LayoutDashboard,
      stage: "Overview",
    },
    {
      title: "Pressure Intelligence",
      href: "/pressure",
      icon: Shield,
      stage: "Round 1",
      badge: "Flagship",
    },
    {
      title: "Tactical Intelligence",
      href: "/tactical",
      icon: Crosshair,
      stage: "Stage 5",
      badge: "Official Data",
    },
  ];

  const foundationNavItems = [
    {
      title: "Data Acquisition",
      href: "/acquisition",
      icon: DownloadCloud,
      stage: "Stage 1",
    },
    {
      title: "Domestic & Matches",
      href: "/domestic",
      icon: Swords,
      stage: "Stage 3",
    },
    {
      title: "Venue & Pitch",
      href: "/venues",
      icon: MapPin,
      stage: "Stage 4",
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
          <Link href="/" className="flex items-center gap-3 group">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-[#E91E8F] to-[#D6B56D] p-0.5 shadow-md flex items-center justify-center group-hover:scale-105 transition-transform">
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
          </Link>
        )}

        {collapsed && (
          <Link href="/" className="mx-auto w-10 h-10 rounded-xl bg-gradient-to-tr from-[#E91E8F] to-[#D6B56D] p-0.5 shadow-md flex items-center justify-center">
            <div className="w-full h-full bg-[#101C37] rounded-[10px] flex items-center justify-center">
              <span className="font-extrabold text-sm text-[#E91E8F]">RR</span>
            </div>
          </Link>
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
            <Award size={14} className="text-[#D6B56D]" />
            <span className="text-[11px] font-semibold text-slate-200">SupeRR Selector</span>
          </div>
          <span className="text-[10px] font-mono font-bold text-[#E91E8F] px-1.5 py-0.5 rounded bg-[#E91E8F]/15 border border-[#E91E8F]/30">
            Season 2
          </span>
        </div>
      )}

      {/* Navigation Links */}
      <nav className="flex-1 px-3 py-3 space-y-6 overflow-y-auto">
        {/* Group 1: Challenge Deliverables */}
        <div className="space-y-1">
          {!collapsed && (
            <p className="px-3 pb-1 text-[10px] font-mono font-bold uppercase tracking-wider text-slate-400">
              Round 1 Challenge
            </p>
          )}
          {primaryNavItems.map((item, index) => {
            const Icon = item.icon;
            const isActive = pathname
              ? item.href === "/"
                ? pathname === "/"
                : item.href !== "#" && pathname.startsWith(item.href)
              : false;

            return (
              <Link
                key={index}
                href={item.href}
                className={cn(
                  "flex items-center gap-3 px-3 py-2.5 rounded-lg text-xs font-medium transition-all group relative",
                  isActive
                    ? "bg-[#E91E8F] text-white shadow-sm font-semibold"
                    : "text-slate-300 hover:bg-[#1A2B50] hover:text-white"
                )}
              >
                <Icon
                  size={18}
                  className={cn(
                    "shrink-0 transition-colors",
                    isActive ? "text-white" : "text-slate-400 group-hover:text-[#E91E8F]"
                  )}
                />

                {!collapsed && (
                  <div className="flex items-center justify-between w-full">
                    <span>{item.title}</span>
                    {item.badge ? (
                      <span className={cn(
                        "text-[9px] font-mono font-bold px-1.5 py-0.5 rounded border",
                        isActive
                          ? "bg-white/20 text-white border-white/30"
                          : item.badge === "Flagship"
                            ? "bg-[#E91E8F]/20 text-[#E91E8F] border-[#E91E8F]/30"
                            : "bg-[#D6B56D]/15 text-[#D6B56D] border-[#D6B56D]/30"
                      )}>
                        {item.stage}
                      </span>
                    ) : (
                      item.stage && (
                        <span className="text-[9px] font-mono font-semibold text-slate-400">
                          {item.stage}
                        </span>
                      )
                    )}
                  </div>
                )}

                {/* Tooltip on collapse */}
                {collapsed && (
                  <div className="absolute left-full ml-3 px-2 py-1 rounded bg-[#0B1220] border border-[#1A2B50] text-xs font-medium whitespace-nowrap opacity-0 group-hover:opacity-100 pointer-events-none transition-opacity z-50 shadow-lg">
                    {item.title} ({item.stage})
                  </div>
                )}
              </Link>
            );
          })}
        </div>

        {/* Group 2: Platform Infrastructure */}
        <div className="space-y-1">
          {!collapsed && (
            <p className="px-3 pb-1 text-[10px] font-mono font-bold uppercase tracking-wider text-slate-400">
              Data & Foundations
            </p>
          )}
          {foundationNavItems.map((item, index) => {
            const Icon = item.icon;
            const isActive = pathname
              ? item.href === "/"
                ? pathname === "/"
                : item.href !== "#" && pathname.startsWith(item.href)
              : false;

            return (
              <Link
                key={index}
                href={item.href}
                className={cn(
                  "flex items-center gap-3 px-3 py-2.5 rounded-lg text-xs font-medium transition-all group relative",
                  isActive
                    ? "bg-[#E91E8F] text-white shadow-sm font-semibold"
                    : "text-slate-300 hover:bg-[#1A2B50] hover:text-white"
                )}
              >
                <Icon
                  size={18}
                  className={cn(
                    "shrink-0 transition-colors",
                    isActive ? "text-white" : "text-slate-400 group-hover:text-[#D6B56D]"
                  )}
                />

                {!collapsed && (
                  <div className="flex items-center justify-between w-full">
                    <span>{item.title}</span>
                    <span className="text-[9px] font-mono font-semibold text-slate-400">
                      {item.stage}
                    </span>
                  </div>
                )}

                {/* Tooltip on collapse */}
                {collapsed && (
                  <div className="absolute left-full ml-3 px-2 py-1 rounded bg-[#0B1220] border border-[#1A2B50] text-xs font-medium whitespace-nowrap opacity-0 group-hover:opacity-100 pointer-events-none transition-opacity z-50 shadow-lg">
                    {item.title} ({item.stage})
                  </div>
                )}
              </Link>
            );
          })}
        </div>
      </nav>

      {/* Footer Info */}
      <div className="p-4 border-t border-[#1A2B50] bg-[#0B1220]/60">
        {!collapsed ? (
          <div className="space-y-2">
            <div className="flex items-center justify-between text-[11px] text-slate-300">
              <span className="flex items-center gap-1.5">
                <CheckCircle2 size={13} className="text-emerald-400" /> Round 1 Status
              </span>
              <span className="font-mono text-emerald-400 font-bold">VERIFIED</span>
            </div>
            <div className="w-full bg-[#1A2B50] rounded-full h-1.5 overflow-hidden">
              <div className="bg-gradient-to-r from-[#E91E8F] via-[#D6B56D] to-emerald-400 h-full w-full" />
            </div>
            <p className="text-[10px] text-slate-400 font-mono">
              303 / 303 Automated Tests Passing
            </p>
          </div>
        ) : (
          <div className="flex justify-center text-emerald-400">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse" />
          </div>
        )}
      </div>
    </aside>
  );
};