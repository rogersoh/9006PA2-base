from __future__ import annotations

from typing import Any

import cv2

from app.protocol import Alert, Detection

from app.student_logic import build_alerts, build_metadata
from app.student_config import MODEL_PATH, CONFIDENCE_THRESHOLD, RIPENESS_COLORS

# TO EDIT
### Example: loading pre-trained YOLO26 for object detection (COCO 80 classes).
### Replace this with your actual (fine-tuned) model and initialization logic.
### `inference_pipe` will be called on every frame, so make sure to load your model
### here so you don't have to re-load it on every frame.
from ultralytics import YOLO

model = YOLO(MODEL_PATH)

_DEFAULT_BOX_COLOR = (255, 255, 255)


def inference_pipe1(frame) -> tuple[Any, list[Detection], list[Alert], dict[str, Any]]:
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

def inference_pipe(frame) -> tuple[Any, list[Detection], list[Alert], dict[str, Any]]:
    ############################################################################################
    # Run the trained banana-ripeness YOLO model on this frame.
    # `verbose=False` keeps ultralytics from spamming stdout on every frame.
    results = model(frame, conf=CONFIDENCE_THRESHOLD, verbose=False)
    result = results[0]

    ### Build our Detection list from the YOLO result boxes.
    detections: list[Detection] = []
    for box in result.boxes:
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        confidence = float(box.conf[0])
        class_id = int(box.cls[0])
        label = model.names[class_id]  # one of: overripe, ripe, rotten, unripe

        detection: Detection = {
            "label": label,
            "confidence": confidence,
            "bbox": [int(x1), int(y1), int(x2), int(y2)],
        }

        # If the model was trained with tracking (model.track(...)), each box
        # may also carry a persistent track_id across frames.
        if box.id is not None:
            detection["track_id"] = int(box.id[0])

        detections.append(detection)

    ### Alert on every ripeness detection (see student_logic.build_alerts).
    alerts: list[Alert] = build_alerts(detections)
    metadata: dict[str, Any] = build_metadata(detections, alerts)

    ### Annotate the frame ourselves so each ripeness class gets its own box color
    ### (green=unripe, gold=ripe, orange=overripe, red=rotten) instead of relying
    ### on ultralytics' default palette.
    annotated_frame = frame.copy()
    for detection in detections:
        x1, y1, x2, y2 = detection["bbox"]
        label = detection["label"]
        color = RIPENESS_COLORS.get(label, _DEFAULT_BOX_COLOR)

        cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), color, 2)
        cv2.putText(
            annotated_frame,
            f'{label} {detection["confidence"]:.2f}',
            (x1, max(20, y1 - 10)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            color,
            2,
            cv2.LINE_AA,
        )

    return annotated_frame, detections, alerts, metadata
