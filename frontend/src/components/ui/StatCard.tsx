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
        "bg-white rounded-xl border border-slate-200/80 p-5 shadow-2xs hover:shadow-xs transition-shadow relative overflow-hidden",
        className
      )}
    >
      <div className="flex items-center justify-between mb-3">
        <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
          {title}
        </span>
        {icon && (
          <div className="p-2 rounded-lg bg-slate-50 text-[#111C38] border border-slate-100">
            {icon}
          </div>
        )}
      </div>

      <div className="flex items-baseline gap-2 mb-1">
        <h3 className="text-2xl font-bold tracking-tight text-[#111827] font-mono">
          {value}
        </h3>
        {badgeText && (
          <span className="text-[11px] font-medium px-2 py-0.5 rounded-full bg-slate-100 text-slate-700">
            {badgeText}
          </span>
        )}
      </div>

      <p className="text-xs text-slate-500 leading-relaxed">{subtitle}</p>

      {/* Royals Pink subtle accent stripe at top */}
      <div className="absolute top-0 left-0 right-0 h-0.5 bg-gradient-to-r from-[#111C38] via-[#E91E8C] to-[#D6B56D]" />
    </div>
  );
};
