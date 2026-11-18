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
import uncappedFallbackData from "@/lib/uncapped_fallback_data.json";
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

  // Client-side fallback dynamic calculator (for offline/resilience)
  const computeClientFallback = useCallback((balls: number, matches: number) => {
    const rawBatters = (uncappedFallbackData.batters as any[]) || [];
    const rawBowlers = (uncappedFallbackData.bowlers as any[]) || [];

    const isOfficial = balls === 60 && matches === 0;

    const filteredBatters: UncappedBattingItem[] = rawBatters
      .filter((b) => {
        const pBalls = Number(b.pressure_legal_balls || 0);
        const pMatches = Number(b.pressure_matches || 0);
        if (isOfficial) {
          return pBalls >= 60 || (pBalls >= 50 && pMatches >= 10);
        }
        return pBalls >= balls && (matches === 0 || pMatches >= matches);
      })
      .map((b, idx) => ({
        ...b,
        uncapped_rank: idx + 1,
        is_official_r1_qualified: Boolean(
          Number(b.pressure_legal_balls || 0) >= 60 ||
          (Number(b.pressure_legal_balls || 0) >= 50 && Number(b.pressure_matches || 0) >= 10)
        ),
        meets_active_gate: true,
      }));

    const filteredBowlers: UncappedBowlingItem[] = rawBowlers
      .filter((bw) => {
        const pBalls = Number(bw.pressure_legal_balls || 0);
        const pMatches = Number(bw.pressure_matches || 0);
        if (isOfficial) {
          return pBalls >= 60 || (pBalls >= 50 && pMatches >= 10);
        }
        return pBalls >= balls && (matches === 0 || pMatches >= matches);
      })
      .map((bw, idx) => ({
        ...bw,
        uncapped_rank: idx + 1,
        is_official_r1_qualified: Boolean(
          Number(bw.pressure_legal_balls || 0) >= 60 ||
          (Number(bw.pressure_legal_balls || 0) >= 50 && Number(bw.pressure_matches || 0) >= 10)
        ),
        meets_active_gate: true,
      }));

    const isExploratory = !isOfficial;
    const matchStr = matches > 0 ? ` & >= ${matches} matches` : " & All Matches";
    const gateDesc = isOfficial
      ? ">= 60 pressure deliveries (or >= 50 balls & 10 matches) [Official R1 Benchmark]"
      : `>= ${balls} pressure deliveries${matchStr} [Exploratory Scouting Filter]`;

    return {
      overview: {
        total_verified_uncapped_batters: filteredBatters.length,
        total_verified_uncapped_bowlers: filteredBowlers.length,
        top_uncapped_batter: filteredBatters.length > 0 ? filteredBatters[0].player_name : null,
        top_uncapped_bowler: filteredBowlers.length > 0 ? filteredBowlers[0].player_name : null,
        sample_gate_applied: gateDesc,
        governing_statute: "BCCI IPL Player Regulations 2025/2026",
        audit_date: "2026-11-16",
        min_balls_applied: balls,
        min_matches_applied: matches,
        is_exploratory_filter: isExploratory,
        total_pool_batters: rawBatters.length,
        total_pool_bowlers: rawBowlers.length,
        excluded_batters_count: rawBatters.length - filteredBatters.length,
        excluded_bowlers_count: rawBowlers.length - filteredBowlers.length,
      },
      leaderboards: {
        discipline_filter: "all",
        qualified_only: true,
        batting_count: filteredBatters.length,
        bowling_count: filteredBowlers.length,
        batting_leaderboard: filteredBatters,
        bowling_leaderboard: filteredBowlers,
        sample_gate: gateDesc,
        governing_statute: "BCCI IPL Player Regulations 2025/2026",
        audit_date: "2026-11-16",
        min_balls_applied: balls,
        min_matches_applied: matches,
        is_exploratory_filter: isExploratory,
        excluded_count: (rawBatters.length + rawBowlers.length) - (filteredBatters.length + filteredBowlers.length),
        total_pool_count: rawBatters.length + rawBowlers.length,
      },
    };
  }, []);

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

      if (ovRes && lbRes) {
        setOverview(ovRes);
        setLeaderboards(lbRes);
      } else {
        // Graceful client fallback using verified domestic dataset
        const fallback = computeClientFallback(balls, matches);
        setOverview(fallback.overview);
        setLeaderboards(fallback.leaderboards);
      }
    } catch (err: any) {
      // Graceful fallback on network error
      const fallback = computeClientFallback(balls, matches);
      setOverview(fallback.overview);
      setLeaderboards(fallback.leaderboards);
    } finally {
      setLoading(false);
    }
  }, [minBalls, minMatches, computeClientFallback]);

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
          <span className="font-mono font-bold tracking-widest text-[#E91E8C] uppercase">
            Rajasthan Royals Scouting
          </span>
          <span className="text-slate-300">•</span>
          <span className="font-mono text-slate-500">
            AUCTION-02 Eligibility Ledger
          </span>
          <span className="text-slate-300">•</span>
          <span className="inline-flex items-center gap-1.5 text-emerald-700 font-medium">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
            Strict Domestic Uncapped Scope
          </span>
        </div>

        <div className="flex flex-col md:flex-row md:items-end justify-between gap-4">
          <div className="max-w-3xl space-y-2">
            <h1 className="text-3xl md:text-4xl font-extrabold tracking-tight text-slate-900 leading-tight">
              Uncapped Player Intelligence
            </h1>
            <p className="text-sm md:text-base text-slate-600 leading-relaxed font-normal">
              Targeted talent discovery for Indian domestic prospects with zero senior international caps.
              Ranked under empirical high-pressure scenarios (&gt;1.50 Required Run Rate, middle/death overs, run-chases)
              with Empirical Bayes shrinkage and 1-SE conservative credible bounds.
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-3 shrink-0">
            <Link
              href="/pressure"
              className="inline-flex items-center gap-1.5 px-4 py-2 rounded-lg bg-[#111C38] text-white text-xs font-semibold hover:bg-[#1A2B50] transition-colors shadow-sm"
            >
              <Shield size={14} className="text-[#E91E8C]" />
              <span>Official Global Top 10</span>
              <ArrowRight size={13} className="text-slate-400" />
            </Link>
            <Link
              href="/domestic"
              className="inline-flex items-center gap-1.5 px-4 py-2 rounded-lg bg-white border border-slate-200 text-slate-800 text-xs font-semibold hover:bg-slate-50 transition-colors shadow-sm"
            >
              <Sparkles size={14} className="text-[#D6B56D]" />
              <span>Domestic Match Dossiers</span>
            </Link>
          </div>
        </div>
      </section>

      {/* Connection Notice (if backend unreachable) */}
      {errorMsg && (
        <div className="p-4 rounded-xl bg-amber-50 border border-amber-200 text-amber-900 flex items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <AlertTriangle className="w-5 h-5 text-amber-600 shrink-0" />
            <div>
              <div className="text-xs font-bold">Backend Standby Notice</div>
              <div className="text-xs text-amber-800 mt-0.5">
                {errorMsg} Local high-fidelity domestic dataset active.
              </div>
            </div>
          </div>
          <button
            onClick={() => loadUncappedData(minBalls, minMatches)}
            className="px-3 py-1.5 rounded-lg bg-amber-600 text-white font-bold text-xs hover:bg-amber-700 transition-colors shrink-0 flex items-center gap-1.5"
          >
            <RefreshCw className="w-3.5 h-3.5" />
            <span>Retry</span>
          </button>
        </div>
      )}

      {/* ------------------------------------------------------------------- */}
      {/* 2. Open Editorial Telemetry Strip (No Heavy Boxes) */}
      {/* ------------------------------------------------------------------- */}
      <section className="py-5 border-y border-slate-200/80">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 md:gap-8">
          <div>
            <span className="text-[10px] font-mono uppercase tracking-wider text-slate-500 font-semibold block mb-1">
              Top Uncapped Batter
            </span>
            <div className="text-xl md:text-2xl font-extrabold text-[#111827] tracking-tight flex items-baseline gap-1.5">
              <span>{overview?.top_uncapped_batter ?? "Ashutosh Sharma"}</span>
              <span className="w-1.5 h-1.5 rounded-full bg-[#E91E8C]" />
            </div>
            <p className="text-xs text-slate-500 mt-0.5">
              Rank #1 Qualified • Conservative PRI
            </p>
          </div>

          <div>
            <span className="text-[10px] font-mono uppercase tracking-wider text-slate-500 font-semibold block mb-1">
              Top Uncapped Bowler
            </span>
            <div className="text-xl md:text-2xl font-extrabold text-[#111827] tracking-tight flex items-baseline gap-1.5">
              <span>{overview?.top_uncapped_bowler ?? "Vaibhav Arora"}</span>
              <span className="w-1.5 h-1.5 rounded-full bg-[#E91E8C]" />
            </div>
            <p className="text-xs text-slate-500 mt-0.5">
              Rank #1 Qualified • Runs Saved (1-SE)
            </p>
          </div>

          <div>
            <span className="text-[10px] font-mono uppercase tracking-wider text-slate-500 font-semibold block mb-1">
              Qualified Prospects
            </span>
            <div className="text-xl md:text-2xl font-extrabold text-[#111827] font-mono tracking-tight">
              {overview
                ? `${overview.total_verified_uncapped_batters} Bat / ${overview.total_verified_uncapped_bowlers} Bowl`
                : "14 Bat / 15 Bowl"}
            </div>
            <p className="text-xs text-slate-500 mt-0.5">
              {isExploratory
                ? `Exploratory: ≥${minBalls}b ${minMatches > 0 ? `& ≥${minMatches}m` : "(All matches)"}`
                : "Strict gate ≥ 60 pressure deliveries"}
            </p>
          </div>

          <div>
            <span className="text-[10px] font-mono uppercase tracking-wider text-slate-500 font-semibold block mb-1">
              Sample Excluded
            </span>
            <div className="text-xl md:text-2xl font-extrabold text-amber-700 font-mono tracking-tight">
              {overview?.excluded_batters_count !== undefined
                ? `${overview.excluded_batters_count} Bat / ${overview.excluded_bowlers_count} Bowl`
                : "16 Bat / 7 Bowl"}
            </div>
            <p className="text-xs text-slate-500 mt-0.5">
              {overview?.excluded_batters_count !== undefined
                ? `${overview.excluded_batters_count + (overview.excluded_bowlers_count ?? 0)} candidates below active gate`
                : "23 candidates below active gate"}
            </p>
          </div>
        </div>
      </section>

      {/* ------------------------------------------------------------------- */}
      {/* 3. Configurable Prospect Sample Gate & Qualification Filters */}
      {/* ------------------------------------------------------------------- */}
      <section className="bg-white rounded-2xl border border-slate-200/80 p-5 shadow-sm space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-100 pb-3">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-lg bg-pink-50 border border-pink-100 flex items-center justify-center text-[#E91E8C] shrink-0">
              <SlidersHorizontal className="w-4 h-4" />
            </div>
            <div>
              <h2 className="text-sm font-bold text-[#111C38] flex items-center gap-2">
                <span>Prospect Qualification Gate & Scouting Filters</span>
                <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-slate-100 text-slate-600 font-normal">
                  Configurable
                </span>
              </h2>
              <p className="text-xs text-slate-500 mt-0.5">
                Dynamically adjust empirical sample gates. Official Round 1 Benchmark (≥60 balls) remains the default standard.
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2 shrink-0 self-start sm:self-auto">
            {!isExploratory ? (
              <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-[11px] font-mono font-bold bg-emerald-50 text-emerald-700 border border-emerald-200">
                <Shield className="w-3.5 h-3.5 text-emerald-600" />
                <span>Official R1 Gate Active (Strict ≥ 60 Balls)</span>
              </span>
            ) : (
              <div className="flex items-center gap-2">
                <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-[11px] font-mono font-bold bg-pink-50 text-[#E91E8C] border border-pink-200">
                  <Sparkles className="w-3.5 h-3.5 text-[#E91E8C]" />
                  <span>Exploratory Scouting Filter Active</span>
                </span>
                <button
                  onClick={resetToOfficial}
                  className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg text-xs font-semibold text-slate-600 hover:text-slate-900 bg-slate-100 hover:bg-slate-200 transition-colors"
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
              <span className="font-mono text-[10px] uppercase tracking-wider text-slate-500 font-semibold flex items-center gap-1.5">
                <Crosshair className="w-3 h-3 text-[#E91E8C]" />
                <span>Minimum Pressure Deliveries</span>
              </span>
              <span className="font-mono font-bold text-slate-800 text-xs">
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
                        ? "bg-[#E91E8C] text-white font-bold shadow-sm"
                        : "bg-slate-100 text-slate-600 hover:bg-slate-200/80 font-medium"
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
              <span className="font-mono text-[10px] uppercase tracking-wider text-slate-500 font-semibold flex items-center gap-1.5">
                <Filter className="w-3 h-3 text-[#111C38]" />
                <span>Minimum Matches Played</span>
              </span>
              <span className="font-mono font-bold text-slate-800 text-xs">
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
                        ? "bg-[#111C38] text-white font-bold shadow-sm"
                        : "bg-slate-100 text-slate-600 hover:bg-slate-200/80 font-medium"
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
        <div className="pt-3 border-t border-slate-100 flex flex-wrap items-center justify-between gap-3 text-xs">
          <div className="flex flex-wrap items-center gap-4 text-slate-600 font-mono text-[11px]">
            <div>
              <span className="text-slate-400">Qualified Batters:</span>{" "}
              <span className="font-bold text-emerald-700">
                {leaderboards?.batting_count ?? overview?.total_verified_uncapped_batters ?? 0}
              </span>
            </div>
            <span className="text-slate-300">•</span>
            <div>
              <span className="text-slate-400">Qualified Bowlers:</span>{" "}
              <span className="font-bold text-cyan-700">
                {leaderboards?.bowling_count ?? overview?.total_verified_uncapped_bowlers ?? 0}
              </span>
            </div>
            <span className="text-slate-300">•</span>
            <div>
              <span className="text-slate-400">Excluded by Criteria:</span>{" "}
              <span className="font-bold text-amber-700">
                {overview?.excluded_batters_count !== undefined
                  ? `${overview.excluded_batters_count} Bat / ${overview.excluded_bowlers_count} Bowl (${(overview.excluded_batters_count || 0) + (overview.excluded_bowlers_count || 0)} total)`
                  : "16 Bat / 7 Bowl (23 total)"}
              </span>
            </div>
          </div>

          <div className="text-[11px] font-mono text-slate-500 flex items-center gap-1.5">
            <span className="w-1.5 h-1.5 rounded-full bg-[#E91E8C]" />
            <span>{overview?.sample_gate_applied ?? "Gate active"}</span>
          </div>
        </div>
      </section>

      {/* ------------------------------------------------------------------- */}
      {/* 4. Editorial Segmented Tab Navigation */}
      {/* ------------------------------------------------------------------- */}
      <div className="flex items-center gap-6 border-b border-slate-200">
        <button
          onClick={() => setActiveTab("batting")}
          className={cn(
            "flex items-center gap-2 py-3 text-xs font-semibold transition-all border-b-2 -mb-px whitespace-nowrap",
            activeTab === "batting"
              ? "border-[#E91E8C] text-[#E91E8C] font-bold"
              : "border-transparent text-slate-500 hover:text-slate-800"
          )}
        >
          <TrendingUp className="w-4 h-4 text-emerald-600" />
          <span>
            Top Uncapped Batters Under Pressure ({leaderboards?.batting_count ?? 0})
          </span>
        </button>

        <button
          onClick={() => setActiveTab("bowling")}
          className={cn(
            "flex items-center gap-2 py-3 text-xs font-semibold transition-all border-b-2 -mb-px whitespace-nowrap",
            activeTab === "bowling"
              ? "border-[#E91E8C] text-[#E91E8C] font-bold"
              : "border-transparent text-slate-500 hover:text-slate-800"
          )}
        >
          <Target className="w-4 h-4 text-cyan-600" />
          <span>
            Top Uncapped Bowlers Under Pressure ({leaderboards?.bowling_count ?? 0})
          </span>
        </button>

        <button
          onClick={() => setActiveTab("governance")}
          className={cn(
            "flex items-center gap-2 py-3 text-xs font-semibold transition-all border-b-2 -mb-px whitespace-nowrap",
            activeTab === "governance"
              ? "border-[#E91E8C] text-[#E91E8C] font-bold"
              : "border-transparent text-slate-500 hover:text-slate-800"
          )}
        >
          <FileText className="w-4 h-4 text-[#D6B56D]" />
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
              <h2 className="text-base font-bold text-slate-900">
                Verified Indian Uncapped Batters Under Pressure
              </h2>
              <p className="text-xs text-slate-500">
                Ranked strictly by Conservative PRI (1-SE Lower Credible Bound in Strike Rate points). Domestic Indian players with 0 senior international caps.
              </p>
            </div>
            <div className="flex items-center gap-2 self-start sm:self-auto">
              <span className="text-[11px] font-mono font-medium text-emerald-700 bg-emerald-50 px-2.5 py-1 rounded-full border border-emerald-200/60">
                {leaderboards?.batting_count ?? 0} Qualified Batters
              </span>
            </div>
          </div>

          <div className="bg-white rounded-2xl border border-slate-200/80 shadow-sm overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead className="bg-slate-50/80 text-slate-500 uppercase text-[10px] tracking-wider border-b border-slate-200/80 font-mono">
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
                      <td colSpan={10} className="px-6 py-12 text-center text-slate-400">
                        <div className="flex flex-col items-center justify-center gap-2">
                          <RefreshCw className="w-5 h-5 animate-spin text-emerald-600" />
                          <span className="text-xs">Loading uncapped batting intelligence...</span>
                        </div>
                      </td>
                    </tr>
                  ) : leaderboards?.batting_leaderboard && leaderboards.batting_leaderboard.length > 0 ? (
                    leaderboards.batting_leaderboard.map((batter) => {
                      const isTop1 = batter.uncapped_rank === 1;
                      const isTop3 = batter.uncapped_rank <= 3;
                      const isOfficial = batter.is_official_r1_qualified ?? (batter.pressure_legal_balls >= 60 || (batter.pressure_legal_balls >= 50 && batter.pressure_matches >= 10));
                      return (
                        <tr key={batter.player_id} className="hover:bg-slate-50/70 transition-colors">
                          <td className="px-4 py-3 font-sans text-slate-900">
                            <div className="flex items-center gap-2.5">
                              <span
                                className={cn(
                                  "w-6 h-6 rounded-full flex items-center justify-center text-[10px] font-mono font-bold shrink-0",
                                  isTop1
                                    ? "bg-[#D6B56D] text-[#111C38]"
                                    : isTop3
                                      ? "bg-slate-900 text-white"
                                      : "bg-slate-100 text-slate-600"
                                )}
                              >
                                {batter.uncapped_rank}
                              </span>
                              <div>
                                <div className="font-bold text-slate-900">{batter.player_name}</div>
                                <div className="text-[10px] font-mono text-slate-400">
                                  Overall R1 #{batter.overall_r1_rank} • ID: {batter.player_id}
                                </div>
                              </div>
                            </div>
                          </td>
                          <td className="px-4 py-3 font-sans text-slate-700">
                            <div className="font-semibold text-slate-900">{batter.franchise}</div>
                            <div className="text-[10px] text-slate-500 font-mono">{batter.tactical_role}</div>
                          </td>
                          <td className="px-4 py-3 text-right">
                            <span className="font-bold text-sm text-emerald-700 font-mono">
                              {batter.conservative_pri > 0
                                ? `+${batter.conservative_pri.toFixed(2)}`
                                : batter.conservative_pri.toFixed(2)}{" "}
                              <span className="text-[10px] font-normal text-slate-400">SR</span>
                            </span>
                          </td>
                          <td className="px-4 py-3 text-right text-slate-800 font-bold">
                            {batter.posterior_mean > 0
                              ? `+${batter.posterior_mean.toFixed(2)}`
                              : batter.posterior_mean.toFixed(2)}
                          </td>
                          <td className="px-4 py-3 text-right text-slate-500">
                            &plusmn;{batter.posterior_se.toFixed(2)}
                          </td>
                          <td className="px-4 py-3 text-right text-slate-500 text-[11px]">
                            [{batter.ci_95_lower.toFixed(1)}, +{batter.ci_95_upper.toFixed(1)}]
                          </td>
                          <td className="px-4 py-3 text-right text-slate-900 font-bold">
                            {batter.pressure_legal_balls}
                          </td>
                          <td className="px-4 py-3 text-right text-slate-900 font-bold">
                            {batter.observed_strike_rate.toFixed(1)}
                          </td>
                          <td className="px-4 py-3 text-center font-sans">
                            <div className="flex flex-col items-center gap-1">
                              <span
                                className={cn(
                                  "text-[10px] font-mono font-medium px-2 py-0.5 rounded-full border",
                                  isOfficial
                                    ? "bg-emerald-50 text-emerald-700 border-emerald-200/60"
                                    : "bg-pink-50 text-[#E91E8C] border-pink-200/60"
                                )}
                                title={
                                  isOfficial
                                    ? "Meets strict Official Round 1 gate (>=60 pressure balls)"
                                    : "Qualified under active exploratory scouting filter"
                                }
                              >
                                {isOfficial ? "VERIFIED • OFFICIAL" : "VERIFIED • EXPLORATORY"}
                              </span>
                              <span className="text-[9px] font-mono text-slate-400">
                                {batter.pressure_legal_balls}b / {batter.pressure_matches}m
                              </span>
                            </div>
                          </td>
                          <td className="px-4 py-3 text-center font-sans">
                            <button
                              onClick={() => openDossier(batter, "batting")}
                              className="px-2.5 py-1 rounded-md bg-slate-100 hover:bg-slate-200 text-slate-700 text-[11px] font-semibold transition-all inline-flex items-center gap-1"
                            >
                              <span>Dossier</span>
                              <ChevronRight className="w-3 h-3 text-slate-400" />
                            </button>
                          </td>
                        </tr>
                      );
                    })
                  ) : (
                    <tr>
                      <td colSpan={10} className="px-6 py-12 text-center text-slate-500">
                        <div className="flex flex-col items-center justify-center gap-2">
                          <AlertTriangle className="w-7 h-7 text-amber-500" />
                          <span className="font-semibold text-slate-800">
                            No Uncapped Batters Match Current Filter Criteria
                          </span>
                          <span className="text-xs text-slate-400 max-w-md">
                            Minimum requirements ({minBalls} Balls, {minMatches === 0 ? "All Matches" : `${minMatches} Matches`}) excluded all candidates.
                          </span>
                          <button
                            onClick={resetToOfficial}
                            className="mt-2 px-3 py-1.5 rounded-lg bg-[#111C38] text-white text-xs font-semibold hover:bg-[#1A2B50] transition-colors flex items-center gap-1.5"
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
              <h2 className="text-base font-bold text-slate-900">
                Verified Indian Uncapped Bowlers Under Pressure
              </h2>
              <p className="text-xs text-slate-500">
                Ranked strictly by Conservative Runs Saved per 6 balls (1-SE Lower Credible Bound in Economy). Crucial scouting insight since all official Top 10 bowlers are capped internationals.
              </p>
            </div>
            <div className="flex items-center gap-2 self-start sm:self-auto">
              <span className="text-[11px] font-mono font-medium text-cyan-700 bg-cyan-50 px-2.5 py-1 rounded-full border border-cyan-200/60">
                {leaderboards?.bowling_count ?? 0} Qualified Bowlers
              </span>
            </div>
          </div>

          <div className="bg-white rounded-2xl border border-slate-200/80 shadow-sm overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead className="bg-slate-50/80 text-slate-500 uppercase text-[10px] tracking-wider border-b border-slate-200/80 font-mono">
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
                      <td colSpan={10} className="px-6 py-12 text-center text-slate-400">
                        <div className="flex flex-col items-center justify-center gap-2">
                          <RefreshCw className="w-5 h-5 animate-spin text-cyan-600" />
                          <span className="text-xs">Loading uncapped bowling intelligence...</span>
                        </div>
                      </td>
                    </tr>
                  ) : leaderboards?.bowling_leaderboard && leaderboards.bowling_leaderboard.length > 0 ? (
                    leaderboards.bowling_leaderboard.map((bowler) => {
                      const isTop1 = bowler.uncapped_rank === 1;
                      const isTop3 = bowler.uncapped_rank <= 3;
                      const isOfficial = bowler.is_official_r1_qualified ?? (bowler.pressure_legal_balls >= 60 || (bowler.pressure_legal_balls >= 50 && bowler.pressure_matches >= 10));
                      return (
                        <tr key={bowler.player_id} className="hover:bg-slate-50/70 transition-colors">
                          <td className="px-4 py-3 font-sans text-slate-900">
                            <div className="flex items-center gap-2.5">
                              <span
                                className={cn(
                                  "w-6 h-6 rounded-full flex items-center justify-center text-[10px] font-mono font-bold shrink-0",
                                  isTop1
                                    ? "bg-[#D6B56D] text-[#111C38]"
                                    : isTop3
                                      ? "bg-slate-900 text-white"
                                      : "bg-slate-100 text-slate-600"
                                )}
                              >
                                {bowler.uncapped_rank}
                              </span>
                              <div>
                                <div className="font-bold text-slate-900">{bowler.player_name}</div>
                                <div className="text-[10px] font-mono text-slate-400">
                                  Overall R1 #{bowler.overall_r1_rank} • ID: {bowler.player_id}
                                </div>
                              </div>
                            </div>
                          </td>
                          <td className="px-4 py-3 font-sans text-slate-700">
                            <div className="font-semibold text-slate-900">{bowler.franchise}</div>
                            <div className="text-[10px] text-slate-500 font-mono">{bowler.tactical_role}</div>
                          </td>
                          <td className="px-4 py-3 text-right">
                            <span className="font-bold text-sm text-cyan-700 font-mono">
                              {bowler.conservative_runs_saved.toFixed(2)}{" "}
                              <span className="text-[10px] font-normal text-slate-400">RPO</span>
                            </span>
                          </td>
                          <td className="px-4 py-3 text-right text-slate-800 font-bold">
                            {bowler.posterior_mean > 0
                              ? `+${bowler.posterior_mean.toFixed(2)}`
                              : bowler.posterior_mean.toFixed(2)}
                          </td>
                          <td className="px-4 py-3 text-right text-slate-500">
                            &plusmn;{bowler.posterior_se.toFixed(2)}
                          </td>
                          <td className="px-4 py-3 text-right text-slate-500 text-[11px]">
                            [{bowler.ci_95_lower.toFixed(2)}, +{bowler.ci_95_upper.toFixed(2)}]
                          </td>
                          <td className="px-4 py-3 text-right text-slate-900 font-bold">
                            {bowler.pressure_legal_balls}
                          </td>
                          <td className="px-4 py-3 text-right text-slate-900 font-bold">
                            {bowler.observed_economy.toFixed(2)}
                          </td>
                          <td className="px-4 py-3 text-center font-sans">
                            <div className="flex flex-col items-center gap-1">
                              <span
                                className={cn(
                                  "text-[10px] font-mono font-medium px-2 py-0.5 rounded-full border",
                                  isOfficial
                                    ? "bg-emerald-50 text-emerald-700 border-emerald-200/60"
                                    : "bg-pink-50 text-[#E91E8C] border-pink-200/60"
                                )}
                                title={
                                  isOfficial
                                    ? "Meets strict Official Round 1 gate (>=60 pressure balls)"
                                    : "Qualified under active exploratory scouting filter"
                                }
                              >
                                {isOfficial ? "VERIFIED • OFFICIAL" : "VERIFIED • EXPLORATORY"}
                              </span>
                              <span className="text-[9px] font-mono text-slate-400">
                                {bowler.pressure_legal_balls}b / {bowler.pressure_matches}m
                              </span>
                            </div>
                          </td>
                          <td className="px-4 py-3 text-center font-sans">
                            <button
                              onClick={() => openDossier(bowler, "bowling")}
                              className="px-2.5 py-1 rounded-md bg-slate-100 hover:bg-slate-200 text-slate-700 text-[11px] font-semibold transition-all inline-flex items-center gap-1"
                            >
                              <span>Dossier</span>
                              <ChevronRight className="w-3 h-3 text-slate-400" />
                            </button>
                          </td>
                        </tr>
                      );
                    })
                  ) : (
                    <tr>
                      <td colSpan={10} className="px-6 py-12 text-center text-slate-500">
                        <div className="flex flex-col items-center justify-center gap-2">
                          <AlertTriangle className="w-7 h-7 text-amber-500" />
                          <span className="font-semibold text-slate-800">
                            No Uncapped Bowlers Match Current Filter Criteria
                          </span>
                          <span className="text-xs text-slate-400 max-w-md">
                            Minimum requirements ({minBalls} Balls, {minMatches === 0 ? "All Matches" : `${minMatches} Matches`}) excluded all candidates.
                          </span>
                          <button
                            onClick={resetToOfficial}
                            className="mt-2 px-3 py-1.5 rounded-lg bg-[#111C38] text-white text-xs font-semibold hover:bg-[#1A2B50] transition-colors flex items-center gap-1.5"
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
          <div className="bg-white rounded-2xl border border-slate-200/80 p-6 shadow-sm space-y-4">
            <div className="flex items-center gap-3 border-b border-slate-100 pb-4">
              <Shield className="w-5 h-5 text-purple-600" />
              <h2 className="text-lg font-bold text-slate-900">
                AUCTION-02 Domestic Eligibility Ledger & Protocols
              </h2>
            </div>
            <p className="text-sm text-slate-600 leading-relaxed max-w-3xl">
              To prevent misclassification and preserve auction compliance, all uncapped evaluations adhere to strict BCCI Player Regulations for the IPL 2025/2026 cycle. Retired international stars (e.g., MS Dhoni) and multi-format international capped players (e.g., Virat Kohli, Rohit Sharma, Jasprit Bumrah) are categorically quarantined from uncapped discovery pipelines.
            </p>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-2">
              <div className="p-4 rounded-xl bg-slate-50 border border-slate-200/70 space-y-2">
                <div className="flex items-center gap-2 text-xs font-bold text-slate-900 font-mono uppercase">
                  <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                  <span>Rule 1: International Cap Barrier</span>
                </div>
                <p className="text-xs text-slate-600 leading-relaxed">
                  Zero appearances in Senior Men&apos;s Tests, ODIs, or T20Is for India or any ICC Full Member nation. Any international appearance immediately revokes uncapped eligibility.
                </p>
              </div>

              <div className="p-4 rounded-xl bg-slate-50 border border-slate-200/70 space-y-2">
                <div className="flex items-center gap-2 text-xs font-bold text-slate-900 font-mono uppercase">
                  <AlertTriangle className="w-4 h-4 text-amber-600" />
                  <span>Rule 2: Retirement Exclusion</span>
                </div>
                <p className="text-xs text-slate-600 leading-relaxed">
                  The BCCI 5-year retirement clause (IPL Rule 4.3) is quarantined to administrative auction rosters and strictly excluded from primary talent discovery scouting models.
                </p>
              </div>

              <div className="p-4 rounded-xl bg-slate-50 border border-slate-200/70 space-y-2">
                <div className="flex items-center gap-2 text-xs font-bold text-slate-900 font-mono uppercase">
                  <Crosshair className="w-4 h-4 text-cyan-600" />
                  <span>Rule 3: Configurable Sample Gate</span>
                </div>
                <p className="text-xs text-slate-600 leading-relaxed">
                  Default strict benchmark requires &ge; 60 pressure deliveries (or &ge; 50 balls across &ge; 10 matches). Exploratory filters allow adjusting down to 20 balls for early scouting without corrupting official rankings.
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
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-in fade-in duration-200">
          <div className="bg-white rounded-2xl max-w-2xl w-full p-6 shadow-2xl border border-slate-200 space-y-6 max-h-[90vh] overflow-y-auto">
            {/* Header */}
            <div className="flex items-start justify-between border-b border-slate-100 pb-4">
              <div>
                <div className="flex items-center gap-2">
                  <h3 className="text-xl font-extrabold text-slate-900">{selectedPlayer.player_name}</h3>
                  <span className="text-xs font-mono font-bold text-[#E91E8C] px-2 py-0.5 rounded-full bg-pink-50 border border-pink-100">
                    Uncapped #{selectedPlayer.uncapped_rank}
                  </span>
                  <span
                    className={cn(
                      "text-[10px] font-mono px-2 py-0.5 rounded-full border",
                      selectedPlayer.is_official_r1_qualified
                        ? "bg-emerald-50 text-emerald-700 border-emerald-200"
                        : "bg-pink-50 text-[#E91E8C] border-pink-200"
                    )}
                  >
                    {selectedPlayer.is_official_r1_qualified ? "Official R1 Benchmark" : "Exploratory Qualified"}
                  </span>
                </div>
                <div className="text-xs text-slate-500 font-mono mt-1">
                  {selectedPlayer.franchise} • Tactical Role: {selectedPlayer.tactical_role}
                </div>
              </div>
              <button
                onClick={closeDossier}
                className="w-8 h-8 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-500 flex items-center justify-center transition-colors"
              >
                <X size={16} />
              </button>
            </div>

            {/* Audit Status Section */}
            <div className="p-4 rounded-xl bg-emerald-50/70 border border-emerald-200/80 space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-xs font-mono font-bold text-emerald-800 uppercase tracking-wider">
                  BCCI Eligibility Status
                </span>
                <span className="px-2.5 py-0.5 rounded-full text-xs font-mono font-bold bg-emerald-600 text-white">
                  {selectedPlayer.eligibility_status}
                </span>
              </div>
              <p className="text-xs text-slate-700 leading-relaxed">{selectedPlayer.eligibility_reason}</p>
              <div className="pt-2 border-t border-emerald-200/60 flex flex-wrap items-center justify-between text-[11px] font-mono text-slate-600">
                <span>Source: {selectedPlayer.verification_source}</span>
                <span>Verified: {selectedPlayer.verification_date}</span>
              </div>
            </div>

            {/* Performance Metrics Strip */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
              <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200/70">
                <div className="text-[10px] text-slate-500 font-mono uppercase">Pressure Balls</div>
                <div className="text-lg font-extrabold font-mono text-slate-900 mt-1">
                  {selectedPlayer.pressure_legal_balls}
                </div>
              </div>

              <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200/70">
                <div className="text-[10px] text-slate-500 font-mono uppercase">Pressure Matches</div>
                <div className="text-lg font-extrabold font-mono text-slate-900 mt-1">
                  {selectedPlayer.pressure_matches}
                </div>
              </div>

              <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200/70">
                <div className="text-[10px] text-slate-500 font-mono uppercase">
                  {selectedDiscipline === "batting" ? "Conservative PRI" : "Runs Saved"}
                </div>
                <div className="text-lg font-extrabold font-mono text-emerald-700 mt-1">
                  {selectedDiscipline === "batting"
                    ? `${(selectedPlayer as UncappedBattingItem).conservative_pri.toFixed(2)} SR`
                    : `${(selectedPlayer as UncappedBowlingItem).conservative_runs_saved.toFixed(2)} RPO`}
                </div>
              </div>

              <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200/70">
                <div className="text-[10px] text-slate-500 font-mono uppercase">Overall R1 Rank</div>
                <div className="text-lg font-extrabold font-mono text-[#111C38] mt-1">
                  #{selectedPlayer.overall_r1_rank}
                </div>
              </div>
            </div>

            <div className="p-4 rounded-xl bg-slate-50 border border-slate-200/70">
              <div className="text-xs font-bold text-slate-900 mb-1">Bayesian Reliability Summary</div>
              <p className="text-xs text-slate-600 leading-relaxed">
                Posterior Mean (&theta;) is {selectedPlayer.posterior_mean > 0 ? `+${selectedPlayer.posterior_mean.toFixed(2)}` : selectedPlayer.posterior_mean.toFixed(2)} with standard error &plusmn;{selectedPlayer.posterior_se.toFixed(2)}. The 95% Bayesian credible interval spans [{selectedPlayer.ci_95_lower.toFixed(1)}, +{selectedPlayer.ci_95_upper.toFixed(1)}], confirming statistically significant pressure reliability under the 1-SE conservative rule.
              </p>
            </div>

            <div className="flex justify-end pt-2">
              <button
                onClick={closeDossier}
                className="px-5 py-2 rounded-lg bg-[#111C38] hover:bg-[#1A2B50] text-xs font-semibold text-white transition-colors"
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
