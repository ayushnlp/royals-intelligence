"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import {
  Shield,
  Sparkles,
  Crosshair,
  Swords,
  MapPin,
  ArrowRight,
  X,
  ChevronRight,
} from "lucide-react";

export default function HomePage() {
  const [methodologyOpen, setMethodologyOpen] = useState(false);

  // Close modal on Escape key
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") setMethodologyOpen(false);
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, []);

  const featureCards = [
    {
      title: "PRESSURE INTELLIGENCE",
      href: "/pressure",
    },
    {
      title: "UNCAPPED SCOUTING",
      href: "/uncapped",
    },
    {
      title: "TACTICAL INTELLIGENCE",
      href: "/tactical",
    },
    {
      title: "DOMESTIC & MATCHES",
      href: "/domestic",
    },
    {
      title: "VENUE & PITCH INTELLIGENCE",
      href: "/venues",
    },
  ];

  return (
    <div className="min-h-screen lg:h-screen lg:max-h-screen flex flex-col bg-white text-[#17294B] overflow-x-hidden selection:bg-[#E4005A]/20 selection:text-[#17294B]">
      {/* =================================================================== */}
      {/* 1. HEADER — AUTHENTIC RAJASTHAN ROYALS BRANDING */}
      {/* =================================================================== */}
      <header className="h-14 sm:h-16 shrink-0 bg-white border-b border-[#E7EAF0] px-4 sm:px-6 lg:px-8 flex items-center justify-between z-30">
        {/* Left: Pure Brand Text */}
        <Link
          href="/"
          className="font-heading font-extrabold text-base sm:text-lg tracking-tight text-[#17294B] hover:text-[#E4005A] transition-colors"
        >
          ROYALS INTELLIGENCE
        </Link>

        {/* Right: Prominent Header Explore Button */}
        <Link
          href="/overview"
          className="group inline-flex items-center gap-2 px-4 py-2 sm:px-5 sm:py-2.5 rounded-xl bg-[#17294B] hover:bg-[#950460] text-white text-xs sm:text-[13px] font-bold tracking-wider transition-all duration-200 shadow-md hover:shadow-lg hover:scale-[1.02] active:scale-[0.98]"
        >
          <span>EXPLORE INTELLIGENCE</span>
          <ArrowRight size={14} className="text-[#E4005A] group-hover:text-white transition-colors group-hover:translate-x-0.5" />
        </Link>
      </header>

      {/* =================================================================== */}
      {/* 2. MAIN VIEWPORT CONTENT CONTAINER */}
      {/* =================================================================== */}
      <main className="flex-1 flex flex-col justify-between px-4 sm:px-6 lg:px-8 py-2 sm:py-3 lg:py-4 max-w-7xl mx-auto w-full">
        {/* HERO SECTION — Upper-middle anchor with official RR Jersey treatment */}
        <section className="flex flex-col items-center text-center my-auto pt-2 sm:pt-4 pb-2">
          {/* Eyebrow: ROYALS INTELLIGENCE */}
          <div className="mb-1">
            <span className="font-heading font-extrabold text-[11px] sm:text-xs tracking-[0.25em] text-[#17294B] uppercase">
              ROYALS INTELLIGENCE
            </span>
          </div>

          {/* Badge: SEASON 02 */}
          <div className="mb-1.5">
            <span className="inline-flex items-center gap-1.5 px-3 py-0.5 rounded-full text-[10px] sm:text-[11px] font-mono font-bold tracking-wider bg-[#FCE8F0] text-[#E4005A] border border-[#E4005A]/30 shadow-2xs">
              <span className="w-1.5 h-1.5 rounded-full bg-[#E4005A]" />
              SEASON 02
            </span>
          </div>

          {/* Sublabel: RAJASTHAN ROYALS · DATA-DRIVEN CRICKET */}
          <div className="mb-2">
            <p className="text-[11px] sm:text-xs font-semibold tracking-[0.18em] text-[#74658F] uppercase">
              RAJASTHAN ROYALS · DATA-DRIVEN CRICKET
            </p>
          </div>

          {/* Headline: INTELLIGENCE FOR RAJASTHAN ROYALS. */}
          <h1 className="font-heading font-extrabold text-[clamp(1.5rem,2.6vw,2.4rem)] text-[#17294B] tracking-tight leading-[1.12] max-w-4xl mx-auto mb-1.5">
            INTELLIGENCE FOR RAJASTHAN ROYALS.
          </h1>

          {/* Subtitle: Built to Find the Difference. */}
          <h3 className="font-heading font-bold text-[clamp(0.95rem,1.35vw,1.25rem)] text-[#E4005A] tracking-tight mb-4">
            Built to Find the Difference.
          </h3>

          {/* Hero CTAs */}
          <div className="flex flex-row items-center justify-center gap-3.5">
            <Link
              href="/overview"
              className="group inline-flex items-center justify-center gap-2.5 px-7 py-3 sm:px-8 sm:py-3.5 rounded-xl bg-gradient-to-r from-[#17294B] to-[#E4005A] hover:from-[#17294B] hover:to-[#950460] text-white text-xs sm:text-sm font-bold tracking-wider uppercase transition-all duration-200 shadow-lg hover:shadow-xl hover:scale-[1.02] active:scale-[0.98]"
            >
              <span>EXPLORE INTELLIGENCE</span>
              <ArrowRight size={16} className="text-white transition-transform group-hover:translate-x-0.5" />
            </Link>

            <button
              onClick={() => setMethodologyOpen(true)}
              className="inline-flex items-center justify-center gap-1.5 px-5 py-3 sm:px-6 sm:py-3.5 rounded-xl bg-white text-[#17294B] text-xs font-semibold tracking-wider uppercase border border-[#E7EAF0] hover:bg-[#FCE8F0] hover:text-[#E4005A] hover:border-[#E4005A]/30 transition-all shadow-2xs cursor-pointer"
            >
              <span>OUR METHODOLOGY</span>
            </button>
          </div>
        </section>

        {/* =================================================================== */}
        {/* 3. COMPACT FEATURE CARDS — ALL FIVE IN ONE ROW (DESKTOP) */}
        {/* Simplified: No icons, no numbering, no descriptions. ONLY title & link */}
        {/* =================================================================== */}
        <section className="my-auto py-2 w-full">
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-2.5 sm:gap-3 max-w-6xl mx-auto w-full">
            {featureCards.map((card) => {
              return (
                <Link
                  key={card.title}
                  href={card.href}
                  className="group min-h-[82px] lg:h-[90px] p-3 rounded-xl border border-[#E7EAF0] bg-white hover:border-[#E4005A] hover:bg-[#FCE8F0]/40 hover:shadow-sm transition-all flex flex-col justify-between"
                >
                  <div>
                    <h4 className="text-xs sm:text-[13px] lg:text-sm font-heading font-extrabold text-[#17294B] group-hover:text-[#E4005A] transition-colors tracking-tight leading-snug">
                      {card.title}
                    </h4>
                  </div>

                  <div className="flex items-center gap-1.5 text-[11px] font-bold text-[#E4005A] group-hover:translate-x-0.5 transition-all mt-auto pt-1">
                    <span>Access Module</span>
                    <ArrowRight size={12} className="text-[#E4005A]" />
                  </div>
                </Link>
              );
            })}
          </div>
        </section>

        {/* =================================================================== */}
        {/* 4. FOOTER — CENTERED AT THE BOTTOM */}
        {/* =================================================================== */}
        <footer className="shrink-0 py-1.5 text-center text-[10px] sm:text-[11px] text-[#52627A]">
          <span>Royals Intelligence Season 02 · Rajasthan Royals Cricket Analytics · Built to Find the Difference.</span>
        </footer>
      </main>

      {/* =================================================================== */}
      {/* 5. METHODOLOGY MODAL DIALOG — PRESIGNED ACCESS */}
      {/* =================================================================== */}
      {methodologyOpen && (
        <div
          id="methodology"
          role="dialog"
          aria-modal="true"
          className="fixed inset-0 z-50 bg-[#101D3A]/50 backdrop-blur-xs flex items-center justify-center p-4 overflow-y-auto"
          onClick={() => setMethodologyOpen(false)}
        >
          <div
            className="bg-white rounded-2xl border border-[#E7EAF0] max-w-2xl w-full p-6 sm:p-8 shadow-xl space-y-6 animate-hero-fade relative"
            onClick={(e) => e.stopPropagation()}
          >
            {/* Modal Header */}
            <div className="flex items-start justify-between border-b border-[#E7EAF0] pb-4">
              <div>
                <span className="text-[10px] font-mono font-bold tracking-wider text-[#D4145A] uppercase block mb-1">
                  Rigorous Mathematical Architecture
                </span>
                <h2 className="text-xl font-heading font-extrabold text-[#101D3A] tracking-tight">
                  OUR METHODOLOGY
                </h2>
                <p className="text-xs text-[#52627A] mt-1">
                  Built on evidence. Driven by context. Five scientific pillars governing player valuation.
                </p>
              </div>
              <button
                onClick={() => setMethodologyOpen(false)}
                className="p-1.5 rounded-lg text-[#52627A] hover:text-[#D4145A] hover:bg-[#F8E8EF] transition-colors"
                aria-label="Close modal"
              >
                <X size={18} />
              </button>
            </div>

            {/* 5 Pillars */}
            <div className="space-y-3.5 text-xs text-[#52627A]">
              <div className="p-3.5 rounded-xl border border-[#E7EAF0] bg-[#F8E8EF]">
                <div className="font-heading font-bold text-xs text-[#101D3A] mb-1 flex items-center justify-between">
                  <span>PILLAR 01: Contextual Benchmarking</span>
                  <span className="text-[10px] font-mono font-bold text-[#D4145A]">12-Cell Strata</span>
                </div>
                <p className="leading-relaxed">
                  Every delivery is benchmarked against Innings (2) &times; Phase (3) &times; Tier (2) strata to eliminate structural entry bias and determine true situational expectation.
                </p>
              </div>

              <div className="p-3.5 rounded-xl border border-[#E7EAF0] bg-[#F8E8EF]">
                <div className="font-heading font-bold text-xs text-[#101D3A] mb-1 flex items-center justify-between">
                  <span>PILLAR 02: Empirical Bayes Shrinkage</span>
                  <span className="text-[10px] font-mono font-bold text-[#D4145A]">Gaussian Prior</span>
                </div>
                <p className="leading-relaxed">
                  Separates skill from noise using league population priors (&mu;<sub>0</sub>, &tau;<sup>2</sup>), shrinking small-sample outliers toward the true population mean.
                </p>
              </div>

              <div className="p-3.5 rounded-xl border border-[#E7EAF0] bg-[#F8E8EF]">
                <div className="font-heading font-bold text-xs text-[#101D3A] mb-1 flex items-center justify-between">
                  <span>PILLAR 03: Conservative PRI</span>
                  <span className="text-[10px] font-mono font-bold text-[#D4145A]">Uncertainty Penalty</span>
                </div>
                <p className="leading-relaxed">
                  Ranks candidates conservatively by penalizing high posterior uncertainty, valuing repeatable execution over speculative high-volatility spikes.
                </p>
              </div>

              <div className="p-3.5 rounded-xl border border-[#E7EAF0] bg-[#F8E8EF]">
                <div className="font-heading font-bold text-xs text-[#101D3A] mb-1 flex items-center justify-between">
                  <span>PILLAR 04: 1-SE Lower Credible Bounds</span>
                  <span className="text-[10px] font-mono font-bold text-[#D4145A]">1-Standard-Error</span>
                </div>
                <p className="leading-relaxed">
                  Calculates rigorous 1-standard-error defensive lower bounds across all posterior distributions for defensible worst-case reliability estimates.
                </p>
              </div>

              <div className="p-3.5 rounded-xl border border-[#E7EAF0] bg-[#F8E8EF]">
                <div className="font-heading font-bold text-xs text-[#101D3A] mb-1 flex items-center justify-between">
                  <span>PILLAR 05: Official Qualification Threshold</span>
                  <span className="text-[10px] font-mono font-bold text-[#D4145A]">&ge; 60 Balls</span>
                </div>
                <p className="leading-relaxed">
                  Strict qualification standard enforcing at least 60 pressure deliveries to guarantee sample adequacy before candidate ranking.
                </p>
              </div>
            </div>

            {/* Modal Footer */}
            <div className="pt-2 border-t border-[#E7EAF0] flex items-center justify-between">
              <Link
                href="/overview"
                onClick={() => setMethodologyOpen(false)}
                className="text-xs font-bold text-[#101D3A] hover:text-[#D4145A] hover:underline inline-flex items-center gap-1"
              >
                <span>View Full Executive Architecture</span>
                <ArrowRight size={12} />
              </Link>
              <button
                onClick={() => setMethodologyOpen(false)}
                className="px-4 py-1.5 rounded-xl bg-[#101D3A] text-white text-xs font-semibold hover:bg-[#A80F50] transition-colors"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
