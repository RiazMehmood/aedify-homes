type Property = {
  status: string;
  views: number;
  rating: number;
};

const OverviewPanel = ({ properties }: { properties: Property[] }) => {
  const total = properties.length;
  const approved = properties.filter((p) => p.status === "approved").length;
  const notApproved = properties.filter((p) => p.status === "not approved").length;
  const pending = properties.filter((p) => p.status === "pending approval").length;

  const totalViews = properties.reduce((sum, p) => sum + (p.views || 0), 0);
  const avgRating = properties.length
    ? (properties.reduce((sum, p) => sum + (p.rating || 0), 0) / properties.length).toFixed(1)
    : "N/A";

  const recentViews = Math.floor(totalViews * 0.25); // Customize if needed

  return (
    <div className="space-y-6">
      {/* 🔔 Subscription & Analytics */}
      <div className="bg-white p-4 rounded-xl shadow">
        <h2 className="text-lg font-bold mb-4">🔔 Subscription & Analytics</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <OverviewCard label="Subscription" value="Pro Plan 🪙" />
          <OverviewCard label="Total Views" value={`${totalViews} 👁️`} />
          <OverviewCard label="Recent Views" value={`${recentViews} 👀`} />
          <OverviewCard label="Avg. Rating" value={`${avgRating} ⭐`} />
        </div>
      </div>

      {/* 🏘️ Property Stats */}
      <div className="bg-white p-4 rounded-xl shadow">
        <h2 className="text-lg font-bold mb-4">🏘️ Property Status</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <OverviewCard label="Total Properties" value={String(total)} />
          <OverviewCard label="Approved" value={String(approved)} />
          <OverviewCard label="Not Approved" value={String(notApproved)} />
          <OverviewCard label="Pending" value={String(pending)} />
        </div>
      </div>
    </div>
  );
};

const OverviewCard = ({ label, value }: { label: string; value: string }) => (
  <div className="p-3 bg-gray-50 border rounded-xl text-center">
    <div className="text-gray-500 text-sm">{label}</div>
    <div className="text-xl font-semibold text-gray-800">{value}</div>
  </div>
);

export default OverviewPanel;
