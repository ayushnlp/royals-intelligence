"use client";

import { useState, useEffect } from "react";
import {
  UncappedPlayerSummary,
  UncappedPlayerDetail,
  BattingAggregates,
  BowlingAggregates,
  RecentFormWindow,
  SchemaDiscoveryResult,
  RRDataPackIngestionSummary,
} from "@/types";
import {
  fetchUncappedPlayers,
  fetchUncappedPlayerDetail,
  verifyPlayerEligibility,
  fetchPlayerBatting,
  fetchPlayerBowling,
  fetchPlayerRecentForm,
  discoverProprietarySchema,
  ingestProprietaryPack,
  fetchPlayerEvaluations,
} from "@/lib/api";

export default function UncappedScoutingPage() {
  const [activeTab, setActiveTab] = useState<"roster" | "analytics" | "form" | "datapack">("roster");
  const [players, setPlayers] = useState<UncappedPlayerSummary[]>([]);
  const [selectedPlayerId, setSelectedPlayerId] = useState<string>("uncapped_rr_01");
  const [selectedPlayer, setSelectedPlayer] = useState<UncappedPlayerDetail | null>(null);
  const [loading, setLoading] = useState(true);

  // Filters
  const [searchName, setSearchName] = useState("");
  const [filterEligibility, setFilterEligibility] = useState<string>("");
  const [filterTier, setFilterTier] = useState<string>("");
  const [trialistOnly, setTrialistOnly] = useState<boolean>(false);

  // Analytics states
  const [battingStats, setBattingStats] = useState<BattingAggregates | null>(null);
  const [bowlingStats, setBowlingStats] = useState<BowlingAggregates | null>(null);
  const [recentForm, setRecentForm] = useState<RecentFormWindow | null>(null);

  // Eligibility modal / audit state
  const [auditNotes, setAuditNotes] = useState("");
  const [auditStatus, setAuditStatus] = useState("CONFIRMED_UNCAPPED");
  const [auditSubmitting, setAuditSubmitting] = useState(false);
  const [auditSuccessMsg, setAuditSuccessMsg] = useState("");

  // RR 8 Nov Data Pack state
  const [schemaResult, setSchemaResult] = useState<SchemaDiscoveryResult | null>(null);
  const [ingestionSummary, setIngestionSummary] = useState<RRDataPackIngestionSummary | null>(null);
  const [dataPackJson, setDataPackJson] = useState(
    JSON.stringify(
      [
        {
          player_name: "Ashutosh Sharma",
          dob: "1998-09-15",
          state_association: "Madhya Pradesh",
          primary_role: "Finisher",
          batting_hand: "Right",
          technical_rating: 8.5,
          confidential_notes: "Target for auction finisher role. Max bid INR 7.5 Cr.",
          is_rr_trialist: "true",
        },
        {
          player_name: "Priyansh Arya",
          dob: "2001-01-18",
          state_association: "Delhi",
          primary_role: "Top Order Batter",
          batting_hand: "Left",
          technical_rating: 9.0,
          confidential_notes: "Dominant powerplay striker. 6 sixes in DPL over.",
          is_rr_trialist: "true",
        },
        {
          player_name: "Unverified State Prospect",
          dob: "", // Missing DOB to test validation & PENDING_VERIFICATION
          state_association: "Himachal Pradesh",
          primary_role: "Pace Bowler",
          batting_hand: "Right",
          technical_rating: 7.0,
          confidential_notes: "Physical testing pending at Nagpur academy.",
          is_rr_trialist: "false",
        },
      ],
      null,
      2
    )
  );
  const [userRole, setUserRole] = useState<"public" | "rr_scout_admin">("public");
  const [evaluations, setEvaluations] = useState<any[]>([]);

  // Load roster
  useEffect(() => {
    async function loadData() {
      setLoading(true);
      const res = await fetchUncappedPlayers({
        eligibility: filterEligibility || undefined,
        tier: filterTier || undefined,
        trialist_only: trialistOnly,
      });
      setPlayers(res);
      setLoading(false);
    }
    loadData();
  }, [filterEligibility, filterTier, trialistOnly]);

  // Load selected player detail & analytics
  useEffect(() => {
    if (!selectedPlayerId) return;

    async function loadPlayerTelemetry() {
      const detail = await fetchUncappedPlayerDetail(selectedPlayerId);
      setSelectedPlayer(detail);

      const bat = await fetchPlayerBatting(selectedPlayerId);
      setBattingStats(bat);

      const bowl = await fetchPlayerBowling(selectedPlayerId);
      setBowlingStats(bowl);

      const form = await fetchPlayerRecentForm(selectedPlayerId, 5, "batting");
      setRecentForm(form);

      const evals = await fetchPlayerEvaluations(selectedPlayerId, userRole);
      setEvaluations(evals);
    }

    loadPlayerTelemetry();
  }, [selectedPlayerId, userRole]);

  const handleAuditSubmit = async () => {
    if (!selectedPlayerId) return;
    setAuditSubmitting(true);
    setAuditSuccessMsg("");
    try {
      await verifyPlayerEligibility(selectedPlayerId, {
        new_status: auditStatus,
        verification_notes: auditNotes || "Eligibility confirmed via domestic BCCI scorecard audit.",
        verified_by: "LEAD_SCOUT_PANEL",
      });
      setAuditSuccessMsg(`Successfully updated status to ${auditStatus}`);
      // Refresh detail
      const updated = await fetchUncappedPlayerDetail(selectedPlayerId);
      setSelectedPlayer(updated);
    } catch (err: any) {
      setAuditSuccessMsg("Failed to update: " + err.message);
    } finally {
      setAuditSubmitting(false);
    }
  };

  const handleDiscoverSchema = async () => {
    try {
      const parsed = JSON.parse(dataPackJson);
      const res = await discoverProprietarySchema(parsed);
      setSchemaResult(res);
    } catch (err: any) {
      alert("Invalid JSON format: " + err.message);
    }
  };

  const handleIngestPack = async () => {
    try {
      const parsed = JSON.parse(dataPackJson);
      const res = await ingestProprietaryPack({
        records: parsed,
        column_mapping: schemaResult?.recommended_mapping,
        dataset_key: "rr_uncapped_pack_2026_test",
      });
      setIngestionSummary(res);
    } catch (err: any) {
      alert("Ingestion error: " + err.message);
    }
  };

  const filteredPlayers = players.filter((p) =>
    p.full_name.toLowerCase().includes(searchName.toLowerCase()) ||
    (p.home_state_association || "").toLowerCase().includes(searchName.toLowerCase())
  );

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-navy-800 pb-5">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="text-2xl font-bold tracking-tight text-white">
              Uncapped Talent Scouting Hub
            </h1>
            <span className="rounded-full bg-pink-500/10 px-3 py-1 text-xs font-semibold text-pink-400 border border-pink-500/30">
              STAGE 2 SEALED
            </span>
            <span className="rounded-full bg-gold-500/10 px-3 py-1 text-xs font-semibold text-gold-400 border border-gold-500/30">
              UNCAPPED ONLY
            </span>
          </div>
          <p className="mt-1 text-sm text-navy-400">
            Relational intelligence database for domestic T20 prospects, age-group eligibility, and RR 8 Nov Data Pack integration.
          </p>
        </div>

        {/* Global Reference Cutoff Date Pill */}
        <div className="flex items-center gap-2 rounded-lg bg-navy-900 border border-navy-700 px-3 py-2 text-xs">
          <span className="text-navy-400">Eligibility Cutoff Reference:</span>
          <span className="font-semibold text-gold-400 font-mono">18 Nov 2026</span>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="flex flex-wrap gap-2 border-b border-navy-800 pb-2">
        <button
          onClick={() => setActiveTab("roster")}
          className={`px-4 py-2 text-sm font-medium rounded-lg transition-colors ${
            activeTab === "roster"
              ? "bg-pink-600 text-white shadow-lg shadow-pink-600/30"
              : "text-navy-400 hover:text-white hover:bg-navy-800"
          }`}
        >
          Uncapped Roster & Eligibility ({filteredPlayers.length})
        </button>
        <button
          onClick={() => setActiveTab("analytics")}
          className={`px-4 py-2 text-sm font-medium rounded-lg transition-colors ${
            activeTab === "analytics"
              ? "bg-pink-600 text-white shadow-lg shadow-pink-600/30"
              : "text-navy-400 hover:text-white hover:bg-navy-800"
          }`}
        >
          Analytics & Phase Breakdown
        </button>
        <button
          onClick={() => setActiveTab("form")}
          className={`px-4 py-2 text-sm font-medium rounded-lg transition-colors ${
            activeTab === "form"
              ? "bg-pink-600 text-white shadow-lg shadow-pink-600/30"
              : "text-navy-400 hover:text-white hover:bg-navy-800"
          }`}
        >
          Recent Form Window (Last 5)
        </button>
        <button
          onClick={() => setActiveTab("datapack")}
          className={`px-4 py-2 text-sm font-medium rounded-lg transition-colors ${
            activeTab === "datapack"
              ? "bg-pink-600 text-white shadow-lg shadow-pink-600/30"
              : "text-navy-400 hover:text-white hover:bg-navy-800"
          }`}
        >
          RR 8 Nov Data Pack Readiness
        </button>
      </div>

      {/* TAB 1: Roster & Eligibility */}
      {activeTab === "roster" && (
        <div className="space-y-4">
          {/* Filter Bar */}
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-3 bg-navy-900/60 p-4 rounded-xl border border-navy-800">
            <div>
              <label className="text-xs text-navy-400 block mb-1">Search Player or State</label>
              <input
                type="text"
                placeholder="e.g. Shashank, Delhi..."
                value={searchName}
                onChange={(e) => setSearchName(e.target.value)}
                className="w-full bg-navy-950 border border-navy-700 rounded-lg px-3 py-1.5 text-sm text-white placeholder-navy-500 focus:outline-none focus:border-pink-500"
              />
            </div>
            <div>
              <label className="text-xs text-navy-400 block mb-1">Eligibility Status</label>
              <select
                value={filterEligibility}
                onChange={(e) => setFilterEligibility(e.target.value)}
                className="w-full bg-navy-950 border border-navy-700 rounded-lg px-3 py-1.5 text-sm text-white focus:outline-none focus:border-pink-500"
              >
                <option value="">All Verification States</option>
                <option value="CONFIRMED_UNCAPPED">Confirmed Uncapped</option>
                <option value="SUSPECTED_CAPPED">Suspected Capped</option>
                <option value="PENDING_VERIFICATION">Pending Verification</option>
                <option value="FLAGGED_CONFLICT">Flagged Conflict</option>
              </select>
            </div>
            <div>
              <label className="text-xs text-navy-400 block mb-1">Scouting Priority Tier</label>
              <select
                value={filterTier}
                onChange={(e) => setFilterTier(e.target.value)}
                className="w-full bg-navy-950 border border-navy-700 rounded-lg px-3 py-1.5 text-sm text-white focus:outline-none focus:border-pink-500"
              >
                <option value="">All Tiers</option>
                <option value="TARGET_A_LIST">Target A-List</option>
                <option value="WATCHLIST_HIGH">Watchlist High</option>
                <option value="MONITOR">Monitor</option>
              </select>
            </div>
            <div className="flex items-center pt-5">
              <label className="flex items-center gap-2 cursor-pointer text-sm text-navy-300">
                <input
                  type="checkbox"
                  checked={trialistOnly}
                  onChange={(e) => setTrialistOnly(e.target.checked)}
                  className="rounded border-navy-700 bg-navy-950 text-pink-500 focus:ring-0"
                />
                <span>RR Trialists Only</span>
              </label>
            </div>
          </div>

          {/* Roster Grid */}
          {loading ? (
            <div className="p-8 text-center text-navy-400">Loading uncapped player profiles...</div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {filteredPlayers.map((player) => (
                <div
                  key={player.id}
                  onClick={() => setSelectedPlayerId(player.id)}
                  className={`p-4 rounded-xl border cursor-pointer transition-all ${
                    selectedPlayerId === player.id
                      ? "bg-navy-900 border-pink-500 shadow-md shadow-pink-500/20"
                      : "bg-navy-900/50 border-navy-800 hover:border-navy-700 hover:bg-navy-900"
                  }`}
                >
                  <div className="flex items-start justify-between">
                    <div>
                      <h3 className="font-semibold text-white text-base">{player.full_name}</h3>
                      <p className="text-xs text-navy-400 mt-0.5">
                        {player.primary_role || "All-Rounder"} • {player.home_state_association || "Domestic"}
                      </p>
                    </div>
                    {/* Status Badge */}
                    <span
                      className={`text-xs px-2.5 py-0.5 rounded-full font-medium ${
                        player.eligibility_status === "CONFIRMED_UNCAPPED"
                          ? "bg-emerald-500/20 text-emerald-400 border border-emerald-500/30"
                          : player.eligibility_status === "SUSPECTED_CAPPED"
                          ? "bg-amber-500/20 text-amber-400 border border-amber-500/30"
                          : "bg-purple-500/20 text-purple-400 border border-purple-500/30"
                      }`}
                    >
                      {player.eligibility_status.replace("_", " ")}
                    </span>
                  </div>

                  <div className="mt-3 grid grid-cols-2 gap-2 text-xs pt-3 border-t border-navy-800">
                    <div>
                      <span className="text-navy-500">Calculated Age:</span>{" "}
                      <span className="font-semibold text-navy-200">
                        {player.calculated_age !== null && player.calculated_age !== undefined
                          ? `${player.calculated_age} yrs`
                          : (player.dob ? "Unresolved Cutoff" : "Missing DOB")}
                      </span>
                    </div>
                    <div>
                      <span className="text-navy-500">Tier:</span>{" "}
                      <span className="font-semibold text-gold-400">
                        {player.scouting_tier.replace("_", " ")}
                      </span>
                    </div>
                    <div>
                      <span className="text-navy-500">Batting:</span>{" "}
                      <span className="text-navy-300">{player.batting_hand || "Right"}</span>
                    </div>
                    <div>
                      <span className="text-navy-500">Trialist:</span>{" "}
                      <span className={player.is_rr_trialist ? "text-pink-400 font-semibold" : "text-navy-400"}>
                        {player.is_rr_trialist ? "Yes (RR Academy)" : "No"}
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* Detailed Verification Drawer */}
          {selectedPlayer && (
            <div className="mt-6 p-5 rounded-xl bg-navy-900 border border-navy-700 space-y-4">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-navy-800 pb-3">
                <div>
                  <h2 className="text-lg font-bold text-white flex items-center gap-2">
                    {selectedPlayer.full_name}
                    <span className="text-xs px-2 py-0.5 rounded bg-navy-800 text-navy-300 font-mono">
                      {selectedPlayer.canonical_id}
                    </span>
                  </h2>
                  <p className="text-xs text-navy-400">
                    DOB: {selectedPlayer.dob || "Missing"} ({selectedPlayer.dob_source || "Unverified"}) • Age at Cutoff: {selectedPlayer.calculated_age ?? "N/A"}
                  </p>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-xs text-navy-400">Cap Status:</span>
                  <span className="text-xs font-semibold text-emerald-400 bg-emerald-500/10 px-2 py-1 rounded">
                    Uncapped (0 Senior Caps)
                  </span>
                </div>
              </div>

              {/* External Source Identifiers */}
              <div>
                <h4 className="text-xs font-semibold text-navy-400 uppercase tracking-wider mb-2">
                  External Source Identifiers
                </h4>
                <div className="flex flex-wrap gap-2">
                  {selectedPlayer.identities.map((id, i) => (
                    <span
                      key={i}
                      className="text-xs px-2.5 py-1 bg-navy-950 border border-navy-800 rounded font-mono text-navy-300"
                    >
                      <strong className="text-pink-400 uppercase">{id.source_name}:</strong> {id.external_player_id} (conf: {id.confidence_score})
                    </span>
                  ))}
                </div>
              </div>

              {/* Audit Verification Form */}
              <div className="pt-2 border-t border-navy-800">
                <h4 className="text-xs font-semibold text-navy-300 mb-2">Audit & Update Verification State</h4>
                <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-3">
                  <select
                    value={auditStatus}
                    onChange={(e) => setAuditStatus(e.target.value)}
                    className="bg-navy-950 border border-navy-700 rounded-lg px-3 py-1.5 text-xs text-white"
                  >
                    <option value="CONFIRMED_UNCAPPED">CONFIRMED_UNCAPPED</option>
                    <option value="SUSPECTED_CAPPED">SUSPECTED_CAPPED</option>
                    <option value="PENDING_VERIFICATION">PENDING_VERIFICATION</option>
                    <option value="FLAGGED_CONFLICT">FLAGGED_CONFLICT</option>
                  </select>
                  <input
                    type="text"
                    placeholder="Enter audit justification or verification reference..."
                    value={auditNotes}
                    onChange={(e) => setAuditNotes(e.target.value)}
                    className="flex-1 bg-navy-950 border border-navy-700 rounded-lg px-3 py-1.5 text-xs text-white placeholder-navy-500"
                  />
                  <button
                    onClick={handleAuditSubmit}
                    disabled={auditSubmitting}
                    className="px-4 py-1.5 bg-pink-600 hover:bg-pink-700 text-white rounded-lg text-xs font-semibold transition-colors disabled:opacity-50"
                  >
                    {auditSubmitting ? "Updating..." : "Confirm State"}
                  </button>
                </div>
                {auditSuccessMsg && (
                  <p className="text-xs text-emerald-400 mt-2 font-medium">{auditSuccessMsg}</p>
                )}
              </div>
            </div>
          )}
        </div>
      )}

      {/* TAB 2: Analytics & Phase Breakdown */}
      {activeTab === "analytics" && (
        <div className="space-y-5">
          <div className="flex items-center justify-between bg-navy-900/60 p-4 rounded-xl border border-navy-800">
            <div>
              <span className="text-xs text-navy-400">Selected Player:</span>
              <h2 className="text-lg font-bold text-white">{selectedPlayer?.full_name || "Select Player"}</h2>
            </div>
            <span className="text-xs font-mono bg-pink-500/10 text-pink-400 border border-pink-500/20 px-3 py-1 rounded-full">
              Phase Analytics Active
            </span>
          </div>

          {/* Batting Metrics Cards */}
          {battingStats && battingStats.innings_count > 0 ? (
            <div className="space-y-4">
              <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-6 gap-3">
                <div className="p-3 bg-navy-900 rounded-xl border border-navy-800">
                  <div className="text-navy-400 text-xs">Total Runs</div>
                  <div className="text-xl font-bold text-white mt-1">{battingStats.runs}</div>
                  <div className="text-navy-500 text-xs mt-0.5">{battingStats.innings_count} innings</div>
                </div>
                <div className="p-3 bg-navy-900 rounded-xl border border-navy-800">
                  <div className="text-navy-400 text-xs">Strike Rate</div>
                  <div className="text-xl font-bold text-pink-400 mt-1">{battingStats.strike_rate}</div>
                  <div className="text-navy-500 text-xs mt-0.5">{battingStats.balls_faced} balls</div>
                </div>
                <div className="p-3 bg-navy-900 rounded-xl border border-navy-800">
                  <div className="text-navy-400 text-xs">Batting Average</div>
                  <div className="text-xl font-bold text-white mt-1">{battingStats.batting_average ?? "N/A"}</div>
                  <div className="text-navy-500 text-xs mt-0.5">{battingStats.dismissals} outs</div>
                </div>
                <div className="p-3 bg-navy-900 rounded-xl border border-navy-800">
                  <div className="text-navy-400 text-xs">Boundary %</div>
                  <div className="text-xl font-bold text-gold-400 mt-1">{battingStats.boundary_percentage}%</div>
                  <div className="text-navy-500 text-xs mt-0.5">{battingStats.fours} 4s, {battingStats.sixes} 6s</div>
                </div>
                <div className="p-3 bg-navy-900 rounded-xl border border-navy-800">
                  <div className="text-navy-400 text-xs">Dot Ball %</div>
                  <div className="text-xl font-bold text-white mt-1">{battingStats.dot_ball_percentage}%</div>
                  <div className="text-navy-500 text-xs mt-0.5">{battingStats.dot_balls} dots</div>
                </div>
                <div className="p-3 bg-navy-900 rounded-xl border border-navy-800">
                  <div className="text-navy-400 text-xs">High Score</div>
                  <div className="text-xl font-bold text-white mt-1">{battingStats.high_score}</div>
                  <div className="text-navy-500 text-xs mt-0.5">Career best</div>
                </div>
              </div>

              {/* Phase Breakdown Grid */}
              <div className="p-5 bg-navy-900/60 rounded-xl border border-navy-800">
                <h3 className="text-sm font-semibold text-white mb-4">Phase-Specific Batting Acceleration</h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  {Object.entries(battingStats.phase_splits).map(([phase, stats]) => (
                    <div key={phase} className="p-4 rounded-xl bg-navy-950 border border-navy-800">
                      <div className="flex items-center justify-between mb-2">
                        <span className="font-semibold text-sm text-pink-400">{phase}</span>
                        <span className="text-xs font-mono text-navy-400">{stats.balls} balls</span>
                      </div>
                      <div className="text-2xl font-bold text-white">{stats.runs} <span className="text-xs text-navy-400 font-normal">runs</span></div>
                      <div className="mt-2 flex items-center justify-between text-xs text-navy-300">
                        <span>Phase Strike Rate:</span>
                        <span className="font-semibold text-gold-400">{stats.strike_rate}</span>
                      </div>
                      {/* Bar indicator */}
                      <div className="w-full bg-navy-800 h-1.5 rounded-full mt-3 overflow-hidden">
                        <div
                          className="bg-pink-500 h-full rounded-full"
                          style={{ width: `${Math.min(stats.strike_rate / 2.5, 100)}%` }}
                        />
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          ) : (
            <div className="p-8 text-center text-navy-400 bg-navy-900/40 rounded-xl border border-navy-800">
              No domestic batting innings recorded for this player yet.
            </div>
          )}
        </div>
      )}

      {/* TAB 3: Recent Form Window */}
      {activeTab === "form" && (
        <div className="space-y-4">
          <div className="flex items-center justify-between bg-navy-900/60 p-4 rounded-xl border border-navy-800">
            <div>
              <span className="text-xs text-navy-400">Recent Form Diagnostic:</span>
              <h2 className="text-lg font-bold text-white">{selectedPlayer?.full_name}</h2>
            </div>
            <span className="text-xs font-mono text-gold-400 bg-gold-500/10 border border-gold-500/20 px-3 py-1 rounded-full">
              Window: Last 5 Match Innings
            </span>
          </div>

          {recentForm && recentForm.recent_matches.length > 0 ? (
            <div className="space-y-3">
              <p className="text-xs text-navy-400 italic">{recentForm.aggregate_metric_summary}</p>
              <div className="overflow-x-auto">
                <table className="w-full text-left border-collapse text-xs">
                  <thead>
                    <tr className="border-b border-navy-800 text-navy-400">
                      <th className="py-2.5 px-3">Date</th>
                      <th className="py-2.5 px-3">Opposition</th>
                      <th className="py-2.5 px-3">Venue</th>
                      <th className="py-2.5 px-3">Performance</th>
                      <th className="py-2.5 px-3">SR / Economy</th>
                    </tr>
                  </thead>
                  <tbody>
                    {recentForm.recent_matches.map((m, idx) => (
                      <tr key={idx} className="border-b border-navy-800/50 hover:bg-navy-900">
                        <td className="py-2.5 px-3 font-mono text-navy-300">{m.match_date}</td>
                        <td className="py-2.5 px-3 font-semibold text-white">{m.opposition_team}</td>
                        <td className="py-2.5 px-3 text-navy-300">{m.venue_name}</td>
                        <td className="py-2.5 px-3 font-bold text-pink-400">{m.runs_or_wickets_display}</td>
                        <td className="py-2.5 px-3 font-mono text-gold-400">{m.strike_rate_or_economy}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          ) : (
            <div className="p-8 text-center text-navy-400 bg-navy-900/40 rounded-xl border border-navy-800">
              No recent match scorecards logged in this window. Ingest domestic match scorecards in Data Acquisition Hub.
            </div>
          )}
        </div>
      )}

      {/* TAB 4: RR 8 Nov Data Pack Readiness */}
      {activeTab === "datapack" && (
        <div className="space-y-6">
          <div className="p-4 bg-navy-900 rounded-xl border border-navy-800 space-y-2">
            <h2 className="text-base font-bold text-white flex items-center gap-2">
              <span>Rajasthan Royals 8 November Proprietary Data Pack Ingestion Harness</span>
              <span className="text-xs bg-gold-500/20 text-gold-300 border border-gold-500/30 px-2 py-0.5 rounded">
                Pre-Flight Ready
              </span>
            </h2>
            <p className="text-xs text-navy-400">
              Paste or inspect incoming scout records. Test dynamic schema discovery, column mapping, missing DOB detection, and role-based security masking boundaries.
            </p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Input JSON */}
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <label className="text-xs font-semibold text-navy-300">Incoming Records Payload (JSON)</label>
                <button
                  onClick={handleDiscoverSchema}
                  className="px-3 py-1 bg-navy-800 hover:bg-navy-700 text-white rounded text-xs transition-colors"
                >
                  1. Discover Schema
                </button>
              </div>
              <textarea
                value={dataPackJson}
                onChange={(e) => setDataPackJson(e.target.value)}
                rows={14}
                className="w-full bg-navy-950 border border-navy-800 rounded-xl p-3 font-mono text-xs text-navy-200 focus:outline-none focus:border-pink-500"
              />
              <div className="flex justify-end gap-2">
                <button
                  onClick={handleIngestPack}
                  className="px-4 py-2 bg-pink-600 hover:bg-pink-700 text-white rounded-lg text-xs font-semibold shadow-lg shadow-pink-600/30 transition-colors"
                >
                  2. Simulate Ingestion & Conflict Audit
                </button>
              </div>
            </div>

            {/* Results / Audit View */}
            <div className="space-y-4">
              {schemaResult && (
                <div className="p-4 bg-navy-900 rounded-xl border border-navy-800 space-y-3">
                  <h3 className="text-xs font-semibold text-pink-400 uppercase tracking-wider">
                    Discovered Schema ({schemaResult.detected_columns.length} columns)
                  </h3>
                  <div className="flex flex-wrap gap-1.5">
                    {schemaResult.detected_columns.map((col) => (
                      <span key={col} className="px-2 py-1 bg-navy-950 border border-navy-700 rounded text-xs font-mono text-navy-300">
                        {col} ({schemaResult.column_type_hints[col] || "str"})
                      </span>
                    ))}
                  </div>
                  <div className="text-xs text-navy-400 pt-2 border-t border-navy-800">
                    <strong>Auto-Mapped Name:</strong> {schemaResult.recommended_mapping.name_col} •{" "}
                    <strong>DOB Col:</strong> {schemaResult.recommended_mapping.dob_col || "None"}
                  </div>
                </div>
              )}

              {ingestionSummary && (
                <div className="p-4 bg-navy-900 rounded-xl border border-navy-800 space-y-3">
                  <h3 className="text-xs font-semibold text-emerald-400 uppercase tracking-wider">
                    Ingestion Execution Telemetry
                  </h3>
                  <div className="grid grid-cols-2 gap-2 text-xs">
                    <div>Rows Processed: <span className="font-bold text-white">{ingestionSummary.total_rows_parsed}</span></div>
                    <div>Players Created: <span className="font-bold text-white">{ingestionSummary.players_created}</span></div>
                    <div>Missing DOBs: <span className="font-bold text-amber-400">{ingestionSummary.missing_dob_count}</span></div>
                    <div>Evaluations Logged: <span className="font-bold text-white">{ingestionSummary.evaluations_recorded}</span></div>
                  </div>
                  {ingestionSummary.missing_field_reports.length > 0 && (
                    <div className="pt-2 border-t border-navy-800">
                      <span className="text-xs text-amber-400 font-semibold">Missing DOB Audit:</span>
                      {ingestionSummary.missing_field_reports.map((r, i) => (
                        <p key={i} className="text-xs text-navy-400 mt-1">
                          • {r.player_name}: {r.action_taken}
                        </p>
                      ))}
                    </div>
                  )}
                </div>
              )}

              {/* Security Boundary Demo */}
              <div className="p-4 bg-navy-900/60 rounded-xl border border-navy-800 space-y-3">
                <div className="flex items-center justify-between">
                  <h4 className="text-xs font-semibold text-white">Security Isolation & Data Masking Preview</h4>
                  <div className="flex items-center gap-1 bg-navy-950 p-1 rounded-lg border border-navy-800 text-xs">
                    <button
                      onClick={() => setUserRole("public")}
                      className={`px-2 py-0.5 rounded ${userRole === "public" ? "bg-navy-800 text-white font-medium" : "text-navy-400"}`}
                    >
                      Public Role
                    </button>
                    <button
                      onClick={() => setUserRole("rr_scout_admin")}
                      className={`px-2 py-0.5 rounded ${userRole === "rr_scout_admin" ? "bg-pink-600 text-white font-medium" : "text-navy-400"}`}
                    >
                      RR Scout Admin
                    </button>
                  </div>
                </div>

                {evaluations.length > 0 ? (
                  <div className="p-3 bg-navy-950 rounded-lg border border-navy-800 text-xs space-y-2">
                    <div className="flex items-center justify-between">
                      <span className="text-navy-400">Scout ID:</span>
                      <span className="font-mono text-pink-400">{evaluations[0].scout_identifier}</span>
                    </div>
                    <div>
                      <span className="text-navy-400 block mb-0.5">Scout Strategic Evaluation:</span>
                      <p className="text-navy-200 font-mono bg-navy-900 p-2 rounded border border-navy-800">
                        {evaluations[0].proprietary_notes || "No notes"}
                      </p>
                    </div>
                  </div>
                ) : (
                  <p className="text-xs text-navy-500">Select a player to view confidential evaluations.</p>
                )}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
