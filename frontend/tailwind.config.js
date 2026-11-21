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
          navy: "#101D3A",
          pink: "#D4145A",
          pinkDeep: "#A80F50",
          rose: "#F8E8EF",
          white: "#FFFFFF",
          border: "#E7EAF0",
          body: "#52627A",
          orange: "#F28C28",
          green: "#15966B",
          // Functional tokens
          bg: "#FFFFFF",
          bgSecondary: "#F8E8EF",
          card: "#FFFFFF",
          surface: "#FFFFFF",
          text: "#101D3A",
          textPrimary: "#101D3A",
          textSecondary: "#52627A",
          muted: "#52627A",
          success: "#15966B",
          warning: "#F28C28",
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
