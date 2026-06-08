from __future__ import annotations

from typing import Any, Literal, TypedDict


class Detection(TypedDict, total=False):
    label: str
    confidence: float
    bbox: list[int]
    track_id: int


class Alert(TypedDict, total=False):
    type: str
    message: str
    severity: Literal["low", "medium", "high"]
    source_detection: Detection


class StatusMessage(TypedDict):
    type: Literal["status"]
    fps: float
    model_status: Literal["loading", "live", "error"]


class AlertsMessage(TypedDict):
    type: Literal["alerts"]
    alerts: list[Alert]


class MetadataMessage(TypedDict):
    type: Literal["metadata"]
    metadata: dict[str, Any]
