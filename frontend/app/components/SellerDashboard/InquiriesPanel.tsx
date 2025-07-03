
// InquiriesPanel.tsx
const InquiriesPanel = () => {
  const inquiries = [
    { name: "Ali Khan", message: "Interested in Flat A", time: "2h ago" },
    { name: "Sara Ahmed", message: "Can I visit Villa B?", time: "5h ago" },
    { name: "Bilal", message: "Price negotiable for House C?", time: "1d ago" },
  ];

  return (
    <div className="bg-white p-4 rounded-xl shadow">
      <h2 className="text-lg font-bold mb-4">📬 Inquiries</h2>
      <ul className="space-y-3">
        {inquiries.map((inq, i) => (
          <li key={i} className="border-b pb-2">
            <div className="font-semibold text-gray-800">{inq.name}</div>
            <div className="text-sm text-gray-600">{inq.message}</div>
            <div className="text-xs text-gray-400">{inq.time}</div>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default InquiriesPanel;