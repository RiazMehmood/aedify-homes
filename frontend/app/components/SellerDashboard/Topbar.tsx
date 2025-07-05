// components/TopBar.tsx
type TopBarProps = {
  onAddPropertyClick: () => void;
  onSignOut: () => void;
};

const TopBar = ({ onAddPropertyClick, onSignOut }: TopBarProps) => {
  return (
    <div className="sticky top-0 bg-white shadow z-10 border-b py-3 px-4">
      <div className="max-w-screen-2xl mx-auto flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
        
        {/* Top row for small screens: title + Sign Out */}
        <div className="flex justify-between items-center md:hidden">
          <span className="text-base font-semibold text-gray-800">
            Aedify Homes Seller Dashboard
          </span>
          <button
            onClick={onSignOut}
            className="text-sm text-red-500 font-medium hover:underline"
          >
            Sign Out
          </button>
        </div>

        {/* Left Section: Title + Search */}
        <div className="w-full md:flex md:items-center md:gap-4">
          {/* Title for medium and larger screens */}
          <span className="hidden md:inline text-xl font-semibold text-gray-800">
            Aedify Homes Seller Dashboard
          </span>

          {/* Search bar */}
          <input
            type="text"
            placeholder="Search properties..."
            className="border px-3 py-1 rounded-lg text-sm w-full md:w-64 mt-2 md:mt-0"
          />
        </div>

        {/* Right Section: Add button, icons, Sign Out */}
        <div className="w-full flex flex-wrap md:flex-nowrap items-center justify-between md:justify-end gap-3">
          {/* Add Property Button */}
          <button
            onClick={onAddPropertyClick}
            className="bg-blue-600 text-white px-3 py-2 rounded-lg text-sm font-medium w-fit"
          >
            <span className="md:hidden text-lg">+</span>
            <span className="hidden md:inline">+ Add Property</span>
          </button>

          <div className="text-gray-600 text-sm md:text-base">👤 Riaz</div>
          <div className="text-gray-400 cursor-pointer text-lg">🔔</div>

          {/* Sign Out for md+ screens */}
          <button
            onClick={onSignOut}
            className="hidden md:block text-md text-red-500 font-medium hover:underline"
          >
            Sign Out
          </button>
        </div>
      </div>
    </div>
  );
};

export default TopBar;
