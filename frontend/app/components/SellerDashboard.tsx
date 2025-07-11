'use client';

import { useEffect, useRef, useState } from "react";
import { useSession, signOut } from "next-auth/react";
import TopBar from "./SellerDashboard/Topbar";
import OverviewPanel from "./SellerDashboard/OverviewPanel";
import PropertyList from "./SellerDashboard/PropertyList";
import FloatingAIChat from "./SellerDashboard/FloatingAIChat";
import AddPropertyCard from "./SellerDashboard/AddPropertyCard";
import ManagePropertiesCard from "./SellerDashboard/ManagePropertiesCard";

const SellerDashboard = () => {
  const { data: session } = useSession();
  const [showAddProperty, setShowAddProperty] = useState(false);
  const socketRef = useRef<WebSocket | null>(null);

  const [properties, setProperties] = useState([]);
  const [showUpdatePropertyModal, setShowUpdatePropertyModal] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const fetchProperties = async () => {
    try {
      const res = await fetch("http://localhost:8000/api/properties/me", {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${session?.user?.accessToken}`,
        },
      });
      if (!res.ok) throw new Error("Failed to fetch properties");
      const data = await res.json();
      setProperties(data);
    } catch (err: any) {
      setError(err.message || "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (session?.user?.accessToken) {
      fetchProperties();
    }
  }, [session]);

  const handleAddPropertyClick = () => {
    setShowAddProperty(true);
  };

  const handleCloseModal = () => {
    setShowAddProperty(false);
  };

  const handleSignOut = () => {
    signOut({ callbackUrl: "/signin" });
  };

  useEffect(() => {
    const token = session?.user.accessToken;
    if (!token) return;

    if (socketRef.current) {
      if (socketRef.current.readyState === WebSocket.OPEN && socketRef.current.url.includes(`token=${token}`)) {
        return;
      } else {
        socketRef.current.close();
        socketRef.current = null;
      }
    }

    const socket = new WebSocket(`ws://localhost:8000/ws?token=${token}`);
    socketRef.current = socket;

    let heartbeatInterval: NodeJS.Timeout;

    socket.onopen = () => {
      console.log("✅ WebSocket connected");
      heartbeatInterval = setInterval(() => {
        if (socket.readyState === WebSocket.OPEN) {
          socket.send("ping");
        }
      }, 30000);
    };

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      console.log("📨 WebSocket received:", data);

      if (data.type === "open_add_property_modal") {
        setShowAddProperty(true);
      } else if (data.type === "moderation_updated") {
        console.log("🔄 Moderation update received:", data);
        fetchProperties();  // Re-fetch to reflect updated status/review
      } else if (data.type === "open_update_properties_modal") {
        console.log("🔄 Update properties modal opened:", data);
        setShowUpdatePropertyModal(true);
        // You can pass the property data to the modal if needed
      }
    };
    socket.onerror = (err) => {
      if (process.env.NODE_ENV === 'development' && socket.readyState === WebSocket.CLOSED) {
        console.warn("⚠️ WebSocket error during development HMR");
      } else {
        console.error("❌ WebSocket error:", err);
      }
    };

    socket.onclose = () => {
      console.log("❌ WebSocket disconnected");
      clearInterval(heartbeatInterval);
      socketRef.current = null;
    };

    return () => {
      if (socket.readyState === WebSocket.OPEN || socket.readyState === WebSocket.CONNECTING) {
        socket.close();
      }
      clearInterval(heartbeatInterval);
      socketRef.current = null;
    };
  }, [session]);

  return (
    <div className="min-h-screen bg-gray-100">
      <TopBar onAddPropertyClick={handleAddPropertyClick} onSignOut={handleSignOut} />

      <div className="w-full pt-4 px-4 py-6 sm:px-6 lg:px-6">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <section className="lg:col-span-2">
            <div className="space-y-6 max-h-[calc(100vh-8rem)] overflow-y-auto pr-2">
              <OverviewPanel properties={properties} />
              <PropertyList properties={properties} loading={loading} error={error} />
            </div>
          </section>

          <section className="lg:block space-y-6">
            <FloatingAIChat />
          </section>
        </div>
      </div>

{showAddProperty && (
  <div className="fixed inset-0 z-50 flex">
    {/* Left 2/3 Add Property Panel */}
    <div className="w-2/3 h-full bg-white shadow-2xl overflow-y-auto">
      <AddPropertyCard onClose={handleCloseModal} onPropertyAdded={fetchProperties} />
    </div>

    {/* Right 1/3 Dimmed Backdrop */}
    <div
      className="w-1/3 h-full  cursor-pointer"
      onClick={handleCloseModal}
    />
  </div>
)}

{showUpdatePropertyModal && (
  <ManagePropertiesCard
    properties={properties}
    onClose={() => setShowUpdatePropertyModal(false)}
    onEditProperty={(property) => {
      // TODO: trigger edit modal here and pass selected property
      console.log("Editing:", property);
    }}
  />
)}


    </div>
  );
};

export default SellerDashboard;
