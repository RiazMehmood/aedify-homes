// components/SellerDashboard/ImageUpload.tsx
'use client';

import React from 'react';

type Props = {
  images: string[];
  onUpload: (urls: string[]) => void;
  accessToken: string;
};

const ImageUpload: React.FC<Props> = ({ images, onUpload, accessToken }) => {
  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (!files || files.length === 0) return;

    const uploadedUrls: string[] = [];

    for (const file of Array.from(files)) {
      const formData = new FormData();
      formData.append('file', file);

      const res = await fetch('http://localhost:8000/api/upload', {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
        body: formData,
      });

      const data = await res.json();
      if (res.ok) {
        uploadedUrls.push(data.url);
      } else {
        alert('❌ Failed to upload image');
      }
    }

    onUpload([...images, ...uploadedUrls]);
  };

  return (
    <div>
      {images?.length > 0 && (
        <div className="flex flex-wrap gap-2 mb-4">
          {images.map((url, idx) => (
            <img
              key={idx}
              src={url}
              alt={`Uploaded ${idx}`}
              className="w-24 h-24 object-cover rounded border shadow-sm"
            />
          ))}
        </div>
      )}

      <label
        htmlFor="imageUpload"
        className="block w-full p-6 text-center text-sm text-gray-500 bg-white border-2 border-dashed border-gray-300 rounded-lg cursor-pointer hover:border-blue-400 hover:text-blue-500 transition"
      >
        <svg
          className="mx-auto mb-2 w-8 h-8 text-gray-400"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M3 15a4 4 0 014-4h1m4 0h1a4 4 0 014 4m0 0v4m0-4l-4 4m0-4l-4 4"
          />
        </svg>
        <span className="block font-medium">Click to upload</span>
        <span className="text-xs text-gray-400">or drag and drop images</span>
        <input
          id="imageUpload"
          type="file"
          accept="image/*"
          multiple
          onChange={handleUpload}
          className="hidden"
        />
      </label>
    </div>
  );
};

export default ImageUpload;
