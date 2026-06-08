from __future__ import annotations

import asyncio
import json
import threading
import time
from dataclasses import dataclass, field
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
)
from app.student_pipeline import inference_pipe


BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

app = FastAPI()
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


@dataclass
class RuntimeState:
    latest_jpeg: bytes | None = None
    latest_alerts: list[dict[str, Any]] = field(default_factory=list)
    latest_metadata: dict[str, Any] = field(default_factory=dict)
    latest_fps: float = 0.0
    model_status: str = "loading"


_state_lock = threading.Lock()
_state = RuntimeState()
_shutdown = threading.Event()


def _get_state() -> dict[str, Any]:
    with _state_lock:
        return {
            "latest_jpeg": _state.latest_jpeg,
            "latest_alerts": list(_state.latest_alerts),
            "latest_metadata": dict(_state.latest_metadata),
            "latest_fps": _state.latest_fps,
            "model_status": _state.model_status,
        }


def _set_model_status(status: str) -> None:
    with _state_lock:
        _state.model_status = status


def _open_camera() -> cv2.VideoCapture | None:
    cap = cv2.VideoCapture(CAMERA_INDEX)
    if not cap.isOpened():
        return None
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
    return cap


def _encode_jpeg(frame: Any) -> bytes | None:
    success, encoded = cv2.imencode(
        ".jpg",
        frame,
        [int(cv2.IMWRITE_JPEG_QUALITY), JPEG_QUALITY],
    )
    if not success:
        return None
    return encoded.tobytes()


def _publish_state(
    *,
    jpeg: bytes,
    alerts: list[dict[str, Any]],
    metadata: dict[str, Any],
    fps: float,
) -> None:
    with _state_lock:
        _state.latest_jpeg = jpeg
        _state.latest_alerts = list(alerts)
        _state.latest_metadata = dict(metadata)
        _state.latest_fps = fps


def _capture_loop() -> None:
    cap = _open_camera()
    if cap is None:
        _set_model_status("error")
        return

    _set_model_status("live")

    last = time.perf_counter()
    while not _shutdown.is_set():
        ok, frame = cap.read()
        if not ok:
            _set_model_status("error")
            break
        annotated, _detections, alerts, metadata = inference_pipe(frame)
        now = time.perf_counter()
        fps = 1.0 / max(now - last, 1e-6)
        last = now
        jpeg = _encode_jpeg(annotated)
        if jpeg is None:
            continue
        _publish_state(jpeg=jpeg, alerts=alerts, metadata=metadata, fps=fps)
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
    try:
        while True:
            state = _get_state()
            await _send_status(websocket, state)
            await _send_alerts(websocket, state)
            if state["latest_jpeg"] is not None:
                await _send_frame(websocket, state["latest_jpeg"])
            await asyncio.sleep(0.03)
    except WebSocketDisconnect:
        return
    except Exception:
        await websocket.close()


async def _send_status(websocket: WebSocket, state: dict[str, Any]) -> None:
    await websocket.send_text(
        json.dumps(
            {
                "type": "status",
                "fps": state["latest_fps"],
                "model_status": state["model_status"],
            }
        )
    )


async def _send_alerts(websocket: WebSocket, state: dict[str, Any]) -> None:
    await websocket.send_text(json.dumps({"type": "alerts", "alerts": state["latest_alerts"]}))


async def _send_frame(websocket: WebSocket, jpeg: bytes) -> None:
    await websocket.send_bytes(jpeg)


def run() -> None:
    uvicorn.run("app.server:app", host="127.0.0.1", port=8000, reload=False)
