// OverviewPanel.tsx
const OverviewPanel = () => {
  return (
    <div className="bg-white p-4 rounded-xl shadow">
      <h2 className="text-lg font-bold mb-4">📊 Property Overview</h2>
      <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
        <OverviewCard label="Total Properties" value="12" />
        <OverviewCard label="Active Listings" value="8" />
        <OverviewCard label="Pending Approval" value="2" />
        <OverviewCard label="Watched" value="150 ❤️" />
        <OverviewCard label="Avg. Rating" value="4.5 ⭐" />
        <OverviewCard label="Recent Views" value="860 👀" />
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
