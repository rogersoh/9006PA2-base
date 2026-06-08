---
title: inference_pipe Contract
description: The inputs, outputs, and update rules for the student inference hook.
---

## Role

`inference_pipe(frame)` is the main student extension point.
The backend passes each raw webcam frame into this function and expects a fully annotated result back.

## Signature

```python
annotated, detections, alerts, metadata = inference_pipe(frame)
```

The input is a raw OpenCV frame.
The return value should keep this shape stable so the rest of the app can stay small.

## Inputs

- `frame`: the current webcam frame from OpenCV

Treat the input as read-only.
If you need to draw on it, copy it first and annotate the copy.

## Outputs

- `annotated`: the frame that should be shown in the browser
- `detections`: a list of detection records
- `alerts`: a list of alert records
- `metadata`: a dict for extra project-specific state

The base app currently forwards `alerts` and `metadata` to the runtime state.
The annotated frame is JPEG-encoded and streamed to the frontend.

## Expected Shapes

The shared types live in [`app/protocol.py`](/C:/Users/zhenw/Documents/DSAC/explore/9006PA2-base/app/protocol.py).

- `Detection`
  - `label`: string, for example `"PLACEHOLDER_OBJECT"`
  - `confidence`: number, for example `0.0`
  - `bbox`: absolute `xyxy` pixel coordinates, for example `[50, 50, 200, 200]`
  - `track_id`: optional integer
- `Alert`
  - `type`: string, for example `"PLACEHOLDER_ALERT"`
  - `message`: string, for example `"Placeholder alert from the base scaffold."`
  - `severity`: one of `low`, `medium`, `high`
  - `source_detection`: optional `Detection`

`metadata` is intentionally open-ended so student projects can add fields without changing the transport layer.

## Update Rules

Keep these rules in mind when changing the hook:

1. Return the same four-part tuple every time.
2. Keep annotations on `annotated`, not on the original input frame.
3. Put display-ready information in `alerts` and `metadata`.
4. Avoid adding transport logic inside `inference_pipe(frame)`.
5. If the shape changes, update this page and `app/protocol.py` together.

## Example Pattern

The scaffold in `app/student_pipeline.py` shows the basic pattern:

1. Build detections and alerts.
2. Copy the frame.
3. Draw boxes, labels, or overlays on the copy.
4. Return the annotated frame plus the supporting data.

That gives students a place to add model inference, tracking, business rules, or post-processing without
touching the webcam loop or browser transport.
