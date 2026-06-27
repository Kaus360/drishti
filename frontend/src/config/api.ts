// Drishti API Configuration
// All backend endpoints are defined here
// Backend runs on localhost:8000 (Kaustubh's FastAPI server)
export const API_BASE_URL = 'http://localhost:8000';

export const API_ENDPOINTS = {
  health: `${API_BASE_URL}/health`,
  detect: `${API_BASE_URL}/detect`,
  stream: `${API_BASE_URL}/stream`,
  alertsLatest: `${API_BASE_URL}/alerts/latest`,
  alertsCount: `${API_BASE_URL}/alerts/count`,
};
