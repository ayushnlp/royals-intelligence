"use client";

import React, { useState, useEffect, useMemo } from "react";
import Link from "next/link";
import {
  TacticalDatasetSummaryResponse,
  TacticalPhaseResponse,
  TacticalStrokesResponse,
  HandednessMatrixResponse,
  DeliveryStylesResponse,
  SpeedProfileResponse,
  PlayerTacticalProfileResponse,
  DeathOversRankingResponse,
  HeadToHeadMatchupResponse,
  PlayerLookupItem,
} from "@/types";
import {
  fetchTacticalSummary,
  fetchTacticalPhases,
  fetchTacticalStrokes,
  fetchTacticalHandedness,
  fetchTacticalVariations,
  fetchTacticalSpeedProfiles,
  fetchPlayerTacticalProfile,
  fetchTacticalDeathOvers,
  fetchTacticalMatchup,
  fetchTacticalPlayers,
} from "@/lib/api";
import {
  Target,
  Shield,
  BarChart2,
  Flame,
  Gauge,
  Users,
  Search,
  ChevronRight,
  ArrowRight,
  CheckCircle2,
  AlertTriangle,
  RefreshCw,
  Sparkles,
  Swords,
  Layers,
  Zap,
  TrendingUp,
} from "lucide-react";
import { cn } from "@/lib/utils";

// Pre-defined marquee players for rapid exploration
const MARQUEE_PLAYERS = [
  { id: 2258, name: "Sanju Samson", role: "Batter / Captain", team: "RR" },
  { id: 813, name: "Jos Buttler", role: "Opener / Finisher", team: "RR" },
  { id: 6819, name: "Yashasvi Jaiswal", role: "Opener / LHB", team: "RR" },
  { id: 2320, name: "Trent Boult", role: "Pace Spearhead", team: "RR" },
  { id: 1612, name: "Yuzvendra Chahal", role: "Leg-Break Specialist", team: "RR" },
  { id: 4489, name: "Prasidh Krishna", role: "Express Pace", team: "RR" },
  { id: 47, name: "Virat Kohli", role: "Anchor / Aggressor", team: "RCB" },
  { id: 4722, name: "Rashid Khan", role: "Wrist-Spin / Matchup", team: "GT" },
  { id: 2933, name: "Jasprit Bumrah", role: "Death Specialist", team: "MI" },
  { id: 4260, name: "Heinrich Klaasen", role: "Spin Destroyer", team: "SRH" },
];

// Pre-defined head-to-head micro battles
const PRESET_MATCHUPS = [
  { strikerId: 47, strikerName: "Virat Kohli", bowlerId: 4722, bowlerName: "Rashid Khan", label: "Kohli vs Rashid" },
  { strikerId: 2258, strikerName: "Sanju Samson", bowlerId: 1612, bowlerName: "Yuzvendra Chahal", label: "Samson vs Chahal" },
  { strikerId: 813, strikerName: "Jos Buttler", bowlerId: 2933, bowlerName: "Jasprit Bumrah", label: "Buttler vs Bumrah" },
  { strikerId: 4260, strikerName: "Heinrich Klaasen", bowlerId: 1612, bowlerName: "Yuzvendra Chahal", label: "Klaasen vs Chahal" },
  { strikerId: 6819, strikerName: "Yashasvi Jaiswal", bowlerId: 2320, bowlerName: "Trent Boult", label: "Jaiswal vs Boult" },
];

