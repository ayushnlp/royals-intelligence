"use client";

import React from "react";
import { Sidebar } from "@/components/layout/Sidebar";
import { Header } from "@/components/layout/Header";

interface AppShellProps {
  children: React.ReactNode;
}

export const AppShell: React.FC<AppShellProps> = ({ children }) => {
  return (
    <div className="bg-[#FFFFFF] text-[#17294B] antialiased flex min-h-screen selection:bg-[#E4005A]/20 selection:text-[#17294B] overflow-x-hidden max-w-[100vw]">
      {/* Dashboard Sidebar */}
      <Sidebar />

      {/* Main Dashboard Application Shell */}
      <div className="flex-1 flex flex-col min-w-0 bg-[#FFFFFF] overflow-x-hidden">
        <Header />
        <main className="flex-1 p-4 sm:p-6 md:p-8 max-w-7xl w-full mx-auto overflow-y-auto bg-[#FFFFFF] min-w-0">
          {children}
        </main>
      </div>
    </div>
  );
};
