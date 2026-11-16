"use client";

import React, { useState, useEffect, useMemo } from "react";
import Link from "next/link";
import {
  TacticalDatasetSummaryResponse,
  TacticalPhaseResponse,
  TacticalPhaseSplitItem,
  TacticalStrokesResponse,
  TacticalStrokeItem,
  HandednessMatrixResponse,
  HandednessSplitItem,
  DeliveryStylesResponse,
  DeliveryStyleItem,
  SpeedProfileResponse,
  FastestBowlerItem,
  PlayerTacticalProfileResponse,
  DeathOversRankingResponse,
  DeathOverPerformerBattingItem,
  DeathOverPerformerBowlingItem,
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
  Activity,
  Zap,
  Target,
  Shield,
  Crosshair,
  TrendingUp,
  BarChart2,
  Flame,
  Gauge,
  Users,
  Award,
  Search,
  ChevronRight,
  Filter,
  ArrowUpRight,
  ArrowRight,
  CheckCircle2,
  AlertTriangle,
  Info,
  RefreshCw,
  Sparkles,
  Swords,
  ChevronDown,
  Layers,
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
  const [phaseFilterPlayerId, setPhaseFilterPlayerId] = useState<number | null>(null);
  const [phaseFilterRole, setPhaseFilterRole] = useState<"overall" | "batter" | "bowler">("overall");

  // Module C: Strokes
  const [strokesData, setStrokesData] = useState<TacticalStrokesResponse | null>(null);
  const [strokeMinBalls, setStrokeMinBalls] = useState<number>(50);
  const [strokeSortKey, setStrokeSortKey] = useState<"runs_per_shot" | "deliveries_faced" | "boundary_pct" | "dismissal_rate_pct">("runs_per_shot");

  // Module D: Handedness
  const [handednessData, setHandednessData] = useState<HandednessMatrixResponse | null>(null);

  // Module E: Variations
  const [variationsData, setVariationsData] = useState<DeliveryStylesResponse | null>(null);
  const [variationMinBalls, setVariationMinBalls] = useState<number>(50);
  const [variationSortKey, setVariationSortKey] = useState<"economy_rate" | "deliveries_bowled" | "wickets" | "dot_ball_pct">("economy_rate");

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
  useEffect(() => {
    async function loadTacticalBase() {
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
      } catch (err: any) {
        setErrorMsg("Failed to communicate with Tactical Intelligence backend services.");
      } finally {
        setLoading(false);
      }
    }

    loadTacticalBase();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // 2. Load Player Tactical Profile when selected
  useEffect(() => {
    async function loadPlayerDossier() {
      if (!selectedPlayerId) return;
      const dossier = await fetchPlayerTacticalProfile(selectedPlayerId);
      if (dossier) {
        setPlayerProfile(dossier);
      }
    }
    loadPlayerDossier();
  }, [selectedPlayerId]);

  // 3. Load Head to Head Matchup
  useEffect(() => {
    async function loadH2H() {
      if (!h2hStrikerId || !h2hBowlerId) return;
      setH2hLoading(true);
      const matchRes = await fetchTacticalMatchup(h2hStrikerId, h2hBowlerId);
      if (matchRes) {
        setH2hData(matchRes);
      }
      setH2hLoading(false);
    }
    loadH2H();
  }, [h2hStrikerId, h2hBowlerId]);

  // 4. Update Death Overs Rankings on Filter Changes
  useEffect(() => {
    async function reloadDeathOvers() {
      const deathRes = await fetchTacticalDeathOvers({
        discipline: deathDiscipline,
        min_balls: deathMinBalls,
        limit: 10,
      });
      if (deathRes) setDeathOversData(deathRes);
    }
    reloadDeathOvers();
  }, [deathDiscipline, deathMinBalls]);

  // 5. Update Strokes on Min Balls Change
  useEffect(() => {
    async function reloadStrokes() {
      const strokeRes = await fetchTacticalStrokes({ min_balls: strokeMinBalls });
      if (strokeRes) setStrokesData(strokeRes);
    }
    reloadStrokes();
  }, [strokeMinBalls]);

  // 6. Update Variations on Min Balls Change
  useEffect(() => {
    async function reloadVariations() {
      const varRes = await fetchTacticalVariations({ min_balls: variationMinBalls });
      if (varRes) setVariationsData(varRes);
    }
    reloadVariations();
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
    <div className="min-h-screen bg-[#0B132B] text-slate-100 p-6 md:p-8 space-y-8">
      {/* ------------------------------------------------------------------- */}
      {/* Header Banner & Tactical Command Context */}
      {/* ------------------------------------------------------------------- */}
      <div className="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-4 pb-6 border-b border-[#1A2B50]">
        <div>
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-[#E91E8F] to-[#D6B56D] p-0.5 shadow-lg flex items-center justify-center">
              <div className="w-full h-full bg-[#101C37] rounded-[10px] flex items-center justify-center">
                <Crosshair className="w-5 h-5 text-[#E91E8F]" />
              </div>
            </div>
            <div>
              <h1 className="text-2xl font-bold tracking-tight text-white flex items-center gap-3">
                Tactical Cricket Intelligence
                <span className="text-xs font-mono font-bold px-2 py-0.5 rounded-full bg-[#E91E8F]/20 text-[#E91E8F] border border-[#E91E8F]/30">
                  Stage 5 Live
                </span>
              </h1>
              <p className="text-xs text-slate-400 mt-0.5">
                Official Rajasthan Royals Data Pack • Phase Splits • Micro-Battles • Speed Telemetry
              </p>
            </div>
          </div>
        </div>

        {/* Global Metadata Badges & Cross-Navigation */}
        <div className="flex flex-wrap items-center gap-2">
          <Link
            href="/pressure"
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-[#E91E8F] text-white hover:bg-[#E91E8F]/90 transition-all text-xs font-semibold shadow-sm"
          >
            <Shield className="w-3.5 h-3.5" />
            <span>Pressure Leaderboards</span>
            <ArrowRight size={13} />
          </Link>
          <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-[#101C37] border border-[#1A2B50] text-xs font-mono text-slate-300">
            <Shield className="w-3.5 h-3.5 text-[#D6B56D]" />
            <span>200,999 Balls Analyzed</span>
          </div>
          <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-[#101C37] border border-[#1A2B50] text-xs font-mono text-slate-300">
            <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
            <span>867 Deliveries Matches (16 Abandoned Reconciled)</span>
          </div>
          <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-[#E91E8F]/10 border border-[#E91E8F]/30 text-xs font-mono text-[#E91E8F] font-semibold">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Official RR Round 1 Pack</span>
          </div>
        </div>
      </div>

      {/* ------------------------------------------------------------------- */}
      {/* Module A: Aggregate Tactical Telemetry Dashboard (Always Top) */}
      {/* ------------------------------------------------------------------- */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3.5">
        <div className="p-4 rounded-xl bg-[#101C37]/80 border border-[#1A2B50] hover:border-[#E91E8F]/40 transition-all">
          <div className="flex items-center justify-between text-slate-400 mb-1">
            <span className="text-[11px] font-medium uppercase tracking-wider">Total Balls</span>
            <Activity className="w-3.5 h-3.5 text-[#E91E8F]" />
          </div>
          <div className="text-xl font-bold font-mono text-white">
            {summary ? summary.total_deliveries.toLocaleString() : "200,999"}
          </div>
          <div className="text-[10px] text-slate-400 mt-1">
            {summary ? summary.legal_deliveries.toLocaleString() : "192,709"} legal deliveries
          </div>
        </div>

        <div className="p-4 rounded-xl bg-[#101C37]/80 border border-[#1A2B50] hover:border-[#E91E8F]/40 transition-all">
          <div className="flex items-center justify-between text-slate-400 mb-1">
            <span className="text-[11px] font-medium uppercase tracking-wider">Matches Covered</span>
            <Layers className="w-3.5 h-3.5 text-[#D6B56D]" />
          </div>
          <div className="text-xl font-bold font-mono text-white">
            {summary ? summary.total_matches_with_deliveries : "867"}
          </div>
          <div className="text-[10px] text-slate-400 mt-1">
            +16 abandoned without ball
          </div>
        </div>

        <div className="p-4 rounded-xl bg-[#101C37]/80 border border-[#1A2B50] hover:border-[#E91E8F]/40 transition-all">
          <div className="flex items-center justify-between text-slate-400 mb-1">
            <span className="text-[11px] font-medium uppercase tracking-wider">Runs Off Bat</span>
            <TrendingUp className="w-3.5 h-3.5 text-emerald-400" />
          </div>
          <div className="text-xl font-bold font-mono text-white">
            {summary ? summary.total_runs_off_bat.toLocaleString() : "260,209"}
          </div>
          <div className="text-[10px] text-slate-400 mt-1">
            Run rate: {summary ? summary.overall_run_rate_per_6_balls.toFixed(2) : "8.10"} rpo
          </div>
        </div>

        <div className="p-4 rounded-xl bg-[#101C37]/80 border border-[#1A2B50] hover:border-[#E91E8F]/40 transition-all">
          <div className="flex items-center justify-between text-slate-400 mb-1">
            <span className="text-[11px] font-medium uppercase tracking-wider">Total Wickets</span>
            <Target className="w-3.5 h-3.5 text-rose-400" />
          </div>
          <div className="text-xl font-bold font-mono text-white">
            {summary ? summary.total_wickets_fallen.toLocaleString() : "11,460"}
          </div>
          <div className="text-[10px] text-slate-400 mt-1">
            {summary ? summary.total_bowler_wickets.toLocaleString() : "10,489"} bowler wickets
          </div>
        </div>

        <div className="p-4 rounded-xl bg-[#101C37]/80 border border-[#1A2B50] hover:border-[#E91E8F]/40 transition-all">
          <div className="flex items-center justify-between text-slate-400 mb-1">
            <span className="text-[11px] font-medium uppercase tracking-wider">Active Players</span>
            <Users className="w-3.5 h-3.5 text-cyan-400" />
          </div>
          <div className="text-xl font-bold font-mono text-white">
            {summary ? `${summary.total_unique_strikers} / ${summary.total_unique_bowlers}` : "618 / 460"}
          </div>
          <div className="text-[10px] text-slate-400 mt-1">
            Batters / Bowlers mapped
          </div>
        </div>

        <div className="p-4 rounded-xl bg-[#101C37]/80 border border-[#1A2B50] hover:border-[#E91E8F]/40 transition-all">
          <div className="flex items-center justify-between text-slate-400 mb-1">
            <span className="text-[11px] font-medium uppercase tracking-wider">Radar Speeds</span>
            <Gauge className="w-3.5 h-3.5 text-amber-400" />
          </div>
          <div className="text-xl font-bold font-mono text-white">
            {summary ? summary.valid_radar_speed_records.toLocaleString() : "123,113"}
          </div>
          <div className="text-[10px] text-emerald-400 font-semibold mt-1">
            61.3% sensor coverage
          </div>
        </div>
      </div>

      {/* ------------------------------------------------------------------- */}
      {/* Tactical Sub-System Navigation Tabs */}
      {/* ------------------------------------------------------------------- */}
      <div className="flex items-center gap-2 border-b border-[#1A2B50] pb-2 overflow-x-auto">
        <button
          onClick={() => setActiveTab("overview")}
          className={cn(
            "flex items-center gap-2 px-4 py-2 rounded-lg text-xs font-semibold transition-all whitespace-nowrap",
            activeTab === "overview"
              ? "bg-[#E91E8F] text-white shadow-md shadow-[#E91E8F]/20"
              : "text-slate-400 hover:text-white hover:bg-[#101C37]"
          )}
        >
          <BarChart2 className="w-4 h-4" />
          <span>Phase Mastery & Splits (Mod B)</span>
        </button>

        <button
          onClick={() => setActiveTab("strokes_handedness")}
          className={cn(
            "flex items-center gap-2 px-4 py-2 rounded-lg text-xs font-semibold transition-all whitespace-nowrap",
            activeTab === "strokes_handedness"
              ? "bg-[#E91E8F] text-white shadow-md shadow-[#E91E8F]/20"
              : "text-slate-400 hover:text-white hover:bg-[#101C37]"
          )}
        >
          <Target className="w-4 h-4" />
          <span>Strokes & Handedness (Mods C & D)</span>
        </button>

        <button
          onClick={() => setActiveTab("bowling_speed")}
          className={cn(
            "flex items-center gap-2 px-4 py-2 rounded-lg text-xs font-semibold transition-all whitespace-nowrap",
            activeTab === "bowling_speed"
              ? "bg-[#E91E8F] text-white shadow-md shadow-[#E91E8F]/20"
              : "text-slate-400 hover:text-white hover:bg-[#101C37]"
          )}
        >
          <Gauge className="w-4 h-4" />
          <span>Variations & Radar Speed (Mods E & F)</span>
        </button>

        <button
          onClick={() => setActiveTab("death_overs")}
          className={cn(
            "flex items-center gap-2 px-4 py-2 rounded-lg text-xs font-semibold transition-all whitespace-nowrap",
            activeTab === "death_overs"
              ? "bg-[#E91E8F] text-white shadow-md shadow-[#E91E8F]/20"
              : "text-slate-400 hover:text-white hover:bg-[#101C37]"
          )}
        >
          <Flame className="w-4 h-4 text-amber-400" />
          <span>Death Overs Finishers & Containment (Mod H)</span>
        </button>

        <button
          onClick={() => setActiveTab("matchups_players")}
          className={cn(
            "flex items-center gap-2 px-4 py-2 rounded-lg text-xs font-semibold transition-all whitespace-nowrap",
            activeTab === "matchups_players"
              ? "bg-[#E91E8F] text-white shadow-md shadow-[#E91E8F]/20"
              : "text-slate-400 hover:text-white hover:bg-[#101C37]"
          )}
        >
          <Swords className="w-4 h-4" />
          <span>Matchup Battles & Player Dossiers (Mods G & I)</span>
        </button>
      </div>

      {/* ------------------------------------------------------------------- */}
      {/* TAB 1: PHASE MASTERY (MODULE B) */}
      {/* ------------------------------------------------------------------- */}
      {activeTab === "overview" && (
        <div className="space-y-6">
          <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 p-5 rounded-xl bg-[#101C37]/60 border border-[#1A2B50]">
            <div>
              <h2 className="text-lg font-bold text-white flex items-center gap-2">
                <BarChart2 className="w-5 h-5 text-[#E91E8F]" />
                Tournament Match Phase Architecture
              </h2>
              <p className="text-xs text-slate-400 mt-1">
                Governed breakdown: Powerplay (Overs 1–6), Middle Overs (Overs 7–15), Death Overs (Overs 16–20)
              </p>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-xs text-slate-400 font-medium">Tournament Phase Baseline:</span>
              <span className="text-xs font-mono font-bold px-2.5 py-1 rounded-md bg-[#1A2B50] text-[#D6B56D]">
                All 867 Matches
              </span>
            </div>
          </div>

          {/* Phase Cards Grid */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* Powerplay Card */}
            <div className="p-6 rounded-xl bg-[#101C37]/80 border border-[#1A2B50] hover:border-[#E91E8F]/50 transition-all relative overflow-hidden group">
              <div className="absolute top-0 right-0 w-28 h-28 bg-[#E91E8F]/5 rounded-bl-full pointer-events-none group-hover:bg-[#E91E8F]/10 transition-colors" />
              <div className="flex items-center justify-between mb-4">
                <span className="text-xs font-mono font-bold px-2.5 py-1 rounded bg-[#E91E8F]/20 text-[#E91E8F] border border-[#E91E8F]/30">
                  Overs 1 – 6
                </span>
                <span className="text-xs font-semibold text-slate-400">Powerplay Phase</span>
              </div>
              <h3 className="text-2xl font-bold text-white mb-2">Powerplay</h3>
              <p className="text-xs text-slate-400 mb-6">
                Field restrictions active (2 fielders outside 30-yard circle). High swing ball period.
              </p>

              <div className="space-y-3 font-mono text-xs">
                <div className="flex items-center justify-between pb-2 border-b border-[#1A2B50]/60">
                  <span className="text-slate-400">Strike Rate / Economy</span>
                  <span className="text-white font-bold">
                    {phasesData?.phases["Powerplay"]?.strike_rate?.toFixed(1) ?? "125.7"} / {phasesData?.phases["Powerplay"]?.economy_rate?.toFixed(2) ?? "7.54"}
                  </span>
                </div>
                <div className="flex items-center justify-between pb-2 border-b border-[#1A2B50]/60">
                  <span className="text-slate-400">Boundary Frequency</span>
                  <span className="text-emerald-400 font-bold">
                    {phasesData?.phases["Powerplay"]?.boundary_percentage?.toFixed(1) ?? "18.2"}%
                  </span>
                </div>
                <div className="flex items-center justify-between pb-2 border-b border-[#1A2B50]/60">
                  <span className="text-slate-400">Dot Ball Percentage</span>
                  <span className="text-amber-400 font-bold">
                    {phasesData?.phases["Powerplay"]?.dot_ball_percentage?.toFixed(1) ?? "46.8"}%
                  </span>
                </div>
                <div className="flex items-center justify-between pb-2 border-b border-[#1A2B50]/60">
                  <span className="text-slate-400">Bowling Average</span>
                  <span className="text-slate-200 font-bold">
                    {phasesData?.phases["Powerplay"]?.average?.toFixed(1) ?? "31.4"} runs/wkt
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-slate-400">Balls Per Wicket</span>
                  <span className="text-slate-200 font-bold">
                    {phasesData?.phases["Powerplay"]?.balls_per_wicket?.toFixed(1) ?? "25.0"} balls
                  </span>
                </div>
              </div>
            </div>

            {/* Middle Overs Card */}
            <div className="p-6 rounded-xl bg-[#101C37]/80 border border-[#1A2B50] hover:border-[#D6B56D]/50 transition-all relative overflow-hidden group">
              <div className="absolute top-0 right-0 w-28 h-28 bg-[#D6B56D]/5 rounded-bl-full pointer-events-none group-hover:bg-[#D6B56D]/10 transition-colors" />
              <div className="flex items-center justify-between mb-4">
                <span className="text-xs font-mono font-bold px-2.5 py-1 rounded bg-[#D6B56D]/20 text-[#D6B56D] border border-[#D6B56D]/30">
                  Overs 7 – 15
                </span>
                <span className="text-xs font-semibold text-slate-400">Middle Phase</span>
              </div>
              <h3 className="text-2xl font-bold text-white mb-2">Middle Overs</h3>
              <p className="text-xs text-slate-400 mb-6">
                Spin strangle, rotation of strike, boundary containment, and wicket-taking through pressure.
              </p>

              <div className="space-y-3 font-mono text-xs">
                <div className="flex items-center justify-between pb-2 border-b border-[#1A2B50]/60">
                  <span className="text-slate-400">Strike Rate / Economy</span>
                  <span className="text-white font-bold">
                    {phasesData?.phases["Middle"]?.strike_rate?.toFixed(1) ?? "130.5"} / {phasesData?.phases["Middle"]?.economy_rate?.toFixed(2) ?? "7.83"}
                  </span>
                </div>
                <div className="flex items-center justify-between pb-2 border-b border-[#1A2B50]/60">
                  <span className="text-slate-400">Boundary Frequency</span>
                  <span className="text-emerald-400 font-bold">
                    {phasesData?.phases["Middle"]?.boundary_percentage?.toFixed(1) ?? "13.9"}%
                  </span>
                </div>
                <div className="flex items-center justify-between pb-2 border-b border-[#1A2B50]/60">
                  <span className="text-slate-400">Dot Ball Percentage</span>
                  <span className="text-amber-400 font-bold">
                    {phasesData?.phases["Middle"]?.dot_ball_percentage?.toFixed(1) ?? "34.2"}%
                  </span>
                </div>
                <div className="flex items-center justify-between pb-2 border-b border-[#1A2B50]/60">
                  <span className="text-slate-400">Bowling Average</span>
                  <span className="text-slate-200 font-bold">
                    {phasesData?.phases["Middle"]?.average?.toFixed(1) ?? "27.6"} runs/wkt
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-slate-400">Balls Per Wicket</span>
                  <span className="text-slate-200 font-bold">
                    {phasesData?.phases["Middle"]?.balls_per_wicket?.toFixed(1) ?? "21.1"} balls
                  </span>
                </div>
              </div>
            </div>

            {/* Death Overs Card */}
            <div className="p-6 rounded-xl bg-[#101C37]/80 border border-[#1A2B50] hover:border-rose-500/50 transition-all relative overflow-hidden group">
              <div className="absolute top-0 right-0 w-28 h-28 bg-rose-500/5 rounded-bl-full pointer-events-none group-hover:bg-rose-500/10 transition-colors" />
              <div className="flex items-center justify-between mb-4">
                <span className="text-xs font-mono font-bold px-2.5 py-1 rounded bg-rose-500/20 text-rose-400 border border-rose-500/30">
                  Overs 16 – 20
                </span>
                <span className="text-xs font-semibold text-slate-400">Death Phase</span>
              </div>
              <h3 className="text-2xl font-bold text-white mb-2">Death Overs</h3>
              <p className="text-xs text-slate-400 mb-6">
                Max aggression, boundary hitting, yorkers, wide cutters, high pressure execution.
              </p>

              <div className="space-y-3 font-mono text-xs">
                <div className="flex items-center justify-between pb-2 border-b border-[#1A2B50]/60">
                  <span className="text-slate-400">Strike Rate / Economy</span>
                  <span className="text-white font-bold">
                    {phasesData?.phases["Death"]?.strike_rate?.toFixed(1) ?? "168.1"} / {phasesData?.phases["Death"]?.economy_rate?.toFixed(2) ?? "10.09"}
                  </span>
                </div>
                <div className="flex items-center justify-between pb-2 border-b border-[#1A2B50]/60">
                  <span className="text-slate-400">Boundary Frequency</span>
                  <span className="text-emerald-400 font-bold">
                    {phasesData?.phases["Death"]?.boundary_percentage?.toFixed(1) ?? "20.8"}%
                  </span>
                </div>
                <div className="flex items-center justify-between pb-2 border-b border-[#1A2B50]/60">
                  <span className="text-slate-400">Dot Ball Percentage</span>
                  <span className="text-amber-400 font-bold">
                    {phasesData?.phases["Death"]?.dot_ball_percentage?.toFixed(1) ?? "28.5"}%
                  </span>
                </div>
                <div className="flex items-center justify-between pb-2 border-b border-[#1A2B50]/60">
                  <span className="text-slate-400">Bowling Average</span>
                  <span className="text-slate-200 font-bold">
                    {phasesData?.phases["Death"]?.average?.toFixed(1) ?? "16.9"} runs/wkt
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-slate-400">Balls Per Wicket</span>
                  <span className="text-slate-200 font-bold">
                    {phasesData?.phases["Death"]?.balls_per_wicket?.toFixed(1) ?? "10.1"} balls
                  </span>
                </div>
              </div>
            </div>
          </div>

          {/* Tactical Takeaways Box */}
          <div className="p-5 rounded-xl bg-gradient-to-r from-[#101C37] to-[#1A2B50] border border-[#1A2B50] flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
            <div className="flex items-center gap-3">
              <div className="p-2.5 rounded-lg bg-[#E91E8F]/20 text-[#E91E8F]">
                <Sparkles className="w-5 h-5" />
              </div>
              <div>
                <h4 className="text-sm font-bold text-white">Tactical Phase Intelligence Insight</h4>
                <p className="text-xs text-slate-300 mt-0.5">
                  Death overs economy climbs to <strong className="text-white">10.09 rpo</strong> with boundary frequency at <strong className="text-emerald-400">20.8%</strong>, while bowling strike rate drops dramatically to a wicket every <strong className="text-white">10.1 balls</strong>.
                </p>
              </div>
            </div>
            <button
              onClick={() => setActiveTab("death_overs")}
              className="px-4 py-2 rounded-lg bg-[#101C37] hover:bg-[#1A2B50] text-xs font-semibold text-[#D6B56D] border border-[#D6B56D]/30 flex items-center gap-1.5 whitespace-nowrap transition-colors"
            >
              <span>Explore Death Specialists</span>
              <ChevronRight className="w-3.5 h-3.5" />
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
            <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 p-5 rounded-xl bg-[#101C37]/60 border border-[#1A2B50]">
              <div>
                <h2 className="text-lg font-bold text-white flex items-center gap-2">
                  <Target className="w-5 h-5 text-[#E91E8F]" />
                  Batting Stroke Efficiency & Dismissal Threat (30 Strokes)
                </h2>
                <p className="text-xs text-slate-400 mt-1">
                  Empirical productivity across all stroke types recorded in official Rajasthan Royals telemetry.
                </p>
              </div>

              {/* Filters for Stroke Table */}
              <div className="flex flex-wrap items-center gap-3">
                <div className="flex items-center gap-2">
                  <span className="text-xs text-slate-400">Min Balls:</span>
                  <select
                    value={strokeMinBalls}
                    onChange={(e) => setStrokeMinBalls(Number(e.target.value))}
                    className="bg-[#101C37] text-white text-xs font-mono border border-[#1A2B50] rounded-lg px-2.5 py-1.5 focus:outline-none focus:border-[#E91E8F]"
                  >
                    <option value={20}>20+ Balls</option>
                    <option value={50}>50+ Balls</option>
                    <option value={100}>100+ Balls</option>
                    <option value={250}>250+ Balls</option>
                    <option value={500}>500+ Balls</option>
                  </select>
                </div>

                <div className="flex items-center gap-2">
                  <span className="text-xs text-slate-400">Sort By:</span>
                  <select
                    value={strokeSortKey}
                    onChange={(e) => setStrokeSortKey(e.target.value as any)}
                    className="bg-[#101C37] text-white text-xs font-mono border border-[#1A2B50] rounded-lg px-2.5 py-1.5 focus:outline-none focus:border-[#E91E8F]"
                  >
                    <option value="runs_per_shot">Runs / Shot (Highest)</option>
                    <option value="deliveries_faced">Sample Volume (Balls)</option>
                    <option value="boundary_pct">Boundary % (Highest)</option>
                    <option value="dismissal_rate_pct">Dismissal Risk (Safest)</option>
                  </select>
                </div>
              </div>
            </div>

            {/* Stroke Table */}
            <div className="rounded-xl border border-[#1A2B50] overflow-hidden bg-[#101C37]/80">
              <div className="overflow-x-auto max-h-[460px]">
                <table className="w-full text-left text-xs">
                  <thead className="bg-[#101C37] text-slate-400 font-mono uppercase text-[10px] tracking-wider sticky top-0 border-b border-[#1A2B50] z-10">
                    <tr>
                      <th className="px-4 py-3">Stroke Category</th>
                      <th className="px-4 py-3 text-right">Balls Faced</th>
                      <th className="px-4 py-3 text-right">Runs Scored</th>
                      <th className="px-4 py-3 text-right">Runs / Shot</th>
                      <th className="px-4 py-3 text-right">Boundary %</th>
                      <th className="px-4 py-3 text-right">Dismissals</th>
                      <th className="px-4 py-3 text-right">Dismissal Risk %</th>
                      <th className="px-4 py-3 text-center">Tactical Profile</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-[#1A2B50]/60 font-mono">
                    {sortedStrokes.map((stroke, idx) => {
                      const isHighYield = stroke.runs_per_shot >= 1.5;
                      const isHighRisk = stroke.dismissal_rate_pct >= 6.0;
                      return (
                        <tr key={idx} className="hover:bg-[#1A2B50]/40 transition-colors">
                          <td className="px-4 py-3 font-semibold text-white font-sans flex items-center gap-2">
                            <span className="w-1.5 h-1.5 rounded-full bg-[#E91E8F]" />
                            {stroke.stroke}
                          </td>
                          <td className="px-4 py-3 text-right text-slate-300">
                            {stroke.deliveries_faced.toLocaleString()}
                          </td>
                          <td className="px-4 py-3 text-right text-white font-bold">
                            {stroke.runs_scored.toLocaleString()}
                          </td>
                          <td className="px-4 py-3 text-right">
                            <span className={cn(
                              "font-bold",
                              isHighYield ? "text-emerald-400" : "text-slate-200"
                            )}>
                              {stroke.runs_per_shot.toFixed(2)}
                            </span>
                          </td>
                          <td className="px-4 py-3 text-right text-emerald-400">
                            {stroke.boundary_pct.toFixed(1)}%
                          </td>
                          <td className="px-4 py-3 text-right text-slate-300">
                            {stroke.dismissals}
                          </td>
                          <td className="px-4 py-3 text-right">
                            <span className={cn(
                              "font-bold",
                              isHighRisk ? "text-rose-400" : "text-slate-300"
                            )}>
                              {stroke.dismissal_rate_pct.toFixed(2)}%
                            </span>
                          </td>
                          <td className="px-4 py-3 text-center font-sans">
                            {isHighYield && !isHighRisk && (
                              <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                                High Yield / Safe
                              </span>
                            )}
                            {isHighYield && isHighRisk && (
                              <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-amber-500/10 text-amber-400 border border-amber-500/20">
                                High Risk / High Reward
                              </span>
                            )}
                            {!isHighYield && isHighRisk && (
                              <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-rose-500/10 text-rose-400 border border-rose-500/20">
                                High Hazard
                              </span>
                            )}
                            {!isHighYield && !isHighRisk && (
                              <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-slate-500/10 text-slate-400 border border-slate-500/20">
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
            <div className="p-5 rounded-xl bg-[#101C37]/60 border border-[#1A2B50]">
              <h2 className="text-lg font-bold text-white flex items-center gap-2">
                <Swords className="w-5 h-5 text-[#D6B56D]" />
                Batter Handedness vs Bowling Discipline Matrix (4-Way Cross-Split)
              </h2>
              <p className="text-xs text-slate-400 mt-1">
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
                    className="p-5 rounded-xl bg-[#101C37]/80 border border-[#1A2B50] hover:border-[#D6B56D]/50 transition-all flex flex-col justify-between"
                  >
                    <div>
                      <div className="flex items-center justify-between mb-3">
                        <span className={cn(
                          "text-xs font-mono font-bold px-2.5 py-0.5 rounded border",
                          isLHB
                            ? "bg-[#E91E8F]/20 text-[#E91E8F] border-[#E91E8F]/30"
                            : "bg-[#D6B56D]/20 text-[#D6B56D] border-[#D6B56D]/30"
                        )}>
                          {split.batting_type}
                        </span>
                        <span className={cn(
                          "text-xs font-mono font-bold px-2.5 py-0.5 rounded border",
                          isSpin
                            ? "bg-purple-500/20 text-purple-300 border-purple-500/30"
                            : "bg-blue-500/20 text-blue-300 border-blue-500/30"
                        )}>
                          vs {split.pace_or_spin}
                        </span>
                      </div>

                      <h4 className="text-base font-bold text-white mb-4">
                        {split.batting_type} vs {split.pace_or_spin}
                      </h4>

                      <div className="space-y-2.5 font-mono text-xs">
                        <div className="flex justify-between pb-1.5 border-b border-[#1A2B50]/60">
                          <span className="text-slate-400">Balls Faced:</span>
                          <span className="text-white font-bold">{split.balls_faced.toLocaleString()}</span>
                        </div>
                        <div className="flex justify-between pb-1.5 border-b border-[#1A2B50]/60">
                          <span className="text-slate-400">Strike Rate:</span>
                          <span className="text-emerald-400 font-bold">{split.strike_rate.toFixed(1)}</span>
                        </div>
                        <div className="flex justify-between pb-1.5 border-b border-[#1A2B50]/60">
                          <span className="text-slate-400">Economy Conceded:</span>
                          <span className="text-amber-400 font-bold">{split.economy_rate.toFixed(2)}</span>
                        </div>
                        <div className="flex justify-between pb-1.5 border-b border-[#1A2B50]/60">
                          <span className="text-slate-400">Bowling Average:</span>
                          <span className="text-slate-200 font-bold">{split.bowling_average ? split.bowling_average.toFixed(1) : "N/A"}</span>
                        </div>
                        <div className="flex justify-between pb-1.5 border-b border-[#1A2B50]/60">
                          <span className="text-slate-400">Dot Ball %:</span>
                          <span className="text-slate-300 font-bold">{split.dot_pct.toFixed(1)}%</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-slate-400">Boundary %:</span>
                          <span className="text-emerald-400 font-bold">{split.boundary_pct.toFixed(1)}%</span>
                        </div>
                      </div>
                    </div>

                    <div className="mt-4 pt-3 border-t border-[#1A2B50] text-[11px] text-slate-400 italic">
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
            <div className="p-5 rounded-xl bg-[#101C37]/60 border border-[#1A2B50] flex flex-col lg:flex-row items-start lg:items-center justify-between gap-4">
              <div>
                <h2 className="text-lg font-bold text-white flex items-center gap-2">
                  <Gauge className="w-5 h-5 text-amber-400" />
                  Bowling Radar Telemetry & Speed Profiles
                </h2>
                <p className="text-xs text-slate-400 mt-1">
                  Radar release velocity with automated domain safeguards and physical boundary filters.
                </p>
              </div>

              {/* Sensor Disclaimer Pill */}
              <div className="flex items-center gap-2 px-3.5 py-1.5 rounded-lg bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-mono">
                <CheckCircle2 className="w-4 h-4" />
                <span>Sensor Safeguard Active: Scaling & Outlier Clipping</span>
              </div>
            </div>

            {/* Sensor Calibration Safeguard Notice Banner */}
            <div className="p-4 rounded-xl bg-amber-500/10 border border-amber-500/20 flex items-start gap-3">
              <AlertTriangle className="w-5 h-5 text-amber-400 shrink-0 mt-0.5" />
              <div className="text-xs text-amber-200/90 leading-relaxed">
                <strong className="text-amber-300 font-semibold block mb-0.5">Sensor Safeguard & Quality Verification:</strong>
                Raw radar release speed is recorded on <strong className="text-white">123,113 deliveries (61.3% coverage)</strong>. Governed scaling divides erroneous 10x multiplier values (<span className="font-mono text-amber-300">speed &ge; 500.0</span>) by 10 (e.g. 1456.1 &rarr; 145.61 km/h). Extreme anomalous outliers (<span className="font-mono text-amber-300">&lt; 50.0</span> or <span className="font-mono text-amber-300">&gt; 170.0 km/h</span>) are strictly filtered out to prevent skewing velocity distributions.
              </div>
            </div>

            {/* Velocity Brackets */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="p-4 rounded-xl bg-[#101C37]/80 border border-[#1A2B50]">
                <span className="text-[11px] font-medium text-slate-400 uppercase tracking-wider block mb-1">
                  Slow / Spin (&lt; 110 km/h)
                </span>
                <span className="text-2xl font-bold font-mono text-purple-300">
                  {speedData?.speed_brackets?.slow_under_110.toLocaleString() ?? "43,303"}
                </span>
                <span className="text-[10px] text-slate-400 block mt-1">Spinners & off-pace cutters</span>
              </div>

              <div className="p-4 rounded-xl bg-[#101C37]/80 border border-[#1A2B50]">
                <span className="text-[11px] font-medium text-slate-400 uppercase tracking-wider block mb-1">
                  Medium (110 – 125 km/h)
                </span>
                <span className="text-2xl font-bold font-mono text-blue-300">
                  {speedData?.speed_brackets?.medium_110_to_125.toLocaleString() ?? "15,832"}
                </span>
                <span className="text-[10px] text-slate-400 block mt-1">Military medium & fast spin</span>
              </div>

              <div className="p-4 rounded-xl bg-[#101C37]/80 border border-[#1A2B50]">
                <span className="text-[11px] font-medium text-slate-400 uppercase tracking-wider block mb-1">
                  Fast-Medium (125 – 140 km/h)
                </span>
                <span className="text-2xl font-bold font-mono text-cyan-300">
                  {speedData?.speed_brackets?.fast_medium_125_to_140.toLocaleString() ?? "54,233"}
                </span>
                <span className="text-[10px] text-slate-400 block mt-1">Modern seam bowling core</span>
              </div>

              <div className="p-4 rounded-xl bg-[#101C37]/80 border border-[#1A2B50]">
                <span className="text-[11px] font-medium text-slate-400 uppercase tracking-wider block mb-1">
                  Express Pace (&gt; 140 km/h)
                </span>
                <span className="text-2xl font-bold font-mono text-rose-400">
                  {speedData?.speed_brackets?.express_over_140.toLocaleString() ?? "9,745"}
                </span>
                <span className="text-[10px] text-rose-300/80 block mt-1">Elite express velocity</span>
              </div>
            </div>

            {/* Fastest Bowlers Table */}
            <div className="rounded-xl border border-[#1A2B50] overflow-hidden bg-[#101C37]/80">
              <div className="p-4 border-b border-[#1A2B50] flex items-center justify-between">
                <h3 className="text-sm font-bold text-white flex items-center gap-2">
                  <Flame className="w-4 h-4 text-rose-400" />
                  Top 10 Fastest Bowlers by Mean Release Velocity
                </h3>
                <span className="text-xs font-mono text-slate-400">Min 30 Valid Deliveries</span>
              </div>
              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs font-mono">
                  <thead className="bg-[#101C37] text-slate-400 uppercase text-[10px] tracking-wider border-b border-[#1A2B50]">
                    <tr>
                      <th className="px-4 py-3 font-sans">Rank & Bowler</th>
                      <th className="px-4 py-3 text-right">Valid Radar Balls</th>
                      <th className="px-4 py-3 text-right">Mean Speed (km/h)</th>
                      <th className="px-4 py-3 text-right">Peak Speed (km/h)</th>
                      <th className="px-4 py-3 text-right">Balls &gt; 140 km/h</th>
                      <th className="px-4 py-3 text-center font-sans">RR Roster Match</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-[#1A2B50]/60">
                    {speedData?.top_fastest_bowlers?.map((bowler, idx) => {
                      const isRR = [2320, 4489].includes(bowler.bowler_id);
                      return (
                        <tr key={idx} className="hover:bg-[#1A2B50]/40 transition-colors">
                          <td className="px-4 py-3 font-sans font-semibold text-white flex items-center gap-2.5">
                            <span className={cn(
                              "w-5 h-5 rounded-full flex items-center justify-center text-[10px] font-mono font-bold",
                              idx === 0 ? "bg-amber-400 text-[#101C37]" : "bg-[#1A2B50] text-slate-300"
                            )}>
                              {idx + 1}
                            </span>
                            {bowler.bowler_name}
                          </td>
                          <td className="px-4 py-3 text-right text-slate-300">
                            {bowler.valid_deliveries.toLocaleString()}
                          </td>
                          <td className="px-4 py-3 text-right font-bold text-rose-400 text-sm">
                            {bowler.mean_speed_kmh.toFixed(1)}
                          </td>
                          <td className="px-4 py-3 text-right font-bold text-amber-300">
                            {bowler.max_speed_kmh.toFixed(1)}
                          </td>
                          <td className="px-4 py-3 text-right text-slate-200">
                            {bowler.express_balls_count}
                          </td>
                          <td className="px-4 py-3 text-center font-sans">
                            {isRR ? (
                              <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-[#E91E8F]/20 text-[#E91E8F] border border-[#E91E8F]/30">
                                Royals Bowler
                              </span>
                            ) : (
                              <span className="text-[10px] text-slate-500 font-mono">Opponent</span>
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
            <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 p-5 rounded-xl bg-[#101C37]/60 border border-[#1A2B50]">
              <div>
                <h2 className="text-lg font-bold text-white flex items-center gap-2">
                  <Layers className="w-5 h-5 text-[#E91E8F]" />
                  Bowling Variations & Delivery Styles (34 Styles)
                </h2>
                <p className="text-xs text-slate-400 mt-1">
                  Seam movements, spin variations, bouncers, yorkers, and knuckleballs profiled for containment & threat.
                </p>
              </div>

              {/* Filters for Variations */}
              <div className="flex flex-wrap items-center gap-3">
                <div className="flex items-center gap-2">
                  <span className="text-xs text-slate-400">Min Deliveries:</span>
                  <select
                    value={variationMinBalls}
                    onChange={(e) => setVariationMinBalls(Number(e.target.value))}
                    className="bg-[#101C37] text-white text-xs font-mono border border-[#1A2B50] rounded-lg px-2.5 py-1.5 focus:outline-none focus:border-[#E91E8F]"
                  >
                    <option value={20}>20+ Balls</option>
                    <option value={50}>50+ Balls</option>
                    <option value={100}>100+ Balls</option>
                    <option value={250}>250+ Balls</option>
                  </select>
                </div>

                <div className="flex items-center gap-2">
                  <span className="text-xs text-slate-400">Sort By:</span>
                  <select
                    value={variationSortKey}
                    onChange={(e) => setVariationSortKey(e.target.value as any)}
                    className="bg-[#101C37] text-white text-xs font-mono border border-[#1A2B50] rounded-lg px-2.5 py-1.5 focus:outline-none focus:border-[#E91E8F]"
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
            <div className="rounded-xl border border-[#1A2B50] overflow-hidden bg-[#101C37]/80">
              <div className="overflow-x-auto max-h-[460px]">
                <table className="w-full text-left text-xs font-mono">
                  <thead className="bg-[#101C37] text-slate-400 uppercase text-[10px] tracking-wider sticky top-0 border-b border-[#1A2B50] z-10">
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
                  <tbody className="divide-y divide-[#1A2B50]/60">
                    {sortedVariations.map((style, idx) => {
                      const isContainment = style.economy_rate <= 7.5;
                      const isHighThreat = style.wickets >= 50;
                      return (
                        <tr key={idx} className="hover:bg-[#1A2B50]/40 transition-colors">
                          <td className="px-4 py-3 font-sans font-semibold text-white flex items-center gap-2">
                            <span className="w-1.5 h-1.5 rounded-full bg-[#D6B56D]" />
                            {style.delivery_style}
                          </td>
                          <td className="px-4 py-3 text-right text-slate-300">
                            {style.deliveries_bowled.toLocaleString()}
                          </td>
                          <td className="px-4 py-3 text-right text-slate-300">
                            {style.runs_conceded.toLocaleString()}
                          </td>
                          <td className="px-4 py-3 text-right text-white font-bold">
                            {style.wickets}
                          </td>
                          <td className="px-4 py-3 text-right">
                            <span className={cn(
                              "font-bold",
                              isContainment ? "text-emerald-400" : "text-amber-400"
                            )}>
                              {style.economy_rate.toFixed(2)}
                            </span>
                          </td>
                          <td className="px-4 py-3 text-right text-slate-300">
                            {style.bowling_average ? style.bowling_average.toFixed(1) : "N/A"}
                          </td>
                          <td className="px-4 py-3 text-right text-cyan-400">
                            {style.dot_ball_pct.toFixed(1)}%
                          </td>
                          <td className="px-4 py-3 text-center font-sans">
                            {isContainment && isHighThreat && (
                              <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                                Gold Standard
                              </span>
                            )}
                            {isContainment && !isHighThreat && (
                              <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/20">
                                Containment Weapon
                              </span>
                            )}
                            {!isContainment && isHighThreat && (
                              <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-rose-500/10 text-rose-400 border border-rose-500/20">
                                Wicket Hunter
                              </span>
                            )}
                            {!isContainment && !isHighThreat && (
                              <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-slate-500/10 text-slate-400 border border-slate-500/20">
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
          <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 p-5 rounded-xl bg-[#101C37]/60 border border-[#1A2B50]">
            <div>
              <h2 className="text-lg font-bold text-white flex items-center gap-2">
                <Flame className="w-5 h-5 text-rose-500" />
                Death Overs Mastery (Overs 16–20)
              </h2>
              <p className="text-xs text-slate-400 mt-1">
                Elite finishers ranked by strike rate and boundary execution; elite containment bowlers ranked by economy.
              </p>
            </div>

            {/* Discipline Selector */}
            <div className="flex flex-wrap items-center gap-3">
              <div className="flex items-center rounded-lg bg-[#101C37] border border-[#1A2B50] p-0.5">
                <button
                  onClick={() => setDeathDiscipline("all")}
                  className={cn(
                    "px-3 py-1 rounded-md text-xs font-semibold transition-all",
                    deathDiscipline === "all" ? "bg-[#E91E8F] text-white" : "text-slate-400 hover:text-white"
                  )}
                >
                  Dual View
                </button>
                <button
                  onClick={() => setDeathDiscipline("batting")}
                  className={cn(
                    "px-3 py-1 rounded-md text-xs font-semibold transition-all",
                    deathDiscipline === "batting" ? "bg-[#E91E8F] text-white" : "text-slate-400 hover:text-white"
                  )}
                >
                  Finishers (Batting)
                </button>
                <button
                  onClick={() => setDeathDiscipline("bowling")}
                  className={cn(
                    "px-3 py-1 rounded-md text-xs font-semibold transition-all",
                    deathDiscipline === "bowling" ? "bg-[#E91E8F] text-white" : "text-slate-400 hover:text-white"
                  )}
                >
                  Containment (Bowling)
                </button>
              </div>

              <div className="flex items-center gap-2">
                <span className="text-xs text-slate-400">Min Balls:</span>
                <select
                  value={deathMinBalls}
                  onChange={(e) => setDeathMinBalls(Number(e.target.value))}
                  className="bg-[#101C37] text-white text-xs font-mono border border-[#1A2B50] rounded-lg px-2.5 py-1 focus:outline-none focus:border-[#E91E8F]"
                >
                  <option value={50}>50+ Balls</option>
                  <option value={100}>100+ Balls (Recommended)</option>
                  <option value={150}>150+ Balls</option>
                </select>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Batting Finishers Leaderboard */}
            {(deathDiscipline === "all" || deathDiscipline === "batting") && (
              <div className="rounded-xl border border-[#1A2B50] overflow-hidden bg-[#101C37]/80">
                <div className="p-4 border-b border-[#1A2B50] flex items-center justify-between bg-gradient-to-r from-[#101C37] to-[#1A2B50]/60">
                  <div className="flex items-center gap-2">
                    <TrendingUp className="w-4 h-4 text-emerald-400" />
                    <h3 className="text-sm font-bold text-white">Elite Death Finishers (Strike Rate)</h3>
                  </div>
                  <span className="text-[11px] font-mono text-[#D6B56D]">Overs 16–20</span>
                </div>
                <div className="overflow-x-auto">
                  <table className="w-full text-left text-xs font-mono">
                    <thead className="bg-[#101C37] text-slate-400 uppercase text-[10px] tracking-wider border-b border-[#1A2B50]">
                      <tr>
                        <th className="px-4 py-3 font-sans">Rank & Batter</th>
                        <th className="px-4 py-3 text-right">Runs</th>
                        <th className="px-4 py-3 text-right">Balls</th>
                        <th className="px-4 py-3 text-right">4s / 6s</th>
                        <th className="px-4 py-3 text-right">Strike Rate</th>
                        <th className="px-4 py-3 text-right">Boundary %</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-[#1A2B50]/60">
                      {deathOversData?.batting_finishers?.map((batter, idx) => (
                        <tr key={idx} className="hover:bg-[#1A2B50]/40 transition-colors">
                          <td className="px-4 py-3 font-sans font-semibold text-white flex items-center gap-2.5">
                            <span className={cn(
                              "w-5 h-5 rounded-full flex items-center justify-center text-[10px] font-mono font-bold",
                              idx === 0 ? "bg-amber-400 text-[#101C37]" : "bg-[#1A2B50] text-slate-300"
                            )}>
                              {idx + 1}
                            </span>
                            {batter.striker_name}
                          </td>
                          <td className="px-4 py-3 text-right text-slate-200 font-bold">{batter.runs}</td>
                          <td className="px-4 py-3 text-right text-slate-400">{batter.balls}</td>
                          <td className="px-4 py-3 text-right text-slate-300">{batter.fours} / {batter.sixes}</td>
                          <td className="px-4 py-3 text-right font-bold text-emerald-400 text-sm">
                            {batter.strike_rate.toFixed(1)}
                          </td>
                          <td className="px-4 py-3 text-right text-slate-200">{batter.boundary_pct.toFixed(1)}%</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}

            {/* Bowling Containment Leaderboard */}
            {(deathDiscipline === "all" || deathDiscipline === "bowling") && (
              <div className="rounded-xl border border-[#1A2B50] overflow-hidden bg-[#101C37]/80">
                <div className="p-4 border-b border-[#1A2B50] flex items-center justify-between bg-gradient-to-r from-[#101C37] to-[#1A2B50]/60">
                  <div className="flex items-center gap-2">
                    <Shield className="w-4 h-4 text-cyan-400" />
                    <h3 className="text-sm font-bold text-white">Elite Death Bowlers (Containment Economy)</h3>
                  </div>
                  <span className="text-[11px] font-mono text-[#D6B56D]">Overs 16–20</span>
                </div>
                <div className="overflow-x-auto">
                  <table className="w-full text-left text-xs font-mono">
                    <thead className="bg-[#101C37] text-slate-400 uppercase text-[10px] tracking-wider border-b border-[#1A2B50]">
                      <tr>
                        <th className="px-4 py-3 font-sans">Rank & Bowler</th>
                        <th className="px-4 py-3 text-right">Legal Balls</th>
                        <th className="px-4 py-3 text-right">Runs</th>
                        <th className="px-4 py-3 text-right">Wickets</th>
                        <th className="px-4 py-3 text-right">Economy</th>
                        <th className="px-4 py-3 text-right">Dot Ball %</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-[#1A2B50]/60">
                      {deathOversData?.bowling_containment?.map((bowler, idx) => (
                        <tr key={idx} className="hover:bg-[#1A2B50]/40 transition-colors">
                          <td className="px-4 py-3 font-sans font-semibold text-white flex items-center gap-2.5">
                            <span className={cn(
                              "w-5 h-5 rounded-full flex items-center justify-center text-[10px] font-mono font-bold",
                              idx === 0 ? "bg-cyan-400 text-[#101C37]" : "bg-[#1A2B50] text-slate-300"
                            )}>
                              {idx + 1}
                            </span>
                            <div>
                              <div>{bowler.bowler_name}</div>
                              <div className="text-[10px] font-mono text-slate-400">{bowler.bowling_type}</div>
                            </div>
                          </td>
                          <td className="px-4 py-3 text-right text-slate-400">{bowler.legal_balls}</td>
                          <td className="px-4 py-3 text-right text-slate-300">{bowler.runs}</td>
                          <td className="px-4 py-3 text-right text-white font-bold">{bowler.wickets}</td>
                          <td className="px-4 py-3 text-right font-bold text-cyan-400 text-sm">
                            {bowler.economy.toFixed(2)}
                          </td>
                          <td className="px-4 py-3 text-right text-slate-200">{bowler.dot_pct.toFixed(1)}%</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
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
            <div className="p-5 rounded-xl bg-[#101C37]/60 border border-[#1A2B50] flex flex-col lg:flex-row items-start lg:items-center justify-between gap-4">
              <div>
                <h2 className="text-lg font-bold text-white flex items-center gap-2">
                  <Swords className="w-5 h-5 text-[#E91E8F]" />
                  Direct Head-to-Head Micro-Battle Explorer
                </h2>
                <p className="text-xs text-slate-400 mt-1">
                  Empirical head-to-head records across all official deliveries between a striker and bowler.
                </p>
              </div>

              {/* Quick Preset Buttons */}
              <div className="flex flex-wrap items-center gap-2">
                <span className="text-xs text-slate-400">Presets:</span>
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
                        ? "bg-[#E91E8F] text-white border-[#E91E8F]"
                        : "bg-[#101C37] text-slate-300 border-[#1A2B50] hover:border-slate-600"
                    )}
                  >
                    {preset.label}
                  </button>
                ))}
              </div>
            </div>

            {/* Micro-Battle Visual Result Card */}
            <div className="p-6 rounded-2xl bg-gradient-to-br from-[#101C37] via-[#101C37] to-[#1A2B50] border border-[#1A2B50] shadow-xl">
              {h2hLoading ? (
                <div className="flex items-center justify-center py-12 text-slate-400 text-xs font-mono">
                  <RefreshCw className="w-5 h-5 animate-spin text-[#E91E8F] mr-2" />
                  Extracting empirical micro-battle records...
                </div>
              ) : h2hData ? (
                <div className="space-y-6">
                  {/* Versus Banner */}
                  <div className="flex flex-col md:flex-row items-center justify-between gap-6 pb-6 border-b border-[#1A2B50]">
                    {/* Striker side */}
                    <div className="flex items-center gap-4 text-left w-full md:w-auto">
                      <div className="w-12 h-12 rounded-xl bg-[#E91E8F]/20 border border-[#E91E8F]/30 flex items-center justify-center text-[#E91E8F] font-bold text-lg">
                        BAT
                      </div>
                      <div>
                        <span className="text-[11px] font-mono text-[#E91E8F] uppercase tracking-wider font-semibold">Striker (Batter)</span>
                        <h3 className="text-xl font-bold text-white">{h2hData.striker_name}</h3>
                        <span className="text-xs text-slate-400 font-mono">ID: {h2hData.striker_id}</span>
                      </div>
                    </div>

                    {/* VS Badge */}
                    <div className="flex flex-col items-center justify-center">
                      <span className="px-3 py-1 rounded-full bg-[#D6B56D]/20 text-[#D6B56D] border border-[#D6B56D]/30 font-mono font-bold text-xs">
                        VS
                      </span>
                      <span className="text-[10px] text-slate-400 mt-1 font-mono">
                        {h2hData.balls_faced} balls faced
                      </span>
                    </div>

                    {/* Bowler side */}
                    <div className="flex items-center gap-4 text-right justify-end w-full md:w-auto">
                      <div>
                        <span className="text-[11px] font-mono text-cyan-400 uppercase tracking-wider font-semibold">Opponent Bowler</span>
                        <h3 className="text-xl font-bold text-white">{h2hData.bowler_name}</h3>
                        <span className="text-xs text-slate-400 font-mono">ID: {h2hData.bowler_id}</span>
                      </div>
                      <div className="w-12 h-12 rounded-xl bg-cyan-500/20 border border-cyan-500/30 flex items-center justify-center text-cyan-400 font-bold text-lg">
                        BWL
                      </div>
                    </div>
                  </div>

                  {/* Micro-Battle Stats Grid */}
                  <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-3 text-center">
                    <div className="p-3 rounded-lg bg-[#0B132B] border border-[#1A2B50]">
                      <span className="text-[10px] text-slate-400 uppercase tracking-wider block">Balls</span>
                      <span className="text-lg font-mono font-bold text-white">{h2hData.balls_faced}</span>
                    </div>
                    <div className="p-3 rounded-lg bg-[#0B132B] border border-[#1A2B50]">
                      <span className="text-[10px] text-slate-400 uppercase tracking-wider block">Runs Scored</span>
                      <span className="text-lg font-mono font-bold text-emerald-400">{h2hData.runs_scored}</span>
                    </div>
                    <div className="p-3 rounded-lg bg-[#0B132B] border border-[#1A2B50]">
                      <span className="text-[10px] text-slate-400 uppercase tracking-wider block">Dismissals</span>
                      <span className={cn(
                        "text-lg font-mono font-bold",
                        h2hData.dismissals > 0 ? "text-rose-400" : "text-slate-300"
                      )}>
                        {h2hData.dismissals}
                      </span>
                    </div>
                    <div className="p-3 rounded-lg bg-[#0B132B] border border-[#1A2B50]">
                      <span className="text-[10px] text-slate-400 uppercase tracking-wider block">Strike Rate</span>
                      <span className="text-lg font-mono font-bold text-white">{h2hData.strike_rate.toFixed(1)}</span>
                    </div>
                    <div className="p-3 rounded-lg bg-[#0B132B] border border-[#1A2B50]">
                      <span className="text-[10px] text-slate-400 uppercase tracking-wider block">4s / 6s</span>
                      <span className="text-lg font-mono font-bold text-slate-200">{h2hData.fours} / {h2hData.sixes}</span>
                    </div>
                    <div className="p-3 rounded-lg bg-[#0B132B] border border-[#1A2B50]">
                      <span className="text-[10px] text-slate-400 uppercase tracking-wider block">Dot Ball %</span>
                      <span className="text-lg font-mono font-bold text-amber-400">{h2hData.dot_ball_pct.toFixed(1)}%</span>
                    </div>
                    <div className="p-3 rounded-lg bg-[#0B132B] border border-[#1A2B50]">
                      <span className="text-[10px] text-slate-400 uppercase tracking-wider block">Boundary %</span>
                      <span className="text-lg font-mono font-bold text-emerald-400">{h2hData.boundary_pct.toFixed(1)}%</span>
                    </div>
                  </div>

                  {/* Tactical Verdict Pill */}
                  <div className="p-4 rounded-xl bg-[#0B132B]/80 border border-[#1A2B50] flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <Sparkles className="w-4 h-4 text-[#D6B56D]" />
                      <span className="text-xs font-semibold text-slate-200">Micro-Battle Verdict:</span>
                    </div>
                    <div className="text-xs font-mono font-bold">
                      {h2hData.balls_faced === 0 && (
                        <span className="text-slate-400">Zero Direct Deliveries Recorded in Dataset</span>
                      )}
                      {h2hData.balls_faced > 0 && h2hData.dismissals >= 2 && (
                        <span className="text-rose-400">Bowler Dominant — Multiple Dismissals</span>
                      )}
                      {h2hData.balls_faced > 0 && h2hData.dismissals === 0 && h2hData.strike_rate >= 140 && (
                        <span className="text-emerald-400">Batter Dominant — Unbeaten High Strike Rate</span>
                      )}
                      {h2hData.balls_faced > 0 && !(h2hData.dismissals >= 2) && !(h2hData.dismissals === 0 && h2hData.strike_rate >= 140) && (
                        <span className="text-[#D6B56D]">Balanced Contest — Tactical Execution Required</span>
                      )}
                    </div>
                  </div>
                </div>
              ) : null}
            </div>
          </div>

          {/* Module G: Individual Player Multi-Dimensional Tactical Profile */}
          <div className="space-y-4">
            <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 p-5 rounded-xl bg-[#101C37]/60 border border-[#1A2B50]">
              <div>
                <h2 className="text-lg font-bold text-white flex items-center gap-2">
                  <Users className="w-5 h-5 text-[#D6B56D]" />
                  Multi-Dimensional Player Tactical Dossier (Module G)
                </h2>
                <p className="text-xs text-slate-400 mt-1">
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
                    className="w-full bg-[#101C37] text-white text-xs pl-9 pr-4 py-2 rounded-lg border border-[#1A2B50] focus:outline-none focus:border-[#E91E8F]"
                  />
                </div>

                {/* Autocomplete Dropdown */}
                {playerSearchResults.length > 0 && (
                  <div className="absolute top-full left-0 right-0 mt-1 max-h-56 overflow-y-auto bg-[#101C37] border border-[#1A2B50] rounded-xl shadow-2xl z-20 divide-y divide-[#1A2B50]/60">
                    {playerSearchResults.map((p) => (
                      <button
                        key={p.player_id}
                        onClick={() => {
                          setSelectedPlayerId(p.player_id);
                          setPlayerSearchQuery("");
                          setPlayerSearchResults([]);
                        }}
                        className="w-full px-3.5 py-2 text-left text-xs text-slate-200 hover:bg-[#1A2B50] transition-colors flex items-center justify-between"
                      >
                        <span className="font-semibold text-white">{p.player_name}</span>
                        <div className="flex items-center gap-1.5 text-[10px] font-mono text-slate-400">
                          {p.is_batter && <span className="text-[#E91E8F]">BAT</span>}
                          {p.is_bowler && <span className="text-cyan-400">BWL</span>}
                        </div>
                      </button>
                    ))}
                  </div>
                )}
              </div>
            </div>

            {/* Quick Marquee Selection Pills */}
            <div className="flex flex-wrap items-center gap-2">
              <span className="text-xs text-slate-400">Quick Select:</span>
              {MARQUEE_PLAYERS.map((player) => (
                <button
                  key={player.id}
                  onClick={() => setSelectedPlayerId(player.id)}
                  className={cn(
                    "px-3 py-1 rounded-lg text-xs font-semibold border transition-all flex items-center gap-1.5",
                    selectedPlayerId === player.id
                      ? "bg-[#D6B56D] text-[#101C37] border-[#D6B56D] font-bold"
                      : "bg-[#101C37] text-slate-300 border-[#1A2B50] hover:border-slate-500"
                  )}
                >
                  <span>{player.name}</span>
                  <span className="text-[10px] font-mono opacity-70">({player.team})</span>
                </button>
              ))}
            </div>

            {/* Selected Player Dossier Card */}
            {playerProfile && (
              <div className="p-6 rounded-2xl bg-[#101C37]/90 border border-[#1A2B50] shadow-xl space-y-6">
                {/* Dossier Header */}
                <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 pb-4 border-b border-[#1A2B50]">
                  <div className="flex items-center gap-3">
                    <div className="w-12 h-12 rounded-xl bg-gradient-to-tr from-[#E91E8F] to-[#D6B56D] p-0.5 flex items-center justify-center">
                      <div className="w-full h-full bg-[#101C37] rounded-[10px] flex items-center justify-center font-bold text-lg text-white">
                        {playerProfile.player_name.substring(0, 2).toUpperCase()}
                      </div>
                    </div>
                    <div>
                      <h3 className="text-xl font-bold text-white flex items-center gap-2">
                        {playerProfile.player_name}
                        <span className="text-xs font-mono text-slate-400">ID: {playerProfile.player_id}</span>
                      </h3>
                      <div className="flex items-center gap-2 mt-0.5">
                        {playerProfile.is_batter && (
                          <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded bg-[#E91E8F]/20 text-[#E91E8F] border border-[#E91E8F]/30">
                            Batter Profile Active
                          </span>
                        )}
                        {playerProfile.is_bowler && (
                          <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded bg-cyan-500/20 text-cyan-300 border border-cyan-500/30">
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
                    <h4 className="text-sm font-bold text-white flex items-center gap-2">
                      <TrendingUp className="w-4 h-4 text-[#E91E8F]" />
                      Batting Diagnostics & Phase Splits
                    </h4>

                    {/* Batting Overall Stats */}
                    <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
                      <div className="p-3 rounded-xl bg-[#0B132B] border border-[#1A2B50]">
                        <span className="text-[10px] text-slate-400 uppercase block">Total Runs</span>
                        <span className="text-lg font-mono font-bold text-white">{playerProfile.batting_profile.total_runs.toLocaleString()}</span>
                      </div>
                      <div className="p-3 rounded-xl bg-[#0B132B] border border-[#1A2B50]">
                        <span className="text-[10px] text-slate-400 uppercase block">Balls Faced</span>
                        <span className="text-lg font-mono font-bold text-slate-300">{playerProfile.batting_profile.balls_faced.toLocaleString()}</span>
                      </div>
                      <div className="p-3 rounded-xl bg-[#0B132B] border border-[#1A2B50]">
                        <span className="text-[10px] text-slate-400 uppercase block">Strike Rate</span>
                        <span className="text-lg font-mono font-bold text-emerald-400">{playerProfile.batting_profile.strike_rate.toFixed(1)}</span>
                      </div>
                      <div className="p-3 rounded-xl bg-[#0B132B] border border-[#1A2B50]">
                        <span className="text-[10px] text-slate-400 uppercase block">Boundary %</span>
                        <span className="text-lg font-mono font-bold text-emerald-400">{playerProfile.batting_profile.boundary_pct.toFixed(1)}%</span>
                      </div>
                      <div className="p-3 rounded-xl bg-[#0B132B] border border-[#1A2B50]">
                        <span className="text-[10px] text-slate-400 uppercase block">Dot Ball %</span>
                        <span className="text-lg font-mono font-bold text-amber-400">{playerProfile.batting_profile.dot_ball_pct.toFixed(1)}%</span>
                      </div>
                    </div>

                    {/* Batting Phase Breakdown Cards */}
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                      {["Powerplay", "Middle", "Death"].map((phaseName) => {
                        const phase = playerProfile.batting_profile?.phase_splits[phaseName];
                        return (
                          <div key={phaseName} className="p-3.5 rounded-xl bg-[#0B132B]/80 border border-[#1A2B50]">
                            <div className="flex items-center justify-between mb-2">
                              <span className="text-xs font-bold text-white">{phaseName}</span>
                              <span className="text-[10px] font-mono text-slate-400">{phase?.total_balls ?? 0} balls</span>
                            </div>
                            <div className="font-mono text-xs space-y-1">
                              <div className="flex justify-between">
                                <span className="text-slate-400">SR:</span>
                                <span className="text-white font-bold">{phase?.strike_rate ? phase.strike_rate.toFixed(1) : "N/A"}</span>
                              </div>
                              <div className="flex justify-between">
                                <span className="text-slate-400">Runs:</span>
                                <span className="text-slate-200">{phase?.runs ?? 0}</span>
                              </div>
                              <div className="flex justify-between">
                                <span className="text-slate-400">Dismissals:</span>
                                <span className="text-rose-400">{phase?.wickets ?? 0}</span>
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
                  <div className="space-y-4 pt-4 border-t border-[#1A2B50]">
                    <h4 className="text-sm font-bold text-white flex items-center gap-2">
                      <Target className="w-4 h-4 text-cyan-400" />
                      Bowling Mechanics & Variations
                    </h4>

                    {/* Bowling Overall Stats */}
                    <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
                      <div className="p-3 rounded-xl bg-[#0B132B] border border-[#1A2B50]">
                        <span className="text-[10px] text-slate-400 uppercase block">Total Wickets</span>
                        <span className="text-lg font-mono font-bold text-white">{playerProfile.bowling_profile.total_wickets}</span>
                      </div>
                      <div className="p-3 rounded-xl bg-[#0B132B] border border-[#1A2B50]">
                        <span className="text-[10px] text-slate-400 uppercase block">Legal Balls</span>
                        <span className="text-lg font-mono font-bold text-slate-300">{playerProfile.bowling_profile.legal_balls.toLocaleString()}</span>
                      </div>
                      <div className="p-3 rounded-xl bg-[#0B132B] border border-[#1A2B50]">
                        <span className="text-[10px] text-slate-400 uppercase block">Economy Rate</span>
                        <span className="text-lg font-mono font-bold text-cyan-400">{playerProfile.bowling_profile.economy_rate.toFixed(2)}</span>
                      </div>
                      <div className="p-3 rounded-xl bg-[#0B132B] border border-[#1A2B50]">
                        <span className="text-[10px] text-slate-400 uppercase block">Bowling Average</span>
                        <span className="text-lg font-mono font-bold text-slate-200">{playerProfile.bowling_profile.bowling_average ? playerProfile.bowling_profile.bowling_average.toFixed(1) : "N/A"}</span>
                      </div>
                      <div className="p-3 rounded-xl bg-[#0B132B] border border-[#1A2B50]">
                        <span className="text-[10px] text-slate-400 uppercase block">Dot Ball %</span>
                        <span className="text-lg font-mono font-bold text-amber-400">{playerProfile.bowling_profile.dot_ball_pct.toFixed(1)}%</span>
                      </div>
                    </div>

                    {/* Speed Telemetry if Available */}
                    {playerProfile.bowling_profile.speed_profile.mean_speed_kmh && (
                      <div className="p-3.5 rounded-xl bg-cyan-950/20 border border-cyan-800/40 flex items-center justify-between text-xs font-mono">
                        <div className="flex items-center gap-2">
                          <Gauge className="w-4 h-4 text-cyan-400" />
                          <span className="text-slate-300">Mean Radar Release Speed:</span>
                          <span className="text-cyan-300 font-bold">{playerProfile.bowling_profile.speed_profile.mean_speed_kmh.toFixed(1)} km/h</span>
                        </div>
                        <div className="flex items-center gap-2">
                          <span className="text-slate-400">Peak Velocity:</span>
                          <span className="text-amber-300 font-bold">{playerProfile.bowling_profile.speed_profile.max_speed_kmh?.toFixed(1) ?? "N/A"} km/h</span>
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
