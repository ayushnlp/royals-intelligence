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
      bg: "bg-emerald-500/10 border-emerald-500/30 text-emerald-600 dark:text-emerald-400",
      dot: "bg-emerald-500",
      defaultLabel: "Healthy / Online",
    },
    standby: {
      bg: "bg-amber-500/10 border-amber-500/30 text-amber-600 dark:text-amber-400",
      dot: "bg-amber-500",
      defaultLabel: "Standby / Ready",
    },
    pending: {
      bg: "bg-blue-500/10 border-blue-500/30 text-blue-600 dark:text-blue-400",
      dot: "bg-blue-500",
      defaultLabel: "Integration Pending",
    },
    degraded: {
      bg: "bg-rose-500/10 border-rose-500/30 text-rose-600 dark:text-rose-400",
      dot: "bg-rose-500",
      defaultLabel: "Degraded",
    },
    stage0: {
      bg: "bg-pink-500/10 border-pink-500/30 text-pink-600 dark:text-pink-400",
      dot: "bg-[#E91E8F]",
      defaultLabel: "Stage 0 Baseline",
    },
  };

  const config = configs[status] || configs.pending;

  return (
    <span
      className={cn(
        "inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium border",
        config.bg,
        className
      )}
    >
      <span className={cn("w-1.5 h-1.5 rounded-full animate-pulse", config.dot)} />
      {label || config.defaultLabel}
    </span>
  );
};
