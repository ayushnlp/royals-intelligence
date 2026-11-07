"use client";

import { useState, useEffect } from "react";
import {
  CompetitionSeasonSummary,
  MatchSummaryItem,
  MatchScorecardResponse,
  InningsAnalysisResponse,
  PlayerDomesticSeasonStats,
  PlayerPhaseSplitDetail,
  AllRoundContributionResponse,
} from "@/types";
import {
  fetchDomesticCompetitions,
  fetchSeasonMatches,
  fetchSeasonSummary,
  fetchMatchScorecard,
  fetchPlayerDomesticStats,
  fetchPlayerPhaseSplits,
  fetchPlayerAllRoundSummary,
} from "@/lib/api";
import {
  Swords,
  Trophy,
  Calendar,
  Layers,
  ChevronRight,
  TrendingUp,
  Target,
  Shield,
  Activity,
  ArrowUpRight,
  Award,
  Users,
  AlertCircle,
  CheckCircle2,
  Filter,
  BarChart3,
  X,
} from "lucide-react";

export default function DomesticIntelligencePage() {
  const [activeTab, setActiveTab] = useState<"tournaments" | "matches" | "player_profile">("tournaments");
  const [competitions, setCompetitions] = useState<CompetitionSeasonSummary[]>([]);
  const [selectedCompId, setSelectedCompId] = useState<string>("SMAT");
  const [selectedSeason, setSelectedSeason] = useState<string>("2024-25");
  const [loading, setLoading] = useState(true);

  // Match List state
  const [matches, setMatches] = useState<MatchSummaryItem[]>([]);
  const [matchTotal, setMatchTotal] = useState(0);
  const [teamFilter, setTeamFilter] = useState("");
  const [selectedMatchId, setSelectedMatchId] = useState<string | null>(null);
  const [matchScorecard, setMatchScorecard] = useState<MatchScorecardResponse | null>(null);
  const [activeInningsIdx, setActiveInningsIdx] = useState(0);
  const [loadingScorecard, setLoadingScorecard] = useState(false);

  // Player All-Round Profile State
  const [uncappedPlayersList] = useState([
    { id: "uncapped_rr_01", name: "Ashutosh Sharma", team: "Punjab / Railways", role: "Middle-Order Finisher" },
    { id: "uncapped_rr_02", name: "Priyansh Arya", team: "Delhi", role: "Top-Order Batter" },
    { id: "uncapped_rr_03", name: "Vipraj Nigam", team: "Uttar Pradesh", role: "Bowling All-Rounder (Leg-Spin)" },
    { id: "uncapped_rr_04", name: "Abhinandan Singh", team: "Delhi", role: "Right-Arm Medium Fast" },
    { id: "uncapped_rr_05", name: "Digvesh Rathi", team: "Delhi", role: "Right-Arm Off-Spin" },
  ]);
  const [selectedPlayerId, setSelectedPlayerId] = useState("uncapped_rr_01");
  const [allRoundData, setAllRoundData] = useState<AllRoundContributionResponse | null>(null);
  const [playerSeasonStats, setPlayerSeasonStats] = useState<PlayerDomesticSeasonStats[]>([]);
  const [playerPhaseSplits, setPlayerPhaseSplits] = useState<PlayerPhaseSplitDetail[]>([]);
  const [loadingPlayer, setLoadingPlayer] = useState(false);

  // Load competitions on initial mount
  useEffect(() => {
    async function loadComps() {
      setLoading(true);
      const res = await fetchDomesticCompetitions();
      setCompetitions(res);
      setLoading(false);
    }
    loadComps();
  }, []);

  // Load matches when competition or season or team changes
  useEffect(() => {
    async function loadMatches() {
      const res = await fetchSeasonMatches(selectedCompId, selectedSeason, {
        team: teamFilter || undefined,
        page: 1,
        page_size: 20,
      });
      setMatches(res.matches);
      setMatchTotal(res.total);
    }
    loadMatches();
  }, [selectedCompId, selectedSeason, teamFilter]);

  // Load match scorecard when a match is selected
  useEffect(() => {
    if (!selectedMatchId) {
      setMatchScorecard(null);
      return;
    }
    async function loadCard() {
      setLoadingScorecard(true);
      const card = await fetchMatchScorecard(selectedMatchId!);
      setMatchScorecard(card);
      setActiveInningsIdx(0);
      setLoadingScorecard(false);
    }
    loadCard();
  }, [selectedMatchId]);

  // Load player all-round data when player tab is viewed or player changed
  useEffect(() => {
    if (activeTab !== "player_profile") return;
    async function loadProfile() {
      setLoadingPlayer(true);
      const [allRound, stats, splits] = await Promise.all([
        fetchPlayerAllRoundSummary(selectedPlayerId),
        fetchPlayerDomesticStats(selectedPlayerId),
        fetchPlayerPhaseSplits(selectedPlayerId),
      ]);
      setAllRoundData(allRound);
      setPlayerSeasonStats(stats);
      setPlayerPhaseSplits(splits);
      setLoadingPlayer(false);
    }
    loadProfile();
  }, [selectedPlayerId, activeTab]);

  const activeInnings: InningsAnalysisResponse | undefined =
    matchScorecard?.innings && matchScorecard.innings.length > activeInningsIdx
      ? matchScorecard.innings[activeInningsIdx]
      : undefined;

  return (
    <div className="space-y-6">
      {/* Top Header & Context */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
        <div>
          <div className="flex items-center gap-2 mb-2">
            <span className="px-2.5 py-0.5 rounded-full text-[11px] font-mono font-bold bg-[#E91E8F] text-white">
              STAGE 3
            </span>
            <span className="px-2.5 py-0.5 rounded-full text-[11px] font-mono font-semibold bg-[#D6B56D]/20 text-[#8C6D1F] border border-[#D6B56D]/40">
              UNCAPPED SCOPE ONLY
            </span>
            <span className="text-xs text-slate-500 font-mono">SMAT • VHT • Ranji • DPL</span>
          </div>
          <h1 className="text-2xl font-extrabold text-[#101C37] tracking-tight">
            Domestic Season & Match Intelligence
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Format-aware phase diagnostics, ball-by-ball scorecards, partnerships, progression worms,
            and uncompromised all-round dual-contribution tracking for IPL 2027 recruitment.
          </p>
        </div>

        {/* Global Selectors */}
        <div className="flex items-center gap-3">
          <div className="flex flex-col">
            <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-1">
              Competition
            </label>
            <select
              value={selectedCompId}
              onChange={(e) => setSelectedCompId(e.target.value)}
              className="bg-slate-50 border border-slate-200 rounded-xl px-3 py-1.5 text-xs font-semibold text-[#101C37] focus:outline-none focus:ring-2 focus:ring-[#E91E8F]"
            >
              <option value="SMAT">Syed Mushtaq Ali Trophy (T20)</option>
              <option value="VHT">Vijay Hazare Trophy (List A)</option>
              <option value="RANJI">Ranji Trophy (Multi-Day)</option>
              <option value="DPL_T20">Delhi Premier League (T20)</option>
              <option value="UP_T20">UP T20 League (T20)</option>
            </select>
          </div>

          <div className="flex flex-col">
            <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-1">
              Season
            </label>
            <select
              value={selectedSeason}
              onChange={(e) => setSelectedSeason(e.target.value)}
              className="bg-slate-50 border border-slate-200 rounded-xl px-3 py-1.5 text-xs font-semibold text-[#101C37] focus:outline-none focus:ring-2 focus:ring-[#E91E8F]"
            >
              <option value="2024-25">2024-25</option>
              <option value="2025-26">2025-26</option>
            </select>
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="flex items-center gap-2 border-b border-slate-200 pb-2">
        <button
          onClick={() => setActiveTab("tournaments")}
          className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-bold transition-colors ${
            activeTab === "tournaments"
              ? "bg-[#101C37] text-white shadow-sm"
              : "text-slate-600 hover:bg-slate-100"
          }`}
        >
          <Trophy size={15} />
          Tournament Directory ({competitions.length})
        </button>
        <button
          onClick={() => setActiveTab("matches")}
          className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-bold transition-colors ${
            activeTab === "matches"
              ? "bg-[#101C37] text-white shadow-sm"
              : "text-slate-600 hover:bg-slate-100"
          }`}
        >
          <Swords size={15} />
          Match Intelligence & Scorecards ({matchTotal})
        </button>
        <button
          onClick={() => setActiveTab("player_profile")}
          className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-bold transition-colors ${
            activeTab === "player_profile"
              ? "bg-[#101C37] text-white shadow-sm"
              : "text-slate-600 hover:bg-slate-100"
          }`}
        >
          <Target size={15} />
          All-Round Dual Contribution & Phase Splits
        </button>
      </div>

      {/* TAB 1: TOURNAMENT DIRECTORY */}
      {activeTab === "tournaments" && (
        <div className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
            {competitions.map((comp) => (
              <div
                key={comp.competition_id}
                onClick={() => {
                  setSelectedCompId(comp.competition_id);
                  setSelectedSeason(comp.season);
                  setActiveTab("matches");
                }}
                className={`group p-5 rounded-2xl bg-white border cursor-pointer transition-all hover:shadow-md ${
                  selectedCompId === comp.competition_id
                    ? "border-[#E91E8F] ring-2 ring-[#E91E8F]/20"
                    : "border-slate-200 hover:border-slate-300"
                }`}
              >
                <div className="flex items-center justify-between mb-3">
                  <span className="px-2.5 py-0.5 rounded-full text-[10px] font-mono font-bold bg-slate-100 text-[#101C37]">
                    {comp.competition_type}
                  </span>
                  <span className="text-xs font-mono font-bold text-[#E91E8F]">{comp.season}</span>
                </div>

                <h3 className="font-bold text-base text-[#101C37] group-hover:text-[#E91E8F] transition-colors mb-1">
                  {comp.competition_name}
                </h3>
                <p className="text-xs text-slate-500 mb-4">Governing Body: {comp.governing_body}</p>

                <div className="grid grid-cols-3 gap-2 py-3 px-3 bg-slate-50 rounded-xl border border-slate-100 text-center mb-4">
                  <div>
                    <div className="text-[10px] uppercase font-bold text-slate-400">Matches</div>
                    <div className="text-sm font-extrabold text-[#101C37]">{comp.match_count}</div>
                  </div>
                  <div>
                    <div className="text-[10px] uppercase font-bold text-slate-400">Teams</div>
                    <div className="text-sm font-extrabold text-[#101C37]">{comp.teams_count}</div>
                  </div>
                  <div>
                    <div className="text-[10px] uppercase font-bold text-slate-400">Ball-by-Ball</div>
                    <div className="text-sm font-extrabold text-emerald-600">
                      {comp.has_ball_by_ball ? "Verified" : "Pending"}
                    </div>
                  </div>
                </div>

                <div className="flex items-center justify-between text-xs text-slate-500 pt-2 border-t border-slate-100">
                  <span className="flex items-center gap-1 text-[11px]">
                    <CheckCircle2 size={13} className="text-emerald-500" />
                    {comp.validation_pass_rate}% validated
                  </span>
                  <span className="flex items-center gap-1 font-semibold text-[#101C37] group-hover:translate-x-1 transition-transform">
                    Explore Matches <ChevronRight size={14} />
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* TAB 2: MATCH INTELLIGENCE & SCORECARDS */}
      {activeTab === "matches" && (
        <div className="space-y-6">
          {/* Filter Bar */}
          <div className="flex flex-col sm:flex-row items-center justify-between gap-4 bg-white p-4 rounded-xl border border-slate-200">
            <div className="flex items-center gap-2 w-full sm:w-auto">
              <Filter size={15} className="text-slate-400" />
              <input
                type="text"
                placeholder="Filter by team (e.g. Punjab, Delhi)..."
                value={teamFilter}
                onChange={(e) => setTeamFilter(e.target.value)}
                className="bg-slate-50 border border-slate-200 rounded-lg px-3 py-1.5 text-xs text-[#101C37] placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-[#E91E8F] w-full sm:w-64"
              />
            </div>
            <div className="text-xs text-slate-500">
              Showing <span className="font-bold text-[#101C37]">{matches.length}</span> matches for{" "}
              <span className="font-bold text-[#E91E8F]">{selectedCompId}</span> ({selectedSeason})
            </div>
          </div>

          {/* Matches Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {matches.map((m) => (
              <div
                key={m.match_id}
                className="p-5 rounded-2xl bg-white border border-slate-200 hover:border-slate-300 transition-shadow shadow-sm flex flex-col justify-between"
              >
                <div>
                  <div className="flex items-center justify-between mb-3 text-xs text-slate-500">
                    <span className="flex items-center gap-1 font-mono text-[11px]">
                      <Calendar size={13} className="text-[#D6B56D]" />
                      {m.match_date}
                    </span>
                    <span className="px-2 py-0.5 rounded text-[10px] font-mono font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200">
                      Ball-by-ball Verified
                    </span>
                  </div>

                  <div className="flex items-center justify-between py-2 border-y border-slate-100 my-2">
                    <div className="flex items-center gap-2">
                      <div className="w-8 h-8 rounded-lg bg-[#101C37] text-white flex items-center justify-center font-bold text-xs">
                        {m.home_team_code.slice(0, 3)}
                      </div>
                      <span className="font-bold text-sm text-[#101C37]">{m.home_team_name}</span>
                    </div>
                    <span className="text-xs font-mono font-bold text-slate-400">vs</span>
                    <div className="flex items-center gap-2">
                      <span className="font-bold text-sm text-[#101C37]">{m.away_team_name}</span>
                      <div className="w-8 h-8 rounded-lg bg-[#E91E8F] text-white flex items-center justify-center font-bold text-xs">
                        {m.away_team_code.slice(0, 3)}
                      </div>
                    </div>
                  </div>

                  <div className="text-xs text-slate-600 mt-2">
                    <span className="font-bold text-[#101C37]">Outcome:</span> {m.result_outcome}
                  </div>
                  <div className="text-[11px] text-slate-400 mt-1">
                    Venue: {m.venue_name}, {m.venue_city}
                  </div>
                </div>

                <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between">
                  <span className="text-[11px] font-mono text-slate-400">ID: {m.external_match_id}</span>
                  <button
                    onClick={() => setSelectedMatchId(m.match_id)}
                    className="flex items-center gap-1 text-xs font-bold text-[#E91E8F] hover:text-[#c2185b] px-3 py-1.5 rounded-lg bg-pink-50 hover:bg-pink-100 transition-colors"
                  >
                    Inspect Scorecard & Phases <ChevronRight size={14} />
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* MATCH SCORECARD MODAL / OVERLAY */}
      {selectedMatchId && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4 backdrop-blur-sm overflow-y-auto">
          <div className="bg-white rounded-2xl max-w-5xl w-full max-h-[92vh] flex flex-col shadow-2xl overflow-hidden border border-slate-200">
            {/* Modal Header */}
            <div className="flex items-center justify-between p-5 bg-[#101C37] text-white">
              <div>
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-[#E91E8F] text-white font-bold">
                    {matchScorecard?.competition_type || "MATCH"}
                  </span>
                  <span className="text-xs text-slate-300 font-mono">
                    {matchScorecard?.competition_name} ({matchScorecard?.season})
                  </span>
                </div>
                <h2 className="text-lg font-bold text-white">
                  {matchScorecard?.home_team?.name} vs {matchScorecard?.away_team?.name}
                </h2>
                <p className="text-xs text-slate-300">
                  {matchScorecard?.venue_name}, {matchScorecard?.venue_city} • {matchScorecard?.match_date}
                </p>
              </div>
              <button
                onClick={() => setSelectedMatchId(null)}
                className="p-2 text-slate-300 hover:text-white rounded-lg hover:bg-white/10 transition-colors"
              >
                <X size={20} />
              </button>
            </div>

            {loadingScorecard ? (
              <div className="p-12 text-center text-xs text-slate-500 font-mono">
                Loading format-aware ball-by-ball analysis...
              </div>
            ) : matchScorecard && activeInnings ? (
              <div className="flex-1 overflow-y-auto p-6 space-y-6">
                {/* Toss & Outcome summary bar */}
                <div className="flex flex-wrap items-center justify-between gap-3 p-4 bg-slate-50 rounded-xl border border-slate-200 text-xs">
                  <div>
                    <span className="font-bold text-[#101C37]">Toss:</span> {matchScorecard.toss_winner_code} won and elected to {matchScorecard.toss_decision}
                  </div>
                  <div>
                    <span className="font-bold text-[#101C37]">Winner:</span> {matchScorecard.winner_team_code} ({matchScorecard.win_margin})
                  </div>
                  {matchScorecard.player_of_match && (
                    <div className="flex items-center gap-1 font-bold text-[#E91E8F]">
                      <Award size={14} /> POTM: {matchScorecard.player_of_match}
                    </div>
                  )}
                </div>

                {/* Innings Switcher */}
                <div className="flex items-center gap-2 border-b border-slate-200 pb-2">
                  {matchScorecard.innings.map((inn, idx) => (
                    <button
                      key={inn.innings_number}
                      onClick={() => setActiveInningsIdx(idx)}
                      className={`px-4 py-2 rounded-xl text-xs font-bold transition-colors ${
                        activeInningsIdx === idx
                          ? "bg-[#101C37] text-white"
                          : "bg-slate-100 text-slate-600 hover:bg-slate-200"
                      }`}
                    >
                      Innings {inn.innings_number}: {inn.batting_team_name} ({inn.total_runs}/{inn.wickets} in {inn.overs_completed} ov)
                    </button>
                  ))}
                </div>

                {/* Format-Aware Phase Diagnostics Cards */}
                <div>
                  <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-3">
                    Format-Aware Phase Leverage Diagnostics
                  </h4>
                  <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                    {activeInnings.phase_summaries.map((phase) => (
                      <div
                        key={phase.phase_name}
                        className="p-4 rounded-xl bg-gradient-to-br from-slate-50 to-slate-100 border border-slate-200"
                      >
                        <div className="flex items-center justify-between mb-1">
                          <span className="text-xs font-bold text-[#101C37]">{phase.phase_name}</span>
                          <span className="text-[10px] font-mono text-slate-500">{phase.overs_range}</span>
                        </div>
                        <div className="text-xl font-black text-[#101C37] my-1">
                          {phase.runs} <span className="text-xs font-normal text-slate-500">runs / {phase.wickets} wkts</span>
                        </div>
                        <div className="flex items-center justify-between text-[11px] text-slate-600 pt-2 border-t border-slate-200/60">
                          <span>Run Rate: {phase.run_rate}</span>
                          <span>Boundary: {phase.boundary_runs} runs</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Batting Scorecard */}
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400">
                      Batting Scorecard — {activeInnings.batting_team_name}
                    </h4>
                    <span className="text-xs font-mono text-slate-500">
                      Total: {activeInnings.total_runs}/{activeInnings.wickets} ({activeInnings.overs_completed} ov, RR {activeInnings.run_rate})
                    </span>
                  </div>
                  <div className="overflow-x-auto border border-slate-200 rounded-xl">
                    <table className="w-full text-left text-xs">
                      <thead className="bg-slate-50 text-slate-600 font-semibold border-b border-slate-200">
                        <tr>
                          <th className="py-2.5 px-3">Batter</th>
                          <th className="py-2.5 px-3">Dismissal</th>
                          <th className="py-2.5 px-3 text-right">R</th>
                          <th className="py-2.5 px-3 text-right">B</th>
                          <th className="py-2.5 px-3 text-right">4s</th>
                          <th className="py-2.5 px-3 text-right">6s</th>
                          <th className="py-2.5 px-3 text-right">SR</th>
                          <th className="py-2.5 px-3 text-right">PP (R/B)</th>
                          <th className="py-2.5 px-3 text-right">Death (R/B)</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-slate-100">
                        {activeInnings.batting_scorecards.map((b) => (
                          <tr key={b.player_id} className="hover:bg-slate-50/80">
                            <td className="py-2.5 px-3 font-semibold text-[#101C37] flex items-center gap-1.5">
                              {b.player_name}
                              {b.is_uncapped && (
                                <span className="px-1.5 py-0.2 rounded text-[9px] font-mono font-bold bg-[#E91E8F]/15 text-[#E91E8F]">
                                  UNCAPPED
                                </span>
                              )}
                            </td>
                            <td className="py-2.5 px-3 text-slate-500 text-[11px]">
                              {b.is_out ? (
                                <span>
                                  {b.dismissal_kind} {b.bowler_name ? `b ${b.bowler_name}` : ""}{" "}
                                  {b.fielder_name ? `c ${b.fielder_name}` : ""}
                                </span>
                              ) : (
                                <span className="font-semibold text-emerald-600">not out</span>
                              )}
                            </td>
                            <td className="py-2.5 px-3 text-right font-extrabold text-[#101C37]">{b.runs}</td>
                            <td className="py-2.5 px-3 text-right text-slate-600">{b.balls_faced}</td>
                            <td className="py-2.5 px-3 text-right text-slate-600">{b.fours}</td>
                            <td className="py-2.5 px-3 text-right text-slate-600">{b.sixes}</td>
                            <td className="py-2.5 px-3 text-right font-mono font-bold text-[#101C37]">{b.strike_rate}</td>
                            <td className="py-2.5 px-3 text-right font-mono text-slate-500 text-[11px]">
                              {b.powerplay_runs !== undefined ? `${b.powerplay_runs}/${b.powerplay_balls}` : "-"}
                            </td>
                            <td className="py-2.5 px-3 text-right font-mono text-slate-500 text-[11px]">
                              {b.death_runs !== undefined ? `${b.death_runs}/${b.death_balls}` : "-"}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                  <div className="text-[11px] text-slate-500 mt-2 px-1">
                    Extras: <span className="font-semibold text-[#101C37]">{activeInnings.extras_total}</span> (w: {activeInnings.extras_breakdown.wides || 0}, nb: {activeInnings.extras_breakdown.noballs || 0}, b: {activeInnings.extras_breakdown.byes || 0}, lb: {activeInnings.extras_breakdown.legbyes || 0})
                  </div>
                </div>

                {/* Bowling Scorecard */}
                <div>
                  <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">
                    Bowling Scorecard — {activeInnings.bowling_team_name}
                  </h4>
                  <div className="overflow-x-auto border border-slate-200 rounded-xl">
                    <table className="w-full text-left text-xs">
                      <thead className="bg-slate-50 text-slate-600 font-semibold border-b border-slate-200">
                        <tr>
                          <th className="py-2.5 px-3">Bowler</th>
                          <th className="py-2.5 px-3 text-right">O</th>
                          <th className="py-2.5 px-3 text-right">M</th>
                          <th className="py-2.5 px-3 text-right">R</th>
                          <th className="py-2.5 px-3 text-right">W (Bowler)</th>
                          <th className="py-2.5 px-3 text-right">Econ</th>
                          <th className="py-2.5 px-3 text-right">Dots</th>
                          <th className="py-2.5 px-3 text-right">Extras</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-slate-100">
                        {activeInnings.bowling_scorecards.map((bw) => (
                          <tr key={bw.player_id} className="hover:bg-slate-50/80">
                            <td className="py-2.5 px-3 font-semibold text-[#101C37] flex items-center gap-1.5">
                              {bw.player_name}
                              {bw.is_uncapped && (
                                <span className="px-1.5 py-0.2 rounded text-[9px] font-mono font-bold bg-[#E91E8F]/15 text-[#E91E8F]">
                                  UNCAPPED
                                </span>
                              )}
                            </td>
                            <td className="py-2.5 px-3 text-right text-slate-600">{bw.overs}</td>
                            <td className="py-2.5 px-3 text-right text-slate-600">{bw.maidens}</td>
                            <td className="py-2.5 px-3 text-right text-slate-600">{bw.runs_conceded}</td>
                            <td className="py-2.5 px-3 text-right font-extrabold text-[#E91E8F]">{bw.bowler_wickets}</td>
                            <td className="py-2.5 px-3 text-right font-mono font-bold text-[#101C37]">{bw.economy_rate}</td>
                            <td className="py-2.5 px-3 text-right text-slate-600">{bw.dot_balls ?? "-"}</td>
                            <td className="py-2.5 px-3 text-right text-slate-500 font-mono text-[11px]">
                              w: {bw.wides}, nb: {bw.noballs}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                  <div className="text-[10px] text-slate-400 mt-1 italic">
                    * Wickets credited strictly exclude run-outs per platform integrity rules.
                  </div>
                </div>

                {/* Fall of Wickets & Partnerships Grid */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {/* Fall of Wickets */}
                  <div className="p-4 rounded-xl border border-slate-200 bg-slate-50/60">
                    <h5 className="text-xs font-bold text-[#101C37] mb-2">Fall of Wickets (FoW)</h5>
                    <div className="space-y-1.5 max-h-48 overflow-y-auto pr-1">
                      {activeInnings.fall_of_wickets.map((fow) => (
                        <div
                          key={fow.wicket_number}
                          className="flex items-center justify-between text-xs py-1 px-2 rounded bg-white border border-slate-200/80"
                        >
                          <span className="font-bold text-[#101C37]">
                            {fow.runs}/{fow.wicket_number}
                          </span>
                          <span className="text-slate-600">{fow.batter_out_name}</span>
                          <span className="font-mono text-slate-400 text-[11px]">{fow.over_display} ov</span>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Partnerships */}
                  <div className="p-4 rounded-xl border border-slate-200 bg-slate-50/60">
                    <h5 className="text-xs font-bold text-[#101C37] mb-2">Partnerships</h5>
                    <div className="space-y-1.5 max-h-48 overflow-y-auto pr-1">
                      {activeInnings.partnerships.map((p) => (
                        <div
                          key={p.wicket_number}
                          className="text-xs p-2 rounded bg-white border border-slate-200/80"
                        >
                          <div className="flex items-center justify-between font-bold text-[#101C37] mb-1">
                            <span>
                              {p.wicket_number === 1 ? "1st" : p.wicket_number === 2 ? "2nd" : p.wicket_number === 3 ? "3rd" : `${p.wicket_number}th`} Wicket: {p.runs} runs ({p.balls}b)
                            </span>
                            {p.is_unbroken && (
                              <span className="text-[10px] text-emerald-600 font-mono">Unbroken</span>
                            )}
                          </div>
                          <div className="text-[11px] text-slate-500 flex justify-between">
                            <span>{p.batter_1_name}: {p.batter_1_runs} ({p.batter_1_balls}b)</span>
                            <span>{p.batter_2_name}: {p.batter_2_runs} ({p.batter_2_balls}b)</span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>

                {/* Over progression worm data */}
                <div>
                  <h5 className="text-xs font-bold text-[#101C37] mb-2">
                    Over-by-Over Progression (Scoring Trajectory)
                  </h5>
                  <div className="flex items-center gap-1.5 overflow-x-auto pb-2">
                    {activeInnings.scoring_progression.map((ov) => (
                      <div
                        key={ov.over_number}
                        className="flex-shrink-0 w-12 text-center p-2 rounded-lg bg-slate-50 border border-slate-200"
                      >
                        <div className="text-[10px] text-slate-400 font-mono">Ov {ov.over_number}</div>
                        <div className="text-xs font-extrabold text-[#101C37]">+{ov.runs_in_over}</div>
                        <div className="text-[10px] font-mono text-slate-600 mt-0.5">
                          {ov.cumulative_runs}/{ov.cumulative_wickets}
                        </div>
                        {ov.wickets_in_over > 0 && (
                          <div className="text-[9px] font-bold text-[#E91E8F] mt-0.5">
                            {ov.wickets_in_over}w
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            ) : null}

            {/* Modal Footer */}
            <div className="p-4 bg-slate-50 border-t border-slate-200 flex justify-between items-center text-xs text-slate-500">
              <span className="font-mono text-[11px]">Provenance: Rajasthan Royals Analytics Pipeline (Stage 3)</span>
              <button
                onClick={() => setSelectedMatchId(null)}
                className="px-4 py-1.5 rounded-lg bg-slate-200 text-[#101C37] font-bold hover:bg-slate-300 transition-colors"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}

      {/* TAB 3: ALL-ROUND DUAL CONTRIBUTION & PHASE SPLITS */}
      {activeTab === "player_profile" && (
        <div className="space-y-6">
          {/* Player Selector Bar */}
          <div className="flex flex-wrap items-center gap-2 p-4 bg-white rounded-xl border border-slate-200">
            <span className="text-xs font-bold text-slate-400 uppercase tracking-wider mr-2">
              Select Uncapped Talent:
            </span>
            {uncappedPlayersList.map((p) => (
              <button
                key={p.id}
                onClick={() => setSelectedPlayerId(p.id)}
                className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
                  selectedPlayerId === p.id
                    ? "bg-[#E91E8F] text-white shadow-sm"
                    : "bg-slate-100 text-slate-700 hover:bg-slate-200"
                }`}
              >
                {p.name}
              </button>
            ))}
          </div>

          {loadingPlayer ? (
            <div className="p-12 text-center text-xs text-slate-500 font-mono">
              Loading domestic intelligence dossier...
            </div>
          ) : (
            <>
              {/* Dual-Discipline Summary Card */}
              {allRoundData && (
                <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-6">
                  <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-100 pb-5">
                    <div>
                      <div className="flex items-center gap-2 mb-1">
                        <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-[#D6B56D]/20 text-[#8C6D1F]">
                          {allRoundData.eligibility_status}
                        </span>
                        <span className="text-xs font-mono text-slate-400">
                          {allRoundData.canonical_id}
                        </span>
                      </div>
                      <h2 className="text-2xl font-black text-[#101C37]">{allRoundData.full_name}</h2>
                      <p className="text-xs text-slate-500 mt-1">
                        Primary Role: <span className="font-semibold text-[#101C37]">{allRoundData.primary_role}</span> • Team: {allRoundData.domestic_team}
                      </p>
                    </div>

                    {/* Transparent Archetype & Sample Size */}
                    <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 text-right">
                      <div className="text-[10px] font-bold uppercase tracking-wider text-slate-400">
                        Evidence-Based Archetype
                      </div>
                      <div className="text-sm font-extrabold text-[#E91E8F] mt-0.5">
                        {allRoundData.role_archetype_context}
                      </div>
                      <div className="text-[11px] font-mono text-slate-500 mt-1">
                        Sample: {allRoundData.sample_size.matches} matches | {allRoundData.sample_size.innings_batted} inn | {allRoundData.sample_size.overs_bowled} ov
                      </div>
                    </div>
                  </div>

                  {/* Independent Batting vs Bowling Dual Grid */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {/* Batting Dimension */}
                    <div className="p-5 rounded-xl border border-slate-200 bg-pink-50/20">
                      <div className="flex items-center justify-between mb-4">
                        <div className="flex items-center gap-2">
                          <TrendingUp size={16} className="text-[#E91E8F]" />
                          <h4 className="text-sm font-bold text-[#101C37]">Batting Profile</h4>
                        </div>
                        <span className="text-xs font-mono text-slate-500">
                          {allRoundData.batting_summary.innings} innings
                        </span>
                      </div>
                      <div className="grid grid-cols-3 gap-3 text-center">
                        <div className="p-3 bg-white rounded-lg border border-slate-100">
                          <div className="text-[10px] uppercase font-bold text-slate-400">Runs</div>
                          <div className="text-base font-black text-[#101C37]">{allRoundData.batting_summary.runs}</div>
                        </div>
                        <div className="p-3 bg-white rounded-lg border border-slate-100">
                          <div className="text-[10px] uppercase font-bold text-slate-400">Strike Rate</div>
                          <div className="text-base font-black text-[#101C37]">{allRoundData.batting_summary.strike_rate}</div>
                        </div>
                        <div className="p-3 bg-white rounded-lg border border-slate-100">
                          <div className="text-[10px] uppercase font-bold text-slate-400">Average</div>
                          <div className="text-base font-black text-[#101C37]">
                            {allRoundData.batting_summary.average ?? "N/A (0 outs)"}
                          </div>
                        </div>
                      </div>
                      <div className="flex items-center justify-between text-xs text-slate-500 mt-4 px-1">
                        <span>Boundaries: {allRoundData.batting_summary.boundary_percentage}%</span>
                        <span>High Score: {allRoundData.batting_summary.high_score}</span>
                      </div>
                    </div>

                    {/* Bowling Dimension */}
                    <div className="p-5 rounded-xl border border-slate-200 bg-blue-50/20">
                      <div className="flex items-center justify-between mb-4">
                        <div className="flex items-center gap-2">
                          <Target size={16} className="text-blue-600" />
                          <h4 className="text-sm font-bold text-[#101C37]">Bowling Profile</h4>
                        </div>
                        <span className="text-xs font-mono text-slate-500">
                          {allRoundData.bowling_summary.overs_bowled} overs
                        </span>
                      </div>
                      <div className="grid grid-cols-3 gap-3 text-center">
                        <div className="p-3 bg-white rounded-lg border border-slate-100">
                          <div className="text-[10px] uppercase font-bold text-slate-400">Wickets</div>
                          <div className="text-base font-black text-[#101C37]">
                            {allRoundData.bowling_summary.wickets ?? 0}
                          </div>
                        </div>
                        <div className="p-3 bg-white rounded-lg border border-slate-100">
                          <div className="text-[10px] uppercase font-bold text-slate-400">Economy</div>
                          <div className="text-base font-black text-[#101C37]">{allRoundData.bowling_summary.economy}</div>
                        </div>
                        <div className="p-3 bg-white rounded-lg border border-slate-100">
                          <div className="text-[10px] uppercase font-bold text-slate-400">Average</div>
                          <div className="text-base font-black text-[#101C37]">
                            {allRoundData.bowling_summary.average ?? "N/A (0 wkts)"}
                          </div>
                        </div>
                      </div>
                      <div className="flex items-center justify-between text-xs text-slate-500 mt-4 px-1">
                        <span>Maidens: {allRoundData.bowling_summary.maidens ?? 0}</span>
                        <span>Catches: {allRoundData.fielding_summary?.catches ?? 0}</span>
                      </div>
                    </div>
                  </div>

                  <div className="p-3 bg-slate-50 rounded-xl border border-slate-200/80 text-[11px] text-slate-500 flex items-center gap-2">
                    <Shield size={14} className="text-[#D6B56D]" />
                    <span>
                      Integrity Policy: royals-intelligence avoids composite ratings or weighted formulas to represent dual contributors. Independent metrics are preserved with transparent sample sizes.
                    </span>
                  </div>
                </div>
              )}

              {/* Granular Phase Splits Table */}
              <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="text-base font-bold text-[#101C37]">
                      Granular Phase Performance Splits
                    </h3>
                    <p className="text-xs text-slate-500">
                      Powerplay (overs 0-5), Middle (overs 6-14), and Death (overs 15-19) breakdown
                    </p>
                  </div>
                  <BarChart3 size={18} className="text-slate-400" />
                </div>

                <div className="overflow-x-auto border border-slate-200 rounded-xl">
                  <table className="w-full text-left text-xs">
                    <thead className="bg-slate-50 text-slate-600 font-semibold border-b border-slate-200">
                      <tr>
                        <th className="py-2.5 px-3">Phase</th>
                        <th className="py-2.5 px-3">Overs</th>
                        <th className="py-2.5 px-3 text-right">Bat Runs</th>
                        <th className="py-2.5 px-3 text-right">Balls</th>
                        <th className="py-2.5 px-3 text-right">Bat SR</th>
                        <th className="py-2.5 px-3 text-right">4s / 6s</th>
                        <th className="py-2.5 px-3 text-right">Bowl Overs</th>
                        <th className="py-2.5 px-3 text-right">Bowl Wkts</th>
                        <th className="py-2.5 px-3 text-right">Bowl Econ</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100">
                      {playerPhaseSplits.map((split) => (
                        <tr key={split.phase} className="hover:bg-slate-50/80">
                          <td className="py-2.5 px-3 font-bold text-[#101C37]">{split.phase}</td>
                          <td className="py-2.5 px-3 font-mono text-slate-500">{split.overs_range}</td>
                          <td className="py-2.5 px-3 text-right font-extrabold text-[#101C37]">{split.batting_runs}</td>
                          <td className="py-2.5 px-3 text-right text-slate-600">{split.batting_balls}</td>
                          <td className="py-2.5 px-3 text-right font-mono font-bold text-[#E91E8F]">{split.batting_strike_rate}</td>
                          <td className="py-2.5 px-3 text-right text-slate-600">{split.batting_fours} / {split.batting_sixes}</td>
                          <td className="py-2.5 px-3 text-right text-slate-600">{split.bowling_overs}</td>
                          <td className="py-2.5 px-3 text-right font-bold text-blue-600">{split.bowler_wickets}</td>
                          <td className="py-2.5 px-3 text-right font-mono text-slate-600">{split.bowling_economy}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </>
          )}
        </div>
      )}
    </div>
  );
}

