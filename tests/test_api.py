# test_api.py
# QA test suite for Drishti's FastAPI backend
# Project: Drishti — Tata Technologies InnoVent 2026
# Author: Tanisha (Member 4 — API Testing + Documentation)
#
# This script tests each backend API endpoint one by one and prints
# PASS or FAIL for each. It is written to be simple and beginner-friendly.

import requests  # used to send HTTP requests to the backend
import base64    # used to encode our test image into base64 text
import json      # used to handle JSON data
import os        # used for any file/path operations (kept for consistency)

# The address where the backend server is running (started by Kaustubh)
BASE_URL = "http://localhost:8000"

# A real, valid, tiny 1x1 pixel PNG image, encoded in base64.
# We use this instead of random bytes because the backend needs to
# actually be able to decode it as a real image.
TINY_PNG_BASE64 = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk"
    "+A8AAQUBAScY42YAAAAASUVORK5CYII="
)


def test_health():
    # Tests the /health endpoint, which tells us the server is alive
    try:
        response = requests.get(BASE_URL + "/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "running"
        print("PASS: /health endpoint working")
    except Exception as e:
        print(f"FAIL: /health — {e}")


def test_detect():
    # Tests the /detect endpoint, which runs PPE detection on an image
    try:
        # Send a real, valid base64-encoded image so the backend can decode it
        payload = {"image": TINY_PNG_BASE64}
        response = requests.post(BASE_URL + "/detect", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "detections" in data
        assert isinstance(data["detections"], list)
        print("PASS: /detect endpoint working")
    except Exception as e:
        print(f"FAIL: /detect — {e}")


def test_alerts_latest():
    # Tests the /alerts/latest endpoint, which returns recent violations
    try:
        response = requests.get(BASE_URL + "/alerts/latest")
        assert response.status_code == 200
        data = response.json()
        assert "alerts" in data
        assert isinstance(data["alerts"], list)
        print("PASS: /alerts/latest endpoint working")
    except Exception as e:
        print(f"FAIL: /alerts/latest — {e}")


def test_alerts_count():
    # Tests the /alerts/count endpoint, which returns today's violation count
    try:
        response = requests.get(BASE_URL + "/alerts/count")
        assert response.status_code == 200
        data = response.json()
        # The backend returns "violationsToday" as the count field
        assert "violationsToday" in data
        print("PASS: /alerts/count endpoint working")
    except Exception as e:
        print(f"FAIL: /alerts/count — {e}")


if __name__ == "__main__":
    print("=" * 50)
    print("DRISHTI — API Test Suite")
    print("=" * 50)
    test_health()
    test_detect()
    test_alerts_latest()
    test_alerts_count()
    print("=" * 50)
    print("All tests completed.")
    print("=" * 50)