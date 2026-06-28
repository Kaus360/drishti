# Drishti — Integration Testing & Quality Report

**Prepared by:** Anmol (Member 5 — Integration, PPT & Demo)
**Hackathon:** Tata Technologies InnoVent 2026
**Date:** 28 June 2026
**Environment:** macOS · Backend `localhost:8000` · Frontend `localhost:5173`

---

## Executive Summary

The backend (FastAPI + YOLOv8) and frontend (React dashboard) were independently configured, launched, and connected on a clean local environment. Of the seven integration checks performed, **six passed successfully**, confirming that the core real-time PPE detection pipeline — camera capture, AI inference, and live dashboard rendering — functions correctly end-to-end.

One functional gap was identified: two dashboard views (statistics and alert history) do not refresh with live detection data. Root cause and a plain-language fix are detailed in **Section 3**. All findings below have been verified independently and are ready for the development team's review.

---

## 1. Integration Checklist Results

Each item was tested manually against the live running system.

| Check | Result | Observation |
|---|---|---|
| Health Endpoint | ✅ PASS | Backend responded correctly at `/health` with status, model name, and project name. |
| Dashboard Loads | ✅ PASS | All dashboard sections (stats cards, compliance chart) render with no blank screen. |
| Live Camera Feed | ✅ PASS | Real webcam feed displayed with live AI bounding boxes (Hardhat, Mask, Safety Vest). |
| Alerts Feed | ✅ PASS | Alerts History page lists violations with type, timestamp, and confidence score. |
| Stats Auto-Update | ❌ FAIL | Dashboard numbers remained unchanged after 20+ seconds of observation. |
| Page Navigation | ✅ PASS | All five sidebar pages load successfully with no errors or blank screens. |
| CORS / Console | ✅ PASS | Zero errors and zero warnings in browser console; no cross-origin issues detected. |

**Result: 6 of 7 checks passed (86%).**

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

### Issue 1 — Dashboard and Alerts History do not reflect live detections
**Severity:** Medium

**What was observed:** The Dashboard statistics (Violations Today, Compliance Rate, Active Cameras, Workers Monitored) and the Alerts History table do not update when new violations are detected live on the Live Monitor page. Both continue to display the same fixed values regardless of new detections.

**Likely cause:** The Live Monitor page is confirmed to be genuinely live — it streams real camera frames and polls the backend's `/health` endpoint every few seconds. The Dashboard and Alerts History pages, however, do not show this same repeated-polling behavior, which strongly suggests they are reading from a static or seed dataset instead of the live detection stream.

**Recommended fix (in simple terms):** Two pages in the app are showing old, fixed sample numbers instead of checking in with the AI brain (the backend) for updates. The Live Monitor page already does this correctly — it asks the backend for new information every few seconds. The Dashboard and Alerts History pages need to do the same thing: add a repeating timer (the same kind already used on Live Monitor) to these two pages, and point them to read from the live results the backend produces, rather than from a fixed list of sample numbers.

### Issue 2 — "OFFLINE" status badge stuck regardless of actual connection state
**Severity:** Low

**What was observed:** The status badge at the top-right corner of every page permanently displays "OFFLINE", even while the Live Monitor feed and Alerts data are confirmed to be working correctly.

**Likely cause:** This is most likely a separate, narrower status check used only for that one badge, which is not correctly reading the real connection state that the rest of the app uses successfully.

**Recommended fix (in simple terms):** The small red "OFFLINE" label in the corner is asking a different, possibly outdated question than the rest of the app. It probably needs to be pointed at the same health/connection check that the Live Monitor page already uses successfully, so it shows "ONLINE" once that check succeeds.

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

1. Backend/Frontend team to review and address Issue 1 and Issue 2 above.
2. Once addressed, integration testing will be re-run to confirm the Dashboard and Alerts History pages reflect live data.
3. Demo video recording to follow immediately after re-verification.
4. Final PPT and demo assets to be committed to the `feature/member5-integration` branch with a pull request opened for review.

---

*Drishti — Tata Technologies InnoVent 2026 | Prepared by Anmol, Member 5*
