from __future__ import annotations

from pathlib import Path
from typing import Iterable

import psutil

from watchserver.models.metrics import DiskMetrics, DiskUsage


def collect_disk_metrics(paths: Iterable[str]) -> DiskMetrics:
    filesystems = [_collect_disk_usage(path) for path in paths]
    return DiskMetrics(filesystems=filesystems)


def _collect_disk_usage(path_value: str) -> DiskUsage:
    path = Path(path_value)

    if not path.exists():
        return DiskUsage(
            path=str(path),
            total_bytes=None,
            used_bytes=None,
            free_bytes=None,
            percent_used=None,
            error="path does not exist",
        )

    try:
        usage = psutil.disk_usage(str(path))
    except (OSError, RuntimeError) as exc:
        return DiskUsage(
            path=str(path),
            total_bytes=None,
            used_bytes=None,
            free_bytes=None,
            percent_used=None,
            error=f"disk usage unavailable: {exc}",
        )

    return DiskUsage(
        path=str(path),
        total_bytes=usage.total,
        used_bytes=usage.used,
        free_bytes=usage.free,
        percent_used=usage.percent,
        error=None,
    )
