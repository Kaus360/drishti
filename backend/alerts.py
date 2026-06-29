import csv
import os
from datetime import datetime

LOG_PATH = os.path.join(os.path.dirname(__file__), '..', 'logs', 'violations.csv')
CSV_COLUMNS = ['timestamp', 'violation_type', 'confidence']
_LAST_LOGGED_AT = None


def _ensure_log_file() -> None:
    log_dir = os.path.dirname(LOG_PATH)
    os.makedirs(log_dir, exist_ok=True)
    if not os.path.exists(LOG_PATH):
        with open(LOG_PATH, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=CSV_COLUMNS)
            writer.writeheader()


def _read_rows() -> list[dict]:
    if not os.path.exists(LOG_PATH):
        return []

    with open(LOG_PATH, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)


def _parse_timestamp(value: str) -> datetime:
    return datetime.fromisoformat(value)


def _format_confidence(value: str) -> int:
    confidence = float(value)
    if confidence <= 1:
        confidence *= 100
    return int(round(confidence))


def log_violation(violation_type: str, confidence: float) -> None:
    global _LAST_LOGGED_AT

    try:
        now = datetime.now()
        if _LAST_LOGGED_AT is not None and (now - _LAST_LOGGED_AT).total_seconds() < 1:
            return

        _ensure_log_file()
        with open(LOG_PATH, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=CSV_COLUMNS)
            writer.writerow(
                {
                    'timestamp': now.isoformat(),
                    'violation_type': violation_type,
                    'confidence': float(confidence),
                }
            )
        _LAST_LOGGED_AT = now
    except Exception as exc:
        print(f'WARNING: failed to log violation: {exc}')


def get_latest_alerts(limit: int = 10) -> list[dict]:
    rows = _read_rows()
    if not rows:
        return []

    sorted_rows = sorted(rows, key=lambda row: _parse_timestamp(row['timestamp']), reverse=True)
    alerts = []
    for index, row in enumerate(sorted_rows[:limit], start=1):
        alerts.append(
            {
                'id': index,
                'type': row['violation_type'],
                'date': _parse_timestamp(row['timestamp']).strftime('%Y-%m-%d %H:%M'),
                'confidence': _format_confidence(row['confidence']),
            }
        )
    return alerts


def get_alert_stats() -> dict:
    rows = _read_rows()
    if not rows:
        return {
            'violationsToday': 0,
            'complianceRate': 100.0,
            'activeCameras': 1,
            'workersMonitored': 0,
        }

    today = datetime.now().date()
    todays_rows = [row for row in rows if _parse_timestamp(row['timestamp']).date() == today]
    violations_today = len(todays_rows)

    # Simplified heuristic until compliant detections are tracked separately.
    compliance_rate = max(0.0, min(100.0, 100.0 - (violations_today * 5)))

    # Approximation for the prototype: each logged row stands in for a monitored worker event.
    workers_monitored = len(todays_rows)

    return {
        'violationsToday': violations_today,
        'complianceRate': round(compliance_rate, 1),
        'activeCameras': 1,
        'workersMonitored': workers_monitored,
    }
