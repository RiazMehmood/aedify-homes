'use client';

import { useState } from "react";

const SellerDashboard = () => {
  const [formData, setFormData] = useState<{
    title: string;
    price: string;
    description: string;
    location: string;
    images: File[];
  }>({
    title: "",
    price: "",
    description: "",
    location: "",
    images: [],
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files || []);
    setFormData({ ...formData, images: files });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const form = new FormData();
    form.append("title", formData.title);
    form.append("price", formData.price);
    form.append("description", formData.description);
    form.append("location", formData.location);
    formData.images.forEach((img: File) => form.append("images", img));

    const res = await fetch("http://localhost:8000/properties", {
      method: "POST",
      body: form,
    });

    if (res.ok) alert("Property submitted successfully!");
    else alert("Failed to submit property.");
  };

  return (
    <main className="p-6 max-w-2xl mx-auto">
      <h2 className="text-2xl font-bold mb-4">🏡 List a Property</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input name="title" placeholder="Title" onChange={handleChange} className="w-full border p-2 rounded" required />
        <input name="price" placeholder="Price" type="number" onChange={handleChange} className="w-full border p-2 rounded" required />
        <input name="location" placeholder="Location" onChange={handleChange} className="w-full border p-2 rounded" required />
        <textarea name="description" placeholder="Description" onChange={handleChange} className="w-full border p-2 rounded" rows={4} required />
        <input type="file" accept="image/*" multiple onChange={handleImageUpload} className="w-full border p-2 rounded" />
        <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">Submit</button>
      </form>
    </main>
  );
};

export default SellerDashboard;
