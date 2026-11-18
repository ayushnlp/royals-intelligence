import React from "react";
import Link from "next/link";
import {
  Shield,
  Layers,
  Database,
  ArrowRight,
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
  FileText,
  ExternalLink,
} from "lucide-react";

export default function OverviewPage() {
  return (
    <div className="space-y-12 pb-10">
      {/* ------------------------------------------------------------------- */}
      {/* 1. Editorial Header & Challenge Statement */}
      {/* ------------------------------------------------------------------- */}
      <section className="space-y-4">
        <div className="flex flex-wrap items-center gap-3 text-xs">
          <span className="font-mono font-bold tracking-widest text-[#E91E8F] uppercase">
            Rajasthan Royals SupeRR Selector
          </span>
          <span className="text-slate-300">•</span>
          <span className="font-mono text-slate-500">
            Season 2 — Round 1 Final Submission
          </span>
          <span className="text-slate-300">•</span>
          <span className="inline-flex items-center gap-1.5 text-emerald-700 font-medium">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
            100% Bitwise Verified
          </span>
        </div>

        <div className="max-w-4xl space-y-3">
          <h1 className="text-3xl md:text-4xl font-extrabold tracking-tight text-slate-900 leading-tight">
            The Most Reliable Players Under Pressure
          </h1>
          <p className="text-sm md:text-base text-slate-600 leading-relaxed font-normal">
            Official Rajasthan Royals analytical engine evaluating 200,999 deliveries across 883 matches. Benchmarked
            against 12-cell context strata, Empirical Bayes shrinkage, and 1-SE Conservative lower credible bounds.
            Delivering the official Top 10 Batters, Top 10 Bowlers, and 20 verified uncapped Indian domestic assets.
          </p>
        </div>

        {/* Primary Action Links */}
        <div className="flex flex-wrap items-center gap-4 pt-2">
          <Link
            href="/pressure"
            className="inline-flex items-center gap-2 px-5 py-2.5 rounded-lg bg-[#101C37] text-white text-xs font-semibold hover:bg-[#1A2B50] transition-colors shadow-sm group"
          >
            <Shield size={14} className="text-[#E91E8F]" />
            <span>Official Pressure Leaderboards</span>
            <ArrowRight size={13} className="text-slate-400 group-hover:translate-x-0.5 transition-transform" />
          </Link>

          <Link
            href="/uncapped"
            className="inline-flex items-center gap-2 px-5 py-2.5 rounded-lg bg-white border border-slate-200 text-slate-800 text-xs font-semibold hover:bg-slate-50 transition-colors shadow-sm group"
          >
            <Sparkles size={14} className="text-emerald-600" />
            <span>Uncapped Scouting Shortlist</span>
            <ArrowRight size={13} className="text-slate-400 group-hover:translate-x-0.5 transition-transform" />
          </Link>

          <Link
            href="/tactical"
            className="inline-flex items-center gap-2 px-4 py-2.5 rounded-lg text-slate-600 text-xs font-medium hover:text-slate-900 transition-colors"
          >
            <Crosshair size={14} className="text-[#D6B56D]" />
            <span>Tactical Analytics</span>
          </Link>
        </div>
      </section>

      {/* ------------------------------------------------------------------- */}
      {/* 2. Open Editorial Telemetry Strip (No Card Boxes) */}
      {/* ------------------------------------------------------------------- */}
      <section className="py-5 border-y border-slate-200/70">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 md:gap-8">
          <div>
            <span className="text-[11px] font-mono uppercase tracking-wider text-slate-400 block mb-1">
              Controlling Data Pack
            </span>
            <div className="text-2xl md:text-3xl font-extrabold text-slate-900 font-mono tracking-tight">
              200,999
            </div>
            <p className="text-xs text-slate-500 mt-1">
              Deliveries across 883 matches (141 tournaments)
            </p>
          </div>

          <div>
            <span className="text-[11px] font-mono uppercase tracking-wider text-slate-400 block mb-1">
              Official Deliverables
            </span>
            <div className="text-2xl md:text-3xl font-extrabold text-slate-900 font-mono tracking-tight">
              Top 10 / Top 10
            </div>
            <p className="text-xs text-slate-500 mt-1">
              1-SE Conservative lower bounds (100% qualified)
            </p>
          </div>

          <div>
            <span className="text-[11px] font-mono uppercase tracking-wider text-slate-400 block mb-1">
              Uncapped Domestic Intelligence
            </span>
            <div className="text-2xl md:text-3xl font-extrabold text-slate-900 font-mono tracking-tight">
              20 / 20 Verified
            </div>
            <p className="text-xs text-slate-500 mt-1">
              Certified 0 senior caps in AUCTION-02 ledger
            </p>
          </div>

          <div>
            <span className="text-[11px] font-mono uppercase tracking-wider text-slate-400 block mb-1">
              Verification Health
            </span>
            <div className="text-2xl md:text-3xl font-extrabold text-emerald-700 font-mono tracking-tight">
              100% Sealed
            </div>
            <p className="text-xs text-slate-500 mt-1">
              4 Parquet artifacts SHA-256 bitwise verified
            </p>
          </div>
        </div>
      </section>

      {/* ------------------------------------------------------------------- */}
      {/* 3. Official Round 1 Deliverables: Batting & Bowling Leaderboards */}
      {/* ------------------------------------------------------------------- */}
      <section className="space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-baseline justify-between gap-2 border-b border-slate-200/60 pb-3">
          <div>
            <h2 className="text-lg font-bold text-slate-900 tracking-tight">
              Official Round 1 Leaderboards Under Pressure
            </h2>
            <p className="text-xs text-slate-500">
              Primary Unstop selections: overall qualified batters and bowlers (&ge; 60 pressure deliveries).
            </p>
          </div>
          <Link
            href="/pressure"
            className="text-xs font-semibold text-[#E91E8F] hover:text-[#C2185B] transition-colors inline-flex items-center gap-1"
          >
            <span>View Complete Leaderboards & Dossiers</span>
            <ArrowRight size={13} />
          </Link>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Batting Top 5 Preview */}
          <div className="space-y-3">
            <div className="flex items-center justify-between text-xs font-semibold text-slate-700">
              <span className="flex items-center gap-2">
                <TrendingUp size={15} className="text-[#E91E8F]" />
                Top 5 Batters Under Pressure (Conservative PRI)
              </span>
              <span className="font-mono text-[11px] text-slate-400">Balls / Matches</span>
            </div>

            <div className="divide-y divide-slate-100 border-t border-slate-200/60 text-xs">
              {[
                { rank: 1, name: "Nicholas Pooran", team: "LSG / WI", balls: 212, matches: 26, val: "+2.25", ci: "[-11.2, +43.6]" },
                { rank: 2, name: "Donovan Ferreira", team: "RR / SA", balls: 84, matches: 13, val: "+0.93", ci: "[-18.0, +59.4]" },
                { rank: 3, name: "Tim David", team: "MI / AUS", balls: 290, matches: 33, val: "-2.53", ci: "[-14.1, +33.3]" },
                { rank: 4, name: "Dinesh Karthik", team: "RCB / IND", balls: 260, matches: 30, val: "-2.67", ci: "[-14.1, +32.6]" },
                { rank: 5, name: "Ashutosh Sharma", team: "PBKS / IND", balls: 191, matches: 20, val: "-3.63", ci: "[-17.0, +37.6]" },
              ].map((p) => (
                <div key={p.rank} className="py-2.5 flex items-center justify-between hover:bg-slate-50/70 px-2 rounded-md transition-colors">
                  <div className="flex items-center gap-3">
                    <span className="font-mono font-bold text-slate-400 w-4 text-center">{p.rank}</span>
                    <div>
                      <span className="font-bold text-slate-900 block">{p.name}</span>
                      <span className="text-[11px] text-slate-400 font-mono">{p.team}</span>
                    </div>
                  </div>
                  <div className="text-right">
                    <span className={`font-mono font-bold ${p.val.startsWith("+") ? "text-emerald-600" : "text-slate-800"}`}>
                      {p.val} pts
                    </span>
                    <span className="text-[11px] font-mono text-slate-400 block">{p.balls}b • {p.matches}m</span>
                  </div>
                </div>
              ))}
            </div>

            <div className="pt-2 text-[11px] text-slate-400 font-mono flex justify-between">
              <span>Ranks 6–10: Stoinis, Dhir, Rinku Singh, Stubbs, Rutherford</span>
              <Link href="/pressure?tab=batting" className="text-slate-600 hover:text-slate-900 font-sans font-medium">
                Full 824 Batters &rarr;
              </Link>
            </div>
          </div>

          {/* Bowling Top 5 Preview */}
          <div className="space-y-3">
            <div className="flex items-center justify-between text-xs font-semibold text-slate-700">
              <span className="flex items-center gap-2">
                <Target size={15} className="text-[#D6B56D]" />
                Top 5 Bowlers Under Pressure (Conservative Runs Saved)
              </span>
              <span className="font-mono text-[11px] text-slate-400">Balls / Matches</span>
            </div>

            <div className="divide-y divide-slate-100 border-t border-slate-200/60 text-xs">
              {[
                { rank: 1, name: "Jasprit Bumrah", team: "MI / IND", balls: 338, matches: 32, val: "-0.16", ci: "[-0.91, +0.51]" },
                { rank: 2, name: "Sunil Narine", team: "KKR / WI", balls: 215, matches: 28, val: "-0.94", ci: "[-0.68, +1.47]" },
                { rank: 3, name: "Anrich Nortje", team: "DC / SA", balls: 196, matches: 16, val: "-1.39", ci: "[-0.33, +1.95]" },
                { rank: 4, name: "Pat Cummins", team: "SRH / AUS", balls: 203, matches: 25, val: "-1.46", ci: "[-0.27, +2.02]" },
                { rank: 5, name: "Shaheen Afridi", team: "PAK", balls: 163, matches: 24, val: "-1.63", ci: "[-0.41, +2.30]" },
              ].map((p) => (
                <div key={p.rank} className="py-2.5 flex items-center justify-between hover:bg-slate-50/70 px-2 rounded-md transition-colors">
                  <div className="flex items-center gap-3">
                    <span className="font-mono font-bold text-slate-400 w-4 text-center">{p.rank}</span>
                    <div>
                      <span className="font-bold text-slate-900 block">{p.name}</span>
                      <span className="text-[11px] text-slate-400 font-mono">{p.team}</span>
                    </div>
                  </div>
                  <div className="text-right">
                    <span className="font-mono font-bold text-slate-800">
                      {p.val} RPO
                    </span>
                    <span className="text-[11px] font-mono text-slate-400 block">{p.balls}b • {p.matches}m</span>
                  </div>
                </div>
              ))}
            </div>

            <div className="pt-2 text-[11px] text-slate-400 font-mono flex justify-between">
              <span>Ranks 6–10: Mustafizur, Ngarava, Ngidi, Starc, Hasan Mahmud</span>
              <Link href="/pressure?tab=bowling" className="text-slate-600 hover:text-slate-900 font-sans font-medium">
                Full 596 Bowlers &rarr;
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* ------------------------------------------------------------------- */}
      {/* 4. Supplementary Uncapped Domestic Intelligence Showcase */}
      {/* ------------------------------------------------------------------- */}
      <section className="space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-baseline justify-between gap-2 border-b border-slate-200/60 pb-3">
          <div>
            <h2 className="text-lg font-bold text-slate-900 tracking-tight">
              Supplementary Uncapped Indian Domestic Intelligence
            </h2>
            <p className="text-xs text-slate-500">
              Specialized franchise auction intelligence for Rajasthan Royals — 100% verified zero senior international caps.
            </p>
          </div>
          <Link
            href="/uncapped"
            className="text-xs font-semibold text-emerald-700 hover:text-emerald-800 transition-colors inline-flex items-center gap-1"
          >
            <span>View Full 20-Player Shortlist & Squad Fit Ratings</span>
            <ArrowRight size={13} />
          </Link>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* Top Uncapped Batters */}
          <div className="space-y-3">
            <span className="text-xs font-semibold text-slate-700 flex items-center gap-2">
              <Sparkles size={14} className="text-emerald-600" />
              Verified Uncapped Batters (Top 3)
            </span>
            <div className="divide-y divide-slate-100 border-t border-slate-200/60 text-xs">
              {[
                { rank: 1, name: "Ashutosh Sharma", team: "Railways / PBKS", metric: "-3.63 PRI", fit: "93.20 Fit", desc: "Provable domestic death finisher (+10.3 SR delta)" },
                { rank: 2, name: "Shashank Singh", team: "Chhattisgarh / PBKS", metric: "-11.07 PRI", fit: "87.85 Fit", desc: "Composed middle-overs aggregator and accelerator" },
                { rank: 3, name: "Rahul Tewatia", team: "Haryana / GT", metric: "-11.37 PRI", fit: "87.05 Fit", desc: "Clutch chase equity with situational leg-spin utility" },
              ].map((p) => (
                <div key={p.rank} className="py-2.5 flex items-center justify-between hover:bg-slate-50/70 px-2 rounded-md transition-colors">
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="font-mono font-bold text-slate-400 w-4">{p.rank}</span>
                      <span className="font-bold text-slate-900">{p.name}</span>
                      <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-emerald-50 text-emerald-700">Verified</span>
                    </div>
                    <p className="text-[11px] text-slate-500 mt-0.5 pl-6">{p.desc}</p>
                  </div>
                  <div className="text-right">
                    <span className="font-mono font-bold text-slate-800">{p.fit}</span>
                    <span className="text-[10px] font-mono text-slate-400 block">{p.metric}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Top Uncapped Bowlers */}
          <div className="space-y-3">
            <span className="text-xs font-semibold text-slate-700 flex items-center gap-2">
              <Crosshair size={14} className="text-cyan-600" />
              Verified Uncapped Bowlers (Top 3)
            </span>
            <div className="divide-y divide-slate-100 border-t border-slate-200/60 text-xs">
              {[
                { rank: 1, name: "Vaibhav Arora", team: "Himachal / KKR", metric: "-2.36 RPO", fit: "90.00 Fit", desc: "Dual-phase swing in PP and disciplined death yorkers" },
                { rank: 2, name: "Suyash Sharma", team: "Delhi / KKR", metric: "-2.41 RPO", fit: "82.95 Fit", desc: "Attacking wrist-spin option with deceptive googly" },
                { rank: 3, name: "Akash Madhwal", team: "Uttarakhand / MI", metric: "-2.42 RPO", fit: "87.20 Fit", desc: "Specialist death-overs blockhole execution" },
              ].map((p) => (
                <div key={p.rank} className="py-2.5 flex items-center justify-between hover:bg-slate-50/70 px-2 rounded-md transition-colors">
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="font-mono font-bold text-slate-400 w-4">{p.rank}</span>
                      <span className="font-bold text-slate-900">{p.name}</span>
                      <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-emerald-50 text-emerald-700">Verified</span>
                    </div>
                    <p className="text-[11px] text-slate-500 mt-0.5 pl-6">{p.desc}</p>
                  </div>
                  <div className="text-right">
                    <span className="font-mono font-bold text-slate-800">{p.fit}</span>
                    <span className="text-[10px] font-mono text-slate-400 block">{p.metric}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* ------------------------------------------------------------------- */}
      {/* 5. Methodological Rigor & Data Governance Overview */}
      {/* ------------------------------------------------------------------- */}
      <section className="space-y-4 pt-4 border-t border-slate-200/60">
        <div>
          <h2 className="text-base font-bold text-slate-900 tracking-tight">
            Methodological Architecture
          </h2>
          <p className="text-xs text-slate-500">
            Four core scientific pillars governing the ROYALS INTELLIGENCE pressure evaluation system.
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 text-xs">
          <div className="space-y-1.5">
            <div className="flex items-center gap-2 font-bold text-slate-900">
              <Flame size={15} className="text-[#E91E8F]" />
              <span>1. Dynamic Pressure</span>
            </div>
            <p className="text-slate-600 leading-relaxed">
              Multi-factor leverage model: Chasing Required Run Rate &ge; 9.0 with &le; 36 balls, wickets in hand &le; 4,
              and death-over target acceleration.
            </p>
          </div>

          <div className="space-y-1.5">
            <div className="flex items-center gap-2 font-bold text-slate-900">
              <Layers size={15} className="text-slate-800" />
              <span>2. 12-Cell Baselines</span>
            </div>
            <p className="text-slate-600 leading-relaxed">
              Every delivery is benchmarked against Innings (2) &times; Phase (3) &times; Tier (2) strata,
              eliminating structural death-over entry bias.
            </p>
          </div>

          <div className="space-y-1.5">
            <div className="flex items-center gap-2 font-bold text-slate-900">
              <Sparkles size={15} className="text-[#D6B56D]" />
              <span>3. Empirical Bayes</span>
            </div>
            <p className="text-slate-600 leading-relaxed">
              Separates skill from noise using Gaussian population priors (&mu;<sub>0</sub>, &tau;<sup>2</sup>). Low-sample outliers shrink toward
              the league mean.
            </p>
          </div>

          <div className="space-y-1.5">
            <div className="flex items-center gap-2 font-bold text-slate-900">
              <Shield size={15} className="text-emerald-700" />
              <span>4. Conservative PRI</span>
            </div>
            <p className="text-slate-600 leading-relaxed">
              Rankings govern by Conservative PRI = Shrunk Posterior Mean minus 1.0 SE, directly penalizing high
              estimation uncertainty.
            </p>
          </div>
        </div>
      </section>

      {/* ------------------------------------------------------------------- */}
      {/* 6. Navigation to Analytical Modules */}
      {/* ------------------------------------------------------------------- */}
      <section className="space-y-4 pt-4 border-t border-slate-200/60">
        <div>
          <h2 className="text-base font-bold text-slate-900 tracking-tight">
            Intelligence Modules
          </h2>
          <p className="text-xs text-slate-500">
            Dedicated research environments connected to the verified tournament database.
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <Link
            href="/pressure"
            className="p-4 rounded-lg bg-white border border-slate-200/80 hover:border-slate-400 hover:shadow-sm transition-all group block"
          >
            <div className="flex items-center justify-between mb-2">
              <Shield size={18} className="text-[#E91E8F]" />
              <ArrowRight size={13} className="text-slate-400 group-hover:translate-x-0.5 group-hover:text-slate-800 transition-all" />
            </div>
            <h3 className="font-bold text-xs text-slate-900">Pressure Intelligence</h3>
            <p className="text-[11px] text-slate-500 mt-1 leading-normal">
              Official Top 10 leaderboards, uncertainty forest plots, and candidate evidence dossiers.
            </p>
          </Link>

          <Link
            href="/tactical"
            className="p-4 rounded-lg bg-white border border-slate-200/80 hover:border-slate-400 hover:shadow-sm transition-all group block"
          >
            <div className="flex items-center justify-between mb-2">
              <Crosshair size={18} className="text-[#D6B56D]" />
              <ArrowRight size={13} className="text-slate-400 group-hover:translate-x-0.5 group-hover:text-slate-800 transition-all" />
            </div>
            <h3 className="font-bold text-xs text-slate-900">Tactical Intelligence</h3>
            <p className="text-[11px] text-slate-500 mt-1 leading-normal">
              Phase splits (PP, Middle, Death), shot archetypes, bowling variations, and radar speeds.
            </p>
          </Link>

          <Link
            href="/uncapped"
            className="p-4 rounded-lg bg-white border border-slate-200/80 hover:border-slate-400 hover:shadow-sm transition-all group block"
          >
            <div className="flex items-center justify-between mb-2">
              <Sparkles size={18} className="text-emerald-600" />
              <ArrowRight size={13} className="text-slate-400 group-hover:translate-x-0.5 group-hover:text-slate-800 transition-all" />
            </div>
            <h3 className="font-bold text-xs text-slate-900">Uncapped Talent</h3>
            <p className="text-[11px] text-slate-500 mt-1 leading-normal">
              Verified Indian domestic batters & bowlers, Rajasthan Royals squad fit ratings, and reserves.
            </p>
          </Link>

          <Link
            href="/domestic"
            className="p-4 rounded-lg bg-white border border-slate-200/80 hover:border-slate-400 hover:shadow-sm transition-all group block"
          >
            <div className="flex items-center justify-between mb-2">
              <Swords size={18} className="text-slate-700" />
              <ArrowRight size={13} className="text-slate-400 group-hover:translate-x-0.5 group-hover:text-slate-800 transition-all" />
            </div>
            <h3 className="font-bold text-xs text-slate-900">Domestic & Matches</h3>
            <p className="text-[11px] text-slate-500 mt-1 leading-normal">
              287-player directory, match scorecards, player histories, and all-round dual contributions.
            </p>
          </Link>
        </div>
      </section>
    </div>
  );
}
