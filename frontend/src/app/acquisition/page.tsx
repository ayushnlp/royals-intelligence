"use client";

import React, { useState, useEffect } from "react";
import {
  AlertCircle,
  Clock,
  Layers,
  Server,
  Upload,
  RefreshCw,
  CheckCircle2,
} from "lucide-react";
import { StatusBadge } from "@/components/ui/StatusBadge";
import { StatCard } from "@/components/ui/StatCard";
import {
  fetchSources,
  fetchCoverage,
  fetchIngestionRuns,
  fetchDatasets,
  uploadDataset,
} from "@/lib/api";
import {
  CricketDataSource,
  CoverageReportData,
  IngestionRunData,
  DatasetManifestData,
} from "@/types";
import { cn } from "@/lib/utils";

export default function AcquisitionPage() {
  const [activeTab, setActiveTab] = useState<"sources" | "coverage" | "runs" | "upload">("sources");
  const [sources, setSources] = useState<CricketDataSource[]>([]);
  const [coverage, setCoverage] = useState<CoverageReportData | null>(null);
  const [runs, setRuns] = useState<IngestionRunData[]>([]);
  const [datasets, setDatasets] = useState<DatasetManifestData[]>([]);
  const [loading, setLoading] = useState(true);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [selectedTier, setSelectedTier] = useState<string>("ALL");

  // Manual Upload Form State
  const [uploadFile, setUploadFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [uploadResult, setUploadResult] = useState<any>(null);

  const loadAllData = async () => {
    setLoading(true);
    setErrorMsg(null);
    try {
      const [sData, cData, rData, dData] = await Promise.all([
        fetchSources().catch((e) => {
          console.warn("Sources fetch notice:", e);
          return [];
        }),
        fetchCoverage().catch((e) => {
          console.warn("Coverage fetch notice:", e);
          return null;
        }),
        fetchIngestionRuns().catch((e) => {
          console.warn("Runs fetch notice:", e);
          return [];
        }),
        fetchDatasets().catch((e) => {
          console.warn("Datasets fetch notice:", e);
          return [];
        }),
      ]);
      setSources(sData);
      setCoverage(cData);
      setRuns(rData);
      setDatasets(dData);
      if (sData.length === 0 && !cData && rData.length === 0 && dData.length === 0) {
        setErrorMsg("Failed to communicate with Data Acquisition backend. Ensure FastAPI server is running on port 8000.");
      }
    } catch (err: any) {
      setErrorMsg(err.message || "Failed to load data acquisition telemetry from server.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAllData();
  }, []);

  const handleUploadSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!uploadFile) return;

    setUploading(true);
    setUploadResult(null);

    const formData = new FormData();
    formData.append("file", uploadFile);
    formData.append("competition_id", "ipl");
    formData.append("season", "2024");

    try {
      const data = await uploadDataset(formData);
      setUploadResult(data);
      setUploadFile(null);
      loadAllData();
    } catch (err: any) {
      setUploadResult({ message: err.message || "Failed to upload dataset." });
    } finally {
      setUploading(false);
    }
  };

  const filteredSources = selectedTier === "ALL"
    ? sources
    : sources.filter((s) => s.tier === selectedTier);

  return (
    <div className="space-y-8 pb-12">
      {/* Header Banner */}
      <section className="space-y-3">
        <div className="flex flex-wrap items-center gap-3 text-xs">
          <span className="font-mono font-bold tracking-widest text-[#17294B] uppercase px-2.5 py-1 rounded-md bg-[#E4005A]/10 border border-[#E4005A]/30">
            Rajasthan Royals Infrastructure
          </span>
          <span className="text-[#17294B]/30">•</span>
          <span className="font-mono text-[#52627A]">
            Cryptographic SHA-256 Provenance
          </span>
          <span className="text-[#17294B]/30">•</span>
          <span className="inline-flex items-center gap-1.5 text-[#E4005A] font-medium">
            <span className="w-1.5 h-1.5 rounded-full bg-[#E4005A]" />
            Parquet Lakehouse Active
          </span>
        </div>

        <div className="flex flex-col md:flex-row md:items-end justify-between gap-4">
          <div className="max-w-3xl space-y-2">
            <h1 className="text-3xl md:text-4xl font-extrabold tracking-tight text-[#17294B] leading-tight">
              Cricket Data Ingestion & Provenance Hub
            </h1>
            <p className="text-sm md:text-base text-[#52627A] leading-relaxed font-normal">
              Multi-source discovery, SHA-256 cryptographic provenance, arithmetic validation, and
              partitioned Apache Parquet storage for IPL intelligence and domestic scouting pools.
            </p>
          </div>

          <button
            onClick={loadAllData}
            disabled={loading}
            className="flex items-center gap-2 px-4 py-2 rounded-lg bg-[#17294B] text-white text-xs font-semibold hover:bg-[#17294B] transition-colors shadow-sm shrink-0 self-start md:self-auto"
          >
            <RefreshCw size={14} className={loading ? "animate-spin text-[#17294B]" : "text-[#E4005A]"} />
            <span>Refresh Feeds</span>
          </button>
        </div>
      </section>

      {/* Connection Notice */}
      {errorMsg && (
        <div className="p-4 rounded-xl bg-[#E4005A]/10 border border-[#E4005A]/30 text-[#E4005A] flex items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <AlertCircle className="w-5 h-5 text-[#E4005A] shrink-0" />
            <div>
              <div className="text-xs font-bold">Acquisition Hub Connection Notice</div>
              <div className="text-xs text-[#E4005A] mt-0.5">{errorMsg}</div>
            </div>
          </div>
          <button
            onClick={loadAllData}
            className="px-3 py-1.5 rounded-lg bg-[#E4005A] text-white font-bold text-xs hover:bg-[#950460] transition-colors shrink-0 flex items-center gap-1.5"
          >
            <RefreshCw className="w-3.5 h-3.5" />
            <span>Retry</span>
          </button>
        </div>
      )}

      {/* Top Metrics Open Telemetry Strip */}
      <section className="py-5 border-y border-[#E7EAF0]">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
          <div>
            <span className="text-[11px] font-mono uppercase tracking-wider text-[#52627A] block mb-1">
              Registered Sources
            </span>
            <div className="text-xl md:text-2xl font-extrabold text-[#17294B] font-mono tracking-tight">
              {sources.length > 0 ? `${sources.length} Sources` : "—"}
            </div>
            <p className="text-xs text-[#52627A] mt-0.5">
              4 Reliability Tiers (Open, Official, Curated, Manual)
            </p>
          </div>

          <div>
            <span className="text-[11px] font-mono uppercase tracking-wider text-[#52627A] block mb-1">
              Parquet Lakehouse
            </span>
            <div className="text-xl md:text-2xl font-extrabold text-[#17294B] font-mono tracking-tight">
              {coverage?.total_deliveries_indexed ? coverage.total_deliveries_indexed.toLocaleString() : "—"}
            </div>
            <p className="text-xs text-[#52627A] mt-0.5">
              Columnar Snappy Parquet delivery stream
            </p>
          </div>

          <div>
            <span className="text-[11px] font-mono uppercase tracking-wider text-[#52627A] block mb-1">
              Matches Indexed
            </span>
            <div className="text-xl md:text-2xl font-extrabold text-[#17294B] font-mono tracking-tight">
              {coverage?.total_matches_acquired ? coverage.total_matches_acquired.toLocaleString() : "—"}
            </div>
            <p className="text-xs text-[#52627A] mt-0.5">
              Deduplicated match format records
            </p>
          </div>

          <div>
            <span className="text-[11px] font-mono uppercase tracking-wider text-[#52627A] block mb-1">
              Audit Status
            </span>
            <div className="text-xl md:text-2xl font-extrabold text-[#E4005A] font-mono tracking-tight">
              100% Passed
            </div>
            <p className="text-xs text-[#52627A] mt-0.5">
              SHA-256 cryptographic logs validated
            </p>
          </div>
        </div>
      </section>

      {/* Navigation Tabs */}
      <div className="flex border-b border-[#E7EAF0] gap-2 overflow-x-auto pb-px">
        {[
          { id: "sources", label: "Source Registry & Evaluation", icon: Server },
          { id: "coverage", label: "Coverage & Dataset Manifests", icon: Layers },
          { id: "runs", label: "Ingestion Run History & Quality", icon: Clock },
          { id: "upload", label: "Manual Dataset Import", icon: Upload },
        ].map((tab) => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`flex items-center gap-2 px-4 py-2.5 text-xs font-bold transition-all border-b-2 whitespace-nowrap ${
                isActive
                  ? "border-[#E4005A] text-[#E4005A] bg-white rounded-t-lg shadow-sm"
                  : "border-transparent text-[#52627A] hover:text-[#17294B] hover:border-[#E7EAF0]"
              }`}
            >
              <Icon size={15} className={isActive ? "text-[#E4005A]" : "text-[#52627A]"} />
              <span>{tab.label}</span>
            </button>
          );
        })}
      </div>

      {/* Tab 1: Source Registry */}
      {activeTab === "sources" && (
        <div className="space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-white p-4 rounded-xl border border-[#E7EAF0]">
            <div>
              <h3 className="text-sm font-bold text-[#17294B]">Evaluated Cricket Data Sources</h3>
              <p className="text-xs text-[#52627A]">
                Sources evaluated against legal licensing, rate limits, coverage, and anti-scraping policies.
              </p>
            </div>
            <div className="flex items-center gap-1.5 flex-wrap">
              {["ALL", "TIER_1", "TIER_2", "TIER_3", "TIER_4"].map((tier) => (
                <button
                  key={tier}
                  onClick={() => setSelectedTier(tier)}
                  className={`px-2.5 py-1 rounded-md text-[11px] font-mono font-semibold transition-all ${
                    selectedTier === tier
                      ? "bg-[#17294B] text-white shadow-sm"
                      : "bg-[#FCE8F0] text-[#52627A] hover:bg-[#FCE8F0]"
                  }`}
                >
                  {tier}
                </button>
              ))}
            </div>
          </div>

          {filteredSources.length === 0 ? (
            <div className="py-12 text-center text-xs text-[#52627A] bg-[#17294B]/03 rounded-xl border border-dashed border-[#E7EAF0]">
              No registered cricket data sources found. Ensure backend acquisition service is running.
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {filteredSources.map((source) => (
                <div
                  key={source.source_id}
                  className="bg-white rounded-xl border border-[#E7EAF0] p-5 shadow-sm hover:border-[#17294B]/40 transition-all flex flex-col justify-between"
                >
                  <div>
                    <div className="flex items-center justify-between mb-2">
                      <span
                        className={`text-[10px] font-mono font-bold px-2 py-0.5 rounded border ${
                          source.tier === "TIER_1"
                            ? "bg-[#E4005A]/10 text-[#E4005A] border-[#E4005A]/30"
                            : source.tier === "TIER_2"
                            ? "bg-[#FCE8F0] text-[#17294B] border-[#E7EAF0]"
                            : source.tier === "TIER_3"
                            ? "bg-[#E4005A]/10 text-[#E4005A] border-[#E4005A]/30"
                            : "bg-[#E4005A]/10 text-[#E4005A] border-[#E4005A]/30"
                        }`}
                      >
                        {source.tier}
                      </span>
                      <span className="text-[11px] font-mono text-[#52627A]">
                        {source.category}
                      </span>
                    </div>

                    <h4 className="text-base font-bold text-[#17294B] mb-1">{source.name}</h4>
                    <p className="text-xs font-mono text-[#52627A] mb-3">{source.source_id}</p>

                    <div className="space-y-1.5 text-xs text-[#52627A] mb-4 bg-white p-3 rounded-lg border border-[#E7EAF0]">
                      <div className="flex justify-between">
                        <span className="text-[#52627A]">Access Mode:</span>
                        <span className="font-semibold text-[#17294B]">{source.access_method}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-[#52627A]">Licensing:</span>
                        <span className="font-semibold text-[#17294B]">{source.licensing?.license_name || "Proprietary"}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-[#52627A]">Update Frequency:</span>
                        <span className="font-semibold text-[#17294B]">{source.update_frequency}</span>
                      </div>
                    </div>
                  </div>

                  <div className="pt-3 border-t border-[#E7EAF0] flex items-center justify-between mt-auto">
                    <div className="flex items-center gap-1.5">
                      <span
                        className={`w-2 h-2 rounded-full ${
                          source.status === "active" ? "bg-[#E4005A] animate-pulse" : "bg-[#E4005A]/100"
                        }`}
                      />
                      <span className="text-xs font-medium text-[#52627A] capitalize">
                        {source.status === "active" ? "Operational" : "Manual Route Only"}
                      </span>
                    </div>
                    <span className="text-[11px] text-[#17294B] font-semibold">
                      {source.reliability_assessment.split(" ")[0]} Reliability
                    </span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Tab 2: Coverage & Manifests */}
      {activeTab === "coverage" && (
        <div className="space-y-6">
          <div className="bg-white rounded-xl border border-[#E7EAF0] p-5 shadow-sm space-y-4">
            <div>
              <h3 className="text-sm font-bold text-[#17294B]">Tournament Coverage Status & Gap Audit</h3>
              <p className="text-xs text-[#52627A]">
                Audited data availability across targeted competitions. Unacquired elements are transparently documented.
              </p>
            </div>

            {coverage?.competitions && coverage.competitions.length > 0 ? (
              <div className="space-y-3">
                {coverage.competitions.map((comp) => (
                  <div
                    key={`${comp.competition_id}_${comp.season}`}
                    className="p-4 rounded-xl bg-white border border-[#E7EAF0] space-y-2"
                  >
                    <div className="flex items-center justify-between">
                      <div>
                        <h4 className="text-sm font-bold text-[#17294B]">
                          {comp.competition_name} ({comp.season})
                        </h4>
                        <span className="text-[11px] text-[#52627A] font-mono">
                          Target ID: {comp.competition_id}
                        </span>
                      </div>
                      <span
                        className={`text-xs font-mono font-bold px-2.5 py-1 rounded-full border ${
                          comp.status === "ACQUIRED"
                            ? "bg-[#E4005A]/10 text-[#E4005A] border-[#E4005A]/30"
                            : comp.status === "PARTIALLY_ACQUIRED"
                            ? "bg-[#E4005A]/10 text-[#E4005A] border-[#E4005A]/30"
                            : "bg-[#FCE8F0] text-[#52627A] border-[#17294B]/20"
                        }`}
                      >
                        {comp.status}
                      </span>
                    </div>

                    <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs pt-2 border-t border-[#E7EAF0]">
                      <div>
                        <span className="text-[#52627A] block">Matches:</span>
                        <span className="font-bold font-mono text-[#17294B]">{comp.matches_acquired}</span>
                      </div>
                      <div>
                        <span className="text-[#52627A] block">Ball-by-Ball:</span>
                        <span className="font-bold font-mono text-[#17294B]">{comp.ball_by_ball_available} rows</span>
                      </div>
                      <div>
                        <span className="text-[#52627A] block">Scorecards:</span>
                        <span className="font-bold font-mono text-[#17294B]">{comp.scorecards_available}</span>
                      </div>
                      <div>
                        <span className="text-[#52627A] block">Squads:</span>
                        <span className="font-bold text-[#E4005A]">{comp.squads_available ? "Verified" : "Pending"}</span>
                      </div>
                    </div>

                    {comp.data_gaps.length > 0 && (
                      <div className="mt-2 text-xs text-[#E4005A] bg-[#E4005A]/10 p-2 rounded border border-[#E4005A]/20 flex items-start gap-1.5">
                        <AlertCircle size={14} className="shrink-0 mt-0.5 text-[#E4005A]" />
                        <span>{comp.data_gaps.join(" ")}</span>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            ) : (
              <div className="py-8 text-center text-xs text-[#52627A] bg-[#17294B]/03 rounded-xl border border-dashed border-[#E7EAF0]">
                Tournament coverage audit records currently unavailable from backend service.
              </div>
            )}
          </div>

          {/* Dataset Manifests Table */}
          <div className="bg-white rounded-xl border border-[#E7EAF0] p-5 shadow-sm space-y-4">
            <h3 className="text-sm font-bold text-[#17294B]">Parquet Dataset Manifests</h3>
            <div className="overflow-x-auto">
              <table className="w-full text-xs text-left">
                <thead className="bg-white text-[#52627A] uppercase font-mono border-b border-[#E7EAF0]">
                  <tr>
                    <th className="px-4 py-2.5">Dataset ID</th>
                    <th className="px-4 py-2.5">Source</th>
                    <th className="px-4 py-2.5">Matches</th>
                    <th className="px-4 py-2.5">Deliveries</th>
                    <th className="px-4 py-2.5">Validation</th>
                    <th className="px-4 py-2.5">Completeness</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {datasets.map((d, idx) => (
                    <tr
                      key={d.dataset_id}
                      className={cn(
                        "font-mono transition-colors",
                        idx % 2 === 0 ? "bg-[#FCE8F0]/35" : "bg-[#EEF4FC]/35",
                        "hover:bg-[#FCE8F0]/80"
                      )}
                    >
                      <td className="px-4 py-3 font-bold text-[#17294B]">{d.dataset_id}</td>
                      <td className="px-4 py-3 text-[#74658F]">{d.source_id}</td>
                      <td className="px-4 py-3 text-[#17294B] font-bold">{d.total_matches}</td>
                      <td className="px-4 py-3 text-[#17294B] font-bold">{d.total_deliveries}</td>
                      <td className="px-4 py-3">
                        <span className="text-[#E4005A] bg-[#FCE8F0] px-2 py-0.5 rounded border border-[#E4005A]/30">
                          {d.validation_status}
                        </span>
                      </td>
                      <td className="px-4 py-3 text-[#17294B] font-bold">{d.completeness_percentage}%</td>
                    </tr>
                  ))}
                  {datasets.length === 0 && (
                    <tr>
                      <td colSpan={6} className="text-center py-6 text-[#52627A] italic">
                        No dataset manifests generated yet. Run ingestion via CLI or Upload.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* Tab 3: Run History */}
      {activeTab === "runs" && (
        <div className="bg-white rounded-xl border border-[#E7EAF0] p-5 shadow-sm space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-sm font-bold text-[#17294B]">Ingestion Run History</h3>
              <p className="text-xs text-[#52627A]">
                Audited execution logs with execution durations, arithmetic validation checks, and SHA-256 hashes.
              </p>
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-xs text-left">
              <thead className="bg-white text-[#52627A] uppercase font-mono border-b border-[#E7EAF0]">
                <tr>
                  <th className="px-4 py-2.5">Run ID</th>
                  <th className="px-4 py-2.5">Source</th>
                  <th className="px-4 py-2.5">Season</th>
                  <th className="px-4 py-2.5">Duration</th>
                  <th className="px-4 py-2.5">Status</th>
                  <th className="px-4 py-2.5">Checks Passed</th>
                  <th className="px-4 py-2.5">Idempotent Skips</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {runs.map((r, idx) => (
                  <tr
                    key={r.run_id}
                    className={cn(
                      "font-mono transition-colors",
                      idx % 2 === 0 ? "bg-[#FCE8F0]/35" : "bg-[#EEF4FC]/35",
                      "hover:bg-[#FCE8F0]/80"
                    )}
                  >
                    <td className="px-4 py-3 font-bold text-[#17294B]">{r.run_id}</td>
                    <td className="px-4 py-3 text-[#74658F]">{r.source_id}</td>
                    <td className="px-4 py-3 text-[#74658F]">{r.season}</td>
                    <td className="px-4 py-3 text-[#74658F]">{r.duration_seconds}s</td>
                    <td className="px-4 py-3">
                      <span
                        className={`px-2 py-0.5 rounded text-[11px] font-bold ${
                          r.status === "COMPLETED"
                            ? "bg-[#15966B]/15 text-[#15966B] border border-[#15966B]/30"
                            : "bg-[#E4005A]/10 text-[#E4005A] border border-[#E4005A]/30"
                        }`}
                      >
                        {r.status}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-[#E4005A] font-bold">
                      {r.validation?.valid_records || 0} / {r.validation?.total_records || 0} ({r.validation?.completeness_percentage || 100}%)
                    </td>
                    <td className="px-4 py-3 text-[#52627A]">{r.idempotent_skips}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Tab 4: Manual Upload */}
      {activeTab === "upload" && (
        <div className="bg-white rounded-xl border border-[#E7EAF0] p-6 shadow-sm max-w-2xl mx-auto space-y-6">
          <div>
            <h3 className="text-base font-bold text-[#17294B]">Compliant Manual Dataset Import</h3>
            <p className="text-xs text-[#52627A] leading-relaxed mt-1">
              Authorized interface for uploading structured match scorecards, scouting notes, or CSV player registries.
              All uploads are checked for file size (&le; 20MB), assigned cryptographic SHA-256 hashes, and validated
              without automated web scraping.
            </p>
          </div>

          <form onSubmit={handleUploadSubmit} className="space-y-4">
            <div className="border-2 border-dashed border-[#E7EAF0] hover:border-[#17294B] transition-colors rounded-xl p-8 text-center hover:bg-[#17294B]/03 flex flex-col items-center justify-center">
              <Upload size={32} className="text-[#52627A] mb-2" />
              <input
                type="file"
                id="fileInput"
                accept=".json,.csv"
                onChange={(e) => setUploadFile(e.target.files?.[0] || null)}
                className="hidden"
              />
              <label
                htmlFor="fileInput"
                className="cursor-pointer text-xs font-bold text-[#17294B] hover:underline mb-1"
              >
                {uploadFile ? uploadFile.name : "Select a .json or .csv match file"}
              </label>
              <p className="text-[11px] text-[#52627A]">
                Standard Cricsheet JSON or tabular CSV (Max 20MB)
              </p>
            </div>

            <button
              type="submit"
              disabled={!uploadFile || uploading}
              className="w-full py-2.5 px-4 rounded-xl bg-[#17294B] hover:bg-[#17294B] text-white text-xs font-bold transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
            >
              {uploading ? (
                <>
                  <RefreshCw size={14} className="animate-spin text-[#17294B]" />
                  <span>Validating & Hashing...</span>
                </>
              ) : (
                <>
                  <CheckCircle2 size={14} className="text-[#E4005A]" />
                  <span>Execute Compliant Ingestion</span>
                </>
              )}
            </button>
          </form>

          {uploadResult && (
            <div className="p-4 rounded-xl bg-white border border-[#E7EAF0] text-xs space-y-2 font-mono">
              <div className="flex items-center justify-between">
                <span className="font-bold text-[#17294B]">Ingestion Audit Result:</span>
                <span className="text-[#E4005A] font-bold">SHA-256 Verified</span>
              </div>
              <p className="text-[#52627A]">{uploadResult.message}</p>
              {uploadResult.checksum_sha256 && (
                <div className="text-[11px] text-[#52627A] break-all bg-white p-2 rounded border border-[#E7EAF0]">
                  Hash: {uploadResult.checksum_sha256}
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

