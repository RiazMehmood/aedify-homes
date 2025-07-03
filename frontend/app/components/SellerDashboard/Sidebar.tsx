const Sidebar = () => {
  return (
    <aside className="w-64 bg-white border-r p-6 hidden lg:block sticky top-0 h-screen">
      <nav className="space-y-4 text-sm font-medium text-gray-700">
        <a href="#" className="block hover:text-blue-600">🏠 Dashboard</a>
        <a href="#" className="block hover:text-blue-600">🏘️ My Listings</a>
        <a href="#" className="block hover:text-blue-600">✍️ Add Property</a>
        <a href="#" className="block hover:text-blue-600">📢 Complaints</a>
        <a href="#" className="block hover:text-blue-600">💬 Chat Support</a>
        <a href="#" className="block hover:text-blue-600">📊 Insights & AI Tools</a>
        <a href="#" className="block hover:text-blue-600">⚙️ Settings</a>
      </nav>
    </aside>
  );
};

export default Sidebar;
