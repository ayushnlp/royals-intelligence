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
      id: "01",
      title: "PRESSURE INTELLIGENCE",
      href: "/pressure",
      icon: Shield,
    },
    {
      id: "02",
      title: "UNCAPPED SCOUTING",
      href: "/uncapped",
      icon: Sparkles,
    },
    {
      id: "03",
      title: "TACTICAL INTELLIGENCE",
      href: "/tactical",
      icon: Crosshair,
    },
    {
      id: "04",
      title: "DOMESTIC & MATCHES",
      href: "/domestic",
      icon: Swords,
    },
    {
      id: "05",
      title: "VENUE & PITCH INTELLIGENCE",
      href: "/venues",
      icon: MapPin,
    },
  ];

  return (
    <div className="min-h-screen lg:h-screen lg:max-h-screen flex flex-col bg-white text-[#31136C] overflow-x-hidden selection:bg-[#950460]/20 selection:text-[#31136C]">
      {/* =================================================================== */}
      {/* 1. HEADER — AUTHENTIC RAJASTHAN ROYALS BRANDING */}
      {/* =================================================================== */}
      <header className="h-14 sm:h-16 shrink-0 bg-white border-b border-[#31136C]/12 px-4 sm:px-6 lg:px-8 flex items-center justify-between z-30">
        {/* Left: Pure Brand Text */}
        <Link
          href="/"
          className="font-heading font-extrabold text-base sm:text-lg tracking-tight text-[#31136C] hover:text-[#950460] transition-colors"
        >
          ROYALS INTELLIGENCE
        </Link>

        {/* Right: Prominent Header Explore Button */}
        <Link
          href="/overview"
          className="group inline-flex items-center gap-2 px-4 py-2 sm:px-5 sm:py-2.5 rounded-xl bg-[#31136C] hover:bg-[#950460] text-white text-xs sm:text-[13px] font-bold tracking-wider transition-all duration-200 shadow-md hover:shadow-lg hover:scale-[1.02] active:scale-[0.98]"
        >
          <span>EXPLORE INTELLIGENCE</span>
          <ArrowRight size={14} className="text-[#950460] group-hover:text-white transition-colors group-hover:translate-x-0.5" />
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
            <span className="font-heading font-extrabold text-[11px] sm:text-xs tracking-[0.25em] text-[#31136C] uppercase">
              ROYALS INTELLIGENCE
            </span>
          </div>

          {/* Badge: SEASON 02 */}
          <div className="mb-1.5">
            <span className="inline-flex items-center gap-1.5 px-3 py-0.5 rounded-full text-[10px] sm:text-[11px] font-mono font-bold tracking-wider bg-[#F7F6FB] text-[#950460] border border-[#950460]/30 shadow-2xs">
              <span className="w-1.5 h-1.5 rounded-full bg-[#950460]" />
              SEASON 02
            </span>
          </div>

          {/* Sublabel: RAJASTHAN ROYALS · DATA-DRIVEN CRICKET */}
          <div className="mb-2">
            <p className="text-[11px] sm:text-xs font-semibold tracking-[0.18em] text-[#31136C]/70 uppercase">
              RAJASTHAN ROYALS · DATA-DRIVEN CRICKET
            </p>
          </div>

          {/* Headline: INTELLIGENCE FOR RAJASTHAN ROYALS. */}
          <h1 className="font-heading font-extrabold text-[clamp(1.5rem,2.6vw,2.4rem)] text-[#31136C] tracking-tight leading-[1.12] max-w-4xl mx-auto mb-1.5">
            INTELLIGENCE FOR RAJASTHAN ROYALS.
          </h1>

          {/* Subtitle: Built to Find the Difference. */}
          <h3 className="font-heading font-bold text-[clamp(0.95rem,1.35vw,1.25rem)] text-[#950460] tracking-tight mb-4">
            Built to Find the Difference.
          </h3>

          {/* Hero CTAs */}
          <div className="flex flex-row items-center justify-center gap-3.5">
            <Link
              href="/overview"
              className="group inline-flex items-center justify-center gap-2.5 px-7 py-3 sm:px-8 sm:py-3.5 rounded-xl bg-gradient-to-r from-[#31136C] to-[#950460] hover:from-[#31136C] hover:to-[#950460] text-white text-xs sm:text-sm font-bold tracking-wider uppercase transition-all duration-200 shadow-lg hover:shadow-xl hover:scale-[1.02] active:scale-[0.98]"
            >
              <span>EXPLORE INTELLIGENCE</span>
              <ArrowRight size={16} className="text-white transition-transform group-hover:translate-x-0.5" />
            </Link>

            <button
              onClick={() => setMethodologyOpen(true)}
              className="inline-flex items-center justify-center gap-1.5 px-5 py-3 sm:px-6 sm:py-3.5 rounded-xl bg-white text-[#31136C] text-xs font-semibold tracking-wider uppercase border border-[#31136C]/15 hover:bg-[#F7F6FB] hover:text-[#950460] hover:border-[#950460]/30 transition-all shadow-2xs cursor-pointer"
            >
              <span>OUR METHODOLOGY</span>
            </button>
          </div>
        </section>

        {/* =================================================================== */}
        {/* 3. COMPACT FEATURE CARDS — ALL FIVE IN ONE ROW (DESKTOP) */}
        {/* Descriptions completely removed; displays icon, name, ID & link */}
        {/* =================================================================== */}
        <section className="my-auto py-2 w-full">
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-2.5 sm:gap-3 max-w-6xl mx-auto w-full">
            {featureCards.map((card) => {
              const Icon = card.icon;
              return (
                <Link
                  key={card.id}
                  href={card.href}
                  className="group min-h-[82px] lg:h-[90px] p-2.5 sm:p-3 rounded-xl border border-[#31136C]/12 bg-white hover:border-[#950460] hover:bg-[#F7F6FB]/60 hover:shadow-sm transition-all flex flex-col justify-between"
                >
                  <div>
                    <div className="flex items-center justify-between mb-1.5">
                      <div className="w-5 h-5 rounded-md bg-[#950460]/10 border border-[#950460]/30 flex items-center justify-center text-[#950460] shrink-0 group-hover:bg-[#950460] group-hover:text-white transition-colors">
                        <Icon size={12} />
                      </div>
                      <span className="text-[10px] font-mono font-bold text-[#950460]">
                        {card.id}
                      </span>
                    </div>

                    <h4 className="text-[11px] sm:text-xs font-heading font-bold text-[#31136C] group-hover:text-[#950460] transition-colors tracking-tight leading-tight">
                      {card.title}
                    </h4>
                  </div>

                  <div className="flex items-center gap-1 text-[10px] font-bold text-[#950460] group-hover:translate-x-0.5 transition-all mt-auto pt-1">
                    <span>Access Module</span>
                    <ChevronRight size={11} />
                  </div>
                </Link>
              );
            })}
          </div>
        </section>

        {/* =================================================================== */}
        {/* 4. FOOTER — CENTERED AT THE BOTTOM */}
        {/* =================================================================== */}
        <footer className="shrink-0 py-1.5 text-center text-[10px] sm:text-[11px] text-[#31136C]/70">
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
          className="fixed inset-0 z-50 bg-[#31136C]/50 backdrop-blur-xs flex items-center justify-center p-4 overflow-y-auto"
          onClick={() => setMethodologyOpen(false)}
        >
          <div
            className="bg-white rounded-2xl border border-[#31136C]/15 max-w-2xl w-full p-6 sm:p-8 shadow-xl space-y-6 animate-hero-fade relative"
            onClick={(e) => e.stopPropagation()}
          >
            {/* Modal Header */}
            <div className="flex items-start justify-between border-b border-[#31136C]/12 pb-4">
              <div>
                <span className="text-[10px] font-mono font-bold tracking-wider text-[#950460] uppercase block mb-1">
                  Rigorous Mathematical Architecture
                </span>
                <h2 className="text-xl font-heading font-extrabold text-[#31136C] tracking-tight">
                  OUR METHODOLOGY
                </h2>
                <p className="text-xs text-[#31136C]/70 mt-1">
                  Built on evidence. Driven by context. Five scientific pillars governing player valuation.
                </p>
              </div>
              <button
                onClick={() => setMethodologyOpen(false)}
                className="p-1.5 rounded-lg text-[#31136C]/70 hover:text-[#950460] hover:bg-[#F7F6FB] transition-colors"
                aria-label="Close modal"
              >
                <X size={18} />
              </button>
            </div>

            {/* 5 Pillars */}
            <div className="space-y-3.5 text-xs text-[#31136C]/70">
              <div className="p-3.5 rounded-xl border border-[#31136C]/12 bg-[#F7F6FB]">
                <div className="font-heading font-bold text-xs text-[#31136C] mb-1 flex items-center justify-between">
                  <span>PILLAR 01: Contextual Benchmarking</span>
                  <span className="text-[10px] font-mono font-bold text-[#950460]">12-Cell Strata</span>
                </div>
                <p className="leading-relaxed">
                  Every delivery is benchmarked against Innings (2) &times; Phase (3) &times; Tier (2) strata to eliminate structural entry bias and determine true situational expectation.
                </p>
              </div>

              <div className="p-3.5 rounded-xl border border-[#31136C]/12 bg-[#F7F6FB]">
                <div className="font-heading font-bold text-xs text-[#31136C] mb-1 flex items-center justify-between">
                  <span>PILLAR 02: Empirical Bayes Shrinkage</span>
                  <span className="text-[10px] font-mono font-bold text-[#950460]">Gaussian Prior</span>
                </div>
                <p className="leading-relaxed">
                  Separates skill from noise using league population priors (&mu;<sub>0</sub>, &tau;<sup>2</sup>), shrinking small-sample outliers toward the true population mean.
                </p>
              </div>

              <div className="p-3.5 rounded-xl border border-[#31136C]/12 bg-[#F7F6FB]">
                <div className="font-heading font-bold text-xs text-[#31136C] mb-1 flex items-center justify-between">
                  <span>PILLAR 03: Conservative PRI</span>
                  <span className="text-[10px] font-mono font-bold text-[#950460]">Uncertainty Penalty</span>
                </div>
                <p className="leading-relaxed">
                  Ranks candidates conservatively by penalizing high posterior uncertainty, valuing repeatable execution over speculative high-volatility spikes.
                </p>
              </div>

              <div className="p-3.5 rounded-xl border border-[#31136C]/12 bg-[#F7F6FB]">
                <div className="font-heading font-bold text-xs text-[#31136C] mb-1 flex items-center justify-between">
                  <span>PILLAR 04: 1-SE Lower Credible Bounds</span>
                  <span className="text-[10px] font-mono font-bold text-[#950460]">1-Standard-Error</span>
                </div>
                <p className="leading-relaxed">
                  Calculates rigorous 1-standard-error defensive lower bounds across all posterior distributions for defensible worst-case reliability estimates.
                </p>
              </div>

              <div className="p-3.5 rounded-xl border border-[#31136C]/12 bg-[#F7F6FB]">
                <div className="font-heading font-bold text-xs text-[#31136C] mb-1 flex items-center justify-between">
                  <span>PILLAR 05: Official Qualification Threshold</span>
                  <span className="text-[10px] font-mono font-bold text-[#950460]">&ge; 60 Balls</span>
                </div>
                <p className="leading-relaxed">
                  Strict qualification standard enforcing at least 60 pressure deliveries to guarantee sample adequacy before candidate ranking.
                </p>
              </div>
            </div>

            {/* Modal Footer */}
            <div className="pt-2 border-t border-[#31136C]/12 flex items-center justify-between">
              <Link
                href="/overview"
                onClick={() => setMethodologyOpen(false)}
                className="text-xs font-bold text-[#31136C] hover:text-[#950460] hover:underline inline-flex items-center gap-1"
              >
                <span>View Full Executive Architecture</span>
                <ArrowRight size={12} />
              </Link>
              <button
                onClick={() => setMethodologyOpen(false)}
                className="px-4 py-1.5 rounded-xl bg-[#31136C] text-white text-xs font-semibold hover:bg-[#950460] transition-colors"
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
