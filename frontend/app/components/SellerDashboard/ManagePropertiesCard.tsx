"use client";

import { useState } from "react";

type Property = {
  id: string;
  title: string;
  price: string | number;
  images: string[];
  status: "approved" | "not approved" | "pending approval";
  views: number;
  rating: number;
  review_comment?: string;
  ai_review?: string;
};

type Props = {
  properties: Property[];
  onClose: () => void;
  onEditProperty: (property: Property) => void;
};

const ManagePropertiesCard = ({ properties, onClose, onEditProperty }: Props) => {
  const [filter, setFilter] = useState<"approved" | "not approved" | "pending approval">("not approved");
  const filtered = properties.filter((p) => p.status === filter);

  const tabs = [
    { key: "approved", label: "✅ Approved" },
    { key: "not approved", label: "❌ Not Approved" },
    { key: "pending approval", label: "⏳ Pending" },
  ] as const;

  return (
    <div className="fixed inset-0 z-50 flex">
      {/* Panel */}
      <div className="w-full md:w-2/3 bg-white shadow-2xl h-full overflow-y-auto p-6">
        {/* Header */}
        <div className="flex justify-between items-center border-b pb-3 mb-4">
          <h2 className="text-xl font-semibold text-gray-800">🛠️ Manage Your Properties</h2>
          <button onClick={onClose} className="text-gray-500 hover:text-gray-700 text-sm">✖ Close</button>
        </div>

        {/* Filter Tabs */}
        <div className="flex flex-wrap gap-2 mb-6">
          {tabs.map((tab) => (
            <button
              key={tab.key}
              onClick={() => setFilter(tab.key)}
              className={`px-4 py-1.5 rounded-full text-sm font-medium border ${
                filter === tab.key
                  ? "bg-blue-600 text-white border-blue-600"
                  : "bg-gray-50 text-gray-600 hover:bg-gray-100"
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>

        {/* Property List */}
        {filtered.length === 0 ? (
          <div className="text-gray-500 text-center py-10 text-sm">No properties found for this status.</div>
        ) : (
          <div className="space-y-4">
            {filtered.map((p) => (
              <div key={p.id} className="bg-white border border-gray-200 rounded-xl p-4 shadow-sm">
                <div className="flex gap-4">
                  {/* Image */}
                  {p.images?.[0] ? (
                    <img
                      src={p.images[0]}
                      alt={p.title}
                      className="w-24 h-20 object-cover rounded-md border"
                    />
                  ) : (
                    <div className="w-24 h-20 bg-gray-100 rounded-md flex items-center justify-center text-sm text-gray-400">
                      No Image
                    </div>
                  )}

                  {/* Info */}
                  <div className="flex-1 space-y-1">
                    <div className="text-lg font-semibold text-gray-800">{p.title}</div>
                    <div className="text-sm text-gray-500">
                      <span className="mr-2 font-medium">Status:</span>
                      <span className={
                        p.status === "approved"
                          ? "text-green-600"
                          : p.status === "not approved"
                          ? "text-red-600"
                          : "text-yellow-600"
                      }>
                        {p.status}
                      </span>
                    </div>

                    {p.status === "not approved" && p.review_comment && (
                      <div className="text-sm text-red-600 mt-1">
                        ⚠️ <strong>Moderation Review:</strong> {p.review_comment}
                      </div>
                    )}

                    {p.status === "approved" && p.ai_review && (
                      <div className="text-sm text-blue-600 mt-1">
                        💡 <strong>AI Suggestions:</strong> {p.ai_review}
                      </div>
                    )}
                  </div>

                  {/* Action */}
                  <div className="flex items-center">
                    <button
                      onClick={() => onEditProperty(p)}
                      className="px-4 py-1.5 bg-blue-600 hover:bg-blue-700 text-white text-sm rounded-md"
                    >
                      ✏️ Edit
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Backdrop */}
      <div
        className="hidden md:block w-1/3 bg-black/20 cursor-pointer"
        onClick={onClose}
      />
    </div>
  );
};

export default ManagePropertiesCard;
