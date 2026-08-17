from __future__ import annotations

# Config values for app

CAMERA_INDEX = 0       # Server opens camera stream using cv2.VideoCapture(CAMERA_INDEX)
FRAME_WIDTH = 1280
FRAME_HEIGHT = 720
JPEG_QUALITY = 80

# Path to the trained YOLO model weights.
# Update this if best.pt lives somewhere else (e.g. "runs/detect/train/weights/best.pt").
MODEL_PATH = "best.onnx" # onnx format

# Minimum confidence for a YOLO detection to be kept.
CONFIDENCE_THRESHOLD = 0.45

# Banana ripeness classes the model was trained on.
RIPENESS_CLASSES = ["overripe", "ripe", "rotten", "unripe"]

# Alert severity per ripeness class.
RIPENESS_SEVERITY = {
    "unripe": "low",
    "ripe": "low",
    "overripe": "medium",
    "rotten": "high",
}

# Box colors (BGR, for cv2) per ripeness class, used when annotating frames.
RIPENESS_COLORS = {
    "unripe": (0, 200, 0),      # green
    "ripe": (0, 215, 255),      # yellow/gold
    "overripe": (0, 140, 255),  # orange
    "rotten": (0, 0, 255),      # red
}

# Config values for websocket exponential backoff
WEBSOCKET_BACKOFF_START_SECONDS = 0.25
WEBSOCKET_BACKOFF_MAX_SECONDS = 5.0
