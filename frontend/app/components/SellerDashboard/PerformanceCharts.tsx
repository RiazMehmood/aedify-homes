
// PerformanceCharts.tsx
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

const data = [
  { name: 'Flat A', views: 240 },
  { name: 'Villa B', views: 180 },
  { name: 'House C', views: 320 },
  { name: 'Plot D', views: 90 },
];

const PerformanceCharts = () => {
  return (
    <div className="bg-white p-4 rounded-xl shadow">
      <h2 className="text-lg font-bold mb-4">📈 Performance Analytics</h2>
      <ResponsiveContainer width="100%" height={250}>
        <BarChart data={data}>
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="views" fill="#3b82f6" radius={[8, 8, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default PerformanceCharts;
