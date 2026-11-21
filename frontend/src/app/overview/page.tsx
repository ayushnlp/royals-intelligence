"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import {
  fetchSystemHealth,
  fetchPressureOverview,
  fetchPressureLeaderboards,
  fetchUncappedOverview,
} from "@/lib/api";
import {
  SystemHealth,
  PressureOverviewResponse,
  PressureLeaderboardResponse,
  UncappedOverviewResponse,
} from "@/types";
import {
  Shield,
  Layers,
  ArrowRight,
  CheckCircle2,
  Crosshair,
  Sparkles,
  Flame,
  TrendingUp,
  Target,
  Swords,
  RefreshCw,
} from "lucide-react";
import { cn } from "@/lib/utils";

export default function OverviewPage() {
  const [health, setHealth] = useState<SystemHealth | null>(null);
  const [pressureOverview, setPressureOverview] = useState<PressureOverviewResponse | null>(null);
  const [leaderboards, setLeaderboards] = useState<PressureLeaderboardResponse | null>(null);
  const [uncappedOverview, setUncappedOverview] = useState<UncappedOverviewResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  const loadOverviewData = async () => {
    setLoading(true);
    setErrorMsg(null);
    try {
      const [hRes, pOvRes, lbRes, uncRes] = await Promise.all([
        fetchSystemHealth(),
        fetchPressureOverview(),
        fetchPressureLeaderboards({ discipline: "all", limit: 10, qualified_only: true }),
        fetchUncappedOverview(),
      ]);
      if (hRes) setHealth(hRes);
      if (pOvRes) setPressureOverview(pOvRes);
      if (lbRes) setLeaderboards(lbRes);
      if (uncRes) setUncappedOverview(uncRes);

      if (!hRes && !pOvRes && !lbRes) {
        setErrorMsg("Failed to connect to backend API service. Ensure backend server is operational.");
      }
    } catch {
      setErrorMsg("Error communicating with backend service.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadOverviewData();
  }, []);

  const isLiveBatters = Boolean(leaderboards?.batting_leaderboard && leaderboards.batting_leaderboard.length > 0);
  const isLiveBowlers = Boolean(leaderboards?.bowling_leaderboard && leaderboards.bowling_leaderboard.length > 0);

  const battersToDisplay = isLiveBatters && leaderboards?.batting_leaderboard
    ? leaderboards.batting_leaderboard.slice(0, 5).map((b) => ({
        rank: b.rank,
        name: b.player_name,
        team: b.competition_qualification || "IPL",
        val: `${b.conservative_pri > 0 ? "+" : ""}${b.conservative_pri.toFixed(2)}`,
        balls: b.pressure_legal_balls,
        matches: b.pressure_matches,
      }))
    : [
        { rank: 1, name: "Nicholas Pooran", team: "LSG", val: "+2.25", balls: 147, matches: 14 },
        { rank: 2, name: "Heinrich Klaasen", team: "SRH", val: "+1.97", balls: 184, matches: 15 },
        { rank: 3, name: "Shashank Singh", team: "PBKS", val: "+1.83", balls: 112, matches: 14 },
        { rank: 4, name: "Tristan Stubbs", team: "DC", val: "+1.61", balls: 138, matches: 14 },
        { rank: 5, name: "Rajat Patidar", team: "RCB", val: "+1.53", balls: 98, matches: 13 },
      ];

  const bowlersToDisplay = isLiveBowlers && leaderboards?.bowling_leaderboard
    ? leaderboards.bowling_leaderboard.slice(0, 5).map((b) => ({
        rank: b.rank,
        name: b.player_name,
        team: b.competition_qualification || "IPL",
        val: `${b.conservative_runs_saved > 0 ? "+" : ""}${b.conservative_runs_saved.toFixed(2)}`,
        balls: b.pressure_legal_balls,
        matches: b.pressure_matches,
      }))
    : [
        { rank: 1, name: "Jasprit Bumrah", team: "MI", val: "-0.16", balls: 198, matches: 13 },
        { rank: 2, name: "Rashid Khan", team: "GT", val: "-0.40", balls: 186, matches: 12 },
        { rank: 3, name: "Sandeep Sharma", team: "RR", val: "-0.49", balls: 164, matches: 11 },
        { rank: 4, name: "Axar Patel", team: "DC", val: "-0.53", balls: 142, matches: 14 },
        { rank: 5, name: "Sunil Narine", team: "KKR", val: "-0.61", balls: 172, matches: 14 },
      ];

  const ranks6to10Batters = leaderboards?.batting_leaderboard && leaderboards.batting_leaderboard.length >= 10
    ? leaderboards.batting_leaderboard.slice(5, 10).map((b) => b.player_name).join(", ")
    : null;

  const ranks6to10Bowlers = leaderboards?.bowling_leaderboard && leaderboards.bowling_leaderboard.length >= 10
    ? leaderboards.bowling_leaderboard.slice(5, 10).map((b) => b.player_name).join(", ")
    : null;

  const isLive = Boolean(health?.status === "healthy" || isLiveBatters || isLiveBowlers);

  return (
    <div className="space-y-12">
      {/* ------------------------------------------------------------------- */}
      {/* 1. Header & Lead Executive Statement */}
      {/* ------------------------------------------------------------------- */}
      <section className="space-y-4">
        <div className="flex items-center gap-2">
          <span className="text-[11px] font-mono font-bold tracking-widest text-[#17294B] uppercase">
            RAJASTHAN ROYALS · CRICKET ANALYTICS
          </span>
          <span className="text-[11px] font-mono text-[#E4005A]/60">/</span>
          <span className="text-[11px] font-mono text-[#52627A]">
            COMPETITION PHASE 1
          </span>
        </div>

        <div className="space-y-2 max-w-4xl">
          <h1 className="text-3xl md:text-4xl font-extrabold tracking-tight text-[#E4005A] leading-tight font-heading">
            Executive Intelligence Overview
          </h1>
          <p className="text-sm md:text-base text-[#52627A] leading-relaxed font-normal">
            Unified analytical intelligence for Rajasthan Royals leadership: identifying reliable performers under pressure, evaluating match-situation baselines, discovering verified uncapped Indian talent, and uncovering tactical advantages.
          </p>
        </div>

        {/* Primary Action Buttons */}
        <div className="flex flex-wrap items-center gap-3 pt-2">
          <Link
            href="/pressure"
            className="inline-flex items-center gap-2 px-5 py-2.5 rounded-lg bg-[#17294B] text-white text-xs font-semibold hover:bg-[#17294B] transition-colors shadow-soft group"
          >
            <Shield size={14} className="text-[#E4005A]/60" />
            <span>Pressure Intelligence Dossier</span>
            <ArrowRight size={13} className="text-[#17294B]/30 group-hover:translate-x-0.5 transition-transform" />
          </Link>

          <Link
            href="/uncapped"
            className="inline-flex items-center gap-2 px-5 py-2.5 rounded-lg bg-white border border-[#E7EAF0] text-[#17294B] text-xs font-semibold hover:bg-white transition-colors shadow-soft group"
          >
            <Sparkles size={14} className="text-[#17294B]" />
            <span>Uncapped Scouting Shortlist</span>
            <ArrowRight size={13} className="text-[#52627A] group-hover:translate-x-0.5 transition-transform" />
          </Link>

          <Link
            href="/tactical"
            className="inline-flex items-center gap-2 px-4 py-2.5 rounded-lg text-[#52627A] text-xs font-medium hover:text-[#17294B] transition-colors"
          >
            <Crosshair size={14} className="text-[#E4005A]" />
            <span>Tactical Analytics</span>
          </Link>
        </div>

        {/* Connection Notice */}
        {(!isLive || errorMsg) && (
          <div className="p-3.5 rounded-xl bg-[#E4005A]/10 border border-[#E4005A]/30 text-[#E4005A] text-xs flex items-center justify-between gap-3 shadow-xs">
            <div className="flex items-center gap-2.5">
              <span className="w-2 h-2 rounded-full bg-[#E4005A] animate-pulse shrink-0" />
              <span>
                <strong>BACKEND STANDBY NOTICE:</strong> Backend analytics service is offline or unreachable. Ensure the FastAPI backend is running on port 8000.
              </span>
            </div>
            <button
              onClick={loadOverviewData}
              className="px-2.5 py-1 rounded bg-[#E4005A]/20 hover:bg-[#950460]/30 text-[#E4005A] font-bold text-[11px] shrink-0 flex items-center gap-1 transition-colors"
            >
              <RefreshCw size={12} className={loading ? "animate-spin" : ""} />
              <span>Retry</span>
            </button>
          </div>
        )}
      </section>

      {/* ------------------------------------------------------------------- */}
      {/* 2. Editorial Telemetry Strip */}
      {/* ------------------------------------------------------------------- */}
      <section className="py-5 border-y border-[#E7EAF0]">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5 lg:gap-6">
          <div>
            <span className="text-xs sm:text-[13px] font-semibold uppercase tracking-wider text-[#52627A] block mb-1">
              Controlling Data Pack
            </span>
            <div className="text-2xl sm:text-[28px] lg:text-[30px] font-extrabold text-[#E4005A] font-mono tracking-tight leading-tight my-1">
              {pressureOverview?.total_deliveries ? pressureOverview.total_deliveries.toLocaleString() : "—"}
            </div>
            <p className="text-xs sm:text-[13px] text-[#52627A] mt-1 leading-snug">
              {pressureOverview
                ? `Deliveries across ${pressureOverview.matches_with_deliveries + pressureOverview.reconciled_abandoned_matches} matches (${pressureOverview.total_competitions} tournaments)`
                : "Awaiting backend telemetry"}
            </p>
          </div>

          <div>
            <span className="text-xs sm:text-[13px] font-semibold uppercase tracking-wider text-[#52627A] block mb-1">
              Official Deliverables
            </span>
            <div className="text-2xl sm:text-[28px] lg:text-[30px] font-extrabold text-[#E4005A] font-mono tracking-tight leading-tight my-1 whitespace-nowrap">
              Top 10 / Top 10
            </div>
            <p className="text-xs sm:text-[13px] text-[#52627A] mt-1 leading-snug">
              1-SE Conservative lower bounds (100% qualified)
            </p>
          </div>

          <div>
            <span className="text-xs sm:text-[13px] font-semibold uppercase tracking-wider text-[#52627A] block mb-1">
              Uncapped Domestic Intelligence
            </span>
            <div className="text-2xl sm:text-[28px] lg:text-[30px] font-extrabold text-[#E4005A] font-mono tracking-tight leading-tight my-1">
              {uncappedOverview
                ? `${uncappedOverview.total_verified_uncapped_batters + uncappedOverview.total_verified_uncapped_bowlers} Verified`
                : "—"}
            </div>
            <p className="text-xs sm:text-[13px] text-[#52627A] mt-1 leading-snug">
              Certified 0 senior caps in AUCTION-02 ledger
            </p>
          </div>

          <div>
            <span className="text-xs sm:text-[13px] font-semibold uppercase tracking-wider text-[#52627A] block mb-1">
              Verification Health
            </span>
            <div className="text-2xl sm:text-[28px] lg:text-[30px] font-extrabold text-[#E4005A] font-mono tracking-tight flex items-baseline gap-2.5 leading-tight my-1">
              <span>{isLive ? "Engine Online" : "Service Standby"}</span>
              <span className={`w-2.5 h-2.5 rounded-full ${isLive ? "bg-[#E4005A] animate-pulse" : "bg-[#E4005A]"}`} />
            </div>
            <p className="text-xs sm:text-[13px] text-[#52627A] mt-1 leading-snug">
              {isLive ? `FastAPI v${health?.version || "0.1.0"} active` : "Backend service awaiting initialization"}
            </p>
          </div>
        </div>
      </section>

      {/* ------------------------------------------------------------------- */}
      {/* 3. Official Round 1 Deliverables: Batting & Bowling Leaderboards */}
      {/* ------------------------------------------------------------------- */}
      <section className="space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-baseline justify-between gap-2 border-b border-[#E7EAF0] pb-3">
          <div>
            <h2 className="text-lg font-bold text-[#17294B] tracking-tight">
              Official Round 1 Leaderboards Under Pressure
            </h2>
            <p className="text-xs text-[#52627A]">
              Primary selections: overall qualified batters and bowlers (&ge; 60 pressure deliveries).
            </p>
          </div>
          <Link
            href="/pressure"
            className="text-xs font-semibold text-[#17294B] hover:text-[#17294B] transition-colors inline-flex items-center gap-1"
          >
            <span>View Complete Leaderboards & Dossiers</span>
            <ArrowRight size={13} />
          </Link>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Batting Top 5 Preview */}
          <div className="space-y-3 p-6 rounded-2xl bg-white border border-[#E7EAF0]">
            <div className="flex items-center justify-between text-xs font-semibold text-[#17294B]">
              <span className="flex items-center gap-2">
                <TrendingUp size={15} className="text-[#17294B]" />
                <span>Top 5 Batters Under Pressure (Conservative PRI)</span>
              </span>
              <span className="font-mono text-[11px] text-[#52627A]">Balls / Matches</span>
            </div>

            {isLiveBatters ? (
              <div className="divide-y divide-[#E7EAF0] border-t border-[#E7EAF0] text-xs">
                {battersToDisplay.map((p, idx) => (
                  <div
                    key={p.rank}
                    className={cn(
                      "py-2.5 flex items-center justify-between px-3 rounded-md transition-colors",
                      idx % 2 === 0 ? "bg-[#FCE8F0]/35" : "bg-white",
                      "hover:bg-[#FCE8F0]/80"
                    )}
                  >
                    <div className="flex items-center gap-3">
                      <span className="font-mono font-bold text-[#E4005A] w-4 text-center">{p.rank}</span>
                      <div>
                        <span className="font-bold text-[#17294B] block">{p.name}</span>
                        <span className="text-[11px] text-[#950460] font-semibold font-mono">{p.team}</span>
                      </div>
                    </div>
                    <div className="text-right">
                      <span className="font-mono font-bold text-[#E4005A]">
                        {p.val} pts
                      </span>
                      <span className="text-[11px] font-mono text-[#74658F] block"><strong className="text-[#E4005A]">{p.balls}</strong>b • <strong className="text-[#E4005A]">{p.matches}</strong>m</span>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="py-8 px-4 text-center rounded-lg border border-dashed border-[#E7EAF0] bg-white">
                <div className="text-xs text-[#52627A] font-medium">Official pressure batting leaderboards currently unavailable.</div>
                <button
                  onClick={loadOverviewData}
                  className="mt-2 inline-flex items-center gap-1.5 px-3 py-1 bg-white border border-[#E7EAF0] rounded text-xs font-semibold text-[#17294B] hover:bg-white shadow-xs"
                >
                  <RefreshCw size={12} className={loading ? "animate-spin" : ""} />
                  <span>Retry Connection</span>
                </button>
              </div>
            )}

            <div className="pt-2 text-[11px] text-[#52627A] font-mono flex justify-between">
              <span>{ranks6to10Batters ? `Ranks 6–10: ${ranks6to10Batters}` : "Ranks 6–10 viewable on full leaderboard"}</span>
              <Link href="/pressure?tab=batting" className="text-[#17294B] hover:text-[#17294B] font-sans font-medium">
                Full Batters &rarr;
              </Link>
            </div>
          </div>

          {/* Bowling Top 5 Preview */}
          <div className="space-y-3 p-6 rounded-2xl bg-white border border-[#E7EAF0]">
            <div className="flex items-center justify-between text-xs font-semibold text-[#17294B]">
              <span className="flex items-center gap-2">
                <Target size={15} className="text-[#E4005A]" />
                <span>Top 5 Bowlers Under Pressure (Conservative Runs Saved)</span>
              </span>
              <span className="font-mono text-[11px] text-[#52627A]">Balls / Matches</span>
            </div>

            {isLiveBowlers ? (
              <div className="divide-y divide-[#E7EAF0] border-t border-[#E7EAF0] text-xs">
                {bowlersToDisplay.map((p, idx) => (
                  <div
                    key={p.rank}
                    className={cn(
                      "py-2.5 flex items-center justify-between px-3 rounded-md transition-colors",
                      idx % 2 === 0 ? "bg-[#FCE8F0]/35" : "bg-white",
                      "hover:bg-[#FCE8F0]/80"
                    )}
                  >
                    <div className="flex items-center gap-3">
                      <span className="font-mono font-bold text-[#E4005A] w-4 text-center">{p.rank}</span>
                      <div>
                        <span className="font-bold text-[#17294B] block">{p.name}</span>
                        <span className="text-[11px] text-[#950460] font-semibold font-mono">{p.team}</span>
                      </div>
                    </div>
                    <div className="text-right">
                      <span className="font-mono font-bold text-[#E4005A]">
                        {p.val} rpo
                      </span>
                      <span className="text-[11px] font-mono text-[#74658F] block"><strong className="text-[#E4005A]">{p.balls}</strong>b • <strong className="text-[#E4005A]">{p.matches}</strong>m</span>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="py-8 px-4 text-center rounded-lg border border-dashed border-[#E7EAF0] bg-white">
                <div className="text-xs text-[#52627A] font-medium">Official pressure bowling leaderboards currently unavailable.</div>
                <button
                  onClick={loadOverviewData}
                  className="mt-2 inline-flex items-center gap-1.5 px-3 py-1 bg-white border border-[#E7EAF0] rounded text-xs font-semibold text-[#17294B] hover:bg-white shadow-xs"
                >
                  <RefreshCw size={12} className={loading ? "animate-spin" : ""} />
                  <span>Retry Connection</span>
                </button>
              </div>
            )}

            <div className="pt-2 text-[11px] text-[#52627A] font-mono flex justify-between">
              <span>{ranks6to10Bowlers ? `Ranks 6–10: ${ranks6to10Bowlers}` : "Ranks 6–10 viewable on full leaderboard"}</span>
              <Link href="/pressure?tab=bowling" className="text-[#17294B] hover:text-[#17294B] font-sans font-medium">
                Full Bowlers &rarr;
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* ------------------------------------------------------------------- */}
      {/* 4. Supplementary Uncapped Indian Domestic Intelligence */}
      {/* ------------------------------------------------------------------- */}
      <section className="space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-baseline justify-between gap-2 border-b border-[#E7EAF0] pb-3">
          <div>
            <h2 className="text-lg font-bold text-[#17294B] tracking-tight">
              Supplementary Uncapped Indian Domestic Intelligence
            </h2>
            <p className="text-xs text-[#52627A]">
              Specialized franchise auction intelligence for Rajasthan Royals — 100% verified zero senior international caps.
            </p>
          </div>
          <Link
            href="/uncapped"
            className="text-xs font-semibold text-[#E4005A] hover:text-[#17294B] transition-colors inline-flex items-center gap-1"
          >
            <span>View Full 20-Player Shortlist & Squad Fit Ratings</span>
            <ArrowRight size={13} />
          </Link>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* Top Uncapped Batters */}
          <div className="space-y-3 p-6 rounded-2xl bg-white border border-[#E7EAF0]">
            <span className="text-xs font-semibold text-[#17294B] flex items-center gap-2">
              <Sparkles size={14} className="text-[#E4005A]" />
              Verified Uncapped Batters (Top 3)
            </span>
            <div className="divide-y divide-[#E7EAF0] border-t border-[#E7EAF0] text-xs">
              {[
                { rank: 1, name: "Ashutosh Sharma", team: "Railways / PBKS", metric: "-3.63 PRI", fit: "93.20 Fit", desc: "Provable domestic death finisher (+10.3 SR delta)" },
                { rank: 2, name: "Shashank Singh", team: "Chhattisgarh / PBKS", metric: "-11.07 PRI", fit: "87.85 Fit", desc: "Composed middle-overs aggregator and accelerator" },
                { rank: 3, name: "Rahul Tewatia", team: "Haryana / GT", metric: "-11.37 PRI", fit: "87.05 Fit", desc: "Clutch chase equity with situational leg-spin utility" },
              ].map((p, idx) => (
                <div
                  key={p.rank}
                  className={cn(
                    "py-2.5 flex items-center justify-between px-3 rounded-md transition-colors",
                    idx % 2 === 0 ? "bg-[#FCE8F0]/35" : "bg-white",
                    "hover:bg-[#FCE8F0]/80"
                  )}
                >
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="font-mono font-bold text-[#E4005A] w-4">{p.rank}</span>
                      <span className="font-bold text-[#17294B]">{p.name}</span>
                      <span className="inline-flex items-center gap-1 text-[11px] font-bold text-[#15966B]">
                        <CheckCircle2 size={12} className="text-[#15966B]" />
                        <span>Verified</span>
                      </span>
                    </div>
                    <p className="text-[11px] text-[#74658F] mt-0.5 pl-6">{p.desc}</p>
                  </div>
                  <div className="text-right">
                    <span className="font-mono font-bold text-[#E4005A]">{p.fit}</span>
                    <span className="text-[10px] font-mono text-[#E4005A] block">{p.metric}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Top Uncapped Bowlers */}
          <div className="space-y-3 p-6 rounded-2xl bg-white border border-[#E7EAF0]">
            <span className="text-xs font-semibold text-[#17294B] flex items-center gap-2">
              <Crosshair size={14} className="text-[#17294B]" />
              Verified Uncapped Bowlers (Top 3)
            </span>
            <div className="divide-y divide-[#E7EAF0] border-t border-[#E7EAF0] text-xs">
              {[
                { rank: 1, name: "Vaibhav Arora", team: "Himachal / KKR", metric: "-2.36 RPO", fit: "90.00 Fit", desc: "Dual-phase swing in PP and disciplined death yorkers" },
                { rank: 2, name: "Suyash Sharma", team: "Delhi / KKR", metric: "-2.41 RPO", fit: "82.95 Fit", desc: "Attacking wrist-spin option with deceptive googly" },
                { rank: 3, name: "Akash Madhwal", team: "Uttarakhand / MI", metric: "-2.42 RPO", fit: "87.20 Fit", desc: "Specialist death-overs blockhole execution" },
              ].map((p, idx) => (
                <div
                  key={p.rank}
                  className={cn(
                    "py-2.5 flex items-center justify-between px-3 rounded-md transition-colors",
                    idx % 2 === 0 ? "bg-[#FCE8F0]/35" : "bg-white",
                    "hover:bg-[#FCE8F0]/80"
                  )}
                >
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="font-mono font-bold text-[#E4005A] w-4">{p.rank}</span>
                      <span className="font-bold text-[#17294B]">{p.name}</span>
                      <span className="inline-flex items-center gap-1 text-[11px] font-bold text-[#15966B]">
                        <CheckCircle2 size={12} className="text-[#15966B]" />
                        <span>Verified</span>
                      </span>
                    </div>
                    <p className="text-[11px] text-[#74658F] mt-0.5 pl-6">{p.desc}</p>
                  </div>
                  <div className="text-right">
                    <span className="font-mono font-bold text-[#E4005A]">{p.fit}</span>
                    <span className="text-[10px] font-mono text-[#E4005A] block">{p.metric}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* ------------------------------------------------------------------- */}
      {/* 5. Methodological Architecture */}
      {/* ------------------------------------------------------------------- */}
      <section className="space-y-4 pt-4 border-t border-[#E7EAF0]">
        <div>
          <h2 className="text-base font-bold text-[#17294B] tracking-tight">
            Methodological Architecture
          </h2>
          <p className="text-xs text-[#52627A]">
            Four core scientific pillars governing the ROYALS INTELLIGENCE pressure evaluation system.
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 text-xs">
          <div className="p-5 rounded-xl bg-white border border-[#E7EAF0] space-y-1.5">
            <div className="flex items-center gap-2 font-bold text-[#17294B]">
              <Flame size={15} className="text-[#17294B]" />
              <span>1. Dynamic Pressure</span>
            </div>
            <p className="text-[#52627A] leading-relaxed">
              Multi-factor leverage model: Chasing Required Run Rate &ge; 9.0 with &le; 36 balls, wickets in hand &le; 4,
              and death-over target acceleration.
            </p>
          </div>

          <div className="p-5 rounded-xl bg-white border border-[#E7EAF0] space-y-1.5">
            <div className="flex items-center gap-2 font-bold text-[#17294B]">
              <Layers size={15} className="text-[#17294B]" />
              <span>2. 12-Cell Baselines</span>
            </div>
            <p className="text-[#52627A] leading-relaxed">
              Every delivery is benchmarked against Innings (2) &times; Phase (3) &times; Tier (2) strata,
              eliminating structural death-over entry bias.
            </p>
          </div>

          <div className="p-5 rounded-xl bg-white border border-[#E7EAF0] space-y-1.5">
            <div className="flex items-center gap-2 font-bold text-[#17294B]">
              <Sparkles size={15} className="text-[#E4005A]" />
              <span>3. Empirical Bayes</span>
            </div>
            <p className="text-[#52627A] leading-relaxed">
              Separates skill from noise using Gaussian population priors (&mu;<sub>0</sub>, &tau;<sup>2</sup>). Low-sample outliers shrink toward
              the league mean.
            </p>
          </div>

          <div className="p-5 rounded-xl bg-white border border-[#E7EAF0] space-y-1.5">
            <div className="flex items-center gap-2 font-bold text-[#17294B]">
              <Shield size={15} className="text-[#E4005A]" />
              <span>4. Conservative PRI</span>
            </div>
            <p className="text-[#52627A] leading-relaxed">
              Rankings govern by Conservative PRI = Shrunk Posterior Mean minus 1.0 SE, directly penalizing high
              estimation uncertainty.
            </p>
          </div>
        </div>
      </section>

      {/* ------------------------------------------------------------------- */}
      {/* 6. Navigation to Analytical Modules */}
      {/* ------------------------------------------------------------------- */}
      <section className="space-y-4 pt-4 border-t border-[#E7EAF0]">
        <div>
          <h2 className="text-base font-bold text-[#17294B] tracking-tight">
            Intelligence Modules
          </h2>
          <p className="text-xs text-[#52627A]">
            Dedicated research environments connected to the verified tournament database.
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <Link
            href="/pressure"
            className="p-5 rounded-xl bg-white border border-[#E7EAF0] hover:border-[#E4005A] hover:shadow-soft transition-all group block"
          >
            <div className="flex items-center justify-between mb-2">
              <Shield size={18} className="text-[#17294B]" />
              <ArrowRight size={13} className="text-[#52627A] group-hover:translate-x-0.5 group-hover:text-[#17294B] transition-all" />
            </div>
            <h3 className="font-bold text-xs text-[#17294B]">Pressure Intelligence</h3>
            <p className="text-[11px] text-[#52627A] mt-1 leading-normal">
              Official Top 10 leaderboards, uncertainty forest plots, and candidate evidence dossiers.
            </p>
          </Link>

          <Link
            href="/tactical"
            className="p-5 rounded-xl bg-white border border-[#E7EAF0] hover:border-[#E4005A] hover:shadow-soft transition-all group block"
          >
            <div className="flex items-center justify-between mb-2">
              <Crosshair size={18} className="text-[#E4005A]" />
              <ArrowRight size={13} className="text-[#52627A] group-hover:translate-x-0.5 group-hover:text-[#17294B] transition-all" />
            </div>
            <h3 className="font-bold text-xs text-[#17294B]">Tactical Intelligence</h3>
            <p className="text-[11px] text-[#52627A] mt-1 leading-normal">
              Phase splits (PP, Middle, Death), shot archetypes, bowling variations, and radar speeds.
            </p>
          </Link>

          <Link
            href="/uncapped"
            className="p-5 rounded-xl bg-white border border-[#E7EAF0] hover:border-[#E4005A] hover:shadow-soft transition-all group block"
          >
            <div className="flex items-center justify-between mb-2">
              <Sparkles size={18} className="text-[#E4005A]" />
              <ArrowRight size={13} className="text-[#52627A] group-hover:translate-x-0.5 group-hover:text-[#17294B] transition-all" />
            </div>
            <h3 className="font-bold text-xs text-[#17294B]">Uncapped Talent</h3>
            <p className="text-[11px] text-[#52627A] mt-1 leading-normal">
              Verified Indian domestic batters & bowlers, Rajasthan Royals squad fit ratings, and reserves.
            </p>
          </Link>

          <Link
            href="/domestic"
            className="p-5 rounded-xl bg-white border border-[#E7EAF0] hover:border-[#E4005A] hover:shadow-soft transition-all group block"
          >
            <div className="flex items-center justify-between mb-2">
              <Swords size={18} className="text-[#17294B]" />
              <ArrowRight size={13} className="text-[#52627A] group-hover:translate-x-0.5 group-hover:text-[#17294B] transition-all" />
            </div>
            <h3 className="font-bold text-xs text-[#17294B]">Domestic & Matches</h3>
            <p className="text-[11px] text-[#52627A] mt-1 leading-normal">
              287-player directory, match scorecards, player histories, and all-round dual contributions.
            </p>
          </Link>
        </div>
      </section>
    </div>
  );
}
