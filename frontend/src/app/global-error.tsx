"use client";

import React, { useEffect } from "react";
import Link from "next/link";
import "@/styles/globals.css";

export default function GlobalError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    console.error("Royals Intelligence Global Error:", error);
  }, [error]);

  return (
    <html lang="en">
      <body className="bg-[#F5F6FA] text-[#111827] antialiased min-h-screen flex items-center justify-center p-6">
        <div className="max-w-md w-full bg-white border border-slate-200 rounded-xl shadow-sm p-8 text-center space-y-5">
          <div className="w-12 h-12 mx-auto rounded-full bg-rose-50 border border-rose-100 flex items-center justify-center">
            <span className="text-[#E91E8C] text-xl font-bold">!</span>
          </div>

          <div className="space-y-1">
            <h2 className="text-lg font-bold text-slate-900">
              Application Error
            </h2>
            <p className="text-xs text-slate-500">
              A critical failure occurred. Please reload the application.
            </p>
          </div>

          <div className="flex justify-center gap-3 pt-2">
            <button
              onClick={() => reset()}
              className="px-4 py-2 rounded-lg bg-[#111C38] text-white text-xs font-semibold hover:bg-[#1A2B50] transition-colors"
            >
              Reload
            </button>
            <Link
              href="/"
              className="px-4 py-2 rounded-lg bg-slate-100 text-slate-700 text-xs font-semibold hover:bg-slate-200 transition-colors"
            >
              Home
            </Link>
          </div>
        </div>
      </body>
    </html>
  );
}
