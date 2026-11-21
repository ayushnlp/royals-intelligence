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
      bg: "bg-[#15966B]/10 border-[#15966B]/30 text-[#15966B]",
      dot: "bg-[#15966B]",
      defaultLabel: "Healthy / Online",
    },
    standby: {
      bg: "bg-[#FCE8F0] border-[#E7EAF0] text-[#17294B]",
      dot: "bg-[#17294B]/60",
      defaultLabel: "Standby / Ready",
    },
    pending: {
      bg: "bg-[#FCE8F0] border-[#E7EAF0] text-[#17294B]",
      dot: "bg-[#17294B]/60",
      defaultLabel: "Integration Pending",
    },
    degraded: {
      bg: "bg-[#F28C28]/10 border-[#F28C28]/30 text-[#F28C28]",
      dot: "bg-[#F28C28]",
      defaultLabel: "Degraded",
    },
    stage0: {
      bg: "bg-[#FCE8F0] border-[#E4005A]/30 text-[#E4005A]",
      dot: "bg-[#E4005A]",
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
