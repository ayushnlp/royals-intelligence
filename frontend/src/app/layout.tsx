import type { Metadata } from "next";
import "@/styles/globals.css";
import { Sidebar } from "@/components/layout/Sidebar";
import { Header } from "@/components/layout/Header";

export const metadata: Metadata = {
  title: "Royals Intelligence | Rajasthan Royals Analytics",
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
      <body className="bg-[#F4F6FA] text-[#101C37] antialiased flex min-h-screen">
        {/* Rajasthan Royals Sidebar */}
        <Sidebar />

        {/* Main Application Shell Content */}
        <div className="flex-1 flex flex-col min-w-0">
          <Header />
          <main className="flex-1 p-6 md:p-8 max-w-7xl w-full mx-auto overflow-y-auto">
            {children}
          </main>
        </div>
      </body>
    </html>
  );
}
