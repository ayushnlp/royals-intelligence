"use client";

import React from "react";
import { usePathname } from "next/navigation";
import { Sidebar } from "@/components/layout/Sidebar";
import { Header } from "@/components/layout/Header";

interface AppShellProps {
  children: React.ReactNode;
}

export const AppShell: React.FC<AppShellProps> = ({ children }) => {
  const pathname = usePathname();
  const isPublicHome = pathname === "/";

  if (isPublicHome) {
    return (
      <div className="min-h-screen bg-white text-[#101D3A] antialiased selection:bg-[#D4145A]/20 selection:text-[#101D3A]">
        {children}
      </div>
    );
  }

  return (
    <div className="bg-[#FFFFFF] text-[#101D3A] antialiased flex min-h-screen selection:bg-[#D4145A]/20 selection:text-[#101D3A]">
      {/* Dashboard Sidebar */}
      <Sidebar />

      {/* Main Dashboard Application Shell */}
      <div className="flex-1 flex flex-col min-w-0 bg-[#FFFFFF]">
        <Header />
        <main className="flex-1 p-6 md:p-8 max-w-7xl w-full mx-auto overflow-y-auto bg-[#FFFFFF]">
          {children}
        </main>
      </div>
    </div>
  );
};
