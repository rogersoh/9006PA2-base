from __future__ import annotations

from typing import Any

from app.protocol import Alert, Detection


def build_alerts(detections: list[Detection]) -> list[Alert]:
    return []


def build_metadata(detections: list[Detection], fps: float, model_status: str) -> dict[str, Any]:
    return {
        "note": "placeholder metadata",
        "fps": fps,
        "model_status": model_status,
        "detection_count": len(detections),
    }
