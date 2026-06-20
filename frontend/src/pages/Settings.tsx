import { useState, useEffect } from 'react';

export default function Settings() {
  const [camera, setCamera] = useState(() => localStorage.getItem('drishti_camera') || 'default');
  const [threshold, setThreshold] = useState(() => Number(localStorage.getItem('drishti_threshold')) || 75);
  const [soundEnabled, setSoundEnabled] = useState(() => localStorage.getItem('drishti_sound') === 'true');

  useEffect(() => {
    localStorage.setItem('drishti_camera', camera);
  }, [camera]);

  useEffect(() => {
    localStorage.setItem('drishti_threshold', String(threshold));
  }, [threshold]);

  useEffect(() => {
    localStorage.setItem('drishti_sound', String(soundEnabled));
  }, [soundEnabled]);

  return (
    <div className="space-y-6 max-w-xl">
      <div>
        <h2 className="text-2xl font-bold">Settings</h2>
        <p className="text-slate-400 text-sm">Configure detection and alert preferences.</p>
      </div>

      <div className="bg-white/5 border border-white/10 rounded-2xl p-5 space-y-2">
        <label className="text-xs tracking-wide text-slate-400 uppercase">Camera Source</label>
        <select
          value={camera}
          onChange={(e) => setCamera(e.target.value)}
          className="w-full bg-black/40 border border-white/10 rounded-lg px-3 py-2 text-sm"
        >
          <option value="default">Default Webcam</option>
          <option value="external">External Camera</option>
          <option value="rtsp">RTSP Stream</option>
        </select>
      </div>

      <div className="bg-white/5 border border-white/10 rounded-2xl p-5 space-y-3">
        <div className="flex justify-between items-center">
          <label className="text-xs tracking-wide text-slate-400 uppercase">
            Detection Confidence Threshold
          </label>
          <span className="text-sm font-semibold text-primary">{threshold}%</span>
        </div>
        <input
          type="range"
          min={0}
          max={100}
          value={threshold}
          onChange={(e) => setThreshold(Number(e.target.value))}
          className="w-full accent-orange-500"
        />
      </div>

      <div className="bg-white/5 border border-white/10 rounded-2xl p-5 flex justify-between items-center">
        <label className="text-xs tracking-wide text-slate-400 uppercase">Alert Sound</label>
        <button
          onClick={() => setSoundEnabled(!soundEnabled)}
          className={`w-12 h-6 rounded-full transition-all relative ${
            soundEnabled ? 'bg-primary' : 'bg-white/20'
          }`}
        >
          <span
            className={`absolute top-0.5 w-5 h-5 rounded-full bg-white transition-all ${
              soundEnabled ? 'left-6' : 'left-0.5'
            }`}
          />
        </button>
      </div>
    </div>
  );
}


