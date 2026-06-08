# Backend Cleanup TODO

Goal: make the backend easier for students to read and extend without changing the app behavior.

## 1. Simplify `app/server.py`
- Split the file into three obvious sections:
  - app setup and routes
  - shared runtime state
  - capture/stream worker loop
- Remove unused code paths and variables:
  - `_set_state` if it is not used
  - `backoff` in the WebSocket loop if the server is not actually reconnecting there
  - any other dead state that only adds noise
- Keep the startup flow readable:
  - server starts immediately
  - capture thread starts on startup
  - model status transitions through `loading -> live/error`

## 2. Make runtime state explicit
- Replace the current loose globals with a small, clearly named state container if it improves readability.
- Keep only the state students actually need to understand:
  - latest annotated JPEG frame
  - latest alerts
  - latest metadata
  - latest FPS
  - model status
- Keep locking in one place so the concurrency model is easy to explain.

## 3. Clarify the capture loop
- Break `_capture_loop()` into smaller helper functions if needed:
  - open camera
  - process one frame
  - encode frame to JPEG
  - publish latest state
- Make it obvious that the loop always keeps the newest frame and drops old work.
- Keep the error path explicit:
  - if camera open fails, set `model_status = "error"`
  - if capture fails later, set `model_status = "error"` and stop processing

## 4. Clarify the WebSocket contract
- Keep the one-socket multiplexed design.
- Add small helpers for sending:
  - status JSON
  - alerts JSON
  - binary frame bytes
- Make the message types obvious and stable:
  - `status`
  - `alerts`
- Keep the socket loop short and linear so students can follow it quickly.

## 5. Clean up `app/student_pipeline.py`
- Keep `inference_pipe(frame)` as the only student-facing inference hook.
- Make the placeholder behavior more obviously temporary:
  - one placeholder detection in a list
  - one placeholder alert in a list
  - placeholder metadata dict
- Keep the drawing code simple and readable.
- Avoid adding extra framework code that would distract from the student task.

## 6. Tighten shared protocol definitions
- Keep `app/protocol.py` as the single source of truth for message and record shapes.
- Ensure the type names are easy to understand:
  - `Detection`
  - `Alert`
  - `StatusMessage`
  - `AlertsMessage`
  - `MetadataMessage`
- Do not over-model metadata; keep it open-ended on purpose.

## 7. Re-check the smoke test
- Confirm the smoke test still covers:
  - imports for the backend modules
  - server startup
  - health endpoint response
- Make sure the test stays lightweight and does not require webcam hardware to pass import checks.
- If the startup test depends on real hardware, keep that as a separate assumption in the test notes.

## 8. Verify the teaching surface
- Confirm the files students are expected to edit are still obvious:
  - `app/student_pipeline.py`
  - `app/student_logic.py`
  - `app/student_config.py`
- Confirm the frontend stays minimal and unchanged unless there is a clear reason to touch it.
- Update `README.md` only if the backend cleanup changes the workflow or file map.

## Done When
- The backend is shorter, easier to scan, and the control flow is obvious.
- No behavior changes for the current scaffold.
- The student-edit files and runtime contract remain the same.
