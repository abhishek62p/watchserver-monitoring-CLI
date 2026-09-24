from __future__ import annotations

from datetime import datetime, timezone
from typing import Iterable

from watchserver.collectors.cpu import collect_cpu_metrics
from watchserver.collectors.disk import collect_disk_metrics
from watchserver.collectors.memory import collect_memory_metrics
from watchserver.collectors.system import collect_system_metrics
from watchserver.models.metrics import ServerSnapshot


DEFAULT_DISK_PATHS = ("/",)


def collect_phase1_snapshot(disk_paths: Iterable[str] = DEFAULT_DISK_PATHS) -> ServerSnapshot:
    """Collect the Phase 1 metric set: system, CPU, memory, and disk."""

    return ServerSnapshot(
        timestamp=datetime.now(timezone.utc),
        system=collect_system_metrics(),
        cpu=collect_cpu_metrics(),
        memory=collect_memory_metrics(),
        disk=collect_disk_metrics(disk_paths),
    )
