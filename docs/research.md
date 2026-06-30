\# Research Writeup: PPE Compliance and Edge AI for Industrial Safety in India



\*Prepared for Drishti — Tata Technologies InnoVent 2026\*



\## 1. Problem Overview



\- Government data from the Directorate General Factory Advice Service \& Labour Institutes (DGFASLI) shows that registered Indian factories averaged 1,109 deaths and more than 4,000 injuries every year between 2017 and 2020, and separate analysis of the same data found that roughly three workers died and eleven were injured each day on average over that period.

\- Independent tracking suggests the true toll is far higher: in 2024 alone, monitoring by IndustriALL recorded over 240 workplace accidents in manufacturing, mining, and energy that caused more than 400 deaths and 850 serious injuries — and accidents in unregistered units aren't even captured in official counts.

\- Industry-wide compliance with safety norms remains weak: fewer than 40% of Indian companies fully comply with national occupational safety norms, with poor training and inadequate PPE cited as recurring causes of preventable incidents.

\- Manual supervision cannot scale to the size of the problem — large sites, multiple shifts, and limited safety-officer staffing mean a human supervisor simply cannot watch every worker, every entry point, every minute.

\- The result is a structural blind spot: PPE violations go unnoticed in real time, and are only discovered after an incident has already occurred.



\## 2. Existing Solutions \& Their Gaps



\- \*\*Cloud-based monitoring systems\*\* depend on stable, high-bandwidth internet — a major constraint on remote or under-connected industrial and construction sites — and introduce latency between a violation occurring and an alert reaching a supervisor. Ongoing cloud compute and data costs also make them expensive to run continuously.

\- \*\*Manual CCTV review\*\* is reactive rather than preventive: footage is typically reviewed after an incident, not monitored live, and is subject to human fatigue, distraction, and error during long shifts.

\- \*\*Enterprise hardware safety systems\*\* (dedicated sensor arrays, proprietary monitoring suites) can be effective but carry high upfront and maintenance costs, putting them out of reach for India's Micro, Small \& Medium Enterprises (MSMEs), which make up the bulk of the country's industrial base.

\- Across all three approaches, the common gap is the same: detection that is either too slow, too costly, or too dependent on consistent connectivity and human attention to actually prevent the accident before it happens.



\## 3. Why Edge AI is the Answer



\- \*\*Edge AI\*\*, in simple terms, means running an AI model directly on a local device — a laptop, camera, or embedded board — instead of sending data to a remote server for processing.

\- This brings three concrete benefits to industrial safety: near-zero latency (detection and alerting happen in real time, not after a round trip to the cloud), full offline capability (the system works even where internet access is unreliable or unavailable), and stronger data privacy (worker video never leaves the site).

\- For the Indian industrial context specifically — where many sites are remote, connectivity is inconsistent, and budgets are tight — an edge-based approach removes the two biggest barriers (cost and connectivity) that keep safety technology out of reach for smaller operators.



\## 4. Drishti's Approach



\- Drishti runs on-device inference using \*\*YOLOv8-nano\*\*, a lightweight object detection model chosen specifically because it can run in real time on consumer hardware like a standard laptop, without a dedicated GPU server.

\- The model is trained to detect three PPE classes most critical to construction and manufacturing safety: \*\*helmets, safety vests, and goggles\*\*, flagging workers where any of these are missing.

\- When a violation is detected, Drishti triggers an alert instantly through the dashboard and logs it with a timestamp, building a running record of compliance over time rather than a one-off snapshot.

\- A standard laptop is, in effect, the perfect edge device for site deployment: it's already common hardware, requires no specialized installation, has a built-in camera, and needs no recurring cloud subscription to function.



\## 5. Impact \& Benefits



\- \*\*Response time:\*\* where manual supervision can take minutes or longer to notice and respond to a violation (if it's noticed at all), Drishti's on-device detection flags it within seconds of the camera capturing the frame.

\- \*\*Cost:\*\* because Drishti runs entirely on local hardware with no cloud inference or storage costs, it avoids the recurring subscription and bandwidth expenses that make cloud-based monitoring systems expensive to sustain.

\- \*\*Scalability:\*\* the same lightweight model can be deployed across multiple sites or camera points simply by running another instance — no centralized infrastructure investment required.

\- \*\*Accessibility for MSMEs:\*\* by removing the need for specialized hardware or cloud contracts, Drishti puts real-time PPE monitoring within reach of small and medium manufacturers and contractors, not just large enterprises with dedicated safety budgets.



\## 6. References



\- Directorate General Factory Advice Service \& Labour Institutes (DGFASLI), Ministry of Labour \& Employment, Government of India — factory accident and fatality data, 2017–2020.

\- IndustriALL Global Union — 2024 workplace accident tracking, manufacturing, mining, and energy sectors.

\- ILO Global Safety Index / Ministry of Labour / NDMA compliance estimates, as reported in industry safety analysis, 2025.

\- Jocher, G., Chaurasia, A., \& Qiu, J. — \*Ultralytics YOLOv8\* (2023), Ultralytics.



\---

\*Note: Indian workplace safety statistics are widely understood to be undercounted, since official figures cover only registered factories and exclude the large unorganized and informal industrial sector. Actual incident rates are likely higher than reported here.\*



