import { Link, useLocation } from 'react-router-dom';
import { LayoutDashboard, Video, AlertTriangle, BarChart3, Settings as SettingsIcon } from 'lucide-react';
import { useState, useEffect } from 'react';
import { API_ENDPOINTS } from '../config/api';

const navItems = [
  { path: '/', label: 'Dashboard', icon: LayoutDashboard },
  { path: '/live', label: 'Live Monitor', icon: Video },
  { path: '/alerts', label: 'Alerts History', icon: AlertTriangle },
  { path: '/analytics', label: 'Analytics', icon: BarChart3 },
  { path: '/settings', label: 'Settings', icon: SettingsIcon },
];

export default function Layout({ children }: { children: React.ReactNode }) {
  const location = useLocation();
  const [now, setNow] = useState(new Date());
  const [isOnline, setIsOnline] = useState(false);

  useEffect(() => {
    const timer = setInterval(() => setNow(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const res = await fetch(API_ENDPOINTS.health, { signal: AbortSignal.timeout(2000) });
        setIsOnline(res.ok);
      } catch {
        setIsOnline(false);
      }
    };

    checkHealth();
    const interval = setInterval(checkHealth, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="flex min-h-screen bg-background text-white">
      <aside className="w-64 bg-black/30 backdrop-blur-xl border-r border-white/10 flex flex-col p-4">
        <div className="flex items-center gap-2 mb-8 px-2">
          <div className="w-8 h-8 rounded bg-primary flex items-center justify-center font-bold">D</div>
          <span className="font-bold text-lg tracking-wide">DRISHTI</span>
        </div>
        <nav className="flex flex-col gap-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            const active = location.pathname === item.path;
            return (
              <Link
                key={item.path}
                to={item.path}
                className={`flex items-center gap-3 px-3 py-2 rounded-lg transition-all ${
                  active
                    ? 'bg-primary/20 text-primary shadow-[0_0_12px_rgba(249,115,22,0.4)]'
                    : 'text-slate-300 hover:bg-white/5'
                }`}
              >
                <Icon size={18} />
                <span className="text-sm">{item.label}</span>
              </Link>
            );
          })}
        </nav>
      </aside>

      <div className="flex-1 flex flex-col">
        <header className="flex items-center justify-between px-6 py-4 border-b border-white/10 bg-black/20 backdrop-blur-xl">
          <div>
            <h1 className="font-bold tracking-wide">DRISHTI</h1>
            <p className="text-xs text-slate-400">See Every Risk. Stop Every Accident.</p>
          </div>
          <div className="flex items-center gap-4">
            <span className="text-sm text-slate-300">
              {now.toLocaleDateString()} {now.toLocaleTimeString()}
            </span>
            <span
              className={`px-3 py-1 rounded-full text-xs font-semibold border ${
                isOnline
                  ? 'bg-green-500/10 text-green-400 border-green-500/30'
                  : 'bg-red-500/10 text-red-400 border-red-500/30'
              }`}
            >
              {isOnline ? 'ONLINE' : 'OFFLINE'}
            </span>
          </div>
        </header>
        <main className="flex-1 p-6 overflow-y-auto">{children}</main>
      </div>
    </div>
  );
}
