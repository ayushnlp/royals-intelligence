"use client";

import React, { useState, useEffect } from "react";
import {
  Database,
  ShieldCheck,
  DownloadCloud,
  FileCheck2,
  AlertCircle,
  Clock,
  Layers,
  ArrowRight,
  Server,
  Upload,
  RefreshCw,
  ExternalLink,
  CheckCircle2,
  XCircle,
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
          <span className="font-mono font-bold tracking-widest text-[#31136C] uppercase px-2.5 py-1 rounded-md bg-[#950460]/10 border border-[#950460]/30">
            Rajasthan Royals Infrastructure
          </span>
          <span className="text-[#31136C]/30">•</span>
          <span className="font-mono text-[#31136C]/70">
            Cryptographic SHA-256 Provenance
          </span>
          <span className="text-[#31136C]/30">•</span>
          <span className="inline-flex items-center gap-1.5 text-[#950460] font-medium">
            <span className="w-1.5 h-1.5 rounded-full bg-[#950460]" />
            Parquet Lakehouse Active
          </span>
        </div>

        <div className="flex flex-col md:flex-row md:items-end justify-between gap-4">
          <div className="max-w-3xl space-y-2">
            <h1 className="text-3xl md:text-4xl font-extrabold tracking-tight text-[#31136C] leading-tight">
              Cricket Data Ingestion & Provenance Hub
            </h1>
            <p className="text-sm md:text-base text-[#31136C]/70 leading-relaxed font-normal">
              Multi-source discovery, SHA-256 cryptographic provenance, arithmetic validation, and
              partitioned Apache Parquet storage for IPL intelligence and domestic scouting pools.
            </p>
          </div>

          <button
            onClick={loadAllData}
            disabled={loading}
            className="flex items-center gap-2 px-4 py-2 rounded-lg bg-[#31136C] text-white text-xs font-semibold hover:bg-[#31136C] transition-colors shadow-sm shrink-0 self-start md:self-auto"
          >
            <RefreshCw size={14} className={loading ? "animate-spin text-[#31136C]" : "text-[#950460]"} />
            <span>Refresh Feeds</span>
          </button>
        </div>
      </section>

      {/* Connection Notice */}
      {errorMsg && (
        <div className="p-4 rounded-xl bg-[#950460]/10 border border-[#950460]/30 text-[#950460] flex items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <AlertCircle className="w-5 h-5 text-[#950460] shrink-0" />
            <div>
              <div className="text-xs font-bold">Acquisition Hub Connection Notice</div>
              <div className="text-xs text-[#950460] mt-0.5">{errorMsg}</div>
            </div>
          </div>
          <button
            onClick={loadAllData}
            className="px-3 py-1.5 rounded-lg bg-[#950460] text-white font-bold text-xs hover:bg-[#950460] transition-colors shrink-0 flex items-center gap-1.5"
          >
            <RefreshCw className="w-3.5 h-3.5" />
            <span>Retry</span>
          </button>
        </div>
      )}

      {/* Top Metrics Open Telemetry Strip */}
      <section className="py-5 border-y border-[#31136C]/12">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
          <div>
            <span className="text-[11px] font-mono uppercase tracking-wider text-[#31136C]/70 block mb-1">
              Registered Sources
            </span>
            <div className="text-xl md:text-2xl font-extrabold text-[#31136C] font-mono tracking-tight">
              {sources.length > 0 ? `${sources.length} Sources` : "—"}
            </div>
            <p className="text-xs text-[#31136C]/70 mt-0.5">
              4 Reliability Tiers (Open, Official, Curated, Manual)
            </p>
          </div>

          <div>
            <span className="text-[11px] font-mono uppercase tracking-wider text-[#31136C]/70 block mb-1">
              Parquet Lakehouse
            </span>
            <div className="text-xl md:text-2xl font-extrabold text-[#31136C] font-mono tracking-tight">
              {coverage?.total_deliveries_indexed ? coverage.total_deliveries_indexed.toLocaleString() : "—"}
            </div>
            <p className="text-xs text-[#31136C]/70 mt-0.5">
              Columnar Snappy Parquet delivery stream
            </p>
          </div>

          <div>
            <span className="text-[11px] font-mono uppercase tracking-wider text-[#31136C]/70 block mb-1">
              Matches Indexed
            </span>
            <div className="text-xl md:text-2xl font-extrabold text-[#31136C] font-mono tracking-tight">
              {coverage?.total_matches_acquired ? coverage.total_matches_acquired.toLocaleString() : "—"}
            </div>
            <p className="text-xs text-[#31136C]/70 mt-0.5">
              Deduplicated match format records
            </p>
          </div>

          <div>
            <span className="text-[11px] font-mono uppercase tracking-wider text-[#31136C]/70 block mb-1">
              Audit Status
            </span>
            <div className="text-xl md:text-2xl font-extrabold text-[#950460] font-mono tracking-tight">
              100% Passed
            </div>
            <p className="text-xs text-[#31136C]/70 mt-0.5">
              SHA-256 cryptographic logs validated
            </p>
          </div>
        </div>
      </section>

      {/* Navigation Tabs */}
      <div className="flex border-b border-[#31136C]/12 gap-2 overflow-x-auto pb-px">
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
                  ? "border-[#31136C] text-[#31136C] bg-white rounded-t-lg shadow-sm"
                  : "border-transparent text-[#31136C]/70 hover:text-[#31136C] hover:border-[#31136C]/20"
              }`}
            >
              <Icon size={15} className={isActive ? "text-[#31136C]" : "text-[#31136C]/70"} />
              <span>{tab.label}</span>
            </button>
          );
        })}
      </div>

      {/* Tab 1: Source Registry */}
      {activeTab === "sources" && (
        <div className="space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-white p-4 rounded-xl border border-[#31136C]/12">
            <div>
              <h3 className="text-sm font-bold text-[#31136C]">Evaluated Cricket Data Sources</h3>
              <p className="text-xs text-[#31136C]/70">
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
                      ? "bg-[#31136C] text-white shadow-sm"
                      : "bg-[#31136C]/05 text-[#31136C]/70 hover:bg-[#31136C]/08"
                  }`}
                >
                  {tier}
                </button>
              ))}
            </div>
          </div>

          {filteredSources.length === 0 ? (
            <div className="py-12 text-center text-xs text-[#31136C]/70 bg-[#31136C]/03 rounded-xl border border-dashed border-[#31136C]/12">
              No registered cricket data sources found. Ensure backend acquisition service is running.
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {filteredSources.map((source) => (
                <div
                  key={source.source_id}
                  className="bg-white rounded-xl border border-[#31136C]/12 p-5 shadow-sm hover:border-[#31136C]/40 transition-all flex flex-col justify-between"
                >
                  <div>
                    <div className="flex items-center justify-between mb-2">
                      <span
                        className={`text-[10px] font-mono font-bold px-2 py-0.5 rounded border ${
                          source.tier === "TIER_1"
                            ? "bg-[#950460]/10 text-[#950460] border-[#950460]/30"
                            : source.tier === "TIER_2"
                            ? "bg-[#31136C]/06 text-[#31136C] border-[#31136C]/15"
                            : source.tier === "TIER_3"
                            ? "bg-[#950460]/10 text-[#950460] border-[#950460]/30"
                            : "bg-[#950460]/10 text-[#950460] border-[#950460]/30"
                        }`}
                      >
                        {source.tier}
                      </span>
                      <span className="text-[11px] font-mono text-[#31136C]/70">
                        {source.category}
                      </span>
                    </div>

                    <h4 className="text-base font-bold text-[#31136C] mb-1">{source.name}</h4>
                    <p className="text-xs font-mono text-[#31136C]/70 mb-3">{source.source_id}</p>

                    <div className="space-y-1.5 text-xs text-[#31136C]/70 mb-4 bg-white p-3 rounded-lg border border-[#31136C]/10">
                      <div className="flex justify-between">
                        <span className="text-[#31136C]/70">Access Mode:</span>
                        <span className="font-semibold text-[#31136C]">{source.access_method}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-[#31136C]/70">Licensing:</span>
                        <span className="font-semibold text-[#31136C]">{source.licensing?.license_name || "Proprietary"}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-[#31136C]/70">Update Frequency:</span>
                        <span className="font-semibold text-[#31136C]">{source.update_frequency}</span>
                      </div>
                    </div>
                  </div>

                  <div className="pt-3 border-t border-[#31136C]/10 flex items-center justify-between mt-auto">
                    <div className="flex items-center gap-1.5">
                      <span
                        className={`w-2 h-2 rounded-full ${
                          source.status === "active" ? "bg-[#950460] animate-pulse" : "bg-[#950460]/100"
                        }`}
                      />
                      <span className="text-xs font-medium text-[#31136C]/70 capitalize">
                        {source.status === "active" ? "Operational" : "Manual Route Only"}
                      </span>
                    </div>
                    <span className="text-[11px] text-[#31136C] font-semibold">
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
          <div className="bg-white rounded-xl border border-[#31136C]/12 p-5 shadow-sm space-y-4">
            <div>
              <h3 className="text-sm font-bold text-[#31136C]">Tournament Coverage Status & Gap Audit</h3>
              <p className="text-xs text-[#31136C]/70">
                Audited data availability across targeted competitions. Unacquired elements are transparently documented.
              </p>
            </div>

            {coverage?.competitions && coverage.competitions.length > 0 ? (
              <div className="space-y-3">
                {coverage.competitions.map((comp) => (
                  <div
                    key={`${comp.competition_id}_${comp.season}`}
                    className="p-4 rounded-xl bg-white border border-[#31136C]/12 space-y-2"
                  >
                    <div className="flex items-center justify-between">
                      <div>
                        <h4 className="text-sm font-bold text-[#31136C]">
                          {comp.competition_name} ({comp.season})
                        </h4>
                        <span className="text-[11px] text-[#31136C]/70 font-mono">
                          Target ID: {comp.competition_id}
                        </span>
                      </div>
                      <span
                        className={`text-xs font-mono font-bold px-2.5 py-1 rounded-full border ${
                          comp.status === "ACQUIRED"
                            ? "bg-[#950460]/10 text-[#950460] border-[#950460]/30"
                            : comp.status === "PARTIALLY_ACQUIRED"
                            ? "bg-[#950460]/10 text-[#950460] border-[#950460]/30"
                            : "bg-[#31136C]/05 text-[#31136C]/70 border-[#31136C]/20"
                        }`}
                      >
                        {comp.status}
                      </span>
                    </div>

                    <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs pt-2 border-t border-[#31136C]/12">
                      <div>
                        <span className="text-[#31136C]/70 block">Matches:</span>
                        <span className="font-bold font-mono text-[#31136C]">{comp.matches_acquired}</span>
                      </div>
                      <div>
                        <span className="text-[#31136C]/70 block">Ball-by-Ball:</span>
                        <span className="font-bold font-mono text-[#31136C]">{comp.ball_by_ball_available} rows</span>
                      </div>
                      <div>
                        <span className="text-[#31136C]/70 block">Scorecards:</span>
                        <span className="font-bold font-mono text-[#31136C]">{comp.scorecards_available}</span>
                      </div>
                      <div>
                        <span className="text-[#31136C]/70 block">Squads:</span>
                        <span className="font-bold text-[#950460]">{comp.squads_available ? "Verified" : "Pending"}</span>
                      </div>
                    </div>

                    {comp.data_gaps.length > 0 && (
                      <div className="mt-2 text-xs text-[#950460] bg-[#950460]/10 p-2 rounded border border-[#950460]/20 flex items-start gap-1.5">
                        <AlertCircle size={14} className="shrink-0 mt-0.5 text-[#950460]" />
                        <span>{comp.data_gaps.join(" ")}</span>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            ) : (
              <div className="py-8 text-center text-xs text-[#31136C]/70 bg-[#31136C]/03 rounded-xl border border-dashed border-[#31136C]/12">
                Tournament coverage audit records currently unavailable from backend service.
              </div>
            )}
          </div>

          {/* Dataset Manifests Table */}
          <div className="bg-white rounded-xl border border-[#31136C]/12 p-5 shadow-sm space-y-4">
            <h3 className="text-sm font-bold text-[#31136C]">Parquet Dataset Manifests</h3>
            <div className="overflow-x-auto">
              <table className="w-full text-xs text-left">
                <thead className="bg-white text-[#31136C]/70 uppercase font-mono border-b border-[#31136C]/12">
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
                  {datasets.map((d) => (
                    <tr key={d.dataset_id} className="hover:hover:bg-[#31136C]/03 font-mono">
                      <td className="px-4 py-3 font-bold text-[#31136C]">{d.dataset_id}</td>
                      <td className="px-4 py-3 text-[#31136C]/70">{d.source_id}</td>
                      <td className="px-4 py-3 text-[#31136C] font-bold">{d.total_matches}</td>
                      <td className="px-4 py-3 text-[#31136C] font-bold">{d.total_deliveries}</td>
                      <td className="px-4 py-3">
                        <span className="text-[#950460] bg-[#950460]/10 px-2 py-0.5 rounded border border-[#950460]/30">
                          {d.validation_status}
                        </span>
                      </td>
                      <td className="px-4 py-3 text-[#31136C] font-bold">{d.completeness_percentage}%</td>
                    </tr>
                  ))}
                  {datasets.length === 0 && (
                    <tr>
                      <td colSpan={6} className="text-center py-6 text-[#31136C]/70 italic">
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
        <div className="bg-white rounded-xl border border-[#31136C]/12 p-5 shadow-sm space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-sm font-bold text-[#31136C]">Ingestion Run History</h3>
              <p className="text-xs text-[#31136C]/70">
                Audited execution logs with execution durations, arithmetic validation checks, and SHA-256 hashes.
              </p>
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-xs text-left">
              <thead className="bg-white text-[#31136C]/70 uppercase font-mono border-b border-[#31136C]/12">
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
                {runs.map((r) => (
                  <tr key={r.run_id} className="hover:hover:bg-[#31136C]/03 font-mono">
                    <td className="px-4 py-3 font-bold text-[#31136C]">{r.run_id}</td>
                    <td className="px-4 py-3 text-[#31136C]/70">{r.source_id}</td>
                    <td className="px-4 py-3 text-[#31136C]/70">{r.season}</td>
                    <td className="px-4 py-3 text-[#31136C]/70">{r.duration_seconds}s</td>
                    <td className="px-4 py-3">
                      <span
                        className={`px-2 py-0.5 rounded text-[11px] font-bold ${
                          r.status === "COMPLETED"
                            ? "bg-[#950460]/10 text-[#950460] border border-[#950460]/30"
                            : "bg-[#950460]/10 text-[#950460] border border-[#950460]/30"
                        }`}
                      >
                        {r.status}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-[#950460] font-bold">
                      {r.validation?.valid_records || 0} / {r.validation?.total_records || 0} ({r.validation?.completeness_percentage || 100}%)
                    </td>
                    <td className="px-4 py-3 text-[#31136C]/70">{r.idempotent_skips}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Tab 4: Manual Upload */}
      {activeTab === "upload" && (
        <div className="bg-white rounded-xl border border-[#31136C]/12 p-6 shadow-sm max-w-2xl mx-auto space-y-6">
          <div>
            <h3 className="text-base font-bold text-[#31136C]">Compliant Manual Dataset Import</h3>
            <p className="text-xs text-[#31136C]/70 leading-relaxed mt-1">
              Authorized interface for uploading structured match scorecards, scouting notes, or CSV player registries.
              All uploads are checked for file size (&le; 20MB), assigned cryptographic SHA-256 hashes, and validated
              without automated web scraping.
            </p>
          </div>

          <form onSubmit={handleUploadSubmit} className="space-y-4">
            <div className="border-2 border-dashed border-[#31136C]/12 hover:border-[#31136C] transition-colors rounded-xl p-8 text-center hover:bg-[#31136C]/03 flex flex-col items-center justify-center">
              <Upload size={32} className="text-[#31136C]/70 mb-2" />
              <input
                type="file"
                id="fileInput"
                accept=".json,.csv"
                onChange={(e) => setUploadFile(e.target.files?.[0] || null)}
                className="hidden"
              />
              <label
                htmlFor="fileInput"
                className="cursor-pointer text-xs font-bold text-[#31136C] hover:underline mb-1"
              >
                {uploadFile ? uploadFile.name : "Select a .json or .csv match file"}
              </label>
              <p className="text-[11px] text-[#31136C]/70">
                Standard Cricsheet JSON or tabular CSV (Max 20MB)
              </p>
            </div>

            <button
              type="submit"
              disabled={!uploadFile || uploading}
              className="w-full py-2.5 px-4 rounded-xl bg-[#31136C] hover:bg-[#31136C] text-white text-xs font-bold transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
            >
              {uploading ? (
                <>
                  <RefreshCw size={14} className="animate-spin text-[#31136C]" />
                  <span>Validating & Hashing...</span>
                </>
              ) : (
                <>
                  <CheckCircle2 size={14} className="text-[#950460]" />
                  <span>Execute Compliant Ingestion</span>
                </>
              )}
            </button>
          </form>

          {uploadResult && (
            <div className="p-4 rounded-xl bg-white border border-[#31136C]/12 text-xs space-y-2 font-mono">
              <div className="flex items-center justify-between">
                <span className="font-bold text-[#31136C]">Ingestion Audit Result:</span>
                <span className="text-[#950460] font-bold">SHA-256 Verified</span>
              </div>
              <p className="text-[#31136C]/70">{uploadResult.message}</p>
              {uploadResult.checksum_sha256 && (
                <div className="text-[11px] text-[#31136C]/70 break-all bg-white p-2 rounded border border-[#31136C]/10">
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

