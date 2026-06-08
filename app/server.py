from __future__ import annotations

import asyncio
import json
import threading
import time
from pathlib import Path
from typing import Any

import cv2
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.student_config import (
    CAMERA_INDEX,
    FRAME_HEIGHT,
    FRAME_WIDTH,
    JPEG_QUALITY,
    WEBSOCKET_BACKOFF_MAX_SECONDS,
    WEBSOCKET_BACKOFF_START_SECONDS,
)
from app.student_pipeline import inference_pipe


BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

app = FastAPI()
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

_state_lock = threading.Lock()
_latest_frame = None
_latest_jpeg: bytes | None = None
_latest_alerts: list[dict[str, Any]] = []
_latest_metadata: dict[str, Any] = {}
_latest_fps = 0.0
_model_status = "loading"
_shutdown = threading.Event()


def _set_state(**kwargs: Any) -> None:
    global _latest_frame, _latest_jpeg, _latest_alerts, _latest_metadata, _latest_fps, _model_status
    with _state_lock:
        for key, value in kwargs.items():
            globals()[f"_{key}"] = value


def _get_state() -> dict[str, Any]:
    with _state_lock:
        return {
            "latest_jpeg": _latest_jpeg,
            "latest_alerts": list(_latest_alerts),
            "latest_metadata": dict(_latest_metadata),
            "latest_fps": _latest_fps,
            "model_status": _model_status,
        }


def _set_model_status(status: str) -> None:
    global _model_status
    with _state_lock:
        _model_status = status


def _capture_loop() -> None:
    cap = cv2.VideoCapture(CAMERA_INDEX)
    if not cap.isOpened():
        _set_model_status("error")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
    _set_model_status("live")

    last = time.perf_counter()
    while not _shutdown.is_set():
        ok, frame = cap.read()
        if not ok:
            _set_model_status("error")
            break
        annotated, detections, alerts, metadata = inference_pipe(frame)
        now = time.perf_counter()
        fps = 1.0 / max(now - last, 1e-6)
        last = now
        success, encoded = cv2.imencode(
            ".jpg",
            annotated,
            [int(cv2.IMWRITE_JPEG_QUALITY), JPEG_QUALITY],
        )
        if not success:
            continue
        with _state_lock:
            global _latest_frame, _latest_jpeg, _latest_alerts, _latest_metadata, _latest_fps
            _latest_frame = frame
            _latest_jpeg = encoded.tobytes()
            _latest_alerts = list(alerts)
            _latest_metadata = dict(metadata)
            _latest_fps = fps
        time.sleep(0.001)

    cap.release()


@app.on_event("startup")
async def on_startup() -> None:
    threading.Thread(target=_capture_loop, daemon=True).start()


@app.get("/")
def index() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    await websocket.accept()
    backoff = WEBSOCKET_BACKOFF_START_SECONDS
    try:
        while True:
            state = _get_state()
            await websocket.send_text(
                json.dumps(
                    {
                        "type": "status",
                        "fps": state["latest_fps"],
                        "model_status": state["model_status"],
                    }
                )
            )
            await websocket.send_text(
                json.dumps({"type": "alerts", "alerts": state["latest_alerts"]})
            )
            if state["latest_jpeg"] is not None:
                await websocket.send_bytes(state["latest_jpeg"])
            await asyncio.sleep(0.03)
            backoff = WEBSOCKET_BACKOFF_START_SECONDS
    except WebSocketDisconnect:
        return
    except Exception:
        await websocket.close()


def run() -> None:
    uvicorn.run("app.server:app", host="127.0.0.1", port=8000, reload=False)
