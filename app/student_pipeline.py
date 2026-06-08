from __future__ import annotations

from typing import Any

import cv2

from app.protocol import Alert, Detection
from app.student_logic import build_alerts, build_metadata


def inference_pipe(frame) -> tuple[Any, list[Detection], list[Alert], dict[str, Any]]:
    detections: list[Detection] = [
        {
            "label": "PLACEHOLDER_OBJECT",
            "confidence": 0.0,
            "bbox": [50, 50, 200, 200],
        }
    ]
    alerts: list[Alert] = [
        {
            "type": "PLACEHOLDER_ALERT",
            "message": "Placeholder alert from the base scaffold.",
            "severity": "low",
        }
    ]
    metadata = build_metadata(detections, fps=0.0, model_status="loading")

    annotated = frame.copy()
    for detection in detections:
        x1, y1, x2, y2 = detection["bbox"]
        cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 255, 255), 2)
        cv2.putText(
            annotated,
            f'{detection["label"]} {detection["confidence"]:.2f}',
            (x1, max(20, y1 - 10)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 255),
            2,
            cv2.LINE_AA,
        )

    alerts = build_alerts(detections) or alerts
    return annotated, detections, alerts, metadata
