import { useEffect, useState } from 'react';
import { API_ENDPOINTS } from '../config/api';
import { formatViolationType } from '../utils/labels';

function badgeColor(type: string) {
  const normalized = type.toLowerCase();
  if (normalized.includes('helmet') || normalized.includes('hardhat')) {
    return 'bg-red-500/10 text-red-300 border-red-500/30';
  }
  if (normalized.includes('vest')) {
    return 'bg-orange-500/10 text-orange-300 border-orange-500/30';
  }
  return 'bg-yellow-500/10 text-yellow-300 border-yellow-500/30';
}

export default function AlertsHistory() {
  const [filterType, setFilterType] = useState('All');
  const [alerts, setAlerts] = useState<any[]>([]);

  useEffect(() => {
    const fetchAlerts = async () => {
      try {
        const res = await fetch(API_ENDPOINTS.alertsLatest, { signal: AbortSignal.timeout(2000) });
        if (!res.ok) {
          return;
        }

        const data = await res.json();
        setAlerts(data.alerts ?? []);
      } catch {
        // Keep the last successful alert list during transient polling failures.
      }
    };

    fetchAlerts();
    const interval = setInterval(fetchAlerts, 3000);
    return () => clearInterval(interval);
  }, []);

  const filtered = alerts.filter(
    (a) => filterType === 'All' || formatViolationType(a.type) === filterType
  );

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
        {['All', 'No Helmet', 'No Vest', 'No Goggles', 'No Mask'].map((t) => (
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
            {filtered.map((a) => {
              const displayType = formatViolationType(a.type);
              return (
                <tr key={a.id} className="border-t border-white/10">
                  <td className="px-4 py-3">
                    <span className={`px-2 py-1 rounded-full text-xs border ${badgeColor(displayType)}`}>
                      {displayType}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-slate-300">{a.date}</td>
                  <td className="px-4 py-3 text-slate-300">{a.confidence}%</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
