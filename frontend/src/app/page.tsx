import React from "react";
import Link from "next/link";
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
  Crosshair,
  Award,
  Sparkles,
  Flame,
  TrendingUp,
  Target,
  Swords,
  MapPin,
  DownloadCloud,
  ExternalLink,
  HelpCircle,
  FileText,
  BarChart2,
} from "lucide-react";
import { StatCard } from "@/components/ui/StatCard";

export default function OverviewPage() {
  return (
    <div className="space-y-8">
      {/* ------------------------------------------------------------------- */}
      {/* 1. Official Challenge Hero Banner */}
      {/* ------------------------------------------------------------------- */}
      <div className="relative rounded-2xl bg-gradient-to-r from-[#101C37] via-[#1A2B50] to-[#101C37] p-6 md:p-8 text-white shadow-lg overflow-hidden border border-[#1A2B50]">
        <div className="relative z-10 max-w-3xl">
          <div className="flex flex-wrap items-center gap-2 mb-3">
            <span className="px-3 py-1 rounded-full text-xs font-mono font-bold bg-[#E91E8F] text-white flex items-center gap-1.5 shadow-sm">
              <Award size={13} />
              ROUND 1 VERIFIED
            </span>
            <span className="px-3 py-1 rounded-full text-xs font-mono bg-[#D6B56D]/20 text-[#D6B56D] border border-[#D6B56D]/40">
              SUPERR SELECTOR SEASON 2
            </span>
            <span className="text-xs text-slate-300 font-mono">
              Official Rajasthan Royals Challenge • 2022–2026 Data Pack
            </span>
          </div>

          <h1 className="text-2xl md:text-3xl font-extrabold tracking-tight text-white mb-2">
            The Most Reliable Players Under Pressure
          </h1>
          <p className="text-sm text-slate-300 leading-relaxed mb-6">
            Official SupeRR Selector Round 1 challenge decision engine. Context-stratified 12-cell baselines,
            Empirical Bayes shrinkage, and 1-SE Conservative PRI rankings across 200,999 deliveries in 883 matches.
            Verified Top 10 Batters and Top 10 Bowlers Under Pressure with complete 11-question candidate evidence profiles.
          </p>

          {/* Action Navigation Buttons */}
          <div className="flex flex-wrap items-center gap-3 mb-6">
            <Link
              href="/pressure"
              className="px-5 py-2.5 rounded-xl bg-[#E91E8F] text-white font-semibold text-xs shadow-lg shadow-[#E91E8F]/25 hover:bg-[#E91E8F]/90 transition-all flex items-center gap-2 group"
            >
              <Shield size={15} />
              <span>Launch Pressure Intelligence (Round 1 Flagship)</span>
              <ArrowRight size={14} className="group-hover:translate-x-0.5 transition-transform" />
            </Link>

            <Link
              href="/tactical"
              className="px-5 py-2.5 rounded-xl bg-[#101C37] text-[#D6B56D] border border-[#D6B56D]/40 font-semibold text-xs hover:bg-[#1A2B50] transition-all flex items-center gap-2 group"
            >
              <Crosshair size={15} />
              <span>Explore Tactical Analytics (Stage 5)</span>
              <ArrowRight size={14} className="group-hover:translate-x-0.5 transition-transform" />
            </Link>

            <Link
              href="/pressure#methodology"
              className="px-4 py-2.5 rounded-xl bg-slate-800/80 text-slate-200 border border-slate-700/60 font-semibold text-xs hover:bg-slate-700/80 transition-all flex items-center gap-2"
            >
              <FileText size={15} className="text-[#D6B56D]" />
              <span>Read Methodology</span>
            </Link>
          </div>

          <div className="inline-flex items-center gap-3 bg-[#0B1220]/80 border border-slate-700/60 rounded-xl px-4 py-2 text-xs">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
            <span className="font-semibold text-slate-200">
              Official Data Governance Policy:
            </span>
            <span className="text-slate-400">
              Zero synthetic records. 100% verified against official competition data pack (SHA-256 sealed).
            </span>
          </div>
        </div>

        {/* Decorative Watermark */}
        <div className="absolute right-4 -bottom-6 text-[#1A2B50]/40 font-black text-9xl select-none pointer-events-none font-mono">
          RR
        </div>
      </div>

      {/* ------------------------------------------------------------------- */}
      {/* 2. System & Challenge Telemetry */}
      {/* ------------------------------------------------------------------- */}
      <section className="space-y-3">
        <div className="flex items-center justify-between">
          <h2 className="text-sm font-bold uppercase tracking-wider text-slate-500">
            System & Challenge Telemetry
          </h2>
          <span className="text-xs font-mono text-slate-400">Checkpoint: 6005022 (Sealed Baseline)</span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <StatCard
            title="Official Deliverables"
            value="Top 10 Batters & Bowlers"
            subtitle="Conservative PRI lower bound rankings with complete candidate evidence dossiers"
            badgeText="Sealed & Audited"
            icon={<Award size={18} />}
          />
          <StatCard
            title="Controlling Dataset"
            value="200,999 Balls"
            subtitle="883 matches across 141 competitions (IPL & Senior T20Is)"
            badgeText="192,709 Legal"
            icon={<Database size={18} />}
          />
          <StatCard
            title="Tactical Intelligence"
            value="10 REST APIs"
            subtitle="Phases, 30 strokes, 4-way handedness, 34 variations, radar speed"
            badgeText="Stage 5 Operational"
            icon={<Crosshair size={18} />}
          />
          <StatCard
            title="Statistical Reliability"
            value="303 / 303 Passed"
            subtitle="100% test pass rate across backend and Round 1 pressure verification suites"
            badgeText="Verified"
            icon={<CheckCircle2 size={18} />}
          />
        </div>
      </section>

      {/* ------------------------------------------------------------------- */}
      {/* 3. Official Round 1 Deliverables Showcase */}
      {/* ------------------------------------------------------------------- */}
      <section className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Batting Top 10 Showcase */}
        <div className="bg-white rounded-2xl border border-slate-200/80 p-6 shadow-sm flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between pb-4 border-b border-slate-100">
              <div className="flex items-center gap-2.5">
                <div className="w-8 h-8 rounded-lg bg-[#E91E8F]/10 text-[#E91E8F] flex items-center justify-center font-bold">
                  <TrendingUp size={18} />
                </div>
                <div>
                  <h3 className="font-bold text-[#101C37] text-base">
                    Top 10 Batters Under Pressure
                  </h3>
                  <p className="text-xs text-slate-500 font-mono">
                    Governing Metric: Conservative PRI (Strike Rate Points)
                  </p>
                </div>
              </div>
              <span className="px-2.5 py-1 rounded-md text-[11px] font-mono font-bold bg-[#E91E8F]/10 text-[#E91E8F] border border-[#E91E8F]/20">
                Deliverable 1
              </span>
            </div>

            <p className="text-xs text-slate-600 mt-3 leading-relaxed">
              Ranked by Conservative PRI (Posterior Mean minus 1.0 SE), penalizing small-sample volatility
              against context-stratified 12-cell ordinary baselines.
            </p>

            <div className="mt-4 space-y-2">
              {/* Podium Item #1 */}
              <div className="flex items-center justify-between p-3 rounded-xl bg-gradient-to-r from-amber-500/10 to-transparent border border-amber-500/20">
                <div className="flex items-center gap-3">
                  <span className="w-6 h-6 rounded-full bg-amber-500 text-white font-bold text-xs flex items-center justify-center shadow-sm">
                    1
                  </span>
                  <div>
                    <h4 className="text-xs font-bold text-[#101C37]">Nicholas Pooran</h4>
                    <span className="text-[10px] text-slate-500 font-mono">212 balls • 26 matches • Dual Qualified</span>
                  </div>
                </div>
                <div className="text-right">
                  <span className="text-xs font-bold font-mono text-emerald-600">+2.25 SR pts</span>
                  <p className="text-[10px] text-slate-400 font-mono">95% CI: [-11.2, +43.6]</p>
                </div>
              </div>

              {/* Podium Item #2 */}
              <div className="flex items-center justify-between p-3 rounded-xl bg-slate-50 border border-slate-200/60">
                <div className="flex items-center gap-3">
                  <span className="w-6 h-6 rounded-full bg-slate-400 text-white font-bold text-xs flex items-center justify-center">
                    2
                  </span>
                  <div>
                    <h4 className="text-xs font-bold text-[#101C37]">Donovan Ferreira</h4>
                    <span className="text-[10px] text-slate-500 font-mono">84 balls • 13 matches • IPL Qualified</span>
                  </div>
                </div>
                <div className="text-right">
                  <span className="text-xs font-bold font-mono text-emerald-600">+0.93 SR pts</span>
                  <p className="text-[10px] text-slate-400 font-mono">95% CI: [-18.1, +59.4]</p>
                </div>
              </div>

              {/* Podium Item #3 */}
              <div className="flex items-center justify-between p-3 rounded-xl bg-slate-50 border border-slate-200/60">
                <div className="flex items-center gap-3">
                  <span className="w-6 h-6 rounded-full bg-amber-700/80 text-white font-bold text-xs flex items-center justify-center">
                    3
                  </span>
                  <div>
                    <h4 className="text-xs font-bold text-[#101C37]">Tim David</h4>
                    <span className="text-[10px] text-slate-500 font-mono">290 balls • 33 matches • Dual Qualified</span>
                  </div>
                </div>
                <div className="text-right">
                  <span className="text-xs font-bold font-mono text-slate-700">-2.53 SR pts</span>
                  <p className="text-[10px] text-slate-400 font-mono">95% CI: [-14.1, +33.3]</p>
                </div>
              </div>
            </div>
          </div>

          <div className="mt-5 pt-4 border-t border-slate-100 flex items-center justify-between">
            <span className="text-xs text-slate-500 font-mono">
              Ranks 4–10: Karthik, Ashutosh, Stoinis, Dhir, Rinku, Stubbs, Rutherford
            </span>
            <Link
              href="/pressure"
              className="inline-flex items-center gap-1.5 text-xs font-bold text-[#E91E8F] hover:underline"
            >
              <span>View Full Top 10</span>
              <ArrowRight size={13} />
            </Link>
          </div>
        </div>

        {/* Bowling Top 10 Showcase */}
        <div className="bg-white rounded-2xl border border-slate-200/80 p-6 shadow-sm flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between pb-4 border-b border-slate-100">
              <div className="flex items-center gap-2.5">
                <div className="w-8 h-8 rounded-lg bg-[#D6B56D]/15 text-[#D6B56D] flex items-center justify-center font-bold">
                  <Target size={18} />
                </div>
                <div>
                  <h3 className="font-bold text-[#101C37] text-base">
                    Top 10 Bowlers Under Pressure
                  </h3>
                  <p className="text-xs text-slate-500 font-mono">
                    Governing Metric: Conservative Runs Saved per 6 Balls (RPO)
                  </p>
                </div>
              </div>
              <span className="px-2.5 py-1 rounded-md text-[11px] font-mono font-bold bg-[#D6B56D]/15 text-[#D6B56D] border border-[#D6B56D]/30">
                Deliverable 2
              </span>
            </div>

            <p className="text-xs text-slate-600 mt-3 leading-relaxed">
              Ranked by Conservative Runs Saved (Delta Economy lower bound), where negative economy diff
              represents superior run suppression under pressure.
            </p>

            <div className="mt-4 space-y-2">
              {/* Podium Item #1 */}
              <div className="flex items-center justify-between p-3 rounded-xl bg-gradient-to-r from-amber-500/10 to-transparent border border-amber-500/20">
                <div className="flex items-center gap-3">
                  <span className="w-6 h-6 rounded-full bg-amber-500 text-white font-bold text-xs flex items-center justify-center shadow-sm">
                    1
                  </span>
                  <div>
                    <h4 className="text-xs font-bold text-[#101C37]">Jasprit Bumrah</h4>
                    <span className="text-[10px] text-slate-500 font-mono">521 balls • 60 matches • Dual Qualified</span>
                  </div>
                </div>
                <div className="text-right">
                  <span className="text-xs font-bold font-mono text-emerald-600">-0.16 RPO</span>
                  <p className="text-[10px] text-slate-400 font-mono">95% CI: [-0.90, +0.50]</p>
                </div>
              </div>

              {/* Podium Item #2 */}
              <div className="flex items-center justify-between p-3 rounded-xl bg-slate-50 border border-slate-200/60">
                <div className="flex items-center gap-3">
                  <span className="w-6 h-6 rounded-full bg-slate-400 text-white font-bold text-xs flex items-center justify-center">
                    2
                  </span>
                  <div>
                    <h4 className="text-xs font-bold text-[#101C37]">Sunil Narine</h4>
                    <span className="text-[10px] text-slate-500 font-mono">153 balls • 24 matches • IPL Qualified</span>
                  </div>
                </div>
                <div className="text-right">
                  <span className="text-xs font-bold font-mono text-slate-700">-0.94 RPO</span>
                  <p className="text-[10px] text-slate-400 font-mono">95% CI: [-0.68, +1.47]</p>
                </div>
              </div>

              {/* Podium Item #3 */}
              <div className="flex items-center justify-between p-3 rounded-xl bg-slate-50 border border-slate-200/60">
                <div className="flex items-center gap-3">
                  <span className="w-6 h-6 rounded-full bg-amber-700/80 text-white font-bold text-xs flex items-center justify-center">
                    3
                  </span>
                  <div>
                    <h4 className="text-xs font-bold text-[#101C37]">Maheesh Theekshana</h4>
                    <span className="text-[10px] text-slate-500 font-mono">421 balls • 58 matches • Dual Qualified</span>
                  </div>
                </div>
                <div className="text-right">
                  <span className="text-xs font-bold font-mono text-slate-700">-0.96 RPO</span>
                  <p className="text-[10px] text-slate-400 font-mono">95% CI: [-0.25, +1.35]</p>
                </div>
              </div>
            </div>
          </div>

          <div className="mt-5 pt-4 border-t border-slate-100 flex items-center justify-between">
            <span className="text-xs text-slate-500 font-mono">
              Ranks 4–10: Pathirana, Afridi, Mustafizur, Ngarava, Ngidi, Ashwin, Mahmud
            </span>
            <Link
              href="/pressure"
              className="inline-flex items-center gap-1.5 text-xs font-bold text-[#D6B56D] hover:underline"
            >
              <span>View Full Top 10</span>
              <ArrowRight size={13} />
            </Link>
          </div>
        </div>
      </section>

      {/* ------------------------------------------------------------------- */}
      {/* 4. Methodological Rigor & Data Governance Overview */}
      {/* ------------------------------------------------------------------- */}
      <section className="bg-white rounded-2xl border border-slate-200/80 p-6 shadow-sm">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6 pb-6 border-b border-slate-100">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <Shield size={18} className="text-[#E91E8F]" />
              <h3 className="text-lg font-bold text-[#101C37]">
                Empirical Foundations & Methodological Principles
              </h3>
            </div>
            <p className="text-xs text-slate-500">
              The four foundational principles governing the SupeRR Selector Round 1 challenge solution.
            </p>
          </div>

          <div className="flex items-center gap-2">
            <span className="px-3 py-1 rounded-full text-xs font-mono font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200 flex items-center gap-1">
              <CheckCircle2 size={13} />
              Mathematically Audited
            </span>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="p-4 rounded-xl bg-slate-50 border border-slate-200/60">
            <div className="flex items-center gap-2 text-xs font-bold text-[#101C37] mb-2">
              <Flame size={16} className="text-[#E91E8F]" />
              <span>1. Dynamic Pressure</span>
            </div>
            <p className="text-xs text-slate-600 leading-relaxed">
              Multi-factor leverage model: Chasing Required Run Rate &ge; 9.0 with &le; 36 balls, wickets in hand &le; 4,
              and death-over target acceleration.
            </p>
          </div>

          <div className="p-4 rounded-xl bg-slate-50 border border-slate-200/60">
            <div className="flex items-center gap-2 text-xs font-bold text-[#101C37] mb-2">
              <Layers size={16} className="text-[#101C37]" />
              <span>2. 12-Cell Baselines</span>
            </div>
            <p className="text-xs text-slate-600 leading-relaxed">
              Every delivery is benchmarked against Innings (2) &times; Phase (3) &times; Tier (2) strata,
              eliminating structural death-over entry bias.
            </p>
          </div>

          <div className="p-4 rounded-xl bg-slate-50 border border-slate-200/60">
            <div className="flex items-center gap-2 text-xs font-bold text-[#101C37] mb-2">
              <Sparkles size={16} className="text-[#D6B56D]" />
              <span>3. Empirical Bayes</span>
            </div>
            <p className="text-xs text-slate-600 leading-relaxed">
              Separates skill from noise using Gaussian population priors (&mu;<sub>0</sub>, &tau;<sup>2</sup>). Low-sample outliers shrink toward
              the league mean.
            </p>
          </div>

          <div className="p-4 rounded-xl bg-slate-50 border border-slate-200/60">
            <div className="flex items-center gap-2 text-xs font-bold text-[#101C37] mb-2">
              <Shield size={16} className="text-emerald-600" />
              <span>4. Conservative Lower Bound</span>
            </div>
            <p className="text-xs text-slate-600 leading-relaxed">
              Rankings govern by Conservative PRI = Shrunk Posterior Mean minus 1.0 SE. Directly penalizes high
              estimation uncertainty.
            </p>
          </div>
        </div>
      </section>

      {/* ------------------------------------------------------------------- */}
      {/* 5. Platform Architecture & Data Exploration Modules */}
      {/* ------------------------------------------------------------------- */}
      <section className="space-y-4">
        <div>
          <h2 className="text-base font-bold text-[#101C37]">
            Platform Architecture & Exploration Modules
          </h2>
          <p className="text-xs text-slate-500">
            Integrated analytical modules connected to the verified competition data pack.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {/* Module 1: Pressure Intelligence */}
          <Link
            href="/pressure"
            className="group block p-5 rounded-2xl bg-white border border-slate-200/80 shadow-sm hover:border-[#E91E8F]/40 hover:shadow-md transition-all"
          >
            <div className="flex items-center justify-between mb-3">
              <div className="w-9 h-9 rounded-xl bg-[#E91E8F]/10 text-[#E91E8F] flex items-center justify-center">
                <Shield size={20} />
              </div>
              <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded bg-[#E91E8F]/10 text-[#E91E8F]">
                Round 1 Flagship
              </span>
            </div>
            <h3 className="font-bold text-sm text-[#101C37] group-hover:text-[#E91E8F] transition-colors">
              Pressure Intelligence Engine
            </h3>
            <p className="text-xs text-slate-500 mt-1.5 leading-relaxed">
              Explore the sealed Top 10 leaderboards, uncertainty bands, and interactive 11-question candidate evidence dossiers.
            </p>
            <div className="mt-4 flex items-center gap-1 text-xs font-semibold text-[#E91E8F]">
              <span>Open Leaderboards</span>
              <ArrowRight size={13} className="group-hover:translate-x-1 transition-transform" />
            </div>
          </Link>

          {/* Module 2: Tactical Intelligence */}
          <Link
            href="/tactical"
            className="group block p-5 rounded-2xl bg-white border border-slate-200/80 shadow-sm hover:border-[#D6B56D]/40 hover:shadow-md transition-all"
          >
            <div className="flex items-center justify-between mb-3">
              <div className="w-9 h-9 rounded-xl bg-[#D6B56D]/15 text-[#D6B56D] flex items-center justify-center">
                <Crosshair size={20} />
              </div>
              <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded bg-[#D6B56D]/15 text-[#D6B56D]">
                Stage 5 Operational
              </span>
            </div>
            <h3 className="font-bold text-sm text-[#101C37] group-hover:text-[#D6B56D] transition-colors">
              Tactical Cricket Intelligence
            </h3>
            <p className="text-xs text-slate-500 mt-1.5 leading-relaxed">
              10 REST APIs analyzing phases, 30 stroke types, 4-way batter/bowler handedness splits, 34 delivery styles, and speed profiles.
            </p>
            <div className="mt-4 flex items-center gap-1 text-xs font-semibold text-[#D6B56D]">
              <span>Explore Tactical Splits</span>
              <ArrowRight size={13} className="group-hover:translate-x-1 transition-transform" />
            </div>
          </Link>

          {/* Module 3: Data Provenance & Telemetry */}
          <Link
            href="/acquisition"
            className="group block p-5 rounded-2xl bg-white border border-slate-200/80 shadow-sm hover:border-slate-300 hover:shadow-md transition-all"
          >
            <div className="flex items-center justify-between mb-3">
              <div className="w-9 h-9 rounded-xl bg-slate-100 text-slate-700 flex items-center justify-center">
                <Database size={20} />
              </div>
              <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded bg-slate-100 text-slate-600">
                Data Infrastructure
              </span>
            </div>
            <h3 className="font-bold text-sm text-[#101C37] group-hover:text-slate-900 transition-colors">
              Data Ingestion & Coverage
            </h3>
            <p className="text-xs text-slate-500 mt-1.5 leading-relaxed">
              Inspect match and delivery counts, CSV schemas, legal delivery decoupling, and 883 match verification status.
            </p>
            <div className="mt-4 flex items-center gap-1 text-xs font-semibold text-slate-700">
              <span>View Data Ingestion</span>
              <ArrowRight size={13} className="group-hover:translate-x-1 transition-transform" />
            </div>
          </Link>
        </div>
      </section>

      {/* ------------------------------------------------------------------- */}
      {/* 6. Evaluation Scope & Governance Seal */}
      {/* ------------------------------------------------------------------- */}
      <div className="rounded-xl border border-slate-200 bg-slate-50/80 p-5 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div className="flex items-start gap-3">
          <div className="p-2 rounded-lg bg-emerald-100/70 text-emerald-700 shrink-0 mt-0.5">
            <CheckCircle2 size={16} />
          </div>
          <div>
            <h4 className="text-xs font-bold text-[#101C37]">
              SupeRR Selector Season 2 — Round 1 Evaluation Scope
            </h4>
            <p className="text-xs text-slate-500 leading-relaxed mt-0.5">
              The evaluation evaluates all qualified players in the 2022–2026 IPL and Senior T20I matches.
              Zero speculative scouting filters, uncapped-only restrictions, or synthetic records are applied.
            </p>
          </div>
        </div>

        <div className="shrink-0">
          <Link
            href="/pressure"
            className="px-4 py-2 rounded-lg bg-[#101C37] text-white text-xs font-semibold hover:bg-[#1A2B50] transition-colors inline-flex items-center gap-1.5"
          >
            <span>Review Full Submission</span>
            <ExternalLink size={13} />
          </Link>
        </div>
      </div>
    </div>
  );
}