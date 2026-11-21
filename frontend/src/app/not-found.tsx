"use client";

import Link from "next/link";

export default function NotFound() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] space-y-4 text-center bg-white">
      <h2 className="text-2xl font-bold text-[#31136C] font-heading">Page Not Found</h2>
      <p className="text-xs text-[#31136C]/70">The requested tactical resource could not be located.</p>
      <Link
        href="/overview"
        className="px-4 py-2 rounded-lg bg-[#31136C] text-white text-xs font-semibold shadow-soft hover:bg-[#31136C]/90 transition-all"
      >
        Return to Executive Overview
      </Link>
    </div>
  );
}
