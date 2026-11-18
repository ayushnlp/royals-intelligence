"use client";

import Link from "next/link";

export default function NotFound() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] space-y-4 text-center">
      <h2 className="text-2xl font-bold text-[#101C37]">Page Not Found</h2>
      <p className="text-xs text-slate-500">The requested tactical resource could not be located.</p>
      <Link
        href="/"
        className="px-4 py-2 rounded-lg bg-[#E91E8C] text-white text-xs font-semibold shadow-md hover:bg-[#E91E8C]/90 transition-all"
      >
        Return to Overview
      </Link>
    </div>
  );
}
