from __future__ import annotations

import psutil

from watchserver.models.metrics import MemoryMetrics


def collect_memory_metrics() -> MemoryMetrics:
    errors: list[str] = []

    try:
        virtual_memory = psutil.virtual_memory()
        total = virtual_memory.total
        available = virtual_memory.available
        used = virtual_memory.used
        percent_used = virtual_memory.percent
    except (OSError, RuntimeError) as exc:
        total = available = used = percent_used = None
        errors.append(f"virtual memory unavailable: {exc}")

    try:
        swap = psutil.swap_memory()
        swap_total = swap.total
        swap_used = swap.used
        swap_percent_used = swap.percent
    except (OSError, RuntimeError) as exc:
        swap_total = swap_used = swap_percent_used = None
        errors.append(f"swap memory unavailable: {exc}")

    return MemoryMetrics(
        total_bytes=total,
        available_bytes=available,
        used_bytes=used,
        percent_used=percent_used,
        swap_total_bytes=swap_total,
        swap_used_bytes=swap_used,
        swap_percent_used=swap_percent_used,
        errors=errors,
    )
