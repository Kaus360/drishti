# Drishti — Integration Testing & Quality Report

**Prepared by:** Anmol (Member 5 — Integration, PPT & Demo)
**Hackathon:** Tata Technologies InnoVent 2026
**Date:** 28 June 2026
**Environment:** macOS · Backend `localhost:8000` · Frontend `localhost:5173`

---

## Executive Summary

The backend (FastAPI + YOLOv8) and frontend (React dashboard) were independently configured, launched, and connected on a clean local environment. On final re-verification, **all seven integration checks passed**, confirming that the complete real-time PPE detection pipeline — camera capture, AI inference, live dashboard rendering, and live alert logging — functions correctly end-to-end.

Two issues were identified during the initial testing pass (static Dashboard stats and a non-reflective Alerts History page). Both were reported to the Backend and Frontend leads, fixed and merged into `main`, and have now been independently re-verified as resolved. Full before/after detail is in **Section 3**.

---

## 1. Integration Checklist Results — Final Re-Verification

Each item was re-tested manually against the live running system after the team's fixes were merged.

| Check | Result | Observation |
|---|---|---|
| Health Endpoint | ✅ PASS | Backend responded correctly at `/health` with status, model name, and project name. |
| Dashboard Loads | ✅ PASS | All dashboard sections (stats cards, compliance chart) render with no blank screen. |
| Live Camera Feed | ✅ PASS | Real webcam feed displayed with live AI bounding boxes (Hardhat, Mask, Safety Vest). |
| Alerts Feed | ✅ PASS | Alerts History page now logs new violations in real time, with current-session timestamps (verified at 2026-06-29 12:31 onward). |
| Stats Auto-Update | ✅ PASS | Dashboard numbers (Violations Today, Compliance Rate, etc.) now increment live, confirmed across multiple 15–20 second observation windows. |
| Page Navigation | ✅ PASS | All five sidebar pages load successfully with no errors or blank screens. |
| CORS / Console | ✅ PASS | Zero errors and zero warnings in browser console; no cross-origin issues detected. |

**Result: 7 of 7 checks passed (100%).**

---

## 2. Work Completed

- Cloned the team repository and created a dedicated integration branch (`feature/member5-integration`).
- Installed and configured all backend dependencies (FastAPI, Ultralytics YOLOv8, OpenCV, Torch) and frontend dependencies (npm packages).
- Resolved a Python package version conflict between OpenCV and the AI libraries that initially prevented the backend from starting.
- Synced a missing AI model file (`best.pt`) that had not been fully merged into the `main` branch, restoring it from the correct source branch.
- Launched the backend and frontend simultaneously and verified live communication between them.
- Executed all seven items on the integration checklist using direct browser testing and developer tools.
- Verified live AI detection directly: helmet, mask, and safety-vest detection all triggered correctly with confidence scores.
- Identified, isolated, and reported two functional issues with clear technical evidence (network logs and console output).
- Documented all findings in this report for team review prior to recording the final demo video.

---

## 3. Issues Identified & Recommended Fixes

Each issue includes what was observed, the likely technical cause, and a plain-language fix that any team member can act on without needing the full debugging context.

### Issue 1 — Dashboard and Alerts History did not reflect live detections *(Resolved)*
**Severity:** Resolved

**What was observed:** The Dashboard statistics and the Alerts History table did not update when new violations were detected live on the Live Monitor page.

**Fix applied & verified:** Backend Lead and Frontend Developer merged a fix into `main` (changes to `backend/alerts.py`, `backend/main.py`, `Dashboard.tsx`, and `AlertsHistory.tsx`). Re-tested after pulling the fix: Dashboard numbers now increment live, and Alerts History logs each new detection with a current, real-time timestamp. Confirmed working as of 2026-06-29.

### Issue 2 — "OFFLINE" status badge stuck regardless of actual connection state *(Resolved)*
**Severity:** Resolved

**What was observed:** The status badge at the top-right corner of every page permanently displayed "OFFLINE", even while the rest of the app was working correctly.

**Fix applied & verified:** Fixed as part of the same merge (`Layout.tsx` updated). Re-tested: badge now correctly displays "ONLINE" in green across all pages.

### Issue 3 — AI model file (best.pt) missing from main branch *(Resolved during testing)*
**Severity:** Resolved

**What was observed:** At the start of integration testing, the trained YOLOv8 model file (`training/best.pt`) was missing from the `main` branch, even though the corresponding pull request appeared as merged. Only an empty placeholder file was present.

**Likely cause:** The merge that was meant to bring the model weights into `main` did not fully carry over the actual file content, despite the merge commit completing successfully.

**Recommended fix:** Already resolved — flagged to the Backend Lead, who re-synced the branch. After re-pulling, the model file was confirmed present (6.25 MB) and the backend started and ran correctly. No further action needed.

---

## 4. Environment & Setup Notes

For future reference, the following environment-specific steps were required and may help other team members or future setups:

- **Git LFS** (Large File Storage) must be installed (`brew install git-lfs`) before cloning, otherwise large files such as `best.pt` will not download correctly.
- **numpy** must be pinned below version 2, and **opencv-python** below version 4.10, installed together in a single command (`pip3 install "numpy<2" "opencv-python<4.10" --force-reinstall`). Installing them separately causes pip to repeatedly override one with an incompatible version of the other.

---

## 5. Next Steps

1. ✅ ~~Backend/Frontend team to review and address Issue 1 and Issue 2~~ — **Done.**
2. ✅ ~~Re-run integration testing to confirm fixes~~ — **Done, 7/7 checks now pass.**
3. Record demo video showing the fully working system end-to-end.
4. Create final PPT using the Antigravity prompt and team research data.
5. Commit demo video and PPT to the `feature/member5-integration` branch and open a Pull Request for review.

---

*Drishti — Tata Technologies InnoVent 2026 | Prepared by Anmol, Member 5*
