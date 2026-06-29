"""
Drishti API - FastAPI Application Entry Point

This module sets up a FastAPI server with endpoints for:
1. Health checks (/health)
2. Single frame AI inference (/detect)
3. Live webcam video streaming with real-time annotations (/stream)
4. Alert endpoints backed by logged violation data
"""

import os
import io
import base64
import cv2
import numpy as np
import uvicorn
import fastapi
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from backend import alerts
from backend.inference import run_inference, frame_to_base64, base64_to_frame

app = fastapi.FastAPI(
    title="Drishti API",
    version="1.0.0",
    description="Real-time PPE compliance detection API for Drishti"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class DetectRequest(BaseModel):
    image: str


@app.get("/health")
async def health():
    return {
        "status": "running",
        "model": "YOLOv8-nano",
        "project": "Drishti"
    }


@app.post("/detect")
async def detect(request: DetectRequest):
    try:
        if not request.image or len(request.image.strip()) == 0:
            raise fastapi.HTTPException(status_code=400, detail="Empty base64 image data")

        frame = base64_to_frame(request.image)

        if frame is None or frame.size == 0:
            raise ValueError("Failed to decode image from base64 string")

        annotated_frame, detections = run_inference(frame)

        violation_detected = any(d["label"].startswith("NO-") for d in detections)
        for detection in detections:
            if detection["label"].startswith("NO-"):
                alerts.log_violation(detection["label"], detection["confidence"])

        annotated_b64 = frame_to_base64(annotated_frame)

        return {
            "detections": detections,
            "violation_detected": violation_detected,
            "annotated_frame": annotated_b64
        }
    except Exception as e:
        raise fastapi.HTTPException(status_code=400, detail=f"Invalid image or inference error: {str(e)}")


def generate_frames():
    cap = cv2.VideoCapture(0)

    try:
        if not cap.isOpened():
            print("WARNING: Could not open webcam (index 0).")
            error_frame = np.zeros((480, 640, 3), dtype=np.uint8)
            cv2.putText(
                error_frame,
                "Camera Unavailable",
                (100, 240),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.0,
                (0, 0, 255),
                2,
                cv2.LINE_AA
            )
            success, encoded_error = cv2.imencode('.jpg', error_frame)
            if success:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + encoded_error.tobytes() + b'\r\n')
            return

        while True:
            success, frame = cap.read()
            if not success:
                break

            annotated_frame, detections = run_inference(frame)
            for detection in detections:
                if detection["label"].startswith("NO-"):
                    alerts.log_violation(detection["label"], detection["confidence"])

            success, jpeg_buffer = cv2.imencode('.jpg', annotated_frame)
            if not success:
                continue

            frame_bytes = jpeg_buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    finally:
        cap.release()


@app.get("/stream")
def stream():
    return StreamingResponse(
        generate_frames(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )


@app.get("/alerts/latest")
async def latest_alerts():
    return {"alerts": alerts.get_latest_alerts()}


@app.get("/alerts/count")
async def alerts_count():
    return alerts.get_alert_stats()


if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
