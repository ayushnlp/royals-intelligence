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
  DomesticPlayerSummary,
} from "@/types";
import {
  fetchDomesticCompetitions,
  fetchSeasonMatches,
  fetchSeasonSummary,
  fetchMatchScorecard,
  fetchPlayerDomesticStats,
  fetchPlayerPhaseSplits,
  fetchPlayerAllRoundSummary,
  fetchDomesticPlayers,
} from "@/lib/api";
import {
  Swords,
  Trophy,
  Calendar,
  Layers,
  ChevronRight,
  ChevronLeft,
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
  Search,
  Database,
  RefreshCw,
} from "lucide-react";
import { cn } from "@/lib/utils";

export default function DomesticIntelligencePage() {
  const [activeTab, setActiveTab] = useState<"tournaments" | "matches" | "player_profile">("tournaments");
  const [competitions, setCompetitions] = useState<CompetitionSeasonSummary[]>([]);
  const [selectedCompId, setSelectedCompId] = useState<string>("ipl");
  const [selectedSeason, setSelectedSeason] = useState<string>("2024");
  const [loading, setLoading] = useState(true);

  // Match List state
  const [matches, setMatches] = useState<MatchSummaryItem[]>([]);
  const [matchTotal, setMatchTotal] = useState(0);
  const [teamFilter, setTeamFilter] = useState("");
  const [selectedMatchId, setSelectedMatchId] = useState<string | null>(null);
  const [matchScorecard, setMatchScorecard] = useState<MatchScorecardResponse | null>(null);
  const [activeInningsIdx, setActiveInningsIdx] = useState(0);
  const [loadingScorecard, setLoadingScorecard] = useState(false);

  // Player Discovery & Dossier State
  const [domesticPlayers, setDomesticPlayers] = useState<DomesticPlayerSummary[]>([]);
  const [playerTotal, setPlayerTotal] = useState(0);
  const [playerPage, setPlayerPage] = useState(1);
  const [playerSearch, setPlayerSearch] = useState("");
  const [playerEligibilityFilter, setPlayerEligibilityFilter] = useState<string>("ALL");
  const [playerRoleFilter, setPlayerRoleFilter] = useState<string>("");
  const [selectedPlayerId, setSelectedPlayerId] = useState<string>("");
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [eligibilityCounts, setEligibilityCounts] = useState<{
    ALL: number;
    VERIFIED_UNCAPPED: number;
    PENDING_VERIFICATION: number;
  }>({ ALL: 0, VERIFIED_UNCAPPED: 0, PENDING_VERIFICATION: 0 });
  const [allRoundData, setAllRoundData] = useState<AllRoundContributionResponse | null>(null);
  const [playerSeasonStats, setPlayerSeasonStats] = useState<PlayerDomesticSeasonStats[]>([]);
  const [playerPhaseSplits, setPlayerPhaseSplits] = useState<PlayerPhaseSplitDetail[]>([]);
  const [loadingPlayer, setLoadingPlayer] = useState(false);
  const [loadingPlayerList, setLoadingPlayerList] = useState(false);

  // Load live eligibility totals on mount
  useEffect(() => {
    let isCurrent = true;
    async function loadCounts() {
      try {
        const [allRes, uncappedRes, pendingRes] = await Promise.all([
          fetchDomesticPlayers({ page: 1, page_size: 1, eligibility_status: "ALL" }),
          fetchDomesticPlayers({ page: 1, page_size: 1, eligibility_status: "VERIFIED_UNCAPPED" }),
          fetchDomesticPlayers({ page: 1, page_size: 1, eligibility_status: "PENDING_VERIFICATION" }),
        ]);
        if (isCurrent) {
          setEligibilityCounts({
            ALL: allRes.total,
            VERIFIED_UNCAPPED: uncappedRes.total,
            PENDING_VERIFICATION: pendingRes.total,
          });
        }
      } catch (err) {
        if (isCurrent) console.warn("Failed to load domestic eligibility counts:", err);
      }
    }
    loadCounts();
    return () => {
      isCurrent = false;
    };
  }, []);

  // Load competitions on initial mount
  const loadComps = async () => {
    setLoading(true);
    setErrorMsg(null);
    try {
      const res = await fetchDomesticCompetitions();
      setCompetitions(res);
      if (res.length > 0) {
        setSelectedCompId((prev) => (!prev || !res.some((c) => c.competition_id === prev) ? res[0].competition_id : prev));
        setSelectedSeason((prev) => (!prev || !res.some((c) => c.season === prev) ? res[0].season : prev));
      }
    } catch (err: any) {
      setErrorMsg(err.message || "Failed to load domestic competitions.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadComps();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Load matches when competition or season or team changes
  useEffect(() => {
    let isCurrent = true;
    async function loadMatches() {
      try {
        const res = await fetchSeasonMatches(selectedCompId, selectedSeason, {
          team: teamFilter || undefined,
          page: 1,
          page_size: 20,
        });
        if (isCurrent) {
          setMatches(res.matches);
          setMatchTotal(res.total);
        }
      } catch (err) {
        if (isCurrent) {
          console.warn("Failed to load season matches:", err);
          setMatches([]);
          setMatchTotal(0);
        }
      }
    }
    loadMatches();
    return () => {
      isCurrent = false;
    };
  }, [selectedCompId, selectedSeason, teamFilter]);

  // Load match scorecard when a match is selected
  useEffect(() => {
    if (!selectedMatchId) {
      setMatchScorecard(null);
      return;
    }
    let isCurrent = true;
    async function loadCard() {
      setLoadingScorecard(true);
      try {
        const card = await fetchMatchScorecard(selectedMatchId!);
        if (isCurrent) {
          setMatchScorecard(card);
          setActiveInningsIdx(0);
        }
      } catch (err) {
        if (isCurrent) {
          console.warn("Failed to load match scorecard:", err);
          setMatchScorecard(null);
        }
      } finally {
        if (isCurrent) setLoadingScorecard(false);
      }
    }
    loadCard();
    return () => {
      isCurrent = false;
    };
  }, [selectedMatchId]);

  // Load dynamic player discovery catalog
  useEffect(() => {
    let isCurrent = true;
    async function loadPlayers() {
      setLoadingPlayerList(true);
      try {
        const res = await fetchDomesticPlayers({
          page: playerPage,
          page_size: 12,
          search: playerSearch || undefined,
          eligibility_status: playerEligibilityFilter,
          role: playerRoleFilter || undefined,
        });
        if (isCurrent) {
          setDomesticPlayers(res.items);
          setPlayerTotal(res.total);
          if (res.items.length > 0) {
            setSelectedPlayerId((prev) => (!prev || !res.items.some((p) => String(p.canonical_id) === prev) ? String(res.items[0].canonical_id) : prev));
          } else {
            setSelectedPlayerId("");
          }
        }
      } catch (err) {
        if (isCurrent) {
          console.warn("Failed to load domestic players:", err);
          setDomesticPlayers([]);
          setPlayerTotal(0);
        }
      } finally {
        if (isCurrent) setLoadingPlayerList(false);
      }
    }
    loadPlayers();
    return () => {
      isCurrent = false;
    };
  }, [playerPage, playerSearch, playerEligibilityFilter, playerRoleFilter]);

  // Load player all-round data when player tab is viewed or player changed
  useEffect(() => {
    if (activeTab !== "player_profile" || !selectedPlayerId) return;
    let isCurrent = true;
    async function loadProfile() {
      setLoadingPlayer(true);
      try {
        const [allRound, stats, splits] = await Promise.all([
          fetchPlayerAllRoundSummary(selectedPlayerId).catch((e) => {
            console.warn("All-round summary fetch notice:", e);
            return null;
          }),
          fetchPlayerDomesticStats(selectedPlayerId).catch((e) => {
            console.warn("Domestic stats fetch notice:", e);
            return [];
          }),
          fetchPlayerPhaseSplits(selectedPlayerId).catch((e) => {
            console.warn("Phase splits fetch notice:", e);
            return [];
          }),
        ]);
        if (isCurrent) {
          setAllRoundData(allRound);
          setPlayerSeasonStats(stats);
          setPlayerPhaseSplits(splits);
        }
      } catch (err) {
        if (isCurrent) console.warn("Failed to load player dossier:", err);
      } finally {
        if (isCurrent) setLoadingPlayer(false);
      }
    }
    loadProfile();
    return () => {
      isCurrent = false;
    };
  }, [selectedPlayerId, activeTab]);

  const activeInnings: InningsAnalysisResponse | undefined =
    matchScorecard?.innings && matchScorecard.innings.length > activeInningsIdx
      ? matchScorecard.innings[activeInningsIdx]
      : undefined;

  return (
    <div className="space-y-8 pb-12">
      {/* Top Header & Context */}
      <section className="space-y-3">
        <div className="flex flex-wrap items-center gap-3 text-xs">
          <span className="font-mono font-bold tracking-widest text-[#101D3A] uppercase px-2.5 py-1 rounded-md bg-[#D4145A]/10 border border-[#D4145A]/30">
            Rajasthan Royals Recruitment
          </span>
          <span className="text-[#101D3A]/30">•</span>
          <span className="font-mono text-[#52627A]">
            IPL • SMAT • VHT • Ranji • DPL
          </span>
          <span className="text-[#101D3A]/30">•</span>
          <span className="inline-flex items-center gap-1.5 text-[#D4145A] font-medium">
            <span className="w-1.5 h-1.5 rounded-full bg-[#D4145A]" />
            Verified Domestic Coverage
          </span>
        </div>

        <div className="flex flex-col md:flex-row md:items-end justify-between gap-4">
          <div className="max-w-3xl space-y-2">
            <h1 className="text-3xl md:text-4xl font-extrabold tracking-tight text-[#101D3A] leading-tight">
              Domestic Season & Match Intelligence
            </h1>
            <p className="text-sm md:text-base text-[#52627A] leading-relaxed font-normal">
              Format-aware phase diagnostics, ball-by-ball scorecards, partnerships, progression worms,
              and uncompromised all-round dual-contribution tracking for IPL 2027 recruitment.
            </p>
          </div>

          {/* Global Selectors */}
          <div className="flex items-center gap-3 shrink-0">
            <div className="flex flex-col">
              <label className="text-[10px] font-bold text-[#52627A] uppercase tracking-wider mb-1 font-mono">
                Competition
              </label>
              <select
                value={selectedCompId}
                onChange={(e) => setSelectedCompId(e.target.value)}
                className="bg-white border border-[#E7EAF0] rounded-lg px-3 py-1.5 text-xs font-semibold text-[#101D3A] focus:outline-none focus:ring-2 focus:ring-[#101D3A] shadow-sm"
              >
                {competitions.length > 0 ? (
                  competitions.map((c) => (
                    <option key={`${c.competition_id}_${c.season}`} value={c.competition_id}>
                      {c.competition_name} ({c.competition_type})
                    </option>
                  ))
                ) : (
                  <>
                    <option value="ipl">Indian Premier League (T20)</option>
                    <option value="smat">Syed Mushtaq Ali Trophy (T20)</option>
                    <option value="vht">Vijay Hazare Trophy (List A)</option>
                    <option value="ranji">Ranji Trophy (Multi-Day)</option>
                    <option value="dpl">Delhi Premier League (T20)</option>
                  </>
                )}
              </select>
            </div>

            <div className="flex flex-col">
              <label className="text-[10px] font-bold text-[#52627A] uppercase tracking-wider mb-1 font-mono">
                Season
              </label>
              <select
                value={selectedSeason}
                onChange={(e) => setSelectedSeason(e.target.value)}
                className="bg-white border border-[#E7EAF0] rounded-lg px-3 py-1.5 text-xs font-semibold text-[#101D3A] focus:outline-none focus:ring-2 focus:ring-[#101D3A] shadow-sm"
              >
                <option value="2024">2024</option>
                <option value="2025">2025</option>
                <option value="2026">2026</option>
                <option value="2024-25">2024-25</option>
              </select>
            </div>
          </div>
        </div>
      </section>

      {/* Connection Notice */}
      {errorMsg && (
        <div className="p-4 rounded-xl bg-[#D4145A]/10 border border-[#D4145A]/30 text-[#D4145A] flex items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <AlertCircle className="w-5 h-5 text-[#D4145A] shrink-0" />
            <div>
              <div className="text-xs font-bold">Domestic Service Connection Notice</div>
              <div className="text-xs text-[#D4145A] mt-0.5">{errorMsg}</div>
            </div>
          </div>
          <button
            onClick={loadComps}
            className="px-3 py-1.5 rounded-lg bg-[#D4145A] text-white font-bold text-xs hover:bg-[#A80F50] transition-colors shrink-0 flex items-center gap-1.5"
          >
            <RefreshCw className="w-3.5 h-3.5" />
            <span>Retry</span>
          </button>
        </div>
      )}

      {/* Navigation Tabs */}
      <div className="flex items-center gap-6 border-b border-[#E7EAF0]">
        <button
          onClick={() => setActiveTab("tournaments")}
          className={`flex items-center gap-2 py-3 text-xs font-semibold transition-all border-b-2 -mb-px whitespace-nowrap ${
            activeTab === "tournaments"
              ? "border-[#101D3A] text-[#101D3A] font-bold"
              : "border-transparent text-[#52627A] hover:text-[#101D3A]"
          }`}
        >
          <Trophy size={14} className="text-[#D4145A]" />
          <span>Tournament Directory ({competitions.length})</span>
        </button>
        <button
          onClick={() => setActiveTab("matches")}
          className={`flex items-center gap-2 py-3 text-xs font-semibold transition-all border-b-2 -mb-px whitespace-nowrap ${
            activeTab === "matches"
              ? "border-[#101D3A] text-[#101D3A] font-bold"
              : "border-transparent text-[#52627A] hover:text-[#101D3A]"
          }`}
        >
          <Swords size={14} className="text-[#52627A]" />
          <span>Match Intelligence & Scorecards ({matchTotal})</span>
        </button>
        <button
          onClick={() => setActiveTab("player_profile")}
          className={`flex items-center gap-2 py-3 text-xs font-semibold transition-all border-b-2 -mb-px whitespace-nowrap ${
            activeTab === "player_profile"
              ? "border-[#101D3A] text-[#101D3A] font-bold"
              : "border-transparent text-[#52627A] hover:text-[#101D3A]"
          }`}
        >
          <Target size={14} className="text-[#D4145A]" />
          <span>Uncapped Player Dossier & Splits ({playerTotal})</span>
        </button>
      </div>

      {/* TAB 1: TOURNAMENT DIRECTORY */}
      {activeTab === "tournaments" && (
        <div className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
            {competitions.map((comp, idx) => (
              <div
                key={`${comp.competition_id}_${comp.season}`}
                onClick={() => {
                  setSelectedCompId(comp.competition_id);
                  setSelectedSeason(comp.season);
                  setActiveTab("matches");
                }}
                className={cn(
                  "group p-5 rounded-2xl border cursor-pointer transition-all hover:shadow-md",
                  selectedCompId === comp.competition_id && selectedSeason === comp.season
                    ? "border-[#E4005A] ring-2 ring-[#E4005A]/30 bg-white shadow-sm"
                    : idx % 2 === 0
                    ? "bg-[#FCE8F0]/40 border-[#E7EAF0] hover:border-[#E4005A]/40"
                    : "bg-[#EEF4FC]/50 border-[#E7EAF0] hover:border-[#E4005A]/40"
                )}
              >
                <div className="flex items-center justify-between mb-3">
                  <span className="px-2.5 py-0.5 rounded-full text-[10px] font-mono font-bold bg-[#FCE8F0] text-[#950460]">
                    {comp.competition_type}
                  </span>
                  <span className="text-xs font-mono font-bold text-[#17294B]">{comp.season}</span>
                </div>

                <h3 className="font-bold text-base text-[#17294B] group-hover:text-[#E4005A] transition-colors mb-1">
                  {comp.competition_name}
                </h3>
                <p className="text-xs text-[#74658F] mb-4">Governing Body: {comp.governing_body}</p>

                <div className="grid grid-cols-3 gap-2 py-3 px-3 bg-white/90 rounded-xl border border-[#E7EAF0] text-center mb-4">
                  <div>
                    <div className="text-[10px] uppercase font-bold text-[#74658F]">Matches</div>
                    <div className="text-sm font-extrabold text-[#17294B]">{comp.match_count}</div>
                  </div>
                  <div>
                    <div className="text-[10px] uppercase font-bold text-[#74658F]">Teams</div>
                    <div className="text-sm font-extrabold text-[#17294B]">{comp.teams_count}</div>
                  </div>
                  <div>
                    <div className="text-[10px] uppercase font-bold text-[#74658F]">Ball-by-Ball</div>
                    <div className="text-sm font-extrabold text-[#15966B] flex items-center justify-center gap-1">
                      <CheckCircle2 size={12} className="text-[#15966B]" />
                      <span>{comp.has_ball_by_ball ? "Verified" : "Pending"}</span>
                    </div>
                  </div>
                </div>

                <div className="flex items-center justify-between text-xs text-[#74658F] pt-2 border-t border-[#E7EAF0]">
                  <span className="flex items-center gap-1 text-[11px] text-[#15966B] font-semibold">
                    <CheckCircle2 size={13} className="text-[#15966B]" />
                    Audit Pass: {comp.validation_pass_rate}%
                  </span>
                  <span className="text-[11px] font-mono font-bold text-[#E4005A] flex items-center">
                    Explore Fixtures <ChevronRight size={13} />
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
          {/* Match Filter & List */}
          <div className="flex flex-col md:flex-row items-center justify-between gap-4 bg-white p-4 rounded-xl border border-[#E7EAF0]">
            <div className="flex items-center gap-3 w-full md:w-auto">
              <Filter size={16} className="text-[#74658F]" />
              <input
                type="text"
                placeholder="Filter by Team Name / Code..."
                value={teamFilter}
                onChange={(e) => setTeamFilter(e.target.value)}
                className="bg-white border border-[#E7EAF0] rounded-lg px-3 py-1.5 text-xs text-[#17294B] focus:outline-none focus:ring-2 focus:ring-[#E4005A]"
              />
            </div>
            <span className="text-xs text-[#74658F] font-mono">
              Displaying {matches.length} of {matchTotal} Recorded Matches
            </span>
          </div>

          {/* Matches Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {matches.map((m, mIdx) => (
              <div
                key={m.match_id}
                onClick={() => setSelectedMatchId(m.match_id)}
                className={cn(
                  "p-4 rounded-xl border cursor-pointer transition-all hover:shadow-sm",
                  mIdx % 2 === 0 ? "bg-[#FCE8F0]/30 border-[#E7EAF0] hover:border-[#E4005A]" : "bg-[#EEF4FC]/40 border-[#E7EAF0] hover:border-[#E4005A]"
                )}
              >
                <div className="flex items-center justify-between text-[11px] text-[#74658F] font-mono mb-2">
                  <span>Match #{m.match_number || "—"}</span>
                  <span>{m.match_date}</span>
                </div>

                <div className="flex items-center justify-between my-2">
                  <div className="flex items-center gap-2">
                    <span className="font-extrabold text-sm text-[#950460]">{m.home_team_name}</span>
                    <span className="text-xs text-[#74658F] font-mono">vs</span>
                    <span className="font-extrabold text-sm text-[#950460]">{m.away_team_name}</span>
                  </div>
                  {m.winner_team_code && (
                    <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-[#FCE8F0] text-[#E4005A] border border-[#E4005A]/20">
                      Won: {m.winner_team_code}
                    </span>
                  )}
                </div>

                <div className="flex items-center justify-between text-xs text-[#74658F] pt-2 border-t border-[#E7EAF0] mt-2">
                  <span>{m.venue_name}, {m.venue_city}</span>
                  <span className="text-[#E4005A] font-bold flex items-center text-[11px]">
                    Full Scorecard <ChevronRight size={12} />
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Match Scorecard Modal */}
      {selectedMatchId && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4 overflow-y-auto">
          <div className="bg-white rounded-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto shadow-2xl border border-[#E7EAF0]">
            {/* Modal Header */}
            <div className="p-5 border-b border-[#E7EAF0] flex items-center justify-between bg-white sticky top-0 z-10">
              <div>
                <span className="text-[10px] font-mono font-bold text-[#101D3A] uppercase tracking-wider">
                  Verified Match Telemetry
                </span>
                <h3 className="text-lg font-extrabold text-[#101D3A]">
                  {matchScorecard ? `${matchScorecard.home_team.name} vs ${matchScorecard.away_team.name}` : "Loading Scorecard..."}
                </h3>
                {matchScorecard && (
                  <p className="text-xs text-[#52627A] mt-0.5">
                    {matchScorecard.venue_name}, {matchScorecard.venue_city} • {matchScorecard.match_date} • {matchScorecard.win_margin}
                  </p>
                )}
              </div>
              <button
                onClick={() => setSelectedMatchId(null)}
                className="p-1.5 rounded-lg text-[#52627A] hover:text-[#52627A] hover:bg-[#F8E8EF] transition-colors"
              >
                <X size={18} />
              </button>
            </div>

            {loadingScorecard ? (
              <div className="p-12 text-center text-xs text-[#52627A] font-mono">
                Extracting ball-by-ball match diagnostics...
              </div>
            ) : matchScorecard && activeInnings ? (
              <div className="p-6 space-y-6">
                {/* Innings Selector */}
                <div className="flex items-center gap-2 border-b border-[#E7EAF0] pb-3">
                  {matchScorecard.innings.map((inn, idx) => (
                    <button
                      key={inn.innings_number}
                      onClick={() => setActiveInningsIdx(idx)}
                      className={`px-4 py-1.5 rounded-xl text-xs font-bold transition-all ${
                        activeInningsIdx === idx
                          ? "bg-[#101D3A] text-white shadow-sm"
                          : "bg-[#F8E8EF] text-[#52627A] hover:bg-[#F8E8EF]"
                      }`}
                    >
                      Innings {inn.innings_number}: {inn.batting_team_name} ({inn.total_runs}/{inn.wickets})
                    </button>
                  ))}
                </div>

                {/* Phase Summaries Cards */}
                <div>
                  <h4 className="text-xs font-bold uppercase tracking-wider text-[#52627A] mb-3">
                    Phase-by-Phase Scoring Trajectory
                  </h4>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                    {activeInnings.phase_summaries.map((phase) => (
                      <div key={phase.phase_name} className="p-3 bg-white rounded-xl border border-[#E7EAF0]">
                        <div className="flex items-center justify-between mb-1">
                          <span className="text-xs font-bold text-[#101D3A]">{phase.phase_name}</span>
                          <span className="text-[10px] font-mono text-[#52627A]">{phase.overs_range}</span>
                        </div>
                        <div className="text-xl font-black text-[#101D3A] my-1">
                          {phase.runs} <span className="text-xs font-normal text-[#52627A]">runs / {phase.wickets} wkts</span>
                        </div>
                        <div className="flex items-center justify-between text-[11px] text-[#52627A] pt-2 border-t border-[#E7EAF0]">
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
                    <h4 className="text-xs font-bold uppercase tracking-wider text-[#52627A]">
                      Batting Scorecard — {activeInnings.batting_team_name}
                    </h4>
                    <span className="text-xs font-mono text-[#52627A]">
                      Total: {activeInnings.total_runs}/{activeInnings.wickets} ({activeInnings.overs_completed} ov, RR {activeInnings.run_rate})
                    </span>
                  </div>
                  <div className="overflow-x-auto border border-[#E7EAF0] rounded-xl">
                    <table className="w-full text-left text-xs">
                      <thead className="bg-white text-[#52627A] font-semibold border-b border-[#E7EAF0]">
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
                          <tr key={b.player_id} className="hover:bg-white/80">
                            <td className="py-2.5 px-3 font-semibold text-[#101D3A] flex items-center gap-1.5">
                              {b.player_name}
                              {b.is_uncapped && (
                                <span className="px-1.5 py-0.2 rounded text-[9px] font-mono font-bold bg-[#101D3A]/15 text-[#101D3A]">
                                  UNCAPPED
                                </span>
                              )}
                            </td>
                            <td className="py-2.5 px-3 text-[#52627A] text-[11px]">
                              {b.is_out ? (
                                <span>
                                  {b.dismissal_kind} {b.bowler_name ? `b ${b.bowler_name}` : ""}{" "}
                                  {b.fielder_name ? `c ${b.fielder_name}` : ""}
                                </span>
                              ) : (
                                <span className="font-semibold text-[#D4145A]">not out</span>
                              )}
                            </td>
                            <td className="py-2.5 px-3 text-right font-extrabold text-[#101D3A]">{b.runs}</td>
                            <td className="py-2.5 px-3 text-right text-[#52627A]">{b.balls_faced}</td>
                            <td className="py-2.5 px-3 text-right text-[#52627A]">{b.fours}</td>
                            <td className="py-2.5 px-3 text-right text-[#52627A]">{b.sixes}</td>
                            <td className="py-2.5 px-3 text-right font-mono font-bold text-[#101D3A]">{b.strike_rate}</td>
                            <td className="py-2.5 px-3 text-right font-mono text-[#52627A] text-[11px]">
                              {b.powerplay_runs !== undefined ? `${b.powerplay_runs}/${b.powerplay_balls}` : "-"}
                            </td>
                            <td className="py-2.5 px-3 text-right font-mono text-[#52627A] text-[11px]">
                              {b.death_runs !== undefined ? `${b.death_runs}/${b.death_balls}` : "-"}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>

                {/* Bowling Scorecard */}
                <div>
                  <h4 className="text-xs font-bold uppercase tracking-wider text-[#52627A] mb-2">
                    Bowling Scorecard — {activeInnings.bowling_team_name}
                  </h4>
                  <div className="overflow-x-auto border border-[#E7EAF0] rounded-xl">
                    <table className="w-full text-left text-xs">
                      <thead className="bg-white text-[#52627A] font-semibold border-b border-[#E7EAF0]">
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
                          <tr key={bw.player_id} className="hover:bg-white/80">
                            <td className="py-2.5 px-3 font-semibold text-[#101D3A] flex items-center gap-1.5">
                              {bw.player_name}
                              {bw.is_uncapped && (
                                <span className="px-1.5 py-0.2 rounded text-[9px] font-mono font-bold bg-[#101D3A]/15 text-[#101D3A]">
                                  UNCAPPED
                                </span>
                              )}
                            </td>
                            <td className="py-2.5 px-3 text-right font-mono text-[#101D3A]">{bw.overs}</td>
                            <td className="py-2.5 px-3 text-right text-[#52627A]">{bw.maidens}</td>
                            <td className="py-2.5 px-3 text-right font-extrabold text-[#101D3A]">{bw.runs_conceded}</td>
                            <td className="py-2.5 px-3 text-right font-extrabold text-[#101D3A]">{bw.bowler_wickets}</td>
                            <td className="py-2.5 px-3 text-right font-mono font-bold text-[#101D3A]">{bw.economy_rate}</td>
                            <td className="py-2.5 px-3 text-right text-[#52627A]">{bw.dot_balls ?? 0}</td>
                            <td className="py-2.5 px-3 text-right text-[#52627A] font-mono text-[11px]">
                              w:{bw.wides} nb:{bw.noballs}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            ) : null}

            {/* Modal Footer */}
            <div className="p-4 bg-white border-t border-[#E7EAF0] flex justify-between items-center text-xs text-[#52627A]">
              <span className="font-mono text-[11px]">Provenance: Rajasthan Royals Analytics Pipeline (Stage 3)</span>
              <button
                onClick={() => setSelectedMatchId(null)}
                className="px-4 py-1.5 rounded-lg bg-[#F8E8EF] text-[#101D3A] font-bold hover:bg-[#101D3A]/20 transition-colors"
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
          {/* Dynamic Player Discovery & Search Bar */}
          <div className="bg-white p-5 rounded-2xl border border-[#E7EAF0] shadow-sm space-y-4">
            <div className="flex flex-col md:flex-row items-stretch md:items-center justify-between gap-4">
              {/* Search Input */}
              <div className="relative flex-1">
                <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 text-[#52627A]" size={15} />
                <input
                  type="text"
                  placeholder="Search domestic player by name, ID, or role..."
                  value={playerSearch}
                  onChange={(e) => {
                    setPlayerSearch(e.target.value);
                    setPlayerPage(1);
                  }}
                  className="w-full pl-9 pr-4 py-2 bg-white/80 border border-[#E7EAF0] rounded-lg text-xs font-medium text-[#101D3A] placeholder:text-[#52627A] focus:outline-none focus:ring-2 focus:ring-[#101D3A]"
                />
                {playerSearch && (
                  <button
                    onClick={() => {
                      setPlayerSearch("");
                      setPlayerPage(1);
                    }}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-[#52627A] hover:text-[#52627A]"
                  >
                    <X size={14} />
                  </button>
                )}
              </div>

              {/* Eligibility Filter Tabs */}
              <div className="flex items-center gap-1 p-1 bg-[#F8E8EF] rounded-lg">
                <button
                  onClick={() => {
                    setPlayerEligibilityFilter("ALL");
                    setPlayerPage(1);
                  }}
                  className={`px-3 py-1.5 rounded-md text-xs font-semibold transition-all ${
                    playerEligibilityFilter === "ALL"
                      ? "bg-white text-[#101D3A] shadow-sm"
                      : "text-[#52627A] hover:text-[#101D3A]"
                  }`}
                >
                  All ({eligibilityCounts.ALL || playerTotal})
                </button>
                <button
                  onClick={() => {
                    setPlayerEligibilityFilter("VERIFIED_UNCAPPED");
                    setPlayerPage(1);
                  }}
                  className={`px-3 py-1.5 rounded-md text-xs font-semibold transition-all ${
                    playerEligibilityFilter === "VERIFIED_UNCAPPED"
                      ? "bg-[#101D3A] text-white shadow-sm"
                      : "text-[#52627A] hover:text-[#101D3A]"
                  }`}
                >
                  Uncapped ({eligibilityCounts.VERIFIED_UNCAPPED || (playerEligibilityFilter === "VERIFIED_UNCAPPED" ? playerTotal : 0)})
                </button>
                <button
                  onClick={() => {
                    setPlayerEligibilityFilter("PENDING_VERIFICATION");
                    setPlayerPage(1);
                  }}
                  className={`px-3 py-1.5 rounded-md text-xs font-semibold transition-all ${
                    playerEligibilityFilter === "PENDING_VERIFICATION"
                      ? "bg-[#D4145A] text-[#101D3A] shadow-sm"
                      : "text-[#52627A] hover:text-[#101D3A]"
                  }`}
                >
                  Pending ({eligibilityCounts.PENDING_VERIFICATION || (playerEligibilityFilter === "PENDING_VERIFICATION" ? playerTotal : 0)})
                </button>
              </div>

              {/* Role Dropdown */}
              <select
                value={playerRoleFilter}
                onChange={(e) => {
                  setPlayerRoleFilter(e.target.value);
                  setPlayerPage(1);
                }}
                className="bg-white/80 border border-[#E7EAF0] rounded-lg px-3 py-2 text-xs font-semibold text-[#101D3A] focus:outline-none focus:ring-2 focus:ring-[#101D3A]"
              >
                <option value="">All Roles</option>
                <option value="Batter">Batter</option>
                <option value="Bowler">Bowler</option>
                <option value="All-rounder">All-Rounder</option>
                <option value="Wicketkeeper">Wicketkeeper-Batter</option>
              </select>
            </div>

            {/* Player Grid / Selector Strip */}
            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-2">
              {domesticPlayers.map((p) => {
                const isSelected = String(p.canonical_id) === selectedPlayerId;
                return (
                  <button
                    key={p.canonical_id}
                    onClick={() => setSelectedPlayerId(String(p.canonical_id))}
                    className={`p-3 rounded-xl text-left border transition-all ${
                      isSelected
                        ? "bg-[#101D3A] text-white border-[#101D3A] shadow-sm"
                        : "bg-white hover:bg-white text-[#101D3A] border-[#E7EAF0]"
                    }`}
                  >
                    <div className="flex items-center justify-between gap-1 mb-1">
                      <span
                        className={`text-[9px] font-mono px-1.5 py-0.2 rounded font-bold ${
                          p.eligibility_status === "VERIFIED_UNCAPPED"
                            ? isSelected
                              ? "bg-[#101D3A] text-white"
                              : "bg-[#D4145A]/10 text-[#D4145A] border border-[#D4145A]/30/60"
                            : isSelected
                            ? "bg-[#101D3A] text-white"
                            : "bg-[#F8E8EF] text-[#52627A]"
                        }`}
                      >
                        {p.eligibility_status === "VERIFIED_UNCAPPED" ? "UNCAPPED" : "PENDING"}
                      </span>
                      <span
                        className={`w-1.5 h-1.5 rounded-full ${
                          p.statistical_coverage_status === "AVAILABLE" ? "bg-[#D4145A]" : "bg-[#101D3A]/20"
                        }`}
                        title={p.statistical_coverage_status === "AVAILABLE" ? "Telemetry Available" : "No Match Data"}
                      />
                    </div>
                    <div className="font-bold text-xs truncate">{p.player_name}</div>
                    <div className={`text-[10px] truncate mt-0.5 ${isSelected ? "text-[#101D3A]/30" : "text-[#52627A]"}`}>
                      {p.team || "Domestic"} • {p.role || "Prospect"}
                    </div>
                  </button>
                );
              })}
            </div>

            {/* Pagination Bar */}
            {playerTotal > 12 && (
              <div className="flex items-center justify-between pt-3 border-t border-[#E7EAF0] text-xs">
                <span className="text-[#52627A] font-mono text-[11px]">
                  {(playerPage - 1) * 12 + 1}–{Math.min(playerPage * 12, playerTotal)} of {playerTotal} candidates
                </span>
                <div className="flex items-center gap-1.5">
                  <button
                    disabled={playerPage <= 1}
                    onClick={() => setPlayerPage((p) => Math.max(1, p - 1))}
                    className="p-1.5 rounded-lg border border-[#E7EAF0] text-[#52627A] disabled:opacity-40 hover:bg-white"
                  >
                    <ChevronLeft size={14} />
                  </button>
                  <span className="font-mono text-xs font-bold text-[#101D3A] px-2">
                    Page {playerPage} of {Math.ceil(playerTotal / 12)}
                  </span>
                  <button
                    disabled={playerPage >= Math.ceil(playerTotal / 12)}
                    onClick={() => setPlayerPage((p) => p + 1)}
                    className="p-1.5 rounded-lg border border-[#E7EAF0] text-[#52627A] disabled:opacity-40 hover:bg-white"
                  >
                    <ChevronRight size={14} />
                  </button>
                </div>
              </div>
            )}
          </div>

          {loadingPlayer ? (
            <div className="p-12 text-center text-xs text-[#52627A] font-mono">
              Loading domestic intelligence dossier...
            </div>
          ) : (
            <>
              {/* Dual-Discipline Summary Card */}
              {allRoundData && (
                <div className="bg-white p-6 md:p-8 rounded-2xl border border-[#E7EAF0] shadow-sm space-y-6">
                  <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-[#E7EAF0] pb-5">
                    <div>
                      <div className="flex items-center gap-2 mb-1.5">
                        <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-[#D4145A]/10 text-[#D4145A] border border-[#D4145A]/30/60">
                          {allRoundData.eligibility_status}
                        </span>
                        <span className="text-xs font-mono text-[#52627A]">
                          Canonical ID: #{allRoundData.canonical_id}
                        </span>
                        <span
                          className={`px-2 py-0.5 rounded text-[10px] font-mono font-bold ${
                            allRoundData.statistical_coverage_status === "AVAILABLE"
                              ? "bg-[#F8E8EF] text-[#101D3A]"
                              : "bg-[#D4145A]/10 text-[#D4145A] border border-[#D4145A]/30/60"
                          }`}
                        >
                          {allRoundData.statistical_coverage_status === "AVAILABLE" ? "TELEMETRY ACTIVE" : "PENDING MATCH COVERAGE"}
                        </span>
                      </div>
                      <h2 className="text-2xl font-black text-[#101D3A]">{allRoundData.full_name}</h2>
                      <p className="text-xs text-[#52627A] mt-1">
                        Primary Role: <span className="font-semibold text-[#101D3A]">{allRoundData.primary_role}</span> • Team: {allRoundData.domestic_team}
                      </p>
                    </div>

                    {/* Transparent Archetype & Sample Size */}
                    <div className="p-3.5 rounded-xl bg-white border border-[#E7EAF0] text-right">
                      <div className="text-[10px] font-mono font-bold uppercase tracking-wider text-[#52627A]">
                        Evidence-Based Archetype
                      </div>
                      <div className="text-sm font-bold text-[#101D3A] mt-0.5">
                        {allRoundData.role_archetype_context}
                      </div>
                      <div className="text-[11px] font-mono text-[#52627A] mt-0.5">
                        Sample: {allRoundData.sample_size?.matches ?? 0} matches • {allRoundData.sample_size?.innings_batted ?? 0} inn • {allRoundData.sample_size?.overs_bowled ?? 0} ov
                      </div>
                    </div>
                  </div>

                  {/* Informational Banner when No Statistical Coverage */}
                  {allRoundData.statistical_coverage_status === "NO_STATISTICAL_COVERAGE" && (
                    <div className="p-4 rounded-xl bg-[#D4145A]/10 border border-[#D4145A]/30 text-[#D4145A] flex items-start gap-3">
                      <AlertCircle className="text-[#D4145A] mt-0.5 flex-shrink-0" size={16} />
                      <div>
                        <div className="text-xs font-bold">
                          No Domestic Match Telemetry Recorded in Current Dataset
                        </div>
                        <div className="text-xs text-[#D4145A] mt-0.5">
                          Candidate is confirmed in official BCCI registries. Ball-by-ball match delivery records are pending ingestion for this cricketer. Zero statistics are presented to avoid speculative fabrication.
                        </div>
                      </div>
                    </div>
                  )}

                  {/* Independent Batting vs Bowling Dual Columns (Open Layout) */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-8 pt-2">
                    {/* Batting Dimension */}
                    <div className="space-y-4">
                      <div className="flex items-center justify-between pb-2 border-b border-[#E7EAF0]">
                        <div className="flex items-center gap-2">
                          <TrendingUp size={16} className="text-[#101D3A]" />
                          <h4 className="text-sm font-bold text-[#101D3A]">Batting Profile</h4>
                        </div>
                        <span className="text-xs font-mono text-[#52627A]">
                          {allRoundData.batting_summary?.innings ?? 0} innings
                        </span>
                      </div>
                      <div className="grid grid-cols-3 gap-4">
                        <div>
                          <div className="text-[10px] font-mono uppercase text-[#52627A]">Runs</div>
                          <div className="text-xl font-bold font-mono text-[#101D3A] mt-0.5">
                            {allRoundData.batting_summary?.runs ?? 0}
                          </div>
                        </div>
                        <div>
                          <div className="text-[10px] font-mono uppercase text-[#52627A]">Strike Rate</div>
                          <div className="text-xl font-bold font-mono text-[#101D3A] mt-0.5">
                            {allRoundData.batting_summary?.strike_rate ?? 0.0}
                          </div>
                        </div>
                        <div>
                          <div className="text-[10px] font-mono uppercase text-[#52627A]">Average</div>
                          <div className="text-xl font-bold font-mono text-[#101D3A] mt-0.5">
                            {allRoundData.batting_summary?.batting_average ?? allRoundData.batting_summary?.average ?? "N/A"}
                          </div>
                        </div>
                      </div>
                      <div className="flex items-center justify-between text-xs text-[#52627A] pt-2 border-t border-[#E7EAF0]">
                        <span>Boundaries: {allRoundData.batting_summary?.boundary_percentage ?? 0.0}%</span>
                        <span>High Score: {allRoundData.batting_summary?.high_score ?? 0}</span>
                      </div>
                    </div>

                    {/* Bowling Dimension */}
                    <div className="space-y-4">
                      <div className="flex items-center justify-between pb-2 border-b border-[#E7EAF0]">
                        <div className="flex items-center gap-2">
                          <Target size={16} className="text-[#101D3A]" />
                          <h4 className="text-sm font-bold text-[#101D3A]">Bowling Profile</h4>
                        </div>
                        <span className="text-xs font-mono text-[#52627A]">
                          {allRoundData.bowling_summary?.overs ?? allRoundData.bowling_summary?.overs_bowled ?? 0} overs
                        </span>
                      </div>
                      <div className="grid grid-cols-3 gap-4">
                        <div>
                          <div className="text-[10px] font-mono uppercase text-[#52627A]">Wickets</div>
                          <div className="text-xl font-bold font-mono text-[#101D3A] mt-0.5">
                            {allRoundData.bowling_summary?.bowler_wickets ?? allRoundData.bowling_summary?.wickets ?? 0}
                          </div>
                        </div>
                        <div>
                          <div className="text-[10px] font-mono uppercase text-[#52627A]">Economy</div>
                          <div className="text-xl font-bold font-mono text-[#101D3A] mt-0.5">
                            {allRoundData.bowling_summary?.economy_rate ?? allRoundData.bowling_summary?.economy ?? 0.0}
                          </div>
                        </div>
                        <div>
                          <div className="text-[10px] font-mono uppercase text-[#52627A]">Average</div>
                          <div className="text-xl font-bold font-mono text-[#101D3A] mt-0.5">
                            {allRoundData.bowling_summary?.bowling_average ?? allRoundData.bowling_summary?.average ?? "N/A"}
                          </div>
                        </div>
                      </div>
                      <div className="flex items-center justify-between text-xs text-[#52627A] pt-2 border-t border-[#E7EAF0]">
                        <span>Dots: {allRoundData.bowling_summary?.dot_balls_bowled ?? 0}</span>
                        <span>Catches: {allRoundData.fielding_summary?.catches ?? 0}</span>
                      </div>
                    </div>
                  </div>

                  <div className="pt-4 border-t border-[#E7EAF0] text-[11px] text-[#52627A] flex items-center gap-2">
                    <Shield size={13} className="text-[#D4145A]" />
                    <span>
                      Integrity Policy: Independent metrics are preserved without composite ratings or speculative weights.
                    </span>
                  </div>
                </div>
              )}

              {/* Granular Phase Splits Table */}
              <div className="bg-white p-6 rounded-2xl border border-[#E7EAF0] shadow-sm space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="text-base font-bold text-[#101D3A]">
                      Granular Phase Performance Splits
                    </h3>
                    <p className="text-xs text-[#52627A]">
                      Powerplay (overs 0-5), Middle (overs 6-14), and Death (overs 15-19) breakdown
                    </p>
                  </div>
                  <BarChart3 size={18} className="text-[#52627A]" />
                </div>

                <div className="overflow-x-auto border border-[#E7EAF0] rounded-xl">
                  <table className="w-full text-left text-xs">
                    <thead className="bg-white text-[#52627A] font-semibold border-b border-[#E7EAF0]">
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
                        <tr key={split.phase} className="hover:bg-white/80">
                          <td className="py-2.5 px-3 font-bold text-[#101D3A]">{split.phase}</td>
                          <td className="py-2.5 px-3 font-mono text-[#52627A]">{split.overs_range}</td>
                          <td className="py-2.5 px-3 text-right font-extrabold text-[#101D3A]">{split.batting_runs}</td>
                          <td className="py-2.5 px-3 text-right text-[#52627A]">{split.batting_balls}</td>
                          <td className="py-2.5 px-3 text-right font-mono font-bold text-[#101D3A]">{split.batting_strike_rate}</td>
                          <td className="py-2.5 px-3 text-right text-[#52627A]">{split.batting_fours} / {split.batting_sixes}</td>
                          <td className="py-2.5 px-3 text-right text-[#52627A]">{split.bowling_overs}</td>
                          <td className="py-2.5 px-3 text-right font-bold text-[#101D3A]">{split.bowler_wickets}</td>
                          <td className="py-2.5 px-3 text-right font-mono text-[#52627A]">{split.bowling_economy}</td>
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
