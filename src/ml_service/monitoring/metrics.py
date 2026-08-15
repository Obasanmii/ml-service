from __future__ import annotations

from collections import deque
from threading import Lock

import numpy as np


class Metrics:
    def __init__(self, window: int = 1000) -> None:
        self._latencies_ms: deque[float] = deque(maxlen=window)
        self._total = 0
        self._server_errors = 0
        self._lock = Lock()

    def record(self, duration_ms: float, status_code: int) -> None:
        with self._lock:
            self._latencies_ms.append(duration_ms)
            self._total += 1
            if status_code >= 500:
                self._server_errors += 1

    def snapshot(self) -> dict:
        with self._lock:
            latencies = list(self._latencies_ms)
            total = self._total
            errors = self._server_errors
        if latencies:
            arr = np.array(latencies)
            latency = {
                "p50_ms": round(float(np.percentile(arr, 50)), 2),
                "p95_ms": round(float(np.percentile(arr, 95)), 2),
                "p99_ms": round(float(np.percentile(arr, 99)), 2),
            }
        else:
            latency = {"p50_ms": 0.0, "p95_ms": 0.0, "p99_ms": 0.0}
        return {
            "total_requests": total,
            "server_errors": errors,
            "window_size": len(latencies),
            "latency_ms": latency,
        }


metrics = Metrics()
