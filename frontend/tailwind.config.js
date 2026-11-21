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
          navy: "#31136C",
          pink: "#950460",
          white: "#FFFFFF",
          orange: "#950460",
          green: "#950460",
          // Functional tokens derived strictly from the five authorized colors
          bg: "#FFFFFF",
          bgSecondary: "#FFFFFF",
          card: "#FFFFFF",
          surface: "#FFFFFF",
          text: "#31136C",
          textPrimary: "#31136C",
          textSecondary: "rgba(23, 43, 73, 0.7)",
          muted: "rgba(23, 43, 73, 0.7)",
          border: "rgba(23, 43, 73, 0.12)",
          rose: "#950460",
          dustyPink: "#950460",
          pinkBg: "rgba(183, 110, 133, 0.1)",
          success: "#950460",
          warning: "#950460",
          gold: "#950460",
          navyDark: "#31136C",
          navyLight: "#31136C",
        },
      },
      fontFamily: {
        sans: ["Inter", "-apple-system", "BlinkMacSystemFont", "Segoe UI", "Roboto", "sans-serif"],
        heading: ["Sora", "Inter", "-apple-system", "BlinkMacSystemFont", "sans-serif"],
        mono: ["JetBrains Mono", "IBM Plex Mono", "SFMono-Regular", "Menlo", "monospace"],
      },
      boxShadow: {
        soft: "0 2px 8px rgba(23, 43, 73, 0.05), 0 1px 2px rgba(23, 43, 73, 0.03)",
        elevation: "0 6px 20px rgba(23, 43, 73, 0.08), 0 2px 4px rgba(23, 43, 73, 0.04)",
        card: "0 1px 3px rgba(23, 43, 73, 0.05)",
      },
    },
  },
  plugins: [],
};
