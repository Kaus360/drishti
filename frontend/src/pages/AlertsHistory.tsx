import { useState } from 'react';

const mockAlerts = [
  { id: 1, type: 'No Helmet', date: '2026-06-20 09:12', confidence: 92 },
  { id: 2, type: 'No Vest', date: '2026-06-20 08:47', confidence: 87 },
  { id: 3, type: 'No Helmet', date: '2026-06-19 17:30', confidence: 95 },
  { id: 4, type: 'No Goggles', date: '2026-06-19 14:05', confidence: 81 },
];

function badgeColor(type: string) {
  if (type === 'No Helmet') return 'bg-red-500/10 text-red-300 border-red-500/30';
  if (type === 'No Vest') return 'bg-orange-500/10 text-orange-300 border-orange-500/30';
  return 'bg-yellow-500/10 text-yellow-300 border-yellow-500/30';
}

export default function AlertsHistory() {
  const [filterType, setFilterType] = useState('All');

  const filtered = mockAlerts.filter((a) => filterType === 'All' || a.type === filterType);

  const exportCSV = () => {
    const header = 'ID,Type,Date,Confidence\n';
    const rows = filtered.map((a) => `${a.id},${a.type},${a.date},${a.confidence}`).join('\n');
    const blob = new Blob([header + rows], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'drishti-alerts.csv';
    link.click();
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold">Alerts History</h2>
          <p className="text-slate-400 text-sm">All recorded PPE compliance violations.</p>
        </div>
        <button
          onClick={exportCSV}
          className="bg-primary/20 text-primary border border-primary/30 px-4 py-2 rounded-lg text-sm font-medium hover:bg-primary/30 transition-all"
        >
          Export to CSV
        </button>
      </div>

      <div className="flex gap-2">
        {['All', 'No Helmet', 'No Vest', 'No Goggles'].map((t) => (
          <button
            key={t}
            onClick={() => setFilterType(t)}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium border transition-all ${
              filterType === t
                ? 'bg-primary/20 text-primary border-primary/30'
                : 'bg-white/5 text-slate-400 border-white/10 hover:bg-white/10'
            }`}
          >
            {t}
          </button>
        ))}
      </div>

      <div className="bg-white/5 border border-white/10 rounded-2xl overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-white/5 text-slate-400 text-xs uppercase">
            <tr>
              <th className="text-left px-4 py-3">Type</th>
              <th className="text-left px-4 py-3">Date</th>
              <th className="text-left px-4 py-3">Confidence</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map((a) => (
              <tr key={a.id} className="border-t border-white/10">
                <td className="px-4 py-3">
                  <span className={`px-2 py-1 rounded-full text-xs border ${badgeColor(a.type)}`}>
                    {a.type}
                  </span>
                </td>
                <td className="px-4 py-3 text-slate-300">{a.date}</td>
                <td className="px-4 py-3 text-slate-300">{a.confidence}%</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
