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
          <span className="font-mono font-bold tracking-widest text-[#17294B] uppercase px-2.5 py-1 rounded-md bg-[#E4005A]/10 border border-[#E4005A]/30">
            Rajasthan Royals Analytics
          </span>
          <span className="text-[#17294B]/30">•</span>
          <span className="font-mono text-[#52627A]">
            SupeRR Selector Season 2 — Round 1 Deliverable
          </span>
          <span className="text-[#17294B]/30">•</span>
          <span className="inline-flex items-center gap-1.5 text-[#E4005A] font-medium">
            <span className="w-1.5 h-1.5 rounded-full bg-[#E4005A]" />
            Empirical Bayes Engine
          </span>
        </div>

        <div className="space-y-2 max-w-4xl">
          <h1 className="text-3xl md:text-4xl font-extrabold tracking-tight text-[#E4005A] leading-tight font-heading">
            Pressure Reliability & Ranking Engine
          </h1>
          <p className="text-sm md:text-base text-[#52627A] leading-relaxed font-normal">
            Official Top 10 Batters and Top 10 Bowlers Under Pressure. Benchmarked against 12-cell
            non-pressure context strata, Empirical Bayes shrinkage, and 1-SE Conservative lower credible bounds.
          </p>
        </div>
      </section>

      {/* Connection Notice */}
      {errorMsg && (
        <div className="p-4 rounded-xl bg-[#E4005A]/10 border border-[#E4005A]/30 text-[#E4005A] flex items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <AlertTriangle className="w-5 h-5 text-[#E4005A] shrink-0" />
            <div>
              <div className="text-xs font-bold">Backend Connection Notice</div>
              <div className="text-xs text-[#E4005A] mt-0.5">{errorMsg}</div>
            </div>
          </div>
          <button
            onClick={loadPressureData}
            className="px-3 py-1.5 rounded-lg bg-[#E4005A] text-white font-bold text-xs hover:bg-[#950460] transition-colors shrink-0 flex items-center gap-1.5"
          >
            <RefreshCw className="w-3.5 h-3.5" />
            <span>Retry</span>
          </button>
        </div>
      )}

      {/* ------------------------------------------------------------------- */}
      {/* 2. Open Editorial Telemetry Strip (No Card Boxes) */}
      {/* ------------------------------------------------------------------- */}
      <section className="py-6 sm:py-7 border-y border-[#E7EAF0]">
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 sm:gap-6 lg:gap-5 xl:gap-6">
          <div>
            <span className="text-xs sm:text-[12.5px] font-mono font-bold uppercase tracking-wider text-[#52627A] block mb-1.5">
              Strict Pressure Balls
            </span>
            <div className="text-2xl sm:text-[26px] lg:text-[24px] xl:text-[28px] font-extrabold text-[#17294B] font-mono tracking-tight leading-tight my-1">
              {overview ? overview.strict_pressure_bowling_balls.toLocaleString() : "—"}
            </div>
            <p className="text-xs sm:text-[13px] text-[#52627A] mt-1 leading-snug">
              31,163 Batting Pressure
            </p>
          </div>

          <div>
            <span className="text-xs sm:text-[12.5px] font-mono font-bold uppercase tracking-wider text-[#52627A] block mb-1.5">
              Death Concentration
            </span>
            <div className="text-2xl sm:text-[26px] lg:text-[24px] xl:text-[28px] font-extrabold text-[#17294B] font-mono tracking-tight leading-tight my-1">
              {overview ? `${overview.death_overs_bowling_pressure_share_pct}%` : "—"}
            </div>
            <p className="text-xs sm:text-[13px] text-[#52627A] mt-1 leading-snug">
              Overs 16–20 Pressure Share
            </p>
          </div>

          <div>
            <span className="text-xs sm:text-[12.5px] font-mono font-bold uppercase tracking-wider text-[#52627A] block mb-1.5">
              Candidate Scope
            </span>
            <div className="text-2xl sm:text-[26px] lg:text-[24px] xl:text-[28px] font-extrabold text-[#17294B] font-mono tracking-tight leading-tight my-1">
              {overview ? `${overview.total_evaluated_batters} / ${overview.total_evaluated_bowlers}` : "—"}
            </div>
            <p className="text-xs sm:text-[13px] text-[#52627A] mt-1 leading-snug">
              Batters / Bowlers Evaluated
            </p>
          </div>

          <div>
            <span className="text-xs sm:text-[12.5px] font-mono font-bold uppercase tracking-wider text-[#52627A] block mb-1.5">
              Sample Size Gate
            </span>
            <div className="text-2xl sm:text-[26px] lg:text-[24px] xl:text-[28px] font-extrabold text-[#17294B] font-mono tracking-tight leading-tight my-1">
              &ge; 60 Balls
            </div>
            <p className="text-xs sm:text-[13px] text-[#52627A] mt-1 leading-snug">
              Strict official qualification gate
            </p>
          </div>

          <div>
            <span className="text-xs sm:text-[12.5px] font-mono font-bold uppercase tracking-wider text-[#52627A] block mb-1.5">
              Baseline Strata
            </span>
            <div className="text-2xl sm:text-[26px] lg:text-[24px] xl:text-[28px] font-extrabold text-[#17294B] font-mono tracking-tight leading-tight my-1">
              12 Cells
            </div>
            <p className="text-xs sm:text-[13px] text-[#52627A] mt-1 leading-snug">
              Phase &times; Tier &times; Innings
            </p>
          </div>

          <div>
            <span className="text-xs sm:text-[12.5px] font-mono font-bold uppercase tracking-wider text-[#52627A] block mb-1.5">
              Governing Metric
            </span>
            <div className="text-2xl sm:text-[26px] lg:text-[24px] xl:text-[28px] font-extrabold text-[#17294B] font-mono tracking-tight leading-tight my-1">
              1-SE Bound
            </div>
            <p className="text-xs sm:text-[13px] text-[#52627A] mt-1 leading-snug">
              Conservative PRI &minus; 1.0 SE
            </p>
          </div>
        </div>
      </section>

      {/* ------------------------------------------------------------------- */}
      {/* 3. Segmented Tab Navigation */}
      {/* ------------------------------------------------------------------- */}
      <div className="flex items-center gap-6 border-b border-[#E7EAF0]">
        <button
          onClick={() => setActiveTab("batting")}
          className={cn(
            "flex items-center gap-2 py-3 text-xs font-semibold transition-all border-b-2 -mb-px whitespace-nowrap",
            activeTab === "batting"
              ? "border-[#E4005A] text-[#E4005A] font-bold"
              : "border-transparent text-[#52627A] hover:text-[#17294B]"
          )}
        >
          <TrendingUp className={cn("w-4 h-4", activeTab === "batting" ? "text-[#E4005A]" : "text-[#52627A]")} />
          <span>Top 10 Batters Under Pressure</span>
        </button>

        <button
          onClick={() => setActiveTab("bowling")}
          className={cn(
            "flex items-center gap-2 py-3 text-xs font-semibold transition-all border-b-2 -mb-px whitespace-nowrap",
            activeTab === "bowling"
              ? "border-[#E4005A] text-[#E4005A] font-bold"
              : "border-transparent text-[#52627A] hover:text-[#17294B]"
          )}
        >
          <Target className={cn("w-4 h-4", activeTab === "bowling" ? "text-[#E4005A]" : "text-[#52627A]")} />
          <span>Top 10 Bowlers Under Pressure</span>
        </button>

        <button
          onClick={() => setActiveTab("methodology")}
          className={cn(
            "flex items-center gap-2 py-3 text-xs font-semibold transition-all border-b-2 -mb-px whitespace-nowrap",
            activeTab === "methodology"
              ? "border-[#E4005A] text-[#E4005A] font-bold"
              : "border-transparent text-[#52627A] hover:text-[#17294B]"
          )}
        >
          <FileText className={cn("w-4 h-4", activeTab === "methodology" ? "text-[#E4005A]" : "text-[#52627A]")} />
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
              <h2 className="text-base font-bold text-[#17294B]">
                Official Top 10 Batters Under Pressure (Unstop Dropdown Guide)
              </h2>
              <p className="text-xs text-[#52627A]">
                Ranked strictly by Conservative PRI (1-SE Lower Credible Bound in Strike Rate points).
              </p>
            </div>

            <div className="flex items-center gap-1 p-1 bg-[#FCE8F0] rounded-lg self-start sm:self-auto">
              <button
                onClick={() => setCompetitionFilter("all")}
                className={cn(
                  "px-2.5 py-1 rounded text-xs font-semibold transition-all",
                  competitionFilter === "all"
                    ? "bg-white text-[#17294B] shadow-sm"
                    : "text-[#52627A] hover:text-[#17294B]"
                )}
              >
                Combined
              </button>
              <button
                onClick={() => setCompetitionFilter("ipl")}
                className={cn(
                  "px-2.5 py-1 rounded text-xs font-semibold transition-all",
                  competitionFilter === "ipl"
                    ? "bg-white text-[#17294B] shadow-sm"
                    : "text-[#52627A] hover:text-[#17294B]"
                )}
              >
                IPL
              </button>
              <button
                onClick={() => setCompetitionFilter("t20i")}
                className={cn(
                  "px-2.5 py-1 rounded text-xs font-semibold transition-all",
                  competitionFilter === "t20i"
                    ? "bg-white text-[#17294B] shadow-sm"
                    : "text-[#52627A] hover:text-[#17294B]"
                )}
              >
                T20I
              </button>
            </div>
          </div>

          <div className="bg-white rounded-2xl border border-[#E7EAF0] shadow-sm overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead className="bg-white/80 text-[#52627A] uppercase text-[10px] tracking-wider border-b border-[#E7EAF0] font-mono">
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
                      <td colSpan={9} className="px-6 py-12 text-center text-[#52627A]">
                        <div className="flex flex-col items-center justify-center gap-2">
                          <RefreshCw className="w-5 h-5 animate-spin text-[#E4005A]" />
                          <span className="text-xs">Loading official batting leaderboard...</span>
                        </div>
                      </td>
                    </tr>
                  ) : filteredBatters.length > 0 ? (
                    filteredBatters.map((batter: PressureLeaderboardBattingItem, idx: number) => {
                      const isTop1 = batter.rank === 1;
                      const isTop3 = batter.rank <= 3;
                      return (
                        <tr
                          key={batter.player_id}
                          className={cn(
                            "transition-colors",
                            idx % 2 === 0 ? "bg-[#FCE8F0]/35" : "bg-white",
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
                                {batter.rank}
                              </span>
                              <div>
                                <div className="font-bold text-[#17294B]">{batter.player_name}</div>
                                <div className="text-[10px] font-mono text-[#74658F]">ID: {batter.player_id}</div>
                              </div>
                            </div>
                          </td>
                          <td className="px-4 py-3 text-right">
                            <span className="font-bold text-sm text-[#E4005A] font-mono">
                              {batter.conservative_pri > 0 ? `+${batter.conservative_pri.toFixed(1)}` : batter.conservative_pri.toFixed(1)}{" "}
                              <span className="text-[10px] font-normal text-[#74658F]">SR pts</span>
                            </span>
                          </td>
                          <td className="px-4 py-3 text-right text-[#E4005A] font-bold">
                            +{batter.posterior_mean.toFixed(1)}
                          </td>
                          <td className="px-4 py-3 text-right text-[#74658F]">
                            &plusmn;{batter.posterior_se.toFixed(1)}
                          </td>
                          <td className="px-4 py-3 text-right text-[#74658F] text-[11px]">
                            [{batter.ci_95_lower.toFixed(1)}, +{batter.ci_95_upper.toFixed(1)}]
                          </td>
                          <td className="px-4 py-3 text-right text-[#E4005A] font-bold">
                            {batter.pressure_legal_balls}
                          </td>
                          <td className="px-4 py-3 text-right text-[#74658F]">
                            {batter.pressure_matches}
                          </td>
                          <td className="px-4 py-3 text-center font-sans">
                            <span className="text-[11px] font-mono font-bold text-[#E4005A] tracking-tight">
                              {batter.competition_qualification.replace("_QUALIFIED", "")}
                            </span>
                          </td>
                          <td className="px-4 py-3 text-center font-sans">
                            <button
                              onClick={() => handleInspectCandidate(batter.player_id, "batting")}
                              className="px-2.5 py-1 rounded-md bg-[#FCE8F0] hover:bg-[#FCE8F0] text-[#17294B] text-[11px] font-semibold transition-all inline-flex items-center gap-1"
                            >
                              <span>Q1–Q11</span>
                              <ChevronRight className="w-3 h-3 text-[#52627A]" />
                            </button>
                          </td>
                        </tr>
                      );
                    })
                  ) : (
                    <tr>
                      <td colSpan={9} className="px-6 py-12 text-center text-[#52627A]">
                        <div className="flex flex-col items-center justify-center gap-2">
                          <AlertTriangle className="w-7 h-7 text-[#E4005A]" />
                          <span className="font-semibold text-[#17294B]">No Batting Data Available</span>
                          <span className="text-xs text-[#52627A] max-w-md">
                            {errorMsg || "Ensure the backend service is running on http://localhost:8000"}
                          </span>
                          <button
                            onClick={loadPressureData}
                            className="mt-2 px-3 py-1.5 rounded-lg bg-[#17294B] text-white text-xs font-semibold hover:bg-[#17294B] transition-colors flex items-center gap-1.5"
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
              <h2 className="text-base font-bold text-[#17294B]">
                Official Top 10 Bowlers Under Pressure (Unstop Dropdown Guide)
              </h2>
              <p className="text-xs text-[#52627A]">
                Ranked strictly by Conservative Runs Saved per 6 balls (1-SE Lower Credible Bound in Economy).
              </p>
            </div>

            <div className="flex items-center gap-1 p-1 bg-[#FCE8F0] rounded-lg self-start sm:self-auto">
              <button
                onClick={() => setCompetitionFilter("all")}
                className={cn(
                  "px-2.5 py-1 rounded text-xs font-semibold transition-all",
                  competitionFilter === "all"
                    ? "bg-white text-[#17294B] shadow-sm"
                    : "text-[#52627A] hover:text-[#17294B]"
                )}
              >
                Combined
              </button>
              <button
                onClick={() => setCompetitionFilter("ipl")}
                className={cn(
                  "px-2.5 py-1 rounded text-xs font-semibold transition-all",
                  competitionFilter === "ipl"
                    ? "bg-white text-[#17294B] shadow-sm"
                    : "text-[#52627A] hover:text-[#17294B]"
                )}
              >
                IPL
              </button>
              <button
                onClick={() => setCompetitionFilter("t20i")}
                className={cn(
                  "px-2.5 py-1 rounded text-xs font-semibold transition-all",
                  competitionFilter === "t20i"
                    ? "bg-white text-[#17294B] shadow-sm"
                    : "text-[#52627A] hover:text-[#17294B]"
                )}
              >
                T20I
              </button>
            </div>
          </div>

          <div className="bg-white rounded-2xl border border-[#E7EAF0] shadow-sm overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead className="bg-white/80 text-[#52627A] uppercase text-[10px] tracking-wider border-b border-[#E7EAF0] font-mono">
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
                      <td colSpan={9} className="px-6 py-12 text-center text-[#52627A]">
                        <div className="flex flex-col items-center justify-center gap-2">
                          <RefreshCw className="w-5 h-5 animate-spin text-[#17294B]" />
                          <span className="text-xs">Loading official bowling leaderboard...</span>
                        </div>
                      </td>
                    </tr>
                  ) : filteredBowlers.length > 0 ? (
                    filteredBowlers.map((bowler: PressureLeaderboardBowlingItem, idx: number) => {
                      const isTop1 = bowler.rank === 1;
                      const isTop3 = bowler.rank <= 3;
                      return (
                        <tr
                          key={bowler.player_id}
                          className={cn(
                            "transition-colors",
                            idx % 2 === 0 ? "bg-[#FCE8F0]/35" : "bg-white",
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
                                {bowler.rank}
                              </span>
                              <div>
                                <div className="font-bold text-[#17294B]">{bowler.player_name}</div>
                                <div className="text-[10px] font-mono text-[#74658F]">ID: {bowler.player_id}</div>
                              </div>
                            </div>
                          </td>
                          <td className="px-4 py-3 text-right">
                            <span className="font-bold text-sm text-[#E4005A] font-mono">
                              {bowler.conservative_runs_saved.toFixed(2)}{" "}
                              <span className="text-[10px] font-normal text-[#74658F]">RPO</span>
                            </span>
                          </td>
                          <td className="px-4 py-3 text-right text-[#E4005A] font-bold">
                            {bowler.posterior_mean > 0 ? `+${bowler.posterior_mean.toFixed(2)}` : bowler.posterior_mean.toFixed(2)}
                          </td>
                          <td className="px-4 py-3 text-right text-[#74658F]">
                            &plusmn;{bowler.posterior_se.toFixed(2)}
                          </td>
                          <td className="px-4 py-3 text-right text-[#74658F] text-[11px]">
                            [{bowler.ci_95_lower.toFixed(2)}, +{bowler.ci_95_upper.toFixed(2)}]
                          </td>
                          <td className="px-4 py-3 text-right text-[#E4005A] font-bold">
                            {bowler.pressure_legal_balls}
                          </td>
                          <td className="px-4 py-3 text-right text-[#74658F]">
                            {bowler.pressure_matches}
                          </td>
                          <td className="px-4 py-3 text-center font-sans">
                            <span className="text-[11px] font-mono font-bold text-[#E4005A] tracking-tight">
                              {bowler.competition_qualification.replace("_QUALIFIED", "")}
                            </span>
                          </td>
                          <td className="px-4 py-3 text-center font-sans">
                            <button
                              onClick={() => handleInspectCandidate(bowler.player_id, "bowling")}
                              className="px-2.5 py-1 rounded-md bg-[#FCE8F0] hover:bg-[#FCE8F0] text-[#17294B] text-[11px] font-semibold transition-all inline-flex items-center gap-1"
                            >
                              <span>Q1–Q11</span>
                              <ChevronRight className="w-3 h-3 text-[#52627A]" />
                            </button>
                          </td>
                        </tr>
                      );
                    })
                  ) : (
                    <tr>
                      <td colSpan={9} className="px-6 py-12 text-center text-[#52627A]">
                        <div className="flex flex-col items-center justify-center gap-2">
                          <AlertTriangle className="w-7 h-7 text-[#E4005A]" />
                          <span className="font-semibold text-[#17294B]">No Bowling Data Available</span>
                          <span className="text-xs text-[#52627A] max-w-md">
                            {errorMsg || "Ensure the backend service is running on http://localhost:8000"}
                          </span>
                          <button
                            onClick={loadPressureData}
                            className="mt-2 px-3 py-1.5 rounded-lg bg-[#17294B] text-white text-xs font-semibold hover:bg-[#17294B] transition-colors flex items-center gap-1.5"
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
          <div className="bg-white rounded-2xl border border-[#E7EAF0] p-6 md:p-8 shadow-sm space-y-6">
            <div>
              <h2 className="text-lg font-bold text-[#17294B] flex items-center gap-2 mb-2 font-heading">
                <FileText className="w-5 h-5 text-[#E4005A]" />
                Statistical Methodology & Reliability Framework
              </h2>
              <p className="text-sm text-[#52627A] leading-relaxed max-w-3xl">
                Mathematical formulations, empirical Bayes shrinkage, and 12-cell baseline context stratification.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-4 border-t border-[#E7EAF0]">
              {/* Pressure Situation Definition */}
              <div className="space-y-3">
                <h3 className="text-sm font-bold text-[#17294B] flex items-center gap-2">
                  <Flame className="w-4 h-4 text-[#E4005A]" />
                  Dynamic Pressure Situation Definition
                </h3>
                <div className="text-xs text-[#52627A] space-y-2 leading-relaxed">
                  <p>
                    <strong className="text-[#17294B]">Chasing (Innings 2):</strong> Required Run Rate &ge; 9.0 with balls remaining &le; 36, OR RRR &ge; 12.0 at any point, OR close finishes (balls &le; 18, runs &le; 36, wkts &le; 5).
                  </p>
                  <p>
                    <strong className="text-[#17294B]">Setting Target (Innings 1):</strong> Overs 16–20 where team has lost &ge; 4 wickets, OR overs 18–20 in any contested match.
                  </p>
                  <p className="text-[#E4005A] font-mono text-[11px] font-medium">
                    Death Overs Concentration: 87.28% of bowling pressure and 78.95% of batting pressure occur in overs 16–20.
                  </p>
                </div>
              </div>

              {/* 12-Cell Context Stratified Baselines */}
              <div className="space-y-3">
                <h3 className="text-sm font-bold text-[#17294B] flex items-center gap-2">
                  <Sliders className="w-4 h-4 text-[#E4005A]" />
                  12-Cell Context-Stratified Baselines
                </h3>
                <p className="text-xs text-[#52627A] leading-relaxed">
                  To eliminate structural phase and venue biases, expected baselines are calculated across a 12-cell non-pressure matrix:
                </p>
                <div className="grid grid-cols-2 gap-2 font-mono text-[10px] text-[#17294B]">
                  {methodology.baseline_strata_12_cell.map((cell: string, idx: number) => (
                    <div key={idx} className="p-2 rounded-lg bg-white border border-[#E7EAF0] truncate">
                      {cell}
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Empirical Bayes Shrinkage */}
            <div className="pt-6 border-t border-[#E7EAF0] space-y-3">
              <h3 className="text-sm font-bold text-[#17294B] flex items-center gap-2">
                <Sparkles className="w-4 h-4 text-[#E4005A]" />
                Hierarchical Empirical Bayes Shrinkage & Conservative PRI
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 font-mono text-xs">
                <div className="space-y-1.5 p-4 rounded-xl bg-white border border-[#E7EAF0]">
                  <span className="text-[#52627A] text-[11px] font-sans font-semibold">Prior & Shrinkage Weight</span>
                  <div className="text-[#17294B]">B_i = &sigma;_i&sup2; / (&sigma;_i&sup2; + &tau;&sup2;)</div>
                  <div className="text-[#17294B]">&theta;_hat_i = B_i &times; &mu;_0 + (1 &minus; B_i) &times; &Delta;_i</div>
                </div>
                <div className="space-y-1.5 p-4 rounded-xl bg-white border border-[#E7EAF0]">
                  <span className="text-[#52627A] text-[11px] font-sans font-semibold">Conservative Lower Bound (1-SE)</span>
                  <div className="text-[#E4005A] font-bold">Batting: Conservative PRI = &theta;_hat_i &minus; 1.0 &times; SE_i</div>
                  <div className="text-[#17294B] font-bold">Bowling: Runs Saved = &minus;(&theta;_hat_i + 1.0 &times; SE_i)</div>
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
        <div className="fixed inset-0 bg-[#17294B]/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-white border border-[#E7EAF0] rounded-2xl max-w-3xl w-full max-h-[85vh] overflow-y-auto shadow-2xl p-6 md:p-8 space-y-6">
            {/* Modal Header */}
            <div className="flex items-center justify-between pb-4 border-b border-[#E7EAF0]">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-[#17294B] text-white flex items-center justify-center font-bold text-sm font-mono">
                  #{candidateProfile?.rank ?? "—"}
                </div>
                <div>
                  <h3 className="text-xl font-bold text-[#17294B] flex items-center gap-2">
                    {candidateProfile?.player_name ?? "Loading Candidate..."}
                    <span className="text-xs font-mono text-[#52627A]">ID: {candidateProfile?.player_id}</span>
                  </h3>
                  <div className="flex items-center gap-2 mt-0.5">
                    <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded-full bg-[#FCE8F0] text-[#17294B]">
                      {candidateProfile?.discipline.toUpperCase()}
                    </span>
                    <span className="text-[10px] font-mono font-semibold px-2 py-0.5 rounded-full bg-[#E4005A]/10 text-[#E4005A] border border-[#E4005A]/30/60">
                      {candidateProfile?.competition_qualification}
                    </span>
                  </div>
                </div>
              </div>

              <button
                onClick={closeCandidateModal}
                className="p-1.5 rounded-lg text-[#52627A] hover:text-[#52627A] hover:bg-[#FCE8F0] transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Modal Body: Q1–Q11 Evidence Questions */}
            {candidateLoading ? (
              <div className="flex items-center justify-center py-12 text-[#52627A] text-xs font-mono">
                <RefreshCw className="w-5 h-5 animate-spin text-[#17294B] mr-2" />
                Loading candidate evidence dossier...
              </div>
            ) : candidateProfile ? (
              <div className="space-y-4">
                {/* Stats Summary Strip */}
                <div className="grid grid-cols-2 md:grid-cols-4 gap-3 font-mono text-xs text-center">
                  <div className="p-3.5 rounded-xl bg-white border border-[#E7EAF0]">
                    <span className="text-[10px] text-[#52627A] uppercase block">Governing Bound</span>
                    <span className="text-base font-bold text-[#E4005A]">
                      {candidateProfile.governing_metric_value > 0 ? `+${candidateProfile.governing_metric_value.toFixed(2)}` : candidateProfile.governing_metric_value.toFixed(2)}
                    </span>
                  </div>
                  <div className="p-3.5 rounded-xl bg-white border border-[#E7EAF0]">
                    <span className="text-[10px] text-[#52627A] uppercase block">Posterior Mean (&theta;)</span>
                    <span className="text-base font-bold text-[#17294B]">
                      {candidateProfile.posterior_mean > 0 ? `+${candidateProfile.posterior_mean.toFixed(2)}` : candidateProfile.posterior_mean.toFixed(2)}
                    </span>
                  </div>
                  <div className="p-3.5 rounded-xl bg-white border border-[#E7EAF0]">
                    <span className="text-[10px] text-[#52627A] uppercase block">Uncertainty (SE)</span>
                    <span className="text-base font-bold text-[#17294B]">
                      &plusmn;{candidateProfile.posterior_se.toFixed(2)}
                    </span>
                  </div>
                  <div className="p-3.5 rounded-xl bg-white border border-[#E7EAF0]">
                    <span className="text-[10px] text-[#52627A] uppercase block">Pressure Balls</span>
                    <span className="text-base font-bold text-[#17294B]">
                      {candidateProfile.pressure_legal_balls} ({candidateProfile.pressure_matches} M)
                    </span>
                  </div>
                </div>

                {/* Evidence Q1 through Q11 */}
                <div className="space-y-3 pt-2">
                  <h4 className="text-xs font-mono font-bold text-[#52627A] uppercase tracking-wider">
                    Official Methodology Evidence Dossier (Q1–Q11)
                  </h4>

                  <div className="space-y-2.5 text-xs">
                    <div className="p-3.5 rounded-xl bg-white border border-[#E7EAF0]">
                      <span className="font-bold text-[#17294B] block mb-1">Q1: Why is this candidate considered reliable?</span>
                      <p className="text-[#52627A] leading-relaxed">{candidateProfile.evidence_questions.q1_why_considered}</p>
                    </div>

                    <div className="p-3.5 rounded-xl bg-white border border-[#E7EAF0]">
                      <span className="font-bold text-[#17294B] block mb-1">Q2: How many deliveries were evaluated under pressure?</span>
                      <p className="text-[#52627A] leading-relaxed">{candidateProfile.evidence_questions.q2_pressure_deliveries}</p>
                    </div>

                    <div className="p-3.5 rounded-xl bg-white border border-[#E7EAF0]">
                      <span className="font-bold text-[#17294B] block mb-1">Q3: What match and season span is represented?</span>
                      <p className="text-[#52627A] leading-relaxed">{candidateProfile.evidence_questions.q3_matches_and_seasons}</p>
                    </div>

                    <div className="p-3.5 rounded-xl bg-white border border-[#E7EAF0]">
                      <span className="font-bold text-[#17294B] block mb-1">Q4: Observed performance metrics under pressure:</span>
                      <p className="text-[#52627A] leading-relaxed">{candidateProfile.evidence_questions.q4_observed_performance}</p>
                    </div>

                    <div className="p-3.5 rounded-xl bg-white border border-[#E7EAF0]">
                      <span className="font-bold text-[#17294B] block mb-1">Q5: Context-stratified expected baseline:</span>
                      <p className="text-[#52627A] leading-relaxed">{candidateProfile.evidence_questions.q5_expected_performance}</p>
                    </div>

                    <div className="p-3.5 rounded-xl bg-white border border-[#E7EAF0]">
                      <span className="font-bold text-[#17294B] block mb-1">Q6: Conservative diagnostic bound:</span>
                      <p className="text-[#52627A] leading-relaxed">{candidateProfile.evidence_questions.q6_conservative_diagnostic}</p>
                    </div>

                    <div className="p-3.5 rounded-xl bg-white border border-[#E7EAF0]">
                      <span className="font-bold text-[#17294B] block mb-1">Q7: Posterior uncertainty and shrinkage:</span>
                      <p className="text-[#52627A] leading-relaxed">{candidateProfile.evidence_questions.q7_posterior_uncertainty}</p>
                    </div>

                    <div className="p-3.5 rounded-xl bg-white border border-[#E7EAF0]">
                      <span className="font-bold text-[#17294B] block mb-1">Q8: 95% Bayesian credible interval:</span>
                      <p className="text-[#52627A] leading-relaxed">{candidateProfile.evidence_questions.q8_credible_interval}</p>
                    </div>

                    <div className="p-3.5 rounded-xl bg-white border border-[#E7EAF0]">
                      <span className="font-bold text-[#17294B] block mb-1">Q9: Tournament & competition cross-support:</span>
                      <p className="text-[#52627A] leading-relaxed">{candidateProfile.evidence_questions.q9_competition_support}</p>
                    </div>

                    <div className="p-3.5 rounded-xl bg-white border border-[#E7EAF0]">
                      <span className="font-bold text-[#17294B] block mb-1">Q10: Major limitations and sample caveats:</span>
                      <p className="text-[#52627A] leading-relaxed">{candidateProfile.evidence_questions.q10_major_limitations}</p>
                    </div>

                    <div className="p-3.5 rounded-xl bg-white border border-[#E7EAF0]">
                      <span className="font-bold text-[#17294B] block mb-1">Q11: Sensitivity to modeling assumptions:</span>
                      <p className="text-[#52627A] leading-relaxed">{candidateProfile.evidence_questions.q11_sensitivity_to_assumptions}</p>
                    </div>
                  </div>
                </div>

                <div className="flex justify-end pt-2">
                  <button
                    onClick={closeCandidateModal}
                    className="px-5 py-2 rounded-lg bg-[#17294B] hover:bg-[#17294B] text-xs font-semibold text-white transition-colors"
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
