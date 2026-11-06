import React from "react";
import {
  Shield,
  Layers,
  Server,
  Database,
  Cpu,
  ArrowRight,
  Info,
  Clock,
  CheckCircle2,
} from "lucide-react";
import { StatCard } from "@/components/ui/StatCard";
import { StatusBadge } from "@/components/ui/StatusBadge";
import { ModuleCard } from "@/components/ui/ModuleCard";
import { AnalyticalModule } from "@/types";

const plannedModules: AnalyticalModule[] = [
  {
    id: "mod-01",
    number: 1,
    title: "IPL 2026 Season Intelligence",
    category: "In-Season",
    stage: 9,
    status: "Data integration pending",
    description:
      "Campaign trajectory, Net Run Rate sensitivity, and playoff qualification Monte Carlo simulations.",
  },
  {
    id: "mod-02",
    number: 2,
    title: "Match-by-Match Intelligence",
    category: "In-Season",
    stage: 9,
    status: "Data integration pending",
    description:
      "Opponent weakness dossiers, phase leverage tracking (PP, Middle, Death), and real-time Win Probability Added (WPA).",
  },
  {
    id: "mod-03",
    number: 3,
    title: "Stadium & Venue Intelligence",
    category: "Match & Venue",
    stage: 5,
    status: "Data integration pending",
    description:
      "Asymmetric boundary lengths, altitude air-density coefficients, and first-innings par score decay models.",
  },
  {
    id: "mod-04",
    number: 4,
    title: "Pitch & Weather Intelligence",
    category: "Match & Venue",
    stage: 5,
    status: "Data integration pending",
    description:
      "Black soil vs red soil wear curves, spin turn degrees, and dew-point ball grip impact regressions.",
  },
  {
    id: "mod-05",
    number: 5,
    title: "Batting Diagnostics & Splits",
    category: "Player Performance",
    stage: 3,
    status: "Data integration pending",
    description:
      "Control percentage, dot ball mitigation index, entry point acceleration curves, and pace-vs-spin boundary frequency.",
  },
  {
    id: "mod-06",
    number: 6,
    title: "Bowling Mechanics & Variations",
    category: "Player Performance",
    stage: 4,
    status: "Data integration pending",
    description:
      "Release point consistency, length cluster strike zones, and slower-ball disguise efficacy.",
  },
  {
    id: "mod-08",
    number: 8,
    title: "Uncapped Talent Discovery",
    category: "Talent & Scouting",
    stage: 8,
    status: "Data integration pending",
    description:
      "Cross-competition normalization for domestic SMAT, Ranji, and VHT with raw biomechanical pace/striking indicators.",
  },
  {
    id: "mod-11",
    number: 11,
    title: "Player vs Player Matchups",
    category: "Player Performance",
    stage: 6,
    status: "Data integration pending",
    description:
      "Granular batter-vs-bowler head-to-head empirical dossiers and archetype clustering for low-sample pairs.",
  },
  {
    id: "mod-13",
    number: 13,
    title: "Playing XI & Impact Player Optimizer",
    category: "Match & Venue",
    stage: 7,
    status: "Data integration pending",
    description:
      "Integer Linear Programming (ILP) optimizer for dynamic batting-first vs bowling-first substitution matrices.",
  },
  {
    id: "mod-15",
    number: 15,
    title: "IPL 2027 Auction Decision Hub",
    category: "Auction & Roster",
    stage: 12,
    status: "Data integration pending",
    description:
      "Shadow auction simulator, dynamic purse exhaustion tracker, and Wins Above Replacement (WAR) per INR crore.",
  },
  {
    id: "mod-20",
    number: 20,
    title: "Model Explainability & Confidence",
    category: "Core Science",
    stage: 1,
    status: "Data integration pending",
    description:
      "Sample size confidence bands (Wilson score / Bayesian priors) and SHAP feature attributions on all analytical models.",
  },
  {
    id: "mod-22",
    number: 22,
    title: "Replacement & Upgrade Simulator",
    category: "Auction & Roster",
    stage: 11,
    status: "Data integration pending",
    description:
      "Monte Carlo roster simulation calculating delta in expected season points for injury replacement scenarios.",
  },
];

