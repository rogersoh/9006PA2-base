---
title: Getting Started
description: Quick setup and first run steps for students working on the CV project.
---

## Quick Start

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Start the app:

```bash
python main.py
```

3. Open the browser at:

```text
http://127.0.0.1:8000
```

## What To Edit

Start with the student-facing files:

- `app/student_pipeline.py`
- `app/student_logic.py`
- `app/student_config.py`

## What To Expect

- The app uses a live webcam feed.
- The browser shows the latest annotated frame.
- `inference_pipe(frame)` is the main place to add model logic.
- Alerts and metadata are streamed to the frontend as part of the runtime state.

## Keep In Sync

If you change the runtime contract, update these docs too:

- [`App Architecture`](./architecture)
- [`inference_pipe` Contract](./inference-pipe)
