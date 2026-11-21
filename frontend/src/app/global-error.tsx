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
      <body className="bg-white text-[#17294B] antialiased min-h-screen flex items-center justify-center p-6">
        <div className="max-w-md w-full bg-white border border-[#E7EAF0] rounded-xl shadow-soft p-8 text-center space-y-5">
          <div className="w-12 h-12 mx-auto rounded-full bg-[#E4005A]/10 border border-[#E4005A]/30 flex items-center justify-center">
            <span className="text-[#17294B] text-xl font-bold font-heading">!</span>
          </div>

          <div className="space-y-1">
            <h2 className="text-lg font-bold text-[#17294B] font-heading">
              Application Error
            </h2>
            <p className="text-xs text-[#52627A]">
              A critical failure occurred. Please reload the application.
            </p>
          </div>

          <div className="flex justify-center gap-3 pt-2">
            <button
              onClick={() => reset()}
              className="px-4 py-2 rounded-lg bg-[#17294B] text-white text-xs font-semibold hover:bg-[#17294B]/90 transition-colors"
            >
              Reload
            </button>
            <Link
              href="/overview"
              className="px-4 py-2 rounded-lg border border-[#E7EAF0] bg-white text-[#17294B] text-xs font-semibold hover:bg-[#FCE8F0] transition-colors"
            >
              Overview
            </Link>
          </div>
        </div>
      </body>
    </html>
  );
}
