import type { Metadata } from "next";
import "@/styles/globals.css";
import { AppShell } from "@/components/layout/AppShell";

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
    <html lang="en">
      <body className="bg-white text-[#17294B] antialiased min-h-screen">
        <AppShell>{children}</AppShell>
      </body>
    </html>
  );
}
