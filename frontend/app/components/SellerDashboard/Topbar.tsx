// components/TopBar.tsx
type TopBarProps = {
  onAddPropertyClick: () => void;
  onSignOut: () => void;
};

const TopBar = ({ onAddPropertyClick, onSignOut }: TopBarProps) => {
  return (
    <div className="sticky top-0 bg-white shadow z-10 flex items-center justify-between px-6 py-4 border-b">
      <div className="flex items-center gap-4">
        <span className="text-xl font-bold text-gray-800">Seller Dashboard</span>
        <input
          type="text"
          placeholder="Search properties..."
          className="border px-3 py-1 rounded-lg text-sm"
        />
      </div>

      <div className="flex items-center gap-4">
        <button
          onClick={onAddPropertyClick}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-medium"
        >
          + Add Property
        </button>

        <div className="text-gray-600">👤 Riaz</div>
        <div className="text-gray-400 cursor-pointer">🔔</div>

        <button
          onClick={onSignOut}
          className="text-sm text-red-500 font-medium hover:underline"
        >
          Sign Out
        </button>
      </div>
    </div>
  );
};

export default TopBar;
