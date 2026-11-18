"use client";

import React, { useState, useEffect, useMemo } from "react";
import Link from "next/link";
import {
  PressureOverviewResponse,
  PressureLeaderboardResponse,
  CandidateEvidenceProfileResponse,
  PressureMethodologyResponse,
  PressureLeaderboardBattingItem,
  PressureLeaderboardBowlingItem,
} from "@/types";
import {
  fetchPressureOverview,
  fetchPressureLeaderboards,
  fetchCandidateProfile,
  fetchPressureMethodology,
} from "@/lib/api";
import {
  Shield,
  TrendingUp,
  Target,
  Sparkles,
  ChevronRight,
  X,
  FileText,
  RefreshCw,
  Flame,
  Sliders,
  Crosshair,
  ArrowRight,
  AlertTriangle,
} from "lucide-react";
import { cn } from "@/lib/utils";

export default function PressureIntelligencePage() {
  const [activeTab, setActiveTab] = useState<"batting" | "bowling" | "methodology">("batting");
  const [loading, setLoading] = useState<boolean>(true);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  // Core Data
  const [overview, setOverview] = useState<PressureOverviewResponse | null>(null);
  const [leaderboards, setLeaderboards] = useState<PressureLeaderboardResponse | null>(null);
  const [methodology, setMethodology] = useState<PressureMethodologyResponse | null>(null);

  // Filter state
  const [competitionFilter, setCompetitionFilter] = useState<"all" | "ipl" | "t20i">("all");

  // Candidate Inspection Drawer
  const [selectedPlayerId, setSelectedPlayerId] = useState<number | null>(null);
  const [candidateProfile, setCandidateProfile] = useState<CandidateEvidenceProfileResponse | null>(null);
  const [candidateLoading, setCandidateLoading] = useState<boolean>(false);

  const loadPressureData = async () => {
    setLoading(true);
    setErrorMsg(null);
    try {
      const [ovRes, lbRes, methRes] = await Promise.all([
        fetchPressureOverview(),
        fetchPressureLeaderboards({ discipline: "all", limit: 25, qualified_only: true }),
        fetchPressureMethodology(),
      ]);

      if (ovRes) setOverview(ovRes);
      if (lbRes) setLeaderboards(lbRes);
      if (methRes) setMethodology(methRes);

      if (!ovRes && !lbRes) {
        setErrorMsg("Failed to communicate with Pressure Intelligence backend service. Ensure backend is running on port 8000.");
      }
    } catch (err: any) {
      setErrorMsg("Failed to fetch official pressure datasets from server.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadPressureData();

    if (typeof window !== "undefined") {
      const params = new URLSearchParams(window.location.search);
      const tab = params.get("tab") || params.get("discipline");
      if (tab === "bowling") setActiveTab("bowling");
      if (tab === "batting") setActiveTab("batting");
      if (tab === "methodology") setActiveTab("methodology");
    }
  }, []);

  // Filtered Leaderboard Views
  const filteredBatters = useMemo(() => {
    if (!leaderboards?.batting_leaderboard) return [];
    if (competitionFilter === "all") return leaderboards.batting_leaderboard.slice(0, 10);
    if (competitionFilter === "ipl") {
      return leaderboards.batting_leaderboard.filter(
        (b) => b.competition_qualification.includes("IPL") || (b.ipl_legal_balls && b.ipl_legal_balls >= 30)
      ).slice(0, 10);
    }
    return leaderboards.batting_leaderboard.filter(
      (b) => b.competition_qualification.includes("T20I") || (b.t20i_legal_balls && b.t20i_legal_balls >= 30)
    ).slice(0, 10);
  }, [leaderboards, competitionFilter]);

  const filteredBowlers = useMemo(() => {
    if (!leaderboards?.bowling_leaderboard) return [];
    if (competitionFilter === "all") return leaderboards.bowling_leaderboard.slice(0, 10);
    if (competitionFilter === "ipl") {
      return leaderboards.bowling_leaderboard.filter(
        (b) => b.competition_qualification.includes("IPL") || (b.ipl_legal_balls && b.ipl_legal_balls >= 30)
      ).slice(0, 10);
    }
    return leaderboards.bowling_leaderboard.filter(
      (b) => b.competition_qualification.includes("T20I") || (b.t20i_legal_balls && b.t20i_legal_balls >= 30)
    ).slice(0, 10);
  }, [leaderboards, competitionFilter]);

  const handleInspectCandidate = async (playerId: number, discipline: "batting" | "bowling") => {
    setSelectedPlayerId(playerId);
    setCandidateLoading(true);
    const profile = await fetchCandidateProfile(playerId, discipline);
    if (profile) {
      setCandidateProfile(profile);
    }
    setCandidateLoading(false);
  };

  const closeCandidateModal = () => {
    setSelectedPlayerId(null);
    setCandidateProfile(null);
  };

  return (
    <div className="space-y-8 pb-12">
      {/* ------------------------------------------------------------------- */}
      {/* 1. Editorial Header & Challenge Context */}
      {/* ------------------------------------------------------------------- */}
      <section className="space-y-3">
        <div className="flex flex-wrap items-center gap-3 text-xs">
          <span className="font-mono font-bold tracking-widest text-[#E91E8C] uppercase">
            Rajasthan Royals Analytics
          </span>
          <span className="text-slate-300">•</span>
          <span className="font-mono text-slate-500">
            SupeRR Selector Season 2 — Round 1 Deliverable
          </span>
          <span className="text-slate-300">•</span>
          <span className="inline-flex items-center gap-1.5 text-emerald-700 font-medium">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
            Empirical Bayes Engine
          </span>
        </div>

        <div className="flex flex-col md:flex-row md:items-end justify-between gap-4">
          <div className="max-w-3xl space-y-2">
            <h1 className="text-3xl md:text-4xl font-extrabold tracking-tight text-slate-900 leading-tight">
              Pressure Reliability & Ranking Engine
            </h1>
            <p className="text-sm md:text-base text-slate-600 leading-relaxed font-normal">
              Official Top 10 Batters and Top 10 Bowlers Under Pressure. Benchmarked against 12-cell
              non-pressure context strata, Empirical Bayes shrinkage, and 1-SE Conservative lower credible bounds.
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-3 shrink-0">
            <Link
              href="/uncapped"
              className="inline-flex items-center gap-1.5 px-4 py-2 rounded-lg bg-white border border-slate-200 text-slate-800 text-xs font-semibold hover:bg-slate-50 transition-colors shadow-sm"
            >
              <Sparkles size={14} className="text-emerald-600" />
              <span>Uncapped Scouting</span>
              <ArrowRight size={13} className="text-slate-400" />
            </Link>
            <Link
              href="/tactical"
              className="inline-flex items-center gap-1.5 px-4 py-2 rounded-lg bg-[#111C38] text-white text-xs font-semibold hover:bg-[#1A2B50] transition-colors shadow-sm"
            >
              <Crosshair size={14} className="text-[#D6B56D]" />
              <span>Tactical Analytics</span>
            </Link>
          </div>
        </div>
      </section>

      {/* Connection Notice */}
      {errorMsg && (
        <div className="p-4 rounded-xl bg-amber-50 border border-amber-200 text-amber-900 flex items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <AlertTriangle className="w-5 h-5 text-amber-600 shrink-0" />
            <div>
              <div className="text-xs font-bold">Backend Connection Notice</div>
              <div className="text-xs text-amber-800 mt-0.5">{errorMsg}</div>
            </div>
          </div>
          <button
            onClick={loadPressureData}
            className="px-3 py-1.5 rounded-lg bg-amber-600 text-white font-bold text-xs hover:bg-amber-700 transition-colors shrink-0 flex items-center gap-1.5"
          >
            <RefreshCw className="w-3.5 h-3.5" />
            <span>Retry</span>
          </button>
        </div>
      )}

      {/* ------------------------------------------------------------------- */}
      {/* 2. Open Editorial Telemetry Strip (No Card Boxes) */}
      {/* ------------------------------------------------------------------- */}
      <section className="py-5 border-y border-slate-200/70">
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6">
          <div>
            <span className="text-[11px] font-mono uppercase tracking-wider text-slate-400 block mb-1">
              Strict Pressure Balls
            </span>
            <div className="text-xl font-extrabold text-slate-900 font-mono tracking-tight">
              {overview ? overview.strict_pressure_bowling_balls.toLocaleString() : "37,014"}
            </div>
            <p className="text-xs text-slate-500 mt-0.5">
              31,163 Batting Pressure
            </p>
          </div>

          <div>
            <span className="text-[11px] font-mono uppercase tracking-wider text-slate-400 block mb-1">
              Death Concentration
            </span>
            <div className="text-xl font-extrabold text-slate-900 font-mono tracking-tight">
              {overview ? `${overview.death_overs_bowling_pressure_share_pct}%` : "87.3%"}
            </div>
            <p className="text-xs text-slate-500 mt-0.5">
              Overs 16–20 Pressure Share
            </p>
          </div>

          <div>
            <span className="text-[11px] font-mono uppercase tracking-wider text-slate-400 block mb-1">
              Candidate Scope
            </span>
            <div className="text-xl font-extrabold text-slate-900 font-mono tracking-tight">
              {overview ? `${overview.total_evaluated_batters} / ${overview.total_evaluated_bowlers}` : "278 / 239"}
            </div>
            <p className="text-xs text-slate-500 mt-0.5">
              Batters / Bowlers Evaluated
            </p>
          </div>

          <div>
            <span className="text-[11px] font-mono uppercase tracking-wider text-slate-400 block mb-1">
              Sample Size Gate
            </span>
            <div className="text-xl font-extrabold text-slate-900 font-mono tracking-tight">
              &ge; 60 Balls
            </div>
            <p className="text-xs text-slate-500 mt-0.5">
              Strict official qualification gate
            </p>
          </div>

          <div>
            <span className="text-[11px] font-mono uppercase tracking-wider text-slate-400 block mb-1">
              Baseline Strata
            </span>
            <div className="text-xl font-extrabold text-slate-900 font-mono tracking-tight">
              12 Cells
            </div>
            <p className="text-xs text-slate-500 mt-0.5">
              Phase &times; Tier &times; Innings
            </p>
          </div>

          <div>
            <span className="text-[11px] font-mono uppercase tracking-wider text-slate-400 block mb-1">
              Governing Metric
            </span>
            <div className="text-xl font-extrabold text-[#E91E8C] font-mono tracking-tight">
              1-SE Bound
            </div>
            <p className="text-xs text-slate-500 mt-0.5">
              Conservative PRI &minus; 1.0 SE
            </p>
          </div>
        </div>
      </section>

      {/* ------------------------------------------------------------------- */}
      {/* 3. Segmented Tab Navigation */}
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
          <span>Top 10 Batters Under Pressure</span>
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
          <span>Top 10 Bowlers Under Pressure</span>
        </button>

        <button
          onClick={() => setActiveTab("methodology")}
          className={cn(
            "flex items-center gap-2 py-3 text-xs font-semibold transition-all border-b-2 -mb-px whitespace-nowrap",
            activeTab === "methodology"
              ? "border-[#E91E8C] text-[#E91E8C] font-bold"
              : "border-transparent text-slate-500 hover:text-slate-800"
          )}
        >
          <FileText className="w-4 h-4 text-[#D6B56D]" />
          <span>Bayesian Methodology</span>
        </button>
      </div>

      {/* ------------------------------------------------------------------- */}
      {/* TAB 1: TOP 10 BATTERS UNDER PRESSURE */}
      {/* ------------------------------------------------------------------- */}
      {activeTab === "batting" && (
        <div className="space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div>
              <h2 className="text-base font-bold text-slate-900">
                Official Top 10 Batters Under Pressure (Unstop Dropdown Guide)
              </h2>
              <p className="text-xs text-slate-500">
                Ranked strictly by Conservative PRI (1-SE Lower Credible Bound in Strike Rate points).
              </p>
            </div>

            <div className="flex items-center gap-1 p-1 bg-slate-100 rounded-lg self-start sm:self-auto">
              <button
                onClick={() => setCompetitionFilter("all")}
                className={cn(
                  "px-2.5 py-1 rounded text-xs font-semibold transition-all",
                  competitionFilter === "all"
                    ? "bg-white text-slate-900 shadow-sm"
                    : "text-slate-500 hover:text-slate-700"
                )}
              >
                Combined
              </button>
              <button
                onClick={() => setCompetitionFilter("ipl")}
                className={cn(
                  "px-2.5 py-1 rounded text-xs font-semibold transition-all",
                  competitionFilter === "ipl"
                    ? "bg-white text-slate-900 shadow-sm"
                    : "text-slate-500 hover:text-slate-700"
                )}
              >
                IPL
              </button>
              <button
                onClick={() => setCompetitionFilter("t20i")}
                className={cn(
                  "px-2.5 py-1 rounded text-xs font-semibold transition-all",
                  competitionFilter === "t20i"
                    ? "bg-white text-slate-900 shadow-sm"
                    : "text-slate-500 hover:text-slate-700"
                )}
              >
                T20I
              </button>
            </div>
          </div>

          <div className="bg-white rounded-2xl border border-slate-200/80 shadow-sm overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead className="bg-slate-50/80 text-slate-500 uppercase text-[10px] tracking-wider border-b border-slate-200/80 font-mono">
                  <tr>
                    <th className="px-4 py-3 font-sans font-semibold">Rank & Batter</th>
                    <th className="px-4 py-3 text-right font-semibold">Conservative PRI</th>
                    <th className="px-4 py-3 text-right font-semibold">Posterior Mean (&theta;)</th>
                    <th className="px-4 py-3 text-right font-semibold">Uncertainty (SE)</th>
                    <th className="px-4 py-3 text-right font-semibold">95% Credible Region</th>
                    <th className="px-4 py-3 text-right font-semibold">Pressure Balls</th>
                    <th className="px-4 py-3 text-right font-semibold">Matches</th>
                    <th className="px-4 py-3 text-center font-sans font-semibold">Tournament</th>
                    <th className="px-4 py-3 text-center font-sans font-semibold">Evidence</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 font-mono">
                  {loading ? (
                    <tr>
                      <td colSpan={9} className="px-6 py-12 text-center text-slate-400">
                        <div className="flex flex-col items-center justify-center gap-2">
                          <RefreshCw className="w-5 h-5 animate-spin text-emerald-600" />
                          <span className="text-xs">Loading official batting leaderboard...</span>
                        </div>
                      </td>
                    </tr>
                  ) : filteredBatters.length > 0 ? (
                    filteredBatters.map((batter: PressureLeaderboardBattingItem) => {
                      const isTop1 = batter.rank === 1;
                      const isTop3 = batter.rank <= 3;
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
                                {batter.rank}
                              </span>
                              <div>
                                <div className="font-bold text-slate-900">{batter.player_name}</div>
                                <div className="text-[10px] font-mono text-slate-400">ID: {batter.player_id}</div>
                              </div>
                            </div>
                          </td>
                          <td className="px-4 py-3 text-right">
                            <span className="font-bold text-sm text-emerald-700 font-mono">
                              {batter.conservative_pri > 0 ? `+${batter.conservative_pri.toFixed(1)}` : batter.conservative_pri.toFixed(1)}{" "}
                              <span className="text-[10px] font-normal text-slate-400">SR pts</span>
                            </span>
                          </td>
                          <td className="px-4 py-3 text-right text-slate-800 font-bold">
                            +{batter.posterior_mean.toFixed(1)}
                          </td>
                          <td className="px-4 py-3 text-right text-slate-500">
                            &plusmn;{batter.posterior_se.toFixed(1)}
                          </td>
                          <td className="px-4 py-3 text-right text-slate-500 text-[11px]">
                            [{batter.ci_95_lower.toFixed(1)}, +{batter.ci_95_upper.toFixed(1)}]
                          </td>
                          <td className="px-4 py-3 text-right text-slate-900 font-bold">
                            {batter.pressure_legal_balls}
                          </td>
                          <td className="px-4 py-3 text-right text-slate-600">
                            {batter.pressure_matches}
                          </td>
                          <td className="px-4 py-3 text-center font-sans">
                            <span className="text-[10px] font-mono font-medium px-2 py-0.5 rounded-full bg-slate-100 text-slate-700">
                              {batter.competition_qualification.replace("_QUALIFIED", "")}
                            </span>
                          </td>
                          <td className="px-4 py-3 text-center font-sans">
                            <button
                              onClick={() => handleInspectCandidate(batter.player_id, "batting")}
                              className="px-2.5 py-1 rounded-md bg-slate-100 hover:bg-slate-200 text-slate-700 text-[11px] font-semibold transition-all inline-flex items-center gap-1"
                            >
                              <span>Q1–Q11</span>
                              <ChevronRight className="w-3 h-3 text-slate-400" />
                            </button>
                          </td>
                        </tr>
                      );
                    })
                  ) : (
                    <tr>
                      <td colSpan={9} className="px-6 py-12 text-center text-slate-500">
                        <div className="flex flex-col items-center justify-center gap-2">
                          <AlertTriangle className="w-7 h-7 text-amber-500" />
                          <span className="font-semibold text-slate-800">No Batting Data Available</span>
                          <span className="text-xs text-slate-400 max-w-md">
                            {errorMsg || "Ensure the backend service is running on http://localhost:8000"}
                          </span>
                          <button
                            onClick={loadPressureData}
                            className="mt-2 px-3 py-1.5 rounded-lg bg-[#111C38] text-white text-xs font-semibold hover:bg-[#1A2B50] transition-colors flex items-center gap-1.5"
                          >
                            <RefreshCw className="w-3.5 h-3.5" />
                            <span>Retry Request</span>
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
      {/* TAB 2: TOP 10 BOWLERS UNDER PRESSURE */}
      {/* ------------------------------------------------------------------- */}
      {activeTab === "bowling" && (
        <div className="space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div>
              <h2 className="text-base font-bold text-slate-900">
                Official Top 10 Bowlers Under Pressure (Unstop Dropdown Guide)
              </h2>
              <p className="text-xs text-slate-500">
                Ranked strictly by Conservative Runs Saved per 6 balls (1-SE Lower Credible Bound in Economy).
              </p>
            </div>

            <div className="flex items-center gap-1 p-1 bg-slate-100 rounded-lg self-start sm:self-auto">
              <button
                onClick={() => setCompetitionFilter("all")}
                className={cn(
                  "px-2.5 py-1 rounded text-xs font-semibold transition-all",
                  competitionFilter === "all"
                    ? "bg-white text-slate-900 shadow-sm"
                    : "text-slate-500 hover:text-slate-700"
                )}
              >
                Combined
              </button>
              <button
                onClick={() => setCompetitionFilter("ipl")}
                className={cn(
                  "px-2.5 py-1 rounded text-xs font-semibold transition-all",
                  competitionFilter === "ipl"
                    ? "bg-white text-slate-900 shadow-sm"
                    : "text-slate-500 hover:text-slate-700"
                )}
              >
                IPL
              </button>
              <button
                onClick={() => setCompetitionFilter("t20i")}
                className={cn(
                  "px-2.5 py-1 rounded text-xs font-semibold transition-all",
                  competitionFilter === "t20i"
                    ? "bg-white text-slate-900 shadow-sm"
                    : "text-slate-500 hover:text-slate-700"
                )}
              >
                T20I
              </button>
            </div>
          </div>

          <div className="bg-white rounded-2xl border border-slate-200/80 shadow-sm overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead className="bg-slate-50/80 text-slate-500 uppercase text-[10px] tracking-wider border-b border-slate-200/80 font-mono">
                  <tr>
                    <th className="px-4 py-3 font-sans font-semibold">Rank & Bowler</th>
                    <th className="px-4 py-3 text-right font-semibold">Conservative Runs Saved</th>
                    <th className="px-4 py-3 text-right font-semibold">Posterior Mean (&theta;)</th>
                    <th className="px-4 py-3 text-right font-semibold">Uncertainty (SE)</th>
                    <th className="px-4 py-3 text-right font-semibold">95% Credible Region</th>
                    <th className="px-4 py-3 text-right font-semibold">Pressure Balls</th>
                    <th className="px-4 py-3 text-right font-semibold">Matches</th>
                    <th className="px-4 py-3 text-center font-sans font-semibold">Tournament</th>
                    <th className="px-4 py-3 text-center font-sans font-semibold">Evidence</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 font-mono">
                  {loading ? (
                    <tr>
                      <td colSpan={9} className="px-6 py-12 text-center text-slate-400">
                        <div className="flex flex-col items-center justify-center gap-2">
                          <RefreshCw className="w-5 h-5 animate-spin text-cyan-600" />
                          <span className="text-xs">Loading official bowling leaderboard...</span>
                        </div>
                      </td>
                    </tr>
                  ) : filteredBowlers.length > 0 ? (
                    filteredBowlers.map((bowler: PressureLeaderboardBowlingItem) => {
                      const isTop1 = bowler.rank === 1;
                      const isTop3 = bowler.rank <= 3;
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
                                {bowler.rank}
                              </span>
                              <div>
                                <div className="font-bold text-slate-900">{bowler.player_name}</div>
                                <div className="text-[10px] font-mono text-slate-400">ID: {bowler.player_id}</div>
                              </div>
                            </div>
                          </td>
                          <td className="px-4 py-3 text-right">
                            <span className="font-bold text-sm text-cyan-700 font-mono">
                              {bowler.conservative_runs_saved.toFixed(2)}{" "}
                              <span className="text-[10px] font-normal text-slate-400">RPO</span>
                            </span>
                          </td>
                          <td className="px-4 py-3 text-right text-slate-800 font-bold">
                            {bowler.posterior_mean > 0 ? `+${bowler.posterior_mean.toFixed(2)}` : bowler.posterior_mean.toFixed(2)}
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
                          <td className="px-4 py-3 text-right text-slate-600">
                            {bowler.pressure_matches}
                          </td>
                          <td className="px-4 py-3 text-center font-sans">
                            <span className="text-[10px] font-mono font-medium px-2 py-0.5 rounded-full bg-slate-100 text-slate-700">
                              {bowler.competition_qualification.replace("_QUALIFIED", "")}
                            </span>
                          </td>
                          <td className="px-4 py-3 text-center font-sans">
                            <button
                              onClick={() => handleInspectCandidate(bowler.player_id, "bowling")}
                              className="px-2.5 py-1 rounded-md bg-slate-100 hover:bg-slate-200 text-slate-700 text-[11px] font-semibold transition-all inline-flex items-center gap-1"
                            >
                              <span>Q1–Q11</span>
                              <ChevronRight className="w-3 h-3 text-slate-400" />
                            </button>
                          </td>
                        </tr>
                      );
                    })
                  ) : (
                    <tr>
                      <td colSpan={9} className="px-6 py-12 text-center text-slate-500">
                        <div className="flex flex-col items-center justify-center gap-2">
                          <AlertTriangle className="w-7 h-7 text-amber-500" />
                          <span className="font-semibold text-slate-800">No Bowling Data Available</span>
                          <span className="text-xs text-slate-400 max-w-md">
                            {errorMsg || "Ensure the backend service is running on http://localhost:8000"}
                          </span>
                          <button
                            onClick={loadPressureData}
                            className="mt-2 px-3 py-1.5 rounded-lg bg-[#111C38] text-white text-xs font-semibold hover:bg-[#1A2B50] transition-colors flex items-center gap-1.5"
                          >
                            <RefreshCw className="w-3.5 h-3.5" />
                            <span>Retry Request</span>
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
      {/* TAB 3: METHODOLOGY & BASELINE STRATA */}
      {/* ------------------------------------------------------------------- */}
      {activeTab === "methodology" && methodology && (
        <div className="space-y-6">
          <div className="bg-white rounded-2xl border border-slate-200/80 p-6 md:p-8 shadow-sm space-y-6">
            <div>
              <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2 mb-2">
                <FileText className="w-5 h-5 text-[#D6B56D]" />
                Statistical Methodology & Reliability Framework
              </h2>
              <p className="text-sm text-slate-600 leading-relaxed max-w-3xl">
                Mathematical formulations, empirical Bayes shrinkage, and 12-cell baseline context stratification.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-4 border-t border-slate-100">
              {/* Pressure Situation Definition */}
              <div className="space-y-3">
                <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
                  <Flame className="w-4 h-4 text-rose-500" />
                  Dynamic Pressure Situation Definition
                </h3>
                <div className="text-xs text-slate-600 space-y-2 leading-relaxed">
                  <p>
                    <strong className="text-slate-900">Chasing (Innings 2):</strong> Required Run Rate &ge; 9.0 with balls remaining &le; 36, OR RRR &ge; 12.0 at any point, OR close finishes (balls &le; 18, runs &le; 36, wkts &le; 5).
                  </p>
                  <p>
                    <strong className="text-slate-900">Setting Target (Innings 1):</strong> Overs 16–20 where team has lost &ge; 4 wickets, OR overs 18–20 in any contested match.
                  </p>
                  <p className="text-emerald-700 font-mono text-[11px] font-medium">
                    Death Overs Concentration: 87.28% of bowling pressure and 78.95% of batting pressure occur in overs 16–20.
                  </p>
                </div>
              </div>

              {/* 12-Cell Context Stratified Baselines */}
              <div className="space-y-3">
                <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
                  <Sliders className="w-4 h-4 text-purple-600" />
                  12-Cell Context-Stratified Baselines
                </h3>
                <p className="text-xs text-slate-600 leading-relaxed">
                  To eliminate structural phase and venue biases, expected baselines are calculated across a 12-cell non-pressure matrix:
                </p>
                <div className="grid grid-cols-2 gap-2 font-mono text-[10px] text-slate-700">
                  {methodology.baseline_strata_12_cell.map((cell: string, idx: number) => (
                    <div key={idx} className="p-2 rounded-lg bg-slate-50 border border-slate-200/70 truncate">
                      {cell}
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Empirical Bayes Shrinkage */}
            <div className="pt-6 border-t border-slate-100 space-y-3">
              <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
                <Sparkles className="w-4 h-4 text-[#D6B56D]" />
                Hierarchical Empirical Bayes Shrinkage & Conservative PRI
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 font-mono text-xs">
                <div className="space-y-1.5 p-4 rounded-xl bg-slate-50 border border-slate-200/70">
                  <span className="text-slate-500 text-[11px] font-sans font-semibold">Prior & Shrinkage Weight</span>
                  <div className="text-slate-800">B_i = &sigma;_i&sup2; / (&sigma;_i&sup2; + &tau;&sup2;)</div>
                  <div className="text-slate-800">&theta;_hat_i = B_i &times; &mu;_0 + (1 &minus; B_i) &times; &Delta;_i</div>
                </div>
                <div className="space-y-1.5 p-4 rounded-xl bg-slate-50 border border-slate-200/70">
                  <span className="text-slate-500 text-[11px] font-sans font-semibold">Conservative Lower Bound (1-SE)</span>
                  <div className="text-emerald-700 font-bold">Batting: Conservative PRI = &theta;_hat_i &minus; 1.0 &times; SE_i</div>
                  <div className="text-cyan-700 font-bold">Bowling: Runs Saved = &minus;(&theta;_hat_i + 1.0 &times; SE_i)</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* ------------------------------------------------------------------- */}
      {/* CANDIDATE EVIDENCE PROFILE MODAL */}
      {/* ------------------------------------------------------------------- */}
      {selectedPlayerId && (
        <div className="fixed inset-0 bg-slate-900/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-white border border-slate-200 rounded-2xl max-w-3xl w-full max-h-[85vh] overflow-y-auto shadow-2xl p-6 md:p-8 space-y-6">
            {/* Modal Header */}
            <div className="flex items-center justify-between pb-4 border-b border-slate-100">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-slate-900 text-white flex items-center justify-center font-bold text-sm font-mono">
                  #{candidateProfile?.rank ?? "—"}
                </div>
                <div>
                  <h3 className="text-xl font-bold text-slate-900 flex items-center gap-2">
                    {candidateProfile?.player_name ?? "Loading Candidate..."}
                    <span className="text-xs font-mono text-slate-400">ID: {candidateProfile?.player_id}</span>
                  </h3>
                  <div className="flex items-center gap-2 mt-0.5">
                    <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded-full bg-slate-100 text-slate-700">
                      {candidateProfile?.discipline.toUpperCase()}
                    </span>
                    <span className="text-[10px] font-mono font-semibold px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200/60">
                      {candidateProfile?.competition_qualification}
                    </span>
                  </div>
                </div>
              </div>

              <button
                onClick={closeCandidateModal}
                className="p-1.5 rounded-lg text-slate-400 hover:text-slate-600 hover:bg-slate-100 transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Modal Body: Q1–Q11 Evidence Questions */}
            {candidateLoading ? (
              <div className="flex items-center justify-center py-12 text-slate-400 text-xs font-mono">
                <RefreshCw className="w-5 h-5 animate-spin text-[#E91E8C] mr-2" />
                Loading candidate evidence dossier...
              </div>
            ) : candidateProfile ? (
              <div className="space-y-4">
                {/* Stats Summary Strip */}
                <div className="grid grid-cols-2 md:grid-cols-4 gap-3 font-mono text-xs text-center">
                  <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200/70">
                    <span className="text-[10px] text-slate-400 uppercase block">Governing Bound</span>
                    <span className="text-base font-bold text-emerald-700">
                      {candidateProfile.governing_metric_value > 0 ? `+${candidateProfile.governing_metric_value.toFixed(2)}` : candidateProfile.governing_metric_value.toFixed(2)}
                    </span>
                  </div>
                  <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200/70">
                    <span className="text-[10px] text-slate-400 uppercase block">Posterior Mean (&theta;)</span>
                    <span className="text-base font-bold text-slate-900">
                      {candidateProfile.posterior_mean > 0 ? `+${candidateProfile.posterior_mean.toFixed(2)}` : candidateProfile.posterior_mean.toFixed(2)}
                    </span>
                  </div>
                  <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200/70">
                    <span className="text-[10px] text-slate-400 uppercase block">Uncertainty (SE)</span>
                    <span className="text-base font-bold text-slate-700">
                      &plusmn;{candidateProfile.posterior_se.toFixed(2)}
                    </span>
                  </div>
                  <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200/70">
                    <span className="text-[10px] text-slate-400 uppercase block">Pressure Balls</span>
                    <span className="text-base font-bold text-slate-900">
                      {candidateProfile.pressure_legal_balls} ({candidateProfile.pressure_matches} M)
                    </span>
                  </div>
                </div>

                {/* Evidence Q1 through Q11 */}
                <div className="space-y-3 pt-2">
                  <h4 className="text-xs font-mono font-bold text-slate-400 uppercase tracking-wider">
                    Official Methodology Evidence Dossier (Q1–Q11)
                  </h4>

                  <div className="space-y-2.5 text-xs">
                    <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200/70">
                      <span className="font-bold text-slate-900 block mb-1">Q1: Why is this candidate considered reliable?</span>
                      <p className="text-slate-600 leading-relaxed">{candidateProfile.evidence_questions.q1_why_considered}</p>
                    </div>

                    <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200/70">
                      <span className="font-bold text-slate-900 block mb-1">Q2: How many deliveries were evaluated under pressure?</span>
                      <p className="text-slate-600 leading-relaxed">{candidateProfile.evidence_questions.q2_pressure_deliveries}</p>
                    </div>

                    <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200/70">
                      <span className="font-bold text-slate-900 block mb-1">Q3: What match and season span is represented?</span>
                      <p className="text-slate-600 leading-relaxed">{candidateProfile.evidence_questions.q3_matches_and_seasons}</p>
                    </div>

                    <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200/70">
                      <span className="font-bold text-slate-900 block mb-1">Q4: Observed performance metrics under pressure:</span>
                      <p className="text-slate-600 leading-relaxed">{candidateProfile.evidence_questions.q4_observed_performance}</p>
                    </div>

                    <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200/70">
                      <span className="font-bold text-slate-900 block mb-1">Q5: Context-stratified expected baseline:</span>
                      <p className="text-slate-600 leading-relaxed">{candidateProfile.evidence_questions.q5_expected_performance}</p>
                    </div>

                    <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200/70">
                      <span className="font-bold text-slate-900 block mb-1">Q6: Conservative diagnostic bound:</span>
                      <p className="text-slate-600 leading-relaxed">{candidateProfile.evidence_questions.q6_conservative_diagnostic}</p>
                    </div>

                    <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200/70">
                      <span className="font-bold text-slate-900 block mb-1">Q7: Posterior uncertainty and shrinkage:</span>
                      <p className="text-slate-600 leading-relaxed">{candidateProfile.evidence_questions.q7_posterior_uncertainty}</p>
                    </div>

                    <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200/70">
                      <span className="font-bold text-slate-900 block mb-1">Q8: 95% Bayesian credible interval:</span>
                      <p className="text-slate-600 leading-relaxed">{candidateProfile.evidence_questions.q8_credible_interval}</p>
                    </div>

                    <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200/70">
                      <span className="font-bold text-slate-900 block mb-1">Q9: Tournament & competition cross-support:</span>
                      <p className="text-slate-600 leading-relaxed">{candidateProfile.evidence_questions.q9_competition_support}</p>
                    </div>

                    <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200/70">
                      <span className="font-bold text-slate-900 block mb-1">Q10: Major limitations and sample caveats:</span>
                      <p className="text-slate-600 leading-relaxed">{candidateProfile.evidence_questions.q10_major_limitations}</p>
                    </div>

                    <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200/70">
                      <span className="font-bold text-slate-900 block mb-1">Q11: Sensitivity to modeling assumptions:</span>
                      <p className="text-slate-600 leading-relaxed">{candidateProfile.evidence_questions.q11_sensitivity_to_assumptions}</p>
                    </div>
                  </div>
                </div>

                <div className="flex justify-end pt-2">
                  <button
                    onClick={closeCandidateModal}
                    className="px-5 py-2 rounded-lg bg-[#111C38] hover:bg-[#1A2B50] text-xs font-semibold text-white transition-colors"
                  >
                    Close Dossier
                  </button>
                </div>
              </div>
            ) : null}
          </div>
        </div>
      )}
    </div>
  );
}
