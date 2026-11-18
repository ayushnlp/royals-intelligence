"use client";

import { useState, useEffect } from "react";
import {
  VenueSummaryItem,
  VenueDetailResponse,
  VenueScoringTrendsResponse,
  PitchEvidenceAnalysisResponse,
  WeatherObservationItem,
  UncappedPlayerVenuePerformanceResponse,
} from "@/types";
import {
  fetchVenues,
  fetchVenueDetail,
  fetchVenueScoringTrends,
  fetchVenuePitchAnalysis,
  fetchHistoricalWeather,
  fetchPlayerVenuePerformance,
} from "@/lib/api";
import {
  MapPin,
  Compass,
  Wind,
  Droplets,
  Thermometer,
  Shield,
  Layers,
  ChevronRight,
  Target,
  TrendingUp,
  AlertTriangle,
  Info,
  Calendar,
  Award,
  Sparkles,
  BarChart3,
  Sun,
  CloudRain,
  Eye,
  CheckCircle2,
} from "lucide-react";

export default function VenuePitchIntelligencePage() {
  const [venues, setVenues] = useState<VenueSummaryItem[]>([]);
  const [selectedVenueCode, setSelectedVenueCode] = useState<string>("SMS_JAIPUR");
  const [rrOnly, setRrOnly] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(true);

  // Venue Details state
  const [venueDetail, setVenueDetail] = useState<VenueDetailResponse | null>(null);
  const [scoringTrends, setScoringTrends] = useState<VenueScoringTrendsResponse | null>(null);
  const [pitchEvidence, setPitchEvidence] = useState<PitchEvidenceAnalysisResponse | null>(null);
  const [weatherObservations, setWeatherObservations] = useState<WeatherObservationItem[]>([]);
  const [activeTab, setActiveTab] = useState<"geometry" | "scoring" | "pitch" | "weather" | "uncapped_track">("geometry");

  // Uncapped Player Venue Performance state
  const [uncappedProspects] = useState([
    { id: "uncapped_rr_01", name: "Ashutosh Sharma", role: "Death-Overs Power Finisher" },
    { id: "uncapped_rr_02", name: "Priyansh Arya", role: "Top-Order Powerplay Striker" },
    { id: "uncapped_rr_03", name: "Vipraj Nigam", role: "Bowling All-Rounder (Leg-Spin)" },
  ]);
  const [selectedPlayerId, setSelectedPlayerId] = useState<string>("uncapped_rr_01");
  const [playerPerformance, setPlayerPerformance] = useState<UncappedPlayerVenuePerformanceResponse | null>(null);

  // Load venue directory
  useEffect(() => {
    async function loadDirectory() {
      setLoading(true);
      const res = await fetchVenues(rrOnly);
      setVenues(res);
      setLoading(false);
    }
    loadDirectory();
  }, [rrOnly]);

  // Load detailed venue dossier when selected venue changes
  useEffect(() => {
    async function loadVenueDossier() {
      if (!selectedVenueCode) return;
      const [detail, trends, pitch, weather, playerPerf] = await Promise.all([
        fetchVenueDetail(selectedVenueCode),
        fetchVenueScoringTrends(selectedVenueCode),
        fetchVenuePitchAnalysis(selectedVenueCode),
        fetchHistoricalWeather(selectedVenueCode, "2024-04-06"),
        fetchPlayerVenuePerformance(selectedVenueCode, selectedPlayerId),
      ]);
      setVenueDetail(detail);
      setScoringTrends(trends);
      setPitchEvidence(pitch);
      setWeatherObservations(weather);
      setPlayerPerformance(playerPerf);
    }
    loadVenueDossier();
  }, [selectedVenueCode, selectedPlayerId]);

  return (
    <div className="space-y-8 pb-12">
      {/* Top Header & Context Banner */}
      <section className="space-y-3">
        <div className="flex flex-wrap items-center gap-3 text-xs">
          <span className="font-mono font-bold tracking-widest text-[#E91E8F] uppercase">
            Rajasthan Royals Operations
          </span>
          <span className="text-slate-300">•</span>
          <span className="font-mono text-slate-500">
            Open-Meteo CC-BY 4.0 • BCCI Geometry
          </span>
          <span className="text-slate-300">•</span>
          <span className="inline-flex items-center gap-1.5 text-emerald-700 font-medium">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
            Environmental Analytics
          </span>
        </div>

        <div className="flex flex-col md:flex-row md:items-end justify-between gap-4">
          <div className="max-w-3xl space-y-2">
            <h1 className="text-3xl md:text-4xl font-extrabold tracking-tight text-slate-900 leading-tight">
              Stadium Geometry, Pitch Evidence & Weather Telemetry
            </h1>
            <p className="text-sm md:text-base text-slate-600 leading-relaxed font-normal">
              Measured boundary dimensions, empirical pace-vs-spin wicket shares, evening dew point progression,
              and venue-specific performance dossiers for uncapped prospects.
            </p>
          </div>

          {/* Home Grounds vs All Filter */}
          <div className="flex items-center gap-1.5 p-1 bg-slate-100 rounded-lg shrink-0">
            <button
              onClick={() => setRrOnly(false)}
              className={`px-3 py-1.5 text-xs font-semibold rounded-md transition-all ${
                !rrOnly
                  ? "bg-white text-slate-900 shadow-sm"
                  : "text-slate-500 hover:text-slate-700"
              }`}
            >
              All Venues ({venues.length})
            </button>
            <button
              onClick={() => setRrOnly(true)}
              className={`flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold rounded-md transition-all ${
                rrOnly
                  ? "bg-[#101C37] text-white shadow-sm"
                  : "text-slate-500 hover:text-slate-700"
              }`}
            >
              <Shield size={13} className="text-[#E91E8F]" />
              <span>RR Grounds (2)</span>
            </button>
          </div>
        </div>
      </section>

      {/* Stadium Directory Horizontal Carousel / Selector */}
      <div className="flex items-center gap-2 overflow-x-auto pb-2">
        {venues.map((v) => (
          <button
            key={v.venue_code}
            onClick={() => setSelectedVenueCode(v.venue_code)}
            className={`flex-shrink-0 px-4 py-2.5 rounded-xl border text-left transition-all ${
              selectedVenueCode === v.venue_code
                ? "bg-[#101C37] text-white border-[#101C37] shadow-md ring-2 ring-[#E91E8F]/20"
                : "bg-white text-slate-700 border-slate-200 hover:border-slate-300"
            }`}
          >
            <div className="flex items-center justify-between gap-3">
              <span className="font-bold text-xs">{v.name}</span>
              {v.is_rr_home && (
                <span className="px-1.5 py-0.2 rounded text-[9px] font-mono font-bold bg-[#E91E8F] text-white">
                  RR HOME
                </span>
              )}
            </div>
            <div className="text-[11px] text-slate-400 mt-0.5">
              {v.city} • {v.matches_hosted_count} matches
            </div>
          </button>
        ))}
      </div>

      {/* Selected Stadium Hero Dossier */}
      {venueDetail && (
        <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 space-y-6">
          {/* Stadium Title Bar */}
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-100 pb-5">
            <div>
              <div className="flex items-center gap-2 mb-1">
                <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-slate-100 text-slate-700">
                  {venueDetail.venue_code}
                </span>
                <span className="text-xs font-mono font-bold text-[#E91E8F]">
                  {venueDetail.rr_venue_type}
                </span>
                {venueDetail.altitude_m && (
                  <span className="text-xs text-slate-400 font-mono">
                    Altitude: {venueDetail.altitude_m}m
                  </span>
                )}
              </div>
              <h2 className="text-2xl font-black text-[#101C37]">{venueDetail.name}</h2>
              <p className="text-xs text-slate-500 mt-1 flex items-center gap-1.5">
                <MapPin size={13} className="text-[#E91E8F]" />
                {venueDetail.city}, {venueDetail.state ? `${venueDetail.state}, ` : ""}{venueDetail.country} • GPS: {venueDetail.latitude}°N, {venueDetail.longitude}°E
              </p>
            </div>

            {/* Quick Metrics Badge */}
            <div className="flex items-center gap-4 text-right">
              <div className="p-3 bg-slate-50 rounded-xl border border-slate-100">
                <div className="text-[10px] font-bold uppercase tracking-wider text-slate-400">Total Matches</div>
                <div className="text-lg font-black text-[#101C37]">{venueDetail.matches_hosted_count}</div>
              </div>
              <div className="p-3 bg-slate-50 rounded-xl border border-slate-100">
                <div className="text-[10px] font-bold uppercase tracking-wider text-slate-400">Soil Type</div>
                <div className="text-sm font-extrabold text-[#E91E8F] mt-0.5">{venueDetail.pitch_soil_type || "Standard Turf"}</div>
              </div>
            </div>
          </div>

          {/* Navigation Tabs within Venue */}
          <div className="flex flex-wrap gap-2 border-b border-slate-200 pb-2">
            <button
              onClick={() => setActiveTab("geometry")}
              className={`flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg text-xs font-bold transition-all ${
                activeTab === "geometry"
                  ? "bg-[#101C37] text-white shadow-sm"
                  : "text-slate-600 hover:bg-slate-100"
              }`}
            >
              <Compass size={14} />
              Boundary Geometry
            </button>
            <button
              onClick={() => setActiveTab("scoring")}
              className={`flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg text-xs font-bold transition-all ${
                activeTab === "scoring"
                  ? "bg-[#101C37] text-white shadow-sm"
                  : "text-slate-600 hover:bg-slate-100"
              }`}
            >
              <TrendingUp size={14} />
              Historical Scoring & Phases
            </button>
            <button
              onClick={() => setActiveTab("pitch")}
              className={`flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg text-xs font-bold transition-all ${
                activeTab === "pitch"
                  ? "bg-[#101C37] text-white shadow-sm"
                  : "text-slate-600 hover:bg-slate-100"
              }`}
            >
              <Target size={14} />
              Pitch & Pace-vs-Spin Evidence
            </button>
            <button
              onClick={() => setActiveTab("weather")}
              className={`flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg text-xs font-bold transition-all ${
                activeTab === "weather"
                  ? "bg-[#101C37] text-white shadow-sm"
                  : "text-slate-600 hover:bg-slate-100"
              }`}
            >
              <Droplets size={14} />
              Weather & Dew Telemetry
            </button>
            <button
              onClick={() => setActiveTab("uncapped_track")}
              className={`flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg text-xs font-bold transition-all ${
                activeTab === "uncapped_track"
                  ? "bg-[#E91E8F] text-white shadow-sm"
                  : "text-[#E91E8F] bg-pink-50 hover:bg-pink-100"
              }`}
            >
              <Award size={14} />
              Uncapped Prospect Tracking
            </button>
          </div>

          {/* TAB 1: BOUNDARY GEOMETRY */}
          {activeTab === "geometry" && (
            <div className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {/* Straight Boundary */}
                <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 text-center">
                  <div className="text-[10px] font-bold uppercase tracking-wider text-slate-400">
                    Straight Boundary (Down the V)
                  </div>
                  <div className="text-3xl font-black text-[#101C37] my-1">
                    {venueDetail.boundary_dimensions.straight_m ? (
                      <span>{venueDetail.boundary_dimensions.straight_m} <span className="text-sm font-normal text-slate-500">meters</span></span>
                    ) : (
                      <span className="text-sm font-semibold text-slate-400">Unavailable</span>
                    )}
                  </div>
                  <div className="text-[11px] text-slate-500">Stump to sight-screen distance</div>
                </div>

                {/* Off-Side Boundary */}
                <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 text-center">
                  <div className="text-[10px] font-bold uppercase tracking-wider text-slate-400">
                    Off-Side Square Boundary
                  </div>
                  <div className="text-3xl font-black text-[#101C37] my-1">
                    {venueDetail.boundary_dimensions.off_boundary_m ? (
                      <span>{venueDetail.boundary_dimensions.off_boundary_m} <span className="text-sm font-normal text-slate-500">meters</span></span>
                    ) : (
                      <span className="text-sm font-semibold text-slate-400">Unavailable</span>
                    )}
                  </div>
                  <div className="text-[11px] text-slate-500">Pitch centre to point/cover boundary</div>
                </div>

                {/* Leg-Side Boundary */}
                <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 text-center">
                  <div className="text-[10px] font-bold uppercase tracking-wider text-slate-400">
                    Leg-Side Square Boundary
                  </div>
                  <div className="text-3xl font-black text-[#101C37] my-1">
                    {venueDetail.boundary_dimensions.leg_boundary_m ? (
                      <span>{venueDetail.boundary_dimensions.leg_boundary_m} <span className="text-sm font-normal text-slate-500">meters</span></span>
                    ) : (
                      <span className="text-sm font-semibold text-slate-400">Unavailable</span>
                    )}
                  </div>
                  <div className="text-[11px] text-slate-500">Pitch centre to square leg / midwicket</div>
                </div>
              </div>

              {/* Surface Details & Drainage */}
              <div className="p-5 rounded-xl border border-slate-200 bg-slate-50/60 space-y-3">
                <h4 className="text-xs font-bold uppercase tracking-wider text-[#101C37] flex items-center gap-1.5">
                  <Layers size={14} className="text-[#D6B56D]" />
                  Soil, Turf & Environmental Specification
                </h4>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs text-slate-600">
                  <div>
                    <span className="font-bold text-[#101C37]">Soil Composition:</span>{" "}
                    {venueDetail.surface_details.soil_composition || "Standard Clay/Loam Turf"}
                  </div>
                  <div>
                    <span className="font-bold text-[#101C37]">Grass Specification:</span>{" "}
                    {venueDetail.surface_details.grass_type || "Bermuda Turf"}
                  </div>
                  <div>
                    <span className="font-bold text-[#101C37]">Outfield Speed:</span>{" "}
                    {venueDetail.surface_details.outfield_speed || "Medium-Fast Outfield"}
                  </div>
                  <div>
                    <span className="font-bold text-[#101C37]">Evening Dew Tendency:</span>{" "}
                    {venueDetail.surface_details.dew_tendency || "Moderate coastal / atmospheric dew"}
                  </div>
                </div>
                <div className="pt-2 border-t border-slate-200/80 text-[11px] text-slate-500 flex items-center justify-between">
                  <span>Dimension Source: {venueDetail.boundary_dimensions.dimension_source || "Pending BCCI survey"}</span>
                  <span className="flex items-center gap-1 text-emerald-600 font-semibold">
                    <CheckCircle2 size={13} /> {venueDetail.boundary_dimensions.status}
                  </span>
                </div>
              </div>
            </div>
          )}

          {/* TAB 2: HISTORICAL SCORING & PHASES */}
          {activeTab === "scoring" && scoringTrends && (
            <div className="space-y-6">
              {/* Scoring Summary Cards */}
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                <div className="p-4 bg-slate-50 rounded-xl border border-slate-200 text-center">
                  <div className="text-[10px] font-bold uppercase text-slate-400">1st Innings Average</div>
                  <div className="text-2xl font-black text-[#101C37] mt-1">{scoringTrends.avg_first_innings_score}</div>
                  <div className="text-[10px] text-slate-500 mt-0.5">Par Score Target</div>
                </div>
                <div className="p-4 bg-slate-50 rounded-xl border border-slate-200 text-center">
                  <div className="text-[10px] font-bold uppercase text-slate-400">2nd Innings Average</div>
                  <div className="text-2xl font-black text-[#101C37] mt-1">{scoringTrends.avg_second_innings_score}</div>
                  <div className="text-[10px] text-slate-500 mt-0.5">Chasing Par</div>
                </div>
                <div className="p-4 bg-slate-50 rounded-xl border border-slate-200 text-center">
                  <div className="text-[10px] font-bold uppercase text-slate-400">Chasing Win Rate</div>
                  <div className="text-2xl font-black text-emerald-600 mt-1">
                    {scoringTrends.match_outcome_by_innings.chase_win_pct}%
                  </div>
                  <div className="text-[10px] text-slate-500 mt-0.5">Bat 2nd Advantage</div>
                </div>
                <div className="p-4 bg-slate-50 rounded-xl border border-slate-200 text-center">
                  <div className="text-[10px] font-bold uppercase text-slate-400">Avg Wickets / Match</div>
                  <div className="text-2xl font-black text-[#E91E8F] mt-1">{scoringTrends.avg_wickets_per_innings}</div>
                  <div className="text-[10px] text-slate-500 mt-0.5">Wickets fallen</div>
                </div>
              </div>

              {/* Phase Run Rates */}
              <div className="p-5 rounded-xl border border-slate-200 bg-slate-50/60 space-y-3">
                <h4 className="text-xs font-bold uppercase tracking-wider text-[#101C37]">
                  Phase-Specific Run Rates at {scoringTrends.venue_name}
                </h4>
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                  <div className="p-3 bg-white rounded-lg border border-slate-200">
                    <div className="text-[10px] font-bold text-slate-400 uppercase">Powerplay (Overs 0-5)</div>
                    <div className="text-xl font-black text-[#101C37] mt-0.5">
                      {scoringTrends.phase_scoring_rates.powerplay} <span className="text-xs font-normal text-slate-500">rpo</span>
                    </div>
                  </div>
                  <div className="p-3 bg-white rounded-lg border border-slate-200">
                    <div className="text-[10px] font-bold text-slate-400 uppercase">Middle Overs (Overs 6-14)</div>
                    <div className="text-xl font-black text-[#101C37] mt-0.5">
                      {scoringTrends.phase_scoring_rates.middle} <span className="text-xs font-normal text-slate-500">rpo</span>
                    </div>
                  </div>
                  <div className="p-3 bg-white rounded-lg border border-slate-200">
                    <div className="text-[10px] font-bold text-slate-400 uppercase">Death Overs (Overs 15-19)</div>
                    <div className="text-xl font-black text-[#E91E8F] mt-0.5">
                      {scoringTrends.phase_scoring_rates.death} <span className="text-xs font-normal text-slate-500">rpo</span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Sample Size Transparency */}
              {scoringTrends.sample_size_warning && (
                <div className="p-3 bg-amber-50 rounded-xl border border-amber-200 text-xs text-amber-800 flex items-center gap-2">
                  <AlertTriangle size={15} className="text-amber-600 shrink-0" />
                  <span>{scoringTrends.sample_size_warning}</span>
                </div>
              )}
            </div>
          )}

          {/* TAB 3: PITCH & PACE-VS-SPIN EVIDENCE */}
          {activeTab === "pitch" && pitchEvidence && (
            <div className="space-y-6">
              {/* Evidence Classification Banner */}
              <div className="flex flex-wrap items-center justify-between gap-3 p-4 bg-gradient-to-r from-slate-50 to-pink-50/30 rounded-xl border border-slate-200">
                <div>
                  <div className="text-[10px] font-bold uppercase tracking-wider text-slate-400">
                    Empirical Conditions Classification
                  </div>
                  <div className="text-xl font-black text-[#101C37] mt-0.5">
                    {pitchEvidence.conditions_evidence_classification}
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <span className="px-2.5 py-1 rounded text-xs font-mono font-bold bg-[#E91E8F] text-white">
                    Confidence: {pitchEvidence.evidence_confidence}
                  </span>
                  <span className="text-xs font-mono text-slate-500">
                    {pitchEvidence.sample_matches_evaluated} matches evaluated
                  </span>
                </div>
              </div>

              {/* Pace vs Spin Distribution */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {/* Pace Dimension */}
                <div className="p-5 rounded-xl border border-slate-200 bg-blue-50/20">
                  <div className="flex items-center justify-between mb-3">
                    <span className="text-xs font-bold text-[#101C37]">Pace Bowler Impact</span>
                    <span className="text-xs font-mono font-extrabold text-blue-600">
                      {pitchEvidence.observed_pace_vs_spin.pace_wickets_share_pct}% wickets
                    </span>
                  </div>
                  <div className="grid grid-cols-2 gap-2 text-center text-xs">
                    <div className="p-2 bg-white rounded border border-slate-100">
                      <div className="text-[10px] text-slate-400">Economy</div>
                      <div className="font-bold text-[#101C37]">{pitchEvidence.observed_pace_vs_spin.pace_economy}</div>
                    </div>
                    <div className="p-2 bg-white rounded border border-slate-100">
                      <div className="text-[10px] text-slate-400">Average</div>
                      <div className="font-bold text-[#101C37]">{pitchEvidence.observed_pace_vs_spin.pace_average}</div>
                    </div>
                  </div>
                </div>

                {/* Spin Dimension */}
                <div className="p-5 rounded-xl border border-slate-200 bg-amber-50/20">
                  <div className="flex items-center justify-between mb-3">
                    <span className="text-xs font-bold text-[#101C37]">Spin Bowler Impact</span>
                    <span className="text-xs font-mono font-extrabold text-amber-600">
                      {pitchEvidence.observed_pace_vs_spin.spin_wickets_share_pct}% wickets
                    </span>
                  </div>
                  <div className="grid grid-cols-2 gap-2 text-center text-xs">
                    <div className="p-2 bg-white rounded border border-slate-100">
                      <div className="text-[10px] text-slate-400">Economy</div>
                      <div className="font-bold text-[#101C37]">{pitchEvidence.observed_pace_vs_spin.spin_economy}</div>
                    </div>
                    <div className="p-2 bg-white rounded border border-slate-100">
                      <div className="text-[10px] text-slate-400">Average</div>
                      <div className="font-bold text-[#101C37]">{pitchEvidence.observed_pace_vs_spin.spin_average}</div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Boundary vs Dot-Ball Distribution */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div className="p-4 bg-slate-50 rounded-xl border border-slate-200">
                  <div className="text-[10px] font-bold uppercase text-slate-400">Boundary Runs Contribution</div>
                  <div className="text-xl font-black text-[#101C37] mt-1">
                    {pitchEvidence.boundary_patterns.boundary_runs_pct}%
                  </div>
                  <div className="text-[11px] text-slate-500 mt-0.5">
                    ~{pitchEvidence.boundary_patterns.fours_per_match} fours, ~{pitchEvidence.boundary_patterns.sixes_per_match} sixes per fixture
                  </div>
                </div>
                <div className="p-4 bg-slate-50 rounded-xl border border-slate-200">
                  <div className="text-[10px] font-bold uppercase text-slate-400">Dot Ball Percentage</div>
                  <div className="text-xl font-black text-[#101C37] mt-1">
                    {pitchEvidence.dot_ball_patterns.dot_ball_pct}%
                  </div>
                  <div className="text-[11px] text-slate-500 mt-0.5">
                    Percentage of deliveries yielding zero runs
                  </div>
                </div>
              </div>

              {/* Observed Summary & Caveats */}
              <div className="p-4 bg-slate-50 rounded-xl border border-slate-200 text-xs text-slate-600 space-y-2">
                <p><span className="font-bold text-[#101C37]">Observed Evidence:</span> {pitchEvidence.observed_statistical_summary}</p>
                <p className="text-[11px] text-slate-500 italic border-t border-slate-200 pt-2">
                  * {pitchEvidence.limitations_disclaimer}
                </p>
              </div>
            </div>
          )}

          {/* TAB 4: WEATHER & DEW TELEMETRY */}
          {activeTab === "weather" && (
            <div className="space-y-6">
              <div className="flex flex-wrap items-center justify-between gap-3 p-4 bg-slate-50 rounded-xl border border-slate-200">
                <div className="flex items-center gap-2">
                  <Droplets className="text-blue-500" size={18} />
                  <div>
                    <h4 className="text-xs font-bold text-[#101C37]">Open-Meteo Hourly Telemetry</h4>
                    <p className="text-[11px] text-slate-500">Attribution: Weather data by Open-Meteo.com under CC-BY 4.0</p>
                  </div>
                </div>
                <span className="px-2.5 py-1 rounded text-xs font-mono font-bold bg-emerald-100 text-emerald-800 border border-emerald-200">
                  HISTORICAL OBSERVATION (VERIFIED)
                </span>
              </div>

              {/* Hourly Weather Cards */}
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                {weatherObservations.map((obs, idx) => (
                  <div
                    key={idx}
                    className="p-4 rounded-xl border border-slate-200 bg-white hover:border-slate-300 transition-all space-y-2"
                  >
                    <div className="flex items-center justify-between text-xs">
                      <span className="font-mono font-bold text-[#101C37]">
                        {obs.observation_time.split("T")[-1] || obs.observation_time}
                      </span>
                      <span className={`px-2 py-0.5 rounded text-[10px] font-mono font-bold ${
                        obs.dew_severity_risk === "HIGH_DEW_RISK"
                          ? "bg-red-100 text-red-700"
                          : obs.dew_severity_risk === "MODERATE"
                          ? "bg-amber-100 text-amber-700"
                          : "bg-emerald-100 text-emerald-700"
                      }`}>
                        {obs.dew_severity_risk}
                      </span>
                    </div>

                    <div className="grid grid-cols-2 gap-2 text-xs py-2 border-y border-slate-100">
                      <div>
                        <span className="text-slate-400 text-[10px]">Temperature:</span>
                        <div className="font-black text-sm text-[#101C37]">{obs.temperature_c}°C</div>
                      </div>
                      <div>
                        <span className="text-slate-400 text-[10px]">Humidity:</span>
                        <div className="font-black text-sm text-[#101C37]">{obs.relative_humidity_pct}%</div>
                      </div>
                      <div>
                        <span className="text-slate-400 text-[10px]">Dew Point:</span>
                        <div className="font-bold text-[#101C37]">{obs.dew_point_c}°C</div>
                      </div>
                      <div>
                        <span className="text-slate-400 text-[10px]">Wind:</span>
                        <div className="font-bold text-[#101C37]">{obs.wind_speed_kph} km/h {obs.wind_direction_compass}</div>
                      </div>
                    </div>

                    <div className="text-[10px] text-slate-400 flex items-center justify-between">
                      <span>Phase: {obs.phase_in_match}</span>
                      <span>{obs.weather_condition}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* TAB 5: UNCAPPED PROSPECT TRACKING */}
          {activeTab === "uncapped_track" && (
            <div className="space-y-6">
              {/* Prospect Selector */}
              <div className="flex flex-wrap items-center gap-2 p-4 bg-slate-50 rounded-xl border border-slate-200">
                <span className="text-xs font-bold text-slate-400 uppercase mr-2">Select Uncapped Talent:</span>
                {uncappedProspects.map((p) => (
                  <button
                    key={p.id}
                    onClick={() => setSelectedPlayerId(p.id)}
                    className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
                      selectedPlayerId === p.id
                        ? "bg-[#E91E8F] text-white shadow-sm"
                        : "bg-white text-slate-700 border border-slate-200 hover:bg-slate-100"
                    }`}
                  >
                    {p.name}
                  </button>
                ))}
              </div>

              {/* Player Venue Record */}
              {playerPerformance && (
                <div className="p-6 rounded-2xl border border-slate-200 bg-white shadow-sm space-y-4">
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-100 pb-4">
                    <div>
                      <div className="flex items-center gap-2 mb-1">
                        <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-[#E91E8F]/15 text-[#E91E8F]">
                          {playerPerformance.eligibility_status}
                        </span>
                        <span className="text-xs font-mono text-slate-400">
                          {playerPerformance.player_id}
                        </span>
                      </div>
                      <h3 className="text-xl font-bold text-[#101C37]">
                        {playerPerformance.player_name} at {playerPerformance.venue_name}
                      </h3>
                      <p className="text-xs text-slate-500 mt-0.5">Role Archetype: {playerPerformance.role_archetype}</p>
                    </div>

                    <div className="p-3 bg-slate-50 rounded-xl border border-slate-200 text-right">
                      <div className="text-[10px] font-bold uppercase text-slate-400">Matches at Venue</div>
                      <div className="text-base font-extrabold text-[#101C37]">{playerPerformance.matches_at_venue}</div>
                    </div>
                  </div>

                  {/* Batting vs Bowling Dual Grid at this venue */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="p-4 rounded-xl border border-slate-200 bg-pink-50/20">
                      <h4 className="text-xs font-bold text-[#101C37] mb-2 flex items-center gap-1.5">
                        <TrendingUp size={14} className="text-[#E91E8F]" /> Batting at Venue
                      </h4>
                      <div className="grid grid-cols-3 gap-2 text-center text-xs">
                        <div className="p-2 bg-white rounded border border-slate-100">
                          <div className="text-[10px] text-slate-400">Runs</div>
                          <div className="font-extrabold text-sm text-[#101C37]">{playerPerformance.batting_at_venue.runs}</div>
                        </div>
                        <div className="p-2 bg-white rounded border border-slate-100">
                          <div className="text-[10px] text-slate-400">Strike Rate</div>
                          <div className="font-extrabold text-sm text-[#E91E8F]">{playerPerformance.batting_at_venue.strike_rate}</div>
                        </div>
                        <div className="p-2 bg-white rounded border border-slate-100">
                          <div className="text-[10px] text-slate-400">Average</div>
                          <div className="font-bold text-sm text-[#101C37]">{playerPerformance.batting_at_venue.average ?? "N/A"}</div>
                        </div>
                      </div>
                      {playerPerformance.batting_at_venue.death_sr && (
                        <div className="text-[11px] text-slate-600 mt-2">
                          Death Overs SR at this ground: <span className="font-bold text-[#E91E8F]">{playerPerformance.batting_at_venue.death_sr}</span>
                        </div>
                      )}
                    </div>

                    <div className="p-4 rounded-xl border border-slate-200 bg-blue-50/20">
                      <h4 className="text-xs font-bold text-[#101C37] mb-2 flex items-center gap-1.5">
                        <Target size={14} className="text-blue-600" /> Bowling at Venue
                      </h4>
                      <div className="grid grid-cols-3 gap-2 text-center text-xs">
                        <div className="p-2 bg-white rounded border border-slate-100">
                          <div className="text-[10px] text-slate-400">Wickets</div>
                          <div className="font-extrabold text-sm text-[#101C37]">{playerPerformance.bowling_at_venue.wickets}</div>
                        </div>
                        <div className="p-2 bg-white rounded border border-slate-100">
                          <div className="text-[10px] text-slate-400">Economy</div>
                          <div className="font-extrabold text-sm text-[#101C37]">{playerPerformance.bowling_at_venue.economy}</div>
                        </div>
                        <div className="p-2 bg-white rounded border border-slate-100">
                          <div className="text-[10px] text-slate-400">Overs</div>
                          <div className="font-bold text-sm text-[#101C37]">{playerPerformance.bowling_at_venue.overs}</div>
                        </div>
                      </div>
                    </div>
                  </div>

                  {playerPerformance.sample_size_warning && (
                    <div className="p-3 bg-amber-50 rounded-xl border border-amber-200 text-xs text-amber-800 flex items-center gap-2">
                      <AlertTriangle size={14} className="text-amber-600 shrink-0" />
                      <span>{playerPerformance.sample_size_warning}</span>
                    </div>
                  )}

                  <div className="text-[10px] text-slate-400 italic">
                    * Scope Restriction: Analysis strictly covers uncapped domestic players for Rajasthan Royals auction preparation. Capped international players are excluded.
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
