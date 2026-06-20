import { useEffect, useState } from 'react';
import { AlertTriangle, ShieldCheck, Camera, Users } from 'lucide-react';
import { motion } from 'framer-motion';

function StatCard({ icon: Icon, label, value, suffix, trend, color }: any) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white/5 border border-white/10 rounded-2xl p-5 backdrop-blur-xl hover:shadow-[0_0_20px_rgba(249,115,22,0.15)] transition-all"
    >
      <div className="flex items-center justify-between mb-3">
        <span className="text-xs tracking-wide text-slate-400 uppercase">{label}</span>
        <div className={`w-9 h-9 rounded-full flex items-center justify-center ${color}`}>
          <Icon size={16} />
        </div>
      </div>
      <div className="text-3xl font-bold">
        {value}
        {suffix && <span className="text-base text-slate-400 ml-1">{suffix}</span>}
      </div>
      <div className="text-xs text-slate-400 mt-1">{trend}</div>
    </motion.div>
  );
}

export default function Dashboard() {
  const [compliance, setCompliance] = useState(0);

  useEffect(() => {
    const target = 78.4;
    let current = 0;
    const step = target / 30;
    const interval = setInterval(() => {
      current += step;
      if (current >= target) {
        current = target;
        clearInterval(interval);
      }
      setCompliance(Number(current.toFixed(1)));
    }, 20);
    return () => clearInterval(interval);
  }, []);

  const circumference = 2 * Math.PI * 70;
  const offset = circumference - (compliance / 100) * circumference;

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold">Mission Control</h2>
        <p className="text-slate-400 text-sm">Real-time PPE compliance overview across all monitored zones.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          icon={AlertTriangle}
          label="Violations Today"
          value={12}
          trend="Down 12% vs yesterday"
          color="bg-red-500/10 text-red-400"
        />
        <StatCard
          icon={ShieldCheck}
          label="Compliance Rate"
          value={78.4}
          suffix="%"
          trend="Up 4% vs yesterday"
          color="bg-green-500/10 text-green-400"
        />
        <StatCard
          icon={Camera}
          label="Active Cameras"
          value={8}
          trend="No change vs yesterday"
          color="bg-cyan-500/10 text-cyan-400"
        />
        <StatCard
          icon={Users}
          label="Workers Monitored"
          value={142}
          trend="Up 6% vs yesterday"
          color="bg-orange-500/10 text-orange-400"
        />
      </div>

      <div className="bg-white/5 border border-white/10 rounded-2xl p-6 backdrop-blur-xl">
        <h3 className="text-xs tracking-wide text-slate-400 uppercase mb-4">Site Compliance</h3>
        <div className="flex justify-center">
          <svg width="180" height="180" viewBox="0 0 180 180">
            <circle cx="90" cy="90" r="70" stroke="#1e293b" strokeWidth="14" fill="none" />
            <circle
              cx="90"
              cy="90"
              r="70"
              stroke="#f97316"
              strokeWidth="14"
              fill="none"
              strokeLinecap="round"
              strokeDasharray={circumference}
              strokeDashoffset={offset}
              transform="rotate(-90 90 90)"
              style={{ transition: 'stroke-dashoffset 0.3s ease' }}
            />
            <text x="90" y="95" textAnchor="middle" fontSize="28" fontWeight="bold" fill="white">
              {compliance}%
            </text>
          </svg>
        </div>
      </div>
    </div>
  );
}
