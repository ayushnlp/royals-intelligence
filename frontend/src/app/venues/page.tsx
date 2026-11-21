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
  RefreshCw,
} from "lucide-react";

export default function VenuePitchIntelligencePage() {
  const [venues, setVenues] = useState<VenueSummaryItem[]>([]);
  const [selectedVenueCode, setSelectedVenueCode] = useState<string>("SMS_JAIPUR");
  const [rrOnly, setRrOnly] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(true);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

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
  const loadDirectory = async () => {
    setLoading(true);
    setErrorMsg(null);
    try {
      const res = await fetchVenues(rrOnly);
      setVenues(res);
      if (res.length > 0) {
        if (!selectedVenueCode || !res.some((v) => v.venue_code === selectedVenueCode)) {
          setSelectedVenueCode(res[0].venue_code);
        }
      } else {
        setSelectedVenueCode("");
      }
    } catch (err: any) {
      setErrorMsg(err.message || "Failed to load registered cricket venues.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDirectory();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [rrOnly]);

  // Load detailed venue dossier when selected venue changes
  useEffect(() => {
    let isCurrent = true;
    async function loadVenueDossier() {
      if (!selectedVenueCode) {
        setVenueDetail(null);
        setScoringTrends(null);
        setPitchEvidence(null);
        setWeatherObservations([]);
        setPlayerPerformance(null);
        return;
      }
      try {
        const [detail, trends, pitch, weather, playerPerf] = await Promise.all([
          fetchVenueDetail(selectedVenueCode).catch((e) => {
            console.warn("Venue detail fetch notice:", e);
            return null;
          }),
          fetchVenueScoringTrends(selectedVenueCode).catch((e) => {
            console.warn("Scoring trends fetch notice:", e);
            return null;
          }),
          fetchVenuePitchAnalysis(selectedVenueCode).catch((e) => {
            console.warn("Pitch analysis fetch notice:", e);
            return null;
          }),
          fetchHistoricalWeather(selectedVenueCode, "2024-04-06").catch((e) => {
            console.warn("Weather fetch notice:", e);
            return [];
          }),
          fetchPlayerVenuePerformance(selectedVenueCode, selectedPlayerId).catch((e) => {
            console.warn("Player venue performance fetch notice:", e);
            return null;
          }),
        ]);
        if (isCurrent) {
          setVenueDetail(detail);
          setScoringTrends(trends);
          setPitchEvidence(pitch);
          setWeatherObservations(weather);
          setPlayerPerformance(playerPerf);
        }
      } catch (err) {
        console.error("Failed to load venue dossier:", err);
      }
    }
    loadVenueDossier();
    return () => {
      isCurrent = false;
    };
  }, [selectedVenueCode, selectedPlayerId]);

  return (
    <div className="space-y-8 pb-12">
      {/* Top Header & Context Banner */}
      <section className="space-y-3">
        <div className="flex flex-wrap items-center gap-3 text-xs">
          <span className="font-mono font-bold tracking-widest text-[#101D3A] uppercase px-2.5 py-1 rounded-md bg-[#D4145A]/10 border border-[#D4145A]/30">
            Rajasthan Royals Operations
          </span>
          <span className="text-[#101D3A]/30">•</span>
          <span className="font-mono text-[#52627A]">
            Open-Meteo CC-BY 4.0 • BCCI Geometry
          </span>
          <span className="text-[#101D3A]/30">•</span>
          <span className="inline-flex items-center gap-1.5 text-[#D4145A] font-medium">
            <span className="w-1.5 h-1.5 rounded-full bg-[#D4145A]" />
            Environmental Analytics
          </span>
        </div>

        <div className="flex flex-col md:flex-row md:items-end justify-between gap-4">
          <div className="max-w-3xl space-y-2">
            <h1 className="text-3xl md:text-4xl font-extrabold tracking-tight text-[#101D3A] leading-tight">
              Stadium Geometry, Pitch Evidence & Weather Telemetry
            </h1>
            <p className="text-sm md:text-base text-[#52627A] leading-relaxed font-normal">
              Measured boundary dimensions, empirical pace-vs-spin wicket shares, evening dew point progression,
              and venue-specific performance dossiers for uncapped prospects.
            </p>
          </div>

          {/* Home Grounds vs All Filter */}
          <div className="flex items-center gap-1.5 p-1 bg-[#F8E8EF] rounded-lg shrink-0">
            <button
              onClick={() => setRrOnly(false)}
              className={`px-3 py-1.5 text-xs font-semibold rounded-md transition-all ${
                !rrOnly
                  ? "bg-white text-[#101D3A] shadow-sm"
                  : "text-[#52627A] hover:text-[#101D3A]"
              }`}
            >
              All Venues ({venues.length})
            </button>
            <button
              onClick={() => setRrOnly(true)}
              className={`flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold rounded-md transition-all ${
                rrOnly
                  ? "bg-[#101D3A] text-white shadow-sm"
                  : "text-[#52627A] hover:text-[#101D3A]"
              }`}
            >
              <Shield size={13} className="text-[#101D3A]" />
              <span>RR Grounds (2)</span>
            </button>
          </div>
        </div>
      </section>

      {/* Connection / Error Notice */}
      {errorMsg && (
        <div className="p-4 rounded-xl bg-[#D4145A]/10 border border-[#D4145A]/30 text-[#D4145A] flex items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <AlertTriangle className="w-5 h-5 text-[#D4145A] shrink-0" />
            <div>
              <div className="text-xs font-bold">Venue Intelligence Connection Notice</div>
              <div className="text-xs text-[#D4145A] mt-0.5">{errorMsg}</div>
            </div>
          </div>
          <button
            onClick={loadDirectory}
            className="px-3 py-1.5 rounded-lg bg-[#D4145A] text-white font-bold text-xs hover:bg-[#A80F50] transition-colors shrink-0 flex items-center gap-1.5"
          >
            <RefreshCw className="w-3.5 h-3.5" />
            <span>Retry</span>
          </button>
        </div>
      )}

      {/* Loading Directory Skeleton */}
      {loading && (
        <div className="p-8 rounded-2xl bg-white border border-[#E7EAF0] shadow-sm flex flex-col items-center justify-center gap-2 text-[#52627A]">
          <RefreshCw className="w-5 h-5 animate-spin text-[#D4145A]" />
          <span className="text-xs font-mono">Loading stadium directory from backend...</span>
        </div>
      )}

      {/* Empty State */}
      {!loading && !errorMsg && venues.length === 0 && (
        <div className="p-12 text-center rounded-2xl bg-white border border-[#E7EAF0] shadow-sm space-y-2">
          <MapPin className="w-8 h-8 text-[#101D3A]/30 mx-auto" />
          <div className="text-sm font-bold text-[#101D3A]">No Venues Found</div>
          <p className="text-xs text-[#52627A]">
            No cricket venues registered matching {rrOnly ? "Rajasthan Royals home venue" : "catalog"} filter.
          </p>
        </div>
      )}

      {/* Stadium Directory Horizontal Carousel / Selector */}
      {!loading && venues.length > 0 && (
        <div className="flex items-center gap-2 overflow-x-auto pb-2">
          {venues.map((v) => (
            <button
              key={v.venue_code}
              onClick={() => setSelectedVenueCode(v.venue_code)}
              className={`flex-shrink-0 px-4 py-2.5 rounded-xl border text-left transition-all ${
                selectedVenueCode === v.venue_code
                  ? "bg-[#101D3A] text-white border-[#101D3A] shadow-md ring-2 ring-[#D4145A]/30"
                  : "bg-white text-[#101D3A] border-[#E7EAF0] hover:border-[#101D3A]/20"
              }`}
            >
              <div className="flex items-center justify-between gap-3">
                <span className="font-bold text-xs">{v.name}</span>
                {v.is_rr_home && (
                  <span className="px-1.5 py-0.2 rounded text-[9px] font-mono font-bold bg-[#101D3A] text-white">
                    RR HOME
                  </span>
                )}
              </div>
              <div className="text-[11px] text-[#52627A] mt-0.5">
                {v.city} • {v.matches_hosted_count} matches
              </div>
            </button>
          ))}
        </div>
      )}

      {/* Selected Stadium Hero Dossier */}
      {venueDetail && (
        <div className="bg-white rounded-2xl border border-[#E7EAF0] shadow-sm p-6 space-y-6">
          {/* Stadium Title Bar */}
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-[#E7EAF0] pb-5">
            <div>
              <div className="flex items-center gap-2 mb-1">
                <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-[#F8E8EF] text-[#101D3A]">
                  {venueDetail.venue_code}
                </span>
                <span className="text-xs font-mono font-bold text-[#101D3A]">
                  {venueDetail.rr_venue_type}
                </span>
                {venueDetail.altitude_m && (
                  <span className="text-xs text-[#52627A] font-mono">
                    Altitude: {venueDetail.altitude_m}m
                  </span>
                )}
              </div>
              <h2 className="text-2xl font-black text-[#101D3A]">{venueDetail.name}</h2>
              <p className="text-xs text-[#52627A] mt-1 flex items-center gap-1.5">
                <MapPin size={13} className="text-[#101D3A]" />
                {venueDetail.city}, {venueDetail.state ? `${venueDetail.state}, ` : ""}{venueDetail.country} • GPS: {venueDetail.latitude}°N, {venueDetail.longitude}°E
              </p>
            </div>

            {/* Quick Metrics Badge */}
            <div className="flex items-center gap-4 text-right">
              <div className="p-3 bg-white rounded-xl border border-[#E7EAF0]">
                <div className="text-[10px] font-bold uppercase tracking-wider text-[#52627A]">Total Matches</div>
                <div className="text-lg font-black text-[#101D3A]">{venueDetail.matches_hosted_count}</div>
              </div>
              <div className="p-3 bg-white rounded-xl border border-[#E7EAF0]">
                <div className="text-[10px] font-bold uppercase tracking-wider text-[#52627A]">Soil Type</div>
                <div className="text-sm font-extrabold text-[#101D3A] mt-0.5">{venueDetail.pitch_soil_type || "Standard Turf"}</div>
              </div>
            </div>
          </div>

          {/* Navigation Tabs within Venue */}
          <div className="flex items-center gap-6 border-b border-[#E7EAF0] overflow-x-auto">
            <button
              onClick={() => setActiveTab("geometry")}
              className={`flex items-center gap-2 py-3 text-xs font-semibold transition-all border-b-2 -mb-px whitespace-nowrap ${
                activeTab === "geometry"
                  ? "border-[#101D3A] text-[#101D3A] font-bold"
                  : "border-transparent text-[#52627A] hover:text-[#101D3A]"
              }`}
            >
              <Compass size={14} className="text-[#D4145A]" />
              <span>Boundary Geometry</span>
            </button>
            <button
              onClick={() => setActiveTab("scoring")}
              className={`flex items-center gap-2 py-3 text-xs font-semibold transition-all border-b-2 -mb-px whitespace-nowrap ${
                activeTab === "scoring"
                  ? "border-[#101D3A] text-[#101D3A] font-bold"
                  : "border-transparent text-[#52627A] hover:text-[#101D3A]"
              }`}
            >
              <TrendingUp size={14} className="text-[#D4145A]" />
              <span>Historical Scoring & Phases</span>
            </button>
            <button
              onClick={() => setActiveTab("pitch")}
              className={`flex items-center gap-2 py-3 text-xs font-semibold transition-all border-b-2 -mb-px whitespace-nowrap ${
                activeTab === "pitch"
                  ? "border-[#101D3A] text-[#101D3A] font-bold"
                  : "border-transparent text-[#52627A] hover:text-[#101D3A]"
              }`}
            >
              <Target size={14} className="text-[#101D3A]" />
              <span>Pitch & Pace-vs-Spin Evidence</span>
            </button>
            <button
              onClick={() => setActiveTab("weather")}
              className={`flex items-center gap-2 py-3 text-xs font-semibold transition-all border-b-2 -mb-px whitespace-nowrap ${
                activeTab === "weather"
                  ? "border-[#101D3A] text-[#101D3A] font-bold"
                  : "border-transparent text-[#52627A] hover:text-[#101D3A]"
              }`}
            >
              <Droplets size={14} className="text-[#101D3A]" />
              <span>Weather & Dew Telemetry</span>
            </button>
            <button
              onClick={() => setActiveTab("uncapped_track")}
              className={`flex items-center gap-2 py-3 text-xs font-semibold transition-all border-b-2 -mb-px whitespace-nowrap ${
                activeTab === "uncapped_track"
                  ? "border-[#101D3A] text-[#101D3A] font-bold"
                  : "border-transparent text-[#52627A] hover:text-[#101D3A]"
              }`}
            >
              <Award size={14} className="text-[#101D3A]" />
              <span>Uncapped Prospect Tracking</span>
            </button>
          </div>

          {/* TAB 1: BOUNDARY GEOMETRY */}
          {activeTab === "geometry" && (
            <div className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {/* Straight Boundary */}
                <div className="p-4 rounded-xl bg-white border border-[#E7EAF0] text-center">
                  <div className="text-[10px] font-bold uppercase tracking-wider text-[#52627A]">
                    Straight Boundary (Down the V)
                  </div>
                  <div className="text-3xl font-black text-[#101D3A] my-1">
                    {venueDetail.boundary_dimensions.straight_m ? (
                      <span>{venueDetail.boundary_dimensions.straight_m} <span className="text-sm font-normal text-[#52627A]">meters</span></span>
                    ) : (
                      <span className="text-sm font-semibold text-[#52627A]">Unavailable</span>
                    )}
                  </div>
                  <div className="text-[11px] text-[#52627A]">Stump to sight-screen distance</div>
                </div>

                {/* Off-Side Boundary */}
                <div className="p-4 rounded-xl bg-white border border-[#E7EAF0] text-center">
                  <div className="text-[10px] font-bold uppercase tracking-wider text-[#52627A]">
                    Off-Side Square Boundary
                  </div>
                  <div className="text-3xl font-black text-[#101D3A] my-1">
                    {venueDetail.boundary_dimensions.off_boundary_m ? (
                      <span>{venueDetail.boundary_dimensions.off_boundary_m} <span className="text-sm font-normal text-[#52627A]">meters</span></span>
                    ) : (
                      <span className="text-sm font-semibold text-[#52627A]">Unavailable</span>
                    )}
                  </div>
                  <div className="text-[11px] text-[#52627A]">Pitch centre to point/cover boundary</div>
                </div>

                {/* Leg-Side Boundary */}
                <div className="p-4 rounded-xl bg-white border border-[#E7EAF0] text-center">
                  <div className="text-[10px] font-bold uppercase tracking-wider text-[#52627A]">
                    Leg-Side Square Boundary
                  </div>
                  <div className="text-3xl font-black text-[#101D3A] my-1">
                    {venueDetail.boundary_dimensions.leg_boundary_m ? (
                      <span>{venueDetail.boundary_dimensions.leg_boundary_m} <span className="text-sm font-normal text-[#52627A]">meters</span></span>
                    ) : (
                      <span className="text-sm font-semibold text-[#52627A]">Unavailable</span>
                    )}
                  </div>
                  <div className="text-[11px] text-[#52627A]">Pitch centre to square leg / midwicket</div>
                </div>
              </div>

              {/* Surface Details & Drainage */}
              <div className="p-5 rounded-xl border border-[#E7EAF0] bg-[#101D3A]/03 space-y-3">
                <h4 className="text-xs font-bold uppercase tracking-wider text-[#101D3A] flex items-center gap-1.5">
                  <Layers size={14} className="text-[#D4145A]" />
                  Soil, Turf & Environmental Specification
                </h4>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs text-[#52627A]">
                  <div>
                    <span className="font-bold text-[#101D3A]">Soil Composition:</span>{" "}
                    {venueDetail.surface_details.soil_composition || "Standard Clay/Loam Turf"}
                  </div>
                  <div>
                    <span className="font-bold text-[#101D3A]">Grass Specification:</span>{" "}
                    {venueDetail.surface_details.grass_type || "Bermuda Turf"}
                  </div>
                  <div>
                    <span className="font-bold text-[#101D3A]">Outfield Speed:</span>{" "}
                    {venueDetail.surface_details.outfield_speed || "Medium-Fast Outfield"}
                  </div>
                  <div>
                    <span className="font-bold text-[#101D3A]">Evening Dew Tendency:</span>{" "}
                    {venueDetail.surface_details.dew_tendency || "Moderate coastal / atmospheric dew"}
                  </div>
                </div>
                <div className="pt-2 border-t border-[#E7EAF0] text-[11px] text-[#52627A] flex items-center justify-between">
                  <span>Dimension Source: {venueDetail.boundary_dimensions.dimension_source || "Pending BCCI survey"}</span>
                  <span className="flex items-center gap-1 text-[#D4145A] font-semibold">
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
                <div className="p-4 bg-white rounded-xl border border-[#E7EAF0] text-center">
                  <div className="text-[10px] font-bold uppercase text-[#52627A]">1st Innings Average</div>
                  <div className="text-2xl font-black text-[#101D3A] mt-1">{scoringTrends.avg_first_innings_score}</div>
                  <div className="text-[10px] text-[#52627A] mt-0.5">Par Score Target</div>
                </div>
                <div className="p-4 bg-white rounded-xl border border-[#E7EAF0] text-center">
                  <div className="text-[10px] font-bold uppercase text-[#52627A]">2nd Innings Average</div>
                  <div className="text-2xl font-black text-[#101D3A] mt-1">{scoringTrends.avg_second_innings_score}</div>
                  <div className="text-[10px] text-[#52627A] mt-0.5">Chasing Par</div>
                </div>
                <div className="p-4 bg-white rounded-xl border border-[#E7EAF0] text-center">
                  <div className="text-[10px] font-bold uppercase text-[#52627A]">Chasing Win Rate</div>
                  <div className="text-2xl font-black text-[#D4145A] mt-1">
                    {scoringTrends.match_outcome_by_innings.chase_win_pct}%
                  </div>
                  <div className="text-[10px] text-[#52627A] mt-0.5">Bat 2nd Advantage</div>
                </div>
                <div className="p-4 bg-white rounded-xl border border-[#E7EAF0] text-center">
                  <div className="text-[10px] font-bold uppercase text-[#52627A]">Avg Wickets / Match</div>
                  <div className="text-2xl font-black text-[#101D3A] mt-1">{scoringTrends.avg_wickets_per_innings}</div>
                  <div className="text-[10px] text-[#52627A] mt-0.5">Wickets fallen</div>
                </div>
              </div>

              {/* Phase Run Rates */}
              <div className="p-5 rounded-xl border border-[#E7EAF0] bg-[#101D3A]/03 space-y-3">
                <h4 className="text-xs font-bold uppercase tracking-wider text-[#101D3A]">
                  Phase-Specific Run Rates at {scoringTrends.venue_name}
                </h4>
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                  <div className="p-3 bg-white rounded-lg border border-[#E7EAF0]">
                    <div className="text-[10px] font-bold text-[#52627A] uppercase">Powerplay (Overs 0-5)</div>
                    <div className="text-xl font-black text-[#101D3A] mt-0.5">
                      {scoringTrends.phase_scoring_rates.powerplay} <span className="text-xs font-normal text-[#52627A]">rpo</span>
                    </div>
                  </div>
                  <div className="p-3 bg-white rounded-lg border border-[#E7EAF0]">
                    <div className="text-[10px] font-bold text-[#52627A] uppercase">Middle Overs (Overs 6-14)</div>
                    <div className="text-xl font-black text-[#101D3A] mt-0.5">
                      {scoringTrends.phase_scoring_rates.middle} <span className="text-xs font-normal text-[#52627A]">rpo</span>
                    </div>
                  </div>
                  <div className="p-3 bg-white rounded-lg border border-[#E7EAF0]">
                    <div className="text-[10px] font-bold text-[#52627A] uppercase">Death Overs (Overs 15-19)</div>
                    <div className="text-xl font-black text-[#101D3A] mt-0.5">
                      {scoringTrends.phase_scoring_rates.death} <span className="text-xs font-normal text-[#52627A]">rpo</span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Sample Size Transparency */}
              {scoringTrends.sample_size_warning && (
                <div className="p-3 bg-[#D4145A]/10 rounded-xl border border-[#D4145A]/30 text-xs text-[#D4145A] flex items-center gap-2">
                  <AlertTriangle size={15} className="text-[#D4145A] shrink-0" />
                  <span>{scoringTrends.sample_size_warning}</span>
                </div>
              )}
            </div>
          )}

          {/* TAB 3: PITCH & PACE-VS-SPIN EVIDENCE */}
          {activeTab === "pitch" && pitchEvidence && (
            <div className="space-y-6">
              {/* Evidence Classification Banner */}
              <div className="flex flex-wrap items-center justify-between gap-3 p-4 bg-[#D4145A]/05 rounded-xl border border-[#E7EAF0]">
                <div>
                  <div className="text-[10px] font-bold uppercase tracking-wider text-[#52627A]">
                    Empirical Conditions Classification
                  </div>
                  <div className="text-xl font-black text-[#101D3A] mt-0.5">
                    {pitchEvidence.conditions_evidence_classification}
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <span className="px-2.5 py-1 rounded text-xs font-mono font-bold bg-[#101D3A] text-white">
                    Confidence: {pitchEvidence.evidence_confidence}
                  </span>
                  <span className="text-xs font-mono text-[#52627A]">
                    {pitchEvidence.sample_matches_evaluated} matches evaluated
                  </span>
                </div>
              </div>

              {/* Pace vs Spin Distribution */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {/* Pace Dimension */}
                <div className="p-5 rounded-xl border border-[#E7EAF0] bg-[#F8E8EF]">
                  <div className="flex items-center justify-between mb-3">
                    <span className="text-xs font-bold text-[#101D3A]">Pace Bowler Impact</span>
                    <span className="text-xs font-mono font-extrabold text-[#101D3A]">
                      {pitchEvidence.observed_pace_vs_spin.pace_wickets_share_pct}% wickets
                    </span>
                  </div>
                  <div className="grid grid-cols-2 gap-2 text-center text-xs">
                    <div className="p-2 bg-white rounded border border-[#E7EAF0]">
                      <div className="text-[10px] text-[#52627A]">Economy</div>
                      <div className="font-bold text-[#101D3A]">{pitchEvidence.observed_pace_vs_spin.pace_economy}</div>
                    </div>
                    <div className="p-2 bg-white rounded border border-[#E7EAF0]">
                      <div className="text-[10px] text-[#52627A]">Average</div>
                      <div className="font-bold text-[#101D3A]">{pitchEvidence.observed_pace_vs_spin.pace_average}</div>
                    </div>
                  </div>
                </div>

                {/* Spin Dimension */}
                <div className="p-5 rounded-xl border border-[#E7EAF0] bg-[#D4145A]/05">
                  <div className="flex items-center justify-between mb-3">
                    <span className="text-xs font-bold text-[#101D3A]">Spin Bowler Impact</span>
                    <span className="text-xs font-mono font-extrabold text-[#D4145A]">
                      {pitchEvidence.observed_pace_vs_spin.spin_wickets_share_pct}% wickets
                    </span>
                  </div>
                  <div className="grid grid-cols-2 gap-2 text-center text-xs">
                    <div className="p-2 bg-white rounded border border-[#E7EAF0]">
                      <div className="text-[10px] text-[#52627A]">Economy</div>
                      <div className="font-bold text-[#101D3A]">{pitchEvidence.observed_pace_vs_spin.spin_economy}</div>
                    </div>
                    <div className="p-2 bg-white rounded border border-[#E7EAF0]">
                      <div className="text-[10px] text-[#52627A]">Average</div>
                      <div className="font-bold text-[#101D3A]">{pitchEvidence.observed_pace_vs_spin.spin_average}</div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Boundary vs Dot-Ball Distribution */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div className="p-4 bg-white rounded-xl border border-[#E7EAF0]">
                  <div className="text-[10px] font-bold uppercase text-[#52627A]">Boundary Runs Contribution</div>
                  <div className="text-xl font-black text-[#101D3A] mt-1">
                    {pitchEvidence.boundary_patterns.boundary_runs_pct}%
                  </div>
                  <div className="text-[11px] text-[#52627A] mt-0.5">
                    ~{pitchEvidence.boundary_patterns.fours_per_match} fours, ~{pitchEvidence.boundary_patterns.sixes_per_match} sixes per fixture
                  </div>
                </div>
                <div className="p-4 bg-white rounded-xl border border-[#E7EAF0]">
                  <div className="text-[10px] font-bold uppercase text-[#52627A]">Dot Ball Percentage</div>
                  <div className="text-xl font-black text-[#101D3A] mt-1">
                    {pitchEvidence.dot_ball_patterns.dot_ball_pct}%
                  </div>
                  <div className="text-[11px] text-[#52627A] mt-0.5">
                    Percentage of deliveries yielding zero runs
                  </div>
                </div>
              </div>

              {/* Observed Summary & Caveats */}
              <div className="p-4 bg-white rounded-xl border border-[#E7EAF0] text-xs text-[#52627A] space-y-2">
                <p><span className="font-bold text-[#101D3A]">Observed Evidence:</span> {pitchEvidence.observed_statistical_summary}</p>
                <p className="text-[11px] text-[#52627A] italic border-t border-[#E7EAF0] pt-2">
                  * {pitchEvidence.limitations_disclaimer}
                </p>
              </div>
            </div>
          )}

          {/* TAB 4: WEATHER & DEW TELEMETRY */}
          {activeTab === "weather" && (
            <div className="space-y-6">
              <div className="flex flex-wrap items-center justify-between gap-3 p-4 bg-white rounded-xl border border-[#E7EAF0]">
                <div className="flex items-center gap-2">
                  <Droplets className="text-[#101D3A]" size={18} />
                  <div>
                    <h4 className="text-xs font-bold text-[#101D3A]">Open-Meteo Hourly Telemetry</h4>
                    <p className="text-[11px] text-[#52627A]">Attribution: Weather data by Open-Meteo.com under CC-BY 4.0</p>
                  </div>
                </div>
                <span className="px-2.5 py-1 rounded text-xs font-mono font-bold bg-[#D4145A]/10 text-[#D4145A] border border-[#D4145A]/30">
                  HISTORICAL OBSERVATION (VERIFIED)
                </span>
              </div>

              {/* Hourly Weather Cards */}
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                {weatherObservations.map((obs, idx) => (
                  <div
                    key={idx}
                    className="p-4 rounded-xl border border-[#E7EAF0] bg-white hover:border-[#101D3A]/20 transition-all space-y-2"
                  >
                    <div className="flex items-center justify-between text-xs">
                      <span className="font-mono font-bold text-[#101D3A]">
                        {obs.observation_time.split("T")[-1] || obs.observation_time}
                      </span>
                      <span className={`px-2 py-0.5 rounded text-[10px] font-mono font-bold ${
                        obs.dew_severity_risk === "HIGH_DEW_RISK"
                          ? "bg-[#D4145A]/10 text-[#D4145A]"
                          : obs.dew_severity_risk === "MODERATE"
                          ? "bg-[#D4145A]/10 text-[#D4145A]"
                          : "bg-[#D4145A]/10 text-[#D4145A]"
                      }`}>
                        {obs.dew_severity_risk}
                      </span>
                    </div>

                    <div className="grid grid-cols-2 gap-2 text-xs py-2 border-y border-[#E7EAF0]">
                      <div>
                        <span className="text-[#52627A] text-[10px]">Temperature:</span>
                        <div className="font-black text-sm text-[#101D3A]">{obs.temperature_c}°C</div>
                      </div>
                      <div>
                        <span className="text-[#52627A] text-[10px]">Humidity:</span>
                        <div className="font-black text-sm text-[#101D3A]">{obs.relative_humidity_pct}%</div>
                      </div>
                      <div>
                        <span className="text-[#52627A] text-[10px]">Dew Point:</span>
                        <div className="font-bold text-[#101D3A]">{obs.dew_point_c}°C</div>
                      </div>
                      <div>
                        <span className="text-[#52627A] text-[10px]">Wind:</span>
                        <div className="font-bold text-[#101D3A]">{obs.wind_speed_kph} km/h {obs.wind_direction_compass}</div>
                      </div>
                    </div>

                    <div className="text-[10px] text-[#52627A] flex items-center justify-between">
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
              <div className="flex flex-wrap items-center gap-2 p-4 bg-white rounded-xl border border-[#E7EAF0]">
                <span className="text-xs font-bold text-[#52627A] uppercase mr-2">Select Uncapped Talent:</span>
                {uncappedProspects.map((p) => (
                  <button
                    key={p.id}
                    onClick={() => setSelectedPlayerId(p.id)}
                    className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
                      selectedPlayerId === p.id
                        ? "bg-[#101D3A] text-white shadow-sm"
                        : "bg-white text-[#101D3A] border border-[#E7EAF0] hover:bg-[#F8E8EF]"
                    }`}
                  >
                    {p.name}
                  </button>
                ))}
              </div>

              {/* Player Venue Record */}
              {playerPerformance && (
                <div className="p-6 rounded-2xl border border-[#E7EAF0] bg-white shadow-sm space-y-4">
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-[#E7EAF0] pb-4">
                    <div>
                      <div className="flex items-center gap-2 mb-1">
                        <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-[#101D3A]/15 text-[#101D3A]">
                          {playerPerformance.eligibility_status}
                        </span>
                        <span className="text-xs font-mono text-[#52627A]">
                          {playerPerformance.player_id}
                        </span>
                      </div>
                      <h3 className="text-xl font-bold text-[#101D3A]">
                        {playerPerformance.player_name} at {playerPerformance.venue_name}
                      </h3>
                      <p className="text-xs text-[#52627A] mt-0.5">Role Archetype: {playerPerformance.role_archetype}</p>
                    </div>

                    <div className="p-3 bg-white rounded-xl border border-[#E7EAF0] text-right">
                      <div className="text-[10px] font-bold uppercase text-[#52627A]">Matches at Venue</div>
                      <div className="text-base font-extrabold text-[#101D3A]">{playerPerformance.matches_at_venue}</div>
                    </div>
                  </div>

                  {/* Batting vs Bowling Dual Grid at this venue */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="p-4 rounded-xl border border-[#E7EAF0] bg-[#D4145A]/10/20">
                      <h4 className="text-xs font-bold text-[#101D3A] mb-2 flex items-center gap-1.5">
                        <TrendingUp size={14} className="text-[#101D3A]" /> Batting at Venue
                      </h4>
                      <div className="grid grid-cols-3 gap-2 text-center text-xs">
                        <div className="p-2 bg-white rounded border border-[#E7EAF0]">
                          <div className="text-[10px] text-[#52627A]">Runs</div>
                          <div className="font-extrabold text-sm text-[#101D3A]">{playerPerformance.batting_at_venue.runs}</div>
                        </div>
                        <div className="p-2 bg-white rounded border border-[#E7EAF0]">
                          <div className="text-[10px] text-[#52627A]">Strike Rate</div>
                          <div className="font-extrabold text-sm text-[#101D3A]">{playerPerformance.batting_at_venue.strike_rate}</div>
                        </div>
                        <div className="p-2 bg-white rounded border border-[#E7EAF0]">
                          <div className="text-[10px] text-[#52627A]">Average</div>
                          <div className="font-bold text-sm text-[#101D3A]">{playerPerformance.batting_at_venue.average ?? "N/A"}</div>
                        </div>
                      </div>
                      {playerPerformance.batting_at_venue.death_sr && (
                        <div className="text-[11px] text-[#52627A] mt-2">
                          Death Overs SR at this ground: <span className="font-bold text-[#101D3A]">{playerPerformance.batting_at_venue.death_sr}</span>
                        </div>
                      )}
                    </div>

                    <div className="p-4 rounded-xl border border-[#E7EAF0] bg-[#F8E8EF]">
                      <h4 className="text-xs font-bold text-[#101D3A] mb-2 flex items-center gap-1.5">
                        <Target size={14} className="text-[#101D3A]" /> Bowling at Venue
                      </h4>
                      <div className="grid grid-cols-3 gap-2 text-center text-xs">
                        <div className="p-2 bg-white rounded border border-[#E7EAF0]">
                          <div className="text-[10px] text-[#52627A]">Wickets</div>
                          <div className="font-extrabold text-sm text-[#101D3A]">{playerPerformance.bowling_at_venue.wickets}</div>
                        </div>
                        <div className="p-2 bg-white rounded border border-[#E7EAF0]">
                          <div className="text-[10px] text-[#52627A]">Economy</div>
                          <div className="font-extrabold text-sm text-[#101D3A]">{playerPerformance.bowling_at_venue.economy}</div>
                        </div>
                        <div className="p-2 bg-white rounded border border-[#E7EAF0]">
                          <div className="text-[10px] text-[#52627A]">Overs</div>
                          <div className="font-bold text-sm text-[#101D3A]">{playerPerformance.bowling_at_venue.overs}</div>
                        </div>
                      </div>
                    </div>
                  </div>

                  {playerPerformance.sample_size_warning && (
                    <div className="p-3 bg-[#D4145A]/10 rounded-xl border border-[#D4145A]/30 text-xs text-[#D4145A] flex items-center gap-2">
                      <AlertTriangle size={14} className="text-[#D4145A] shrink-0" />
                      <span>{playerPerformance.sample_size_warning}</span>
                    </div>
                  )}

                  <div className="text-[10px] text-[#52627A] italic">
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
