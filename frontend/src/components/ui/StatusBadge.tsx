import React from "react";
import { cn } from "@/lib/utils";

interface StatusBadgeProps {
  status: "healthy" | "standby" | "pending" | "degraded" | "stage0";
  label?: string;
  className?: string;
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({ status, label, className }) => {
  const configs = {
    healthy: {
      bg: "bg-[#950460]/10 border-[#950460]/30 text-[#950460]",
      dot: "bg-[#950460]",
      defaultLabel: "Healthy / Online",
    },
    standby: {
      bg: "bg-[#31136C]/08 border-[#31136C]/20 text-[#31136C]",
      dot: "bg-[#31136C]",
      defaultLabel: "Standby / Ready",
    },
    pending: {
      bg: "bg-[#31136C]/08 border-[#31136C]/20 text-[#31136C]",
      dot: "bg-[#31136C]",
      defaultLabel: "Integration Pending",
    },
    degraded: {
      bg: "bg-[#950460]/10 border-[#950460]/30 text-[#950460]",
      dot: "bg-[#950460]",
      defaultLabel: "Degraded",
    },
    stage0: {
      bg: "bg-[#950460]/10 border-[#950460]/30 text-[#31136C]",
      dot: "bg-[#950460]",
      defaultLabel: "Stage 0 Baseline",
    },
  };

  const config = configs[status] || configs.pending;

  return (
    <span
      className={cn(
        "inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold border",
        config.bg,
        className
      )}
    >
      <span className={cn("w-1.5 h-1.5 rounded-full", config.dot)} />
      {label || config.defaultLabel}
    </span>
  );
};
