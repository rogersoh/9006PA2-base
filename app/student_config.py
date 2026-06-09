from __future__ import annotations

# Config values for app

CAMERA_INDEX = 0       # Server opens camera stream using cv2.VideoCapture(CAMERA_INDEX)
FRAME_WIDTH = 1280
FRAME_HEIGHT = 720
JPEG_QUALITY = 80

# Config values for websocket exponential backoff
WEBSOCKET_BACKOFF_START_SECONDS = 0.25
WEBSOCKET_BACKOFF_MAX_SECONDS = 5.0