export default function TacticalIntelligencePage() {
  // Navigation / Tabs state
  const [activeTab, setActiveTab] = useState<
    "overview" | "strokes_handedness" | "bowling_speed" | "death_overs" | "matchups_players"
  >("overview");

  // Loading & Error states
  const [loading, setLoading] = useState<boolean>(true);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  // Module A: Summary
  const [summary, setSummary] = useState<TacticalDatasetSummaryResponse | null>(null);

  // Module B: Phases
  const [phasesData, setPhasesData] = useState<TacticalPhaseResponse | null>(null);

  // Module C: Strokes
  const [strokesData, setStrokesData] = useState<TacticalStrokesResponse | null>(null);
  const [strokeMinBalls, setStrokeMinBalls] = useState<number>(50);
  const [strokeSortKey, setStrokeSortKey] = useState<
    "runs_per_shot" | "deliveries_faced" | "boundary_pct" | "dismissal_rate_pct"
  >("runs_per_shot");

  // Module D: Handedness
  const [handednessData, setHandednessData] = useState<HandednessMatrixResponse | null>(null);

  // Module E: Variations
  const [variationsData, setVariationsData] = useState<DeliveryStylesResponse | null>(null);
  const [variationMinBalls, setVariationMinBalls] = useState<number>(50);
  const [variationSortKey, setVariationSortKey] = useState<
    "economy_rate" | "deliveries_bowled" | "wickets" | "dot_ball_pct"
  >("economy_rate");

  // Module F: Speed Profiles
  const [speedData, setSpeedData] = useState<SpeedProfileResponse | null>(null);

  // Module G: Player Dossier
  const [selectedPlayerId, setSelectedPlayerId] = useState<number>(2258); // Default: Sanju Samson
  const [playerProfile, setPlayerProfile] = useState<PlayerTacticalProfileResponse | null>(null);
  const [playerSearchQuery, setPlayerSearchQuery] = useState<string>("");
  const [playerSearchResults, setPlayerSearchResults] = useState<PlayerLookupItem[]>([]);
  const [isSearchingPlayer, setIsSearchingPlayer] = useState<boolean>(false);

  // Module H: Death Overs
  const [deathDiscipline, setDeathDiscipline] = useState<"all" | "batting" | "bowling">("all");
  const [deathMinBalls, setDeathMinBalls] = useState<number>(100);
  const [deathOversData, setDeathOversData] = useState<DeathOversRankingResponse | null>(null);

  // Module I: Head to Head
  const [h2hStrikerId, setH2hStrikerId] = useState<number>(47); // Virat Kohli
  const [h2hBowlerId, setH2hBowlerId] = useState<number>(4722); // Rashid Khan
  const [h2hData, setH2hData] = useState<HeadToHeadMatchupResponse | null>(null);
  const [h2hLoading, setH2hLoading] = useState<boolean>(false);

  // 1. Initial Load of Core Tactical Datasets
  const loadTacticalBase = async () => {
    setLoading(true);
    setErrorMsg(null);
    try {
      const [sumRes, phaseRes, strokeRes, handRes, varRes, spdRes, deathRes] = await Promise.all([
        fetchTacticalSummary(),
        fetchTacticalPhases(),
        fetchTacticalStrokes({ min_balls: strokeMinBalls }),
        fetchTacticalHandedness(),
        fetchTacticalVariations({ min_balls: variationMinBalls }),
        fetchTacticalSpeedProfiles({ min_balls: 30, top_n: 10 }),
        fetchTacticalDeathOvers({ discipline: deathDiscipline, min_balls: deathMinBalls, limit: 10 }),
      ]);

      if (sumRes) setSummary(sumRes);
      if (phaseRes) setPhasesData(phaseRes);
      if (strokeRes) setStrokesData(strokeRes);
      if (handRes) setHandednessData(handRes);
      if (varRes) setVariationsData(varRes);
      if (spdRes) setSpeedData(spdRes);
      if (deathRes) setDeathOversData(deathRes);

      if (!sumRes && !phaseRes) {
        setErrorMsg("Tactical Intelligence backend service offline or in standby. Ensure backend is running on port 8000.");
      }
    } catch (err: any) {
      setErrorMsg(err.message || "Failed to communicate with Tactical Intelligence backend services.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadTacticalBase();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // 2. Load Player Tactical Profile when selected
  useEffect(() => {
    let isCurrent = true;
    async function loadPlayerDossier() {
      if (!selectedPlayerId) return;
      try {
        const dossier = await fetchPlayerTacticalProfile(selectedPlayerId);
        if (isCurrent && dossier) {
          setPlayerProfile(dossier);
        }
      } catch (err) {
        if (isCurrent) {
          console.warn(`Could not load tactical profile for player ${selectedPlayerId}:`, err);
        }
      }
    }
    loadPlayerDossier();
    return () => {
      isCurrent = false;
    };
  }, [selectedPlayerId]);

  // 3. Load Head to Head Matchup
  useEffect(() => {
    let isCurrent = true;
    async function loadH2H() {
      if (!h2hStrikerId || !h2hBowlerId) return;
      setH2hLoading(true);
      try {
        const matchRes = await fetchTacticalMatchup(h2hStrikerId, h2hBowlerId);
        if (isCurrent && matchRes) {
          setH2hData(matchRes);
        }
      } catch (err) {
        if (isCurrent) {
          console.warn("Could not load head-to-head matchup:", err);
          setH2hData(null);
        }
      } finally {
        if (isCurrent) setH2hLoading(false);
      }
    }
    loadH2H();
    return () => {
      isCurrent = false;
    };
  }, [h2hStrikerId, h2hBowlerId]);

  // 4. Update Death Overs Rankings on Filter Changes
  useEffect(() => {
    let isCurrent = true;
    async function reloadDeathOvers() {
      try {
        const deathRes = await fetchTacticalDeathOvers({
          discipline: deathDiscipline,
          min_balls: deathMinBalls,
          limit: 10,
        });
        if (isCurrent && deathRes) setDeathOversData(deathRes);
      } catch (err) {
        if (isCurrent) console.warn("Could not reload death overs rankings:", err);
      }
    }
    reloadDeathOvers();
    return () => {
      isCurrent = false;
    };
  }, [deathDiscipline, deathMinBalls]);

  // 5. Update Strokes on Min Balls Change
  useEffect(() => {
    let isCurrent = true;
    async function reloadStrokes() {
      try {
        const strokeRes = await fetchTacticalStrokes({ min_balls: strokeMinBalls });
        if (isCurrent && strokeRes) setStrokesData(strokeRes);
      } catch (err) {
        if (isCurrent) console.warn("Could not reload strokes:", err);
      }
    }
    reloadStrokes();
    return () => {
      isCurrent = false;
    };
  }, [strokeMinBalls]);

  // 6. Update Variations on Min Balls Change
  useEffect(() => {
    let isCurrent = true;
    async function reloadVariations() {
      try {
        const varRes = await fetchTacticalVariations({ min_balls: variationMinBalls });
        if (isCurrent && varRes) setVariationsData(varRes);
      } catch (err) {
        if (isCurrent) console.warn("Could not reload variations:", err);
      }
    }
    reloadVariations();
    return () => {
      isCurrent = false;
    };
  }, [variationMinBalls]);

  // 7. Interactive Player Search
  const handlePlayerSearch = async (query: string) => {
    setPlayerSearchQuery(query);
    if (query.trim().length < 2) {
      setPlayerSearchResults([]);
      return;
    }
    setIsSearchingPlayer(true);
    const results = await fetchTacticalPlayers(query, 12);
    setPlayerSearchResults(results);
    setIsSearchingPlayer(false);
  };

  // Sorted Strokes
  const sortedStrokes = useMemo(() => {
    if (!strokesData?.strokes) return [];
    return [...strokesData.strokes].sort((a, b) => {
      if (strokeSortKey === "runs_per_shot") return b.runs_per_shot - a.runs_per_shot;
      if (strokeSortKey === "deliveries_faced") return b.deliveries_faced - a.deliveries_faced;
      if (strokeSortKey === "boundary_pct") return b.boundary_pct - a.boundary_pct;
      if (strokeSortKey === "dismissal_rate_pct") return a.dismissal_rate_pct - b.dismissal_rate_pct;
      return 0;
    });
  }, [strokesData, strokeSortKey]);

  // Sorted Variations
  const sortedVariations = useMemo(() => {
    if (!variationsData?.styles) return [];
    return [...variationsData.styles].sort((a, b) => {
      if (variationSortKey === "economy_rate") return a.economy_rate - b.economy_rate;
      if (variationSortKey === "deliveries_bowled") return b.deliveries_bowled - a.deliveries_bowled;
      if (variationSortKey === "wickets") return b.wickets - a.wickets;
      if (variationSortKey === "dot_ball_pct") return b.dot_ball_pct - a.dot_ball_pct;
      return 0;
    });
  }, [variationsData, variationSortKey]);

  return (
    <div className="space-y-8 pb-12">
      {/* ------------------------------------------------------------------- */}
      {/* 1. Editorial Header & Tactical Command Context */}
      {/* ------------------------------------------------------------------- */}
      <section className="space-y-3">
        <div className="flex flex-wrap items-center gap-3 text-xs">
          <span className="font-mono font-bold tracking-widest text-[#E91E8C] uppercase">
            Rajasthan Royals Analytics
          </span>
          <span className="text-slate-300">•</span>
          <span className="font-mono text-slate-500">
            Official Data Pack • 200,999 Balls
          </span>
          <span className="text-slate-300">•</span>
          <span className="inline-flex items-center gap-1.5 text-emerald-700 font-medium">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
            Phase & Telemetry Engine
          </span>
        </div>

        <div className="flex flex-col md:flex-row md:items-end justify-between gap-4">
          <div className="max-w-3xl space-y-2">
            <h1 className="text-3xl md:text-4xl font-extrabold tracking-tight text-slate-900 leading-tight">
              Tactical Cricket Intelligence
            </h1>
            <p className="text-sm md:text-base text-slate-600 leading-relaxed font-normal">
              Official Rajasthan Royals Data Pack • Phase Splits • Micro-Battles • Speed Telemetry.
              867 active matches analyzed with 16 zero-delivery fixtures reconciled.
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-3 shrink-0">
            <Link
              href="/pressure"
              className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-[#111C38] text-white text-xs font-semibold hover:bg-[#1A2B50] transition-colors shadow-sm"
            >
              <Shield size={14} className="text-[#E91E8C]" />
              <span>Pressure Leaderboards</span>
              <ArrowRight size={13} className="text-slate-400" />
            </Link>
          </div>
        </div>
      </section>

      {/* Connection Alert Banner (if backend unreachable) */}
      {errorMsg && (
        <div className="p-4 rounded-xl bg-amber-50 border border-amber-200 text-amber-900 flex items-center justify-between gap-4 shadow-2xs">
          <div className="flex items-center gap-3">
            <AlertTriangle className="w-5 h-5 text-amber-600 shrink-0" />
            <div>
              <div className="text-xs font-bold">Backend Connection Notice</div>
              <div className="text-xs text-amber-800 mt-0.5">{errorMsg}</div>
            </div>
          </div>
          <button
            onClick={loadTacticalBase}
            className="px-3 py-1.5 rounded-lg bg-amber-600 text-white font-bold text-xs hover:bg-amber-700 transition-colors shrink-0 flex items-center gap-1.5"
          >
            <RefreshCw className="w-3.5 h-3.5" />
            <span>Retry</span>
          </button>
        </div>
      )}

      {/* ------------------------------------------------------------------- */}
      {/* 2. Open Editorial Telemetry Strip (Inline Metric Groups) */}
      {/* ------------------------------------------------------------------- */}
      <section className="py-5 border-y border-slate-200/80">
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6 md:gap-4">
          <div className="space-y-1">
            <span className="text-[10px] font-mono uppercase tracking-wider text-slate-500 font-semibold block">
              Total Deliveries
            </span>
            <div className="text-2xl md:text-3xl font-extrabold text-[#111827] font-mono tracking-tight flex items-baseline gap-1.5">
              <span>{summary ? summary.total_deliveries.toLocaleString() : "—"}</span>
              <span className="w-1.5 h-1.5 rounded-full bg-[#E91E8C]" />
            </div>
            <p className="text-[11px] text-slate-500 truncate">
              {summary ? `${summary.legal_deliveries.toLocaleString()} legal deliveries` : "—"}
            </p>
          </div>

          <div className="space-y-1">
            <span className="text-[10px] font-mono uppercase tracking-wider text-slate-500 font-semibold block">
              Matches Covered
            </span>
            <div className="text-2xl md:text-3xl font-extrabold text-[#111827] font-mono tracking-tight">
              {summary ? summary.total_matches_with_deliveries : "—"}
            </div>
            <p className="text-[11px] text-slate-500 truncate">
              {summary ? "Matches with deliveries indexed" : "—"}
            </p>
          </div>

          <div className="space-y-1">
            <span className="text-[10px] font-mono uppercase tracking-wider text-slate-500 font-semibold block">
              Runs Off Bat
            </span>
            <div className="text-2xl md:text-3xl font-extrabold text-[#111827] font-mono tracking-tight">
              {summary ? summary.total_runs_off_bat.toLocaleString() : "—"}
            </div>
            <p className="text-[11px] text-slate-500 truncate">
              Run rate: {summary ? `${summary.overall_run_rate_per_6_balls.toFixed(2)} rpo` : "—"}
            </p>
          </div>

          <div className="space-y-1">
            <span className="text-[10px] font-mono uppercase tracking-wider text-slate-500 font-semibold block">
              Total Wickets
            </span>
            <div className="text-2xl md:text-3xl font-extrabold text-[#111827] font-mono tracking-tight">
              {summary ? summary.total_wickets_fallen.toLocaleString() : "—"}
            </div>
            <p className="text-[11px] text-slate-500 truncate">
              {summary ? `${summary.total_bowler_wickets.toLocaleString()} bowler wickets` : "—"}
            </p>
          </div>

          <div className="space-y-1">
            <span className="text-[10px] font-mono uppercase tracking-wider text-slate-500 font-semibold block">
              Active Players
            </span>
            <div className="text-2xl md:text-3xl font-extrabold text-[#111827] font-mono tracking-tight">
              {summary ? `${summary.total_unique_strikers} / ${summary.total_unique_bowlers}` : "—"}
            </div>
            <p className="text-[11px] text-slate-500 truncate">
              Batters / Bowlers mapped
            </p>
          </div>

          <div className="space-y-1">
            <span className="text-[10px] font-mono uppercase tracking-wider text-slate-500 font-semibold block">
              Radar Speeds
            </span>
            <div className="text-2xl md:text-3xl font-extrabold text-[#111827] font-mono tracking-tight">
              {summary ? summary.valid_radar_speed_records.toLocaleString() : "—"}
            </div>
            <p className="text-[11px] text-emerald-700 font-medium truncate">
              {summary ? `${((summary.valid_radar_speed_records / summary.total_deliveries) * 100).toFixed(1)}% sensor coverage` : "—"}
            </p>
          </div>
        </div>
      </section>

      {/* ------------------------------------------------------------------- */}
      {/* 3. Tactical Sub-System Navigation Tabs (Refined Pink Underline) */}
      {/* ------------------------------------------------------------------- */}
      <div className="border-b border-slate-200">
        <div className="flex items-center gap-6 overflow-x-auto">
          <button
            onClick={() => setActiveTab("overview")}
            className={cn(
              "flex items-center gap-2 py-3 text-xs font-semibold transition-all border-b-2 -mb-px whitespace-nowrap",
              activeTab === "overview"
                ? "border-[#E91E8C] text-[#E91E8C] font-bold"
                : "border-transparent text-slate-500 hover:text-slate-800"
            )}
          >
            <BarChart2 className={cn("w-4 h-4", activeTab === "overview" ? "text-[#E91E8C]" : "text-slate-400")} />
            <span>Phase Mastery & Splits</span>
          </button>

          <button
            onClick={() => setActiveTab("strokes_handedness")}
            className={cn(
              "flex items-center gap-2 py-3 text-xs font-semibold transition-all border-b-2 -mb-px whitespace-nowrap",
              activeTab === "strokes_handedness"
                ? "border-[#E91E8C] text-[#E91E8C] font-bold"
                : "border-transparent text-slate-500 hover:text-slate-800"
            )}
          >
            <Target className={cn("w-4 h-4", activeTab === "strokes_handedness" ? "text-[#E91E8C]" : "text-slate-400")} />
            <span>Strokes & Handedness</span>
          </button>

          <button
            onClick={() => setActiveTab("bowling_speed")}
            className={cn(
              "flex items-center gap-2 py-3 text-xs font-semibold transition-all border-b-2 -mb-px whitespace-nowrap",
              activeTab === "bowling_speed"
                ? "border-[#E91E8C] text-[#E91E8C] font-bold"
                : "border-transparent text-slate-500 hover:text-slate-800"
            )}
          >
            <Gauge className={cn("w-4 h-4", activeTab === "bowling_speed" ? "text-[#E91E8C]" : "text-slate-400")} />
            <span>Variations & Radar Speed</span>
          </button>

          <button
            onClick={() => setActiveTab("death_overs")}
            className={cn(
              "flex items-center gap-2 py-3 text-xs font-semibold transition-all border-b-2 -mb-px whitespace-nowrap",
              activeTab === "death_overs"
                ? "border-[#E91E8C] text-[#E91E8C] font-bold"
                : "border-transparent text-slate-500 hover:text-slate-800"
            )}
          >
            <Flame className={cn("w-4 h-4", activeTab === "death_overs" ? "text-[#E91E8C]" : "text-slate-400")} />
            <span>Death Overs Finishers</span>
          </button>

          <button
            onClick={() => setActiveTab("matchups_players")}
            className={cn(
              "flex items-center gap-2 py-3 text-xs font-semibold transition-all border-b-2 -mb-px whitespace-nowrap",
              activeTab === "matchups_players"
                ? "border-[#E91E8C] text-[#E91E8C] font-bold"
                : "border-transparent text-slate-500 hover:text-slate-800"
            )}
          >
            <Swords className={cn("w-4 h-4", activeTab === "matchups_players" ? "text-[#E91E8C]" : "text-slate-400")} />
            <span>Matchup Battles & Dossiers</span>
          </button>
        </div>
      </div>

      {/* ------------------------------------------------------------------- */}
      {/* TAB 1: PHASE MASTERY (MODULE B) */}
      {/* ------------------------------------------------------------------- */}
      {activeTab === "overview" && (
        <div className="space-y-6">
          <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 p-5 rounded-xl bg-white border border-slate-200/80 shadow-2xs">
            <div>
              <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
                <BarChart2 className="w-5 h-5 text-[#E91E8C]" />
                Tournament Match Phase Architecture
              </h2>
              <p className="text-xs text-slate-500 mt-0.5">
                Governed breakdown: Powerplay (Overs 1–6), Middle Overs (Overs 7–15), Death Overs (Overs 16–20)
              </p>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-xs text-slate-500 font-medium">Tournament Phase Baseline:</span>
              <span className="text-xs font-mono font-bold px-2.5 py-1 rounded-md bg-slate-100 text-slate-800 border border-slate-200">
                All 867 Matches
              </span>
            </div>
          </div>

          {/* Phase Cards Grid (Refined Light Theme) */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* Powerplay Card */}
            <div className="p-6 rounded-xl bg-white border border-slate-200/80 shadow-2xs hover:shadow-sm hover:border-[#E91E8C]/40 transition-all flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between mb-4">
                  <span className="text-xs font-mono font-bold px-2.5 py-0.5 rounded bg-pink-50 text-pink-700 border border-pink-200">
                    Overs 1 – 6
                  </span>
                  <span className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider font-mono">
                    Phase 1
                  </span>
                </div>
                <h3 className="text-2xl font-bold text-slate-900 mb-1.5">Powerplay</h3>
                <p className="text-xs text-slate-600 mb-6 leading-relaxed">
                  Field restrictions active (2 fielders outside 30-yard circle). High new-ball swing period.
                </p>

                <div className="space-y-3 text-xs">
                  <div className="flex items-center justify-between pb-2 border-b border-slate-100">
                    <span className="text-slate-500">Strike Rate / Economy</span>
                    <span className="text-slate-900 font-bold font-mono">
                      {phasesData?.phases["Powerplay"]?.strike_rate?.toFixed(1) ?? "125.7"} / {phasesData?.phases["Powerplay"]?.economy_rate?.toFixed(2) ?? "7.54"}
                    </span>
                  </div>
                  <div className="flex items-center justify-between pb-2 border-b border-slate-100">
                    <span className="text-slate-500">Boundary Frequency</span>
                    <span className="text-emerald-700 font-bold font-mono">
                      {phasesData?.phases["Powerplay"]?.boundary_percentage?.toFixed(1) ?? "18.2"}%
                    </span>
                  </div>
                  <div className="flex items-center justify-between pb-2 border-b border-slate-100">
                    <span className="text-slate-500">Dot Ball Percentage</span>
                    <span className="text-amber-700 font-bold font-mono">
                      {phasesData?.phases["Powerplay"]?.dot_ball_percentage?.toFixed(1) ?? "46.8"}%
                    </span>
                  </div>
                  <div className="flex items-center justify-between pb-2 border-b border-slate-100">
                    <span className="text-slate-500">Bowling Average</span>
                    <span className="text-slate-800 font-bold font-mono">
                      {phasesData?.phases["Powerplay"]?.average?.toFixed(1) ?? "31.4"} runs/wkt
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-slate-500">Balls Per Wicket</span>
                    <span className="text-slate-800 font-bold font-mono">
                      {phasesData?.phases["Powerplay"]?.balls_per_wicket?.toFixed(1) ?? "25.0"} balls
                    </span>
                  </div>
                </div>
              </div>
            </div>

            {/* Middle Overs Card */}
            <div className="p-6 rounded-xl bg-white border border-slate-200/80 shadow-2xs hover:shadow-sm hover:border-[#D6B56D]/60 transition-all flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between mb-4">
                  <span className="text-xs font-mono font-bold px-2.5 py-0.5 rounded bg-amber-50 text-amber-800 border border-amber-200">
                    Overs 7 – 15
                  </span>
                  <span className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider font-mono">
                    Phase 2
                  </span>
                </div>
                <h3 className="text-2xl font-bold text-slate-900 mb-1.5">Middle Overs</h3>
                <p className="text-xs text-slate-600 mb-6 leading-relaxed">
                  Spin strangle, strike rotation, boundary containment, and wicket-taking through pressure accumulation.
                </p>

                <div className="space-y-3 text-xs">
                  <div className="flex items-center justify-between pb-2 border-b border-slate-100">
                    <span className="text-slate-500">Strike Rate / Economy</span>
                    <span className="text-slate-900 font-bold font-mono">
                      {phasesData?.phases["Middle"]?.strike_rate?.toFixed(1) ?? "130.5"} / {phasesData?.phases["Middle"]?.economy_rate?.toFixed(2) ?? "7.83"}
                    </span>
                  </div>
                  <div className="flex items-center justify-between pb-2 border-b border-slate-100">
                    <span className="text-slate-500">Boundary Frequency</span>
                    <span className="text-emerald-700 font-bold font-mono">
                      {phasesData?.phases["Middle"]?.boundary_percentage?.toFixed(1) ?? "13.9"}%
                    </span>
                  </div>
                  <div className="flex items-center justify-between pb-2 border-b border-slate-100">
                    <span className="text-slate-500">Dot Ball Percentage</span>
                    <span className="text-amber-700 font-bold font-mono">
                      {phasesData?.phases["Middle"]?.dot_ball_percentage?.toFixed(1) ?? "34.2"}%
                    </span>
                  </div>
                  <div className="flex items-center justify-between pb-2 border-b border-slate-100">
                    <span className="text-slate-500">Bowling Average</span>
                    <span className="text-slate-800 font-bold font-mono">
                      {phasesData?.phases["Middle"]?.average?.toFixed(1) ?? "27.6"} runs/wkt
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-slate-500">Balls Per Wicket</span>
                    <span className="text-slate-800 font-bold font-mono">
                      {phasesData?.phases["Middle"]?.balls_per_wicket?.toFixed(1) ?? "21.1"} balls
                    </span>
                  </div>
                </div>
              </div>
            </div>

            {/* Death Overs Card */}
            <div className="p-6 rounded-xl bg-white border border-slate-200/80 shadow-2xs hover:shadow-sm hover:border-rose-300 transition-all flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between mb-4">
                  <span className="text-xs font-mono font-bold px-2.5 py-0.5 rounded bg-rose-50 text-rose-700 border border-rose-200">
                    Overs 16 – 20
                  </span>
                  <span className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider font-mono">
                    Phase 3
                  </span>
                </div>
                <h3 className="text-2xl font-bold text-slate-900 mb-1.5">Death Overs</h3>
                <p className="text-xs text-slate-600 mb-6 leading-relaxed">
                  Maximum aggression, boundary hunting, pinpoint yorkers, wide cutters, high pressure execution.
                </p>

                <div className="space-y-3 text-xs">
                  <div className="flex items-center justify-between pb-2 border-b border-slate-100">
                    <span className="text-slate-500">Strike Rate / Economy</span>
                    <span className="text-slate-900 font-bold font-mono">
                      {phasesData?.phases["Death"]?.strike_rate?.toFixed(1) ?? "168.1"} / {phasesData?.phases["Death"]?.economy_rate?.toFixed(2) ?? "10.09"}
                    </span>
                  </div>
                  <div className="flex items-center justify-between pb-2 border-b border-slate-100">
                    <span className="text-slate-500">Boundary Frequency</span>
                    <span className="text-emerald-700 font-bold font-mono">
                      {phasesData?.phases["Death"]?.boundary_percentage?.toFixed(1) ?? "20.8"}%
                    </span>
                  </div>
                  <div className="flex items-center justify-between pb-2 border-b border-slate-100">
                    <span className="text-slate-500">Dot Ball Percentage</span>
                    <span className="text-amber-700 font-bold font-mono">
                      {phasesData?.phases["Death"]?.dot_ball_percentage?.toFixed(1) ?? "28.5"}%
                    </span>
                  </div>
                  <div className="flex items-center justify-between pb-2 border-b border-slate-100">
                    <span className="text-slate-500">Bowling Average</span>
                    <span className="text-slate-800 font-bold font-mono">
                      {phasesData?.phases["Death"]?.average?.toFixed(1) ?? "16.9"} runs/wkt
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-slate-500">Balls Per Wicket</span>
                    <span className="text-slate-800 font-bold font-mono">
                      {phasesData?.phases["Death"]?.balls_per_wicket?.toFixed(1) ?? "10.1"} balls
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Tactical Takeaways Box */}
          <div className="p-5 rounded-xl bg-white border border-slate-200/80 shadow-2xs flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
            <div className="flex items-center gap-3">
              <div className="p-2.5 rounded-lg bg-pink-50 text-[#E91E8C] border border-pink-100">
                <Sparkles className="w-5 h-5" />
              </div>
              <div>
                <h4 className="text-sm font-bold text-slate-900">Tactical Phase Intelligence Insight</h4>
                <p className="text-xs text-slate-600 mt-0.5">
                  Death overs economy climbs to <strong className="text-slate-900">10.09 rpo</strong> with boundary frequency at <strong className="text-emerald-700">20.8%</strong>, while bowling strike rate drops dramatically to a wicket every <strong className="text-slate-900">10.1 balls</strong>.
                </p>
              </div>
            </div>
            <button
              onClick={() => setActiveTab("death_overs")}
              className="px-4 py-2 rounded-lg bg-[#111C38] hover:bg-[#1A2B50] text-xs font-semibold text-white flex items-center gap-1.5 whitespace-nowrap transition-colors shadow-2xs"
            >
              <span>Explore Death Specialists</span>
              <ChevronRight className="w-3.5 h-3.5 text-[#D6B56D]" />
            </button>
          </div>
        </div>
      )}

      {/* ------------------------------------------------------------------- */}
      {/* TAB 2: STROKES & HANDEDNESS (MODULES C & D) */}
      {/* ------------------------------------------------------------------- */}
      {activeTab === "strokes_handedness" && (
        <div className="space-y-8">
          {/* Module C: Shot Stroke Efficiency */}
          <div className="space-y-4">
            <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 p-5 rounded-xl bg-white border border-slate-200/80 shadow-2xs">
              <div>
                <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
                  <Target className="w-5 h-5 text-[#E91E8C]" />
                  Batting Stroke Efficiency & Dismissal Threat (30 Strokes)
                </h2>
                <p className="text-xs text-slate-500 mt-0.5">
                  Empirical productivity across all stroke types recorded in official Rajasthan Royals telemetry.
                </p>
              </div>

              {/* Filters for Stroke Table */}
              <div className="flex flex-wrap items-center gap-3">
                <div className="flex items-center gap-2">
                  <span className="text-xs text-slate-500">Min Balls:</span>
                  <select
                    value={strokeMinBalls}
                    onChange={(e) => setStrokeMinBalls(Number(e.target.value))}
                    className="bg-slate-50 text-slate-800 text-xs font-mono border border-slate-200 rounded-lg px-2.5 py-1.5 focus:outline-none focus:border-[#E91E8C]"
                  >
                    <option value={20}>20+ Balls</option>
                    <option value={50}>50+ Balls</option>
                    <option value={100}>100+ Balls</option>
                    <option value={250}>250+ Balls</option>
                    <option value={500}>500+ Balls</option>
                  </select>
                </div>

                <div className="flex items-center gap-2">
                  <span className="text-xs text-slate-500">Sort By:</span>
                  <select
                    value={strokeSortKey}
                    onChange={(e) => setStrokeSortKey(e.target.value as any)}
                    className="bg-slate-50 text-slate-800 text-xs font-mono border border-slate-200 rounded-lg px-2.5 py-1.5 focus:outline-none focus:border-[#E91E8C]"
                  >
                    <option value="runs_per_shot">Runs / Shot (Highest)</option>
                    <option value="deliveries_faced">Sample Volume (Balls)</option>
                    <option value="boundary_pct">Boundary % (Highest)</option>
                    <option value="dismissal_rate_pct">Dismissal Risk (Safest)</option>
                  </select>
                </div>
              </div>
            </div>

            {/* Stroke Table (Clean Light Theme) */}
            <div className="rounded-xl border border-slate-200/80 overflow-hidden bg-white shadow-2xs">
              <div className="overflow-x-auto max-h-[460px]">
                <table className="w-full text-left text-xs">
                  <thead className="bg-slate-50 text-slate-600 font-mono uppercase text-[10px] tracking-wider sticky top-0 border-b border-slate-200 z-10">
                    <tr>
                      <th className="px-4 py-3 font-sans">Stroke Category</th>
                      <th className="px-4 py-3 text-right">Balls Faced</th>
                      <th className="px-4 py-3 text-right">Runs Scored</th>
                      <th className="px-4 py-3 text-right">Runs / Shot</th>
                      <th className="px-4 py-3 text-right">Boundary %</th>
                      <th className="px-4 py-3 text-right">Dismissals</th>
                      <th className="px-4 py-3 text-right">Dismissal Risk %</th>
                      <th className="px-4 py-3 text-center font-sans">Tactical Profile</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100 font-mono">
                    {sortedStrokes.map((stroke, idx) => {
                      const isHighYield = stroke.runs_per_shot >= 1.5;
                      const isHighRisk = stroke.dismissal_rate_pct >= 6.0;
                      return (
                        <tr key={idx} className="hover:bg-slate-50/70 transition-colors">
                          <td className="px-4 py-3 font-semibold text-slate-900 font-sans flex items-center gap-2">
                            <span className="w-1.5 h-1.5 rounded-full bg-[#E91E8C]" />
                            {stroke.stroke}
                          </td>
                          <td className="px-4 py-3 text-right text-slate-600">
                            {stroke.deliveries_faced.toLocaleString()}
                          </td>
                          <td className="px-4 py-3 text-right text-slate-900 font-bold">
                            {stroke.runs_scored.toLocaleString()}
                          </td>
                          <td className="px-4 py-3 text-right">
                            <span className={cn(
                              "font-bold",
                              isHighYield ? "text-emerald-700" : "text-slate-700"
                            )}>
                              {stroke.runs_per_shot.toFixed(2)}
                            </span>
                          </td>
                          <td className="px-4 py-3 text-right text-emerald-700 font-semibold">
                            {stroke.boundary_pct.toFixed(1)}%
                          </td>
                          <td className="px-4 py-3 text-right text-slate-600">
                            {stroke.dismissals}
                          </td>
                          <td className="px-4 py-3 text-right">
                            <span className={cn(
                              "font-bold",
                              isHighRisk ? "text-rose-700" : "text-slate-600"
                            )}>
                              {stroke.dismissal_rate_pct.toFixed(2)}%
                            </span>
                          </td>
                          <td className="px-4 py-3 text-center font-sans">
                            {isHighYield && !isHighRisk && (
                              <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200">
                                High Yield / Safe
                              </span>
                            )}
                            {isHighYield && isHighRisk && (
                              <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-amber-50 text-amber-800 border border-amber-200">
                                High Risk / High Reward
                              </span>
                            )}
                            {!isHighYield && isHighRisk && (
                              <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-rose-50 text-rose-700 border border-rose-200">
                                High Hazard
                              </span>
                            )}
                            {!isHighYield && !isHighRisk && (
                              <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-slate-100 text-slate-700 border border-slate-200">
                                Control / Accumulation
                              </span>
                            )}
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          {/* Module D: Handedness Matchup Matrix */}
          <div className="space-y-4">
            <div className="p-5 rounded-xl bg-white border border-slate-200/80 shadow-2xs">
              <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
                <Swords className="w-5 h-5 text-[#D6B56D]" />
                Batter Handedness vs Bowling Discipline Matrix (4-Way Cross-Split)
              </h2>
              <p className="text-xs text-slate-500 mt-0.5">
                Comparative micro-tactics: Right-Hand Batters (RHB) and Left-Hand Batters (LHB) facing Pace and Spin.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              {handednessData?.matrix.map((split, idx) => {
                const isLHB = split.batting_type === "LHB";
                const isSpin = split.pace_or_spin === "Spin";
                return (
                  <div
                    key={idx}
                    className="p-5 rounded-xl bg-white border border-slate-200/80 shadow-2xs hover:shadow-sm hover:border-slate-300 transition-all flex flex-col justify-between"
                  >
                    <div>
                      <div className="flex items-center justify-between mb-3">
                        <span className={cn(
                          "text-xs font-mono font-bold px-2.5 py-0.5 rounded border",
                          isLHB
                            ? "bg-pink-50 text-pink-700 border-pink-200"
                            : "bg-amber-50 text-amber-800 border-amber-200"
                        )}>
                          {split.batting_type}
                        </span>
                        <span className={cn(
                          "text-xs font-mono font-bold px-2.5 py-0.5 rounded border",
                          isSpin
                            ? "bg-purple-50 text-purple-700 border-purple-200"
                            : "bg-blue-50 text-blue-700 border-blue-200"
                        )}>
                          vs {split.pace_or_spin}
                        </span>
                      </div>

                      <h4 className="text-base font-bold text-slate-900 mb-4">
                        {split.batting_type} vs {split.pace_or_spin}
                      </h4>

                      <div className="space-y-2.5 font-mono text-xs">
                        <div className="flex justify-between pb-1.5 border-b border-slate-100">
                          <span className="text-slate-500">Balls Faced:</span>
                          <span className="text-slate-900 font-bold">{split.balls_faced.toLocaleString()}</span>
                        </div>
                        <div className="flex justify-between pb-1.5 border-b border-slate-100">
                          <span className="text-slate-500">Strike Rate:</span>
                          <span className="text-emerald-700 font-bold">{split.strike_rate.toFixed(1)}</span>
                        </div>
                        <div className="flex justify-between pb-1.5 border-b border-slate-100">
                          <span className="text-slate-500">Economy Conceded:</span>
                          <span className="text-amber-700 font-bold">{split.economy_rate.toFixed(2)}</span>
                        </div>
                        <div className="flex justify-between pb-1.5 border-b border-slate-100">
                          <span className="text-slate-500">Bowling Average:</span>
                          <span className="text-slate-800 font-bold">{split.bowling_average ? split.bowling_average.toFixed(1) : "N/A"}</span>
                        </div>
                        <div className="flex justify-between pb-1.5 border-b border-slate-100">
                          <span className="text-slate-500">Dot Ball %:</span>
                          <span className="text-slate-700 font-bold">{split.dot_pct.toFixed(1)}%</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-slate-500">Boundary %:</span>
                          <span className="text-emerald-700 font-bold">{split.boundary_pct.toFixed(1)}%</span>
                        </div>
                      </div>
                    </div>

                    <div className="mt-4 pt-3 border-t border-slate-100 text-[11px] text-slate-500 italic">
                      {isLHB && isSpin && "Key matchup: Spin economy vs LHB is critical for RR wrist-spin tactics."}
                      {isLHB && !isSpin && "Pace targeting LHB with incoming swing and short-pitch angles."}
                      {!isLHB && isSpin && "Traditional wrist-spin vs RHB contest with high dot percentage."}
                      {!isLHB && !isSpin && "Baseline matchup volume representing highest delivery frequency."}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      )}

      {/* ------------------------------------------------------------------- */}
      {/* TAB 3: VARIATIONS & RADAR SPEED (MODULES E & F) */}
      {/* ------------------------------------------------------------------- */}
      {activeTab === "bowling_speed" && (
        <div className="space-y-8">
          {/* Module F: Radar Velocity & Sensor Safeguards (Prominent on Top) */}
          <div className="space-y-4">
            <div className="p-5 rounded-xl bg-white border border-slate-200/80 shadow-2xs flex flex-col lg:flex-row items-start lg:items-center justify-between gap-4">
              <div>
                <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
                  <Gauge className="w-5 h-5 text-amber-600" />
                  Bowling Radar Telemetry & Speed Profiles
                </h2>
                <p className="text-xs text-slate-500 mt-0.5">
                  Radar release velocity with automated domain safeguards and physical boundary filters.
                </p>
              </div>

              {/* Sensor Disclaimer Pill */}
              <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs font-mono">
                <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                <span>Sensor Safeguard Active: Scaling & Outlier Clipping</span>
              </div>
            </div>

            {/* Sensor Calibration Safeguard Notice Banner */}
            <div className="p-4 rounded-xl bg-amber-50/70 border border-amber-200/80 shadow-2xs flex items-start gap-3">
              <AlertTriangle className="w-5 h-5 text-amber-600 shrink-0 mt-0.5" />
              <div className="text-xs text-amber-900 leading-relaxed">
                <strong className="text-amber-950 font-semibold block mb-0.5">Sensor Safeguard & Quality Verification:</strong>
                Raw radar release speed is recorded on <strong className="text-slate-900">123,113 deliveries (61.3% coverage)</strong>. Governed scaling divides erroneous 10x multiplier values (<span className="font-mono text-amber-800 font-bold">speed &ge; 500.0</span>) by 10 (e.g. 1456.1 &rarr; 145.61 km/h). Extreme anomalous outliers (<span className="font-mono text-amber-800 font-bold">&lt; 50.0</span> or <span className="font-mono text-amber-800 font-bold">&gt; 170.0 km/h</span>) are strictly filtered out to prevent skewing velocity distributions.
              </div>
            </div>

            {/* Velocity Brackets (Clean Cards) */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="p-4 rounded-xl bg-white border border-slate-200/80 shadow-2xs">
                <span className="text-[10px] font-semibold text-slate-500 uppercase tracking-wider block mb-1">
                  Slow / Spin (&lt; 110 km/h)
                </span>
                <span className="text-2xl font-bold font-mono text-purple-700">
                  {speedData?.speed_brackets?.slow_under_110.toLocaleString() ?? "43,303"}
                </span>
                <span className="text-[11px] text-slate-500 block mt-1">Spinners & off-pace cutters</span>
              </div>

              <div className="p-4 rounded-xl bg-white border border-slate-200/80 shadow-2xs">
                <span className="text-[10px] font-semibold text-slate-500 uppercase tracking-wider block mb-1">
                  Medium (110 – 125 km/h)
                </span>
                <span className="text-2xl font-bold font-mono text-blue-700">
                  {speedData?.speed_brackets?.medium_110_to_125.toLocaleString() ?? "15,832"}
                </span>
                <span className="text-[11px] text-slate-500 block mt-1">Military medium & fast spin</span>
              </div>

              <div className="p-4 rounded-xl bg-white border border-slate-200/80 shadow-2xs">
                <span className="text-[10px] font-semibold text-slate-500 uppercase tracking-wider block mb-1">
                  Fast-Medium (125 – 140 km/h)
                </span>
                <span className="text-2xl font-bold font-mono text-cyan-700">
                  {speedData?.speed_brackets?.fast_medium_125_to_140.toLocaleString() ?? "54,233"}
                </span>
                <span className="text-[11px] text-slate-500 block mt-1">Modern seam bowling core</span>
              </div>

              <div className="p-4 rounded-xl bg-white border border-slate-200/80 shadow-2xs">
                <span className="text-[10px] font-semibold text-slate-500 uppercase tracking-wider block mb-1">
                  Express Pace (&gt; 140 km/h)
                </span>
                <span className="text-2xl font-bold font-mono text-rose-700">
                  {speedData?.speed_brackets?.express_over_140.toLocaleString() ?? "9,745"}
                </span>
                <span className="text-[11px] text-rose-600 block mt-1">Elite express velocity</span>
              </div>
            </div>

            {/* Fastest Bowlers Table */}
            <div className="rounded-xl border border-slate-200/80 overflow-hidden bg-white shadow-2xs">
              <div className="p-4 border-b border-slate-200 flex items-center justify-between bg-slate-50/70">
                <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
                  <Flame className="w-4 h-4 text-rose-600" />
                  Top 10 Fastest Bowlers by Mean Release Velocity
                </h3>
                <span className="text-xs font-mono text-slate-500">Min 30 Valid Deliveries</span>
              </div>
              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs font-mono">
                  <thead className="bg-slate-50 text-slate-600 uppercase text-[10px] tracking-wider border-b border-slate-200">
                    <tr>
                      <th className="px-4 py-3 font-sans">Rank & Bowler</th>
                      <th className="px-4 py-3 text-right">Valid Radar Balls</th>
                      <th className="px-4 py-3 text-right">Mean Speed (km/h)</th>
                      <th className="px-4 py-3 text-right">Peak Speed (km/h)</th>
                      <th className="px-4 py-3 text-right">Balls &gt; 140 km/h</th>
                      <th className="px-4 py-3 text-center font-sans">RR Roster Match</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {speedData?.top_fastest_bowlers?.map((bowler, idx) => {
                      const isRR = [2320, 4489].includes(bowler.bowler_id);
                      return (
                        <tr key={idx} className="hover:bg-slate-50/70 transition-colors">
                          <td className="px-4 py-3 font-sans font-semibold text-slate-900 flex items-center gap-2.5">
                            <span className={cn(
                              "w-5 h-5 rounded-full flex items-center justify-center text-[10px] font-mono font-bold",
                              idx === 0 ? "bg-amber-100 text-amber-900 border border-amber-300" : "bg-slate-100 text-slate-700"
                            )}>
                              {idx + 1}
                            </span>
                            {bowler.bowler_name}
                          </td>
                          <td className="px-4 py-3 text-right text-slate-600">
                            {bowler.valid_deliveries.toLocaleString()}
                          </td>
                          <td className="px-4 py-3 text-right font-bold text-rose-700 text-sm">
                            {bowler.mean_speed_kmh.toFixed(1)}
                          </td>
                          <td className="px-4 py-3 text-right font-bold text-slate-900">
                            {bowler.max_speed_kmh.toFixed(1)}
                          </td>
                          <td className="px-4 py-3 text-right text-slate-700">
                            {bowler.express_balls_count}
                          </td>
                          <td className="px-4 py-3 text-center font-sans">
                            {isRR ? (
                              <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-pink-50 text-[#E91E8C] border border-pink-200">
                                Royals Bowler
                              </span>
                            ) : (
                              <span className="text-[10px] text-slate-400 font-mono">Opponent</span>
                            )}
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          {/* Module E: Bowling Variation Styles */}
          <div className="space-y-4">
            <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 p-5 rounded-xl bg-white border border-slate-200/80 shadow-2xs">
              <div>
                <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
                  <Layers className="w-5 h-5 text-[#E91E8C]" />
                  Bowling Variations & Delivery Styles (34 Styles)
                </h2>
                <p className="text-xs text-slate-500 mt-0.5">
                  Seam movements, spin variations, bouncers, yorkers, and knuckleballs profiled for containment & threat.
                </p>
              </div>

              {/* Filters for Variations */}
              <div className="flex flex-wrap items-center gap-3">
                <div className="flex items-center gap-2">
                  <span className="text-xs text-slate-500">Min Deliveries:</span>
                  <select
                    value={variationMinBalls}
                    onChange={(e) => setVariationMinBalls(Number(e.target.value))}
                    className="bg-slate-50 text-slate-800 text-xs font-mono border border-slate-200 rounded-lg px-2.5 py-1.5 focus:outline-none focus:border-[#E91E8C]"
                  >
                    <option value={20}>20+ Balls</option>
                    <option value={50}>50+ Balls</option>
                    <option value={100}>100+ Balls</option>
                    <option value={250}>250+ Balls</option>
                  </select>
                </div>

                <div className="flex items-center gap-2">
                  <span className="text-xs text-slate-500">Sort By:</span>
                  <select
                    value={variationSortKey}
                    onChange={(e) => setVariationSortKey(e.target.value as any)}
                    className="bg-slate-50 text-slate-800 text-xs font-mono border border-slate-200 rounded-lg px-2.5 py-1.5 focus:outline-none focus:border-[#E91E8C]"
                  >
                    <option value="economy_rate">Economy Rate (Most Economical)</option>
                    <option value="wickets">Wickets (Most Threatening)</option>
                    <option value="dot_ball_pct">Dot Ball % (Highest)</option>
                    <option value="deliveries_bowled">Sample Size (Volume)</option>
                  </select>
                </div>
              </div>
            </div>

            {/* Variations Table */}
            <div className="rounded-xl border border-slate-200/80 overflow-hidden bg-white shadow-2xs">
              <div className="overflow-x-auto max-h-[460px]">
                <table className="w-full text-left text-xs font-mono">
                  <thead className="bg-slate-50 text-slate-600 uppercase text-[10px] tracking-wider sticky top-0 border-b border-slate-200 z-10">
                    <tr>
                      <th className="px-4 py-3 font-sans">Delivery Style</th>
                      <th className="px-4 py-3 text-right">Balls Bowled</th>
                      <th className="px-4 py-3 text-right">Runs Conceded</th>
                      <th className="px-4 py-3 text-right">Wickets</th>
                      <th className="px-4 py-3 text-right">Economy Rate</th>
                      <th className="px-4 py-3 text-right">Bowling Avg</th>
                      <th className="px-4 py-3 text-right">Dot Ball %</th>
                      <th className="px-4 py-3 text-center font-sans">Discipline Class</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {sortedVariations.map((style, idx) => {
                      const isContainment = style.economy_rate <= 7.5;
                      const isHighThreat = style.wickets >= 50;
                      return (
                        <tr key={idx} className="hover:bg-slate-50/70 transition-colors">
                          <td className="px-4 py-3 font-sans font-semibold text-slate-900 flex items-center gap-2">
                            <span className="w-1.5 h-1.5 rounded-full bg-[#D6B56D]" />
                            {style.delivery_style}
                          </td>
                          <td className="px-4 py-3 text-right text-slate-600">
                            {style.deliveries_bowled.toLocaleString()}
                          </td>
                          <td className="px-4 py-3 text-right text-slate-600">
                            {style.runs_conceded.toLocaleString()}
                          </td>
                          <td className="px-4 py-3 text-right text-slate-900 font-bold">
                            {style.wickets}
                          </td>
                          <td className="px-4 py-3 text-right">
                            <span className={cn(
                              "font-bold",
                              isContainment ? "text-emerald-700" : "text-amber-800"
                            )}>
                              {style.economy_rate.toFixed(2)}
                            </span>
                          </td>
                          <td className="px-4 py-3 text-right text-slate-600">
                            {style.bowling_average ? style.bowling_average.toFixed(1) : "N/A"}
                          </td>
                          <td className="px-4 py-3 text-right text-cyan-700 font-semibold">
                            {style.dot_ball_pct.toFixed(1)}%
                          </td>
                          <td className="px-4 py-3 text-center font-sans">
                            {isContainment && isHighThreat && (
                              <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200">
                                Gold Standard
                              </span>
                            )}
                            {isContainment && !isHighThreat && (
                              <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-blue-50 text-blue-700 border border-blue-200">
                                Containment Weapon
                              </span>
                            )}
                            {!isContainment && isHighThreat && (
                              <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-rose-50 text-rose-700 border border-rose-200">
                                Wicket Hunter
                              </span>
                            )}
                            {!isContainment && !isHighThreat && (
                              <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-slate-100 text-slate-700 border border-slate-200">
                                Baseline Utility
                              </span>
                            )}
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* ------------------------------------------------------------------- */}
      {/* TAB 4: DEATH OVERS (MODULE H) */}
      {/* ------------------------------------------------------------------- */}
      {activeTab === "death_overs" && (
        <div className="space-y-6">
          <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 p-5 rounded-xl bg-white border border-slate-200/80 shadow-2xs">
            <div>
              <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
                <Flame className="w-5 h-5 text-rose-600" />
                Death Overs Mastery (Overs 16–20)
              </h2>
              <p className="text-xs text-slate-500 mt-0.5">
                Elite finishers ranked by strike rate and boundary execution; elite containment bowlers ranked by economy.
              </p>
            </div>

            {/* Discipline Selector */}
            <div className="flex flex-wrap items-center gap-3">
              <div className="flex items-center rounded-lg bg-slate-100 border border-slate-200 p-0.5">
                <button
                  onClick={() => setDeathDiscipline("all")}
                  className={cn(
                    "px-3 py-1 rounded-md text-xs font-semibold transition-all",
                    deathDiscipline === "all" ? "bg-white text-slate-900 shadow-2xs font-bold" : "text-slate-600 hover:text-slate-900"
                  )}
                >
                  Dual View
                </button>
                <button
                  onClick={() => setDeathDiscipline("batting")}
                  className={cn(
                    "px-3 py-1 rounded-md text-xs font-semibold transition-all",
                    deathDiscipline === "batting" ? "bg-white text-slate-900 shadow-2xs font-bold" : "text-slate-600 hover:text-slate-900"
                  )}
                >
                  Finishers (Batting)
                </button>
                <button
                  onClick={() => setDeathDiscipline("bowling")}
                  className={cn(
                    "px-3 py-1 rounded-md text-xs font-semibold transition-all",
                    deathDiscipline === "bowling" ? "bg-white text-slate-900 shadow-2xs font-bold" : "text-slate-600 hover:text-slate-900"
                  )}
                >
                  Containment (Bowling)
                </button>
              </div>

              <div className="flex items-center gap-2">
                <span className="text-xs text-slate-500">Min Balls:</span>
                <select
                  value={deathMinBalls}
                  onChange={(e) => setDeathMinBalls(Number(e.target.value))}
                  className="bg-slate-50 text-slate-800 text-xs font-mono border border-slate-200 rounded-lg px-2.5 py-1 focus:outline-none focus:border-[#E91E8C]"
                >
                  <option value={50}>50+ Balls</option>
                  <option value={100}>100+ Balls (Standard)</option>
                  <option value={150}>150+ Balls</option>
                </select>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Batting Finishers Leaderboard */}
            {(deathDiscipline === "all" || deathDiscipline === "batting") && (
              <div className="rounded-xl border border-slate-200/80 overflow-hidden bg-white shadow-2xs flex flex-col justify-between">
                <div>
                  <div className="p-4 border-b border-slate-200 flex items-center justify-between bg-slate-50/70">
                    <div className="flex items-center gap-2">
                      <TrendingUp className="w-4 h-4 text-emerald-700" />
                      <h3 className="text-sm font-bold text-slate-900">Elite Death Finishers (Strike Rate)</h3>
                    </div>
                    <span className="text-[11px] font-mono text-slate-500 font-semibold">Overs 16–20</span>
                  </div>
                  <div className="overflow-x-auto">
                    <table className="w-full text-left text-xs font-mono">
                      <thead className="bg-slate-50 text-slate-600 uppercase text-[10px] tracking-wider border-b border-slate-200">
                        <tr>
                          <th className="px-4 py-3 font-sans">Rank & Batter</th>
                          <th className="px-4 py-3 text-right">Runs</th>
                          <th className="px-4 py-3 text-right">Balls</th>
                          <th className="px-4 py-3 text-right">4s / 6s</th>
                          <th className="px-4 py-3 text-right">Strike Rate</th>
                          <th className="px-4 py-3 text-right">Boundary %</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-slate-100">
                        {deathOversData?.batting_finishers?.map((batter, idx) => (
                          <tr key={idx} className="hover:bg-slate-50/70 transition-colors">
                            <td className="px-4 py-3 font-sans font-semibold text-slate-900 flex items-center gap-2.5">
                              <span className={cn(
                                "w-5 h-5 rounded-full flex items-center justify-center text-[10px] font-mono font-bold",
                                idx === 0 ? "bg-amber-100 text-amber-900 border border-amber-300" : "bg-slate-100 text-slate-700"
                              )}>
                                {idx + 1}
                              </span>
                              {batter.striker_name}
                            </td>
                            <td className="px-4 py-3 text-right text-slate-900 font-bold">{batter.runs}</td>
                            <td className="px-4 py-3 text-right text-slate-600">{batter.balls}</td>
                            <td className="px-4 py-3 text-right text-slate-600">{batter.fours} / {batter.sixes}</td>
                            <td className="px-4 py-3 text-right font-bold text-emerald-700 text-sm">
                              {batter.strike_rate.toFixed(1)}
                            </td>
                            <td className="px-4 py-3 text-right text-slate-800">{batter.boundary_pct.toFixed(1)}%</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            )}

            {/* Bowling Containment Leaderboard */}
            {(deathDiscipline === "all" || deathDiscipline === "bowling") && (
              <div className="rounded-xl border border-slate-200/80 overflow-hidden bg-white shadow-2xs flex flex-col justify-between">
                <div>
                  <div className="p-4 border-b border-slate-200 flex items-center justify-between bg-slate-50/70">
                    <div className="flex items-center gap-2">
                      <Shield className="w-4 h-4 text-cyan-700" />
                      <h3 className="text-sm font-bold text-slate-900">Elite Death Bowlers (Containment Economy)</h3>
                    </div>
                    <span className="text-[11px] font-mono text-slate-500 font-semibold">Overs 16–20</span>
                  </div>
                  <div className="overflow-x-auto">
                    <table className="w-full text-left text-xs font-mono">
                      <thead className="bg-slate-50 text-slate-600 uppercase text-[10px] tracking-wider border-b border-slate-200">
                        <tr>
                          <th className="px-4 py-3 font-sans">Rank & Bowler</th>
                          <th className="px-4 py-3 text-right">Legal Balls</th>
                          <th className="px-4 py-3 text-right">Runs</th>
                          <th className="px-4 py-3 text-right">Wickets</th>
                          <th className="px-4 py-3 text-right">Economy</th>
                          <th className="px-4 py-3 text-right">Dot Ball %</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-slate-100">
                        {deathOversData?.bowling_containment?.map((bowler, idx) => (
                          <tr key={idx} className="hover:bg-slate-50/70 transition-colors">
                            <td className="px-4 py-3 font-sans font-semibold text-slate-900 flex items-center gap-2.5">
                              <span className={cn(
                                "w-5 h-5 rounded-full flex items-center justify-center text-[10px] font-mono font-bold",
                                idx === 0 ? "bg-cyan-100 text-cyan-900 border border-cyan-300" : "bg-slate-100 text-slate-700"
                              )}>
                                {idx + 1}
                              </span>
                              <div>
                                <div>{bowler.bowler_name}</div>
                                <div className="text-[10px] font-mono text-slate-500">{bowler.bowling_type}</div>
                              </div>
                            </td>
                            <td className="px-4 py-3 text-right text-slate-600">{bowler.legal_balls}</td>
                            <td className="px-4 py-3 text-right text-slate-600">{bowler.runs}</td>
                            <td className="px-4 py-3 text-right text-slate-900 font-bold">{bowler.wickets}</td>
                            <td className="px-4 py-3 text-right font-bold text-cyan-700 text-sm">
                              {bowler.economy.toFixed(2)}
                            </td>
                            <td className="px-4 py-3 text-right text-slate-800">{bowler.dot_pct.toFixed(1)}%</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* ------------------------------------------------------------------- */}
      {/* TAB 5: MATCHUPS & PLAYER DOSSIERS (MODULES G & I) */}
      {/* ------------------------------------------------------------------- */}
      {activeTab === "matchups_players" && (
        <div className="space-y-8">
          {/* Module I: Direct Head-to-Head Micro-Battles */}
          <div className="space-y-4">
            <div className="p-5 rounded-xl bg-white border border-slate-200/80 shadow-2xs flex flex-col lg:flex-row items-start lg:items-center justify-between gap-4">
              <div>
                <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
                  <Swords className="w-5 h-5 text-[#E91E8C]" />
                  Direct Head-to-Head Micro-Battle Explorer
                </h2>
                <p className="text-xs text-slate-500 mt-0.5">
                  Empirical head-to-head records across all official deliveries between a striker and bowler.
                </p>
              </div>

              {/* Quick Preset Buttons */}
              <div className="flex flex-wrap items-center gap-2">
                <span className="text-xs text-slate-500 font-medium">Presets:</span>
                {PRESET_MATCHUPS.map((preset, idx) => (
                  <button
                    key={idx}
                    onClick={() => {
                      setH2hStrikerId(preset.strikerId);
                      setH2hBowlerId(preset.bowlerId);
                    }}
                    className={cn(
                      "px-2.5 py-1 rounded-md text-xs font-semibold border transition-all",
                      h2hStrikerId === preset.strikerId && h2hBowlerId === preset.bowlerId
                        ? "bg-[#111C38] text-white border-[#111C38] shadow-2xs"
                        : "bg-slate-50 text-slate-700 border-slate-200 hover:bg-slate-100"
                    )}
                  >
                    {preset.label}
                  </button>
                ))}
              </div>
            </div>

            {/* Micro-Battle Visual Result Card (Clean Enterprise Surface) */}
            <div className="p-6 rounded-xl bg-white border border-slate-200/80 shadow-2xs">
              {h2hLoading ? (
                <div className="flex items-center justify-center py-12 text-slate-500 text-xs font-mono">
                  <RefreshCw className="w-5 h-5 animate-spin text-[#E91E8C] mr-2" />
                  Extracting empirical micro-battle records...
                </div>
              ) : h2hData ? (
                <div className="space-y-6">
                  {/* Versus Banner */}
                  <div className="flex flex-col md:flex-row items-center justify-between gap-6 pb-6 border-b border-slate-100">
                    {/* Striker side */}
                    <div className="flex items-center gap-4 text-left w-full md:w-auto">
                      <div className="w-12 h-12 rounded-xl bg-pink-50 border border-pink-200 flex items-center justify-center text-[#E91E8C] font-bold text-sm">
                        BAT
                      </div>
                      <div>
                        <span className="text-[10px] font-mono text-[#E91E8C] uppercase tracking-wider font-bold">Striker (Batter)</span>
                        <h3 className="text-xl font-bold text-slate-900">{h2hData.striker_name}</h3>
                        <span className="text-xs text-slate-500 font-mono">ID: {h2hData.striker_id}</span>
                      </div>
                    </div>

                    {/* VS Badge */}
                    <div className="flex flex-col items-center justify-center">
                      <span className="px-3 py-1 rounded-full bg-slate-100 text-slate-800 border border-slate-200 font-mono font-bold text-xs">
                        VS
                      </span>
                      <span className="text-[11px] text-slate-500 mt-1 font-mono">
                        {h2hData.balls_faced} balls faced
                      </span>
                    </div>

                    {/* Bowler side */}
                    <div className="flex items-center gap-4 text-right justify-end w-full md:w-auto">
                      <div>
                        <span className="text-[10px] font-mono text-cyan-700 uppercase tracking-wider font-bold">Opponent Bowler</span>
                        <h3 className="text-xl font-bold text-slate-900">{h2hData.bowler_name}</h3>
                        <span className="text-xs text-slate-500 font-mono">ID: {h2hData.bowler_id}</span>
                      </div>
                      <div className="w-12 h-12 rounded-xl bg-cyan-50 border border-cyan-200 flex items-center justify-center text-cyan-700 font-bold text-sm">
                        BWL
                      </div>
                    </div>
                  </div>

                  {/* Micro-Battle Stats Grid */}
                  <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-3 text-center">
                    <div className="p-3 rounded-lg bg-slate-50 border border-slate-200/60">
                      <span className="text-[10px] text-slate-500 uppercase tracking-wider block">Balls</span>
                      <span className="text-lg font-mono font-bold text-slate-900">{h2hData.balls_faced}</span>
                    </div>
                    <div className="p-3 rounded-lg bg-slate-50 border border-slate-200/60">
                      <span className="text-[10px] text-slate-500 uppercase tracking-wider block">Runs Scored</span>
                      <span className="text-lg font-mono font-bold text-emerald-700">{h2hData.runs_scored}</span>
                    </div>
                    <div className="p-3 rounded-lg bg-slate-50 border border-slate-200/60">
                      <span className="text-[10px] text-slate-500 uppercase tracking-wider block">Dismissals</span>
                      <span className={cn(
                        "text-lg font-mono font-bold",
                        h2hData.dismissals > 0 ? "text-rose-700" : "text-slate-700"
                      )}>
                        {h2hData.dismissals}
                      </span>
                    </div>
                    <div className="p-3 rounded-lg bg-slate-50 border border-slate-200/60">
                      <span className="text-[10px] text-slate-500 uppercase tracking-wider block">Strike Rate</span>
                      <span className="text-lg font-mono font-bold text-slate-900">{h2hData.strike_rate.toFixed(1)}</span>
                    </div>
                    <div className="p-3 rounded-lg bg-slate-50 border border-slate-200/60">
                      <span className="text-[10px] text-slate-500 uppercase tracking-wider block">4s / 6s</span>
                      <span className="text-lg font-mono font-bold text-slate-800">{h2hData.fours} / {h2hData.sixes}</span>
                    </div>
                    <div className="p-3 rounded-lg bg-slate-50 border border-slate-200/60">
                      <span className="text-[10px] text-slate-500 uppercase tracking-wider block">Dot Ball %</span>
                      <span className="text-lg font-mono font-bold text-amber-700">{h2hData.dot_ball_pct.toFixed(1)}%</span>
                    </div>
                    <div className="p-3 rounded-lg bg-slate-50 border border-slate-200/60">
                      <span className="text-[10px] text-slate-500 uppercase tracking-wider block">Boundary %</span>
                      <span className="text-lg font-mono font-bold text-emerald-700">{h2hData.boundary_pct.toFixed(1)}%</span>
                    </div>
                  </div>

                  {/* Tactical Verdict Pill */}
                  <div className="p-4 rounded-xl bg-slate-50 border border-slate-200/80 flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <Sparkles className="w-4 h-4 text-[#D6B56D]" />
                      <span className="text-xs font-semibold text-slate-800">Micro-Battle Verdict:</span>
                    </div>
                    <div className="text-xs font-mono font-bold">
                      {h2hData.balls_faced === 0 && (
                        <span className="text-slate-500">Zero Direct Deliveries Recorded in Dataset</span>
                      )}
                      {h2hData.balls_faced > 0 && h2hData.dismissals >= 2 && (
                        <span className="text-rose-700 font-bold">Bowler Dominant — Multiple Dismissals</span>
                      )}
                      {h2hData.balls_faced > 0 && h2hData.dismissals === 0 && h2hData.strike_rate >= 140 && (
                        <span className="text-emerald-700 font-bold">Batter Dominant — Unbeaten High Strike Rate</span>
                      )}
                      {h2hData.balls_faced > 0 && !(h2hData.dismissals >= 2) && !(h2hData.dismissals === 0 && h2hData.strike_rate >= 140) && (
                        <span className="text-amber-800 font-bold">Balanced Contest — Tactical Execution Required</span>
                      )}
                    </div>
                  </div>
                </div>
              ) : null}
            </div>
          </div>

          {/* Module G: Individual Player Multi-Dimensional Tactical Profile */}
          <div className="space-y-4">
            <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 p-5 rounded-xl bg-white border border-slate-200/80 shadow-2xs">
              <div>
                <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
                  <Users className="w-5 h-5 text-[#D6B56D]" />
                  Multi-Dimensional Player Tactical Dossier (Module G)
                </h2>
                <p className="text-xs text-slate-500 mt-0.5">
                  Comprehensive tactical profile: Phase performance, top strokes, variations, and radar speed.
                </p>
              </div>

              {/* Interactive Player Search & Select */}
              <div className="relative w-full md:w-72">
                <div className="relative">
                  <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
                  <input
                    type="text"
                    placeholder="Search player name..."
                    value={playerSearchQuery}
                    onChange={(e) => handlePlayerSearch(e.target.value)}
                    className="w-full bg-slate-50 text-slate-900 text-xs pl-9 pr-4 py-2 rounded-lg border border-slate-200 focus:outline-none focus:border-[#E91E8C] focus:bg-white transition-colors"
                  />
                </div>

                {/* Autocomplete Dropdown */}
                {playerSearchResults.length > 0 && (
                  <div className="absolute top-full left-0 right-0 mt-1 max-h-56 overflow-y-auto bg-white border border-slate-200 rounded-xl shadow-lg z-20 divide-y divide-slate-100">
                    {playerSearchResults.map((p) => (
                      <button
                        key={p.player_id}
                        onClick={() => {
                          setSelectedPlayerId(p.player_id);
                          setPlayerSearchQuery("");
                          setPlayerSearchResults([]);
                        }}
                        className="w-full px-3.5 py-2 text-left text-xs text-slate-800 hover:bg-slate-50 transition-colors flex items-center justify-between"
                      >
                        <span className="font-semibold text-slate-900">{p.player_name}</span>
                        <div className="flex items-center gap-1.5 text-[10px] font-mono text-slate-500">
                          {p.is_batter && <span className="text-[#E91E8C] font-bold">BAT</span>}
                          {p.is_bowler && <span className="text-cyan-700 font-bold">BWL</span>}
                        </div>
                      </button>
                    ))}
                  </div>
                )}
              </div>
            </div>

            {/* Quick Marquee Selection Pills */}
            <div className="flex flex-wrap items-center gap-2">
              <span className="text-xs text-slate-500 font-medium">Quick Select:</span>
              {MARQUEE_PLAYERS.map((player) => (
                <button
                  key={player.id}
                  onClick={() => setSelectedPlayerId(player.id)}
                  className={cn(
                    "px-3 py-1 rounded-lg text-xs font-semibold border transition-all flex items-center gap-1.5",
                    selectedPlayerId === player.id
                      ? "bg-[#111C38] text-white border-[#111C38] shadow-2xs font-bold"
                      : "bg-white text-slate-700 border-slate-200 hover:bg-slate-50"
                  )}
                >
                  <span>{player.name}</span>
                  <span className="text-[10px] font-mono opacity-70">({player.team})</span>
                </button>
              ))}
            </div>

            {/* Selected Player Dossier Card */}
            {playerProfile && (
              <div className="p-6 rounded-xl bg-white border border-slate-200/80 shadow-2xs space-y-6">
                {/* Dossier Header */}
                <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 pb-4 border-b border-slate-100">
                  <div className="flex items-center gap-3">
                    <div className="w-12 h-12 rounded-xl bg-slate-100 border border-slate-200 flex items-center justify-center font-bold text-sm text-slate-900 font-mono">
                      {playerProfile.player_name.substring(0, 2).toUpperCase()}
                    </div>
                    <div>
                      <h3 className="text-xl font-bold text-slate-900 flex items-center gap-2">
                        {playerProfile.player_name}
                        <span className="text-xs font-mono text-slate-400 font-normal">ID: {playerProfile.player_id}</span>
                      </h3>
                      <div className="flex items-center gap-2 mt-0.5">
                        {playerProfile.is_batter && (
                          <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded bg-pink-50 text-[#E91E8C] border border-pink-200">
                            Batter Profile Active
                          </span>
                        )}
                        {playerProfile.is_bowler && (
                          <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded bg-cyan-50 text-cyan-800 border border-cyan-200">
                            Bowler Profile Active
                          </span>
                        )}
                      </div>
                    </div>
                  </div>
                </div>

                {/* Batting Section (If Batter) */}
                {playerProfile.batting_profile && (
                  <div className="space-y-4">
                    <h4 className="text-sm font-bold text-slate-900 flex items-center gap-2">
                      <TrendingUp className="w-4 h-4 text-[#E91E8C]" />
                      Batting Diagnostics & Phase Splits
                    </h4>

                    {/* Batting Overall Stats */}
                    <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
                      <div className="p-3 rounded-lg bg-slate-50 border border-slate-200/60">
                        <span className="text-[10px] text-slate-500 uppercase block">Total Runs</span>
                        <span className="text-lg font-mono font-bold text-slate-900">{playerProfile.batting_profile.total_runs.toLocaleString()}</span>
                      </div>
                      <div className="p-3 rounded-lg bg-slate-50 border border-slate-200/60">
                        <span className="text-[10px] text-slate-500 uppercase block">Balls Faced</span>
                        <span className="text-lg font-mono font-bold text-slate-700">{playerProfile.batting_profile.balls_faced.toLocaleString()}</span>
                      </div>
                      <div className="p-3 rounded-lg bg-slate-50 border border-slate-200/60">
                        <span className="text-[10px] text-slate-500 uppercase block">Strike Rate</span>
                        <span className="text-lg font-mono font-bold text-emerald-700">{playerProfile.batting_profile.strike_rate.toFixed(1)}</span>
                      </div>
                      <div className="p-3 rounded-lg bg-slate-50 border border-slate-200/60">
                        <span className="text-[10px] text-slate-500 uppercase block">Boundary %</span>
                        <span className="text-lg font-mono font-bold text-emerald-700">{playerProfile.batting_profile.boundary_pct.toFixed(1)}%</span>
                      </div>
                      <div className="p-3 rounded-lg bg-slate-50 border border-slate-200/60">
                        <span className="text-[10px] text-slate-500 uppercase block">Dot Ball %</span>
                        <span className="text-lg font-mono font-bold text-amber-700">{playerProfile.batting_profile.dot_ball_pct.toFixed(1)}%</span>
                      </div>
                    </div>

                    {/* Batting Phase Breakdown Cards */}
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                      {["Powerplay", "Middle", "Death"].map((phaseName) => {
                        const phase = playerProfile.batting_profile?.phase_splits[phaseName];
                        return (
                          <div key={phaseName} className="p-3.5 rounded-lg bg-slate-50/70 border border-slate-200/70">
                            <div className="flex items-center justify-between mb-2">
                              <span className="text-xs font-bold text-slate-900">{phaseName}</span>
                              <span className="text-[10px] font-mono text-slate-500">{phase?.total_balls ?? 0} balls</span>
                            </div>
                            <div className="font-mono text-xs space-y-1">
                              <div className="flex justify-between">
                                <span className="text-slate-500">SR:</span>
                                <span className="text-slate-900 font-bold">{phase?.strike_rate ? phase.strike_rate.toFixed(1) : "N/A"}</span>
                              </div>
                              <div className="flex justify-between">
                                <span className="text-slate-500">Runs:</span>
                                <span className="text-slate-800">{phase?.runs ?? 0}</span>
                              </div>
                              <div className="flex justify-between">
                                <span className="text-slate-500">Dismissals:</span>
                                <span className="text-rose-700 font-bold">{phase?.wickets ?? 0}</span>
                              </div>
                            </div>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                )}

                {/* Bowling Section (If Bowler) */}
                {playerProfile.bowling_profile && (
                  <div className="space-y-4 pt-4 border-t border-slate-100">
                    <h4 className="text-sm font-bold text-slate-900 flex items-center gap-2">
                      <Target className="w-4 h-4 text-cyan-700" />
                      Bowling Mechanics & Variations
                    </h4>

                    {/* Bowling Overall Stats */}
                    <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
                      <div className="p-3 rounded-lg bg-slate-50 border border-slate-200/60">
                        <span className="text-[10px] text-slate-500 uppercase block">Total Wickets</span>
                        <span className="text-lg font-mono font-bold text-slate-900">{playerProfile.bowling_profile.total_wickets}</span>
                      </div>
                      <div className="p-3 rounded-lg bg-slate-50 border border-slate-200/60">
                        <span className="text-[10px] text-slate-500 uppercase block">Legal Balls</span>
                        <span className="text-lg font-mono font-bold text-slate-700">{playerProfile.bowling_profile.legal_balls.toLocaleString()}</span>
                      </div>
                      <div className="p-3 rounded-lg bg-slate-50 border border-slate-200/60">
                        <span className="text-[10px] text-slate-500 uppercase block">Economy Rate</span>
                        <span className="text-lg font-mono font-bold text-cyan-700">{playerProfile.bowling_profile.economy_rate.toFixed(2)}</span>
                      </div>
                      <div className="p-3 rounded-lg bg-slate-50 border border-slate-200/60">
                        <span className="text-[10px] text-slate-500 uppercase block">Bowling Average</span>
                        <span className="text-lg font-mono font-bold text-slate-800">{playerProfile.bowling_profile.bowling_average ? playerProfile.bowling_profile.bowling_average.toFixed(1) : "N/A"}</span>
                      </div>
                      <div className="p-3 rounded-lg bg-slate-50 border border-slate-200/60">
                        <span className="text-[10px] text-slate-500 uppercase block">Dot Ball %</span>
                        <span className="text-lg font-mono font-bold text-amber-700">{playerProfile.bowling_profile.dot_ball_pct.toFixed(1)}%</span>
                      </div>
                    </div>

                    {/* Speed Telemetry if Available */}
                    {playerProfile.bowling_profile.speed_profile.mean_speed_kmh && (
                      <div className="p-3.5 rounded-lg bg-cyan-50/60 border border-cyan-200 flex items-center justify-between text-xs font-mono">
                        <div className="flex items-center gap-2">
                          <Gauge className="w-4 h-4 text-cyan-700" />
                          <span className="text-slate-600">Mean Radar Release Speed:</span>
                          <span className="text-cyan-800 font-bold">{playerProfile.bowling_profile.speed_profile.mean_speed_kmh.toFixed(1)} km/h</span>
                        </div>
                        <div className="flex items-center gap-2">
                          <span className="text-slate-500">Peak Velocity:</span>
                          <span className="text-amber-800 font-bold">{playerProfile.bowling_profile.speed_profile.max_speed_kmh?.toFixed(1) ?? "N/A"} km/h</span>
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
