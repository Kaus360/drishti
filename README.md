# DRISHTI

> See Every Risk. Stop Every Accident.

![Built With Python](https://img.shields.io/badge/Built%20With-Python-3776AB?logo=python&logoColor=white)
![React](https://img.shields.io/badge/Frontend-React-61DAFB?logo=react&logoColor=white)
![YOLOv8](https://img.shields.io/badge/AI%20Model-YOLOv8-00FFFF)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?logo=fastapi&logoColor=white)

## About

Drishti is a real-time, on-device PPE (Personal Protective Equipment) compliance monitoring system built for industrial construction and manufacturing sites. Using a standard laptop camera and a locally running YOLOv8-nano model, it detects workers missing helmets, safety vests, or goggles instantly, with zero cloud dependency and zero internet requirement. Built for Tata Technologies InnoVent 2026, Drishti brings affordable, edge-based safety monitoring within reach of sites that can't afford expensive enterprise surveillance systems.

## Features

- [x] Real-time PPE detection (helmet, vest, goggles)
- [x] Fully offline - no cloud dependency
- [x] Instant violation alerts on dashboard
- [x] Automatic violation logging with timestamps
- [x] Live annotated camera feed
- [x] Analytics and compliance rate tracking

## Live System Status

As of 2026-07-01, the following parts of Drishti have been verified working end-to-end:

- Real-time YOLOv8 PPE detection via webcam
- Live violation logging to `logs/violations.csv`
- Dashboard, Alerts History, and Live Monitor all display real polled data, not mock data
- Backend health status is reflected accurately in the UI

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, FastAPI, Uvicorn |
| AI Model | YOLOv8-nano (Ultralytics) |
| Computer Vision | OpenCV |
| Frontend | React, TypeScript, Tailwind CSS |
| UI Components | shadcn/ui, framer-motion |
| Charts | Recharts |
| Training | Google Colab, Roboflow |

## Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+
- Git

Note: Git LFS is required to properly download `training/best.pt`. Run `git lfs install` before cloning, or `git lfs pull` after cloning if the file appears as a small placeholder.

### Backend Setup

```bash
git clone <repo-url>
cd drishti
pip install -r requirements.txt
uvicorn backend.main:app --reload
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

## Testing

- Run the official backend test suite with `python tests/test_api.py`
- The 4 core endpoints covered are `/health`, `/detect`, `/alerts/latest`, and `/alerts/count`

## Team

| Role | Name |
|---|---|
| ML Engineer | Arnav |
| Backend Lead | Kaustubh |
| Frontend Developer | Shivam |
| QA & Documentation | Tanisha |
| Integration & Demo | Anmol |

## License

MIT
