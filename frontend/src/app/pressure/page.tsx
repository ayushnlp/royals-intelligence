"use client";

import React, { useState, useEffect, useMemo } from "react";
import Link from "next/link";
import {
  PressureOverviewResponse,
  PressureLeaderboardResponse,
  PressureLeaderboardBattingItem,
  PressureLeaderboardBowlingItem,
  CandidateEvidenceProfileResponse,
  PressureMethodologyResponse,
} from "@/types";
import {
  fetchPressureOverview,
  fetchPressureLeaderboards,
  fetchCandidateProfile,
  fetchPressureMethodology,
} from "@/lib/api";
import {
  Shield,
  Award,
  TrendingUp,
  Target,
  Flame,
  Activity,
  CheckCircle2,
  Sparkles,
  Info,
  ChevronRight,
  X,
  FileText,
  RefreshCw,
  Sliders,
  ExternalLink,
  Crosshair,
  ArrowRight,
  AlertTriangle,
} from "lucide-react";
import { cn } from "@/lib/utils";

export default function PressureIntelligencePage() {
  const [activeTab, setActiveTab] = useState<"batting" | "bowling" | "methodology">("batting");
  const [competitionFilter, setCompetitionFilter] = useState<"all" | "ipl" | "t20i">("all");
  const [loading, setLoading] = useState<boolean>(true);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  // Core Data
  const [overview, setOverview] = useState<PressureOverviewResponse | null>(null);
  const [leaderboards, setLeaderboards] = useState<PressureLeaderboardResponse | null>(null);
  const [methodology, setMethodology] = useState<PressureMethodologyResponse | null>(null);

  // Candidate Evidence Dossier Modal
  const [selectedPlayerId, setSelectedPlayerId] = useState<number | null>(null);
  const [selectedDiscipline, setSelectedDiscipline] = useState<"batting" | "bowling">("batting");
  const [candidateProfile, setCandidateProfile] = useState<CandidateEvidenceProfileResponse | null>(null);
  const [candidateLoading, setCandidateLoading] = useState<boolean>(false);

  // Initial Load
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
      if (lbRes) {
        setLeaderboards(lbRes);
      } else {
        setErrorMsg("Pressure Intelligence backend API is offline or standby. Ensure uvicorn is running on port 8000.");
      }
      if (methRes) setMethodology(methRes);
    } catch (err: any) {
      setErrorMsg("Failed to communicate with Pressure Intelligence backend service.");
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
      if (tab === "methodology" || window.location.hash === "#methodology") {
        setActiveTab("methodology");
      }
    }
  }, []);

  // Filtered Leaderboard Items
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

  // Load Candidate Profile when modal opens
  const handleInspectCandidate = async (playerId: number, discipline: "batting" | "bowling") => {
    setSelectedPlayerId(playerId);
    setSelectedDiscipline(discipline);
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
    <div className="min-h-screen bg-[#0B132B] text-slate-100 p-6 md:p-8 space-y-8">
      {/* ------------------------------------------------------------------- */}
      {/* Header Banner & Challenge Context */}
      {/* ------------------------------------------------------------------- */}
      <div className="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-4 pb-6 border-b border-[#1A2B50]">
        <div>
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-[#E91E8F] to-[#D6B56D] p-0.5 shadow-lg flex items-center justify-center">
              <div className="w-full h-full bg-[#101C37] rounded-[10px] flex items-center justify-center">
                <Shield className="w-5 h-5 text-[#E91E8F]" />
              </div>
            </div>
            <div>
              <h1 className="text-2xl font-bold tracking-tight text-white flex items-center gap-3">
                Pressure Reliability & Ranking Engine
                <span className="text-xs font-mono font-bold px-2 py-0.5 rounded-full bg-[#E91E8F]/20 text-[#E91E8F] border border-[#E91E8F]/30">
                  Round 1 Sealed
                </span>
              </h1>
              <p className="text-xs text-slate-400 mt-0.5">
                SupeRR Selector Season 2 • Official Top 10 Batters & Bowlers Under Pressure • Empirical Bayes PRI
              </p>
            </div>
          </div>
        </div>

        {/* Global Metadata Badges & Cross-Navigation */}
        <div className="flex flex-wrap items-center gap-2">
          <Link
            href="/tactical"
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-[#101C37] text-[#D6B56D] hover:bg-[#1A2B50] border border-[#D6B56D]/40 transition-all text-xs font-semibold shadow-sm"
          >
            <Crosshair className="w-3.5 h-3.5" />
            <span>Tactical Analytics</span>
            <ArrowRight size={13} />
          </Link>
          <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-[#101C37] border border-[#1A2B50] text-xs font-mono text-slate-300">
            <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
            <span>200,999 Balls Verified</span>
          </div>
          <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-[#101C37] border border-[#1A2B50] text-xs font-mono text-[#D6B56D]">
            <Sparkles className="w-3.5 h-3.5" />
            <span>1-SE Lower Credible Bound</span>
          </div>
          <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-[#E91E8F]/10 border border-[#E91E8F]/30 text-xs font-mono text-[#E91E8F] font-semibold">
            <Award className="w-3.5 h-3.5" />
            <span>Official Unstop Selection Deliverable</span>
          </div>
        </div>
      </div>

      {/* Connection Alert Banner (if backend unreachable) */}
      {errorMsg && (
        <div className="p-4 rounded-xl bg-amber-500/10 border border-amber-500/30 flex items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <AlertTriangle className="w-5 h-5 text-amber-400 shrink-0" />
            <div>
              <div className="text-xs font-bold text-amber-300">Backend API Offline / Standby Notice</div>
              <div className="text-[11px] text-slate-300 mt-0.5">{errorMsg}</div>
            </div>
          </div>
          <button
            onClick={loadPressureData}
            className="px-3 py-1.5 rounded-lg bg-amber-500 text-[#101C37] font-bold text-xs hover:bg-amber-400 transition-colors shrink-0 flex items-center gap-1.5"
          >
            <RefreshCw className="w-3.5 h-3.5" />
            <span>Retry Connection</span>
          </button>
        </div>
      )}

      {/* ------------------------------------------------------------------- */}
      {/* Overview Telemetry Ribbon */}
      {/* ------------------------------------------------------------------- */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3.5">
        <div className="p-4 rounded-xl bg-[#101C37]/80 border border-[#1A2B50] hover:border-[#E91E8F]/40 transition-all">
          <div className="flex items-center justify-between text-slate-400 mb-1">
            <span className="text-[11px] font-medium uppercase tracking-wider">Strict Pressure Balls</span>
            <Flame className="w-3.5 h-3.5 text-rose-500" />
          </div>
          <div className="text-xl font-bold font-mono text-white">
            {overview ? `${overview.strict_pressure_bowling_balls.toLocaleString()}` : "37,014"}
          </div>
          <div className="text-[10px] text-slate-400 mt-1">
            Bowling ({overview?.strict_pressure_batting_balls.toLocaleString() ?? "31,163"} Batting)
          </div>
        </div>

        <div className="p-4 rounded-xl bg-[#101C37]/80 border border-[#1A2B50] hover:border-[#E91E8F]/40 transition-all">
          <div className="flex items-center justify-between text-slate-400 mb-1">
            <span className="text-[11px] font-medium uppercase tracking-wider">Death Concentration</span>
            <Activity className="w-3.5 h-3.5 text-amber-400" />
          </div>
          <div className="text-xl font-bold font-mono text-white">
            {overview ? `${overview.death_overs_bowling_pressure_share_pct}%` : "87.3%"}
          </div>
          <div className="text-[10px] text-slate-400 mt-1">
            Overs 16–20 bowling pressure
          </div>
        </div>

        <div className="p-4 rounded-xl bg-[#101C37]/80 border border-[#1A2B50] hover:border-[#E91E8F]/40 transition-all">
          <div className="flex items-center justify-between text-slate-400 mb-1">
            <span className="text-[11px] font-medium uppercase tracking-wider">Candidate Population</span>
            <Target className="w-3.5 h-3.5 text-cyan-400" />
          </div>
          <div className="text-xl font-bold font-mono text-white">
            {overview ? `${overview.total_evaluated_batters} / ${overview.total_evaluated_bowlers}` : "278 / 239"}
          </div>
          <div className="text-[10px] text-slate-400 mt-1">
            Batters / Bowlers evaluated
          </div>
        </div>

        <div className="p-4 rounded-xl bg-[#101C37]/80 border border-[#1A2B50] hover:border-[#E91E8F]/40 transition-all">
          <div className="flex items-center justify-between text-slate-400 mb-1">
            <span className="text-[11px] font-medium uppercase tracking-wider">Sample Gate</span>
            <Shield className="w-3.5 h-3.5 text-emerald-400" />
          </div>
          <div className="text-xl font-bold font-mono text-white">
            &ge; 60 Balls
          </div>
          <div className="text-[10px] text-slate-400 mt-1">
            Or &ge; 50 balls &amp; 10 matches
          </div>
        </div>

        <div className="p-4 rounded-xl bg-[#101C37]/80 border border-[#1A2B50] hover:border-[#E91E8F]/40 transition-all">
          <div className="flex items-center justify-between text-slate-400 mb-1">
            <span className="text-[11px] font-medium uppercase tracking-wider">Baseline Strata</span>
            <Sliders className="w-3.5 h-3.5 text-purple-400" />
          </div>
          <div className="text-xl font-bold font-mono text-white">
            12 Cells
          </div>
          <div className="text-[10px] text-slate-400 mt-1">
            Phase &times; Tier &times; Innings
          </div>
        </div>

        <div className="p-4 rounded-xl bg-[#101C37]/80 border border-[#1A2B50] hover:border-[#E91E8F]/40 transition-all">
          <div className="flex items-center justify-between text-slate-400 mb-1">
            <span className="text-[11px] font-medium uppercase tracking-wider">Governing Metric</span>
            <Sparkles className="w-3.5 h-3.5 text-[#D6B56D]" />
          </div>
          <div className="text-base font-bold font-mono text-[#D6B56D]">
            Cons. PRI
          </div>
          <div className="text-[10px] text-slate-400 mt-1">
            Posterior Mean &minus; 1.0 SE
          </div>
        </div>
      </div>

      {/* ------------------------------------------------------------------- */}
      {/* Sub-System Navigation Tabs */}
      {/* ------------------------------------------------------------------- */}
      <div className="flex items-center gap-2 border-b border-[#1A2B50] pb-2 overflow-x-auto">
        <button
          onClick={() => setActiveTab("batting")}
          className={cn(
            "flex items-center gap-2 px-4 py-2 rounded-lg text-xs font-semibold transition-all whitespace-nowrap",
            activeTab === "batting"
              ? "bg-[#E91E8F] text-white shadow-md shadow-[#E91E8F]/20"
              : "text-slate-400 hover:text-white hover:bg-[#101C37]"
          )}
        >
          <TrendingUp className="w-4 h-4" />
          <span>Top 10 Batters Under Pressure</span>
        </button>

        <button
          onClick={() => setActiveTab("bowling")}
          className={cn(
            "flex items-center gap-2 px-4 py-2 rounded-lg text-xs font-semibold transition-all whitespace-nowrap",
            activeTab === "bowling"
              ? "bg-[#E91E8F] text-white shadow-md shadow-[#E91E8F]/20"
              : "text-slate-400 hover:text-white hover:bg-[#101C37]"
          )}
        >
          <Target className="w-4 h-4" />
          <span>Top 10 Bowlers Under Pressure</span>
        </button>

        <button
          onClick={() => setActiveTab("methodology")}
          className={cn(
            "flex items-center gap-2 px-4 py-2 rounded-lg text-xs font-semibold transition-all whitespace-nowrap",
            activeTab === "methodology"
              ? "bg-[#E91E8F] text-white shadow-md shadow-[#E91E8F]/20"
              : "text-slate-400 hover:text-white hover:bg-[#101C37]"
          )}
        >
          <FileText className="w-4 h-4 text-[#D6B56D]" />
          <span>Bayesian Reliability Methodology</span>
        </button>
      </div>

      {/* ------------------------------------------------------------------- */}
      {/* TAB 1: TOP 10 BATTERS UNDER PRESSURE */}
      {/* ------------------------------------------------------------------- */}
      {activeTab === "batting" && (
        <div className="space-y-4">
          <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 p-5 rounded-xl bg-[#101C37]/60 border border-[#1A2B50]">
            <div>
              <h2 className="text-lg font-bold text-white flex items-center gap-2">
                <TrendingUp className="w-5 h-5 text-[#E91E8F]" />
                Official Top 10 Batters Under Pressure (Unstop Dropdown Guide)
              </h2>
              <p className="text-xs text-slate-400 mt-1">
                Ranked strictly by Conservative PRI (1-SE Lower Credible Bound in Strike Rate points).
              </p>
            </div>
            <div className="flex flex-wrap items-center gap-2">
              {/* Competition Filters */}
              <div className="flex items-center gap-1 bg-[#101C37] p-1 rounded-lg border border-[#1A2B50]">
                <button
                  onClick={() => setCompetitionFilter("all")}
                  className={cn(
                    "px-2.5 py-1 rounded text-[11px] font-mono font-semibold transition-all",
                    competitionFilter === "all"
                      ? "bg-[#E91E8F] text-white shadow-sm"
                      : "text-slate-400 hover:text-white"
                  )}
                >
                  Combined
                </button>
                <button
                  onClick={() => setCompetitionFilter("ipl")}
                  className={cn(
                    "px-2.5 py-1 rounded text-[11px] font-mono font-semibold transition-all",
                    competitionFilter === "ipl"
                      ? "bg-[#E91E8F] text-white shadow-sm"
                      : "text-slate-400 hover:text-white"
                  )}
                >
                  IPL
                </button>
                <button
                  onClick={() => setCompetitionFilter("t20i")}
                  className={cn(
                    "px-2.5 py-1 rounded text-[11px] font-mono font-semibold transition-all",
                    competitionFilter === "t20i"
                      ? "bg-[#E91E8F] text-white shadow-sm"
                      : "text-slate-400 hover:text-white"
                  )}
                >
                  T20I
                </button>
              </div>

              <span className="text-xs font-mono font-bold px-2.5 py-1 rounded bg-[#E91E8F]/20 text-[#E91E8F] border border-[#E91E8F]/30">
                Sealed Baseline: Checkpoint 6005022
              </span>
            </div>
          </div>

          <div className="rounded-xl border border-[#1A2B50] overflow-hidden bg-[#101C37]/80">
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs font-mono">
                <thead className="bg-[#101C37] text-slate-400 uppercase text-[10px] tracking-wider border-b border-[#1A2B50]">
                  <tr>
                    <th className="px-4 py-3 font-sans">Rank & Batter</th>
                    <th className="px-4 py-3 text-right">Conservative PRI</th>
                    <th className="px-4 py-3 text-right">Posterior Mean (&theta;)</th>
                    <th className="px-4 py-3 text-right">Uncertainty (SE)</th>
                    <th className="px-4 py-3 text-right">95% Credible Region</th>
                    <th className="px-4 py-3 text-right">Pressure Balls</th>
                    <th className="px-4 py-3 text-right">Matches</th>
                    <th className="px-4 py-3 text-center font-sans">Tournament Qualification</th>
                    <th className="px-4 py-3 text-center font-sans">Evidence Dossier</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-[#1A2B50]/60">
                  {loading ? (
                    <tr>
                      <td colSpan={9} className="px-6 py-12 text-center text-slate-400">
                        <div className="flex flex-col items-center justify-center gap-2">
                          <RefreshCw className="w-6 h-6 animate-spin text-[#E91E8F]" />
                          <span className="text-xs font-mono">Loading official batting leaderboard from Parquet engine...</span>
                        </div>
                      </td>
                    </tr>
                  ) : filteredBatters.length > 0 ? (
                    filteredBatters.map((batter: PressureLeaderboardBattingItem) => {
                      const isTop1 = batter.rank === 1;
                      const isTop3 = batter.rank <= 3;
                      return (
                        <tr key={batter.player_id} className="hover:bg-[#1A2B50]/40 transition-colors">
                          <td className="px-4 py-3 font-sans font-semibold text-white flex items-center gap-2.5">
                            <span className={cn(
                              "w-6 h-6 rounded-full flex items-center justify-center text-[10px] font-mono font-bold",
                              isTop1 ? "bg-[#D6B56D] text-[#101C37]" : isTop3 ? "bg-[#E91E8F] text-white" : "bg-[#1A2B50] text-slate-300"
                            )}>
                              {batter.rank}
                            </span>
                            <div>
                              <div>{batter.player_name}</div>
                              <div className="text-[10px] font-mono text-slate-400">ID: {batter.player_id}</div>
                            </div>
                          </td>
                          <td className="px-4 py-3 text-right">
                            <span className={cn(
                              "font-bold text-sm",
                              batter.conservative_pri > 0 ? "text-emerald-400" : "text-[#D6B56D]"
                            )}>
                              {batter.conservative_pri > 0 ? `+${batter.conservative_pri.toFixed(1)}` : batter.conservative_pri.toFixed(1)} SR pts
                            </span>
                          </td>
                          <td className="px-4 py-3 text-right text-emerald-400 font-bold">
                            +{batter.posterior_mean.toFixed(1)}
                          </td>
                          <td className="px-4 py-3 text-right text-slate-300">
                            &plusmn;{batter.posterior_se.toFixed(1)}
                          </td>
                          <td className="px-4 py-3 text-right text-slate-400 text-[11px]">
                            [{batter.ci_95_lower.toFixed(1)}, +{batter.ci_95_upper.toFixed(1)}]
                          </td>
                          <td className="px-4 py-3 text-right text-white font-bold">
                            {batter.pressure_legal_balls}
                          </td>
                          <td className="px-4 py-3 text-right text-slate-300">
                            {batter.pressure_matches}
                          </td>
                          <td className="px-4 py-3 text-center font-sans">
                            <span className="text-[10px] font-mono font-semibold px-2 py-0.5 rounded bg-[#101C37] text-slate-300 border border-[#1A2B50]">
                              {batter.competition_qualification.replace("_QUALIFIED", "")}
                            </span>
                          </td>
                          <td className="px-4 py-3 text-center font-sans">
                            <button
                              onClick={() => handleInspectCandidate(batter.player_id, "batting")}
                              className="px-2.5 py-1 rounded bg-[#E91E8F]/20 hover:bg-[#E91E8F]/30 text-[#E91E8F] border border-[#E91E8F]/30 text-[11px] font-semibold transition-all flex items-center gap-1 mx-auto"
                            >
                              <span>Inspect Q1–Q11</span>
                              <ChevronRight className="w-3 h-3" />
                            </button>
                          </td>
                        </tr>
                      );
                    })
                  ) : (
                    <tr>
                      <td colSpan={9} className="px-6 py-12 text-center text-slate-400">
                        <div className="flex flex-col items-center justify-center gap-2">
                          <AlertTriangle className="w-8 h-8 text-amber-400" />
                          <span className="font-semibold text-white">No Batting Data Available</span>
                          <span className="text-xs text-slate-400 max-w-md">
                            {errorMsg || "Ensure the backend service is running on http://localhost:8000"}
                          </span>
                          <button
                            onClick={loadPressureData}
                            className="mt-2 px-3 py-1.5 rounded-lg bg-[#E91E8F] text-white text-xs font-semibold hover:bg-[#E91E8F]/80 transition-colors flex items-center gap-1.5"
                          >
                            <RefreshCw className="w-3.5 h-3.5" />
                            <span>Retry API Request</span>
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
          <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 p-5 rounded-xl bg-[#101C37]/60 border border-[#1A2B50]">
            <div>
              <h2 className="text-lg font-bold text-white flex items-center gap-2">
                <Target className="w-5 h-5 text-cyan-400" />
                Official Top 10 Bowlers Under Pressure (Unstop Dropdown Guide)
              </h2>
              <p className="text-xs text-slate-400 mt-1">
                Ranked strictly by Conservative Runs Saved per 6 balls (1-SE Lower Credible Bound in Economy).
              </p>
            </div>
            <div className="flex flex-wrap items-center gap-2">
              {/* Competition Filters */}
              <div className="flex items-center gap-1 bg-[#101C37] p-1 rounded-lg border border-[#1A2B50]">
                <button
                  onClick={() => setCompetitionFilter("all")}
                  className={cn(
                    "px-2.5 py-1 rounded text-[11px] font-mono font-semibold transition-all",
                    competitionFilter === "all"
                      ? "bg-cyan-500 text-[#101C37] font-bold shadow-sm"
                      : "text-slate-400 hover:text-white"
                  )}
                >
                  Combined
                </button>
                <button
                  onClick={() => setCompetitionFilter("ipl")}
                  className={cn(
                    "px-2.5 py-1 rounded text-[11px] font-mono font-semibold transition-all",
                    competitionFilter === "ipl"
                      ? "bg-cyan-500 text-[#101C37] font-bold shadow-sm"
                      : "text-slate-400 hover:text-white"
                  )}
                >
                  IPL
                </button>
                <button
                  onClick={() => setCompetitionFilter("t20i")}
                  className={cn(
                    "px-2.5 py-1 rounded text-[11px] font-mono font-semibold transition-all",
                    competitionFilter === "t20i"
                      ? "bg-cyan-500 text-[#101C37] font-bold shadow-sm"
                      : "text-slate-400 hover:text-white"
                  )}
                >
                  T20I
                </button>
              </div>

              <span className="text-xs font-mono font-bold px-2.5 py-1 rounded bg-cyan-500/20 text-cyan-300 border border-cyan-500/30">
                Sealed Baseline: Checkpoint 6005022
              </span>
            </div>
          </div>

          <div className="rounded-xl border border-[#1A2B50] overflow-hidden bg-[#101C37]/80">
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs font-mono">
                <thead className="bg-[#101C37] text-slate-400 uppercase text-[10px] tracking-wider border-b border-[#1A2B50]">
                  <tr>
                    <th className="px-4 py-3 font-sans">Rank & Bowler</th>
                    <th className="px-4 py-3 text-right">Conservative Runs Saved</th>
                    <th className="px-4 py-3 text-right">Posterior Mean (&theta;)</th>
                    <th className="px-4 py-3 text-right">Uncertainty (SE)</th>
                    <th className="px-4 py-3 text-right">95% Credible Region</th>
                    <th className="px-4 py-3 text-right">Pressure Balls</th>
                    <th className="px-4 py-3 text-right">Matches</th>
                    <th className="px-4 py-3 text-center font-sans">Tournament Qualification</th>
                    <th className="px-4 py-3 text-center font-sans">Evidence Dossier</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-[#1A2B50]/60">
                  {loading ? (
                    <tr>
                      <td colSpan={9} className="px-6 py-12 text-center text-slate-400">
                        <div className="flex flex-col items-center justify-center gap-2">
                          <RefreshCw className="w-6 h-6 animate-spin text-cyan-400" />
                          <span className="text-xs font-mono">Loading official bowling leaderboard from Parquet engine...</span>
                        </div>
                      </td>
                    </tr>
                  ) : filteredBowlers.length > 0 ? (
                    filteredBowlers.map((bowler: PressureLeaderboardBowlingItem) => {
                      const isTop1 = bowler.rank === 1;
                      const isTop3 = bowler.rank <= 3;
                      return (
                        <tr key={bowler.player_id} className="hover:bg-[#1A2B50]/40 transition-colors">
                          <td className="px-4 py-3 font-sans font-semibold text-white flex items-center gap-2.5">
                            <span className={cn(
                              "w-6 h-6 rounded-full flex items-center justify-center text-[10px] font-mono font-bold",
                              isTop1 ? "bg-[#D6B56D] text-[#101C37]" : isTop3 ? "bg-cyan-500 text-[#101C37]" : "bg-[#1A2B50] text-slate-300"
                            )}>
                              {bowler.rank}
                            </span>
                            <div>
                              <div>{bowler.player_name}</div>
                              <div className="text-[10px] font-mono text-slate-400">ID: {bowler.player_id}</div>
                            </div>
                          </td>
                          <td className="px-4 py-3 text-right">
                            <span className={cn(
                              "font-bold text-sm text-cyan-300"
                            )}>
                              {bowler.conservative_runs_saved.toFixed(2)} RPO
                            </span>
                          </td>
                          <td className="px-4 py-3 text-right text-slate-200 font-bold">
                            {bowler.posterior_mean > 0 ? `+${bowler.posterior_mean.toFixed(2)}` : bowler.posterior_mean.toFixed(2)} RPO
                          </td>
                          <td className="px-4 py-3 text-right text-slate-300">
                            &plusmn;{bowler.posterior_se.toFixed(2)}
                          </td>
                          <td className="px-4 py-3 text-right text-slate-400 text-[11px]">
                            [{bowler.ci_95_lower.toFixed(2)}, +{bowler.ci_95_upper.toFixed(2)}]
                          </td>
                          <td className="px-4 py-3 text-right text-white font-bold">
                            {bowler.pressure_legal_balls}
                          </td>
                          <td className="px-4 py-3 text-right text-slate-300">
                            {bowler.pressure_matches}
                          </td>
                          <td className="px-4 py-3 text-center font-sans">
                            <span className="text-[10px] font-mono font-semibold px-2 py-0.5 rounded bg-[#101C37] text-slate-300 border border-[#1A2B50]">
                              {bowler.competition_qualification.replace("_QUALIFIED", "")}
                            </span>
                          </td>
                          <td className="px-4 py-3 text-center font-sans">
                            <button
                              onClick={() => handleInspectCandidate(bowler.player_id, "bowling")}
                              className="px-2.5 py-1 rounded bg-cyan-500/20 hover:bg-cyan-500/30 text-cyan-300 border border-cyan-500/30 text-[11px] font-semibold transition-all flex items-center gap-1 mx-auto"
                            >
                              <span>Inspect Q1–Q11</span>
                              <ChevronRight className="w-3 h-3" />
                            </button>
                          </td>
                        </tr>
                      );
                    })
                  ) : (
                    <tr>
                      <td colSpan={9} className="px-6 py-12 text-center text-slate-400">
                        <div className="flex flex-col items-center justify-center gap-2">
                          <AlertTriangle className="w-8 h-8 text-amber-400" />
                          <span className="font-semibold text-white">No Bowling Data Available</span>
                          <span className="text-xs text-slate-400 max-w-md">
                            {errorMsg || "Ensure the backend service is running on http://localhost:8000"}
                          </span>
                          <button
                            onClick={loadPressureData}
                            className="mt-2 px-3 py-1.5 rounded-lg bg-cyan-500 text-[#101C37] text-xs font-semibold hover:bg-cyan-400 transition-colors flex items-center gap-1.5"
                          >
                            <RefreshCw className="w-3.5 h-3.5" />
                            <span>Retry API Request</span>
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
          <div className="p-6 rounded-2xl bg-[#101C37]/80 border border-[#1A2B50] space-y-6">
            <div>
              <h2 className="text-xl font-bold text-white flex items-center gap-2">
                <FileText className="w-5 h-5 text-[#D6B56D]" />
                Statistical Methodology & Reliability Framework
              </h2>
              <p className="text-xs text-slate-400 mt-1">
                Mathematical formulations, empirical Bayes shrinkage, and 12-cell baseline context stratification.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Pressure Situation Definition */}
              <div className="p-5 rounded-xl bg-[#0B132B] border border-[#1A2B50] space-y-3">
                <h3 className="text-sm font-bold text-white flex items-center gap-2">
                  <Flame className="w-4 h-4 text-rose-500" />
                  Dynamic Pressure Situation Definition
                </h3>
                <div className="text-xs text-slate-300 space-y-2 leading-relaxed">
                  <p>
                    <strong className="text-white">Chasing (Innings 2):</strong> Required Run Rate &ge; 9.0 with balls remaining &le; 36, OR RRR &ge; 12.0 at any point, OR close finishes (balls &le; 18, runs &le; 36, wkts &le; 5).
                  </p>
                  <p>
                    <strong className="text-white">Setting Target (Innings 1):</strong> Overs 16–20 where team has lost &ge; 4 wickets, OR overs 18–20 in any contested match.
                  </p>
                  <p className="text-amber-300 font-mono text-[11px]">
                    Death Overs Concentration: 87.28% of bowling pressure and 78.95% of batting pressure occur in overs 16–20.
                  </p>
                </div>
              </div>

              {/* 12-Cell Context Stratified Baselines */}
              <div className="p-5 rounded-xl bg-[#0B132B] border border-[#1A2B50] space-y-3">
                <h3 className="text-sm font-bold text-white flex items-center gap-2">
                  <Sliders className="w-4 h-4 text-purple-400" />
                  12-Cell Context-Stratified Baselines
                </h3>
                <p className="text-xs text-slate-300 leading-relaxed">
                  To eliminate structural phase and venue biases, expected baselines are calculated across a 12-cell non-pressure matrix:
                </p>
                <div className="grid grid-cols-2 gap-1.5 font-mono text-[10px] text-slate-300">
                  {methodology.baseline_strata_12_cell.map((cell, idx) => (
                    <div key={idx} className="p-1.5 rounded bg-[#101C37] border border-[#1A2B50] truncate">
                      {cell}
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Empirical Bayes Shrinkage */}
            <div className="p-5 rounded-xl bg-[#0B132B] border border-[#1A2B50] space-y-3">
              <h3 className="text-sm font-bold text-white flex items-center gap-2">
                <Sparkles className="w-4 h-4 text-[#D6B56D]" />
                Hierarchical Empirical Bayes Shrinkage & Conservative PRI
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 font-mono text-xs">
                <div className="space-y-1.5 p-3.5 rounded-lg bg-[#101C37] border border-[#1A2B50]">
                  <span className="text-slate-400 text-[11px] font-sans font-semibold">Prior & Shrinkage Weight</span>
                  <div className="text-slate-200">B_i = &sigma;_i&sup2; / (&sigma;_i&sup2; + &tau;&sup2;)</div>
                  <div className="text-slate-200">&theta;_hat_i = B_i &times; &mu;_0 + (1 &minus; B_i) &times; &Delta;_i</div>
                </div>
                <div className="space-y-1.5 p-3.5 rounded-lg bg-[#101C37] border border-[#1A2B50]">
                  <span className="text-slate-400 text-[11px] font-sans font-semibold">Conservative Lower Bound (1-SE)</span>
                  <div className="text-emerald-400">Batting: Conservative PRI = &theta;_hat_i &minus; 1.0 &times; SE_i</div>
                  <div className="text-cyan-300">Bowling: Runs Saved = &minus;(&theta;_hat_i + 1.0 &times; SE_i)</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* ------------------------------------------------------------------- */}
      {/* CANDIDATE EVIDENCE PROFILE MODAL / DRAWER */}
      {/* ------------------------------------------------------------------- */}
      {selectedPlayerId && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-[#101C37] border border-[#1A2B50] rounded-2xl max-w-3xl w-full max-h-[85vh] overflow-y-auto shadow-2xl p-6 space-y-6">
            {/* Modal Header */}
            <div className="flex items-center justify-between pb-4 border-b border-[#1A2B50]">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-[#E91E8F] to-[#D6B56D] p-0.5 flex items-center justify-center">
                  <div className="w-full h-full bg-[#101C37] rounded-[10px] flex items-center justify-center font-bold text-white">
                    #{candidateProfile?.rank ?? "—"}
                  </div>
                </div>
                <div>
                  <h3 className="text-xl font-bold text-white flex items-center gap-2">
                    {candidateProfile?.player_name ?? "Loading Candidate..."}
                    <span className="text-xs font-mono text-slate-400">ID: {candidateProfile?.player_id}</span>
                  </h3>
                  <div className="flex items-center gap-2 mt-0.5">
                    <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded bg-[#E91E8F]/20 text-[#E91E8F] border border-[#E91E8F]/30">
                      {candidateProfile?.discipline.toUpperCase()}
                    </span>
                    <span className="text-[10px] font-mono font-semibold px-2 py-0.5 rounded bg-[#D6B56D]/20 text-[#D6B56D] border border-[#D6B56D]/30">
                      {candidateProfile?.competition_qualification}
                    </span>
                  </div>
                </div>
              </div>

              <button
                onClick={closeCandidateModal}
                className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-[#1A2B50] transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Modal Body: Q1–Q11 Evidence Questions */}
            {candidateLoading ? (
              <div className="flex items-center justify-center py-12 text-slate-400 text-xs font-mono">
                <RefreshCw className="w-5 h-5 animate-spin text-[#E91E8F] mr-2" />
                Loading candidate evidence dossier...
              </div>
            ) : candidateProfile ? (
              <div className="space-y-4">
                {/* Stats Summary Strip */}
                <div className="grid grid-cols-2 md:grid-cols-4 gap-3 font-mono text-xs text-center">
                  <div className="p-3 rounded-lg bg-[#0B132B] border border-[#1A2B50]">
                    <span className="text-[10px] text-slate-400 uppercase block">Governing Bound</span>
                    <span className="text-base font-bold text-emerald-400">
                      {candidateProfile.governing_metric_value > 0 ? `+${candidateProfile.governing_metric_value.toFixed(2)}` : candidateProfile.governing_metric_value.toFixed(2)}
                    </span>
                  </div>
                  <div className="p-3 rounded-lg bg-[#0B132B] border border-[#1A2B50]">
                    <span className="text-[10px] text-slate-400 uppercase block">Posterior Mean (&theta;)</span>
                    <span className="text-base font-bold text-white">
                      {candidateProfile.posterior_mean > 0 ? `+${candidateProfile.posterior_mean.toFixed(2)}` : candidateProfile.posterior_mean.toFixed(2)}
                    </span>
                  </div>
                  <div className="p-3 rounded-lg bg-[#0B132B] border border-[#1A2B50]">
                    <span className="text-[10px] text-slate-400 uppercase block">Uncertainty (SE)</span>
                    <span className="text-base font-bold text-slate-300">
                      &plusmn;{candidateProfile.posterior_se.toFixed(2)}
                    </span>
                  </div>
                  <div className="p-3 rounded-lg bg-[#0B132B] border border-[#1A2B50]">
                    <span className="text-[10px] text-slate-400 uppercase block">Pressure Balls</span>
                    <span className="text-base font-bold text-white">
                      {candidateProfile.pressure_legal_balls} ({candidateProfile.pressure_matches} M)
                    </span>
                  </div>
                </div>

                {/* Evidence Q1 through Q11 */}
                <div className="space-y-3 pt-2">
                  <h4 className="text-xs font-bold text-[#D6B56D] uppercase tracking-wider">
                    Official Methodology Evidence Dossier (Q1–Q11)
                  </h4>

                  <div className="space-y-2.5 text-xs">
                    <div className="p-3 rounded-lg bg-[#0B132B]/80 border border-[#1A2B50]">
                      <span className="font-bold text-white block mb-0.5">Q1: Why is this candidate considered reliable?</span>
                      <p className="text-slate-300 leading-relaxed">{candidateProfile.evidence_questions.q1_why_considered}</p>
                    </div>

                    <div className="p-3 rounded-lg bg-[#0B132B]/80 border border-[#1A2B50]">
                      <span className="font-bold text-white block mb-0.5">Q2: How many deliveries were evaluated under pressure?</span>
                      <p className="text-slate-300 leading-relaxed">{candidateProfile.evidence_questions.q2_pressure_deliveries}</p>
                    </div>

                    <div className="p-3 rounded-lg bg-[#0B132B]/80 border border-[#1A2B50]">
                      <span className="font-bold text-white block mb-0.5">Q3: What match and season span is represented?</span>
                      <p className="text-slate-300 leading-relaxed">{candidateProfile.evidence_questions.q3_matches_and_seasons}</p>
                    </div>

                    <div className="p-3 rounded-lg bg-[#0B132B]/80 border border-[#1A2B50]">
                      <span className="font-bold text-white block mb-0.5">Q4: Observed performance metrics under pressure:</span>
                      <p className="text-slate-300 leading-relaxed">{candidateProfile.evidence_questions.q4_observed_performance}</p>
                    </div>

                    <div className="p-3 rounded-lg bg-[#0B132B]/80 border border-[#1A2B50]">
                      <span className="font-bold text-white block mb-0.5">Q5: Context-stratified expected baseline:</span>
                      <p className="text-slate-300 leading-relaxed">{candidateProfile.evidence_questions.q5_expected_performance}</p>
                    </div>

                    <div className="p-3 rounded-lg bg-[#0B132B]/80 border border-[#1A2B50]">
                      <span className="font-bold text-white block mb-0.5">Q6: Conservative diagnostic bound:</span>
                      <p className="text-slate-300 leading-relaxed">{candidateProfile.evidence_questions.q6_conservative_diagnostic}</p>
                    </div>

                    <div className="p-3 rounded-lg bg-[#0B132B]/80 border border-[#1A2B50]">
                      <span className="font-bold text-white block mb-0.5">Q7: Posterior uncertainty and shrinkage:</span>
                      <p className="text-slate-300 leading-relaxed">{candidateProfile.evidence_questions.q7_posterior_uncertainty}</p>
                    </div>

                    <div className="p-3 rounded-lg bg-[#0B132B]/80 border border-[#1A2B50]">
                      <span className="font-bold text-white block mb-0.5">Q8: 95% Bayesian credible interval:</span>
                      <p className="text-slate-300 leading-relaxed">{candidateProfile.evidence_questions.q8_credible_interval}</p>
                    </div>

                    <div className="p-3 rounded-lg bg-[#0B132B]/80 border border-[#1A2B50]">
                      <span className="font-bold text-white block mb-0.5">Q9: Tournament & competition cross-support:</span>
                      <p className="text-slate-300 leading-relaxed">{candidateProfile.evidence_questions.q9_competition_support}</p>
                    </div>

                    <div className="p-3 rounded-lg bg-[#0B132B]/80 border border-[#1A2B50]">
                      <span className="font-bold text-white block mb-0.5">Q10: Major limitations and sample caveats:</span>
                      <p className="text-slate-300 leading-relaxed">{candidateProfile.evidence_questions.q10_major_limitations}</p>
                    </div>

                    <div className="p-3 rounded-lg bg-[#0B132B]/80 border border-[#1A2B50]">
                      <span className="font-bold text-white block mb-0.5">Q11: Sensitivity to modeling assumptions:</span>
                      <p className="text-slate-300 leading-relaxed">{candidateProfile.evidence_questions.q11_sensitivity_to_assumptions}</p>
                    </div>
                  </div>
                </div>
              </div>
            ) : null}
          </div>
        </div>
      )}
    </div>
  );
}
