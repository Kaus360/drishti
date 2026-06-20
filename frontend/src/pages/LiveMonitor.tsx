import { useState, useEffect } from 'react';
import { API_ENDPOINTS } from '../config/api';

export default function LiveMonitor() {
  const [streamError, setStreamError] = useState(false);
  const [isLive, setIsLive] = useState(false);

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const res = await fetch(API_ENDPOINTS.health, { signal: AbortSignal.timeout(2000) });
        setIsLive(res.ok);
      } catch {
        setIsLive(false);
      }
    };
    checkHealth();
    const interval = setInterval(checkHealth, 5000);
    return () => clearInterval(interval);
  }, []);

  const violations = [
    { id: 1, label: 'No Helmet', confidence: 92 },
    { id: 2, label: 'No Vest', confidence: 87 },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold">Live Monitor</h2>
        <p className="text-slate-400 text-sm">Real-time camera feed with active detection overlay.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-4">
        <div className="lg:col-span-3 bg-black/40 border border-white/10 rounded-2xl overflow-hidden relative">
          <div className="absolute top-3 left-3 flex items-center gap-2 z-10">
            <span
              className={`w-2.5 h-2.5 rounded-full ${
                isLive ? 'bg-green-400 animate-pulse' : 'bg-red-400'
              }`}
            />
            <span className="text-xs font-medium bg-black/50 px-2 py-1 rounded">
              {isLive ? 'Camera Active' : 'Camera Offline'}
            </span>
          </div>

          <div className="aspect-video flex items-center justify-center bg-black/60">
            {!streamError ? (
              <img
                src={API_ENDPOINTS.stream}
                alt="Live camera feed"
                className="w-full h-full object-cover"
                onError={() => setStreamError(true)}
              />
            ) : (
              <div className="text-center text-slate-500">
                <p className="text-lg font-semibold mb-1">Camera Offline</p>
                <p className="text-sm">Waiting for backend connection at localhost:8000</p>
              </div>
            )}
          </div>
        </div>

        <div className="bg-white/5 border border-white/10 rounded-2xl p-4">
          <h3 className="text-xs tracking-wide text-slate-400 uppercase mb-4">Detected Violations</h3>
          <div className="space-y-3">
            {violations.map((v) => (
              <div key={v.id} className="bg-red-500/10 border border-red-500/20 rounded-xl p-3">
                <div className="flex justify-between items-center">
                  <span className="text-sm font-medium text-red-300">{v.label}</span>
                  <span className="text-xs text-slate-400">{v.confidence}%</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
