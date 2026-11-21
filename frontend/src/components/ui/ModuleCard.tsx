import React from "react";
import { AnalyticalModule } from "@/types";
import { StatusBadge } from "./StatusBadge";

interface ModuleCardProps {
  module: AnalyticalModule;
}

export const ModuleCard: React.FC<ModuleCardProps> = ({ module }) => {
  return (
    <div className="bg-white rounded-xl border border-[#E7EAF0] p-5 shadow-soft hover:border-[#D4145A] hover:shadow-elevation transition-all group flex flex-col justify-between">
      <div>
        <div className="flex items-center justify-between mb-3">
          <span className="text-[11px] font-mono font-bold text-[#52627A] group-hover:text-[#101D3A] transition-colors">
            MOD-{String(module.number).padStart(2, "0")}
          </span>
          <span className="text-[11px] font-medium text-[#101D3A] bg-[#F8E8EF] px-2 py-0.5 rounded">
            Stage {module.stage}
          </span>
        </div>

        <h4 className="text-base font-semibold text-[#101D3A] mb-2 group-hover:text-[#D4145A] transition-colors font-heading">
          {module.title}
        </h4>

        <p className="text-xs text-[#52627A] line-clamp-3 mb-4 leading-relaxed">
          {module.description}
        </p>
      </div>

      <div className="pt-3 border-t border-[#E7EAF0] flex items-center justify-between mt-auto">
        <StatusBadge status="pending" label="Integration Pending" />
        <span className="text-[11px] font-medium text-[#52627A] font-mono">
          {module.category}
        </span>
      </div>
    </div>
  );
};
