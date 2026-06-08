# Computer Vision Live Webcam Base App

This repository is a starter app for student computer vision projects on a local webcam feed.

The base app handles:
- webcam capture in Python
- inference hook wiring
- annotated frame rendering
- live browser display
- alerts and status updates over WebSocket

Students should focus on:
- implementing `inference_pipe`
- adding inference logic with Ultralytics models
- writing post-processing / business logic
- optionally extending the frontend styling

## Install

Install all dependencies in one step:

```bash
pip install -r requirements.txt
```

To set up the documentation site, install the Node dependencies as well:

```bash
npm install
```

## Run

Start the app from the project root:

```bash
python main.py
```

Then open:

```text
http://127.0.0.1:8000
```

## Student Workflow

1. Install dependencies with `pip install -r requirements.txt`.
2. Run `python main.py`.
3. Open the browser at `http://127.0.0.1:8000`.
4. Edit the student hook files to implement your project logic.
5. Keep the frontend minimal unless you want to extend it.

## File Map

### Entry point
- `main.py`: starts the app with a single Python command.

### Backend runtime
- `app/server.py`: FastAPI app, webcam loop, WebSocket transport, startup logic.
- `app/protocol.py`: shared message and data shapes.
- `app/student_config.py`: student-facing constants and defaults.

### Student-edit files
- `app/student_pipeline.py`: defines `inference_pipe(frame)`.
- `app/student_logic.py`: placeholder business-logic helper functions.

### Frontend
- `frontend/index.html`: browser shell.
- `frontend/app.js`: WebSocket client and DOM updates.
- `frontend/style.css`: layout and styling.

### Tests
- `tests/test_smoke.py`: lightweight smoke test for imports and server startup.

## Runtime Contract

The backend exposes `inference_pipe(frame)` with this return shape:

```python
frame, detections, alerts, metadata
```

Where:
- `frame` is the annotated OpenCV frame
- `detections` is a list of plain dicts
- `alerts` is a list of plain dicts
- `metadata` is a dict left open for each student's project

The frontend displays:
- the annotated webcam feed in an `<img>` tag
- FPS
- model status
- alerts

## Model Status Values

The backend uses these `model_status` values:
- `loading`
- `live`
- `error`

If the webcam or model cannot start, the server stays up and the browser shows the error state.
