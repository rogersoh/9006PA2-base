from __future__ import annotations

import socket
import subprocess
import sys
import time
from pathlib import Path
from urllib.request import urlopen


ROOT = Path(__file__).resolve().parent.parent


def test_modules_import() -> None:
    for module in [
        "app.protocol",
        "app.student_config",
        "app.student_logic",
        "app.student_pipeline",
        "app.server",
    ]:
        __import__(module)


def test_server_starts() -> None:
    proc = subprocess.Popen(
        [sys.executable, "main.py"],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        for _ in range(60):
            if proc.poll() is not None:
                raise AssertionError("server exited before becoming ready")
            try:
                with socket.create_connection(("127.0.0.1", 8000), timeout=0.2):
                    break
            except OSError:
                time.sleep(0.5)
        with urlopen("http://127.0.0.1:8000/health", timeout=2) as response:
            assert response.status == 200
    finally:
        proc.terminate()
        proc.wait(timeout=10)
