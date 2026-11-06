import React from "react";
import { AnalyticalModule } from "@/types";
import { StatusBadge } from "./StatusBadge";

interface ModuleCardProps {
  module: AnalyticalModule;
}

export const ModuleCard: React.FC<ModuleCardProps> = ({ module }) => {
  return (
    <div className="bg-white rounded-xl border border-slate-200/80 p-5 shadow-sm hover:border-[#E91E8F]/40 transition-all group flex flex-col justify-between">
      <div>
        <div className="flex items-center justify-between mb-3">
          <span className="text-[11px] font-mono font-bold text-slate-400 group-hover:text-[#E91E8F] transition-colors">
            MOD-{String(module.number).padStart(2, "0")}
          </span>
          <span className="text-[11px] font-medium text-slate-500 bg-slate-100 px-2 py-0.5 rounded">
            Stage {module.stage}
          </span>
        </div>

        <h4 className="text-base font-semibold text-[#101C37] mb-2 group-hover:text-[#E91E8F] transition-colors">
          {module.title}
        </h4>

        <p className="text-xs text-slate-600 line-clamp-3 mb-4 leading-relaxed">
          {module.description}
        </p>
      </div>

      <div className="pt-3 border-t border-slate-100 flex items-center justify-between mt-auto">
        <StatusBadge status="pending" label="Integration Pending" />
        <span className="text-[11px] font-medium text-slate-400 font-mono">
          {module.category}
        </span>
      </div>
    </div>
  );
};
