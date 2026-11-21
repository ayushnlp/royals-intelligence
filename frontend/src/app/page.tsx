"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import {
  ArrowRight,
  X,
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
    <div className="w-full space-y-8 sm:space-y-10 py-2 sm:py-4">
      {/* =================================================================== */}
      {/* 1. HERO SECTION — Central anchor with official RR branding & Poppins */}
      {/* =================================================================== */}
      <section className="flex flex-col items-center text-center pt-2 sm:pt-4 pb-2">
        {/* Eyebrow: ROYALS INTELLIGENCE */}
        <div className="mb-2">
          <span className="font-heading font-extrabold text-xs sm:text-[13px] tracking-[0.28em] text-[#17294B] uppercase">
            ROYALS INTELLIGENCE
          </span>
        </div>

        {/* Badge: SEASON 02 */}
        <div className="mb-2.5">
          <span className="inline-flex items-center gap-1.5 px-3.5 py-1 rounded-full text-xs font-mono font-bold tracking-wider bg-[#FCE8F0] text-[#E4005A] border border-[#E4005A]/30 shadow-2xs">
            <span className="w-1.5 h-1.5 rounded-full bg-[#E4005A]" />
            SEASON 02
          </span>
        </div>

        {/* Sublabel: RAJASTHAN ROYALS · DATA-DRIVEN CRICKET */}
        <div className="mb-3">
          <p className="text-xs sm:text-[13px] font-semibold tracking-[0.22em] text-[#74658F] uppercase">
            RAJASTHAN ROYALS · DATA-DRIVEN CRICKET
          </p>
        </div>

        {/* Headline: INTELLIGENCE FOR RAJASTHAN ROYALS. */}
        <h1 className="font-heading font-extrabold text-[32px] sm:text-[42px] md:text-[48px] lg:text-[54px] text-[#17294B] tracking-tight leading-[1.08] max-w-4xl mx-auto mb-3">
          INTELLIGENCE FOR RAJASTHAN ROYALS.
        </h1>

        {/* Subtitle: Built to Find the Difference. */}
        <h3 className="font-heading font-bold text-lg sm:text-xl lg:text-[22px] text-[#E4005A] tracking-tight mb-8">
          Built to Find the Difference.
        </h3>

        {/* Hero CTAs */}
        <div className="flex flex-row items-center justify-center gap-4">
          <Link
            href="/overview"
            className="group inline-flex items-center justify-center gap-2.5 px-8 py-3.5 sm:px-9 sm:py-4 rounded-xl bg-gradient-to-r from-[#17294B] to-[#E4005A] hover:from-[#17294B] hover:to-[#950460] text-white text-sm sm:text-[15px] font-bold tracking-wider uppercase transition-all duration-200 shadow-lg hover:shadow-xl hover:scale-[1.02] active:scale-[0.98] min-h-[48px] sm:min-h-[52px]"
          >
            <span>EXPLORE INTELLIGENCE</span>
            <ArrowRight size={17} className="text-white transition-transform group-hover:translate-x-0.5" />
          </Link>

          <button
            onClick={() => setMethodologyOpen(true)}
            className="inline-flex items-center justify-center gap-1.5 px-6 py-3.5 sm:px-7 sm:py-4 rounded-xl bg-white text-[#17294B] text-sm sm:text-[15px] font-semibold tracking-wider uppercase border border-[#E7EAF0] hover:bg-[#FCE8F0] hover:text-[#E4005A] hover:border-[#E4005A]/30 transition-all shadow-2xs cursor-pointer min-h-[48px] sm:min-h-[52px]"
          >
            <span>OUR METHODOLOGY</span>
          </button>
        </div>
      </section>

      {/* =================================================================== */}
      {/* 2. COMPACT FEATURE CARDS — ALL FIVE IN ONE ROW (DESKTOP) */}
      {/* =================================================================== */}
      <section className="pt-2 w-full">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3 max-w-6xl mx-auto w-full">
          {featureCards.map((card) => {
            return (
              <Link
                key={card.title}
                href={card.href}
                className="group min-h-[96px] lg:h-[104px] p-3.5 rounded-xl border border-[#E7EAF0] bg-white hover:border-[#E4005A] hover:bg-[#FCE8F0]/40 hover:shadow-sm transition-all flex flex-col justify-between"
              >
                <div>
                  <h4 className="text-xs sm:text-[13px] lg:text-[14px] font-heading font-extrabold text-[#17294B] group-hover:text-[#E4005A] transition-colors tracking-tight leading-snug">
                    {card.title}
                  </h4>
                </div>

                <div className="flex items-center gap-1.5 text-xs font-bold text-[#E4005A] group-hover:translate-x-0.5 transition-all mt-auto pt-1">
                  <span>Access Module</span>
                  <ArrowRight size={13} className="text-[#E4005A]" />
                </div>
              </Link>
            );
          })}
        </div>
      </section>

      {/* =================================================================== */}
      {/* 3. FOOTER — CENTERED AT THE BOTTOM */}
      {/* =================================================================== */}
      <footer className="pt-4 pb-2 text-center text-[10px] sm:text-[11px] text-[#52627A]">
        <span>Royals Intelligence Season 02 · Rajasthan Royals Cricket Analytics · Built to Find the Difference.</span>
      </footer>

      {/* =================================================================== */}
      {/* 4. METHODOLOGY MODAL DIALOG — PRESIGNED ACCESS */}
      {/* =================================================================== */}
      {methodologyOpen && (
        <div
          id="methodology"
          role="dialog"
          aria-modal="true"
          className="fixed inset-0 z-50 bg-[#17294B]/50 backdrop-blur-xs flex items-center justify-center p-4 overflow-y-auto"
          onClick={() => setMethodologyOpen(false)}
        >
          <div
            className="bg-white rounded-2xl border border-[#E7EAF0] max-w-2xl w-full p-6 sm:p-8 shadow-xl space-y-6 animate-hero-fade relative"
            onClick={(e) => e.stopPropagation()}
          >
            {/* Modal Header */}
            <div className="flex items-start justify-between border-b border-[#E7EAF0] pb-4">
              <div>
                <span className="text-[10px] font-mono font-bold tracking-wider text-[#E4005A] uppercase block mb-1">
                  Rigorous Mathematical Architecture
                </span>
                <h2 className="text-xl font-heading font-extrabold text-[#17294B] tracking-tight">
                  OUR METHODOLOGY
                </h2>
                <p className="text-xs text-[#52627A] mt-1">
                  Built on evidence. Driven by context. Five scientific pillars governing player valuation.
                </p>
              </div>
              <button
                onClick={() => setMethodologyOpen(false)}
                className="p-1.5 rounded-lg text-[#52627A] hover:text-[#E4005A] hover:bg-[#FCE8F0] transition-colors"
                aria-label="Close modal"
              >
                <X size={18} />
              </button>
            </div>

            {/* 5 Pillars */}
            <div className="space-y-3.5 text-xs text-[#52627A]">
              <div className="p-3.5 rounded-xl border border-[#E7EAF0] bg-[#FCE8F0]">
                <div className="font-heading font-bold text-xs text-[#17294B] mb-1 flex items-center justify-between">
                  <span>PILLAR 01: Contextual Benchmarking</span>
                  <span className="text-[10px] font-mono font-bold text-[#E4005A]">12-Cell Strata</span>
                </div>
                <p className="leading-relaxed">
                  Every delivery is benchmarked against Innings (2) &times; Phase (3) &times; Tier (2) strata to eliminate structural entry bias and determine true situational expectation.
                </p>
              </div>

              <div className="p-3.5 rounded-xl border border-[#E7EAF0] bg-[#FCE8F0]">
                <div className="font-heading font-bold text-xs text-[#17294B] mb-1 flex items-center justify-between">
                  <span>PILLAR 02: Empirical Bayes Shrinkage</span>
                  <span className="text-[10px] font-mono font-bold text-[#E4005A]">Gaussian Prior</span>
                </div>
                <p className="leading-relaxed">
                  Separates skill from noise using league population priors (&mu;<sub>0</sub>, &tau;<sup>2</sup>), shrinking small-sample outliers toward the true population mean.
                </p>
              </div>

              <div className="p-3.5 rounded-xl border border-[#E7EAF0] bg-[#FCE8F0]">
                <div className="font-heading font-bold text-xs text-[#17294B] mb-1 flex items-center justify-between">
                  <span>PILLAR 03: Conservative PRI</span>
                  <span className="text-[10px] font-mono font-bold text-[#E4005A]">Uncertainty Penalty</span>
                </div>
                <p className="leading-relaxed">
                  Ranks candidates conservatively by penalizing high posterior uncertainty, valuing repeatable execution over speculative high-volatility spikes.
                </p>
              </div>

              <div className="p-3.5 rounded-xl border border-[#E7EAF0] bg-[#FCE8F0]">
                <div className="font-heading font-bold text-xs text-[#17294B] mb-1 flex items-center justify-between">
                  <span>PILLAR 04: 1-SE Lower Credible Bounds</span>
                  <span className="text-[10px] font-mono font-bold text-[#E4005A]">1-Standard-Error</span>
                </div>
                <p className="leading-relaxed">
                  Calculates rigorous 1-standard-error defensive lower bounds across all posterior distributions for defensible worst-case reliability estimates.
                </p>
              </div>

              <div className="p-3.5 rounded-xl border border-[#E7EAF0] bg-[#FCE8F0]">
                <div className="font-heading font-bold text-xs text-[#17294B] mb-1 flex items-center justify-between">
                  <span>PILLAR 05: Official Qualification Threshold</span>
                  <span className="text-[10px] font-mono font-bold text-[#E4005A]">&ge; 60 Balls</span>
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
                className="text-xs font-bold text-[#17294B] hover:text-[#E4005A] hover:underline inline-flex items-center gap-1"
              >
                <span>View Full Executive Architecture</span>
                <ArrowRight size={12} />
              </Link>
              <button
                onClick={() => setMethodologyOpen(false)}
                className="px-4 py-1.5 rounded-xl bg-[#17294B] text-white text-xs font-semibold hover:bg-[#950460] transition-colors"
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
