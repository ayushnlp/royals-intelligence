/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/features/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        royals: {
          navy: "#111C38",
          navyDark: "#0B1220",
          navyLight: "#1A2B50",
          pink: "#E91E8C",
          pinkSoft: "#FCE7F3",
          pinkHover: "#D81B60",
          gold: "#D6B56D",
          goldLight: "#E4CA8F",
          bg: "#F5F6FA",
          surface: "#FFFFFF",
          textPrimary: "#111827",
          textSecondary: "#64748B",
          border: "#E5E7EB",
          success: "#059669",
          warning: "#D97706",
        },
      },
      fontFamily: {
        sans: ["Inter", "-apple-system", "BlinkMacSystemFont", "Segoe UI", "Roboto", "sans-serif"],
        mono: ["JetBrains Mono", "SFMono-Regular", "Menlo", "monospace"],
      },
    },
  },
  plugins: [],
};
