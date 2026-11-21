"use client";

import React, { useEffect } from "react";
import Link from "next/link";
import { AlertTriangle, RefreshCw, Home } from "lucide-react";

export default function ErrorBoundary({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    // Log unexpected client or SSR error
    console.error("Royals Intelligence Application Error:", error);
  }, [error]);

  return (
    <div className="min-h-[70vh] flex items-center justify-center p-6 bg-white">
      <div className="max-w-md w-full bg-white border border-[#31136C]/12 rounded-xl shadow-sm p-8 text-center space-y-6">
        <div className="w-14 h-14 mx-auto rounded-full bg-[#950460]/10 border border-[#950460]/30 flex items-center justify-center">
          <AlertTriangle className="w-7 h-7 text-[#950460]" />
        </div>

        <div className="space-y-2">
          <span className="text-[10px] font-mono tracking-widest text-[#31136C] uppercase font-bold px-2 py-0.5 rounded bg-[#950460]/10 border border-[#950460]/30">
            Analytics System Notification
          </span>
          <h2 className="text-xl font-bold text-[#31136C] tracking-tight font-heading">
            An Unexpected Error Occurred
          </h2>
          <p className="text-xs text-[#31136C]/70 leading-relaxed">
            The application encountered a temporary runtime condition while rendering this view.
          </p>
          {error.digest && (
            <p className="text-[10px] font-mono text-[#31136C]/70">
              Error Digest: {error.digest}
            </p>
          )}
        </div>

        <div className="flex items-center justify-center gap-3 pt-2">
          <button
            onClick={() => reset()}
            className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-[#31136C] text-white text-xs font-semibold hover:bg-[#31136C]/90 transition-colors shadow-soft"
          >
            <RefreshCw size={13} />
            <span>Try Again</span>
          </button>

          <Link
            href="/overview"
            className="inline-flex items-center gap-2 px-4 py-2 rounded-lg border border-[#31136C]/15 bg-white text-[#31136C] text-xs font-semibold hover:bg-[#31136C]/05 transition-colors"
          >
            <Home size={13} />
            <span>Overview</span>
          </Link>
        </div>
      </div>
    </div>
  );
}
