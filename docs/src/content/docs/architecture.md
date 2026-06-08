---
title: App Architecture
description: How webcam frames move through the base app and into the browser.
---

## Purpose

This app is a thin runtime scaffold for student computer vision projects on a live webcam feed.
The base code keeps the capture loop, transport, and browser display stable so students can focus on
`inference_pipe(frame)` and the logic around it.

## System Layout

The app has three layers:

1. Python runtime
   - Opens the webcam.
   - Calls `inference_pipe(frame)` for each frame.
   - Stores the latest annotated output and metadata in shared state.

2. WebSocket transport
   - Streams the latest frame, status, and alerts to the browser.
   - Sends only the newest available state, not a backlog of frames.

3. Frontend display
   - Receives JPEG frames as binary messages.
   - Receives status and alerts as JSON messages.
   - Renders the live image and supporting UI state.

## Frame Flow

The capture path is intentionally simple:

1. Open the camera in `app/server.py`.
2. Read a frame from OpenCV.
3. Pass the raw frame into `inference_pipe(frame)`.
4. Receive:
   - an annotated frame
   - detections
   - alerts
   - metadata
5. Encode the annotated frame as JPEG.
6. Publish the newest JPEG, alerts, metadata, and FPS into shared runtime state.

The important contract is that `inference_pipe(frame)` is the only student-facing inference hook.
Students can replace the placeholder logic inside that function without needing to redesign the runtime.

## Output Flow

The frontend reads from `/ws` in two message forms:

- `status` JSON messages carry `fps` and `model_status`
- `alerts` JSON messages carry the latest alert list
- binary WebSocket messages carry the latest JPEG frame

The browser updates the `<img>` element with the newest JPEG and updates the on-screen status fields
from the JSON payloads.

## Extension Points

Keep future changes aligned to these boundaries:

- `app/student_pipeline.py`: model inference, post-processing, frame annotation
- `app/student_logic.py`: optional helper logic for project-specific rules
- `app/protocol.py`: shared data shapes if the payload grows
- `frontend/app.js`: display behavior and UI state handling

If a project adds new outputs, document the payload shape and the sender/receiver on the same page.
That keeps the architecture readable for both students and coding agents.

## Working Rule

Prefer small, additive changes:

- keep `inference_pipe(frame)` stable
- add new fields to the returned metadata before changing transport
- document any new message type or UI widget in this file as soon as it exists
