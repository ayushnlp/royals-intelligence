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
  Shield,
  Crosshair,
  Sparkles,
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
    },
    {
      title: "Pressure Intelligence",
      href: "/pressure",
      icon: Shield,
    },
    {
      title: "Tactical Intelligence",
      href: "/tactical",
      icon: Crosshair,
    },
    {
      title: "Uncapped Intelligence",
      href: "/uncapped",
      icon: Sparkles,
    },
  ];

  const foundationNavItems = [
    {
      title: "Domestic & Matches",
      href: "/domestic",
      icon: Swords,
    },
    {
      title: "Venue & Pitch",
      href: "/venues",
      icon: MapPin,
    },
    {
      title: "Data Acquisition",
      href: "/acquisition",
      icon: DownloadCloud,
    },
  ];

  const renderNavItem = (item: { title: string; href: string; icon: React.ComponentType<{ size?: number; className?: string }> }) => {
    const Icon = item.icon;
    const isActive = pathname
      ? item.href === "/"
        ? pathname === "/"
        : item.href !== "#" && pathname.startsWith(item.href)
      : false;

    return (
      <Link
        key={item.href}
        href={item.href}
        className={cn(
          "flex items-center gap-3 px-3 py-2.5 rounded-lg text-xs transition-colors group relative",
          isActive
            ? "bg-white/[0.08] text-white font-medium border-l-2 border-[#E91E8F] pl-2.5"
            : "text-slate-400 hover:text-slate-100 hover:bg-white/[0.04]"
        )}
      >
        <Icon
          size={17}
          className={cn(
            "shrink-0 transition-colors",
            isActive ? "text-[#E91E8F]" : "text-slate-400 group-hover:text-slate-200"
          )}
        />

        {!collapsed && (
          <span className="truncate tracking-tight">{item.title}</span>
        )}

        {/* Collapsed Tooltip */}
        {collapsed && (
          <div className="absolute left-full ml-2.5 px-2.5 py-1 rounded-md bg-[#0B1220] border border-slate-800 text-[11px] font-medium text-slate-200 whitespace-nowrap opacity-0 group-hover:opacity-100 pointer-events-none transition-opacity z-50 shadow-xl">
            {item.title}
          </div>
        )}
      </Link>
    );
  };

  return (
    <aside
      className={cn(
        "relative flex flex-col bg-[#101C37] text-slate-200 transition-all duration-200 z-30 min-h-screen border-r border-slate-800/80 select-none",
        collapsed ? "w-16" : "w-60",
        className
      )}
    >
      {/* Brand Identity Header */}
      <div className="flex items-center justify-between px-4 h-16 border-b border-slate-800/60">
        {!collapsed ? (
          <Link href="/" className="flex items-center gap-2.5 group">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-tr from-[#E91E8F] to-[#D6B56D] p-px flex items-center justify-center shrink-0">
              <div className="w-full h-full bg-[#101C37] rounded-[7px] flex items-center justify-center">
                <span className="font-bold text-xs text-transparent bg-clip-text bg-gradient-to-r from-[#E91E8F] to-[#D6B56D]">
                  RR
                </span>
              </div>
            </div>
            <div className="leading-none">
              <span className="font-bold text-xs tracking-wider text-white block">
                ROYALS
              </span>
              <span className="text-[9px] font-mono tracking-widest text-[#D6B56D] font-medium uppercase mt-0.5 block">
                INTELLIGENCE
              </span>
            </div>
          </Link>
        ) : (
          <Link href="/" className="mx-auto w-8 h-8 rounded-lg bg-gradient-to-tr from-[#E91E8F] to-[#D6B56D] p-px flex items-center justify-center">
            <div className="w-full h-full bg-[#101C37] rounded-[7px] flex items-center justify-center">
              <span className="font-bold text-xs text-[#E91E8F]">RR</span>
            </div>
          </Link>
        )}

        <button
          onClick={() => setCollapsed(!collapsed)}
          className="hidden md:flex p-1 rounded-md text-slate-400 hover:text-slate-200 hover:bg-white/[0.06] transition-colors"
          aria-label={collapsed ? "Expand sidebar" : "Collapse sidebar"}
        >
          {collapsed ? <ChevronRight size={15} /> : <ChevronLeft size={15} />}
        </button>
      </div>

      {/* Navigation Sections */}
      <nav className="flex-1 px-2.5 py-4 space-y-5 overflow-y-auto">
        {/* Primary Intelligence Section */}
        <div className="space-y-0.5">
          {!collapsed && (
            <p className="px-3 pb-1.5 text-[10px] font-mono font-medium tracking-wider text-slate-400 uppercase">
              Intelligence
            </p>
          )}
          {primaryNavItems.map(renderNavItem)}
        </div>

        {/* Data & Competitions Section */}
        <div className="space-y-0.5 pt-2 border-t border-slate-800/40">
          {!collapsed && (
            <p className="px-3 pb-1.5 text-[10px] font-mono font-medium tracking-wider text-slate-400 uppercase">
              Data & Matches
            </p>
          )}
          {foundationNavItems.map(renderNavItem)}
        </div>
      </nav>

      {/* Understated Minimalist Footer */}
      {!collapsed ? (
        <div className="px-4 py-3 border-t border-slate-800/60 flex items-center justify-between text-[11px] text-slate-400">
          <span className="font-mono text-[10px] text-slate-400">v4.2 • SupeRR 2</span>
          <span className="text-[10px] font-mono text-[#D6B56D]">RR Analytics</span>
        </div>
      ) : (
        <div className="py-3 border-t border-slate-800/60 flex justify-center">
          <span className="w-1.5 h-1.5 rounded-full bg-[#D6B56D]" />
        </div>
      )}
    </aside>
  );
};