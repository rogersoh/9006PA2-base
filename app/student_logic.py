from __future__ import annotations

from typing import Any

from app.protocol import Alert, Detection


def build_alerts(detections: list[Detection]) -> list[Alert]:
    # Students replace this with real post-processing rules.
    return [
        {
            "type": "PLACEHOLDER_ALERT",
            "message": "Placeholder alert from the base scaffold.",
            "severity": "low",
        }
    ]


def build_metadata(detections: list[Detection], alerts: list[Alert]) -> dict[str, Any]:
    # Keep this scaffold intentionally small and easy to replace.
    return {
        "note": "placeholder metadata",
        "detection_count": len(detections),
        "alert_count": len(alerts),
    }
