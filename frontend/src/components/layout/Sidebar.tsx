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
            ? "bg-[#950460]/10 text-[#950460] font-bold border-l-2 border-[#950460] pl-2.5 shadow-2xs"
            : "text-[#31136C]/70 hover:text-[#950460] hover:bg-[#F7F6FB]"
        )}
      >
        <Icon
          size={16}
          className={cn(
            "shrink-0 transition-colors",
            isActive ? "text-[#950460]" : "text-[#31136C]/70 group-hover:text-[#950460]"
          )}
        />

        {!collapsed && (
          <span className="truncate tracking-tight font-medium">{item.title}</span>
        )}

        {/* Collapsed Tooltip */}
        {collapsed && (
          <div className="absolute left-full ml-2.5 px-2.5 py-1 rounded-md bg-[#31136C] text-white text-[11px] font-medium whitespace-nowrap opacity-0 group-hover:opacity-100 pointer-events-none transition-opacity z-50 shadow-elevation">
            {item.title}
          </div>
        )}
      </Link>
    );
  };

  return (
    <aside
      className={cn(
        "relative flex flex-col bg-white text-[#31136C] transition-all duration-200 z-30 min-h-screen border-r border-[#31136C]/12 select-none",
        collapsed ? "w-16" : "w-64",
        className
      )}
    >
      {/* Brand Identity Header */}
      <div className="flex items-center justify-between px-4 h-16 border-b border-[#31136C]/12">
        {!collapsed ? (
          <Link href="/" className="flex items-center gap-2.5 group">
            <div className="w-8 h-8 rounded-lg bg-[#950460] border border-[#950460] flex items-center justify-center shrink-0 transition-transform group-hover:scale-105 shadow-sm">
              <span className="font-heading font-extrabold text-xs text-white">
                RR
              </span>
            </div>
            <div className="leading-tight">
              <div className="flex items-center gap-1.5">
                <span className="font-heading font-extrabold text-xs tracking-tight text-[#31136C] block">
                  ROYALS
                </span>
                <span className="text-[9px] font-mono font-bold px-1 py-0.2 rounded bg-[#950460]/10 text-[#950460] border border-[#950460]/30">
                  S02
                </span>
              </div>
              <span className="text-[9px] font-mono tracking-wider text-[#31136C]/70 font-semibold uppercase block">
                INTELLIGENCE
              </span>
            </div>
          </Link>
        ) : (
          <Link
            href="/"
            className="mx-auto w-8 h-8 rounded-lg bg-[#950460] border border-[#950460] flex items-center justify-center transition-transform hover:scale-105 shadow-sm"
            title="Royals Intelligence (Season 02)"
          >
            <span className="font-heading font-extrabold text-xs text-white">RR</span>
          </Link>
        )}

        <button
          onClick={() => setCollapsed(!collapsed)}
          className="hidden md:flex p-1 rounded-md text-[#31136C]/70 hover:text-[#950460] hover:bg-[#F7F6FB] transition-colors"
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
            <p className="px-3 pb-1 text-[10px] font-mono font-bold tracking-wider text-[#950460] uppercase">
              Intelligence
            </p>
          )}
          {primaryNavItems.map(renderNavItem)}
        </div>

        {/* Data & Matches Section */}
        <div className="space-y-1 pt-3 border-t border-[#31136C]/12">
          {!collapsed && (
            <p className="px-3 pb-1 text-[10px] font-mono font-bold tracking-wider text-[#950460] uppercase">
              Data & Foundation
            </p>
          )}
          {foundationNavItems.map(renderNavItem)}
        </div>
      </nav>

      {/* Understated Minimalist Footer */}
      {!collapsed ? (
        <div className="px-4 py-3 border-t border-[#31136C]/12 flex items-center justify-between text-[11px] text-[#31136C]/70 bg-[#F7F6FB]">
          <span className="font-mono text-[10px] text-[#31136C]/70">Season 02 · R1</span>
          <span className="text-[10px] font-mono font-bold text-[#950460]">
            RR Analytics
          </span>
        </div>
      ) : (
        <div className="py-3 border-t border-[#31136C]/12 flex justify-center bg-[#F7F6FB]">
          <span className="w-1.5 h-1.5 rounded-full bg-[#950460]" />
        </div>
      )}
    </aside>
  );
};
