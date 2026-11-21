import React from "react";
import { AnalyticalModule } from "@/types";
import { StatusBadge } from "./StatusBadge";

interface ModuleCardProps {
  module: AnalyticalModule;
}

export const ModuleCard: React.FC<ModuleCardProps> = ({ module }) => {
  return (
    <div className="bg-white rounded-xl border border-[#31136C]/12 p-5 shadow-soft hover:border-[#950460] hover:shadow-elevation transition-all group flex flex-col justify-between">
      <div>
        <div className="flex items-center justify-between mb-3">
          <span className="text-[11px] font-mono font-bold text-[#31136C]/70 group-hover:text-[#31136C] transition-colors">
            MOD-{String(module.number).padStart(2, "0")}
          </span>
          <span className="text-[11px] font-medium text-[#31136C] bg-[#31136C]/06 px-2 py-0.5 rounded">
            Stage {module.stage}
          </span>
        </div>

        <h4 className="text-base font-semibold text-[#31136C] mb-2 group-hover:text-[#950460] transition-colors font-heading">
          {module.title}
        </h4>

        <p className="text-xs text-[#31136C]/70 line-clamp-3 mb-4 leading-relaxed">
          {module.description}
        </p>
      </div>

      <div className="pt-3 border-t border-[#31136C]/12 flex items-center justify-between mt-auto">
        <StatusBadge status="pending" label="Integration Pending" />
        <span className="text-[11px] font-medium text-[#31136C]/70 font-mono">
          {module.category}
        </span>
      </div>
    </div>
  );
};
