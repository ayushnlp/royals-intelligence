"use client";

import React, { useState, useEffect, useCallback } from "react";
import Link from "next/link";
import {
  UncappedOverviewResponse,
  UncappedLeaderboardResponse,
  UncappedBattingItem,
  UncappedBowlingItem,
} from "@/types";
import {
  fetchUncappedOverview,
  fetchUncappedLeaderboards,
} from "@/lib/api";
import {
  Shield,
  Award,
  TrendingUp,
  Target,
  Sparkles,
  ChevronRight,
  X,
  FileText,
  RefreshCw,
  Crosshair,
  ArrowRight,
  CheckCircle2,
  AlertTriangle,
  SlidersHorizontal,
  Filter,
  RotateCcw,
} from "lucide-react";
import { cn } from "@/lib/utils";

// Filter Options Definitions
const PRESSURE_BALL_OPTIONS = [
  { label: "20 Balls", value: 20 },
  { label: "30 Balls", value: 30 },
  { label: "40 Balls", value: 40 },
  { label: "50 Balls", value: 50 },
  { label: "60 Balls (Default)", value: 60 },
];

const MATCH_OPTIONS = [
  { label: "All Matches", value: 0 },
  { label: "20 Matches", value: 20 },
  { label: "25 Matches", value: 25 },
  { label: "50 Matches", value: 50 },
];

