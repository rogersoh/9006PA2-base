from __future__ import annotations

from collections import Counter # added
from typing import Any

from app.protocol import Alert, Detection
from app.student_config import RIPENESS_SEVERITY #added

_RIPENESS_MESSAGES = {
    "unripe": "Unripe banana detected — not ready yet.",
    "ripe": "Ripe banana detected — good to eat.",
    "overripe": "Overripe banana detected — use soon.",
    "rotten": "Rotten banana detected — discard.",
}


# def build_alerts(detections: list[Detection]) -> list[Alert]:
#     # Students replace this with real post-processing rules.
#     return [
#         {
#             "type": "PLACEHOLDER_ALERT",
#             "message": "Placeholder alert from the base scaffold.",
#             "severity": "low",
#         }
#     ]

def build_alerts(detections: list[Detection]) -> list[Alert]:
    # Alert on every ripeness detection (overripe / ripe / rotten / unripe).
    # Severity and messaging are keyed off the ripeness class itself rather
    # than confidence, since for this use case the *class* is what matters
    # (a rotten banana is a high-severity alert regardless of how confident
    # the model is, as long as it clears the confidence threshold).
    alerts: list[Alert] = []
    for detection in detections:
        label = detection["label"]
        alerts.append(
            {
                "type": f"{label.upper()}_BANANA",
                "message": _RIPENESS_MESSAGES.get(
                    label,
                    f'Detected {label} ({detection["confidence"]:.2f} confidence).',
                ),
                "severity": RIPENESS_SEVERITY.get(label, "low"),
                "source_detection": detection,
            }
        )
    return alerts

# def build_metadata(detections: list[Detection], alerts: list[Alert]) -> dict[str, Any]:
#     # Keep this scaffold intentionally small and easy to replace.
#     return {
#         "note": "placeholder metadata",
#         "detection_count": len(detections),
#         "alert_count": len(alerts),
#     }

def build_metadata(detections: list[Detection], alerts: list[Alert]) -> dict[str, Any]:
    ripeness_counts = Counter(detection["label"] for detection in detections)
    severity_counts = Counter(alert["severity"] for alert in alerts)

    return {
        "detection_count": len(detections),
        "alert_count": len(alerts),
        "ripeness_counts": {
            "unripe": ripeness_counts.get("unripe", 0),
            "ripe": ripeness_counts.get("ripe", 0),
            "overripe": ripeness_counts.get("overripe", 0),
            "rotten": ripeness_counts.get("rotten", 0),
        },
        "severity_counts": dict(severity_counts),
    }



