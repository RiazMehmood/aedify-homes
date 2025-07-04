'use client';

import { useState, useEffect } from "react";
import { signOut, useSession } from "next-auth/react";
import TopBar from "./SellerDashboard/Topbar";
import Sidebar from "./SellerDashboard/Sidebar";
import OverviewPanel from "./SellerDashboard/OverviewPanel";
import PerformanceCharts from "./SellerDashboard/PerformanceCharts";
import InquiriesPanel from "./SellerDashboard/InquiriesPanel";
import PropertyList from "./SellerDashboard/PropertyList";
import FloatingAIChat from "./SellerDashboard/FloatingAIChat";
import AddPropertyCard from "./SellerDashboard/AddPropertyCard"; // 🔸 Modal to create

const SellerDashboard = () => {
  const [showAddProperty, setShowAddProperty] = useState(false);
  // const { data: session } = useSession();

// useEffect(() => {
//   if (!session?.user?.email) return;

//   const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
//   const host = window.location.host;
//   const token = localStorage.getItem("token"); // If you’re storing JWT manually
//   const socket = new WebSocket(`${protocol}://${host}/ws?token=${token}`);

//   socket.onopen = () => {
//     console.log("🔌 WebSocket connected");
//   };

//   socket.onmessage = (event) => {
//     const data = JSON.parse(event.data);
//     if (data.event === "open_add_property_modal") {
//       setShowAddProperty(true);
//     }
//   };

//   socket.onclose = () => {
//     console.log("🔌 WebSocket disconnected");
//   };

//   socket.onerror = (error) => {
//     console.error("WebSocket error:", error);
//   };

//   return () => {
//     socket.close();
//   };
// }, [session?.user?.email]);


  const handleAddPropertyClick = () => {
    setShowAddProperty(true);
  };

  const handleCloseModal = () => {
    setShowAddProperty(false);
  };

  const handleSignOut = () => {
    signOut({ callbackUrl: "/signin" });
  };

  return (
    <div className="flex h-screen bg-gray-100 relative">
      {/* Sidebar */}
      <Sidebar />

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {/* Top Bar */}
        <TopBar onAddPropertyClick={handleAddPropertyClick} onSignOut={handleSignOut} />

        {/* Dashboard Content */}
        <main className="flex-1 overflow-y-auto p-6 grid grid-cols-1 lg:grid-cols-3 gap-6">
          <section className="col-span-2 space-y-6">
            <OverviewPanel />
            <PerformanceCharts />
            <InquiriesPanel />
            <PropertyList />
          </section>

          <section className="space-y-6">
            <FloatingAIChat />
            {/* Other panels like ComplaintsPanel, RatingsPanel, CalendarWidget can be added here */}
          </section>
        </main>
      </div>

      {/* Add Property Modal */}
      {showAddProperty && (
        <div className="fixed inset-0 bg-black bg-opacity-40 backdrop-blur-sm z-50 flex items-center justify-center">
          <div className="bg-white rounded-xl shadow-lg w-full max-w-2xl p-6 relative">
            <button
              onClick={handleCloseModal}
              className="absolute top-4 right-4 text-gray-400 hover:text-red-500 text-xl"
            >
              &times;
            </button>
            <AddPropertyCard onClose={handleCloseModal} />
          </div>
        </div>
      )}
    </div>
  );
};

export default SellerDashboard;
