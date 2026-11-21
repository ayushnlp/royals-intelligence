"use client";

import React from "react";

interface ConnectionWaveformProps {
  isHealthy: boolean;
  isProbing?: boolean;
  onProbe?: () => void;
  className?: string;
}

/**
 * ConnectionWaveform:
 * Compact, elegant oscilloscope-style waveform indicator.
 * - Connected: Continuously animated up-and-down waveform in authentic Rajasthan Royals gradient (#17294B to #E4005A).
 * - Disconnected: Freezes immediately in a static neutral flatline state.
 * - Respects prefers-reduced-motion.
 */
export const ConnectionWaveform: React.FC<ConnectionWaveformProps> = ({
  isHealthy,
  isProbing = false,
  onProbe,
  className = "",
}) => {
  // Continuous 2-cycle smooth waveform path spanning 128px (2 x 64px periods)
  const activeWavePath =
    "M 0,12 L 6,12 C 9,12 11,8 14,8 C 17,8 19,16 22,16 C 24,16 26,4 29,4 C 32,4 34,20 37,20 C 40,20 42,9 45,9 C 48,9 50,15 53,15 C 56,15 58,12 64,12 L 70,12 C 73,12 75,8 78,8 C 81,8 83,16 86,16 C 88,16 90,4 93,4 C 96,4 98,20 101,20 C 104,20 106,9 109,9 C 112,9 114,15 117,15 C 120,15 122,12 128,12";

  // Neutral static flatline path when disconnected
  const flatlinePath = "M 0,12 L 64,12";

  return (
    <button
      type="button"
      onClick={onProbe}
      disabled={!onProbe}
      aria-label={
        isHealthy
          ? "Backend API Connected — Live Telemetry Active"
          : "Backend API Disconnected — Telemetry Offline (Click to probe)"
      }
      title={
        isHealthy
          ? "Backend API Connected (Live Waveform Active)"
          : isProbing
          ? "Probing Backend API..."
          : "Backend API Disconnected (Click to probe)"
      }
      className={`group relative flex items-center justify-center w-[64px] h-[24px] overflow-hidden bg-transparent border-0 p-0 m-0 cursor-pointer focus:outline-none transition-opacity ${
        isProbing ? "opacity-60" : "opacity-100"
      } ${className}`}
    >
      <svg
        className="w-[64px] h-[24px] overflow-hidden"
        viewBox="0 0 64 24"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <defs>
          {/* Authentic Rajasthan Royals Waveform Gradient: RR Deep Pink (#E4005A) to Cardinal Pink (#950460) */}
          <linearGradient
            id="rr-waveform-gradient"
            x1="0%"
            y1="0%"
            x2="100%"
            y2="0%"
          >
            <stop offset="0%" stopColor="#E4005A" />
            <stop offset="50%" stopColor="#950460" />
            <stop offset="100%" stopColor="#E4005A" />
          </linearGradient>
        </defs>

        {isHealthy ? (
          /* Animated Waveform Group: Translates horizontally from 0 to -64px (-50%) */
          <g className="animate-waveform-flow will-change-transform">
            <path
              d={activeWavePath}
              stroke="url(#rr-waveform-gradient)"
              strokeWidth="1.75"
              strokeLinecap="round"
              strokeLinejoin="round"
              fill="none"
            />
          </g>
        ) : (
          /* Static Neutral Flatline Group: Frozen, zero movement */
          <g>
            <path
              d={flatlinePath}
              stroke="#17294B"
              strokeOpacity="0.3"
              strokeWidth="1.5"
              strokeLinecap="round"
              fill="none"
            />
          </g>
        )}
      </svg>
    </button>
  );
};
