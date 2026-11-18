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
    <div className="min-h-[70vh] flex items-center justify-center p-6">
      <div className="max-w-md w-full bg-white border border-slate-200/80 rounded-xl shadow-sm p-8 text-center space-y-6">
        <div className="w-14 h-14 mx-auto rounded-full bg-rose-50 border border-rose-100 flex items-center justify-center">
          <AlertTriangle className="w-7 h-7 text-[#E91E8C]" />
        </div>

        <div className="space-y-2">
          <span className="text-[10px] font-mono tracking-widest text-[#E91E8C] uppercase font-bold">
            Analytics System Notification
          </span>
          <h2 className="text-xl font-bold text-slate-900 tracking-tight">
            An Unexpected Error Occurred
          </h2>
          <p className="text-xs text-slate-600 leading-relaxed">
            The application encountered a temporary runtime condition while rendering this view.
          </p>
          {error.digest && (
            <p className="text-[10px] font-mono text-slate-400">
              Error Digest: {error.digest}
            </p>
          )}
        </div>

        <div className="flex items-center justify-center gap-3 pt-2">
          <button
            onClick={() => reset()}
            className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-[#111C38] text-white text-xs font-semibold hover:bg-[#1A2B50] transition-colors shadow-sm"
          >
            <RefreshCw size={13} />
            <span>Try Again</span>
          </button>

          <Link
            href="/"
            className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-slate-100 text-slate-700 text-xs font-semibold hover:bg-slate-200 transition-colors"
          >
            <Home size={13} />
            <span>Overview</span>
          </Link>
        </div>
      </div>
    </div>
  );
}
