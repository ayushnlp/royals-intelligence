"use client";

import React, { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  Home,
  LayoutDashboard,
  Shield,
  Crosshair,
  Sparkles,
  Swords,
  MapPin,
  DownloadCloud,
  ChevronLeft,
  ChevronRight,
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
      title: "Public Home",
      href: "/",
      icon: Home,
    },
    {
      title: "Executive Overview",
      href: "/overview",
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

  const renderNavItem = (item: {
    title: string;
    href: string;
    icon: React.ComponentType<{ size?: number; className?: string }>;
  }) => {
    const Icon = item.icon;
    const isActive = pathname
      ? item.href === "/"
        ? pathname === "/"
        : pathname === item.href || pathname.startsWith(item.href + "/")
      : false;

    return (
      <Link
        key={item.href}
        href={item.href}
        className={cn(
          "flex items-center gap-3 px-3 py-2 rounded-lg text-xs transition-all duration-150 group relative",
          isActive
            ? "bg-[#F8E8EF] text-[#D4145A] font-bold border-l-4 border-[#D4145A] pl-2.5 shadow-sm"
            : "text-[#52627A] hover:text-[#D4145A] hover:bg-[#F8E8EF]"
        )}
      >
        <Icon
          size={16}
          className={cn(
            "shrink-0 transition-colors",
            isActive ? "text-[#D4145A]" : "text-[#52627A] group-hover:text-[#D4145A]"
          )}
        />

        {!collapsed && (
          <span className="truncate tracking-tight font-medium">{item.title}</span>
        )}

        {/* Collapsed Tooltip */}
        {collapsed && (
          <div className="absolute left-full ml-2.5 px-2.5 py-1 rounded-md bg-[#101D3A] text-white text-[11px] font-medium whitespace-nowrap opacity-0 group-hover:opacity-100 pointer-events-none transition-opacity z-50 shadow-elevation">
            {item.title}
          </div>
        )}
      </Link>
    );
  };

  return (
    <aside
      className={cn(
        "relative flex flex-col bg-white text-[#101D3A] transition-all duration-200 z-30 min-h-screen border-r border-[#E7EAF0] select-none",
        collapsed ? "w-16" : "w-64",
        className
      )}
    >
      {/* Brand Identity Header */}
      <div className="flex items-center justify-between px-4 h-16 border-b border-[#E7EAF0]">
        {!collapsed ? (
          <Link href="/" className="flex items-center gap-2.5 group">
            <div className="w-8 h-8 rounded-lg bg-[#D4145A] border border-[#D4145A] flex items-center justify-center shrink-0 transition-transform group-hover:scale-105 shadow-sm">
              <span className="font-heading font-extrabold text-xs text-white">
                RR
              </span>
            </div>
            <div className="leading-tight">
              <div className="flex items-center gap-1.5">
                <span className="font-heading font-extrabold text-xs tracking-tight text-[#101D3A] block">
                  ROYALS
                </span>
                <span className="text-[9px] font-mono font-bold px-1 py-0.2 rounded bg-[#D4145A]/10 text-[#D4145A] border border-[#D4145A]/30">
                  S02
                </span>
              </div>
              <span className="text-[9px] font-mono tracking-wider text-[#52627A] font-semibold uppercase block">
                INTELLIGENCE
              </span>
            </div>
          </Link>
        ) : (
          <Link
            href="/"
            className="mx-auto w-8 h-8 rounded-lg bg-[#D4145A] border border-[#D4145A] flex items-center justify-center transition-transform hover:scale-105 shadow-sm"
            title="Royals Intelligence (Season 02)"
          >
            <span className="font-heading font-extrabold text-xs text-white">RR</span>
          </Link>
        )}

        <button
          onClick={() => setCollapsed(!collapsed)}
          className="hidden md:flex p-1 rounded-md text-[#52627A] hover:text-[#D4145A] hover:bg-[#F8E8EF] transition-colors"
          aria-label={collapsed ? "Expand sidebar" : "Collapse sidebar"}
        >
          {collapsed ? <ChevronRight size={15} /> : <ChevronLeft size={15} />}
        </button>
      </div>

      {/* Navigation Sections */}
      <nav className="flex-1 px-3 py-4 space-y-5 overflow-y-auto">
        {/* Primary Intelligence Section */}
        <div className="space-y-1">
          {!collapsed && (
            <p className="px-3 pb-1 text-[10px] font-mono font-bold tracking-wider text-[#D4145A] uppercase">
              Intelligence
            </p>
          )}
          {primaryNavItems.map(renderNavItem)}
        </div>

        {/* Data & Matches Section */}
        <div className="space-y-1 pt-3 border-t border-[#E7EAF0]">
          {!collapsed && (
            <p className="px-3 pb-1 text-[10px] font-mono font-bold tracking-wider text-[#D4145A] uppercase">
              Data & Foundation
            </p>
          )}
          {foundationNavItems.map(renderNavItem)}
        </div>
      </nav>

      {/* Understated Minimalist Footer */}
      {!collapsed ? (
        <div className="px-4 py-3 border-t border-[#E7EAF0] flex items-center justify-between text-[11px] text-[#52627A] bg-[#F8E8EF]">
          <span className="font-mono text-[10px] text-[#52627A]">Season 02 · R1</span>
          <span className="text-[10px] font-mono font-bold text-[#D4145A]">
            RR Analytics
          </span>
        </div>
      ) : (
        <div className="py-3 border-t border-[#E7EAF0] flex justify-center bg-[#F8E8EF]">
          <span className="w-1.5 h-1.5 rounded-full bg-[#D4145A]" />
        </div>
      )}
    </aside>
  );
};
