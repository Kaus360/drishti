"""
Drishti - Real-Time PPE Detection System
AI Inference Engine Module

This module loads the YOLOv8-nano model and handles inference on incoming
camera frames. It extracts bounding boxes, confidence scores, and class labels,
annotates frames with custom-colored bounding boxes based on compliance status,
and provides utility functions for base64 encoding/decoding of images.
"""

import os
import io
import base64
import cv2
import numpy as np
from ultralytics import YOLO

# Define the absolute path to the training weights file (best.pt)
# It is located in the '../training/best.pt' relative to this backend module
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'training', 'best.pt')

# Initialize model variable
model = None

# Attempt to load the model at module level so it loads only once during startup
try:
    model = YOLO(MODEL_PATH)
except Exception as e:
    # Print the specific warning message as required without crashing the server startup
    print(f"WARNING: best.pt not found at {MODEL_PATH}. Inference will fail until model is added.")


def run_inference(frame: np.ndarray) -> tuple:
    """
    Runs YOLOv8 inference on a raw BGR frame from OpenCV.
    
    Draws custom bounding boxes and text badges:
    - Red boxes (#FF0000 -> BGR (0, 0, 255)) for violation classes (starting with "NO-")
    - Green boxes (#00FF00 -> BGR (0, 255, 0)) for compliant classes (e.g., Hardhat, Safety Vest)
    
    Args:
        frame (np.ndarray): The raw OpenCV frame (BGR format) to analyze.
        
    Returns:
        tuple: (annotated_frame: np.ndarray, detections: list[dict])
            - annotated_frame: The frame with drawn boxes and labels.
            - detections: A list of dicts, each with 'label', 'confidence', and 'bbox'.
    """
    # If the model failed to load or frame is invalid, return the original frame and empty list
    if model is None:
        return frame, []
    
    if frame is None:
        return frame, []

    try:
        # Create a deep copy of the original frame to avoid modifying the input array directly
        annotated_frame = frame.copy()
        
        # Run inference using the loaded YOLO model
        # verbose=False reduces terminal logging clutter during stream loops
        results = model(annotated_frame, verbose=False)
        
        # If no results returned from YOLO, return copy of frame and empty list
        if not results:
            return annotated_frame, []
            
        # Get the first result (since we passed a single frame input)
        result = results[0]
        boxes = result.boxes
        
        detections = []
        
        # Process each detected object bounding box
        for box in boxes:
            # 1. Extract class ID and map to class label name using model.names
            cls_id = int(box.cls[0])
            label = model.names.get(cls_id, f"Class {cls_id}")
            
            # 2. Extract confidence score and round it to 2 decimal places
            confidence = float(box.conf[0])
            confidence = round(confidence, 2)
            
            # 3. Extract bounding box coordinates as integers [x1, y1, x2, y2]
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            
            # Append extracted detection dictionary to the list of detections
            detections.append({
                "label": label,
                "confidence": confidence,
                "bbox": [x1, y1, x2, y2]
            })
            
            # 4. Color coding configuration:
            # Red box (#FF0000) for violations starting with "NO-" (BGR is (0, 0, 255))
            # Green box (#00FF00) for compliant labels (BGR is (0, 255, 0))
            if label.startswith("NO-"):
                color = (0, 0, 255)  # OpenCV uses BGR (Red)
            else:
                color = (0, 255, 0)  # OpenCV uses BGR (Green)
                
            # 5. Draw the bounding box on the frame with thickness of 2 pixels
            cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), color, 2)
            
            # 6. Format label text with confidence score (e.g., "NO-Hardhat 0.89")
            text = f"{label} {confidence:.2f}"
            
            # 7. Compute position for label text to ensure it stays within frame borders
            text_y = max(y1 - 10, 20)
            
            # 8. Create a background badge for the text to make it stand out clearly (premium UI)
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.5
            thickness = 1
            (text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, thickness)
            
            # Draw filled rectangle matching the compliance color behind the text
            cv2.rectangle(
                annotated_frame,
                (x1, text_y - text_height - 4),
                (x1 + text_width + 4, text_y + baseline - 4),
                color,
                thickness=cv2.FILLED
            )
            
            # Draw label text inside the background badge in white
            cv2.putText(
                annotated_frame,
                text,
                (x1 + 2, text_y - 2),
                font,
                font_scale,
                (255, 255, 255),
                thickness,
                lineType=cv2.LINE_AA
            )
            
        return annotated_frame, detections
        
    except Exception as e:
        # Catch any unexpected errors, print warning, and return the frame unchanged
        print(f"Error during YOLOv8 inference: {e}")
        return frame, []


def frame_to_base64(frame: np.ndarray) -> str:
    """
    Converts an OpenCV BGR frame (numpy array) to a base64-encoded JPEG string.
    
    Args:
        frame (np.ndarray): The numpy image array to encode.
        
    Returns:
        str: Base64-encoded JPEG image string.
    """
    try:
        # Encode image frame to JPEG format in memory buffer
        success, encoded_image = cv2.imencode('.jpg', frame)
        if not success:
            raise ValueError("Failed to encode frame as JPEG")
            
        # Convert raw byte array to base64 encoding and decode to UTF-8 string
        b64_string = base64.b64encode(encoded_image.tobytes()).decode('utf-8')
        return b64_string
    except Exception as e:
        print(f"Error converting frame to base64: {e}")
        return ""


def base64_to_frame(b64_string: str) -> np.ndarray:
    """
    Decodes a base64-encoded JPEG image string back into a BGR frame (numpy array).
    
    Args:
        b64_string (str): Base64-encoded image string.
        
    Returns:
        np.ndarray: Decoded OpenCV frame, or empty array if conversion fails.
    """
    try:
        # Decode base64 string back into binary bytes
        img_bytes = base64.b64decode(b64_string)
        
        # Convert binary bytes to 1D uint8 numpy array
        np_arr = np.frombuffer(img_bytes, dtype=np.uint8)
        
        # Decode the image array into a 3-channel BGR image
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        return frame
    except Exception as e:
        print(f"Error converting base64 to frame: {e}")
        # Return a blank frame fallback if decoding fails
        return np.zeros((480, 640, 3), dtype=np.uint8)
