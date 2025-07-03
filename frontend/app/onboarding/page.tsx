'use client';


import React, { useState } from 'react';
import { useSession,signIn } from 'next-auth/react';
import { useRouter } from 'next/navigation';


const OnboardingPage: React.FC = () => {
    const router = useRouter();
    const { data: session } = useSession();
  const [form, setForm] = useState({
    phone: '',
    whatsapp: '',
    cnic: '',
    city: '',
    role: 'customer',
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setForm((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

 const handleSubmit = async (e: React.FormEvent) => {
  e.preventDefault();

  try {
    const res = await fetch("http://localhost:8000/api/auth/onboarding", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
    ...form,
    email: session?.user?.email,
  }),
    });

    const data = await res.json();

    if (res.ok) {
       await fetch("/api/auth/session?update=true");
      // ✅ Navigate to /chat
      router.push("/chat");
    } else {
      alert(data.detail || "Failed to complete onboarding.");
    }
  } catch (error) {
    console.error("Onboarding error:", error);
    alert("Something went wrong. Try again.");
  }
};



  return (
    <main className="min-h-screen bg-gray-50 flex items-center justify-center px-4 py-12">
      <div className="bg-white shadow-xl rounded-2xl p-8 max-w-lg w-full">
        <h1 className="text-3xl font-bold text-gray-800 mb-2">Welcome to Onboarding</h1>
        <p className="text-gray-500 mb-6">Please follow the steps to complete your onboarding process.</p>

        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label htmlFor="phone" className="block text-sm font-medium text-gray-700 mb-1">
              Phone Number
            </label>
            <input
              type="tel"
              name="phone"
              id="phone"
              value={form.phone}
              onChange={handleChange}
              required
              className="w-full p-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-yellow-400"
            />
          </div>

          <div>
            <label htmlFor="whatsapp" className="block text-sm font-medium text-gray-700 mb-1">
              WhatsApp Number
            </label>
            <input
              type="tel"
              name="whatsapp"
              id="whatsapp"
              value={form.whatsapp}
              onChange={handleChange}
              required
              className="w-full p-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-yellow-400"
            />
          </div>

          <div>
            <label htmlFor="cnic" className="block text-sm font-medium text-gray-700 mb-1">
              CNIC
            </label>
            <input
              type="text"
              name="cnic"
              id="cnic"
              value={form.cnic}
              onChange={handleChange}
              required
              className="w-full p-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-yellow-400"
            />
          </div>

          <div>
            <label htmlFor="city" className="block text-sm font-medium text-gray-700 mb-1">
              City
            </label>
            <input
              type="text"
              name="city"
              id="city"
              value={form.city}
              onChange={handleChange}
              required
              className="w-full p-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-yellow-400"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Role</label>
            <div className="flex gap-6">
              <label className="flex items-center gap-2 text-sm font-medium text-gray-700">
                <input
                  type="radio"
                  name="role"
                  value="customer"
                  checked={form.role === 'customer'}
                  onChange={handleChange}
                  className="text-yellow-500"
                />
                Customer
              </label>
              <label className="flex items-center gap-2 text-sm font-medium text-gray-700">
                <input
                  type="radio"
                  name="role"
                  value="seller"
                  checked={form.role === 'seller'}
                  onChange={handleChange}
                  className="text-yellow-500"
                />
                Seller
              </label>
            </div>
          </div>

          <button
            type="submit"
            className="w-full p-3 mt-4 bg-yellow-400 text-gray-900 font-bold rounded-lg hover:bg-yellow-500 transition-colors"
          >
            Submit
          </button>
        </form>
      </div>
    </main>
  );
};

export default OnboardingPage;
