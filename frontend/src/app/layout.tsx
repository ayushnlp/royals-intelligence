import type { Metadata } from "next";
import { Poppins } from "next/font/google";
import "@/styles/globals.css";
import { AppShell } from "@/components/layout/AppShell";

const poppins = Poppins({
  subsets: ["latin"],
  weight: ["400", "500", "600", "700", "800"],
  variable: "--font-poppins",
  display: "swap",
});

export const metadata: Metadata = {
  title: "Royals Intelligence | Rajasthan Royals Cricket Analytics",
  description:
    "Rajasthan Royals Cricket Intelligence & Dynamic Pressure Analytics Engine — SupeRR Selector Season 2 Round 1.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={poppins.variable}>
      <body className={`${poppins.className} font-sans bg-white text-[#17294B] antialiased min-h-screen`}>
        <AppShell>{children}</AppShell>
      </body>
    </html>
  );
}
