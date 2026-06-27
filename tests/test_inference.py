import os
import sys
import numpy as np

# Add the project directory to sys.path so we can import backend.inference
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.inference import run_inference, frame_to_base64, base64_to_frame, model, MODEL_PATH

def test_missing_model_warning():
    print("--- Test: Missing Model Warning ---")
    print(f"MODEL_PATH: {MODEL_PATH}")
    print(f"Model loaded: {model}")
    assert model is None, "Model should be None because training/best.pt does not exist yet."
    print("Passed: Model is correctly None and doesn't crash during import.\n")

def test_base64_conversion():
    print("--- Test: Base64 Conversion ---")
    # Create a dummy solid blue frame (BGR: 255, 0, 0)
    original_frame = np.zeros((100, 100, 3), dtype=np.uint8)
    original_frame[:] = (255, 0, 0)
    
    # Convert to base64
    b64_str = frame_to_base64(original_frame)
    assert isinstance(b64_str, str), "Base64 output should be a string"
    assert len(b64_str) > 0, "Base64 string should not be empty"
    print("Successfully converted frame to base64 string.")
    
    # Decode back to frame
    decoded_frame = base64_to_frame(b64_str)
    assert decoded_frame is not None, "Decoded frame should not be None"
    assert decoded_frame.shape == original_frame.shape, f"Decoded shape {decoded_frame.shape} matches original {original_frame.shape}"
    
    # Check that colors are close (due to JPEG compression, they might not be exactly equal, but should be close)
    mean_diff = np.mean(np.abs(decoded_frame.astype(float) - original_frame.astype(float)))
    print(f"Mean pixel color difference (JPEG loss): {mean_diff:.4f}")
    assert mean_diff < 5.0, "Decoded frame pixel values should be very close to original frame values"
    print("Passed: Base64 conversion functions are fully operational.\n")

def test_run_inference_fallback():
    print("--- Test: run_inference Fallback ---")
    # Create a dummy solid blue frame
    dummy_frame = np.zeros((480, 640, 3), dtype=np.uint8)
    dummy_frame[:] = (255, 0, 0)
    
    # Run inference with missing model
    annotated_frame, detections = run_inference(dummy_frame)
    
    # It should return the frame unchanged (same values) and empty detections
    assert np.array_equal(dummy_frame, annotated_frame), "Annotated frame should be identical to input frame when model is missing"
    assert detections == [], "Detections list should be empty when model is missing"
    print("Passed: Inference fallback handled gracefully without crashes.\n")

if __name__ == "__main__":
    test_missing_model_warning()
    test_base64_conversion()
    test_run_inference_fallback()
    print("All tests passed successfully!")
