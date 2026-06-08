from __future__ import annotations

from typing import Any

from app.protocol import Alert, Detection


def build_alerts(detections: list[Detection]) -> list[Alert]:
    # Students replace this with real post-processing rules.
    return []


def build_metadata(detections: list[Detection], fps: float, model_status: str) -> dict[str, Any]:
    # Keep this scaffold intentionally small and easy to replace.
    return {
        "note": "placeholder metadata",
        "fps": fps,
        "model_status": model_status,
        "detection_count": len(detections),
    }