export default function OverviewPage() {
  return (
    <div className="space-y-8">
      {/* Hero / Stage Status Banner */}
      <div className="relative rounded-2xl bg-gradient-to-r from-[#101C37] via-[#1A2B50] to-[#101C37] p-6 md:p-8 text-white shadow-lg overflow-hidden border border-[#1A2B50]">
        <div className="relative z-10 max-w-3xl">
          <div className="flex flex-wrap items-center gap-2 mb-3">
            <span className="px-3 py-1 rounded-full text-xs font-mono font-bold bg-[#E91E8F] text-white">
              STAGE 0 INITIALIZED
            </span>
            <span className="px-3 py-1 rounded-full text-xs font-mono bg-[#D6B56D]/20 text-[#D6B56D] border border-[#D6B56D]/40">
              RAJASTHAN ROYALS CRICKET PLATFORM
            </span>
            <span className="text-xs text-slate-400 font-mono">
              Primary Season: IPL 2026
            </span>
          </div>

          <h1 className="text-2xl md:text-3xl font-extrabold tracking-tight text-white mb-2">
            Royals Intelligence Architectural Foundation
          </h1>
          <p className="text-sm text-slate-300 leading-relaxed mb-6">
            Foundation baseline established. Repository structure, Next.js application shell,
            FastAPI async engine, PostgreSQL database connection architecture, and comprehensive
            documentation suite initialized. Cricket analytics data integration commences in Stage 1.
          </p>

          <div className="inline-flex items-center gap-3 bg-[#0B1220]/80 border border-slate-700/60 rounded-xl px-4 py-2 text-xs">
            <span className="w-2 h-2 rounded-full bg-amber-400 animate-pulse" />
            <span className="font-semibold text-slate-200">
              Strict Verification Policy:
            </span>
            <span className="text-slate-400">
              No fabricated cricket statistics or synthetic scores are rendered.
            </span>
          </div>
        </div>

        {/* Decorative Watermark */}
        <div className="absolute right-4 -bottom-6 text-[#1A2B50]/40 font-black text-9xl select-none pointer-events-none font-mono">
          RR
        </div>
      </div>

      {/* Infrastructure Readiness Metrics (True Architectural Telemetry) */}
      <section className="space-y-3">
        <div className="flex items-center justify-between">
          <h2 className="text-sm font-bold uppercase tracking-wider text-slate-500">
            System & Infrastructure Readiness
          </h2>
          <span className="text-xs font-mono text-slate-400">Environment: Development</span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <StatCard
            title="Backend Service"
            value="FastAPI 0.115"
            subtitle="Async Python 3.12 application with /health and /api/v1/health probes"
            badgeText="Verified"
            icon={<Server size={18} />}
          />
          <StatCard
            title="Database Architecture"
            value="PostgreSQL 16"
            subtitle="SQLAlchemy 2.0 Async + Alembic migration harness initialized"
            badgeText="AsyncPG Engine"
            icon={<Database size={18} />}
          />
          <StatCard
            title="Frontend Application"
            value="Next.js 15"
            subtitle="React 19 App Router with Rajasthan Royals brand design tokens"
            badgeText="TypeScript"
            icon={<Layers size={18} />}
          />
          <StatCard
            title="Project Roadmap"
            value="Stage 0 / 13"
            subtitle="Baseline initialization complete. Next: Stage 1 Data Ingestion"
            badgeText="On Schedule"
            icon={<Cpu size={18} />}
          />
        </div>
      </section>

      {/* Roadmap Architecture Status Card */}
      <section className="bg-white rounded-2xl border border-slate-200/80 p-6 shadow-sm">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6 pb-6 border-b border-slate-100">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <Shield size={18} className="text-[#E91E8F]" />
              <h3 className="text-lg font-bold text-[#101C37]">
                Stage 0 Acceptance & Verification Status
              </h3>
            </div>
            <p className="text-xs text-slate-500">
              Architectural checkpoints required prior to Stage 1 Data Ingestion sign-off.
            </p>
          </div>

          <StatusBadge status="stage0" label="Stage 0 Complete" />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="p-4 rounded-xl bg-slate-50 border border-slate-200/60">
            <div className="flex items-center gap-2 text-xs font-bold text-[#101C37] mb-1">
              <CheckCircle2 size={16} className="text-emerald-600" />
              <span>Independent Monorepo</span>
            </div>
            <p className="text-xs text-slate-500">
              Clean `royals-intelligence` workspace without legacy dependencies or imports.
            </p>
          </div>

          <div className="p-4 rounded-xl bg-slate-50 border border-slate-200/60">
            <div className="flex items-center gap-2 text-xs font-bold text-[#101C37] mb-1">
              <CheckCircle2 size={16} className="text-emerald-600" />
              <span>Design System</span>
            </div>
            <p className="text-xs text-slate-500">
              Royals Navy (#101C37), Pink (#E91E8F), and Gold (#D6B56D) tokens integrated.
            </p>
          </div>

          <div className="p-4 rounded-xl bg-slate-50 border border-slate-200/60">
            <div className="flex items-center gap-2 text-xs font-bold text-[#101C37] mb-1">
              <Clock size={16} className="text-[#D6B56D]" />
              <span>Stage 1 Awaiting Approval</span>
            </div>
            <p className="text-xs text-slate-500">
              Historical match data parsers and Parquet analytical storage ready to initiate.
            </p>
          </div>
        </div>
      </section>

      {/* Analytical Modules Blueprint Directory */}
      <section className="space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
          <div>
            <h2 className="text-base font-bold text-[#101C37]">
              Planned Analytics Modules (Stage 1 to 13)
            </h2>
            <p className="text-xs text-slate-500">
              Architectural blueprints for 20 core analytical modules and 6 advanced features.
            </p>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-xs text-slate-400 font-mono">
              Status: Data integration pending
            </span>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {plannedModules.map((module) => (
            <ModuleCard key={module.id} module={module} />
          ))}
        </div>
      </section>

      {/* Stage 1 Transition Callout */}
      <div className="rounded-xl border border-dashed border-slate-300 p-5 bg-slate-50/50 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div className="flex items-start gap-3">
          <div className="p-2 rounded-lg bg-pink-100/60 text-[#E91E8F] shrink-0 mt-0.5">
            <Info size={16} />
          </div>
          <div>
            <h4 className="text-xs font-bold text-[#101C37]">
              Next Milestone: Stage 1 — Data Ingestion Infrastructure
            </h4>
            <p className="text-xs text-slate-500 leading-relaxed">
              Stage 0 criteria are completely fulfilled. Per strict governance rules, Stage 1
              will only commence upon explicit user confirmation.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
