import React from "react";
import { cn } from "@/lib/utils";

interface StatCardProps {
  title: string;
  value: string;
  subtitle: string;
  badgeText?: string;
  badgeStatus?: "healthy" | "standby" | "pending" | "stage0";
  icon?: React.ReactNode;
  className?: string;
}

export const StatCard: React.FC<StatCardProps> = ({
  title,
  value,
  subtitle,
  badgeText,
  icon,
  className,
}) => {
  return (
    <div
      className={cn(
        "bg-white rounded-xl border border-[#31136C]/12 p-5 shadow-soft hover:shadow-elevation transition-all relative overflow-hidden",
        className
      )}
    >
      <div className="flex items-center justify-between mb-3">
        <span className="text-xs font-semibold text-[#31136C]/70 uppercase tracking-wider">
          {title}
        </span>
        {icon && (
          <div className="p-2 rounded-lg bg-[#F7F6FB] text-[#950460] border border-[#31136C]/12">
            {icon}
          </div>
        )}
      </div>

      <div className="flex items-baseline gap-2 mb-1">
        <h3 className="text-2xl font-bold tracking-tight text-[#31136C] font-mono">
          {value}
        </h3>
        {badgeText && (
          <span className="text-[11px] font-bold px-2 py-0.5 rounded-full bg-[#950460]/10 text-[#950460] border border-[#950460]/30">
            {badgeText}
          </span>
        )}
      </div>

      <p className="text-xs text-[#31136C]/70 leading-relaxed">{subtitle}</p>

      {/* Rajasthan Royals signature Indigo-to-Cardinal Pink accent stripe */}
      <div className="absolute top-0 left-0 right-0 h-0.5 bg-gradient-to-r from-[#31136C] to-[#950460]" />
    </div>
  );
};
