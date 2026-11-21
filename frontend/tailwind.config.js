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
          navy: "#17294B",
          deepNavy: "#17294B",
          pink: "#E4005A",
          deepPink: "#E4005A",
          cardinalPink: "#950460",
          lightPink: "#FCE8F0",
          lightBlue: "#EEF4FC",
          rose: "#FCE8F0",
          white: "#FFFFFF",
          border: "#E7EAF0",
          body: "#263653",
          bodyText: "#263653",
          muted: "#74658F",
          mutedText: "#74658F",
          orange: "#F28C28",
          green: "#15966B",
          verifiedGreen: "#15966B",
          // Functional tokens
          bg: "#FFFFFF",
          bgSecondary: "#FCE8F0",
          card: "#FFFFFF",
          surface: "#FFFFFF",
          text: "#17294B",
          textPrimary: "#17294B",
          textSecondary: "#263653",
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
