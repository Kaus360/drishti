\# DRISHTI

> See Every Risk. Stop Every Accident.



!\[Built With Python](https://img.shields.io/badge/Built%20With-Python-3776AB?logo=python\&logoColor=white)

!\[React](https://img.shields.io/badge/Frontend-React-61DAFB?logo=react\&logoColor=white)

!\[YOLOv8](https://img.shields.io/badge/AI%20Model-YOLOv8-00FFFF)

!\[FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?logo=fastapi\&logoColor=white)



\## About



Drishti is a real-time, on-device PPE (Personal Protective Equipment) compliance monitoring system built for industrial construction and manufacturing sites. Using a standard laptop camera and a locally running YOLOv8-nano model, it detects workers missing helmets, safety vests, or goggles — instantly, with zero cloud dependency and zero internet requirement. Built for Tata Technologies InnoVent 2026, Drishti brings affordable, edge-based safety monitoring within reach of sites that can't afford expensive enterprise surveillance systems.



\## Features



\- \[x] Real-time PPE detection (helmet, vest, goggles)

\- \[x] Fully offline — no cloud dependency

\- \[x] Instant violation alerts on dashboard

\- \[x] Automatic violation logging with timestamps

\- \[x] Live annotated camera feed

\- \[x] Analytics and compliance rate tracking



\## Tech Stack



| Layer | Technology |

|---|---|

| Backend | Python, FastAPI, Uvicorn |

| AI Model | YOLOv8-nano (Ultralytics) |

| Computer Vision | OpenCV |

| Frontend | React, TypeScript, Tailwind CSS |

| UI Components | shadcn/ui, framer-motion |

| Charts | Recharts |

| Training | Google Colab, Roboflow |



\## Getting Started



\### Prerequisites

\- Python 3.10+

\- Node.js 18+

\- Git



\### Backend Setup

```bash

git clone <repo-url>

cd drishti

pip install -r requirements.txt

uvicorn backend.main:app --reload

```



\### Frontend Setup

```bash

cd frontend

npm install

npm run dev

```

\## Team



| Role | Name |

|---|---|

| ML Engineer | Arnav |

| Backend Lead | Kaustubh |

| Frontend Developer | Shivam |

| QA \& Documentation | Tanisha |

| Integration \& Demo | \[Member 5 name] |



\## License



MIT

