import { BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const hourlyViolations = [
  { hour: '08:00', violations: 3 },
  { hour: '09:00', violations: 5 },
  { hour: '10:00', violations: 2 },
  { hour: '11:00', violations: 7 },
  { hour: '12:00', violations: 1 },
  { hour: '13:00', violations: 4 },
];

const complianceOverTime = [
  { day: 'Mon', rate: 72 },
  { day: 'Tue', rate: 75 },
  { day: 'Wed', rate: 70 },
  { day: 'Thu', rate: 80 },
  { day: 'Fri', rate: 78 },
  { day: 'Sat', rate: 82 },
  { day: 'Sun', rate: 78.4 },
];

const violationBreakdown = [
  { name: 'No Helmet', value: 45 },
  { name: 'No Vest', value: 30 },
  { name: 'No Goggles', value: 25 },
];

const COLORS = ['#f97316', '#06b6d4', '#facc15'];

function ChartCard({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="bg-white/5 border border-white/10 rounded-2xl p-5">
      <h3 className="text-xs tracking-wide text-slate-400 uppercase mb-4">{title}</h3>
      {children}
    </div>
  );
}

export default function Analytics() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold">Analytics</h2>
        <p className="text-slate-400 text-sm">Trends and breakdowns of PPE compliance data.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <ChartCard title="Violations Per Hour">
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={hourlyViolations}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
              <XAxis dataKey="hour" stroke="#94a3b8" fontSize={12} />
              <YAxis stroke="#94a3b8" fontSize={12} />
              <Tooltip contentStyle={{ background: '#0a0f1e', border: '1px solid #334155' }} />
              <Bar dataKey="violations" fill="#f97316" radius={[6, 6, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>

        <ChartCard title="Compliance Rate Over Time">
          <ResponsiveContainer width="100%" height={250}>
            <LineChart data={complianceOverTime}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
              <XAxis dataKey="day" stroke="#94a3b8" fontSize={12} />
              <YAxis stroke="#94a3b8" fontSize={12} />
              <Tooltip contentStyle={{ background: '#0a0f1e', border: '1px solid #334155' }} />
              <Line type="monotone" dataKey="rate" stroke="#06b6d4" strokeWidth={2} dot={{ r: 4 }} />
            </LineChart>
          </ResponsiveContainer>
        </ChartCard>

        <ChartCard title="Violation Type Breakdown">
          <ResponsiveContainer width="100%" height={250}>
            <PieChart>
              <Pie data={violationBreakdown} dataKey="value" nameKey="name" outerRadius={90} label>
                {violationBreakdown.map((_, i) => (
                  <Cell key={i} fill={COLORS[i % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip contentStyle={{ background: '#0a0f1e', border: '1px solid #334155' }} />
            </PieChart>
          </ResponsiveContainer>
        </ChartCard>
      </div>
    </div>
  );
}
