// PropertyList.tsx
const PropertyList = () => {
  const properties = [
    { title: "Flat A - DHA Phase 6", price: "PKR 75,000", status: "Active", views: 120, rating: 4.6 },
    { title: "Villa B - Bahria Town", price: "PKR 2.5 Cr", status: "Inactive", views: 60, rating: 4.2 },
    { title: "Plot C - Johar Town", price: "PKR 80 Lac", status: "Active", views: 210, rating: 4.9 },
  ];

  return (
    <div className="bg-white p-4 rounded-xl shadow">
      <h2 className="text-lg font-bold mb-4">🏘️ My Properties</h2>
      <div className="space-y-4">
        {properties.map((p, i) => (
          <div key={i} className="border p-3 rounded-xl flex justify-between items-center">
            <div>
              <div className="font-semibold text-gray-800">{p.title}</div>
              <div className="text-sm text-gray-600">{p.price} • {p.status}</div>
            </div>
            <div className="text-sm text-gray-500 text-right">
              ⭐ {p.rating} <br /> 🔥 {p.views} views
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default PropertyList;
