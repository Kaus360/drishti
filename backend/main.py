"""
Drishti API - FastAPI Application Entry Point

This module sets up a FastAPI server with endpoints for:
1. Health checks (/health)
2. Single frame AI inference (/detect)
3. Live webcam video streaming with real-time annotations (/stream)
4. Placeholder endpoints for alerts (/alerts/latest and /alerts/count)
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

# Import custom inference utilities from backend/inference.py
from backend.inference import run_inference, frame_to_base64, base64_to_frame

# Initialize the FastAPI application
app = fastapi.FastAPI(
    title="Drishti API",
    version="1.0.0",
    description="Real-time PPE compliance detection API for Drishti"
)

# Configure CORS Middleware to allow React frontend (localhost:5173/localhost:3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allow all request headers
)


# Pydantic model representing incoming POST request payload for detection
class DetectRequest(BaseModel):
    image: str  # Base64 encoded JPEG string representing a camera frame


@app.get("/health")
async def health():
    """
    Health check endpoint to verify server status and model loading.
    Returns:
        dict: Status information
    """
    return {
        "status": "running",
        "model": "YOLOv8-nano",
        "project": "Drishti"
    }


@app.post("/detect")
async def detect(request: DetectRequest):
    """
    Inference endpoint for single frame detection.
    Accepts a base64 encoded image, performs YOLOv8 PPE detection, 
    and returns annotated frame with detection coordinates and labels.
    """
    try:
        # Check for empty input
        if not request.image or len(request.image.strip()) == 0:
            raise fastapi.HTTPException(status_code=400, detail="Empty base64 image data")

        # Decode base64 image representation to OpenCV BGR numpy array
        frame = base64_to_frame(request.image)
        
        # If frame is None or is invalid, raise error
        if frame is None or frame.size == 0:
            raise ValueError("Failed to decode image from base64 string")

        # Run inference using the loaded YOLO model
        annotated_frame, detections = run_inference(frame)
        
        # Determine compliance violation status: True if any label starts with "NO-"
        violation_detected = any(d["label"].startswith("NO-") for d in detections)
        
        # Encode annotated image back to base64 for HTTP transport
        annotated_b64 = frame_to_base64(annotated_frame)
        
        return {
            "detections": detections,
            "violation_detected": violation_detected,
            "annotated_frame": annotated_b64
        }
    except Exception as e:
        # Wrap any decoding or inference failures in an HTTP 400 Bad Request response
        raise fastapi.HTTPException(status_code=400, detail=f"Invalid image or inference error: {str(e)}")


def generate_frames():
    """
    Generator function to capture webcam video, perform YOLO inference,
    and yield multipart JPEG stream payloads.
    """
    # OpenCV video capture initialization (0 matches the default local system webcam)
    cap = cv2.VideoCapture(0)
    
    try:
        # Handle failure to open the webcam gracefully
        if not cap.isOpened():
            print("WARNING: Could not open webcam (index 0).")
            # Create a fallback black image showing "Camera Unavailable"
            error_frame = np.zeros((480, 640, 3), dtype=np.uint8)
            cv2.putText(
                error_frame,
                "Camera Unavailable",
                (100, 240),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.0,
                (0, 0, 255),  # Red text color (BGR format)
                2,
                cv2.LINE_AA
            )
            success, encoded_error = cv2.imencode('.jpg', error_frame)
            if success:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + encoded_error.tobytes() + b'\r\n')
            return

        while True:
            # Read a new frame from the webcam stream
            success, frame = cap.read()
            if not success:
                # Break stream generator if reading frames fails (e.g. camera unplugged)
                break
                
            # Perform real-time YOLOv8 object detection on the captured frame
            annotated_frame, _ = run_inference(frame)
            
            # Encode frame to JPEG format
            success, jpeg_buffer = cv2.imencode('.jpg', annotated_frame)
            if not success:
                continue
                
            # Convert JPEG buffer to bytes
            frame_bytes = jpeg_buffer.tobytes()
            
            # Yield frame as multipart boundary response chunk
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
                   
    finally:
        # Ensure camera resource is released when stream stops or error happens
        cap.release()


@app.get("/stream")
def stream():
    """
    Live streaming endpoint. Yields an annotated multipart JPEG replacement stream
    directly from the webcam source.
    """
    return StreamingResponse(
        generate_frames(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )


# --- Placeholder endpoints for alert system integration ---
@app.get("/alerts/latest")
async def latest_alerts():
    """
    Placeholder endpoint to fetch latest alerts.
    To be fully implemented in alerts.py by teammate.
    """
    return {"alerts": [], "message": "alerts module pending"}


@app.get("/alerts/count")
async def alerts_count():
    """
    Placeholder endpoint to fetch count of pending alerts.
    To be fully implemented in alerts.py by teammate.
    """
    return {"count": 0, "message": "alerts module pending"}


# Entry point for running the server directly
if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