export default function UncappedIntelligencePage() {
  const [activeTab, setActiveTab] = useState<"batting" | "bowling" | "governance">("batting");
  const [loading, setLoading] = useState<boolean>(true);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  // Configurable Prospect Sample Gate Filters
  const [minBalls, setMinBalls] = useState<number>(60);
  const [minMatches, setMinMatches] = useState<number>(0); // 0 = All Matches

  // Core Data
  const [overview, setOverview] = useState<UncappedOverviewResponse | null>(null);
  const [leaderboards, setLeaderboards] = useState<UncappedLeaderboardResponse | null>(null);

  // Selected Player Dossier Modal
  const [selectedPlayer, setSelectedPlayer] = useState<UncappedBattingItem | UncappedBowlingItem | null>(null);
  const [selectedDiscipline, setSelectedDiscipline] = useState<"batting" | "bowling">("batting");

  const loadUncappedData = useCallback(async (balls: number = minBalls, matches: number = minMatches) => {
    setLoading(true);
    setErrorMsg(null);
    try {
      const [ovRes, lbRes] = await Promise.all([
        fetchUncappedOverview({ min_balls: balls, min_matches: matches }),
        fetchUncappedLeaderboards({
          discipline: "all",
          limit: 50,
          qualified_only: true,
          min_balls: balls,
          min_matches: matches,
        }),
      ]);

      if (
        ovRes &&
        lbRes &&
        ((lbRes.batting_leaderboard?.length ?? 0) > 0 || (lbRes.bowling_leaderboard?.length ?? 0) > 0)
      ) {
        setOverview(ovRes);
        setLeaderboards(lbRes);
        setErrorMsg(null);
      } else {
        setOverview(ovRes || null);
        setLeaderboards(lbRes || null);
        if (!ovRes && !lbRes) {
          setErrorMsg("Uncapped player intelligence data is currently unavailable from backend service.");
        }
      }
    } catch (err: any) {
      setOverview(null);
      setLeaderboards(null);
      setErrorMsg(err.message || "Failed to communicate with Uncapped Intelligence backend service. Ensure backend is running on port 8000.");
    } finally {
      setLoading(false);
    }
  }, [minBalls, minMatches]);

  useEffect(() => {
    loadUncappedData(minBalls, minMatches);

    if (typeof window !== "undefined") {
      const params = new URLSearchParams(window.location.search);
      const tab = params.get("tab") || params.get("discipline");
      if (tab === "bowling") setActiveTab("bowling");
      if (tab === "batting") setActiveTab("batting");
      if (tab === "governance") setActiveTab("governance");
    }
  }, [loadUncappedData, minBalls, minMatches]);

  const handleBallsChange = (val: number) => {
    setMinBalls(val);
    loadUncappedData(val, minMatches);
  };

  const handleMatchesChange = (val: number) => {
    setMinMatches(val);
    loadUncappedData(minBalls, val);
  };

  const resetToOfficial = () => {
    setMinBalls(60);
    setMinMatches(0);
    loadUncappedData(60, 0);
  };

  const isExploratory = minBalls !== 60 || minMatches > 0;

  const openDossier = (player: UncappedBattingItem | UncappedBowlingItem, discipline: "batting" | "bowling") => {
    setSelectedPlayer(player);
    setSelectedDiscipline(discipline);
  };

  const closeDossier = () => {
    setSelectedPlayer(null);
  };

  return (
    <div className="space-y-8 pb-12">
      {/* ------------------------------------------------------------------- */}
      {/* 1. Editorial Header & Context */}
      {/* ------------------------------------------------------------------- */}
      <section className="space-y-3">
        <div className="flex flex-wrap items-center gap-3 text-xs">
          <span className="font-mono font-bold tracking-widest text-[#17294B] uppercase px-2.5 py-1 rounded-md bg-[#E4005A]/10 border border-[#E4005A]/30">
            Rajasthan Royals Scouting
          </span>
          <span className="text-[#17294B]/30">•</span>
          <span className="font-mono text-[#52627A]">
            AUCTION-02 Eligibility Ledger
          </span>
          <span className="text-[#17294B]/30">•</span>
          <span className="inline-flex items-center gap-1.5 text-[#E4005A] font-medium">
            <span className="w-1.5 h-1.5 rounded-full bg-[#E4005A]" />
            Strict Domestic Uncapped Scope
          </span>
        </div>

        <div className="flex flex-col md:flex-row md:items-end justify-between gap-4">
          <div className="max-w-3xl space-y-2">
            <h1 className="text-3xl md:text-4xl font-extrabold tracking-tight text-[#17294B] leading-tight font-heading">
              Uncapped Player Intelligence
            </h1>
            <p className="text-sm md:text-base text-[#52627A] leading-relaxed font-normal">
              Targeted talent discovery for Indian domestic prospects with zero senior international caps.
              Ranked under empirical high-pressure scenarios (&gt;1.50 Required Run Rate, middle/death overs, run-chases)
              with Empirical Bayes shrinkage and 1-SE conservative credible bounds.
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-3 shrink-0">
            <Link
              href="/pressure"
              className="inline-flex items-center gap-1.5 px-4 py-2 rounded-lg bg-[#17294B] text-white text-xs font-semibold hover:bg-[#17294B] transition-colors shadow-soft"
            >
              <Shield size={14} className="text-[#E4005A]" />
              <span>Official Global Top 10</span>
              <ArrowRight size={13} className="text-[#17294B]/30" />
            </Link>
            <Link
              href="/domestic"
              className="inline-flex items-center gap-1.5 px-4 py-2 rounded-lg bg-white border border-[#E7EAF0] text-[#17294B] text-xs font-semibold hover:bg-white transition-colors shadow-soft"
            >
              <Sparkles size={14} className="text-[#E4005A]" />
              <span>Domestic Match Dossiers</span>
            </Link>
          </div>
        </div>
      </section>

      {/* Connection Notice */}
      {errorMsg && (
        <div className="p-4 rounded-xl bg-[#E4005A]/10/90 border border-[#E4005A]/30 text-[#E4005A] flex items-center justify-between gap-4 shadow-xs">
          <div className="flex items-center gap-3">
            <AlertTriangle className="w-5 h-5 text-[#E4005A] shrink-0" />
            <div>
              <div className="text-xs font-bold uppercase tracking-wider flex items-center gap-2">
                <span>BACKEND CONNECTION NOTICE</span>
              </div>
              <div className="text-xs text-[#E4005A] mt-1">
                {errorMsg}
              </div>
            </div>
          </div>
          <button
            onClick={() => loadUncappedData(minBalls, minMatches)}
            className="px-3 py-1.5 rounded-lg bg-[#E4005A] text-white font-bold text-xs hover:bg-[#950460] transition-colors shrink-0 flex items-center gap-1.5"
          >
            <RefreshCw className="w-3.5 h-3.5" />
            <span>Retry Connection</span>
          </button>
        </div>
      )}

      {/* ------------------------------------------------------------------- */}
      {/* 2. Open Editorial Telemetry Strip (No Heavy Boxes) */}
      {/* ------------------------------------------------------------------- */}
      <section className="py-5 border-y border-[#E7EAF0]">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 md:gap-8">
          <div>
            <span className="text-[10px] font-mono uppercase tracking-wider text-[#52627A] font-semibold block mb-1">
              Top Uncapped Batter
            </span>
            <div className="text-xl md:text-2xl font-extrabold text-[#17294B] tracking-tight flex items-baseline gap-1.5">
              <span>{overview?.top_uncapped_batter ?? "—"}</span>
              <span className="w-1.5 h-1.5 rounded-full bg-[#E4005A]" />
            </div>
            <p className="text-xs text-[#52627A] mt-0.5">
              Rank #1 Qualified • Conservative PRI
            </p>
          </div>

          <div>
            <span className="text-[10px] font-mono uppercase tracking-wider text-[#52627A] font-semibold block mb-1">
              Top Uncapped Bowler
            </span>
            <div className="text-xl md:text-2xl font-extrabold text-[#17294B] tracking-tight flex items-baseline gap-1.5">
              <span>{overview?.top_uncapped_bowler ?? "—"}</span>
              <span className="w-1.5 h-1.5 rounded-full bg-[#E4005A]" />
            </div>
            <p className="text-xs text-[#52627A] mt-0.5">
              Rank #1 Qualified • Runs Saved (1-SE)
            </p>
          </div>

          <div>
            <span className="text-[10px] font-mono uppercase tracking-wider text-[#52627A] font-semibold block mb-1">
              Qualified Prospects
            </span>
            <div className="text-xl md:text-2xl font-extrabold text-[#17294B] font-mono tracking-tight">
              {overview
                ? `${overview.total_verified_uncapped_batters} Bat / ${overview.total_verified_uncapped_bowlers} Bowl`
                : "—"}
            </div>
            <p className="text-xs text-[#52627A] mt-0.5">
              {isExploratory
                ? `Exploratory: ≥${minBalls}b ${minMatches > 0 ? `& ≥${minMatches}m` : "(All matches)"}`
                : "Strict gate ≥ 60 pressure deliveries"}
            </p>
          </div>

          <div>
            <span className="text-[10px] font-mono uppercase tracking-wider text-[#52627A] font-semibold block mb-1">
              Sample Excluded
            </span>
            <div className="text-xl md:text-2xl font-extrabold text-[#E4005A] font-mono tracking-tight">
              {overview?.excluded_batters_count !== undefined
                ? `${overview.excluded_batters_count} Bat / ${overview.excluded_bowlers_count} Bowl`
                : "—"}
            </div>
            <p className="text-xs text-[#52627A] mt-0.5">
              {overview?.excluded_batters_count !== undefined
                ? `${overview.excluded_batters_count + (overview.excluded_bowlers_count ?? 0)} candidates below active gate`
                : "Awaiting backend telemetry"}
            </p>
          </div>
        </div>
      </section>

      {/* ------------------------------------------------------------------- */}
      {/* 3. Configurable Prospect Sample Gate & Qualification Filters */}
      {/* ------------------------------------------------------------------- */}
      <section className="bg-white rounded-2xl border border-[#E7EAF0] p-5 shadow-sm space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-[#E7EAF0] pb-3">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-lg bg-[#E4005A]/10 border border-[#E4005A]/30 flex items-center justify-center text-[#17294B] shrink-0">
              <SlidersHorizontal className="w-4 h-4" />
            </div>
            <div>
              <h2 className="text-sm font-bold text-[#17294B] flex items-center gap-2">
                <span>Prospect Qualification Gate & Scouting Filters</span>
                <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-[#FCE8F0] text-[#52627A] font-normal">
                  Configurable
                </span>
              </h2>
              <p className="text-xs text-[#52627A] mt-0.5">
                Dynamically adjust empirical sample gates. Official Round 1 Benchmark (≥60 balls) remains the default standard.
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2 shrink-0 self-start sm:self-auto">
            {!isExploratory ? (
              <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-[11px] font-mono font-bold bg-[#E4005A]/10 text-[#E4005A] border border-[#E4005A]/30">
                <Shield className="w-3.5 h-3.5 text-[#E4005A]" />
                <span>Official R1 Gate Active (Strict ≥ 60 Balls)</span>
              </span>
            ) : (
              <div className="flex items-center gap-2">
                <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-[11px] font-mono font-bold bg-[#E4005A]/10 text-[#17294B] border border-[#E4005A]/30">
                  <Sparkles className="w-3.5 h-3.5 text-[#17294B]" />
                  <span>Exploratory Scouting Filter Active</span>
                </span>
                <button
                  onClick={resetToOfficial}
                  className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg text-xs font-semibold text-[#52627A] hover:text-[#17294B] bg-[#FCE8F0] hover:bg-[#FCE8F0] transition-colors"
                  title="Reset to Official R1 Gate (60 Balls, All Matches)"
                >
                  <RotateCcw className="w-3 h-3" />
                  <span>Reset to Official</span>
                </button>
              </div>
            )}
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-5 pt-1">
          {/* Selector 1: Minimum Pressure Deliveries */}
          <div className="space-y-2">
            <div className="flex items-center justify-between text-xs">
              <span className="font-mono text-[10px] uppercase tracking-wider text-[#52627A] font-semibold flex items-center gap-1.5">
                <Crosshair className="w-3 h-3 text-[#17294B]" />
                <span>Minimum Pressure Deliveries</span>
              </span>
              <span className="font-mono font-bold text-[#17294B] text-xs">
                Active: {minBalls} Balls
              </span>
            </div>
            <div className="flex flex-wrap gap-1.5">
              {PRESSURE_BALL_OPTIONS.map((opt) => {
                const isSelected = minBalls === opt.value;
                return (
                  <button
                    key={opt.value}
                    onClick={() => handleBallsChange(opt.value)}
                    className={cn(
                      "px-3 py-1.5 rounded-lg text-xs transition-all font-mono",
                      isSelected
                        ? "bg-[#FCE8F0] text-[#17294B] border border-[#E4005A] font-bold shadow-xs"
                        : "bg-white text-[#52627A] border border-[#E7EAF0] hover:bg-[#FCE8F0]/40 hover:text-[#17294B] font-medium"
                    )}
                  >
                    {opt.label}
                  </button>
                );
              })}
            </div>
          </div>

          {/* Selector 2: Minimum Matches Played */}
          <div className="space-y-2">
            <div className="flex items-center justify-between text-xs">
              <span className="font-mono text-[10px] uppercase tracking-wider text-[#52627A] font-semibold flex items-center gap-1.5">
                <Filter className="w-3 h-3 text-[#17294B]" />
                <span>Minimum Matches Played</span>
              </span>
              <span className="font-mono font-bold text-[#17294B] text-xs">
                Active: {minMatches === 0 ? "All Matches" : `${minMatches} Matches`}
              </span>
            </div>
            <div className="flex flex-wrap gap-1.5">
              {MATCH_OPTIONS.map((opt) => {
                const isSelected = minMatches === opt.value;
                return (
                  <button
                    key={opt.value}
                    onClick={() => handleMatchesChange(opt.value)}
                    className={cn(
                      "px-3 py-1.5 rounded-lg text-xs transition-all font-mono",
                      isSelected
                        ? "bg-[#FCE8F0] text-[#17294B] border border-[#E4005A] font-bold shadow-xs"
                        : "bg-white text-[#52627A] border border-[#E7EAF0] hover:bg-[#FCE8F0]/40 hover:text-[#17294B] font-medium"
                    )}
                  >
                    {opt.label}
                  </button>
                );
              })}
            </div>
          </div>
        </div>

        {/* Dynamic Filter Feedback Telemetry Strip */}
        <div className="pt-3 border-t border-[#E7EAF0] flex flex-wrap items-center justify-between gap-3 text-xs">
          <div className="flex flex-wrap items-center gap-4 text-[#52627A] font-mono text-[11px]">
            <div>
              <span className="text-[#52627A]">Qualified Batters:</span>{" "}
              <span className="font-bold text-[#E4005A]">
                {leaderboards?.batting_count ?? overview?.total_verified_uncapped_batters ?? 0}
              </span>
            </div>
            <span className="text-[#17294B]/30">•</span>
            <div>
              <span className="text-[#52627A]">Qualified Bowlers:</span>{" "}
              <span className="font-bold text-[#17294B]">
                {leaderboards?.bowling_count ?? overview?.total_verified_uncapped_bowlers ?? 0}
              </span>
            </div>
            <span className="text-[#17294B]/30">•</span>
            <div>
              <span className="text-[#52627A]">Excluded by Criteria:</span>{" "}
              <span className="font-bold text-[#E4005A]">
                {overview?.excluded_batters_count !== undefined
                  ? `${overview.excluded_batters_count} Bat / ${overview.excluded_bowlers_count} Bowl (${(overview.excluded_batters_count || 0) + (overview.excluded_bowlers_count || 0)} total)`
                  : "—"}
              </span>
            </div>
          </div>

          <div className="text-[11px] font-mono text-[#52627A] flex items-center gap-1.5">
            <span className="w-1.5 h-1.5 rounded-full bg-[#E4005A]" />
            <span>{overview?.sample_gate_applied ?? "Gate active"}</span>
          </div>
        </div>
      </section>

      {/* ------------------------------------------------------------------- */}
      {/* 4. Editorial Segmented Tab Navigation */}
      {/* ------------------------------------------------------------------- */}
      <div className="flex items-center gap-6 border-b border-[#E7EAF0]">
        <button
          onClick={() => setActiveTab("batting")}
          className={cn(
            "flex items-center gap-2 py-3 text-xs font-semibold transition-all border-b-2 -mb-px whitespace-nowrap cursor-pointer",
            activeTab === "batting"
              ? "border-[#E4005A] text-[#E4005A] font-bold"
              : "border-transparent text-[#52627A] hover:text-[#17294B]"
          )}
        >
          <TrendingUp className={cn("w-4 h-4", activeTab === "batting" ? "text-[#E4005A]" : "text-[#52627A]")} />
          <span>
            Top Uncapped Batters Under Pressure ({leaderboards?.batting_count ?? 0})
          </span>
        </button>

        <button
          onClick={() => setActiveTab("bowling")}
          className={cn(
            "flex items-center gap-2 py-3 text-xs font-semibold transition-all border-b-2 -mb-px whitespace-nowrap cursor-pointer",
            activeTab === "bowling"
              ? "border-[#E4005A] text-[#E4005A] font-bold"
              : "border-transparent text-[#52627A] hover:text-[#17294B]"
          )}
        >
          <Target className={cn("w-4 h-4", activeTab === "bowling" ? "text-[#E4005A]" : "text-[#52627A]")} />
          <span>
            Top Uncapped Bowlers Under Pressure ({leaderboards?.bowling_count ?? 0})
          </span>
        </button>

        <button
          onClick={() => setActiveTab("governance")}
          className={cn(
            "flex items-center gap-2 py-3 text-xs font-semibold transition-all border-b-2 -mb-px whitespace-nowrap cursor-pointer",
            activeTab === "governance"
              ? "border-[#E4005A] text-[#E4005A] font-bold"
              : "border-transparent text-[#52627A] hover:text-[#17294B]"
          )}
        >
          <FileText className={cn("w-4 h-4", activeTab === "governance" ? "text-[#E4005A]" : "text-[#52627A]")} />
          <span>Eligibility Governance & Safeguards</span>
        </button>
      </div>

      {/* ------------------------------------------------------------------- */}
      {/* TAB 1: TOP UNCAPPED BATTERS */}
      {/* ------------------------------------------------------------------- */}
      {activeTab === "batting" && (
        <div className="space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
            <div>
              <h2 className="text-base font-bold text-[#17294B]">
                Verified Indian Uncapped Batters Under Pressure
              </h2>
              <p className="text-xs text-[#52627A]">
                Ranked strictly by Conservative PRI (1-SE Lower Credible Bound in Strike Rate points). Domestic Indian players with 0 senior international caps.
              </p>
            </div>
            <div className="flex items-center gap-2 self-start sm:self-auto">
              <span className="text-[11px] font-mono font-medium text-[#E4005A] bg-[#E4005A]/10 px-2.5 py-1 rounded-full border border-[#E4005A]/30/60">
                {leaderboards?.batting_count ?? 0} Qualified Batters
              </span>
            </div>
          </div>

          <div className="bg-white rounded-2xl border border-[#E7EAF0] shadow-sm overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead className="bg-white/80 text-[#52627A] uppercase text-[10px] tracking-wider border-b border-[#E7EAF0] font-mono">
                  <tr>
                    <th className="px-4 py-3 font-sans font-semibold">Rank & Batter</th>
                    <th className="px-4 py-3 font-sans font-semibold">Franchise & Role</th>
                    <th className="px-4 py-3 text-right font-semibold">Conservative PRI</th>
                    <th className="px-4 py-3 text-right font-semibold">Posterior Mean (&theta;)</th>
                    <th className="px-4 py-3 text-right font-semibold">Uncertainty (SE)</th>
                    <th className="px-4 py-3 text-right font-semibold">95% Credible Region</th>
                    <th className="px-4 py-3 text-right font-semibold">Pressure Balls</th>
                    <th className="px-4 py-3 text-right font-semibold">Observed SR</th>
                    <th className="px-4 py-3 text-center font-sans font-semibold">Eligibility Status</th>
                    <th className="px-4 py-3 text-center font-sans font-semibold">Dossier</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 font-mono">
                  {loading ? (
                    <tr>
                      <td colSpan={10} className="px-6 py-12 text-center text-[#52627A]">
                        <div className="flex flex-col items-center justify-center gap-2">
                          <RefreshCw className="w-5 h-5 animate-spin text-[#E4005A]" />
                          <span className="text-xs">Loading uncapped batting intelligence...</span>
                        </div>
                      </td>
                    </tr>
                  ) : leaderboards?.batting_leaderboard && leaderboards.batting_leaderboard.length > 0 ? (
                    leaderboards.batting_leaderboard.map((batter, idx) => {
                      const isTop1 = batter.uncapped_rank === 1;
                      const isTop3 = batter.uncapped_rank <= 3;
                      const isOfficial = batter.is_official_r1_qualified ?? (batter.pressure_legal_balls >= 60);
                      return (
                        <tr
                          key={batter.player_id}
                          className={cn(
                            "transition-colors",
                            idx % 2 === 0 ? "bg-[#FCE8F0]/35" : "bg-[#EEF4FC]/35",
                            "hover:bg-[#FCE8F0]/80"
                          )}
                        >
                          <td className="px-4 py-3 font-sans text-[#17294B]">
                            <div className="flex items-center gap-2.5">
                              <span
                                className={cn(
                                  "w-6 h-6 rounded-full flex items-center justify-center text-[10px] font-mono font-bold shrink-0",
                                  isTop1
                                    ? "bg-[#E4005A] text-white"
                                    : isTop3
                                      ? "bg-[#17294B] text-white"
                                      : "bg-[#FCE8F0] text-[#74658F]"
                                )}
                              >
                                {batter.uncapped_rank}
                              </span>
                              <div>
                                <div className="font-bold text-[#17294B]">{batter.player_name}</div>
                                <div className="text-[10px] font-mono text-[#74658F]">
                                  Overall R1 #{batter.overall_r1_rank} • ID: {batter.player_id}
                                </div>
                              </div>
                            </div>
                          </td>
                          <td className="px-4 py-3 font-sans">
                            <div className="font-semibold text-[#950460]">{batter.franchise}</div>
                            <div className="text-[10px] text-[#74658F] font-mono">{batter.tactical_role}</div>
                          </td>
                          <td className="px-4 py-3 text-right">
                            <span className="font-bold text-sm text-[#E4005A] font-mono">
                              {batter.conservative_pri > 0
                                ? `+${batter.conservative_pri.toFixed(2)}`
                                : batter.conservative_pri.toFixed(2)}{" "}
                              <span className="text-[10px] font-normal text-[#74658F]">SR</span>
                            </span>
                          </td>
                          <td className="px-4 py-3 text-right text-[#17294B] font-bold">
                            {batter.posterior_mean > 0
                              ? `+${batter.posterior_mean.toFixed(2)}`
                              : batter.posterior_mean.toFixed(2)}
                          </td>
                          <td className="px-4 py-3 text-right text-[#74658F]">
                            &plusmn;{batter.posterior_se.toFixed(2)}
                          </td>
                          <td className="px-4 py-3 text-right text-[#74658F] text-[11px]">
                            [{batter.ci_95_lower.toFixed(1)}, +{batter.ci_95_upper.toFixed(1)}]
                          </td>
                          <td className="px-4 py-3 text-right text-[#17294B] font-bold">
                            {batter.pressure_legal_balls}
                          </td>
                          <td className="px-4 py-3 text-right text-[#17294B] font-bold">
                            {batter.observed_strike_rate.toFixed(1)}
                          </td>
                          <td className="px-4 py-3 text-center font-sans">
                            <div className="flex flex-col items-center gap-0.5">
                              <span
                                className="inline-flex items-center gap-1 text-[11px] font-bold text-[#15966B]"
                                title={
                                  isOfficial
                                    ? "Meets strict Official Round 1 gate (>=60 pressure balls)"
                                    : "Qualified under active exploratory scouting filter"
                                }
                              >
                                <CheckCircle2 size={12} className="text-[#15966B]" />
                                <span>Verified</span>
                              </span>
                              <span className="text-[9px] font-mono text-[#74658F]">
                                {batter.pressure_legal_balls}b / {batter.pressure_matches}m
                              </span>
                            </div>
                          </td>
                          <td className="px-4 py-3 text-center font-sans">
                            <button
                              onClick={() => openDossier(batter, "batting")}
                              className="px-2.5 py-1 rounded-md bg-[#FCE8F0] hover:bg-[#FCE8F0] text-[#17294B] text-[11px] font-semibold transition-all inline-flex items-center gap-1"
                            >
                              <span>Dossier</span>
                              <ChevronRight className="w-3 h-3 text-[#52627A]" />
                            </button>
                          </td>
                        </tr>
                      );
                    })
                  ) : (
                    <tr>
                      <td colSpan={10} className="px-6 py-12 text-center text-[#52627A]">
                        <div className="flex flex-col items-center justify-center gap-2">
                          <AlertTriangle className="w-7 h-7 text-[#E4005A]" />
                          <span className="font-semibold text-[#17294B]">
                            No Uncapped Batters Match Current Filter Criteria
                          </span>
                          <span className="text-xs text-[#52627A] max-w-md">
                            Minimum requirements ({minBalls} Balls, {minMatches === 0 ? "All Matches" : `${minMatches} Matches`}) excluded all candidates.
                          </span>
                          <button
                            onClick={resetToOfficial}
                            className="mt-2 px-3 py-1.5 rounded-lg bg-[#17294B] text-white text-xs font-semibold hover:bg-[#17294B] transition-colors flex items-center gap-1.5"
                          >
                            <RotateCcw className="w-3.5 h-3.5" />
                            <span>Reset to Official Gate (60 Balls)</span>
                          </button>
                        </div>
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* ------------------------------------------------------------------- */}
      {/* TAB 2: TOP UNCAPPED BOWLERS */}
      {/* ------------------------------------------------------------------- */}
      {activeTab === "bowling" && (
        <div className="space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
            <div>
              <h2 className="text-base font-bold text-[#17294B]">
                Verified Indian Uncapped Bowlers Under Pressure
              </h2>
              <p className="text-xs text-[#52627A]">
                Ranked strictly by Conservative Runs Saved per 6 balls (1-SE Lower Credible Bound in Economy). Crucial scouting insight since all official Top 10 bowlers are capped internationals.
              </p>
            </div>
            <div className="flex items-center gap-2 self-start sm:self-auto">
              <span className="text-[11px] font-mono font-medium text-[#17294B] bg-[#FCE8F0] px-2.5 py-1 rounded-full border border-[#17294B]/20">
                {leaderboards?.bowling_count ?? 0} Qualified Bowlers
              </span>
            </div>
          </div>

          <div className="bg-white rounded-2xl border border-[#E7EAF0] shadow-sm overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead className="bg-white/80 text-[#52627A] uppercase text-[10px] tracking-wider border-b border-[#E7EAF0] font-mono">
                  <tr>
                    <th className="px-4 py-3 font-sans font-semibold">Rank & Bowler</th>
                    <th className="px-4 py-3 font-sans font-semibold">Franchise & Role</th>
                    <th className="px-4 py-3 text-right font-semibold">Runs Saved (1-SE)</th>
                    <th className="px-4 py-3 text-right font-semibold">Posterior Mean (&theta;)</th>
                    <th className="px-4 py-3 text-right font-semibold">Uncertainty (SE)</th>
                    <th className="px-4 py-3 text-right font-semibold">95% Credible Region</th>
                    <th className="px-4 py-3 text-right font-semibold">Pressure Balls</th>
                    <th className="px-4 py-3 text-right font-semibold">Observed Econ</th>
                    <th className="px-4 py-3 text-center font-sans font-semibold">Eligibility Status</th>
                    <th className="px-4 py-3 text-center font-sans font-semibold">Dossier</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 font-mono">
                  {loading ? (
                    <tr>
                      <td colSpan={10} className="px-6 py-12 text-center text-[#52627A]">
                        <div className="flex flex-col items-center justify-center gap-2">
                          <RefreshCw className="w-5 h-5 animate-spin text-[#17294B]" />
                          <span className="text-xs">Loading uncapped bowling intelligence...</span>
                        </div>
                      </td>
                    </tr>
                  ) : leaderboards?.bowling_leaderboard && leaderboards.bowling_leaderboard.length > 0 ? (
                    leaderboards.bowling_leaderboard.map((bowler, idx) => {
                      const isTop1 = bowler.uncapped_rank === 1;
                      const isTop3 = bowler.uncapped_rank <= 3;
                      const isOfficial = bowler.is_official_r1_qualified ?? (bowler.pressure_legal_balls >= 60);
                      return (
                        <tr
                          key={bowler.player_id}
                          className={cn(
                            "transition-colors",
                            idx % 2 === 0 ? "bg-[#FCE8F0]/35" : "bg-[#EEF4FC]/35",
                            "hover:bg-[#FCE8F0]/80"
                          )}
                        >
                          <td className="px-4 py-3 font-sans text-[#17294B]">
                            <div className="flex items-center gap-2.5">
                              <span
                                className={cn(
                                  "w-6 h-6 rounded-full flex items-center justify-center text-[10px] font-mono font-bold shrink-0",
                                  isTop1
                                    ? "bg-[#E4005A] text-white"
                                    : isTop3
                                      ? "bg-[#17294B] text-white"
                                      : "bg-[#FCE8F0] text-[#74658F]"
                                )}
                              >
                                {bowler.uncapped_rank}
                              </span>
                              <div>
                                <div className="font-bold text-[#17294B]">{bowler.player_name}</div>
                                <div className="text-[10px] font-mono text-[#74658F]">
                                  Overall R1 #{bowler.overall_r1_rank} • ID: {bowler.player_id}
                                </div>
                              </div>
                            </div>
                          </td>
                          <td className="px-4 py-3 font-sans">
                            <div className="font-semibold text-[#950460]">{bowler.franchise}</div>
                            <div className="text-[10px] text-[#74658F] font-mono">{bowler.tactical_role}</div>
                          </td>
                          <td className="px-4 py-3 text-right">
                            <span className="font-bold text-sm text-[#17294B] font-mono">
                              {bowler.conservative_runs_saved.toFixed(2)}{" "}
                              <span className="text-[10px] font-normal text-[#74658F]">RPO</span>
                            </span>
                          </td>
                          <td className="px-4 py-3 text-right text-[#17294B] font-bold">
                            {bowler.posterior_mean > 0
                              ? `+${bowler.posterior_mean.toFixed(2)}`
                              : bowler.posterior_mean.toFixed(2)}
                          </td>
                          <td className="px-4 py-3 text-right text-[#74658F]">
                            &plusmn;{bowler.posterior_se.toFixed(2)}
                          </td>
                          <td className="px-4 py-3 text-right text-[#74658F] text-[11px]">
                            [{bowler.ci_95_lower.toFixed(2)}, +{bowler.ci_95_upper.toFixed(2)}]
                          </td>
                          <td className="px-4 py-3 text-right text-[#17294B] font-bold">
                            {bowler.pressure_legal_balls}
                          </td>
                          <td className="px-4 py-3 text-right text-[#17294B] font-bold">
                            {bowler.observed_economy.toFixed(2)}
                          </td>
                          <td className="px-4 py-3 text-center font-sans">
                            <div className="flex flex-col items-center gap-0.5">
                              <span
                                className="inline-flex items-center gap-1 text-[11px] font-bold text-[#15966B]"
                                title={
                                  isOfficial
                                    ? "Meets strict Official Round 1 gate (>=60 pressure balls)"
                                    : "Qualified under active exploratory scouting filter"
                                }
                              >
                                <CheckCircle2 size={12} className="text-[#15966B]" />
                                <span>Verified</span>
                              </span>
                              <span className="text-[9px] font-mono text-[#74658F]">
                                {bowler.pressure_legal_balls}b / {bowler.pressure_matches}m
                              </span>
                            </div>
                          </td>
                          <td className="px-4 py-3 text-center font-sans">
                            <button
                              onClick={() => openDossier(bowler, "bowling")}
                              className="px-2.5 py-1 rounded-md bg-[#FCE8F0] hover:bg-[#FCE8F0] text-[#17294B] text-[11px] font-semibold transition-all inline-flex items-center gap-1"
                            >
                              <span>Dossier</span>
                              <ChevronRight className="w-3 h-3 text-[#52627A]" />
                            </button>
                          </td>
                        </tr>
                      );
                    })
                  ) : (
                    <tr>
                      <td colSpan={10} className="px-6 py-12 text-center text-[#52627A]">
                        <div className="flex flex-col items-center justify-center gap-2">
                          <AlertTriangle className="w-7 h-7 text-[#E4005A]" />
                          <span className="font-semibold text-[#17294B]">
                            No Uncapped Bowlers Match Current Filter Criteria
                          </span>
                          <span className="text-xs text-[#52627A] max-w-md">
                            Minimum requirements ({minBalls} Balls, {minMatches === 0 ? "All Matches" : `${minMatches} Matches`}) excluded all candidates.
                          </span>
                          <button
                            onClick={resetToOfficial}
                            className="mt-2 px-3 py-1.5 rounded-lg bg-[#17294B] text-white text-xs font-semibold hover:bg-[#17294B] transition-colors flex items-center gap-1.5"
                          >
                            <RotateCcw className="w-3.5 h-3.5" />
                            <span>Reset to Official Gate (60 Balls)</span>
                          </button>
                        </div>
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* ------------------------------------------------------------------- */}
      {/* TAB 3: ELIGIBILITY GOVERNANCE & SAFEGUARDS */}
      {/* ------------------------------------------------------------------- */}
      {activeTab === "governance" && (
        <div className="space-y-6">
          <div className="bg-white rounded-2xl border border-[#E7EAF0] p-6 shadow-sm space-y-4">
            <div className="flex items-center gap-3 border-b border-[#E7EAF0] pb-4">
              <Shield className="w-5 h-5 text-[#E4005A]" />
              <h2 className="text-lg font-bold text-[#17294B]">
                AUCTION-02 Domestic Eligibility Ledger & Protocols
              </h2>
            </div>
            <p className="text-sm text-[#52627A] leading-relaxed max-w-3xl">
              To prevent misclassification and preserve auction compliance, all uncapped evaluations adhere to strict BCCI Player Regulations for the IPL 2025/2026 cycle. Retired international stars (e.g., MS Dhoni) and multi-format international capped players (e.g., Virat Kohli, Rohit Sharma, Jasprit Bumrah) are categorically quarantined from uncapped discovery pipelines.
            </p>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-2">
              <div className="p-4 rounded-xl bg-white border border-[#E7EAF0] space-y-2">
                <div className="flex items-center gap-2 text-xs font-bold text-[#17294B] font-mono uppercase">
                  <CheckCircle2 className="w-4 h-4 text-[#E4005A]" />
                  <span>Rule 1: International Cap Barrier</span>
                </div>
                <p className="text-xs text-[#52627A] leading-relaxed">
                  Zero appearances in Senior Men&apos;s Tests, ODIs, or T20Is for India or any ICC Full Member nation. Any international appearance immediately revokes uncapped eligibility.
                </p>
              </div>

              <div className="p-4 rounded-xl bg-white border border-[#E7EAF0] space-y-2">
                <div className="flex items-center gap-2 text-xs font-bold text-[#17294B] font-mono uppercase">
                  <AlertTriangle className="w-4 h-4 text-[#E4005A]" />
                  <span>Rule 2: Retirement Exclusion</span>
                </div>
                <p className="text-xs text-[#52627A] leading-relaxed">
                  The BCCI 5-year retirement clause (IPL Rule 4.3) is quarantined to administrative auction rosters and strictly excluded from primary talent discovery scouting models.
                </p>
              </div>

              <div className="p-4 rounded-xl bg-white border border-[#E7EAF0] space-y-2">
                <div className="flex items-center gap-2 text-xs font-bold text-[#17294B] font-mono uppercase">
                  <Crosshair className="w-4 h-4 text-[#17294B]" />
                  <span>Rule 3: Configurable Sample Gate</span>
                </div>
                <p className="text-xs text-[#52627A] leading-relaxed">
                  Default strict benchmark requires &ge; 60 pressure deliveries. Exploratory filters allow adjusting down to 20 balls for early scouting without corrupting official rankings.
                </p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* ------------------------------------------------------------------- */}
      {/* 5. Player Dossier Slide-Over / Modal */}
      {/* ------------------------------------------------------------------- */}
      {selectedPlayer && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-[#17294B]/50 backdrop-blur-sm animate-in fade-in duration-200">
          <div className="bg-white rounded-2xl max-w-2xl w-full p-6 shadow-2xl border border-[#E7EAF0] space-y-6 max-h-[90vh] overflow-y-auto">
            {/* Header */}
            <div className="flex items-start justify-between border-b border-[#E7EAF0] pb-4">
              <div>
                <div className="flex items-center gap-2">
                  <h3 className="text-xl font-extrabold text-[#17294B]">{selectedPlayer.player_name}</h3>
                  <span className="text-xs font-mono font-bold text-[#17294B] px-2 py-0.5 rounded-full bg-[#E4005A]/10 border border-[#E4005A]/30">
                    Uncapped #{selectedPlayer.uncapped_rank}
                  </span>
                  <span
                    className={cn(
                      "text-[10px] font-mono px-2 py-0.5 rounded-full border",
                      selectedPlayer.is_official_r1_qualified
                        ? "bg-[#E4005A]/10 text-[#E4005A] border-[#E4005A]/30"
                        : "bg-[#E4005A]/10 text-[#17294B] border-[#E4005A]/30"
                    )}
                  >
                    {selectedPlayer.is_official_r1_qualified ? "Official R1 Benchmark" : "Exploratory Qualified"}
                  </span>
                </div>
                <div className="text-xs text-[#52627A] font-mono mt-1">
                  {selectedPlayer.franchise} • Tactical Role: {selectedPlayer.tactical_role}
                </div>
              </div>
              <button
                onClick={closeDossier}
                className="w-8 h-8 rounded-lg bg-[#FCE8F0] hover:bg-[#FCE8F0] text-[#52627A] flex items-center justify-center transition-colors"
              >
                <X size={16} />
              </button>
            </div>

            {/* Audit Status Section */}
            <div className="p-4 rounded-xl bg-[#E4005A]/10/70 border border-[#E4005A]/30/80 space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-xs font-mono font-bold text-[#E4005A] uppercase tracking-wider">
                  BCCI Eligibility Status
                </span>
                <span className="px-2.5 py-0.5 rounded-full text-xs font-mono font-bold bg-[#E4005A] text-white">
                  {selectedPlayer.eligibility_status}
                </span>
              </div>
              <p className="text-xs text-[#17294B] leading-relaxed">{selectedPlayer.eligibility_reason}</p>
              <div className="pt-2 border-t border-[#E4005A]/30/60 flex flex-wrap items-center justify-between text-[11px] font-mono text-[#52627A]">
                <span>Source: {selectedPlayer.verification_source}</span>
                <span>Verified: {selectedPlayer.verification_date}</span>
              </div>
            </div>

            {/* Performance Metrics Strip */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
              <div className="p-3.5 rounded-xl bg-white border border-[#E7EAF0]">
                <div className="text-[10px] text-[#52627A] font-mono uppercase">Pressure Balls</div>
                <div className="text-lg font-extrabold font-mono text-[#17294B] mt-1">
                  {selectedPlayer.pressure_legal_balls}
                </div>
              </div>

              <div className="p-3.5 rounded-xl bg-white border border-[#E7EAF0]">
                <div className="text-[10px] text-[#52627A] font-mono uppercase">Pressure Matches</div>
                <div className="text-lg font-extrabold font-mono text-[#17294B] mt-1">
                  {selectedPlayer.pressure_matches}
                </div>
              </div>

              <div className="p-3.5 rounded-xl bg-white border border-[#E7EAF0]">
                <div className="text-[10px] text-[#52627A] font-mono uppercase">
                  {selectedDiscipline === "batting" ? "Conservative PRI" : "Runs Saved"}
                </div>
                <div className="text-lg font-extrabold font-mono text-[#E4005A] mt-1">
                  {selectedDiscipline === "batting"
                    ? `${(selectedPlayer as UncappedBattingItem).conservative_pri.toFixed(2)} SR`
                    : `${(selectedPlayer as UncappedBowlingItem).conservative_runs_saved.toFixed(2)} RPO`}
                </div>
              </div>

              <div className="p-3.5 rounded-xl bg-white border border-[#E7EAF0]">
                <div className="text-[10px] text-[#52627A] font-mono uppercase">Overall R1 Rank</div>
                <div className="text-lg font-extrabold font-mono text-[#17294B] mt-1">
                  #{selectedPlayer.overall_r1_rank}
                </div>
              </div>
            </div>

            <div className="p-4 rounded-xl bg-white border border-[#E7EAF0]">
              <div className="text-xs font-bold text-[#17294B] mb-1">Bayesian Reliability Summary</div>
              <p className="text-xs text-[#52627A] leading-relaxed">
                Posterior Mean (&theta;) is {selectedPlayer.posterior_mean > 0 ? `+${selectedPlayer.posterior_mean.toFixed(2)}` : selectedPlayer.posterior_mean.toFixed(2)} with standard error &plusmn;{selectedPlayer.posterior_se.toFixed(2)}. The 95% Bayesian credible interval spans [{selectedPlayer.ci_95_lower.toFixed(1)}, +{selectedPlayer.ci_95_upper.toFixed(1)}], confirming statistically significant pressure reliability under the 1-SE conservative rule.
              </p>
            </div>

            <div className="flex justify-end pt-2">
              <button
                onClick={closeDossier}
                className="px-5 py-2 rounded-lg bg-[#17294B] hover:bg-[#17294B] text-xs font-semibold text-white transition-colors"
              >
                Close Dossier
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
