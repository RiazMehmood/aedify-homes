'use client';

import { useSession, signOut } from "next-auth/react";
import { useRouter } from "next/navigation";
import { useEffect, useState, useRef } from "react";

type Message = {
  sender: 'user' | 'bot';
  text: string;
};

const FloatingAIChat = () => {
  const { data: session, status } = useSession();
  const router = useRouter();
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (status === "unauthenticated") {
      router.push("/signin");
    }
  }, [status]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const getBotResponse = async (userMessage: string): Promise<string> => {
    try {
      const res = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${session?.user?.accessToken}`,
        },
        body: JSON.stringify({ value: userMessage }),
      });
      const data = await res.json();
      return data.result || "No response from agent.";
    } catch (err) {
      console.error("Chat API error:", err);
      return "Error contacting the agent.";
    }
  };

  const handleSend = async (e?: React.FormEvent) => {
    e?.preventDefault();
    if (!input.trim()) return;

    const userMsg: Message = { sender: 'user', text: input };
    setMessages((prev) => [...prev, userMsg]);
    setInput('');

    const botReply = await getBotResponse(input);
    setMessages((prev) => [...prev, { sender: 'bot', text: botReply }]);
  };

  return (
    <div className="flex flex-col bg-[#f7f7f8] rounded-xl shadow border h-[600px] overflow-hidden">
      {/* Scrollable Messages Area */}
      <div className="flex-1 overflow-y-auto px-4 py-6 space-y-4 bg-white">
        {messages.map((msg, idx) => (
          <div key={idx} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div
              className={`px-4 py-3 rounded-2xl max-w-[80%] shadow-sm text-sm whitespace-pre-wrap ${
                msg.sender === 'user'
                  ? 'bg-blue-600 text-white rounded-br-none'
                  : 'bg-gray-100 text-gray-900 border rounded-bl-none'
              }`}
            >
              {msg.text}
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area (non-sticky) */}
      <form
        onSubmit={handleSend}
        className="bg-white border-t flex items-center gap-2 px-4 py-3"
      >
        <input
          type="text"
          placeholder="Send a message..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          className="flex-1 px-4 py-2 rounded-full border border-gray-300 shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white"
        />
        <button
          type="submit"
          className="px-4 py-2 bg-blue-600 text-white font-medium rounded-full hover:bg-blue-700 transition"
        >
          Send
        </button>
      </form>
    </div>
  );
};

export default FloatingAIChat;
