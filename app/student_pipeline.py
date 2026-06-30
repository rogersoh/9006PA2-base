from __future__ import annotations

from typing import Any

import cv2

from app.protocol import Alert, Detection

from app.student_logic import build_alerts, build_metadata

# TO EDIT
### Example: loading pre-trained YOLO26 for object detection (COCO 80 classes).
### Replace this with your actual (fine-tuned) model and initialization logic.
### `inference_pipe` will be called on every frame, so make sure to load your model
### here so you don't have to re-load it on every frame.
from ultralytics import YOLO
model = YOLO('yolo26n.pt')


def inference_pipe(frame) -> tuple[Any, list[Detection], list[Alert], dict[str, Any]]:
    # Replace this scaffold with the student's real inference pipeline.
    # For demonstration purposes, this scaffold simply returns a placeholder
    #  detection, alert, and metadata on every frame.
    # You should replace this with your actual model inference and alerting logic.
    ############################################################################################
    ### Example of detection list
    detections: list[Detection] = [
        {
            "label": "PLACEHOLDER_OBJECT",
            "confidence": 0.0,
            "bbox": [50, 50, 200, 200],
        }
    ]

    ### Example of alert list
    ### Ideally, use `build_alerts` function from `student_logic.py`:
    ###   `alerts = build_alerts(detections)`
    alerts: list[Alert] = [
        {
            "type": "PLACEHOLDER_ALERT",
            "message": "Placeholder alert from the base scaffold.",
            "severity": "low",
        }
    ]

    ### Example of metadata dictionary
    ### Ideally, use `build_metadata` function from `student_logic.py`:
    ###   `metadata = build_metadata(detections, alerts)`
    metadata: dict[str, Any] = {
        "note": "placeholder metadata",
        "detection_count": len(detections),
        "alert_count": len(alerts),
    }

    ### Example of annotated frame, to be displayed on frontend
    ### Note: This example draws the bbox manually, but the Ultralytics library has
    ###       built-in annotation functions that you can use for simplicity!
    annotated_frame = frame.copy()
    for detection in detections:
        x1, y1, x2, y2 = detection["bbox"]
        cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 255, 255), 2)
        cv2.putText(
            annotated_frame,
            f'{detection["label"]} {detection["confidence"]:.2f}',
            (x1, max(20, y1 - 10)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 255),
            2,
            cv2.LINE_AA,
        )
    
    return annotated_frame, detections, alerts, metadata
