'use client';

import { useSession, signOut } from "next-auth/react";
import { useRouter } from "next/navigation";
import ChatGuard from "../components/ChatGuard";
import SellerDashboard from "../components/SellerDashboard";
import CustomerChat from "../components/CustomerChat";



const ChatPage = () => {
  const { data: session, status } = useSession();
  const router = useRouter();
  console.log("Session data:", session);

  
  if (status === "loading") {
    return <div className="p-6">Loading...</div>;
  }

    const role = session?.user?.role;
    console.log("User role:", role);

  return (
    <ChatGuard>
      {role === "seller" ? <SellerDashboard /> : <CustomerChat />}
    
    </ChatGuard>
  );
};

export default ChatPage;
