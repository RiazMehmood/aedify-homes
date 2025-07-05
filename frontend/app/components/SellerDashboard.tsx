'use client';

import { useState } from "react";
import { signOut } from "next-auth/react";
import TopBar from "./SellerDashboard/Topbar";
import OverviewPanel from "./SellerDashboard/OverviewPanel";
import PropertyList from "./SellerDashboard/PropertyList";
import FloatingAIChat from "./SellerDashboard/FloatingAIChat";
import AddPropertyCard from "./SellerDashboard/AddPropertyCard";

const SellerDashboard = () => {
  const [showAddProperty, setShowAddProperty] = useState(false);

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
    <div className="min-h-screen bg-gray-100">
      {/* Sticky TopBar remains unchanged */}
      <TopBar onAddPropertyClick={handleAddPropertyClick} onSignOut={handleSignOut} />

      {/* Main Content pushed below sticky TopBar */}
      <div className="w-full pt-4 px-4 py-6 sm:px-6 lg:px-6">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column */}
          <section className="lg:col-span-2 space-y-6">
            <OverviewPanel />
            <PropertyList />
          </section>

          {/* Right Column (AI Chat only visible on large screens) */}
          <section className="lg:block space-y-6">
            <FloatingAIChat />
          </section>
        </div>
      </div>

      {/* Add Property Modal */}
      {showAddProperty && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-40 backdrop-blur-sm px-4">
          <div className="relative bg-white rounded-xl shadow-lg w-full max-w-2xl p-6">
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
