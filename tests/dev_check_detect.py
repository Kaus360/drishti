# Internal dev verification script — not the official API test suite. See tests/test_api.py for that (owned by Tanisha).
import base64
import cv2
import numpy as np
import requests

def test_detect():
    # Attempt to capture from the default webcam
    print("Attempting to capture frame from webcam...")
    cap = cv2.VideoCapture(0)
    frame = None
    if cap.isOpened():
        ret, captured_frame = cap.read()
        if ret:
            frame = captured_frame
            print("Successfully captured frame from webcam.")
    cap.release()
    
    if frame is None:
        print("Webcam not available or failed to capture. Creating a dummy frame...")
        # Create a dummy solid BGR frame (gray background)
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        frame[:] = (128, 128, 128)
        # Draw a simulated object bounding box on it
        cv2.rectangle(frame, (100, 100), (300, 300), (0, 0, 255), -1)
        cv2.putText(frame, "Test Frame", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)

    # Encode the frame as JPEG
    success, encoded = cv2.imencode('.jpg', frame)
    if not success:
        print("Failed to encode frame to JPEG")
        return
        
    # Convert JPEG bytes to base64 encoded string
    b64_str = base64.b64encode(encoded.tobytes()).decode('utf-8')
    
    # Send POST request to the local FastAPI server
    url = "http://localhost:8000/detect"
    print(f"Sending POST request to {url}...")
    try:
        response = requests.post(url, json={"image": b64_str})
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            res_data = response.json()
            import json
            print("Detections:")
            print(json.dumps(res_data.get("detections"), indent=2))
            print(f"Violation Detected: {res_data.get('violation_detected')}")
            annotated_frame_b64 = res_data.get("annotated_frame", "")
            print(f"Annotated Frame Base64 Length: {len(annotated_frame_b64)}")
        else:
            print(f"Error Response: {response.text}")
    except Exception as e:
        print(f"Failed to query endpoint: {e}")

if __name__ == "__main__":
    test_detect()
