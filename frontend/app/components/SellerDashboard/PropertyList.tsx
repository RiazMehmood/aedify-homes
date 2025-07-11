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

const PropertyList = ({
  properties,
  loading,
  error,
}: {
  properties: Property[];
  loading: boolean;
  error: string;
}) => {
  return (
    <div className="bg-white p-4 rounded-xl shadow">
      <h2 className="text-lg font-bold mb-4">🏘️ My Properties</h2>

      {loading && <p className="text-gray-500">Loading...</p>}
      {error && <p className="text-red-500">{error}</p>}

      {!loading && !error && properties.length === 0 && (
        <p className="text-gray-600">No properties found.</p>
      )}

      <div className="space-y-4">
        {properties.map((p, i) => (
          <div
            key={p.id || i}
            className="border p-3 rounded-xl flex gap-4 items-start"
          >
            {/* Image */}
            {p.images?.length > 0 ? (
              <img
                src={p.images[0]}
                alt={p.title}
                className="w-24 h-20 object-cover rounded-md"
              />
            ) : (
              <div className="w-24 h-20 bg-gray-100 rounded-md flex items-center justify-center text-gray-400 text-sm">
                No Image
              </div>
            )}

            {/* Text Info */}
            <div className="flex-1 space-y-1">
              <div className="font-semibold text-gray-800">{p.title}</div>
              <div className="text-sm text-gray-600">
                {p.price} •{" "}
                <span
                  className={`px-2 py-0.5 rounded-full text-xs font-semibold ${
                    p.status === "approved"
                      ? "bg-green-100 text-green-700"
                      : p.status === "not approved"
                      ? "bg-red-100 text-red-700"
                      : "bg-yellow-100 text-yellow-700"
                  }`}
                >
                  {p.status === "pending approval"
                    ? "Moderation Required"
                    : p.status}
                </span>
              </div>

              {/* Moderation Review or AI Review */}
              {p.status === "approved" && (
                <div className="text-sm text-blue-600 mt-1">
                  💡 <strong>AI Suggestions:</strong>{" "}
                  {p.ai_review
                    ? p.ai_review
                    : "Consider improving the title and description for better search visibility. Add more images showing the interior and front elevation."}
                </div>
              )}

              {p.status === "not approved" && p.review_comment && (
                <div className="text-sm text-red-600 mt-1">
                  ⚠️ <strong>Moderation Review:</strong> {p.review_comment}
                </div>
              )}

              {p.status === "pending approval" && (
                <div className="text-sm text-yellow-700 mt-1">
                  ⏳ <strong>Moderation Status:</strong> Waiting for review...
                </div>
              )}
            </div>

            {/* Metrics */}
            <div className="text-sm text-gray-500 text-right whitespace-nowrap">
              ⭐ {p.rating ?? "N/A"} <br /> 🔥 {p.views ?? 0} views
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default PropertyList;
